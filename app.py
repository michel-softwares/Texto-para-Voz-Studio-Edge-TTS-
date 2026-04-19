import asyncio
import edge_tts
import flet as ft
import os
import re
import json
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES E CONSTANTES
# ==========================================
LIMIT_CHARS = 999
CONFIG_FILE = "config.json"
LOGO_PATH = "logoMichelSoftwares.png"

# Paleta de Cores "Clean White"
COLOR_PRIMARY = "#2b63e1"
COLOR_BG = "#f5f6f7"
COLOR_CARD = "#ffffff"
COLOR_TEXT_MAIN = "#2d3436"
COLOR_TEXT_SECONDARY = "#636e72"

# Removido suporte a emoção pois a API gratuita do Edge não suporta SSML com express-as

def split_text(text, max_chars=LIMIT_CHARS):
    if len(text) <= max_chars:
        return [text.strip()] if text.strip() else []
        
    chunks = []
    text = text.strip()
    
    while len(text) > max_chars:
        chunk = text[:max_chars]
        
        # 1. Prioridade máxima: Final de frase
        cut_index = -1
        for punct in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
            idx = chunk.rfind(punct)
            if idx > cut_index:
                cut_index = idx + 1 # Corta DEPOIS da pontuação

        # 2. Se não achou, tenta vírgula, dois pontos, ponto e vírgula
        if cut_index <= 0:
            for punct in [', ', '; ', ': ', ',\n', ';\n', ':\n']:
                idx = chunk.rfind(punct)
                if idx > cut_index:
                    cut_index = idx + 1

        # 3. Se não achou, tenta espaço ou quebra de linha normal
        if cut_index <= 0:
            for punct in [' ', '\n']:
                idx = chunk.rfind(punct)
                if idx > cut_index:
                    cut_index = idx + 1
        
        # 4. Corte bruto se for uma palavra gigante sem espaços
        if cut_index <= 0:
            cut_index = max_chars
            
        chunks.append(text[:cut_index].strip())
        text = text[cut_index:].strip()

    if text:
        chunks.append(text)
        
    return chunks

# ==========================================
# GESTÃO DE CONFIGURAÇÕES
# ==========================================
def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except: pass

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except: return {}

def get_unique_filename(filename, folder="Meus Áudios"):
    """Retorna um nome de arquivo único adicionando (1), (2), etc se necessário."""
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        return filepath
        
    name, ext = os.path.splitext(filename)
    counter = 1
    while True:
        new_name = f"{name} ({counter}){ext}"
        new_filepath = os.path.join(folder, new_name)
        if not os.path.exists(new_filepath):
            return new_filepath
        counter += 1

# ==========================================
# INTERFACE PRINCIPAL
# ==========================================
async def main(page: ft.Page):
    page.title = "Texto para Voz Studio | Edge-TTS"
    page.window.icon = "mic_icon.ico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLOR_BG
    page.padding = 10
    page.window.width = 540
    page.window.height = 850
    page.window.min_width = 480
    page.window.max_width = 660
    page.window.resizable = True
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Estados
    current_chunks = []
    all_voices = []
    saved_config = load_config()
    
    # Componentes UI
    text_input = ft.TextField(
        label="Texto para narração",
        hint_text="Cole seu texto aqui...",
        multiline=True,
        min_lines=6,
        max_lines=10,
        border_radius=10,
        border_color="#dfe6e9",
        focused_border_color=COLOR_PRIMARY,
        bgcolor=COLOR_CARD,
        on_change=lambda e: update_info(e)
    )

    char_counter = ft.Text("0 caracteres | 0 partes", color=COLOR_TEXT_SECONDARY, size=11)
    
    voice_dropdown = ft.Dropdown(
        label="Escolha a Voz",
        options=[],
        border_radius=10,
        border_color="#dfe6e9",
        focused_border_color=COLOR_PRIMARY,
        bgcolor=COLOR_CARD,
    )



    def create_slider(label, min_val, max_val, initial, unit=""):
        val_text = ft.Text(f"{int(initial):+d}{unit}", size=11, color=COLOR_TEXT_SECONDARY)
        return ft.Column([
            ft.Row([
                ft.Text(label, size=12, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_MAIN),
                val_text
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Slider(
                min=min_val, max=max_val, value=initial,
                active_color=COLOR_PRIMARY,
                on_change=lambda e: update_slider_text(e, val_text, unit)
            )
        ], spacing=0)

    def update_slider_text(e, text_control, unit):
        text_control.value = f"{int(e.control.value):+d}{unit}"
        page.update()

    speed_slider_box = create_slider("Velocidade", -100, 100, saved_config.get("speed", 0), "%")
    volume_slider_box = create_slider("Volume", -100, 100, saved_config.get("volume", 0), "%")
    pitch_slider_box = create_slider("Tom", -100, 100, saved_config.get("pitch", 0), "Hz")

    def toggle_final_name(e):
        final_name_input.visible = merge_switch.value
        page.update()

    merge_switch = ft.Switch(
        label="Unir arquivos em um só", 
        value=saved_config.get("merge", True),
        active_color=COLOR_PRIMARY,
        on_change=toggle_final_name
    )

    final_name_input = ft.TextField(
        label="Nome do Arquivo Unido",
        value="audio_completo",
        dense=True,
        border_radius=8,
        visible=saved_config.get("merge", True)
    )
    
    track_names_list = ft.Column(spacing=10)
    
    status_text = ft.Text("", weight=ft.FontWeight.W_500, size=12, text_align=ft.TextAlign.CENTER)
    progress_bar = ft.ProgressBar(color=COLOR_PRIMARY, bgcolor="#eee", visible=False, border_radius=5)

    logo = ft.Image(src=LOGO_PATH, width=120, height=50)

    async def fetch_voices():
        nonlocal all_voices
        status_text.value = "🔄 Carregando vozes..."
        page.update()
        try:
            voices = await edge_tts.list_voices()
            all_voices = [v for v in voices if "pt-BR" in v["Locale"]]
            voice_dropdown.options = [
                ft.dropdown.Option(key=v["ShortName"], text=f"{v['FriendlyName'].split(' - ')[0]} ({'H' if v['Gender'] == 'Male' else 'M'})")
                for v in all_voices
            ]
            saved_voice = saved_config.get("voice")
            if saved_voice and any(v["ShortName"] == saved_voice for v in all_voices):
                voice_dropdown.value = saved_voice
            elif all_voices:
                voice_dropdown.value = all_voices[0]["ShortName"]
            status_text.value = "✅ Sistema Pronto"
            status_text.color = ft.Colors.GREEN_600
        except:
            status_text.value = "⚠️ Erro de conexão"
            status_text.color = ft.Colors.RED_600
        page.update()

    def update_info(e):
        text = text_input.value
        chunks = split_text(text)
        nonlocal current_chunks
        current_chunks = chunks
        char_counter.value = f"{len(text)} caracteres | {len(chunks)} parte(s)"
        track_names_list.controls.clear()
        for i in range(len(chunks)):
            track_names_list.controls.append(
                ft.TextField(label=f"Nome Parte {i+1}", value=f"audio_{i+1}" if len(chunks) > 1 else "meu_audio", dense=True, border_radius=8)
            )
        page.update()

    async def start_conversion(e):
        if not text_input.value.strip(): return
        
        save_config({
            "voice": voice_dropdown.value, "speed": speed_slider_box.controls[1].value,
            "volume": volume_slider_box.controls[1].value, "pitch": pitch_slider_box.controls[1].value, 
            "merge": merge_switch.value
        })
        
        progress_bar.visible = True
        btn_convert.disabled = True
        status_text.value = "🎙️ Convertendo..."
        page.update()

        try:
            chunks = split_text(text_input.value)
            file_names = [c.value for c in track_names_list.controls]
            temp_files = []
            
            rate = f"{int(speed_slider_box.controls[1].value):+d}%"
            volume = f"{int(volume_slider_box.controls[1].value):+d}%"
            pitch = f"{int(pitch_slider_box.controls[1].value):+d}Hz"
            
            for i, chunk in enumerate(chunks):
                name = file_names[i] if i < len(file_names) else f"pt_{i}"
                if not name.lower().endswith(".mp3"): name += ".mp3"
                name = get_unique_filename(name)
                
                status_text.value = f"Processando: {name} ({i+1}/{len(chunks)})"
                page.update()
                
                c = edge_tts.Communicate(chunk, voice=voice_dropdown.value, 
                                        rate=rate, volume=volume, pitch=pitch)
                
                await c.save(name)
                temp_files.append(name)

            if merge_switch.value and len(temp_files) > 1:
                fn = final_name_input.value.strip() if final_name_input.value.strip() else "audio_completo"
                if not fn.lower().endswith(".mp3"): fn += ".mp3"
                fn = get_unique_filename(fn)
                with open(fn, 'wb') as out_f:
                    for f in temp_files:
                        with open(f, 'rb') as in_f: out_f.write(in_f.read())
                        os.remove(f)
                status_text.value = f"✅ Finalizado: {fn}"
            else:
                status_text.value = f"✅ {len(temp_files)} arquivos criados!"
        except Exception as ex:
            status_text.value = f"❌ Erro: {ex}"
        
        progress_bar.visible = False
        btn_convert.disabled = False
        page.update()

    btn_convert = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED), ft.Text("INICIAR CONVERSÃO", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=COLOR_PRIMARY, padding=25, shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=start_conversion,
    )

    # Layout Vertical Requisitado
    content = ft.Column([
        ft.Row([
            ft.Image(src="mic_icon.png", width=35, height=35),
            ft.Column([
                ft.Text("Texto para Voz Studio | Edge-TTS", size=18, weight=ft.FontWeight.BOLD),
            ], spacing=0)
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Divider(height=10, color="transparent"),
        
        ft.Container(
            content=ft.Column([
                text_input,
                ft.Row([char_counter], alignment=ft.MainAxisAlignment.END),
                
                ft.Divider(height=10, color="#f1f2f6"),
                
                voice_dropdown,
                speed_slider_box,
                volume_slider_box,
                pitch_slider_box,
                
                ft.Row([merge_switch], alignment=ft.MainAxisAlignment.CENTER),
                final_name_input,
                
                ft.Divider(height=10, color="#f1f2f6"),
                
                ft.Text("Nomes dos arquivos:", size=12, weight=ft.FontWeight.BOLD),
                track_names_list,
                
                ft.Divider(height=10, color="transparent"),
                btn_convert,
                ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
                progress_bar,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            padding=15,
            bgcolor=COLOR_CARD,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        ),
        
        ft.Divider(height=20, color="transparent"),
        ft.Row([
            ft.Text("Software desenvolvido por", size=10, color=COLOR_TEXT_SECONDARY),
            logo
        ], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Container(content=content, expand=True))
    
    await fetch_voices()
    update_info(None)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

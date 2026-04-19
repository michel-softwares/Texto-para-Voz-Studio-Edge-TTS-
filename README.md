<div align="center">
  <img src="assets/mic_icon.png" alt="Microfone Icon" width="120" />

  # Texto para Voz Studio | Edge-TTS

  ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
  ![Flet](https://img.shields.io/badge/Flet-GUI-teal?style=for-the-badge)
  ![Edge-TTS](https://img.shields.io/badge/Edge--TTS-API-orange?style=for-the-badge)
  ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
  ![Windows](https://img.shields.io/badge/OS-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

  <br />

  *Um aplicativo simples e direto ao ponto para converter textos longos em áudio de alta qualidade gratuitamente, usando a tecnologia neural da Microsoft.*
  
  **Interface Gráfica (GUI) desenvolvida por Michel Softwares**
</div>

<br />

> ⚠️ **IMPORTANTE:** O motor por trás de toda a geração de voz deste aplicativo é o projeto **[edge-tts](https://github.com/rany2/edge-tts)** criado por [rany2](https://github.com/rany2). Todo o crédito da comunicação com a API da Microsoft pertence a ele.

---

## ⚙️ Funcionalidades

- **Corte Automático:** Divide textos longos para não travar o limite da API. A API tem um limite de 1000 caracteres, se você digitar um texto maior que 1000 caracteres a aplicação irá dividí-lo automaticamente para garantir que todo o texto seja narrado.
- **Unificador de Áudio:** Junta todas as partes automaticamente em um único arquivo `.mp3`. A partes dividas serão unidas ao final, se assim você quiser.
- **Ajustes:** Pequeno menu para mudar Velocidade, Volume e Tom da narração.
- **Vozes:** A vozes Pt-br disponíveis são pt-BR-AntonioNeural, pt-BR-FranciscaNeural e ThalitaMultilingual.
---

## 📦 Requisitos e Instalação

Você precisa ter o **[Python](https://www.python.org/downloads/)** e o **[Node.js](https://nodejs.org/)** instalados no seu computador. 

*(**Dica:** Durante a instalação do Python, é muito importante marcar a caixinha **"Add python.exe to PATH"** na primeira tela).*

1. Baixe os arquivos do projeto:
   - No topo desta página do GitHub, clique no botão verde escrito **"<> Code"**.
   - No menuzinho que abrir, clique em **"Download ZIP"**.
   - Encontre o arquivo baixado no seu computador, clique com o botão direito sobre ele e escolha **"Extrair Tudo..."**.
2. Abra a pasta que você acabou de extrair, clique na barra de endereços (lá em cima), digite `cmd` e aperte Enter. Isso abrirá o terminal.
3. No terminal, instale as bibliotecas necessárias para a interface gráfica e a geração de voz (Python):

```bash
pip install flet edge-tts
```

*(**Nota:** O pacote `edge-tts` instalado neste comando é a biblioteca oficial que se comunica com a API da Microsoft. Em caso de dúvidas sobre as vozes, problemas de rede ou erros na geração de áudio, consulte a documentação oficial do **[projeto edge-tts no GitHub](https://github.com/rany2/edge-tts)**).*

Em seguida, instale as dependências visuais para o script de inicialização do terminal (Node.js):

```bash
npm install figlet gradient-string
```

---

## 🚀 Como Usar

Não é necessário rodar códigos no terminal para usar o programa no dia a dia.
Basta dar um duplo clique no arquivo **`INICIAR.bat`**.

Ele abrirá uma janela de terminal estilizada e, em seguida, a interface gráfica do aplicativo. Todos os áudios gerados serão salvos em uma pasta chamada `Meus Áudios`.

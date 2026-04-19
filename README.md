# Texto para Voz Studio | Edge-TTS

Um aplicativo simples e direto ao ponto para converter textos longos em áudio de alta qualidade gratuitamente, usando a tecnologia neural da Microsoft.

Este projeto é uma **Interface Gráfica (GUI)** desenvolvida por **Michel Softwares**. 

> ⚠️ **IMPORTANTE:** O motor por trás de toda a geração de voz deste aplicativo é o projeto **[edge-tts](https://github.com/rany2/edge-tts)** criado por [rany2](https://github.com/rany2). Todo o crédito da comunicação com a API da Microsoft pertence a ele.

---

## ⚙️ Funcionalidades

- **Corte Automático:** Divide textos longos para não travar o limite da API.
- **Unificador de Áudio:** Junta todas as partes automaticamente em um único arquivo `.mp3`.
- **Ajustes:** Barras deslizantes para mudar Velocidade, Volume e Tom.

---

## 📦 Requisitos e Instalação

Você precisa ter o **Python** e o **Node.js** instalados no seu computador.

1. Baixe os arquivos desta pasta.
2. Abra o terminal na pasta e instale as dependências executando:

\`\`\`bash
pip install -r requirements.txt
npm install
\`\`\`

*(Nota: O comando `pip` acima instalará automaticamente o Flet para a interface e a biblioteca original `edge-tts` do rany2).*

---

## 🚀 Como Usar

Não é necessário rodar códigos no terminal para usar o programa no dia a dia.
Basta dar um duplo clique no arquivo **`INICIAR.bat`**.

Ele abrirá uma janela de terminal estilizada e, em seguida, a interface gráfica do aplicativo. Todos os áudios gerados serão salvos em uma pasta chamada `Meus Áudios`.

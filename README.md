# Texto para Voz Studio | Edge-TTS

Um aplicativo simples e direto ao ponto para converter textos longos em áudio de alta qualidade gratuitamente, usando a tecnologia neural da Microsoft.

Este projeto é uma **Interface Gráfica (GUI)** desenvolvida por **Michel Softwares**. 

> ⚠️ **IMPORTANTE:** O motor por trás de toda a geração de voz deste aplicativo é o projeto **[edge-tts](https://github.com/rany2/edge-tts)** criado por [rany2](https://github.com/rany2). Todo o crédito da comunicação com a API da Microsoft pertence a ele.

---

## ⚙️ Funcionalidades

- **Corte Automático:** Divide textos longos para não travar o limite da API. A API tem um limite de 1000 caracteres, se você digitar um texto maior que 1000 caracteres a aplicação irá dividí-lo automaticamente para garantir que todo o texto seja narrado.
- **Unificador de Áudio:** Junta todas as partes automaticamente em um único arquivo `.mp3`. A partes dividas serão unidas ao final, se assim você quiser.
- **Ajustes:** Pequeno menu para mudar Velocidade, Volume e Tom da narração.
- **Vozes:** A vozes Pt-br disponíveis são pt-BR-AntonioNeural, pt-BR-FranciscaNeural e ThalitaMultilingual.
---

## 📦 Requisitos e Instalação

Você precisa ter o **Python** e o **Node.js** instalados no seu computador.

1. Baixe os arquivos desta pasta.
2. Abra o terminal na pasta e instale as bibliotecas necessárias para a interface gráfica e a geração de voz (Python):

```bash
pip install flet edge-tts
```

Em seguida, instale as dependências visuais para o script de inicialização do terminal (Node.js):

```bash
npm install figlet gradient-string
```

---

## 🚀 Como Usar

Não é necessário rodar códigos no terminal para usar o programa no dia a dia.
Basta dar um duplo clique no arquivo **`INICIAR.bat`**.

Ele abrirá uma janela de terminal estilizada e, em seguida, a interface gráfica do aplicativo. Todos os áudios gerados serão salvos em uma pasta chamada `Meus Áudios`.

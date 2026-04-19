@echo off
setlocal
chcp 65001 > nul
title Texto para Voz Studio ^| Edge-TTS
color 0b

cls
echo.
echo  Iniciando Texto para Voz Studio ^| Edge-TTS, aguarde um momento...
echo.

:: Exibe a assinatura profissional via Node.js
node scripts/signature.js

:: Inicia a aplica??o principal
start "" pythonw "%~dp0app.py"

:: Mantem o terminal aberto por 5 segundos e fecha
timeout /t 5 /nobreak > nul
exit /b

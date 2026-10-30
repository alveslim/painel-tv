@echo off
REM Abre o painel local em tela cheia (modo quiosque) para a TV.
REM Funciona de qualquer pasta: sobe uma pasta a partir deste script (raiz do projeto).
cd /d "%~dp0.."
start "" python app.py
timeout /t 3
start chrome --kiosk "http://127.0.0.1:5000" --edge-kiosk-type=fullscreen

# Prepara o ambiente de desenvolvimento (Windows / PowerShell).
# Uso: powershell -ExecutionPolicy Bypass -File scripts\install_windows.ps1
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path -Path "venv")) {
    Write-Host "Criando ambiente virtual (venv)..." -ForegroundColor Yellow
    python -m venv venv
}

.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\pip.exe install -r requirements-dev.txt

# Gera a planilha fictícia de demonstração, se ainda não existir
if (-not (Test-Path -Path "dados\dados_mock.xlsx")) {
    .\venv\Scripts\python.exe scripts\gerar_dados_demo.py
}

Write-Host "Instalação concluída. Rode: python app.py" -ForegroundColor Green

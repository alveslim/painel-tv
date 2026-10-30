#!/usr/bin/env bash
# Prepara o ambiente de desenvolvimento (Linux/macOS).
# Uso: bash scripts/install_linux_mac.sh
set -e
cd "$(dirname "$0")/.."

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual (venv)..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt

# Gera a planilha fictícia de demonstração, se ainda não existir
[ -f dados/dados_mock.xlsx ] || python scripts/gerar_dados_demo.py

echo "Instalação concluída. Rode: python app.py"

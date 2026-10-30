<p align="center">
<h1 align="center">📊 Smart Dashboard & Sync Bot (Indústria 4.0)</h1>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python"></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-Web_App-black?logo=flask" alt="Flask"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-Data_Processing-150458?logo=pandas" alt="Pandas"></a>
  <a href="https://plotly.com/"><img src="https://img.shields.io/badge/Plotly-Data_Viz-3F4F75?logo=plotly" alt="Plotly"></a>
<br>

Sistema completo de monitoramento em tempo real desenvolvido para painéis de TV em ambientes de fábrica (Chão de Fábrica e Gestão). O projeto consiste em uma arquitetura robusta de dois nós: um robô sincronizador local (ETL) e uma aplicação Web Dashboard responsiva na nuvem.

---

## 📸 Demonstração do Sistema

### Visão Geral do Painel (TV)
<!-- Arraste a imagem da TV aq e dx o link que o gitHub gerar nesta linha -->


### Sistema em Ação

<table align="center">
  <tr>
    <th align="center"> Funcionamento </th>
    <th align="center"> Aplicação real </th>
  </tr>
  <tr>
    <td align="center" width="50%">
      <video src="https://github.com/user-attachments/assets/1a16dbd7-6d2b-4d27-90de-a6ace0948520" controls width="100%"></video>
    </td>
    <td align="center" width="50%">
      <!-- Quando tiver o vídeo do celular, substitua o link falso abaixo pelo real -->
      <img width="1200" height="1600" alt="WhatsApp Image 2026-08-19 at 13 02 17" src="https://github.com/user-attachments/assets/8351d8d9-d914-43ca-b808-479ebf682ab2" />"
    </td>
  </tr>
</table>

## 🧠 Arquitetura e Fluxo de Dados

O diagrama abaixo ilustra como o dado sai da operação, é higienizado e chega aos painéis em tempo real.

```mermaid
graph TD
    subgraph Fabrica [Rede Local - Fábrica]
        E[(Planilha Excel<br>Samba/Rede)]
        R[🤖 Robô Sincronizador<br>Python / Pandas]
        
        E -->|Lê e Higieniza Dados| R
    end

    subgraph Nuvem [Nuvem - Render]
        A{API REST<br>Flask}
        D[Dashboard Web<br>HTML / JS / Plotly]
        
        R -->|POST JSON - Atualiza a cada 5 min| A
        A <--> D
    end

    subgraph Usuarios [Usuários Finais]
        T[📺 TV 16:9<br>Chão de Fábrica]
        C[📱 Mobile<br>Gestão Financeira]
        
        D -->|Visualização Autônoma| T
        D -->|Visualização Interativa| C
    end
    
    style R fill:#2563eb,stroke:#fff,stroke-width:2px,color:#fff
    style A fill:#10b981,stroke:#fff,stroke-width:2px,color:#fff


## 🚀 Como rodar a demonstração

> Esta é a **versão pública de demonstração**: usa dados 100% fictícios e credenciais de teste (`admin` / `admin`). A versão adaptada ao uso em empresa não faz parte deste repositório.

```bash
# 1. Instalar dependências (Linux/macOS: bash scripts/install_linux_mac.sh | Windows: scripts\install_windows.ps1)
pip install -r requirements-dev.txt

# 2. Gerar a planilha fictícia (datas relativas a hoje) em dados/dados_mock.xlsx
python scripts/gerar_dados_demo.py

# 3. Subir o painel e, em outro terminal, o robô sincronizador
python app.py
python sicronizador.py
```

Abra `http://127.0.0.1:5000` (TV) ou `http://127.0.0.1:5000/gestao` (gestão). Também funciona com Docker: `docker build -t painel-tv . && docker run -p 5000:5000 painel-tv`.

## 🧪 Testes

```bash
pytest
```

Os testes cobrem o login, a renderização das telas, a API `/api/sync` e as funções de tratamento de dados e gráficos. O workflow em `.github/workflows/python-app.yml` roda o `flake8` e o `pytest` a cada push e pull request.

## 📁 Estrutura

```
├── app.py                  # Painel web (Flask) + API /api/sync
├── sicronizador.py         # Robô de demonstração (ETL)
├── services/data_service.py
├── templates/index.html    # Telas do painel
├── static/                 # CSS, JS, manifest e logo
├── dados/dados_mock.xlsx   # Dados fictícios de exemplo
├── scripts/                # Gerador de dados e instaladores
└── tests/                  # pytest
```

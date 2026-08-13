<div align="center">
  <!-- LOGO NO TOPO -->
  <!-- DICA: Se você salvou como logo.svg, mude a extensão abaixo -->
  <img src="static/images/logo.png" alt="Logo SyncBoard" width="300">

  # 📊 Smart Dashboard & Sync Bot (Indústria 4.0)

  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-Web_App-black?logo=flask)](https://flask.palletsprojects.com/)
  [![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?logo=pandas)](https://pandas.pydata.org/)
  [![Plotly](https://img.shields.io/badge/Plotly-Data_Viz-3F4F75?logo=plotly)](https://plotly.com/)
</div>

<br>

Sistema completo de monitoramento em tempo real desenvolvido para painéis de TV em ambientes de fábrica (Chão de Fábrica e Gestão). O projeto consiste em uma arquitetura robusta de dois nós: um robô sincronizador local (ETL) e uma aplicação Web Dashboard responsiva na nuvem.

---

## 📸 Demonstração do Sistema

### Visão Geral do Painel (TV)
<!-- PASSO 1 PARA A IMAGEM: 
Vá no site do GitHub, clique em "Editar" no arquivo README.md. 
Arraste e solte o seu print da tela aqui embaixo. O GitHub vai gerar um link automático. Apague este comentário. -->
![Coloque sua Imagem Aqui]()

### Sistema em Ação
<!-- PASSO 2 PARA OS VÍDEOS: 
Arraste e solte os seus vídeos (MP4 ou GIF) aqui embaixo enquanto estiver editando no GitHub. -->
| 📺 Modo TV (Auto-Play e Pausa) | 📱 Modo Celular (Gestão) |
| :---: | :---: |
| *(Arraste seu vídeo 1 aqui)* | *(Arraste seu vídeo 2 aqui)* |

---

## 🧠 Arquitetura e Fluxo de Dados

O diagrama abaixo ilustra como o dado sai da operação, é higienizado e chega aos painéis em tempo real.

```mermaid
graph TD
    subgraph Rede Local (Fábrica)
        E[(Planilha Excel<br>Samba/Rede)]
        R[🤖 Robô Sincronizador<br>Python / Pandas]
        
        E -->|Lê e Higieniza Dados| R
    end

    subgraph Nuvem (Render / AWS)
        A{API REST<br>Flask}
        D[Dashboard Web<br>HTML / JS / Plotly]
        
        R == POST JSON ==>|Atualiza a cada 5 min| A
        A <--> D
    end

    subgraph Usuários Finais
        T[📺 TV 16:9<br>Chão de Fábrica]
        C[📱 Mobile<br>Gestão Financeira]
        
        D -->|Visualização Autônoma| T
        D -->|Visualização Interativa| C
    end
    
    style R fill:#2563eb,stroke:#fff,stroke-width:2px,color:#fff
    style A fill:#10b981,stroke:#fff,stroke-width:2px,color:#fff
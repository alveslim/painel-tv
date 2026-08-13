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
      <video src="COLE_O_LINK_DO_VIDEO_DO_CELULAR_AQUI" controls width="100%"></video>
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

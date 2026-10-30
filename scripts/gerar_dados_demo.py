"""Gera dados/dados_mock.xlsx com dados 100% FICTÍCIOS para a demonstração.

As datas são relativas a hoje, para que as abas "hoje" e "amanhã" do painel
sempre tenham itens. Uso: python scripts/gerar_dados_demo.py
"""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

CLIENTES = ["Cliente Alfa", "Cliente Beta", "Cliente Gama", "Cliente Delta", "Cliente Ômega"]
EMPRESAS = ["Indústria Aurora", "Comercial Horizonte", "Grupo Atlas", "Embalagens Vértice",
            "Metalúrgica Orion", "Têxtil Cedro", "Plásticos Nova", "Logística Ponte"]
SITUACOES = ["NOVO", "PRODUÇÃO", "AVALIAÇÃO", "EM ROTA", "ENTREGUE", "REPOSIÇÃO"]
OBS = ["", "", "", "", "CRÍTICO", "URGENTE"]
LINHAS = 380


def gerar(linhas: int = LINHAS, semente: int = 42) -> pd.DataFrame:
    rnd = random.Random(semente)
    hoje = date.today()
    registros = []
    for i in range(linhas):
        # ~12% hoje, ~12% amanhã; o restante espalhado pelo ano
        sorteio = rnd.random()
        if sorteio < 0.12:
            data = hoje
        elif sorteio < 0.24:
            data = hoje + timedelta(days=1)
        else:
            data = date(hoje.year, 1, 1) + timedelta(days=rnd.randint(0, 364))
        registros.append({
            "CLIENTE": rnd.choice(CLIENTES),
            "EMPRESA": rnd.choice(EMPRESAS),
            "REFERENCIA": f"REF-{rnd.randint(100000, 999999)}",
            "OP/LAYOUT": 30000 + i,
            "FTD": 410000 + i,
            "SITUAÇÃO": rnd.choice(SITUACOES),
            "DATA_PREVISTA": data.strftime("%d/%m/%Y"),
            "VALOR": round(rnd.uniform(150, 4500), 2),
            "OBS": rnd.choice(OBS),
        })
    return pd.DataFrame(registros)


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "dados" / "dados_mock.xlsx"
    destino.parent.mkdir(exist_ok=True)
    gerar().to_excel(destino, index=False)
    print(f"Planilha fictícia gerada em {destino}")

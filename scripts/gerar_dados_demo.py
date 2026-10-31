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
ITENS_HOJE = 8       # cabem bem na tela da TV
ITENS_AMANHA = 6


def gerar(linhas: int = LINHAS, semente: int = 42) -> pd.DataFrame:
    """Gera a planilha fictícia: poucos itens hoje/amanhã (legível na TV) e o resto no ano."""
    rnd = random.Random(semente)
    hoje = date.today()
    amanha = hoje + timedelta(days=1)

    datas = [hoje] * ITENS_HOJE + [amanha] * ITENS_AMANHA
    while len(datas) < linhas:
        d = date(hoje.year, 1, 1) + timedelta(days=rnd.randint(0, 364))
        if d not in (hoje, amanha):
            datas.append(d)

    registros = []
    for i, data in enumerate(datas):
        if data == hoje and i == 0:
            obs = "CRÍTICO"  # garante um item crítico hoje, bom para a demonstração
        elif data in (hoje, amanha):
            obs = rnd.choice(["", "", "", "URGENTE"])
        else:
            obs = rnd.choice(OBS)
        situacao = rnd.choice(["NOVO", "PRODUÇÃO", "AVALIAÇÃO", "EM ROTA"]) if data >= hoje else rnd.choice(SITUACOES)
        registros.append({
            "CLIENTE": rnd.choice(CLIENTES),
            "EMPRESA": rnd.choice(EMPRESAS),
            "REFERENCIA": f"REF-{rnd.randint(100000, 999999)}",
            "OP/LAYOUT": 30000 + i,
            "FTD": 410000 + i,
            "SITUAÇÃO": situacao,
            "DATA_PREVISTA": data.strftime("%d/%m/%Y"),
            "VALOR": round(rnd.uniform(150, 4500), 2),
            "OBS": obs,
        })
    return pd.DataFrame(registros)


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "dados" / "dados_mock.xlsx"
    destino.parent.mkdir(exist_ok=True)
    gerar().to_excel(destino, index=False)
    print(f"Planilha fictícia gerada em {destino}")

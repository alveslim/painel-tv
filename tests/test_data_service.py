from datetime import date

import pandas as pd

from services import data_service as ds


def test_limpar_valor_monetario():
    assert ds.limpar_valor_monetario("R$ 1.000,00") == 1000.0
    assert ds.limpar_valor_monetario("1.234,56") == 1234.56
    assert ds.limpar_valor_monetario(1500) == 1500.0
    assert ds.limpar_valor_monetario("") == 0.0
    assert ds.limpar_valor_monetario(None) == 0.0
    assert ds.limpar_valor_monetario("texto") == 0.0


def test_formata_para_mil():
    assert ds.formata_para_mil(500) == "500"
    assert ds.formata_para_mil(1000) == "1,0mil"
    assert ds.formata_para_mil(1500) == "1,5mil"


def test_remove_accents():
    assert ds.remove_accents("REPOSIÇÃO") == "REPOSICAO"
    assert ds.remove_accents("") == ""
    assert ds.remove_accents(None) == ""


def _planilha(data_entrega: str) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "CLIENTE": ["Cliente Alfa", "Cliente Beta"],
            "EMPRESA": ["Indústria Aurora", "Grupo Atlas"],
            "REFERENCIA": ["REF-1", "REF-2"],
            "OP/LAYOUT": [30000, 30001],
            "FTD": [410000, 410001],
            "SITUAÇÃO": ["NOVO", "REPOSIÇÃO"],
            "DATA_PREVISTA": [data_entrega, "01/01/2020"],
            "VALOR": ["R$ 1.500,00", 2500],
            "OBS": ["CRÍTICO", ""],
        }
    )
    df["DATA_OBJ"] = pd.to_datetime(df["DATA_PREVISTA"], dayfirst=True, errors="coerce")
    df["VALOR_NUM"] = df["VALOR"].apply(ds.limpar_valor_monetario)
    return df


def test_dashboard_vazio_tem_estrutura_minima():
    dados = ds.obter_dados_dashboard(pd.DataFrame())
    assert dados["hoje"] == [] and dados["amanha"] == []
    assert dados["financeiro"] == {}


def test_dashboard_separa_itens_de_hoje():
    hoje = date.today().strftime("%d/%m/%Y")
    dados = ds.obter_dados_dashboard(_planilha(hoje))

    assert dados["data_hoje"] == hoje
    assert len(dados["hoje"]) == 1
    item = dados["hoje"][0]
    assert item["SITUACAO_CLASS"] == "novo"
    assert item["IS_CRITICO"] is True
    assert dados["tem_critico"] is True
    assert dados["financeiro"]["total_anual"] == "R$ 4.000,00"


def test_graficos_retornam_html_ou_vazio():
    df = _planilha(date.today().strftime("%d/%m/%Y"))
    assert "plotly" in ds.gerar_grafico_pizza_html(df)
    assert "plotly" in ds.gerar_grafico_mensal_html(df)
    assert "plotly" in ds.gerar_grafico_faturamento_mensal_html(df)
    assert "plotly" in ds.gerar_grafico_faturamento_cliente_html(df)

    vazio = pd.DataFrame()
    assert ds.gerar_grafico_pizza_html(vazio) == ""
    assert ds.gerar_grafico_mensal_html(vazio) == ""


def test_carregar_dados_demo_le_a_planilha_do_repositorio():
    df = ds.carregar_dados_demo()
    assert not df.empty
    assert {"CLIENTE", "DATA_OBJ", "VALOR_NUM"} <= set(df.columns)

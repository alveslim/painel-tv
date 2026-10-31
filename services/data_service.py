import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_DADOS = RAIZ / "dados" / "dados_mock.xlsx"

def remove_accents(input_str):
    if not input_str: return ""
    nfkd_form = unicodedata.normalize("NFKD", str(input_str))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def limpar_valor_monetario(val):
    if pd.isna(val) or val == "": return 0.0
    if isinstance(val, (int, float)): return float(val)
    val_str = str(val).strip().replace("R$", "").replace(".", "").replace(",", ".").strip()
    try: return float(val_str)
    except: return 0.0

def garantir_dados_demo():
    """Gera a planilha fictícia se ela não existir ou não tiver itens para hoje."""
    precisa = not CAMINHO_DADOS.exists()
    if not precisa:
        try:
            hoje = date.today().strftime("%d/%m/%Y")
            precisa = hoje not in set(pd.read_excel(CAMINHO_DADOS)["DATA_PREVISTA"].astype(str))
        except Exception:
            precisa = True
    if precisa:
        import importlib.util
        script = RAIZ / "scripts" / "gerar_dados_demo.py"
        spec = importlib.util.spec_from_file_location("gerar_dados_demo", script)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        CAMINHO_DADOS.parent.mkdir(parents=True, exist_ok=True)
        modulo.gerar().to_excel(CAMINHO_DADOS, index=False)
        print(f"Planilha fictícia (re)gerada em {CAMINHO_DADOS}")


def carregar_dados_demo():
    try:
        garantir_dados_demo()
        df = pd.read_excel(CAMINHO_DADOS)
        df["DATA_OBJ"] = pd.to_datetime(df["DATA_PREVISTA"], dayfirst=True, errors="coerce")
        df["VALOR_NUM"] = df["VALOR"].apply(limpar_valor_monetario)
        return df
    except Exception as e:
        print("Erro ao ler dados/dados_mock.xlsx. Rode: python scripts/gerar_dados_demo.py")
        return pd.DataFrame()

def obter_dados_dashboard(df):
    if df.empty: return {"hoje": [], "amanha": [], "financeiro": {}}
    
    data_br = date.today().strftime("%d/%m/%Y")
    data_amanha_br = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    
    df_hoje = df[df["DATA_PREVISTA"] == data_br].copy()
    df_amanha = df[df["DATA_PREVISTA"] == data_amanha_br].copy()

    def preparar_tabela(df_temp):
        if df_temp.empty: return df_temp
        df_temp["ITEM"] = range(1, len(df_temp) + 1)
        df_temp["SITUACAO_CLASS"] = df_temp["SITUAÇÃO"].apply(lambda x: remove_accents(str(x)).lower())
        df_temp["IS_CRITICO"] = df_temp["OBS"].apply(lambda x: "CRÍTICO" in str(x).upper() or "URGENTE" in str(x).upper())
        df_temp["SERVICO_SITUACAO"] = df_temp["SITUAÇÃO"]
        df_temp["OP_LAYOUT"] = df_temp["OP/LAYOUT"]
        return df_temp.fillna("")

    fat_anual = df["VALOR_NUM"].sum()
    fat_mes = df[df["DATA_OBJ"].dt.month == date.today().month]["VALOR_NUM"].sum()

    return {
        "hoje": preparar_tabela(df_hoje).to_dict(orient="records"),
        "amanha": preparar_tabela(df_amanha).to_dict(orient="records"),
        "data_hoje": data_br,
        "data_amanha": data_amanha_br,
        "tem_critico": "CRÍTICO" in df_hoje["OBS"].values if not df_hoje.empty else False,
        "financeiro": {
            "total_anual": f"R$ {fat_anual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "total_mensal": f"R$ {fat_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        }
    }

def formata_para_mil(valor):
    if valor >= 1000: return f"{valor/1000:.1f}mil".replace(".", ",")
    return str(int(valor))

def gerar_grafico_pizza_html(df):
    if df.empty: return ""
    fig = px.pie(df, names="CLIENTE", title="Distribuição por Cliente", hole=0.35)
    fig.update_traces(textinfo="percent+label", textposition="auto", insidetextorientation="horizontal")
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10), showlegend=False,
        title=dict(text="Distribuição por Cliente", x=0.5, xanchor="center")
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def gerar_grafico_mensal_html(df):
    if df.empty: return ""
    meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    res = [{"Mes": meses[m-1], "Total": len(df[df["DATA_OBJ"].dt.month == m])} for m in range(1, 13)]
    fig = px.bar(pd.DataFrame(res), x="Mes", y="Total", title="Estatística Mensal (Entradas)")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig.to_html(full_html=False, include_plotlyjs=False)

def gerar_grafico_faturamento_mensal_html(df):
    if df.empty: return ""
    meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    res = [{"Mês": meses[m-1], "Fat": df[df["DATA_OBJ"].dt.month == m]["VALOR_NUM"].sum()} for m in range(1, 13)]
    df_fat = pd.DataFrame(res)
    df_fat["TEXTO"] = df_fat["Fat"].apply(formata_para_mil)
    fig = px.bar(df_fat, x="Mês", y="Fat", title="Faturamento Mensal (R$)", text="TEXTO", color="Fat", color_continuous_scale="Viridis")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False, yaxis=dict(showticklabels=False))
    return fig.to_html(full_html=False, include_plotlyjs=False)

def gerar_grafico_faturamento_cliente_html(df):
    if df.empty: return ""
    df_cli = df.groupby("CLIENTE")["VALOR_NUM"].sum().reset_index().sort_values(by="VALOR_NUM")
    df_cli["TEXTO"] = df_cli["VALOR_NUM"].apply(formata_para_mil)
    fig = px.bar(df_cli, x="VALOR_NUM", y="CLIENTE", orientation="h", title="Faturamento por Cliente", text="TEXTO", color="VALOR_NUM", color_continuous_scale="Greens")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False, xaxis=dict(showticklabels=False))
    return fig.to_html(full_html=False, include_plotlyjs=False)


def montar_pacote(df):
    """Pacote completo (dados + gráficos) que o painel exibe."""
    return {
        "dados": obter_dados_dashboard(df),
        "grafico_pizza": gerar_grafico_pizza_html(df),
        "grafico_mensal": gerar_grafico_mensal_html(df),
        "grafico_fat_mensal": gerar_grafico_faturamento_mensal_html(df),
        "grafico_fat_cliente": gerar_grafico_faturamento_cliente_html(df),
    }

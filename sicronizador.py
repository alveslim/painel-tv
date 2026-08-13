import time
import requests
import schedule
import json
from datetime import datetime
from services.data_service import (
    carregar_dados_demo, obter_dados_dashboard, gerar_grafico_pizza_html,
    gerar_grafico_mensal_html, gerar_grafico_faturamento_mensal_html, gerar_grafico_faturamento_cliente_html
)

URL_NUVEM = "http://127.0.0.1:5000/api/sync" # Aponta para o servidor local no teste
SENHA_API = "demo_api_key_123"

def sincronizar_com_nuvem():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Lendo Excel local...")
    df = carregar_dados_demo()
    
    if df.empty:
        print("⚠️ Sem dados. Abortando.")
        return

    pacote = {
        "dados": obter_dados_dashboard(df),
        "grafico_pizza": gerar_grafico_pizza_html(df),
        "grafico_mensal": gerar_grafico_mensal_html(df),
        "grafico_fat_mensal": gerar_grafico_faturamento_mensal_html(df),
        "grafico_fat_cliente": gerar_grafico_faturamento_cliente_html(df),
    }

    try:
        resp = requests.post(URL_NUVEM, json=json.loads(json.dumps(pacote, default=str)), headers={"x-api-key": SENHA_API})
        if resp.status_code == 200:
            print("✅ Dados enviados com sucesso para a aplicação web!")
        else:
            print("❌ Erro ao enviar. O servidor web (app.py) está rodando?")
    except:
        print("❌ Servidor web não encontrado. Execute 'python app.py' em outro terminal.")

sincronizar_com_nuvem()
schedule.every(1).minutes.do(sincronizar_com_nuvem)

print("🤖 Robô de Demonstração Ativo (Envia dados a cada 1 minuto)")
while True:
    schedule.run_pending()
    time.sleep(1)
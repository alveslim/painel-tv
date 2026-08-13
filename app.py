import os
import time
from functools import wraps
from flask import Flask, render_template, request, Response, jsonify, make_response

app = Flask(__name__)

# Credenciais de Demonstração
USUARIO_CLIENTE = "admin"
SENHA_CLIENTE = "admin"
SENHA_API_SECRETA = "demo_api_key_123"

banco_de_dados = {
    "dados": {"hoje": [], "amanha": [], "data_hoje": "Aguardando robô...", "data_amanha": "Aguardando robô...", "financeiro": {}},
    "grafico_pizza": "Aguardando dados...", "grafico_mensal": "", "grafico_fat_mensal": "", "grafico_fat_cliente": ""
}

def check_auth(username, password):
    return username == USUARIO_CLIENTE and password == SENHA_CLIENTE

def authenticate():
    return Response('Acesso negado.', 401, {'WWW-Authenticate': 'Basic realm="Login Necessário"'})

def requer_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.cookies.get('auth_demo') == SENHA_CLIENTE:
            return f(*args, **kwargs)
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        resposta = make_response(f(*args, **kwargs))
        resposta.set_cookie('auth_demo', SENHA_CLIENTE, max_age=315360000)
        return resposta
    return decorated

@app.route("/api/sync", methods=["POST"])
def receber_dados():
    if request.headers.get("x-api-key") != SENHA_API_SECRETA:
        return jsonify({"erro": "Acesso negado."}), 401
    
    global banco_de_dados
    banco_de_dados = request.json
    return jsonify({"mensagem": "Sucesso"}), 200

@app.route("/")
@requer_login
def index_publico():
    return render_template("index.html", dados=banco_de_dados["dados"], grafico_pizza=banco_de_dados["grafico_pizza"], grafico_mensal=banco_de_dados["grafico_mensal"], is_gestao=False, is_producao=False)

@app.route("/gestao")
@requer_login
def index_gestao():
    return render_template("index.html", dados=banco_de_dados["dados"], grafico_pizza=banco_de_dados["grafico_pizza"], grafico_mensal=banco_de_dados["grafico_mensal"], grafico_fat_mensal=banco_de_dados["grafico_fat_mensal"], grafico_fat_cliente=banco_de_dados["grafico_fat_cliente"], is_gestao=True, is_producao=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
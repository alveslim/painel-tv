from base64 import b64encode

import pytest

import app as painel


def _basic(usuario: str, senha: str) -> dict:
    token = b64encode(f"{usuario}:{senha}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


AUTH = _basic(painel.USUARIO_CLIENTE, painel.SENHA_CLIENTE)


@pytest.fixture
def cliente():
    estado_original = painel.banco_de_dados
    yield painel.app.test_client()
    painel.banco_de_dados = estado_original


@pytest.mark.parametrize("rota", ["/", "/gestao"])
def test_exige_login(cliente, rota):
    assert cliente.get(rota).status_code == 401


@pytest.mark.parametrize("rota", ["/", "/gestao"])
def test_renderiza_o_template_com_login(cliente, rota):
    """Garante que templates/index.html existe e renderiza (erro TemplateNotFound)."""
    resposta = cliente.get(rota, headers=AUTH)
    assert resposta.status_code == 200


def test_senha_errada_e_negada(cliente):
    resposta = cliente.get("/", headers=_basic(painel.USUARIO_CLIENTE, "errada"))
    assert resposta.status_code == 401


def test_api_sync_rejeita_chave_invalida(cliente):
    resposta = cliente.post("/api/sync", json={"dados": {}}, headers={"x-api-key": "errada"})
    assert resposta.status_code == 401


def test_api_sync_atualiza_o_painel(cliente):
    pacote = {
        "dados": {
            "hoje": [],
            "amanha": [],
            "data_hoje": "01/02/2030",
            "data_amanha": "02/02/2030",
            "tem_critico": False,
            "financeiro": {"total_anual": "R$ 9,00", "total_mensal": "R$ 9,00"},
        },
        "grafico_pizza": "<div>pizza</div>",
        "grafico_mensal": "",
        "grafico_fat_mensal": "",
        "grafico_fat_cliente": "",
    }
    resposta = cliente.post("/api/sync", json=pacote, headers={"x-api-key": painel.SENHA_API_SECRETA})
    assert resposta.status_code == 200

    pagina = cliente.get("/gestao", headers=AUTH)
    assert pagina.status_code == 200
    assert b"01/02/2030" in pagina.data

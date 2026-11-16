from agente import atender
from agente.privacidade import mascarar
from agente.roteador import rotear
from agente.base import carregar

BASE = carregar()


def test_mascara_cartao_cpf_cnpj_email():
    t = mascarar("cartão 4111 1111 1111 1111, CPF 123.456.789-00, CNPJ 12.345.678/0001-90, a@b.com")
    assert "4111" not in t and "123.456" not in t and "12.345" not in t and "a@b.com" not in t
    assert "[CARTAO]" in t and "[CPF]" in t and "[CNPJ]" in t and "[EMAIL]" in t


def test_dado_sensivel_nao_vaza_na_decisao():
    d = atender("Fui cobrado duas vezes no cartão 5555 4444 3333 2222", base=BASE)
    assert "5555" not in d.texto_mascarado


def test_roteia_por_palavra_inteira():
    proc, _, _ = rotear("Como configuro meu e-mail?", BASE)
    assert proc is None  # "nf" não pode casar dentro de "configuro"


def test_fraude_sempre_escala():
    d = atender("Meu cartão foi clonado, quero reembolso", base=BASE)
    assert d.acao == "escalar"


def test_multiplos_assuntos_escala():
    d = atender("Paguei o boleto mas quero cancelar e pedir reembolso", base=BASE)
    assert d.acao == "escalar"


def test_caso_simples_responde_sem_api(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    d = atender("Preciso da nota fiscal", nome="Ana", base=BASE)
    assert d.acao == "responder" and d.procedimento == "nota-fiscal"
    assert d.resposta.startswith("Olá, Ana!")


def _fake_anthropic(monkeypatch, resposta):
    import sys, types

    class _Msgs:
        def create(self, **kw):
            assert "[CARTAO]" in kw["messages"][0]["content"] or "cartão" not in kw["messages"][0]["content"]
            return types.SimpleNamespace(content=[types.SimpleNamespace(text=resposta)])

    mod = types.SimpleNamespace(Anthropic=lambda api_key: types.SimpleNamespace(messages=_Msgs()))
    monkeypatch.setitem(sys.modules, "anthropic", mod)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chave-falsa-de-teste")


def test_modo_llm_usa_resposta_do_modelo(monkeypatch):
    _fake_anthropic(monkeypatch, "Olá! Sua nota está na área do cliente.")
    d = atender("Preciso da nota fiscal", base=BASE)
    assert d.acao == "responder" and "área do cliente" in d.resposta


def test_modo_llm_escala_quando_modelo_pede(monkeypatch):
    _fake_anthropic(monkeypatch, "ESCALAR")
    d = atender("Preciso da nota fiscal", base=BASE)
    assert d.acao == "escalar"

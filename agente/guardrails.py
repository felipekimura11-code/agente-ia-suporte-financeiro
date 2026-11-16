"""Regras que obrigam o atendimento humano, independentemente do modelo."""
from .texto import normalizar

# Temas sensíveis: risco jurídico, fraude ou perda financeira relevante.
GATILHOS_HUMANO = {
    "chargeback": "contestação junto ao banco",
    "contestei": "contestação junto ao banco",
    "contestacao": "contestação junto ao banco",
    "fraude": "suspeita de fraude",
    "clonado": "suspeita de fraude",
    "golpe": "suspeita de fraude",
    "nao reconheco": "cobrança não reconhecida",
    "procon": "risco jurídico",
    "advogado": "risco jurídico",
    "processo": "risco jurídico",
    "reclame aqui": "risco reputacional",
}


def motivo_para_humano(texto: str) -> str | None:
    t = normalizar(texto)
    for gatilho, motivo in GATILHOS_HUMANO.items():
        if gatilho in t:
            return motivo
    return None

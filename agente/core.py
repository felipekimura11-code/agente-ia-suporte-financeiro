"""Orquestra: mascarar -> guardrails -> rotear -> responder ou escalar."""
from dataclasses import dataclass

from .base import Procedimento, carregar
from .guardrails import motivo_para_humano
from .privacidade import mascarar
from .respondedor import responder
from .roteador import rotear

CONFIANCA_MINIMA = 0.6


@dataclass
class Decisao:
    acao: str              # "responder" ou "escalar"
    procedimento: str | None
    confianca: float
    motivo: str
    resposta: str | None
    texto_mascarado: str


def atender(texto: str, nome: str = "cliente", base: list[Procedimento] | None = None) -> Decisao:
    base = base or carregar()
    seguro = mascarar(texto)

    motivo = motivo_para_humano(seguro)
    proc, confianca, multiplos = rotear(seguro, base)
    proc_id = proc.id if proc else None

    if motivo:
        return Decisao("escalar", proc_id, confianca, motivo, None, seguro)
    if proc is None:
        return Decisao("escalar", None, 0.0, "nenhum procedimento cobre o caso", None, seguro)
    if multiplos:
        return Decisao("escalar", proc_id, confianca, "mais de um assunto no mesmo ticket", None, seguro)
    if confianca < CONFIANCA_MINIMA:
        return Decisao("escalar", proc_id, confianca, "baixa confiança no roteamento", None, seguro)

    resposta = responder(seguro, proc, nome)
    if resposta.strip().upper() == "ESCALAR":
        return Decisao("escalar", proc_id, confianca, "modelo indicou que o procedimento não cobre", None, seguro)
    return Decisao("responder", proc_id, confianca, "procedimento encontrado", resposta, seguro)

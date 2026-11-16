"""Mascara dados pessoais antes de qualquer processamento (LGPD).

O texto do cliente pode trazer número de cartão, CPF ou CNPJ. Esses dados nunca
devem ir para logs nem para o modelo de linguagem.
"""
import re

_CARTAO = re.compile(r"\b(?:\d[ -]?){13,19}\b")
_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
_CNPJ = re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")
_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")


def mascarar(texto: str) -> str:
    texto = _CNPJ.sub("[CNPJ]", texto)
    texto = _CPF.sub("[CPF]", texto)
    texto = _CARTAO.sub("[CARTAO]", texto)
    texto = _EMAIL.sub("[EMAIL]", texto)
    return texto

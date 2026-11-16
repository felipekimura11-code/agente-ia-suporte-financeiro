"""Escolhe o procedimento mais provável para o ticket (busca por palavras-chave)."""
import re

from .base import Procedimento
from .texto import normalizar


def pontuar(texto: str, proc: Procedimento) -> float:
    t = normalizar(texto)
    pontos = 0.0
    for chave in proc.palavras_chave:
        c = normalizar(chave)
        # \b = palavra inteira: evita que "nf" case dentro de "configuro"
        if re.search(rf"\b{re.escape(c)}\b", t):
            pontos += 1 + len(c.split()) * 0.5  # expressões longas valem mais
    return pontos


def rotear(texto: str, base: list[Procedimento]) -> tuple[Procedimento | None, float, bool]:
    """Retorna (procedimento, confiança 0-1, multiplos_assuntos)."""
    notas = sorted(((pontuar(texto, p), p) for p in base), key=lambda x: x[0], reverse=True)
    melhor, proc = notas[0]
    if melhor == 0:
        return None, 0.0, False
    segundo = notas[1][0] if len(notas) > 1 else 0.0
    confianca = melhor / (melhor + segundo)  # 1.0 quando não há concorrente
    multiplos = segundo > 0 and segundo >= 0.5 * melhor
    return proc, round(confianca, 2), multiplos

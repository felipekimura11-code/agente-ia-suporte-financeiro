"""Gera a resposta ao cliente.

Com ANTHROPIC_API_KEY definida, usa um LLM limitado ao procedimento escolhido.
Sem a chave, usa a resposta modelo do procedimento (modo offline, para testes).
"""
import os

from .base import Procedimento

PROMPT_SISTEMA = """Você é um agente de suporte financeiro de uma empresa de hospedagem.
Responda em português, com cordialidade e no máximo 4 frases.
Use SOMENTE as informações do procedimento abaixo. Se ele não cobrir o caso,
responda exatamente: ESCALAR.
Nunca peça número de cartão, senha ou CPF completo.

PROCEDIMENTO:
{procedimento}"""


def _offline(proc: Procedimento, nome: str) -> str:
    return proc.resposta_modelo.replace("{nome}", nome).replace(
        " {prazo_forma_pagamento}", ""
    )


def responder(texto_mascarado: str, proc: Procedimento, nome: str = "cliente") -> str:
    chave = os.getenv("ANTHROPIC_API_KEY")
    if not chave:
        return _offline(proc, nome)

    import anthropic  # dependência opcional

    cliente = anthropic.Anthropic(api_key=chave)
    msg = cliente.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-5-5"),
        max_tokens=300,
        system=PROMPT_SISTEMA.format(procedimento=proc.corpo),
        messages=[{"role": "user", "content": f"Cliente ({nome}): {texto_mascarado}"}],
    )
    return msg.content[0].text.strip()

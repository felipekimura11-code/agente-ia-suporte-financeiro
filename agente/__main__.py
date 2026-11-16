"""Uso: python -m agente "texto do cliente" [--nome Ana]"""
import argparse

from .core import atender


def main() -> None:
    p = argparse.ArgumentParser(description="Agente de suporte financeiro (demo)")
    p.add_argument("texto")
    p.add_argument("--nome", default="cliente")
    a = p.parse_args()
    d = atender(a.texto, a.nome)
    print(f"Ação: {d.acao.upper()} | procedimento: {d.procedimento} | confiança: {d.confianca}")
    print(f"Motivo: {d.motivo}")
    if d.resposta:
        print(f"\nResposta:\n{d.resposta}")


if __name__ == "__main__":
    main()

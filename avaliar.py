"""Avalia o agente nos tickets de exemplo e imprime as métricas.

Uso: python avaliar.py
"""
import csv
from pathlib import Path

from agente import atender
from agente.base import carregar

ARQ = Path(__file__).parent / "dados" / "tickets_exemplo.csv"


def main() -> None:
    base = carregar()
    linhas = list(csv.DictReader(ARQ.open(encoding="utf-8")))
    acertos_acao = acertos_proc = respondidos_esperados = 0
    falsos_respondidos = 0  # deveria escalar, mas respondeu (erro mais grave)
    erros = []

    for t in linhas:
        d = atender(t["texto"], base=base)
        ok_acao = d.acao == t["esperado_acao"]
        acertos_acao += ok_acao
        if t["esperado_acao"] == "responder":
            respondidos_esperados += 1
            acertos_proc += ok_acao and d.procedimento == t["esperado_procedimento"]
        elif d.acao == "responder":
            falsos_respondidos += 1
        if not ok_acao or (t["esperado_acao"] == "responder" and d.procedimento != t["esperado_procedimento"]):
            erros.append((t["id"], t["texto"], t["esperado_acao"], d.acao, d.procedimento, d.motivo))

    n = len(linhas)
    print(f"Tickets avaliados ............ {n}")
    print(f"Decisão correta (resp/escalar) {acertos_acao}/{n} = {acertos_acao / n:.0%}")
    print(f"Procedimento correto ......... {acertos_proc}/{respondidos_esperados} = {acertos_proc / respondidos_esperados:.0%}")
    print(f"Respondeu quando devia escalar {falsos_respondidos}")
    if erros:
        print("\nCasos para revisar:")
        for e in erros:
            print(f"  #{e[0]} '{e[1]}' -> esperado {e[2]}, obtido {e[3]} ({e[4]}; {e[5]})")


if __name__ == "__main__":
    main()

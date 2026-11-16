"""Carrega a base de conhecimento (um procedimento por arquivo .md)."""
from dataclasses import dataclass, field
from pathlib import Path

PASTA_PADRAO = Path(__file__).resolve().parent.parent / "base_conhecimento"


@dataclass
class Procedimento:
    id: str
    titulo: str
    palavras_chave: list[str]
    escalar_quando: list[str]
    corpo: str
    resposta_modelo: str = field(default="")


def _ler(caminho: Path) -> Procedimento:
    texto = caminho.read_text(encoding="utf-8")
    _, cabecalho, corpo = texto.split("---", 2)
    meta = {}
    for linha in cabecalho.strip().splitlines():
        chave, _, valor = linha.partition(":")
        meta[chave.strip()] = valor.strip()
    resposta = corpo.split("## Resposta modelo", 1)[-1].strip() if "## Resposta modelo" in corpo else ""
    return Procedimento(
        id=meta["id"],
        titulo=meta["titulo"],
        palavras_chave=[p.strip() for p in meta.get("palavras_chave", "").split(",") if p.strip()],
        escalar_quando=[p.strip() for p in meta.get("escalar_quando", "").split(",") if p.strip()],
        corpo=corpo.strip(),
        resposta_modelo=resposta,
    )


def carregar(pasta: Path = PASTA_PADRAO) -> list[Procedimento]:
    return [_ler(arq) for arq in sorted(pasta.glob("*.md"))]

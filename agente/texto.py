import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas e sem acento, para comparar palavras de forma robusta."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.lower().split())

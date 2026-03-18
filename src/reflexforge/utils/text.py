def truncate(text: str, n: int = 120) -> str:
    return text if len(text) <= n else text[: n - 3] + "..."

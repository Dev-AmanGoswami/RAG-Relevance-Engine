def get_prompt(path: str) -> str:
    return path.read_text(encoding="utf-8").strip()

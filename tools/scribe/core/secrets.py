import os
from pathlib import Path

class Secrets:
    def __init__(self, base: str = "/vault/secrets"):
        self.base = Path(base)

    def read_text(self, name: str) -> str:
        p = self.base / name
        if not p.exists():
            raise FileNotFoundError(f"Missing secret: {p}")
        return p.read_text(encoding="utf-8")

    def require_tls(self):
        ca = self.read_text("ca.crt")
        crt = self.read_text("server.crt")
        key = self.read_text("server.key")
        return ca, crt, key
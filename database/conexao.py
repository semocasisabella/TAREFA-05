from contextlib import contextmanager
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT_DIR / "estoque.db"
BACKUP_DIR = ROOT_DIR / "backups"


class BancoDados:
    def __init__(self, caminho=DATABASE_PATH):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.inicializar()

    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        try:
            with conexao:
                yield conexao
        finally:
            conexao.close()

    def inicializar(self):
        schema = ROOT_DIR / "banco.sql"
        with self.conectar() as conexao:
            conexao.executescript(schema.read_text(encoding="utf-8"))

    def criar_backup(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        nome = "estoque_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".db"
        destino = BACKUP_DIR / nome
        with self.conectar() as origem:
            copia = sqlite3.connect(destino)
            try:
                origem.backup(copia)
            finally:
                copia.close()
        backups = sorted(
            BACKUP_DIR.glob("estoque_*.db"),
            key=lambda arquivo: arquivo.stat().st_mtime,
            reverse=True,
        )
        for antigo in backups[10:]:
            antigo.unlink()
        return destino

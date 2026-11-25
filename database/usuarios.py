import hashlib
import hmac
import secrets


class Usuarios:
    ITERACOES = 310_000

    def __init__(self, banco):
        self.banco = banco

    def existe_algum(self):
        with self.banco.conectar() as conexao:
            return conexao.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone() is not None

    def criar(self, usuario, senha):
        salt = secrets.token_bytes(16)
        senha_hash = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), salt, self.ITERACOES
        )
        with self.banco.conectar() as conexao:
            conexao.execute(
                "INSERT INTO usuarios (usuario, salt, senha_hash) VALUES (?, ?, ?)",
                (usuario, salt, senha_hash),
            )

    def autenticar(self, usuario, senha):
        with self.banco.conectar() as conexao:
            registro = conexao.execute(
                "SELECT salt, senha_hash FROM usuarios WHERE usuario = ?",
                (usuario,),
            ).fetchone()
        if registro is None:
            return False
        tentativa = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), registro["salt"], self.ITERACOES
        )
        return hmac.compare_digest(tentativa, registro["senha_hash"])

import sqlite3


class Produtos:
    def __init__(self, banco):
        self.banco = banco

    def listar(self, categoria=None):
        with self.banco.conectar() as conexao:
            if categoria:
                return conexao.execute(
                    "SELECT * FROM produtos WHERE categoria = ? ORDER BY nome",
                    (categoria,),
                ).fetchall()
            return conexao.execute("SELECT * FROM produtos ORDER BY nome").fetchall()

    def categorias(self):
        with self.banco.conectar() as conexao:
            return [
                linha["categoria"]
                for linha in conexao.execute(
                    "SELECT DISTINCT categoria FROM produtos "
                    "WHERE categoria <> '' ORDER BY categoria"
                )
            ]

    def obter(self, codigo):
        with self.banco.conectar() as conexao:
            return conexao.execute(
                "SELECT * FROM produtos WHERE codigo = ?", (codigo,)
            ).fetchone()

    def salvar(self, codigo, nome, categoria, preco, estoque_minimo, codigo_original=None):
        with self.banco.conectar() as conexao:
            if codigo_original:
                conexao.execute(
                    "UPDATE produtos SET codigo = ?, nome = ?, categoria = ?, "
                    "preco = ?, estoque_minimo = ? WHERE codigo = ?",
                    (codigo, nome, categoria, preco, estoque_minimo, codigo_original),
                )
            else:
                conexao.execute(
                    "INSERT INTO produtos "
                    "(codigo, nome, categoria, preco, estoque_minimo) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (codigo, nome, categoria, preco, estoque_minimo),
                )

    def excluir(self, codigo):
        with self.banco.conectar() as conexao:
            conexao.execute("DELETE FROM produtos WHERE codigo = ?", (codigo,))

    def resumo(self):
        with self.banco.conectar() as conexao:
            return conexao.execute(
                "SELECT COUNT(*) AS produtos, "
                "COALESCE(SUM(quantidade), 0) AS unidades, "
                "COALESCE(SUM(preco * quantidade), 0) AS valor, "
                "COALESCE(SUM(CASE WHEN quantidade <= estoque_minimo "
                "THEN 1 ELSE 0 END), 0) AS baixos FROM produtos"
            ).fetchone()

    def listar_baixo_estoque(self):
        with self.banco.conectar() as conexao:
            return conexao.execute(
                "SELECT * FROM produtos WHERE quantidade <= estoque_minimo "
                "ORDER BY quantidade, nome"
            ).fetchall()

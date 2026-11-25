class Movimentacoes:
    def __init__(self, banco):
        self.banco = banco

    def registrar(self, produto_codigo, tipo, quantidade):
        with self.banco.conectar() as conexao:
            conexao.execute(
                "INSERT INTO movimentacoes (produto_codigo, tipo, quantidade) "
                "VALUES (?, ?, ?)",
                (produto_codigo, tipo, quantidade),
            )

    def listar(self, categoria=None, limite=500):
        consulta = (
            "SELECT m.id, m.tipo, m.quantidade, m.data, p.codigo, p.nome, "
            "p.categoria, p.preco FROM movimentacoes m "
            "JOIN produtos p ON p.codigo = m.produto_codigo"
        )
        parametros = []
        if categoria:
            consulta += " WHERE p.categoria = ?"
            parametros.append(categoria)
        consulta += " ORDER BY m.data DESC, m.id DESC LIMIT ?"
        parametros.append(limite)
        with self.banco.conectar() as conexao:
            return conexao.execute(consulta, parametros).fetchall()

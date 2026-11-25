import sqlite3
import tempfile
import unittest
from pathlib import Path

from database.conexao import BancoDados
from database.movimentacoes import Movimentacoes
from database.produtos import Produtos
from database.usuarios import Usuarios
from utilitarios.validacoes import validar_movimentacao, validar_produto


class EstoqueDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.diretorio = tempfile.TemporaryDirectory()
        caminho = Path(self.diretorio.name) / "teste.db"
        self.banco = BancoDados(caminho)
        self.produtos = Produtos(self.banco)
        self.movimentacoes = Movimentacoes(self.banco)

    def tearDown(self):
        self.diretorio.cleanup()

    def test_movimentacoes_atualizam_saldo_e_bloqueiam_saida_excedente(self):
        self.produtos.salvar("A-1", "Caneta", "Papelaria", 2.5, 3)
        self.movimentacoes.registrar("A-1", "entrada", 8)
        self.movimentacoes.registrar("A-1", "saida", 2)
        self.assertEqual(self.produtos.obter("A-1")["quantidade"], 6)
        with self.assertRaisesRegex(sqlite3.IntegrityError, "Estoque insuficiente"):
            self.movimentacoes.registrar("A-1", "saida", 7)
        self.assertEqual(self.produtos.obter("A-1")["quantidade"], 6)

    def test_codigo_unico_e_chave_estrangeira(self):
        self.produtos.salvar("A-1", "Caneta", "Papelaria", 2.5, 3)
        with self.assertRaises(sqlite3.IntegrityError):
            self.produtos.salvar("A-1", "Outra", "Papelaria", 3, 2)
        with self.assertRaises(sqlite3.IntegrityError):
            self.movimentacoes.registrar("inexistente", "entrada", 1)

    def test_validacoes_rejeitam_quantidade_e_preco_invalidos(self):
        for quantidade in ("0", "-2", "1.5", "abc"):
            with self.subTest(quantidade=quantidade):
                with self.assertRaises(ValueError):
                    validar_movimentacao(quantidade)
        with self.assertRaises(ValueError):
            validar_produto("X", "Item", "nan", "0")

    def test_senha_armazenada_com_hash_e_autenticada(self):
        usuarios = Usuarios(self.banco)
        self.assertFalse(usuarios.existe_algum())
        usuarios.criar("operador", "senha-segura-123")
        self.assertTrue(usuarios.existe_algum())
        self.assertTrue(usuarios.autenticar("operador", "senha-segura-123"))
        self.assertFalse(usuarios.autenticar("operador", "senha-incorreta"))


if __name__ == "__main__":
    unittest.main()

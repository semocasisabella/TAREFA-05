import tkinter as tk
from tkinter import messagebox, ttk

from database.conexao import BancoDados
from database.movimentacoes import Movimentacoes
from database.produtos import Produtos
from database.usuarios import Usuarios
from interface.login import LoginFrame
from interface.menu_principal import MenuPrincipal
from interface.tema import configurar_tema


class Aplicacao:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Controle de Estoque")
        self.raiz.geometry("1120x720")
        self.raiz.minsize(900, 600)
        configurar_tema(self.raiz)
        self.banco = BancoDados()
        self.produtos = Produtos(self.banco)
        self.movimentacoes = Movimentacoes(self.banco)
        self.usuarios = Usuarios(self.banco)
        try:
            self.banco.criar_backup()
        except OSError as erro:
            messagebox.showerror("Falha no backup", str(erro), parent=self.raiz)
        self.login = LoginFrame(self.raiz, self.usuarios, self._abrir_sistema)
        self.login.pack(expand=True)
        self.raiz.protocol("WM_DELETE_WINDOW", self._fechar)

    def _abrir_sistema(self, usuario):
        self.login.destroy()
        self.menu = MenuPrincipal(
            self.raiz, self.banco, self.produtos, self.movimentacoes, usuario
        )
        self.menu.pack(fill="both", expand=True)

    def _fechar(self):
        try:
            self.banco.criar_backup()
        except OSError as erro:
            messagebox.showerror("Falha no backup", str(erro), parent=self.raiz)
        self.raiz.destroy()


def main():
    raiz = tk.Tk()
    Aplicacao(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()

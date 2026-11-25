import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class LoginFrame(ttk.Frame):
    def __init__(self, parent, usuarios, ao_autenticar):
        super().__init__(parent, padding=32, style="Page.TFrame")
        self.usuarios = usuarios
        self.ao_autenticar = ao_autenticar
        self.configuracao_inicial = not usuarios.existe_algum()
        self._montar()

    def _montar(self):
        self.columnconfigure(0, weight=1)
        cartao = ttk.Frame(self, padding=(36, 32), style="LoginCard.TFrame")
        cartao.grid(row=0, column=0, sticky="nsew")
        cartao.columnconfigure(0, weight=1)
        ttk.Label(
            cartao, text="ESTOQUE", style="LoginBrand.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Label(
            cartao, text="Gestão simples e organizada", style="LoginSubtitle.TLabel"
        ).grid(row=1, column=0, sticky="w", pady=(0, 24))
        ttk.Label(
            cartao, text="Acesse sua conta", style="LoginHeading.TLabel"
        ).grid(row=2, column=0, sticky="w", pady=(0, 4))
        texto = "Crie a primeira conta para configurar o acesso." if self.configuracao_inicial else "Entre com suas credenciais para continuar."
        ttk.Label(
            cartao, text=texto, style="LoginSubtitle.TLabel"
        ).grid(row=3, column=0, sticky="w", pady=(0, 16))
        formulario = ttk.Frame(cartao, style="LoginCard.TFrame")
        formulario.grid(row=4, column=0, sticky="ew")
        formulario.columnconfigure(0, weight=1)
        ttk.Label(formulario, text="Usuário", style="LoginField.TLabel").grid(
            row=0, column=0, sticky="w", pady=6
        )
        self.usuario = ttk.Entry(formulario, width=30)
        self.usuario.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(formulario, text="Senha", style="LoginField.TLabel").grid(
            row=2, column=0, sticky="w", pady=6
        )
        self.senha = ttk.Entry(formulario, show="*", width=30)
        self.senha.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        self.confirmacao = None
        if self.configuracao_inicial:
            ttk.Label(
                formulario, text="Confirmar senha", style="LoginField.TLabel"
            ).grid(
                row=4, column=0, sticky="w", pady=6
            )
            self.confirmacao = ttk.Entry(formulario, show="*", width=30)
            self.confirmacao.grid(row=5, column=0, sticky="ew", pady=(0, 12))
        self.usuario.bind("<Return>", lambda _evento: self.senha.focus_set())
        self.senha.bind("<Return>", lambda _evento: self._enviar())
        ttk.Button(
            formulario,
            text="Criar conta" if self.configuracao_inicial else "Entrar",
            style="Primary.TButton",
            command=self._enviar,
        ).grid(row=6, column=0, sticky="ew", pady=(4, 0))
        self.usuario.focus_set()

    def _enviar(self):
        usuario = self.usuario.get().strip()
        senha = self.senha.get()
        if not usuario or not senha:
            messagebox.showwarning("Dados obrigatórios", "Informe usuário e senha.", parent=self)
            return
        if self.configuracao_inicial:
            if len(senha) < 8:
                messagebox.showwarning(
                    "Senha fraca", "A senha deve ter pelo menos 8 caracteres.", parent=self
                )
                return
            if senha != self.confirmacao.get():
                messagebox.showwarning("Senha", "As senhas não coincidem.", parent=self)
                return
            try:
                self.usuarios.criar(usuario, senha)
            except sqlite3.IntegrityError:
                messagebox.showerror("Usuário", "Esse usuário já existe.", parent=self)
                return
            self.ao_autenticar(usuario)
        elif self.usuarios.autenticar(usuario, senha):
            self.ao_autenticar(usuario)
        else:
            messagebox.showerror("Acesso negado", "Usuário ou senha incorretos.", parent=self)

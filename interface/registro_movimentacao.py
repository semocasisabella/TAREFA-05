import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from utilitarios.codigo_barras import iniciar_leitor
from utilitarios.validacoes import validar_movimentacao


class RegistroMovimentacao(ttk.Frame):
    def __init__(self, parent, produtos, movimentacoes, ao_alterar):
        super().__init__(parent, padding=28, style="Page.TFrame")
        self.produtos = produtos
        self.movimentacoes = movimentacoes
        self.ao_alterar = ao_alterar
        ttk.Label(self, text="Movimentações", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            self, text="Registre compras, vendas e outros ajustes de saldo.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(3, 0))
        formulario = ttk.LabelFrame(
            self, text="Entrada ou saída de estoque", padding=18, style="Card.TLabelframe"
        )
        formulario.pack(fill="x", pady=14)
        ttk.Label(formulario, text="Produto").grid(row=0, column=0, sticky="w", pady=6)
        self.produto = ttk.Combobox(formulario, state="readonly", width=42)
        self.produto.grid(row=0, column=1, sticky="ew", padx=10, pady=6)
        self.codigos = {}
        ttk.Button(formulario, text="Ler código de barras", command=self._ler_codigo).grid(
            row=0, column=2, padx=4
        )
        ttk.Label(formulario, text="Tipo").grid(row=1, column=0, sticky="w", pady=6)
        self.tipo = ttk.Combobox(formulario, values=("entrada", "saida"), state="readonly")
        self.tipo.current(0)
        self.tipo.grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        ttk.Label(formulario, text="Quantidade").grid(row=2, column=0, sticky="w", pady=6)
        self.quantidade = ttk.Entry(formulario)
        self.quantidade.grid(row=2, column=1, sticky="ew", padx=10, pady=6)
        ttk.Button(
            formulario, text="Registrar movimentação", style="Primary.TButton",
            command=self._registrar,
        ).grid(
            row=3, column=1, sticky="ew", padx=10, pady=(10, 4)
        )
        formulario.columnconfigure(1, weight=1)
        ttk.Label(self, text="Histórico recente", style="SectionTitle.TLabel").pack(
            anchor="w", pady=(8, 0)
        )
        self.tabela = ttk.Treeview(
            self, columns=("data", "codigo", "nome", "tipo", "quantidade"),
            show="headings", height=14,
        )
        for coluna, titulo, largura in (
            ("data", "Data", 170), ("codigo", "Código", 120), ("nome", "Produto", 250),
            ("tipo", "Tipo", 100), ("quantidade", "Quantidade", 110),
        ):
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=largura)
        self.tabela.tag_configure("par", background="#f7f9fc")
        self.tabela.pack(fill="both", expand=True, pady=(8, 0))
        self.atualizar()

    def atualizar(self):
        itens = self.produtos.listar()
        self.codigos = {f"{p['codigo']} - {p['nome']}": p["codigo"] for p in itens}
        atual = self.produto.get()
        self.produto["values"] = list(self.codigos)
        if atual in self.codigos:
            self.produto.set(atual)
        elif self.codigos:
            self.produto.current(0)
        else:
            self.produto.set("")
        self.tabela.delete(*self.tabela.get_children())
        for indice, mov in enumerate(self.movimentacoes.listar(limite=100)):
            self.tabela.insert(
                "", "end",
                values=(mov["data"], mov["codigo"], mov["nome"],
                        mov["tipo"], mov["quantidade"]),
                tags=("par",) if indice % 2 else (),
            )

    def _ler_codigo(self):
        iniciar_leitor(self, self._preencher_codigo)

    def _preencher_codigo(self, codigo):
        for rotulo, produto_codigo in self.codigos.items():
            if produto_codigo == codigo:
                self.produto.set(rotulo)
                return
        messagebox.showwarning(
            "Produto não encontrado",
            f"Nenhum produto cadastrado com o código {codigo}.",
            parent=self,
        )

    def _registrar(self):
        rotulo = self.produto.get()
        if not rotulo or rotulo not in self.codigos:
            messagebox.showwarning("Produto", "Cadastre e selecione um produto.", parent=self)
            return
        try:
            quantidade = validar_movimentacao(self.quantidade.get())
            self.movimentacoes.registrar(
                self.codigos[rotulo], self.tipo.get(), quantidade
            )
        except ValueError as erro:
            messagebox.showwarning("Validação", str(erro), parent=self)
            return
        except sqlite3.IntegrityError as erro:
            messagebox.showerror("Movimentação não registrada", str(erro), parent=self)
            return
        self.quantidade.delete(0, "end")
        self.atualizar()
        self.ao_alterar()
        messagebox.showinfo("Sucesso", "Movimentação registrada.", parent=self)

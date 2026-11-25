import tkinter as tk
from tkinter import ttk


class ConsultaEstoque(ttk.Frame):
    def __init__(self, parent, produtos):
        super().__init__(parent, padding=28, style="Page.TFrame")
        self.produtos = produtos
        ttk.Label(self, text="Estoque atual", style="PageTitle.TLabel").pack(anchor="w")
        filtros = ttk.Frame(self)
        filtros.pack(fill="x", pady=12)
        ttk.Label(filtros, text="Categoria").pack(side="left")
        self.filtro = ttk.Combobox(filtros, state="readonly", width=28)
        self.filtro.pack(side="left", padx=8)
        self.filtro.bind("<<ComboboxSelected>>", lambda _evento: self.atualizar())
        ttk.Button(filtros, text="Todas", command=self._todas).pack(side="left")
        self.valor = ttk.Label(filtros, font=("Segoe UI", 11, "bold"))
        self.valor.pack(side="right")
        self.tabela = ttk.Treeview(
            self, columns=("codigo", "nome", "categoria", "preco", "quantidade", "total", "status"),
            show="headings", height=20,
        )
        for coluna, titulo, largura in (
            ("codigo", "Código", 100), ("nome", "Produto", 210),
            ("categoria", "Categoria", 130), ("preco", "Preço unit.", 100),
            ("quantidade", "Quantidade", 90), ("total", "Valor estoque", 120),
            ("status", "Situação", 125),
        ):
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=largura)
        self.tabela.tag_configure("baixo", background="#fff0d6")
        self.tabela.tag_configure("par", background="#f7f9fc")
        self.tabela.pack(fill="both", expand=True)
        self.atualizar()

    def atualizar(self):
        categorias = ["Todas"] + self.produtos.categorias()
        self.filtro["values"] = categorias
        if self.filtro.get() not in categorias:
            self.filtro.set("Todas")
        categoria = self.filtro.get()
        itens = self.produtos.listar(None if categoria == "Todas" else categoria)
        self.tabela.delete(*self.tabela.get_children())
        total_estoque = 0
        for indice, produto in enumerate(itens):
            total = produto["preco"] * produto["quantidade"]
            total_estoque += total
            baixo = produto["quantidade"] <= produto["estoque_minimo"]
            self.tabela.insert(
                "", "end", values=(
                    produto["codigo"], produto["nome"], produto["categoria"],
                    f"R$ {produto['preco']:.2f}", produto["quantidade"],
                    f"R$ {total:.2f}", "ESTOQUE BAIXO" if baixo else "Normal",
                ), tags=("baixo",) if baixo else (("par",) if indice % 2 else ()),
            )
        self.valor.configure(text=f"Valor em estoque: R$ {total_estoque:.2f}")

    def _todas(self):
        self.filtro.set("Todas")
        self.atualizar()

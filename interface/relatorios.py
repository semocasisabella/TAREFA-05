import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from utilitarios.exportacao import exportar_csv


class Relatorios(ttk.Frame):
    def __init__(self, parent, produtos, movimentacoes):
        super().__init__(parent, padding=28, style="Page.TFrame")
        self.produtos = produtos
        self.movimentacoes = movimentacoes
        ttk.Label(self, text="Relatórios", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            self, text="Consulte e exporte o histórico de movimentações.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(3, 0))
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=12)
        ttk.Label(barra, text="Categoria").pack(side="left")
        self.filtro = ttk.Combobox(barra, state="readonly", width=28)
        self.filtro.pack(side="left", padx=8)
        self.filtro.bind("<<ComboboxSelected>>", lambda _evento: self.atualizar())
        ttk.Button(
            barra, text="Exportar CSV", style="Primary.TButton", command=self._exportar
        ).pack(side="right")
        self.tabela = ttk.Treeview(
            self, columns=("data", "codigo", "nome", "categoria", "tipo", "quantidade", "valor"),
            show="headings", height=20,
        )
        for coluna, titulo, largura in (
            ("data", "Data", 165), ("codigo", "Código", 95), ("nome", "Produto", 190),
            ("categoria", "Categoria", 120), ("tipo", "Tipo", 90),
            ("quantidade", "Quantidade", 100), ("valor", "Valor movimento", 125),
        ):
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=largura)
        self.tabela.tag_configure("par", background="#f7f9fc")
        self.tabela.pack(fill="both", expand=True)
        self.atualizar()

    def atualizar(self):
        categorias = ["Todas"] + self.produtos.categorias()
        self.filtro["values"] = categorias
        if self.filtro.get() not in categorias:
            self.filtro.set("Todas")
        categoria = self.filtro.get()
        movimentos = self.movimentacoes.listar(
            None if categoria == "Todas" else categoria, limite=5000
        )
        self.tabela.delete(*self.tabela.get_children())
        for indice, mov in enumerate(movimentos):
            self.tabela.insert(
                "", "end", values=(
                    mov["data"], mov["codigo"], mov["nome"], mov["categoria"],
                    mov["tipo"], mov["quantidade"],
                    f"R$ {mov['preco'] * mov['quantidade']:.2f}",
                ), tags=("par",) if indice % 2 else (),
            )

    def _exportar(self):
        categoria = self.filtro.get()
        movimentos = self.movimentacoes.listar(
            None if categoria == "Todas" else categoria, limite=5000
        )
        caminho = filedialog.asksaveasfilename(
            parent=self, title="Exportar relatório", defaultextension=".csv",
            filetypes=(("Arquivo CSV", "*.csv"),),
            initialfile="relatorio_estoque.csv",
        )
        if not caminho:
            return
        try:
            exportar_csv(
                caminho,
                ("Data", "Código", "Produto", "Categoria", "Tipo", "Quantidade", "Valor"),
                ((m["data"], m["codigo"], m["nome"], m["categoria"], m["tipo"],
                  m["quantidade"], f"{m['preco'] * m['quantidade']:.2f}") for m in movimentos),
            )
        except OSError as erro:
            messagebox.showerror("Erro ao exportar", str(erro), parent=self)
            return
        messagebox.showinfo("Exportação concluída", f"Arquivo salvo em:\n{caminho}", parent=self)

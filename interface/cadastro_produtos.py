import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from utilitarios.validacoes import validar_produto


class CadastroProdutos(ttk.Frame):
    def __init__(self, parent, produtos, ao_alterar):
        super().__init__(parent, padding=28, style="Page.TFrame")
        self.produtos = produtos
        self.ao_alterar = ao_alterar
        ttk.Label(self, text="Produtos", style="PageTitle.TLabel").pack(anchor="w")
        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=12)
        ttk.Button(
            botoes, text="＋  Novo produto", style="Primary.TButton", command=self._novo
        ).pack(side="left")
        ttk.Button(botoes, text="Editar selecionado", command=self._editar).pack(side="left", padx=8)
        ttk.Button(botoes, text="Excluir selecionado", command=self._excluir).pack(side="left")
        self.tabela = ttk.Treeview(
            self, columns=("codigo", "nome", "categoria", "preco", "quantidade", "minimo"),
            show="headings", height=18,
        )
        titulos = {
            "codigo": "Código", "nome": "Produto", "categoria": "Categoria",
            "preco": "Preço", "quantidade": "Quantidade", "minimo": "Estoque mínimo",
        }
        larguras = {"codigo": 120, "nome": 230, "categoria": 150, "preco": 100,
                    "quantidade": 100, "minimo": 120}
        for coluna, titulo in titulos.items():
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=larguras[coluna], anchor="w")
        self.tabela.tag_configure("par", background="#f7f9fc")
        self.tabela.pack(fill="both", expand=True)
        self.atualizar()

    def atualizar(self):
        self.tabela.delete(*self.tabela.get_children())
        for indice, produto in enumerate(self.produtos.listar()):
            self.tabela.insert(
                "", "end", iid=produto["codigo"],
                values=(produto["codigo"], produto["nome"], produto["categoria"],
                        f"R$ {produto['preco']:.2f}", produto["quantidade"],
                        produto["estoque_minimo"]),
                tags=("par",) if indice % 2 else (),
            )

    def _selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showinfo("Seleção", "Selecione um produto primeiro.", parent=self)
            return None
        return self.produtos.obter(selecao[0])

    def _dialogo(self, produto=None):
        janela = tk.Toplevel(self)
        janela.title("Editar produto" if produto else "Novo produto")
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        janela.columnconfigure(1, weight=1)
        campos = {}
        dados = {
            "Código": produto["codigo"] if produto else "",
            "Nome": produto["nome"] if produto else "",
            "Categoria": produto["categoria"] if produto else "",
            "Preço": str(produto["preco"]) if produto else "",
            "Estoque mínimo": str(produto["estoque_minimo"]) if produto else "5",
        }
        for indice, (rotulo, valor) in enumerate(dados.items()):
            ttk.Label(janela, text=rotulo).grid(row=indice, column=0, sticky="w", padx=12, pady=6)
            campo = ttk.Entry(janela, width=32)
            campo.insert(0, valor)
            campo.grid(row=indice, column=1, sticky="ew", padx=12, pady=6)
            campos[rotulo] = campo
            if produto and rotulo == "Código":
                campo.state(["readonly"])

        def salvar():
            try:
                codigo, nome, preco, minimo = validar_produto(
                    campos["Código"].get(), campos["Nome"].get(),
                    campos["Preço"].get(), campos["Estoque mínimo"].get(),
                )
                self.produtos.salvar(
                    codigo, nome, campos["Categoria"].get().strip(),
                    preco, minimo, produto["codigo"] if produto else None,
                )
            except ValueError as erro:
                messagebox.showwarning("Validação", str(erro), parent=janela)
                return
            except sqlite3.IntegrityError as erro:
                messagebox.showerror(
                    "Não foi possível salvar",
                    "O código já está cadastrado ou o produto possui movimentações "
                    "vinculadas e não pode ser renomeado.\n\n" + str(erro),
                    parent=janela,
                )
                return
            janela.destroy()
            self.atualizar()
            self.ao_alterar()

        ttk.Button(janela, text="Salvar", command=salvar).grid(
            row=len(dados), column=0, columnspan=2, sticky="ew", padx=12, pady=12
        )

    def _novo(self):
        self._dialogo()

    def _editar(self):
        produto = self._selecionado()
        if produto:
            self._dialogo(produto)

    def _excluir(self):
        produto = self._selecionado()
        if not produto or not messagebox.askyesno(
            "Confirmar exclusão", f"Excluir {produto['nome']}?", parent=self
        ):
            return
        try:
            self.produtos.excluir(produto["codigo"])
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Produto em uso",
                "Este produto possui movimentações no histórico e não pode ser excluído.",
                parent=self,
            )
            return
        self.atualizar()
        self.ao_alterar()

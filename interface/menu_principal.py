from tkinter import messagebox, ttk

from interface.cadastro_produtos import CadastroProdutos
from interface.consulta_estoque import ConsultaEstoque
from interface.registro_movimentacao import RegistroMovimentacao
from interface.relatorios import Relatorios


class MenuPrincipal(ttk.Frame):
    def __init__(self, parent, banco, produtos, movimentacoes, usuario):
        super().__init__(parent, style="Page.TFrame")
        self.banco = banco
        self.produtos = produtos
        self.movimentacoes = movimentacoes
        self.usuario = usuario
        self.pagina = None
        self._montar()
        self.mostrar("Dashboard")

    def _montar(self):
        barra = ttk.Frame(self, padding=(24, 15), style="Topbar.TFrame")
        barra.pack(fill="x")
        marca = ttk.Frame(barra, style="Topbar.TFrame")
        marca.pack(side="left")
        ttk.Label(marca, text="ESTOQUE", style="Brand.TLabel").pack(anchor="w")
        ttk.Label(
            marca, text="CONTROLE E MOVIMENTAÇÃO", style="HeaderMeta.TLabel"
        ).pack(anchor="w", pady=(2, 0))
        ttk.Label(
            barra, text=f"●  {self.usuario}", style="HeaderMeta.TLabel"
        ).pack(side="right")
        corpo = ttk.Frame(self)
        corpo.pack(fill="both", expand=True)
        self.navegacao = ttk.Frame(corpo, padding=(12, 22), style="Sidebar.TFrame")
        self.navegacao.pack(side="left", fill="y")
        ttk.Label(
            self.navegacao, text="MENU PRINCIPAL", style="SidebarMeta.TLabel"
        ).pack(anchor="w", padx=12, pady=(2, 12))
        self.conteudo = ttk.Frame(corpo, style="Page.TFrame")
        self.conteudo.pack(side="left", fill="both", expand=True)
        self.botoes_navegacao = {}
        for titulo in ("Dashboard", "Produtos", "Movimentações", "Estoque", "Relatórios"):
            botao = ttk.Button(
                self.navegacao,
                text=f"   {titulo}",
                width=20,
                style="Nav.TButton",
                command=lambda item=titulo: self.mostrar(item),
            )
            botao.pack(fill="x", pady=3)
            self.botoes_navegacao[titulo] = botao

    def mostrar(self, nome):
        if self.pagina is not None:
            self.pagina.destroy()
        for titulo, botao in self.botoes_navegacao.items():
            botao.configure(style="NavActive.TButton" if titulo == nome else "Nav.TButton")
        construtores = {
            "Produtos": lambda: CadastroProdutos(
                self.conteudo, self.produtos, self._atualizar_pagina
            ),
            "Movimentações": lambda: RegistroMovimentacao(
                self.conteudo, self.produtos, self.movimentacoes, self._atualizar_pagina
            ),
            "Estoque": lambda: ConsultaEstoque(self.conteudo, self.produtos),
            "Relatórios": lambda: Relatorios(
                self.conteudo, self.produtos, self.movimentacoes
            ),
            "Dashboard": self._dashboard,
        }
        self.pagina = construtores[nome]()
        self.pagina.pack(fill="both", expand=True)

    def _atualizar_pagina(self):
        self.mostrar("Dashboard") if self.pagina is None else self.pagina.atualizar()

    def _dashboard(self):
        pagina = ttk.Frame(self.conteudo, padding=28, style="Page.TFrame")
        ttk.Label(pagina, text="Visão geral", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            pagina, text="Resumo atualizado do seu estoque.", style="Muted.TLabel"
        ).pack(anchor="w", pady=(3, 0))
        resumo = self.produtos.resumo()
        indicadores = ttk.Frame(pagina)
        indicadores.pack(fill="x", pady=(22, 24))
        for rotulo, valor in (
            ("PRODUTOS", resumo["produtos"]),
            ("UNIDADES", resumo["unidades"]),
            ("VALOR EM ESTOQUE", f"R$ {resumo['valor']:.2f}"),
            ("ESTOQUE BAIXO", resumo["baixos"]),
        ):
            cartao = ttk.LabelFrame(
                indicadores, text=rotulo, padding=(16, 14), style="Card.TLabelframe"
            )
            cartao.pack(side="left", fill="both", expand=True, padx=(0, 10))
            ttk.Label(cartao, text=str(valor), style="Metric.TLabel").pack(anchor="w")
        alertas = ttk.LabelFrame(
            pagina, text="  Alertas de estoque baixo  ", padding=16,
            style="Warning.TLabelframe",
        )
        alertas.pack(fill="x")
        baixos = self.produtos.listar_baixo_estoque()
        if baixos:
            for item in baixos[:8]:
                ttk.Label(
                    alertas,
                    style="Warning.TLabel",
                    text=f"{item['nome']}  ·  {item['codigo']}  —  "
                         f"{item['quantidade']} un. / mínimo {item['estoque_minimo']}",
                ).pack(anchor="w", pady=3)
        else:
            ttk.Label(
                alertas, text="Tudo certo — nenhum produto abaixo do estoque mínimo.",
                style="Warning.TLabel",
            ).pack(anchor="w")
        ttk.Button(
            pagina, text="Ver gráfico de estoque", style="Primary.TButton",
            command=self._grafico,
        ).pack(anchor="w", pady=(20, 0))
        return pagina

    def _grafico(self):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            messagebox.showerror(
                "Dependência ausente",
                "Para exibir gráficos, instale as dependências com: "
                "pip install -r requirements.txt",
                parent=self,
            )
            return
        itens = self.produtos.listar()
        if not itens:
            messagebox.showinfo("Gráfico", "Cadastre produtos para ver o gráfico.", parent=self)
            return
        selecionados = sorted(itens, key=lambda item: item["quantidade"], reverse=True)[:12]
        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.bar(
            [item["nome"] for item in selecionados],
            [item["quantidade"] for item in selecionados],
            color="#2a7f9e",
        )
        eixo.set_title("Unidades disponíveis por produto")
        eixo.set_ylabel("Quantidade")
        eixo.tick_params(axis="x", labelrotation=35)
        figura.tight_layout()
        plt.show()

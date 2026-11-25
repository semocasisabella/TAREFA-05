from tkinter import ttk


CORES = {
    "fundo": "#f3f6fb",
    "superficie": "#ffffff",
    "texto": "#172033",
    "suave": "#68758a",
    "borda": "#e1e7f0",
    "primaria": "#147d92",
    "primaria_escura": "#106578",
    "nav": "#142238",
    "nav_hover": "#20334f",
    "alerta": "#fff3dc",
    "alerta_texto": "#8a5700",
    "sucesso": "#e4f5ef",
    "sucesso_texto": "#176b50",
}


def configurar_tema(raiz):
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")

    estilo.configure(
        ".",
        background=CORES["fundo"],
        foreground=CORES["texto"],
        font=("Segoe UI", 10),
    )
    estilo.configure("TFrame", background=CORES["fundo"])
    estilo.configure("TLabel", background=CORES["fundo"], foreground=CORES["texto"])
    estilo.configure("Page.TFrame", background=CORES["fundo"])
    estilo.configure("LoginCard.TFrame", background=CORES["superficie"])
    estilo.configure(
        "LoginBrand.TLabel",
        background=CORES["superficie"],
        foreground=CORES["primaria"],
        font=("Segoe UI", 13, "bold"),
    )
    estilo.configure(
        "LoginHeading.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 18, "bold"),
    )
    estilo.configure(
        "LoginSubtitle.TLabel",
        background=CORES["superficie"],
        foreground=CORES["suave"],
    )
    estilo.configure(
        "LoginField.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 9, "bold"),
    )
    estilo.configure("Topbar.TFrame", background=CORES["superficie"])
    estilo.configure("Sidebar.TFrame", background=CORES["nav"])
    estilo.configure(
        "Brand.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 15, "bold"),
    )
    estilo.configure(
        "HeaderMeta.TLabel",
        background=CORES["superficie"],
        foreground=CORES["suave"],
        font=("Segoe UI", 9),
    )
    estilo.configure(
        "SidebarTitle.TLabel",
        background=CORES["nav"],
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
    )
    estilo.configure(
        "SidebarMeta.TLabel",
        background=CORES["nav"],
        foreground="#aab8ca",
        font=("Segoe UI", 9),
    )
    estilo.configure(
        "PageTitle.TLabel",
        background=CORES["fundo"],
        foreground=CORES["texto"],
        font=("Segoe UI", 21, "bold"),
    )
    estilo.configure(
        "SectionTitle.TLabel",
        background=CORES["fundo"],
        foreground=CORES["texto"],
        font=("Segoe UI", 13, "bold"),
    )
    estilo.configure(
        "Muted.TLabel",
        background=CORES["fundo"],
        foreground=CORES["suave"],
    )
    estilo.configure(
        "TButton",
        padding=(12, 8),
        background=CORES["superficie"],
        foreground=CORES["texto"],
        borderwidth=0,
        focusthickness=2,
        focuscolor=CORES["primaria"],
    )
    estilo.map(
        "TButton",
        background=[("pressed", "#dce5ef"), ("active", "#e9eff6")],
    )
    estilo.configure(
        "Primary.TButton",
        background=CORES["primaria"],
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
    )
    estilo.map(
        "Primary.TButton",
        background=[
            ("pressed", CORES["primaria_escura"]),
            ("active", CORES["primaria_escura"]),
        ],
        foreground=[("disabled", "#d5e0e4")],
    )
    estilo.configure(
        "Nav.TButton",
        anchor="w",
        padding=(14, 11),
        background=CORES["nav"],
        foreground="#cbd5e1",
        font=("Segoe UI", 10),
    )
    estilo.map(
        "Nav.TButton",
        background=[("active", CORES["nav_hover"])],
        foreground=[("active", "#ffffff")],
    )
    estilo.configure(
        "NavActive.TButton",
        anchor="w",
        padding=(14, 11),
        background=CORES["nav_hover"],
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
    )
    estilo.map("NavActive.TButton", background=[("active", CORES["nav_hover"])])
    estilo.configure(
        "TEntry",
        padding=(10, 8),
        fieldbackground=CORES["superficie"],
        foreground=CORES["texto"],
        bordercolor=CORES["borda"],
        lightcolor=CORES["borda"],
        darkcolor=CORES["borda"],
    )
    estilo.configure(
        "TCombobox",
        padding=(8, 6),
        fieldbackground=CORES["superficie"],
        background=CORES["superficie"],
        foreground=CORES["texto"],
        arrowcolor=CORES["suave"],
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", CORES["superficie"])],
        foreground=[("readonly", CORES["texto"])],
    )
    estilo.configure(
        "TLabelframe",
        background=CORES["superficie"],
        bordercolor=CORES["borda"],
        relief="solid",
        borderwidth=1,
    )
    estilo.configure(
        "TLabelframe.Label",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 10, "bold"),
    )
    estilo.configure(
        "Card.TLabelframe",
        background=CORES["superficie"],
        bordercolor=CORES["borda"],
        relief="solid",
        borderwidth=1,
    )
    estilo.configure(
        "Card.TLabelframe.Label",
        background=CORES["superficie"],
        foreground=CORES["suave"],
        font=("Segoe UI", 9, "bold"),
    )
    estilo.configure(
        "Metric.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 19, "bold"),
    )
    estilo.configure(
        "Warning.TLabelframe",
        background=CORES["alerta"],
        bordercolor="#f0d9a8",
        relief="solid",
        borderwidth=1,
    )
    estilo.configure(
        "Warning.TLabelframe.Label",
        background=CORES["alerta"],
        foreground=CORES["alerta_texto"],
        font=("Segoe UI", 10, "bold"),
    )
    estilo.configure(
        "Warning.TLabel",
        background=CORES["alerta"],
        foreground=CORES["alerta_texto"],
    )
    estilo.configure(
        "Success.TLabel",
        background=CORES["sucesso"],
        foreground=CORES["sucesso_texto"],
        padding=(12, 10),
    )
    estilo.configure(
        "Treeview",
        background=CORES["superficie"],
        fieldbackground=CORES["superficie"],
        foreground=CORES["texto"],
        rowheight=32,
        borderwidth=0,
        font=("Segoe UI", 9),
    )
    estilo.map(
        "Treeview",
        background=[("selected", "#d9eef2")],
        foreground=[("selected", CORES["texto"])],
    )
    estilo.configure(
        "Treeview.Heading",
        background="#eaf0f6",
        foreground="#445168",
        padding=(10, 9),
        font=("Segoe UI", 9, "bold"),
        relief="flat",
    )
    estilo.map("Treeview.Heading", background=[("active", "#dfe7f0")])
    estilo.configure("TSeparator", background=CORES["borda"])
    raiz.configure(background=CORES["fundo"])

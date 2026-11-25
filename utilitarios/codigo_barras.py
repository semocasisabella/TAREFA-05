import tkinter as tk
from tkinter import messagebox, ttk


def iniciar_leitor(parent, ao_ler):
    try:
        import cv2
        from PIL import Image, ImageTk
        from pyzbar.pyzbar import decode
    except (ImportError, OSError) as erro:
        messagebox.showerror(
            "Leitor de código de barras",
            "O leitor exige as dependências opcionais opencv-python, Pillow e "
            "pyzbar, além da biblioteca nativa ZBar.\n\n"
            "Instale os pacotes e verifique a instalação do ZBar.\n\n"
            f"Detalhe: {erro}",
            parent=parent,
        )
        return

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera.release()
        messagebox.showerror("Webcam", "Não foi possível abrir a webcam.", parent=parent)
        return

    janela = tk.Toplevel(parent)
    janela.title("Leitor de código de barras")
    janela.transient(parent)
    visualizacao = ttk.Label(janela, text="Aponte a webcam para um código de barras")
    visualizacao.pack(padx=12, pady=12)
    estado = {"ativa": True}

    def fechar():
        estado["ativa"] = False
        camera.release()
        janela.destroy()

    def atualizar():
        if not janela.winfo_exists():
            return
        sucesso, quadro = camera.read()
        if not sucesso:
            fechar()
            messagebox.showerror("Webcam", "Falha ao capturar imagem da webcam.", parent=parent)
            return
        codigos = decode(quadro)
        if codigos:
            codigo = codigos[0].data.decode("utf-8", errors="replace")
            fechar()
            ao_ler(codigo)
            return
        rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
        imagem = ImageTk.PhotoImage(Image.fromarray(rgb))
        visualizacao.configure(image=imagem, text="")
        visualizacao.image = imagem
        if estado["ativa"]:
            janela.after(30, atualizar)

    janela.protocol("WM_DELETE_WINDOW", fechar)
    janela.after(0, atualizar)

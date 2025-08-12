import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class OrganizacaoBaixas():
    def __init__(self, master):
        self.janela = master

    def org_baixas(self):
        self.tpl_org_baixas = ttk.Toplevel(self.janela)
        self.tpl_org_baixas.title("Organização de Baixas")
        self.tpl_org_baixas.geometry("800x600")

        # ----- Cabeçalho azul claro -----
        cabecalho_frame = ttk.Frame(self.tpl_org_baixas)
        cabecalho_frame.pack(fill=X)
        cabecalho_frame.configure(style='MyHeader.TFrame')

        # ----- Estilo de cor customizada para o cabeçalho -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

        titulo = ttk.Label(
            cabecalho_frame,
            text="Organização de Baixas",
            font=("Inconsolata", 15, "bold"),
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de'
        )
        titulo.pack(expand=True, padx=10, pady=10)
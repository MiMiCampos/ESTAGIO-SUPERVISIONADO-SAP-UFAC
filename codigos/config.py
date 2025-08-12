import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


class Configuracoes():
    def __init__(self, master):
        self.janela = master
    
    def configuracao(self):

        self.tpl_config = ttk.Toplevel(self.janela)
        self.tpl_config.title("Configurações")
        self.tpl_config.geometry("800x600")

        # ----- Cabeçalho azul claro -----
        cabecalho_frame = ttk.Frame(self.tpl_config)
        cabecalho_frame.pack(fill=X)
        cabecalho_frame.configure(style='MyHeader.TFrame')

        # ----- Estilo de cor customizada para o cabeçalho -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

        titulo = ttk.Label(
            cabecalho_frame,
            text="Configurações do Sistema",
            font=("Inconsolata", 15, "bold"),
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de'
        )
        titulo.pack(expand=True, padx=10, pady=10)
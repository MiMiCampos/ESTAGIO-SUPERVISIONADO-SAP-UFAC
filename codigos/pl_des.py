import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class PlanilhaDesfazimento():
    def __init__(self, master):
        self.janela = master

    def planilha_des(self):
        self.tpl_planilha_des = ttk.Toplevel(self.janela)
        self.tpl_planilha_des.title("Planilha de Desfazimento")
        self.tpl_planilha_des.geometry("800x600")

        # ----- Cabeçalho azul claro -----
        cabecalho_frame = ttk.Frame(self.tpl_planilha_des)
        cabecalho_frame.pack(fill=X)
        cabecalho_frame.configure(style='MyHeader.TFrame')

        # ----- Estilo de cor customizada para o cabeçalho -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

        titulo = ttk.Label(
            cabecalho_frame,
            text="Planilha de Desfazimento",
            font=("Inconsolata", 15, "bold"),
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de'
        )
        titulo.pack(expand=True, padx=10, pady=10)
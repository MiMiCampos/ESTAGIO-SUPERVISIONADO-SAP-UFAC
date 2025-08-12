import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class MenuInicial(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("SAP-UFAC - Menu Inicial")
        self.geometry("1000x600")
        # self.resizable(False, False) # Bloqueia o redimensionamento (impede que aumente ou diminua)

        # ----- Cabeçalho azul claro -----
        cabecalho_frame = ttk.Frame(self)
        cabecalho_frame.pack(fill=X)
        cabecalho_frame.configure(style='MyHeader.TFrame')
        
        # ----- Estilo de cor customizada para o cabeçalho -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
            brasao_label = ttk.Label(cabecalho_frame, image=self.brasao)
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        except:
            brasao_label = ttk.Label(cabecalho_frame, text="[BRASÃO]")
            brasao_label.pack(side=LEFT, padx=10, pady=5)

        titulo = ttk.Label(
            cabecalho_frame,
            text="SISTEMA DE AUTOMAÇÃO PATRIMONIAL DA UNIVERSIDADE FEDERAL DO ACRE (SAP-UFAC)",
            font=("Inconsolata", 15, "bold"),            
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de' # Azulzinho padrão da ferramenta
        )
        titulo.pack(expand=True, padx=10, pady=10)

        # ----- Mensagem de boas-vindas -----
        lbl_bem_vindo = ttk.Label(self, text="BEM VINDO!", font=("Inconsolata", 14, "bold"))
        lbl_bem_vindo.pack(pady=20)

        # ----- Área de botões -----
        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(pady=10)

        self.criar_botao(botoes_frame, "Planilha de Desfazimento", "assets/planilha.png", self.acao_planilha, 0, 0)
        self.criar_botao(botoes_frame, "Organização de Baixas", "assets/organizacao.png", self.acao_organizacao, 0, 1)
        self.criar_botao(botoes_frame, "Gerar Documentos", "assets/documentos.png", self.acao_documentos, 1, 0)
        self.criar_botao(botoes_frame, "Configurações", "assets/config.png", self.acao_config, 1, 1)
        
        # ----- Rodapé azul claro -----
        rodape_frame = ttk.Frame(self)
        rodape_frame.pack(fill=X, ipady=30, side=BOTTOM)
        rodape_frame.configure(style='MyHeader.TFrame')
        
        # ----- Estilo de cor customizada para o rodapé -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

    def criar_botao(self, parent, texto, img_path, comando, linha, coluna):
        try:
            img = Image.open(img_path).resize((64, 64))
            icon = ImageTk.PhotoImage(img)
        except:
            icon = None

        btn = ttk.Button(
            parent,
            text=texto,
            image=icon,
            compound=TOP,
            bootstyle=SECONDARY,
            command=comando,
            width=20
        )
        btn.image = icon
        btn.grid(row=linha, column=coluna, padx=20, pady=20, ipadx=10, ipady=10)

    # ----- Funções simuladas -----
    def acao_planilha(self):
        print("Abrindo Planilha de Desfazimento...")

    def acao_organizacao(self):
        print("Abrindo Organização de Baixas...")

    def acao_documentos(self):
        print("Abrindo Gerar Documentos...")

    def acao_config(self):
        print("Abrindo Configurações...")

if __name__ == "__main__":
    app = MenuInicial()
    app.mainloop()
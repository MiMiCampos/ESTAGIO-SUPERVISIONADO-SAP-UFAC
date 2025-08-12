import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from config import Configuracao
from gerar_doc import Gerardoc
from org_baixa import OrganizacaoBaixas
from pl_des import PlanilhaDesfazimento

class MenuInicial():
    def __init__(self, master):
        self.janela = master
        self.janela.title("SAP-UFAC - Menu Inicial")
        self.janela.geometry("1000x600")

        # ------ Chamando outras telas -----
        self.config = Configuracao(self.janela)
        self.gerar_doc = Gerardoc(self.janela)
        self.org_baixa = OrganizacaoBaixas(self.janela)
        self.planilha_des = PlanilhaDesfazimento(self.janela)

        # ----- Estilo de cor customizada para o cabeçalho -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

        # ----- Estilo de cor customizada para os botões -----
        style_azul_btn = ttk.Style()
        style_azul_btn.configure('MyHeader.TButton', font = ("Inconsolata", 26) , background='#5bc0de')

        # ----- Cabeçalho azul claro -----
        self.frm_cabecalho = ttk.Frame(self.janela)
        self.frm_cabecalho.pack(fill=X)
        self.frm_cabecalho.configure(style='MyHeader.TFrame')


        # ----- Inserindo o brasão da UFAC -----
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
            brasao_label = ttk.Label(self.frm_cabecalho, image=self.brasao)
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        except:
            brasao_label = ttk.Label(self.frm_cabecalho, text="[BRASÃO]")
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        
        # ----- Título do sistema -----
        self.lbl_titulo = ttk.Label(self.frm_cabecalho, 
            text="SISTEMA DE AUTOMAÇÃO PATRIMONIAL DA UNIVERSIDADE FEDERAL DO ACRE (SAP-UFAC)",
            font=("Inconsolata", 15, "bold"),            
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de' # Azulzinho padrão da ferramenta
        )
        self.lbl_titulo.pack(expand=True, padx=10, pady=10)

        # ----- Rodapé azul claro -----
        self.frm_rodape = ttk.Frame(self.janela)
        self.frm_rodape.pack(fill=X, ipady=30, side=BOTTOM)
        self.frm_rodape.configure(style='MyHeader.TFrame')

        # ----- Mensagem de boas-vindas -----
        lbl_bem_vindo = ttk.Label(self.janela, text="BEM VINDO!", font=("Inconsolata", 30, "bold"))
        lbl_bem_vindo.pack(pady=20)

        # ----- Área de botões -----
        botoes_frame = ttk.Frame(self.janela)
        botoes_frame.pack(pady=10, expand=True)
        
        # Define largura igual para as colunas
        botoes_frame.grid_columnconfigure(0, minsize=250, weight=1)
        botoes_frame.grid_columnconfigure(1, minsize=250, weight=1)

        # Define altura igual para as linhas
        botoes_frame.grid_rowconfigure(0, minsize=120, weight=1)
        botoes_frame.grid_rowconfigure(1, minsize=120, weight=1)


        # ----- Criando botões -----
        self.btn_planilha_des = ttk.Button(botoes_frame, text="Planilha de Desfazimento", command=self.planilha_des.planilha_des)
        self.btn_planilha_des.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=30, sticky='ew')
        self.btn_planilha_des.configure(style='MyHeader.TButton')

        self.btn_org_baixas = ttk.Button(botoes_frame, text="Organização de Baixas", command=self.org_baixa.org_baixas)
        self.btn_org_baixas.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=30, sticky='ew')
        self.btn_org_baixas.configure(style='MyHeader.TButton')

        self.btn_gerar_docs = ttk.Button(botoes_frame, text="Gerar Documentos", command=self.gerar_doc.gerar_doc)
        self.btn_gerar_docs.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=30, sticky='ew')
        self.btn_gerar_docs.configure(style='MyHeader.TButton')

        self.btn_configuracoes = ttk.Button(botoes_frame, text="Configurações", command=self.config.configuracao)
        self.btn_configuracoes.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=30, sticky='ew')
        self.btn_configuracoes.configure(style='MyHeader.TButton')






janela = ttk.Window()
app = MenuInicial(janela)
janela.mainloop()
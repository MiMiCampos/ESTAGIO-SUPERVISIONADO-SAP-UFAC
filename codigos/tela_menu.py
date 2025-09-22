# Arquivo: tela_menu.py (Lógica Corrigida com Estilo Original dos Botões)

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox

from banco_dados.db_controller import DBController
from utils.path_helper import resource_path

class MenuInicial():
    def __init__(self, master, dados_usuario, on_logout):
        self.janela = master
        self.dados_usuario = dados_usuario
        self.on_logout = on_logout
        self.janela.title("SAP-UFAC - Menu Inicial")
        self.janela.geometry("1300x800")
        self.janela.position_center()
        
        self.db_controller = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        
        try:
            img_data_planilha = Image.open(resource_path("imagens/botao_planilha_desf.png")).resize((300, 175))
            self.img_planilha = ImageTk.PhotoImage(img_data_planilha, master=self.janela)

            img_data_baixas = Image.open(resource_path("imagens/botao_organizacao_baixas.png")).resize((300, 175))
            self.img_baixas = ImageTk.PhotoImage(img_data_baixas, master=self.janela)

            img_data_docs = Image.open(resource_path("imagens/botao_gerar_docs.png")).resize((300, 175))
            self.img_docs = ImageTk.PhotoImage(img_data_docs, master=self.janela)

            img_data_config = Image.open(resource_path("imagens/botao_config.png")).resize((300, 175))
            self.img_config = ImageTk.PhotoImage(img_data_config, master=self.janela)

        except Exception as e:
            Messagebox.show_error("Erro Crítico de Imagem", f"Não foi possível carregar os ícones dos botões.\n\nCausa provável: {e}")
            self.img_planilha = self.img_baixas = self.img_docs = self.img_config = None
        
        style_azul_btn = ttk.Style()
        style_azul_btn.configure('MyHeader.TButton', 
                                font=("Inconsolata", 14, "bold"), 
                                background='white', 
                                foreground="#5bc0de", 
                                borderwidth=5, 
                                padding=10, 
                                bordercolor='#5bc0de')

        self.frm_cabecalho = ttk.Frame(self.janela, bootstyle="info")
        self.frm_cabecalho.pack(fill=X)

        try:
            brasao_img_data = Image.open(resource_path("imagens/brasao_UFAC.png")).resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img_data, master=self.janela)
            brasao_label = ttk.Label(self.frm_cabecalho, image=self.brasao, bootstyle="info")
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        except:
            brasao_label = ttk.Label(self.frm_cabecalho, text="[BRASÃO]", bootstyle="inverse-info")
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        
        self.lbl_titulo = ttk.Label(self.frm_cabecalho, 
            text="SISTEMA DE AUTOMAÇÃO PATRIMONIAL DA UNIVERSIDADE FEDERAL DO ACRE (SAP-UFAC)",
            font=("Inconsolata", 16, "bold"),
            foreground="black",
            bootstyle="inverse-info"
        )
        self.lbl_titulo.pack(expand=True, padx=10, pady=10)

        self.frm_rodape = ttk.Frame(self.janela, bootstyle="info")
        self.frm_rodape.pack(fill=X, ipady=15, side=BOTTOM)
        
        btn_logout = ttk.Button(self.frm_rodape, text="Sair (Logout)", command=self._fazer_logout, bootstyle="info-outline")
        btn_logout.pack(side=RIGHT, padx=20)

        botoes_frame = ttk.Frame(self.janela)
        botoes_frame.pack(pady=10, padx=20, expand=True, fill=BOTH)
        
        botoes_frame.grid_columnconfigure((0, 3), weight=1)
        botoes_frame.grid_columnconfigure((1, 2), weight=0)
        botoes_frame.grid_rowconfigure((0, 4), weight=1)
        botoes_frame.grid_rowconfigure((1, 2, 3), weight=0)

        nome_usuario = self.dados_usuario['nome_completo']
        lbl_bem_vindo = ttk.Label(botoes_frame, text=f"BEM VINDO, {nome_usuario}!", font=("Inconsolata", 15, "bold"))
        lbl_bem_vindo.grid(row=0, column=1, columnspan=2, pady=(0, 20))

        perfil = self.dados_usuario['perfil']

        # Botões principais usam o estilo original 'MyHeader.TButton'
        self.btn_planilha_des = ttk.Button(botoes_frame, command=self.abrir_planilha_des, image=self.img_planilha, style='MyHeader.TButton')
        self.btn_planilha_des.image = self.img_planilha
        self.btn_planilha_des.grid(row=1, column=1, padx=10, pady=10)

        self.btn_org_baixas = ttk.Button(botoes_frame, command=self.abrir_organizacao_baixas, image=self.img_baixas, style='MyHeader.TButton')
        self.btn_org_baixas.image = self.img_baixas
        self.btn_org_baixas.grid(row=1, column=2, padx=10, pady=10)
        if perfil == 'Estagiário':
            self.btn_org_baixas.config(state=DISABLED)

        self.btn_gerar_docs = ttk.Button(botoes_frame, command=self.abrir_gerar_docs, image=self.img_docs, style='MyHeader.TButton')
        self.btn_gerar_docs.image = self.img_docs
        self.btn_gerar_docs.grid(row=2, column=1, padx=10, pady=10)
        if perfil == 'Estagiário':
            self.btn_gerar_docs.config(state=DISABLED)

        self.btn_configuracoes = ttk.Button(botoes_frame, command=self.abrir_config, image=self.img_config, style='MyHeader.TButton')
        self.btn_configuracoes.image = self.img_config
        self.btn_configuracoes.grid(row=2, column=2, padx=10, pady=10)
            
        if perfil == 'Administrador':
            self.btn_gerenciar_usuarios = ttk.Button(botoes_frame, text="Gerenciar Usuários", command=self.abrir_gerenciamento_usuarios, style='MyHeader.TButton')
            self.btn_gerenciar_usuarios.grid(row=3, column=1, columnspan=2, ipady=5, padx=8, sticky="ew")

    def _fazer_logout(self):
        self.on_logout()

    def abrir_planilha_des(self):
        from pl_des import PlanilhaDesfazimento
        PlanilhaDesfazimento(self.janela, self.db_controller, self).planilha_des()

    def abrir_organizacao_baixas(self):
        from org_baixa import OrganizacaoBaixas
        ultima_planilha_info = self.db_controller.get_ultima_planilha_criada()
        if ultima_planilha_info is None:
            Messagebox.show_warning("Nenhuma Planilha Encontrada", "Não há nenhuma planilha registrada no banco de dados para organizar.")
            return
        id_desfazimento = ultima_planilha_info['id_desfazimento']
        dados_brutos = self.db_controller.get_bens_por_desfazimento(id_desfazimento)
        if not dados_brutos:
            Messagebox.show_info("Planilha Vazia", "A última planilha criada ainda não contém nenhum bem para organizar.")
            return
        tela_baixas = OrganizacaoBaixas(
            self.janela,
            nome_planilha=ultima_planilha_info['nome'],
            dados_para_agrupar=dados_brutos,
            numero_processo=ultima_planilha_info['numero_processo'],
            id_desfazimento=id_desfazimento
        )
        tela_baixas.org_baixas()
        
    def abrir_gerar_docs(self):
        from gerar_doc import GerarDocumentos
        GerarDocumentos(self.janela, self.db_controller).gerar_doc()

    def abrir_config(self):
        from config import Configuracoes
        Configuracoes(self.janela, self.db_controller).configuracao()

    def abrir_gerenciamento_usuarios(self):
        from admin import GerenciadorUsuarios
        GerenciadorUsuarios(self.janela, self.db_controller, self.dados_usuario).exibir_tela()

    def fechar_aplicacao(self):
        if self.db_controller:
            self.db_controller.close_connection()
        self.janela.destroy()
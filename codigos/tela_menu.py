import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox

# Imports para as telas que serão abertas a partir do menu
from pl_des import PlanilhaDesfazimento
from org_baixa import OrganizacaoBaixas
from gerar_doc import GerarDocumentos
from config import Configuracoes
from admin import GerenciadorUsuarios

class MenuInicial():
    """
    Esta classe é responsável por criar e gerenciar todos os widgets
    da tela do menu principal.
    """
    def __init__(self, master, db_controller, dados_usuario, logout_callback):
        self.master = master
        self.db_controller = db_controller
        self.dados_usuario = dados_usuario
        self.logout_callback = logout_callback # Função para deslogar
        
        self.master.title("SAP-UFAC - Menu Inicial")
        self.master.geometry("1100x800")
        self.master.position_center()
        
        self._carregar_imagens()
        self._criar_widgets()

    def _carregar_imagens(self):
        """Carrega todas as imagens necessárias para o menu em atributos da classe."""
        try:
            self.img_planilha = ImageTk.PhotoImage(Image.open("imagens/botao_planilha_desf.png").resize((300, 175)))
            self.img_baixas = ImageTk.PhotoImage(Image.open("imagens/botao_organizacao_baixas.png").resize((300, 175)))
            self.img_docs = ImageTk.PhotoImage(Image.open("imagens/botao_gerar_docs.png").resize((300, 175)))
            self.img_config = ImageTk.PhotoImage(Image.open("imagens/botao_config.png").resize((300, 175)))
            self.brasao = ImageTk.PhotoImage(Image.open("imagens/brasao_UFAC.png").resize((50, 50)))
        except Exception as e:
            print(f"Erro ao carregar ícones do menu: {e}")
            self.img_planilha = self.img_baixas = self.img_docs = self.img_config = self.brasao = None

    def _criar_widgets(self):
        """Cria e posiciona todos os widgets do menu na tela."""
        style = ttk.Style()
        style.configure('MyHeader.TFrame', background='#5bc0de')
        style.configure('MyHeader.TButton', font=("Inconsolata", 14, "bold"), background='white', foreground="#5bc0de", borderwidth=5, padding=10, bordercolor='#5bc0de')

        # --- Criação dos Frames Principais ---
        frm_cabecalho = ttk.Frame(self.master, style='MyHeader.TFrame')
        frm_rodape = ttk.Frame(self.master, style='MyHeader.TFrame')
        botoes_frame = ttk.Frame(self.master)

        # --- Preenche o Cabeçalho ---
        if self.brasao:
            lbl_brasao = ttk.Label(frm_cabecalho, image=self.brasao)
            lbl_brasao.image = self.brasao
            lbl_brasao.pack(side=LEFT, padx=10, pady=5)
        lbl_titulo = ttk.Label(frm_cabecalho, 
            text="SISTEMA DE AUTOMAÇÃO PATRIMONIAL DA UNIVERSIDADE FEDERAL DO ACRE (SAP-UFAC)",
            font=("Inconsolata", 16, "bold"), bootstyle=INVERSE, foreground='black', background='#5bc0de')
        lbl_titulo.pack(expand=True, padx=10, pady=10)

        # --- Preenche o Rodapé ---
        btn_logout = ttk.Button(frm_rodape, text="Sair (Logout)", command=self.logout_callback, bootstyle="info-outline")
        btn_logout.pack(side=RIGHT, padx=20, pady=10)

        # --- Preenche o Corpo (botoes_frame) ---
        botoes_frame.grid_columnconfigure((0, 3), weight=1)
        botoes_frame.grid_rowconfigure((0, 4), weight=1)
        botoes_frame.grid_columnconfigure((1, 2), weight=0)
        botoes_frame.grid_rowconfigure((1, 2, 3), weight=0)
        
        nome_usuario = self.dados_usuario['nome_completo']
        lbl_bem_vindo = ttk.Label(botoes_frame, text=f"BEM VINDO, {nome_usuario}!", font=("Inconsolata", 15, "bold"))
        lbl_bem_vindo.grid(row=0, column=1, columnspan=2, pady=(0, 20))
        
        perfil = self.dados_usuario['perfil']

        # Botões com imagens e controle de permissão
        btn_planilha_des = ttk.Button(botoes_frame, command=self.abrir_planilha_des, image=self.img_planilha, style='MyHeader.TButton')
        btn_planilha_des.grid(row=1, column=1, padx=10, pady=10)
        btn_planilha_des.image = self.img_planilha

        btn_org_baixas = ttk.Button(botoes_frame, command=self.abrir_organizacao_baixas, image=self.img_baixas, style='MyHeader.TButton')
        btn_org_baixas.grid(row=1, column=2, padx=10, pady=10)
        btn_org_baixas.image = self.img_baixas
        if perfil == 'Estagiário': btn_org_baixas.config(state=DISABLED)

        btn_gerar_docs = ttk.Button(botoes_frame, command=self.abrir_gerar_docs, image=self.img_docs, style='MyHeader.TButton')
        btn_gerar_docs.grid(row=2, column=1, padx=10, pady=10)
        btn_gerar_docs.image = self.img_docs
        if perfil == 'Estagiário': btn_gerar_docs.config(state=DISABLED)

        btn_configuracoes = ttk.Button(botoes_frame, command=self.abrir_config, image=self.img_config, style='MyHeader.TButton')
        btn_configuracoes.grid(row=2, column=2, padx=10, pady=10)
        btn_configuracoes.image = self.img_config
        
        if perfil == 'Administrador':
            btn_gerenciar_usuarios = ttk.Button(botoes_frame, text="Gerenciar Usuários", command=self.abrir_gerenciamento_usuarios, style="MyHeader.TButton")
            btn_gerenciar_usuarios.grid(row=3, column=1, columnspan=2, pady=20, sticky="ew")

        # --- Ordem de Empacotamento Final ---
        frm_cabecalho.pack(side=TOP, fill=X)
        frm_rodape.pack(side=BOTTOM, fill=X)
        botoes_frame.pack(expand=True, fill=BOTH, padx=20, pady=10)

    # --- Métodos para abrir as outras telas ---
    def abrir_planilha_des(self):
        PlanilhaDesfazimento(self.master, self.db_controller, self).planilha_des()

    def abrir_organizacao_baixas(self):
        ultima_planilha_info = self.db_controller.get_ultima_planilha_criada()
        if not ultima_planilha_info:
            Messagebox.show_warning("Nenhuma Planilha Encontrada", "Não há nenhuma planilha registrada.")
            return
        dados_brutos = self.db_controller.get_bens_por_desfazimento(ultima_planilha_info['id_desfazimento'])
        if not dados_brutos:
            Messagebox.show_info("Planilha Vazia", "A última planilha não contém nenhum bem.")
            return
        tela_baixas = OrganizacaoBaixas(self.master, nome_planilha=ultima_planilha_info['nome'], dados_para_agrupar=dados_brutos)
        tela_baixas.org_baixas()
        
    def abrir_gerar_docs(self):
        GerarDocumentos(self.master, self.db_controller).gerar_doc()

    def abrir_config(self):
        Configuracoes(self.master, self.db_controller).configuracao()

    def abrir_gerenciamento_usuarios(self):
        GerenciadorUsuarios(self.master, self.db_controller, self.dados_usuario).exibir_tela()
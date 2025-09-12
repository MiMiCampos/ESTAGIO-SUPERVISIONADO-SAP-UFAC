import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox

# Novo controlador importado
from banco_dados.db_controller import DBController

from config import Configuracoes
from gerar_doc import GerarDocumentos
from org_baixa import OrganizacaoBaixas
from pl_des import PlanilhaDesfazimento
from utils.excel_formatador import FormatadorExcel

class MenuInicial():
    def __init__(self, master):
        self.janela = master
        self.janela.title("SAP-UFAC - Menu Inicial")
        self.janela.geometry("1100x700")
        
        self.janela.position_center()
        
        # ----- Única instância do controlador do banco de dados -----
        self.db_controller = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
                
        # Garante que a conexão seja fechada quando a janela principal fechar
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

        # ------ Chamando outras telas -----
        # Passando o controlador para as outras telas que precisam dele
        self.config = Configuracoes(self.janela) # Por enquanto não precisa do controlador
        self.gerar_doc = GerarDocumentos(self.janela, self.db_controller)
        self.org_baixa = OrganizacaoBaixas(self.janela) # Recebe dados, não o controlador diretamente
        self.planilha_desf = PlanilhaDesfazimento(self.janela, self.db_controller, self)
        
        # ----- Imagens dos botões iniciais -----
        try:
            self.img_planilha = ImageTk.PhotoImage(Image.open("imagens/botao_planilha_desf.png").resize((300, 175)))
            self.img_baixas = ImageTk.PhotoImage(Image.open("imagens/botao_organizacao_baixas.png").resize((300, 175)))
            self.img_docs = ImageTk.PhotoImage(Image.open("imagens/botao_gerar_docs.png").resize((300, 175)))
            self.img_config = ImageTk.PhotoImage(Image.open("imagens/botao_config.png").resize((300, 175)))
        except Exception as e:
            print(f"Erro ao carregar ícones: {e}")
            # Define como None para o programa não quebrar se não achar a imagem
            self.icon_planilha = self.icon_baixas = self.icon_docs = self.icon_config = None
        
        # ----- Estilo de cor customizada para o cabeçalho e o rodapé -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')

        # ----- Estilo de cor customizada para os botões -----
        style_azul_btn = ttk.Style()
        style_azul_btn.configure('MyHeader.TButton', font = ("Inconsolata", 26), background='white', foreground="#000000", borderwidth=5, padding=10, bordercolor='#5bc0de')

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
            font=("Inconsolata", 16, "bold"),            
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de' # Azulzinho padrão da ferramenta
        )
        self.lbl_titulo.pack(expand=True, padx=10, pady=10)

        # ----- Rodapé azul claro -----
        self.frm_rodape = ttk.Frame(self.janela)
        self.frm_rodape.pack(fill=X, ipady=30, side=BOTTOM)
        self.frm_rodape.configure(style='MyHeader.TFrame')

        # ----- Área de botões -----
        botoes_frame = ttk.Frame(self.janela)
        # O frame dos botões se expande para preencher a janela
        botoes_frame.pack(pady=10, padx=20, expand=True, fill=BOTH)
        
        # RESPONSIVIDADE: Centraliza o conteúdo em vez de expandi-lo.
        # As colunas 0 e 3 (nas bordas) irão expandir, absorvendo o espaço.
        botoes_frame.grid_columnconfigure((0, 3), weight=1)
        # As colunas 1 e 2 (onde os botões estão) não irão expandir.
        botoes_frame.grid_columnconfigure((1, 2), weight=0)

        # As linhas 0 e 4 (nas bordas) irão expandir para centralizar verticalmente.
        botoes_frame.grid_rowconfigure((0, 4), weight=1)
        # As linhas 1, 2 e 3 (para o conteúdo) não irão expandir.
        botoes_frame.grid_rowconfigure((1, 2, 3), weight=0)

        # ----- Mensagem de boas-vindas (MOVIDA PARA DENTRO DO GRID) -----
        lbl_bem_vindo = ttk.Label(botoes_frame, text="BEM VINDO!", font=("Inconsolata", 15, "bold"))
        lbl_bem_vindo.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # ----- Criando botões -----
        # Os botões estão nas colunas/linhas centrais (1 e 2)
        # e não usam 'sticky' para não expandir.
        self.btn_planilha_des = ttk.Button(botoes_frame, command=self.planilha_desf.planilha_des, image=self.img_planilha)
        self.btn_planilha_des.grid(row=1, column=1, padx=10, pady=10)
        self.btn_planilha_des.configure(style='MyHeader.TButton')

        self.btn_org_baixas = ttk.Button(botoes_frame, command=self.abrir_organizacao_baixas_da_ultima_planilha, image=self.img_baixas)
        self.btn_org_baixas.grid(row=1, column=2, padx=10, pady=10)
        self.btn_org_baixas.configure(style='MyHeader.TButton')

        self.btn_gerar_docs = ttk.Button(botoes_frame, command=self.gerar_doc.gerar_doc, image=self.img_docs)
        self.btn_gerar_docs.grid(row=2, column=1, padx=10, pady=10)
        self.btn_gerar_docs.configure(style='MyHeader.TButton')

        self.btn_configuracoes = ttk.Button(botoes_frame, command=self.config.configuracao, image=self.img_config)
        self.btn_configuracoes.grid(row=2, column=2, padx=10, pady=10)
        self.btn_configuracoes.configure(style='MyHeader.TButton')
   
    # --- NOVO: Método para o botão de Organização de Baixas ---
    def abrir_organizacao_baixas_da_ultima_planilha(self):
        """
        Abre a tela de organização de baixas com os dados da ÚLTIMA planilha criada no banco.
        """
        print("INFO: Buscando última planilha no BD para organizar baixas...")
        ultima_planilha_info = self.db_controller.get_ultima_planilha_criada()

        if ultima_planilha_info is None:
            Messagebox.show_warning("Nenhuma Planilha Encontrada", 
                                    "Não há nenhuma planilha registrada no banco de dados para organizar.")
            return
            
        id_desfazimento = ultima_planilha_info['id_desfazimento']
        dados_brutos = self.db_controller.get_bens_por_desfazimento(id_desfazimento)
        
        if not dados_brutos:
            Messagebox.show_info("Planilha Vazia", "A última planilha criada ainda não contém nenhum bem para organizar.")
            return

        tela_baixas = OrganizacaoBaixas(
            self.janela,
            nome_planilha=ultima_planilha_info['nome'],
            dados_para_agrupar=dados_brutos
        )
        tela_baixas.org_baixas()
        
    def fechar_aplicacao(self):
        """Função para fechar a conexão com o BD antes de sair."""
        if self.db_controller:
            self.db_controller.close_connection()
        self.janela.destroy()

janela = ttk.Window()
app = MenuInicial(janela)
janela.mainloop()
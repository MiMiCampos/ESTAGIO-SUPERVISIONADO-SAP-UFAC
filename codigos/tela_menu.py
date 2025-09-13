import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox

from banco_dados.db_controller import DBController
from login import TelaLogin

class MenuInicial():
    def __init__(self, master, dados_usuario):
        self.janela = master
        self.dados_usuario = dados_usuario  # Guarda os dados do usuário logado
        self.janela.title("SAP-UFAC - Menu Inicial")
        self.janela.geometry("1100x750")
        self.janela.position_center()
        
        # Instância do controlador do banco de dados
        self.db_controller = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
                
        # Garante que a conexão seja fechada quando a janela principal fechar
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        
        # ----- Imagens dos botões iniciais -----
        try:
            self.img_planilha = ImageTk.PhotoImage(Image.open("imagens/botao_planilha_desf.png").resize((300, 175)))
            self.img_baixas = ImageTk.PhotoImage(Image.open("imagens/botao_organizacao_baixas.png").resize((300, 175)))
            self.img_docs = ImageTk.PhotoImage(Image.open("imagens/botao_gerar_docs.png").resize((300, 175)))
            self.img_config = ImageTk.PhotoImage(Image.open("imagens/botao_config.png").resize((300, 175)))
        except Exception as e:
            print(f"Erro ao carregar ícones: {e}")
            self.img_planilha = self.img_baixas = self.img_docs = self.img_config = None
        
        # ----- Estilos (mantidos como no original) -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')
        style_azul_btn = ttk.Style()
        style_azul_btn.configure('MyHeader.TButton', font = ("Inconsolata", 14, "bold"), background='white', foreground="#5bc0de", borderwidth=5, padding=10, bordercolor='#5bc0de')

        # ----- Cabeçalho azul claro -----
        self.frm_cabecalho = ttk.Frame(self.janela, style='MyHeader.TFrame')
        self.frm_cabecalho.pack(fill=X)

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
            background='#5bc0de'
        )
        self.lbl_titulo.pack(expand=True, padx=10, pady=10)

        # ----- Rodapé azul claro -----
        self.frm_rodape = ttk.Frame(self.janela, style='MyHeader.TFrame')
        self.frm_rodape.pack(fill=X, ipady=15, side=BOTTOM, pady=(0, 20))
        
        # ----- Botão de Logout -----
        btn_logout = ttk.Button(self.frm_rodape, text="Sair (Logout)", command=self._fazer_logout, bootstyle="info-outline")
        btn_logout.pack(side=RIGHT, padx=20)

        # ----- Área de botões -----
        botoes_frame = ttk.Frame(self.janela)
        botoes_frame.pack(pady=10, padx=20, expand=True, fill=BOTH)
        
        botoes_frame.grid_columnconfigure((0, 3), weight=1)
        botoes_frame.grid_columnconfigure((1, 2), weight=0)
        botoes_frame.grid_rowconfigure((0, 4), weight=1)
        botoes_frame.grid_rowconfigure((1, 2, 3), weight=0)

        # ----- Mensagem de boas-vindas com o nome do usuário -----
        nome_usuario = self.dados_usuario['nome_completo']
        lbl_bem_vindo = ttk.Label(botoes_frame, text=f"BEM VINDO, {nome_usuario}!", font=("Inconsolata", 15, "bold"))
        lbl_bem_vindo.grid(row=0, column=1, columnspan=2, pady=(0, 20))

        # ----- LÓGICA DE PERMISSÕES PARA OS BOTÕES -----
        perfil = self.dados_usuario['perfil']

        # Botão Planilha de Desfazimento (Acessível a todos)
        self.btn_planilha_des = ttk.Button(botoes_frame, command=self.abrir_planilha_des, image=self.img_planilha, style='MyHeader.TButton')
        self.btn_planilha_des.grid(row=1, column=1, padx=10, pady=10)

        # Botão Organização de Baixas (Não acessível para Estagiário)
        self.btn_org_baixas = ttk.Button(botoes_frame, command=self.abrir_organizacao_baixas, image=self.img_baixas, style='MyHeader.TButton')
        self.btn_org_baixas.grid(row=1, column=2, padx=10, pady=10)
        if perfil == 'Estagiário':
            self.btn_org_baixas.config(state=DISABLED)

        # Botão Gerar Documentos (Não acessível para Estagiário)
        self.btn_gerar_docs = ttk.Button(botoes_frame, command=self.abrir_gerar_docs, image=self.img_docs, style='MyHeader.TButton')
        self.btn_gerar_docs.grid(row=2, column=1, padx=10, pady=10)
        if perfil == 'Estagiário':
            self.btn_gerar_docs.config(state=DISABLED)

        # Botão Configurações (Acessível apenas para todos)
        self.btn_configuracoes = ttk.Button(botoes_frame, command=self.abrir_config, image=self.img_config, style='MyHeader.TButton')
        self.btn_configuracoes.grid(row=2, column=2, padx=10, pady=10)
            
        # NOVO: Botão para Gerenciar Usuários (Apenas Administrador)
        if perfil == 'Administrador':
            self.btn_gerenciar_usuarios = ttk.Button(botoes_frame, text="Gerenciar Usuários", command=self.abrir_gerenciamento_usuarios, style="MyHeader.TButton")
            self.btn_gerenciar_usuarios.grid(row=3, column=1, columnspan=2, ipady=5, padx=8, sticky="ew")

    # MÉTODOS PARA ABRIR AS TELAS (COM IMPORTAÇÃO LOCAL)
    
    def _fazer_logout(self):
        """Limpa a janela do menu e recarrega a tela de login."""
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        # Recria a tela de login na mesma janela
        TelaLogin(self.janela, self.db_controller)

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
            dados_para_agrupar=dados_brutos
        )
        tela_baixas.org_baixas()
        
    def abrir_gerar_docs(self):
        from gerar_doc import GerarDocumentos
        GerarDocumentos(self.janela, self.db_controller).gerar_doc()

    def abrir_config(self):
        from config import Configuracoes
        Configuracoes(self.janela).configuracao()

    def abrir_gerenciamento_usuarios(self):
        from admin import GerenciadorUsuarios
        GerenciadorUsuarios(self.janela, self.db_controller, self.dados_usuario).exibir_tela()

    def fechar_aplicacao(self):
        """Função para fechar a conexão com o BD antes de sair."""
        if self.db_controller:
            self.db_controller.close_connection()
        self.janela.destroy()

# ===================================================================
# PONTO DE ENTRADA PRINCIPAL DA APLICAÇÃO
# ===================================================================
if __name__ == "__main__":
    # A aplicação agora importa e inicia a TELA DE LOGIN primeiro.
    # O MenuInicial só será chamado pela TelaLogin após a autenticação.
    
    from banco_dados.db_controller import DBController
    from login import TelaLogin

    janela_login = ttk.Window(themename="litera")
    db_conn = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
    
    # Inicia a aplicação apenas se a conexão com o banco for bem-sucedida
    if db_conn.conn:
        app = TelaLogin(janela_login, db_conn)
        janela_login.mainloop()
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import Image, ImageTk

# ----- Dados Fictícios -----
# Essa parte será substituída pela lógica que lê e agrupa os dados da planilha de desfazimento.
def carregar_dados_agrupados():
    """
    Função que simula o carregamento e agrupamento dos dados da planilha.
    Retorna um dicionário onde a chave é uma tupla (unidade, servidor)
    e o valor é uma lista de bens.
    """
    dados = {
        ("CCET", "João Silva"): [
            {"tombo": "325693", "descricao": "Notebook Dell, memória RAM 8GB", "status": "IRRECUPERÁVEL"},
            {"tombo": "325895", "descricao": "Notebook Acer", "status": "IRRECUPERÁVEL"},
            {"tombo": "323563", "descricao": "Mesa de MDF, cor madeira", "status": "IRRECUPERÁVEL"},
            {"tombo": "324589", "descricao": "Geladeira frost free, branca, Electrolux", "status": "IRRECUPERÁVEL"},
            {"tombo": "93569", "descricao": "Nobreak para geladeira", "status": "IRRECUPERÁVEL"}
        ],
        ("CCET", "Maria Fernandes"): [
            {"tombo": "325693", "descricao": "Notebook Dell, memória RAM 8GB", "status": "IRRECUPERÁVEL"},
            {"tombo": "325895", "descricao": "Notebook Acer", "status": "IRRECUPERÁVEL"},
            {"tombo": "323563", "descricao": "Mesa de MDF, cor madeira", "status": "IRRECUPERÁVEL"},
            {"tombo": "324589", "descricao": "Geladeira frost free, branca, Electrolux", "status": "IRRECUPERÁVEL"},
        ],
        ("CCET", "Josimar Freitas"): [
            {"tombo": "325693", "descricao": "Notebook Dell, memória RAM 8GB", "status": "IRRECUPERÁVEL"},
            {"tombo": "325895", "descricao": "Notebook Acer", "status": "IRRECUPERÁVEL"},
        ],
         ("Administração", "Tobias Junior"): [
            {"tombo": "325693", "descricao": "Notebook Dell, memória RAM 8GB", "status": "IRRECUPERÁVEL"},
            {"tombo": "325895", "descricao": "Notebook Acer", "status": "IRRECUPERÁVEL"},
            {"tombo": "323563", "descricao": "Mesa de MDF, cor madeira", "status": "IRRECUPERÁVEL"},
        ]
    }
    return dados

class OrganizacaoBaixas():
    def __init__(self, master):
        self.janela = master

    def org_baixas(self):
        # Evita criar múltiplas janelas se o botão for clicado várias vezes
        try:
            if self.tpl_org_baixas.winfo_exists():
                self.tpl_org_baixas.focus()
                return
        except AttributeError:
            pass

        self.tpl_org_baixas = ttk.Toplevel(self.janela)
        self.tpl_org_baixas.title("Organização de Baixas Patrimoniais")
        self.tpl_org_baixas.geometry("800x600")
        self.tpl_org_baixas.position_center()

        # ----- Cabeçalho azul claro -----
        self.cabecalho_frame = ttk.Frame(self.tpl_org_baixas)
        self.cabecalho_frame.pack(fill=X)
        self.cabecalho_frame.configure(style='MyHeader.TFrame')

        # ----- Estilo de cor customizada para o cabeçalho -----
        style_azul = ttk.Style()
        style_azul.configure('MyHeader.TFrame', background='#5bc0de')
        
        # ----- Inserindo o brasão da UFAC -----
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
            brasao_label = ttk.Label(self.cabecalho_frame, image=self.brasao)
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        except:
            brasao_label = ttk.Label(self.cabecalho_frame, text="[BRASÃO]")
            brasao_label.pack(side=LEFT, padx=10, pady=5)
            
        # ----- Título da tela -----
        titulo = ttk.Label(
            self.cabecalho_frame,
            text="Organização de Baixas Patrimoniais",
            font=("Inconsolata", 15, "bold"),
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de'
        )
        titulo.pack(expand=True, padx=10, pady=10)
        
        # ===== INÍCIO DA INTEGRAÇÃO DO CONTEÚDO DA TELA =====
        
        # ----- Frame principal para o conteúdo abaixo do cabeçalho -----
        self.frame_conteudo = ttk.Frame(self.tpl_org_baixas)
        self.frame_conteudo.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # ----- Resumo da Planilha -----
        resumo_frame = ttk.Frame(self.frame_conteudo)
        resumo_frame.pack(fill=X, pady=(0, 15), anchor='w')

        self.lbl_resumo = ttk.Label(resumo_frame, 
            text="Resumo da planilha atual",
            foreground='#5bc0de',
            font=("Inconsolata", 12, "bold"))
        self.lbl_resumo.pack(anchor="w")
        
        self.lbl_nome_plan = ttk.Label(resumo_frame, 
            text="Nome da planilha: RELATÓRIO DE DESFAZIMENTO DE BENS MÓVEIS PATRIMONIAIS DE 2024",
            foreground='black',
            font=("Inconsolata", 12, "bold"))
        self.lbl_nome_plan.pack(anchor="w")
        
        self.lbl_tombos = ttk.Label(resumo_frame,
            text="120 tombos",
            foreground='black',
            font=("Inconsolata", 12, "bold"))
        self.lbl_tombos.pack(anchor="w")
        
        self.lbl_unid_resp = ttk.Label(resumo_frame, 
            text="30 unidades, 60 responsáveis",
            foreground='black',
            font=("Inconsolata", 12, "bold"))                                       
        self.lbl_unid_resp.pack(anchor="w")

        # ----- Área de Rolagem para os Grupos -----
        scl_frame_grupos = ScrolledFrame(self.frame_conteudo, autohide=True, bootstyle="light")
        scl_frame_grupos.pack(fill=BOTH, expand=True, pady=(0, 20))

        # Carrega os dados agrupados
        dados_agrupados = carregar_dados_agrupados()

        # ----- Cria os grupos de bens dinamicamente -----
        for (unidade, servidor), bens in dados_agrupados.items():
            group_frame = ttk.Labelframe(scl_frame_grupos, text="", padding=10)
            group_frame.pack(fill=X, expand=True, padx=10, pady=(0, 10))

            info_frame = ttk.Frame(group_frame)
            info_frame.pack(fill=X, expand=True)

            check_var = tk.IntVar(value=1)
            ttk.Checkbutton(info_frame, variable=check_var).pack(side="left", padx=(0, 10))
            
            label_text = f"Unidade: {unidade}\nServidor: {servidor}"
            ttk.Label(info_frame, text=label_text, font=("Helvetica", 10, "bold")).pack(anchor="w")

            ttk.Separator(group_frame, orient='horizontal').pack(fill='x', pady=5, expand=True)

            # Lista dos bens em cada agrupamento
            for bem in bens:
                bem_frame = ttk.Frame(group_frame)
                bem_frame.pack(fill=X, expand=True, padx=(30, 0)) # Adicionado padding à esquerda para alinhar com o texto
                
                self.lbl_tombo = ttk.Label(bem_frame,
                    text=f"Tombo: {bem['tombo']}", 
                    width=15)
                self.lbl_tombo.pack(side="left")
                
                self.lbl_desc = ttk.Label(bem_frame, 
                    text=bem["descricao"], 
                    width=45, 
                    anchor="w")
                self.lbl_desc.pack(side="left", padx=10)
                
                self.lbl_status = ttk.Label(bem_frame, 
                    text=bem["status"], 
                    width=20, 
                    anchor="e")
                self.lbl_status.pack(side="right")
        
        # ----- Botões de Ação -----
        botoes_frame = ttk.Frame(self.frame_conteudo)
        botoes_frame.pack(fill=X, pady=(10, 0), side=BOTTOM)

        self.btn_voltar = ttk.Button(botoes_frame, 
            text="<- Voltar", 
            bootstyle="primary-outline", 
            command=self.tpl_org_baixas.destroy)
        self.btn_voltar.pack(side="left", padx=(0, 5))
        
        self.btn_gerar = ttk.Button(botoes_frame, 
            text="Gerar Documentos de Baixa", 
            bootstyle="success")
        self.btn_gerar.pack(side="right", padx=5)
        
        self.btn_visualizar = ttk.Button(botoes_frame,
            text="Visualizar Documentos",
            bootstyle="info")
        self.btn_visualizar.pack(side='right', padx=5)

        self.btn_atualizar = ttk.Button(botoes_frame, 
            text="Atualizar Organização",
            bootstyle="success-outline")
        self.btn_atualizar.pack(side="right", padx=5)

# ----- Bloco para Teste da Janela (PADRONIZADO) -----
if __name__ == "__main__":
    
    # Classe de teste que simula a sua classe "MenuInicial"
    class AppTeste:
        def __init__(self, master):
            self.janela = master
            self.janela.title("App de Teste para Organização de Baixas")
            self.janela.geometry("400x200")
            
            # 1. Instancia a classe da tela que queremos testar
            self.tela_org = OrganizacaoBaixas(self.janela)

            # 2. Cria um botão para chamar o método que abre a tela
            btn_abrir = ttk.Button(
                self.janela,
                text="Abrir Tela de Organização",
                command=self.tela_org.org_baixas, # Chama o método da instância
                bootstyle="primary"
            )
            btn_abrir.pack(expand=True)

    # Inicialização padrão, igual à tela de menu
    janela_teste = ttk.Window()
    app = AppTeste(janela_teste)
    janela_teste.mainloop()
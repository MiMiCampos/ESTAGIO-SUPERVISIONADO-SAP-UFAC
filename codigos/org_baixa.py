import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk

# A importação de 'GerarDocBaixa' foi REMOVIDA daqui para evitar o ciclo.

# ----- Dados Fictícios (usado apenas se a tela for aberta sem dados) -----
def carregar_dados_agrupados_teste():
    """Função de teste que retorna dados agrupados para fallback."""
    return {
        ("Unidade Teste", "Servidor Teste"): [
            {"tombo": "00000", "descricao": "Item de Teste", "status": "N/A"}
        ]
    }

class OrganizacaoBaixas():
    def __init__(self, master, nome_planilha=None, dados_para_agrupar=None):
        self.janela = master
        self.nome_planilha_recebida = nome_planilha
        self.dados_brutos_recebidos = dados_para_agrupar
        self.brasao = None
        self.check_vars = {} # Dicionário para guardar as variáveis dos checkboxes
        self.dados_agrupados_na_tela = {} # Guarda os dados que estão sendo exibidos
        self._carregar_imagem_brasao()

    def _carregar_imagem_brasao(self):
        """Carrega a imagem do brasão."""
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
        except Exception:
            self.brasao = None

    def _agrupar_dados(self, dados_brutos):
        """Processa a lista de bens e agrupa por Unidade e Servidor."""
        grupos = {}
        # Índices baseados na estrutura da planilha: 5 = Unidade, 6 = Classificação (Status)
        # O nome do servidor não está nos dados, então vamos criar um fictício por unidade.
        for linha in dados_brutos:
            unidade = linha[5] if len(linha) > 5 else "N/A"
            servidor = f"Servidor Responsável de {unidade}" # Servidor fictício
            tombo = linha[1] if len(linha) > 1 else "N/A"
            descricao = linha[2] if len(linha) > 2 else "N/A"
            status = linha[6] if len(linha) > 6 else "N/A"
            
            chave = (unidade, servidor)
            if chave not in grupos:
                grupos[chave] = []
            
            grupos[chave].append({"tombo": tombo, "descricao": descricao, "status": status})
        return grupos

    def org_baixas(self):
        """Cria e exibe a janela de Organização de Baixas."""
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

        # --- UI (Cabeçalho, corpo, etc.) ---
        style = ttk.Style()
        style.configure('MyHeader.TFrame', background='#5bc0de')
        cabecalho_frame = ttk.Frame(self.tpl_org_baixas, style='MyHeader.TFrame')
        cabecalho_frame.pack(fill=X)
        if self.brasao:
            brasao_label = ttk.Label(cabecalho_frame, image=self.brasao)
            brasao_label.image = self.brasao
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        
        titulo = ttk.Label(cabecalho_frame, text="Organização de Baixas", font=("Inconsolata", 15, "bold"), bootstyle=INVERSE, foreground='black', background='#5bc0de')
        titulo.pack(expand=True, padx=10, pady=10)
        
        frame_conteudo = ttk.Frame(self.tpl_org_baixas, padding=(20, 10))
        frame_conteudo.pack(fill=BOTH, expand=True)

        if self.dados_brutos_recebidos is not None:
            self.dados_agrupados_na_tela = self._agrupar_dados(self.dados_brutos_recebidos)
            total_tombos = len(self.dados_brutos_recebidos)
            total_unidades = len(self.dados_agrupados_na_tela)
            nome_exibicao = self.nome_planilha_recebida or "Planilha sem nome"
        else:
            self.dados_agrupados_na_tela = carregar_dados_agrupados_teste()
            total_tombos = sum(len(bens) for bens in self.dados_agrupados_na_tela.values())
            total_unidades = len(self.dados_agrupados_na_tela)
            nome_exibicao = "Planilha de Teste"

        # ----- Resumo da Planilha (dinâmico) -----
        resumo_frame = ttk.Frame(frame_conteudo)
        resumo_frame.pack(fill=X, pady=(0, 15), anchor='w')
        ttk.Label(resumo_frame, text="Resumo da planilha atual", foreground='#5bc0de', font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"Nome da planilha: {nome_exibicao}", foreground='black', font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"{total_tombos} tombos", foreground='black', font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"{total_unidades} unidades/responsáveis", foreground='black', font=("Inconsolata", 12, "bold")).pack(anchor="w")

        # --- Área de Rolagem para os Grupos ---
        scl_frame_grupos = ScrolledFrame(frame_conteudo, autohide=True, bootstyle="light")
        scl_frame_grupos.pack(fill=BOTH, expand=True, pady=(0, 20))

        # Cria os grupos de bens dinamicamente
        for (unidade, servidor), bens in self.dados_agrupados_na_tela.items():
            group_frame = ttk.Labelframe(scl_frame_grupos, text="", padding=10)
            group_frame.pack(fill=X, expand=True, padx=10, pady=(0, 10))
            
            info_frame = ttk.Frame(group_frame)
            info_frame.pack(fill=X, expand=True)
            
            # Guarda a variável do checkbox para saber se foi selecionado
            check_var = tk.IntVar(value=1)
            chave_unica = (unidade, servidor)
            self.check_vars[chave_unica] = check_var
            ttk.Checkbutton(info_frame, variable=check_var).pack(side="left", padx=(0, 10))
            
            label_text = f"Unidade: {unidade}\nServidor: {servidor}"
            ttk.Label(info_frame, text=label_text, font=("Helvetica", 10, "bold")).pack(anchor="w")
            ttk.Separator(group_frame, orient='horizontal').pack(fill='x', pady=5, expand=True)
            for bem in bens:
                bem_frame = ttk.Frame(group_frame)
                bem_frame.pack(fill=X, expand=True, padx=(30, 0))
                ttk.Label(bem_frame, text=f"Tombo: {bem['tombo']}", width=15).pack(side="left")
                ttk.Label(bem_frame, text=bem["descricao"], width=45, anchor="w").pack(side="left", padx=10)
                ttk.Label(bem_frame, text=bem["status"], width=20, anchor="e").pack(side="right")
        
        # --- Botões de Ação ---
        botoes_frame = ttk.Frame(frame_conteudo)
        botoes_frame.pack(fill=X, pady=(10, 0), side=BOTTOM)
        
        ttk.Button(botoes_frame, text="<- Voltar", bootstyle="primary-outline", command=self.tpl_org_baixas.destroy).pack(side="left")
        ttk.Button(botoes_frame, text="Gerar Documentos de Baixa", command=self.abrir_tela_geracao, bootstyle="success").pack(side="right")
        ttk.Button(botoes_frame, text="Visualizar Documentos", bootstyle="info").pack(side='right', padx=5)
        ttk.Button(botoes_frame, text="Atualizar Organização", bootstyle="success-outline").pack(side="right", padx=5)

    def abrir_tela_geracao(self):
        """Coleta os dados dos grupos selecionados e abre a tela de geração."""
        from gerar_doc_baixa import GerarDocBaixa

        dados_selecionados = {}
        for chave, var in self.check_vars.items():
            if var.get() == 1: # Se o checkbox estiver marcado
                dados_selecionados[chave] = self.dados_agrupados_na_tela[chave]

        if not dados_selecionados:
            Messagebox.show_warning("Nenhum grupo selecionado", "Por favor, selecione pelo menos um grupo para gerar os documentos.")
            return

        # ***** CORREÇÃO ABAIXO *****
        # 1. Destrói a janela atual para liberar o foco completamente.
        self.tpl_org_baixas.destroy()
        
        # 2. Cria a nova tela passando a janela PAI da que foi destruída como 'master'.
        #    Neste caso, 'self.janela' é a referência correta à janela anterior.
        tela_geracao = GerarDocBaixa(self.janela, self.nome_planilha_recebida, dados_selecionados)
        tela_geracao.exibir_tela()

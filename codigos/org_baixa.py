import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from gerar_doc_baixa import GerarDocBaixa # Importação movida para o topo
from utils.path_helper import resource_path

class OrganizacaoBaixas():
    def __init__(self, master, db_controller, nome_planilha=None, dados_para_agrupar=None, numero_processo=None, id_desfazimento=None):
        self.janela = master
        self.nome_planilha_recebida = nome_planilha
        self.dados_brutos_recebidos = dados_para_agrupar
        self.numero_processo_recebido = numero_processo
        self.id_desfazimento_recebido = id_desfazimento # << Guarda o ID recebido
        print("\n--- PASSO 2: CHEGANDO EM org_baixa.py ---")
        print(f"[DEBUG] Tela recebendo ID de Desfazimento: {id_desfazimento}")
        print(f"[DEBUG] Tela recebendo Número do Processo: {numero_processo}")
        self.brasao = None
        self.check_vars = {}
        self.dados_agrupados_na_tela = {}
        self.db = db_controller
        self._carregar_imagem_brasao()

    def _carregar_imagem_brasao(self):
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
        except Exception:
            self.brasao = None

    def _agrupar_dados(self, dados_brutos):
        """Processa a lista de bens e agrupa por Unidade e Servidor."""
        grupos = {}
        # Índices da lista 'dados_brutos' que vem do db_controller:
        # 1=tombo, 2=descricao, 3=data_aquisicao, 5=unidade, 6=servidor, 7=status, 9=valor, 10=forma_ingresso
        for linha in dados_brutos:
            unidade = linha[5] if len(linha) > 5 else "Unidade não informada"
            servidor = linha[6] if len(linha) > 6 and linha[6] else "Servidor não informado"
            
            chave = (unidade, servidor)
            if chave not in grupos:
                grupos[chave] = []
            
            # Cria um dicionário completo com todas as informações necessárias
            dados_do_bem = {
                "tombo": linha[1],
                "descricao": linha[2],
                "data_aquisicao": linha[3],
                "valor": linha[9] if len(linha) > 9 else '0,00',
                "forma_ingresso": linha[10] if len(linha) > 10 else 'N/A',
                "status": linha[7] if len(linha) > 7 else "Irrecuperável"
            }
            grupos[chave].append(dados_do_bem)
        return grupos

    def org_baixas(self):
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
        
        cabecalho_frame = ttk.Frame(self.tpl_org_baixas, bootstyle='info')
        cabecalho_frame.pack(fill=X)
        
        if self.brasao:
            brasao_label = ttk.Label(cabecalho_frame, image=self.brasao, bootstyle='info')
            brasao_label.image = self.brasao
            brasao_label.pack(side=LEFT, padx=10, pady=5)
            
        titulo = ttk.Label(cabecalho_frame, text="Organização de Baixas", font=("Inconsolata", 16, "bold"), bootstyle='inverse-info', foreground='black')
        titulo.pack(expand=True, padx=10, pady=10)
        frame_conteudo = ttk.Frame(self.tpl_org_baixas, padding=(20, 10))
        frame_conteudo.pack(fill=BOTH, expand=True)
        
        if self.dados_brutos_recebidos is not None:
            self.dados_agrupados_na_tela = self._agrupar_dados(self.dados_brutos_recebidos)
            total_tombos = len(self.dados_brutos_recebidos)
            total_unidades = len(self.dados_agrupados_na_tela)
            nome_exibicao = self.nome_planilha_recebida or "Planilha sem nome"
        else: # Fallback de teste
            self.dados_agrupados_na_tela = {}
            total_tombos = 0
            total_unidades = 0
            nome_exibicao = "Planilha de Teste"
            
        resumo_frame = ttk.Frame(frame_conteudo)
        resumo_frame.pack(fill=X, pady=(0, 15), anchor='w')
        ttk.Label(resumo_frame, text="Resumo da planilha atual", foreground='#5bc0de', font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"Nome da planilha: {nome_exibicao}", font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"Número do Processo: {self.numero_processo_recebido or 'Não informado'}", font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"{total_tombos} tombos", font=("Inconsolata", 12, "bold")).pack(anchor="w")
        ttk.Label(resumo_frame, text=f"{total_unidades} unidades/responsáveis", font=("Inconsolata", 12, "bold")).pack(anchor="w")
        
        scl_frame_grupos = ScrolledFrame(frame_conteudo, autohide=True, bootstyle="light")
        scl_frame_grupos.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        for (unidade, servidor), bens in self.dados_agrupados_na_tela.items():
            group_frame = ttk.Labelframe(scl_frame_grupos, text="", padding=10)
            group_frame.pack(fill=X, expand=True, padx=10, pady=(0, 10))
            info_frame = ttk.Frame(group_frame)
            info_frame.pack(fill=X, expand=True)
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
                
        botoes_frame = ttk.Frame(frame_conteudo)
        botoes_frame.pack(fill=X, pady=(10, 0), side=BOTTOM)
        ttk.Button(botoes_frame, text="<- Voltar", bootstyle="primary-outline", command=self.tpl_org_baixas.destroy).pack(side="left")
        ttk.Button(botoes_frame, text="Gerar Documentos de Baixa", command=self.abrir_tela_geracao, bootstyle="success").pack(side="right")
        # O botão visualizar foi removido temporariamente para simplificar o fluxo principal
        
    def _coletar_dados_selecionados(self):
        dados_selecionados = {}
        for chave, var in self.check_vars.items():
            if var.get() == 1:
                dados_selecionados[chave] = self.dados_agrupados_na_tela[chave]
        return dados_selecionados

    def abrir_tela_geracao(self):
        dados_selecionados = self._coletar_dados_selecionados()
        if not dados_selecionados:
            Messagebox.show_warning("Nenhum grupo selecionado", "Por favor, selecione pelo menos um grupo para gerar os documentos.")
            return

        self.tpl_org_baixas.destroy()
        
        tela_geracao = GerarDocBaixa(
            master=self.janela, 
            db_controller=self.db, 
            nome_planilha_base=self.nome_planilha_recebida, 
            dados_selecionados=dados_selecionados, 
            dados_brutos_para_voltar=self.dados_brutos_recebidos,
            numero_processo=self.numero_processo_recebido,
            id_desfazimento=self.id_desfazimento_recebido 
        )
        tela_geracao.exibir_tela()
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
from utils.gerador_termo import GeradorDeTermo
from banco_dados.db_controller import DBController

class GerarDocBaixa:
    def __init__(self, master, nome_planilha_base, dados_selecionados, dados_brutos_para_voltar, numero_processo, id_desfazimento):
        self.janela_mestra_gerarbaixa = master 
        self.nome_planilha_base = nome_planilha_base
        self.dados_selecionados_para_gerar = dados_selecionados
        self.dados_brutos_originais = dados_brutos_para_voltar
        self.id_desfazimento = id_desfazimento
        self.numero_processo = numero_processo
        self.toplevel_gerarbaixa = None
        self.db = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
        self.carregar_recursos_gerarbaixa()

    def carregar_recursos_gerarbaixa(self):
        try:
            imagem_brasao = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao_para_gerarbaixa = ImageTk.PhotoImage(imagem_brasao)
        except Exception as e:
            self.brasao_para_gerarbaixa = None

    def exibir_tela(self):
        self.toplevel_gerarbaixa = ttk.Toplevel(self.janela_mestra_gerarbaixa)
        self.toplevel_gerarbaixa.title("Gerar Documento de Baixa")
        self.toplevel_gerarbaixa.geometry("1100x750")
        self.toplevel_gerarbaixa.position_center()
        self.toplevel_gerarbaixa.transient(self.janela_mestra_gerarbaixa)
        self.toplevel_gerarbaixa.grab_set()
        
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure('TEntry', padding=(5, 5))
        style.map('TEntry', fieldbackground=[('readonly', '#f0f0f0')], foreground=[('readonly', '#a0a0a0')])

        frame_cabecalho = ttk.Frame(self.toplevel_gerarbaixa, style='Header.TFrame', padding=(10, 10))
        frame_cabecalho.pack(fill=X)
        if self.brasao_para_gerarbaixa:
            lbl_brasao = ttk.Label(frame_cabecalho, image=self.brasao_para_gerarbaixa, style='Header.TFrame')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))
        lbl_titulo = ttk.Label(frame_cabecalho, text="Gerar Documento de Baixa Patrimonial", font=("Inconsolata", 18, "bold"), background='#5bc0de', foreground='black')
        lbl_titulo.pack(side=LEFT, expand=True)

        frame_corpo = ttk.Frame(self.toplevel_gerarbaixa, padding=20)
        frame_corpo.pack(expand=True, fill=BOTH)

        frame_revisao = ttk.Labelframe(frame_corpo, text="Resumo da Seleção", padding=15)
        frame_revisao.pack(fill=X, pady=(0, 20))
        total_bens = sum(len(bens) for bens in self.dados_selecionados_para_gerar.values())
        total_grupos = len(self.dados_selecionados_para_gerar)
        ttk.Label(frame_revisao, text=f"Planilha base: {self.nome_planilha_base}").pack(anchor=W)
        ttk.Label(frame_revisao, text=f"Total de bens selecionados: {total_bens} em {total_grupos} grupos (unidade/servidor).").pack(anchor=W)

        frame_campos = ttk.Labelframe(frame_corpo, text="Informações Gerais do Documento", padding=15)
        frame_campos.pack(fill=X, pady=(0, 20))
        frame_campos.grid_columnconfigure(1, weight=1)
        frame_campos.grid_columnconfigure(3, weight=1)

        ttk.Label(frame_campos, text="Termo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_termo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_termo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        numero_termo = self.db.get_proximo_numero_termo()
        ano_atual = datetime.now().year
        self.entry_termo.insert(0, f"{numero_termo}/{ano_atual}")
        self.entry_termo.config(state='readonly')
        
        ttk.Label(frame_campos, text="Motivo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_motivo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_motivo.grid(row=0, column=3, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Número do Processo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_num_processo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_num_processo.grid(row=1, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        numero_processo_fresco = self.db.get_processo_por_id_desfazimento(self.id_desfazimento)
        self.entry_num_processo.insert(0, numero_processo_fresco or '')
        self.entry_num_processo.config(state='readonly')

        # CAMPO "SERVIDOR RESPONSÁVEL" FOI REMOVIDO DAQUI

        ttk.Label(frame_campos, text="Unidade de Destino:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_unidade_destino = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_unidade_destino.grid(row=3, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        self.entry_unidade_destino.insert(0, "DMAP - Diretoria de Material e Patrimônio")
        self.entry_unidade_destino.config(state='readonly')

        frame_configs = ttk.Labelframe(frame_corpo, text="Configurações de Saída", padding=15)
        frame_configs.pack(fill=X)
        self.formato_var = tk.StringVar(value=".pdf")
        ttk.Label(frame_configs, text="Formato do documento:").pack(side=LEFT)
        ttk.Radiobutton(frame_configs, text=".pdf", variable=self.formato_var, value=".pdf").pack(side=LEFT, padx=5)
        ttk.Radiobutton(frame_configs, text=".docx (Word)", variable=self.formato_var, value=".docx").pack(side=LEFT, padx=5)
        
        frame_pasta = ttk.Frame(frame_corpo, padding=(0, 20))
        frame_pasta.pack(fill=X, pady=(10,0))
        ttk.Label(frame_pasta, text="Pasta de destino:").pack(anchor=W, pady=(10, 0))
        self.entry_pasta_destino = ttk.Entry(frame_pasta, font=("Inconsolata", 11))
        self.entry_pasta_destino.pack(side=LEFT, fill=X, expand=True, ipady=4)
        ttk.Button(frame_pasta, text="Selecionar...", bootstyle="info-outline", command=self.selecionar_pasta_destino).pack(side=LEFT, padx=(5,0))

        frame_rodape = ttk.Frame(self.toplevel_gerarbaixa, padding=10)
        frame_rodape.pack(fill=X, side=BOTTOM)
        ttk.Button(frame_rodape, text="<- Voltar", command=self.toplevel_gerarbaixa.destroy, bootstyle="primary-outline").pack(side=LEFT, padx=10)
        ttk.Button(frame_rodape, text="Confirmar e Gerar Documento", command=self.confirmar_geracao, bootstyle="success").pack(side=RIGHT, padx=10)

    def selecionar_pasta_destino(self):
        caminho = filedialog.askdirectory(title="Selecione a pasta de destino")
        if caminho:
            self.entry_pasta_destino.delete(0, END)
            self.entry_pasta_destino.insert(0, caminho)

    def confirmar_geracao(self):
        # VALIDAÇÃO ATUALIZADA SEM O CAMPO SERVIDOR
        if not self.entry_pasta_destino.get().strip() or not self.entry_motivo.get().strip():
            Messagebox.show_error("Erro de Validação", "Os campos 'Motivo' e 'Pasta de destino' são obrigatórios.")
            return

        if Messagebox.yesno("Confirmar Geração", "Você confirma a geração do documento com as informações fornecidas?") == "Sim":
            self._gerar_arquivo()

    def _gerar_arquivo(self):
        formato = self.formato_var.get()
        pasta = self.entry_pasta_destino.get()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"Termo_de_Baixa_{timestamp}{formato}"
        caminho_completo = os.path.join(pasta, nome_arquivo)
        
        primeira_chave = next(iter(self.dados_selecionados_para_gerar))
        unidade_origem = primeira_chave[0]

        dados_gerais = {
            'termo': self.entry_termo.get(),
            'motivo': self.entry_motivo.get(),
            'unidade_origem': unidade_origem,
            'unidade_destino': self.entry_unidade_destino.get(),
            'processo': self.entry_num_processo.get()
        }

        try:
            GeradorDeTermo.gerar(
                formato=formato,
                caminho_completo=caminho_completo,
                dados_gerais=dados_gerais,
                dados_agrupados=self.dados_selecionados_para_gerar
            )
            Messagebox.ok("Sucesso", f"Documento gerado com sucesso em:\n{caminho_completo}")
        
        except Exception as e:
            # >>> LINHAS DE DEBUG ADICIONADAS AQUI <<<
            print("--- ERRO DETALHADO CAPTURADO ---")
            print(f"Tipo do Erro: {type(e)}")
            print(f"Mensagem do Erro: {e}")
            print("---------------------------------")
            # ------------------------------------

            Messagebox.show_error("Erro Inesperado", f"Não foi possível gerar o arquivo:\n{e}")
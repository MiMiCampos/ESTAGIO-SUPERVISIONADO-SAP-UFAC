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
from utils.path_helper import resource_path

class GerarDocBaixa:
    def __init__(self, master, db_controller, nome_planilha_base, dados_selecionados, dados_brutos_para_voltar, numero_processo, id_desfazimento):
        self.janela_mestra_gerarbaixa = master 
        self.nome_planilha_base = nome_planilha_base
        self.dados_selecionados_para_gerar = dados_selecionados
        self.dados_brutos_originais = dados_brutos_para_voltar
        self.id_desfazimento = id_desfazimento
        self.numero_processo = numero_processo
        self.toplevel_gerarbaixa = None
        self.db = db_controller
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
        # self.toplevel_gerarbaixa.geometry("1100x750")
        # self.toplevel_gerarbaixa.position_center()
        
        
        screen_width = self.toplevel_gerarbaixa.winfo_screenwidth()
        screen_height = self.toplevel_gerarbaixa.winfo_screenheight()
        self.toplevel_gerarbaixa.geometry(f"{screen_width}x{screen_height}+0+0")   
        
        self.toplevel_gerarbaixa.transient(self.janela_mestra_gerarbaixa)
        self.toplevel_gerarbaixa.grab_set()
        
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure('TEntry', padding=(5, 5))
        style.map('TEntry', fieldbackground=[('readonly', '#f0f0f0')], foreground=[('readonly', '#a0a0a0')])

        frame_cabecalho = ttk.Frame(self.toplevel_gerarbaixa, bootstyle='info', padding=(10, 10))
        frame_cabecalho.pack(fill=X)
        
        if self.brasao_para_gerarbaixa:
            lbl_brasao = ttk.Label(frame_cabecalho, image=self.brasao_para_gerarbaixa, bootstyle='info')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))
        lbl_titulo = ttk.Label(frame_cabecalho, text="Gerar Documento de Baixa Patrimonial", font=("Inconsolata", 16, "bold"), bootstyle='inverse-info', foreground='black')
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

        ttk.Label(frame_campos, text="Termo Inicial:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_termo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_termo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        numero_termo_int = self.db.get_proximo_numero_termo() # Agora retorna um inteiro
        ano_atual = datetime.now().year
        self.entry_termo.insert(0, f"{numero_termo_int:06d}/{ano_atual}") # Formata o inteiro aqui
        self.entry_termo.config(state='readonly')
        
        ttk.Label(frame_campos, text="Motivo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_motivo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_motivo.grid(row=0, column=3, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Número do Processo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_num_processo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_num_processo.grid(row=1, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        self.entry_num_processo.insert(0, self.numero_processo or '')
        self.entry_num_processo.config(state='readonly')

        ttk.Label(frame_campos, text="Unidade de Destino:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_unidade_destino = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_unidade_destino.grid(row=3, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        self.entry_unidade_destino.insert(0, "DMAP - Diretoria de Material e Patrimônio")
        self.entry_unidade_destino.config(state='readonly')

        frame_configs = ttk.Labelframe(frame_corpo, text="Configurações de Saída", padding=15)
        frame_configs.pack(fill=X)
        self.formato_var = tk.StringVar(value=".pdf") # Alterado para .pdf como padrão
        ttk.Label(frame_configs, text="Formato do documento:").pack(side=LEFT)
        ttk.Radiobutton(frame_configs, text=".pdf", variable=self.formato_var, value=".pdf").pack(side=LEFT, padx=5)
        ttk.Radiobutton(frame_configs, text=".docx (Word)", variable=self.formato_var, value=".docx").pack(side=LEFT, padx=5)
        
        frame_pasta = ttk.Frame(frame_corpo, padding=(0, 20))
        frame_pasta.pack(fill=X, pady=(10,0))
        ttk.Label(frame_pasta, text="Pasta de Destino:").pack(anchor=W, pady=(10, 0))
        self.entry_pasta_destino = ttk.Entry(frame_pasta, font=("Inconsolata", 11))
        self.entry_pasta_destino.pack(side=LEFT, fill=X, expand=True, ipady=4)
        ttk.Button(frame_pasta, text="Selecionar Pasta", bootstyle="info-outline", command=self.selecionar_pasta_destino).pack(side=LEFT, padx=(5,0), fill=Y)

        frame_rodape = ttk.Frame(self.toplevel_gerarbaixa, padding=10)
        frame_rodape.pack(fill=X, side=BOTTOM)
        ttk.Button(frame_rodape, text="<- Voltar", command=self.toplevel_gerarbaixa.destroy, bootstyle="primary-outline").pack(side=LEFT, padx=10)
        ttk.Button(frame_rodape, text="Confirmar e Gerar Documentos", command=self.confirmar_geracao, bootstyle="success").pack(side=RIGHT, padx=10)

    def selecionar_pasta_destino(self):
        caminho = filedialog.askdirectory(title="Selecione a pasta de destino")
        if caminho:
            self.entry_pasta_destino.delete(0, END)
            self.entry_pasta_destino.insert(0, caminho)

    def confirmar_geracao(self):
        if not self.entry_pasta_destino.get().strip() or not self.entry_motivo.get().strip():
            Messagebox.show_error("Erro de Validação", "Os campos 'Motivo' e 'Pasta de destino' são obrigatórios.", parent=self.toplevel_gerarbaixa)
            return

        total_docs = len(self.dados_selecionados_para_gerar)
        msg = f"Você confirma a geração de {total_docs} documento(s) de baixa com as informações fornecidas?"
        if Messagebox.yesno("Confirmar Geração", msg, parent=self.toplevel_gerarbaixa) == "Sim":
            self._gerar_multiplos_arquivos()

    def _gerar_multiplos_arquivos(self):
        formato = self.formato_var.get()
        pasta = self.entry_pasta_destino.get()
        ano_atual = datetime.now().year
        
        # Pega o próximo número de termo (como INT) uma vez no início
        proximo_numero_termo = self.db.get_proximo_numero_termo()
        
        documentos_gerados = 0
        erros = 0

        # Loop principal para gerar um arquivo por grupo (servidor/unidade)
        for (unidade, servidor), bens in self.dados_selecionados_para_gerar.items():
            id_novo_documento = None # Garante que o ID é resetado a cada iteração
            try:
                # Formata o número do termo para o documento atual
                numero_termo_formatado = f"{proximo_numero_termo:06d}/{ano_atual}"
                
                # Cria um nome de arquivo único e limpo
                servidor_formatado = "".join(c for c in servidor if c.isalnum() or c in (' ', '_')).rstrip()
                nome_arquivo_sugerido = f"Termo_{proximo_numero_termo:06d}_{servidor_formatado.replace(' ', '_')}{formato}"
                caminho_completo = os.path.join(pasta, nome_arquivo_sugerido)
                
                dados_gerais_doc = {
                    'termo': numero_termo_formatado,
                    'motivo': self.entry_motivo.get(),
                    'unidade_origem': unidade,
                    'unidade_destino': self.entry_unidade_destino.get(),
                    'processo': self.entry_num_processo.get(),
                    'servidor_responsavel': servidor
                }
                
                # Prepara os dados apenas para o grupo atual
                dados_agrupados_doc = {(unidade, servidor): bens}
                
                # 1. Gera o arquivo físico
                GeradorDeTermo.gerar(
                    formato=formato,
                    caminho_completo=caminho_completo,
                    dados_gerais=dados_gerais_doc,
                    dados_agrupados=dados_agrupados_doc
                )
                
                # --- Lógica de Persistência ---
                # 2. Registra o documento no banco e obtém o seu ID
                id_novo_documento = self.db.registrar_documento_baixa(
                    id_desfazimento=self.id_desfazimento,
                    numero_termo=numero_termo_formatado,
                    caminho_arquivo=caminho_completo,
                    motivo=dados_gerais_doc['motivo']
                )

                if id_novo_documento:
                    # 3. Se o registro funcionou, associa os bens a este novo ID
                    lista_tombos = [bem['tombo'] for bem in bens]
                    self.db.associar_bens_a_documento(id_novo_documento, lista_tombos)
                else:
                    # Força um erro se o registro no banco falhar por algum motivo
                    raise Exception("Falha ao registrar o documento no banco de dados.")

                # 4. Incrementa os contadores de sucesso
                documentos_gerados += 1
                proximo_numero_termo += 1

            except Exception as e:
                erros += 1
                print(f"ERRO ao gerar documento para {servidor}: {e}")

        # Mensagem final para o usuário
        if erros == 0:
            Messagebox.ok("Sucesso", f"{documentos_gerados} documento(s) gerado(s) com sucesso na pasta selecionada.", parent=self.toplevel_gerarbaixa)
        else:
            Messagebox.show_warning("Operação Concluída com Erros",
                                   f"Documentos gerados: {documentos_gerados}\n"
                                   f"Falhas: {erros}\n\n"
                                   "Verifique o terminal para mais detalhes sobre os erros.", parent=self.toplevel_gerarbaixa)
        
        self.toplevel_gerarbaixa.destroy()
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
import openpyxl

from pl_des_edit import EdicaoPlanilha

class CriarPlanilha:
    def __init__(self, master, db_controller, menu_principal):
        self.master = master
        self.db = db_controller
        self.menu_principal = menu_principal
        self.tpl_criar_planilha = None
        self.carregar_recursos()

    def carregar_recursos(self):
        """Carrega as imagens necessárias (apenas o brasão)."""
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((40, 40))
            self.brasao = ImageTk.PhotoImage(brasao_img)
        except Exception as e:
            print(f"Erro ao carregar imagem do brasão: {e}")
            self.brasao = None

    def criar(self):
        """Cria e exibe a janela principal para configurar a planilha."""
        if self.tpl_criar_planilha and self.tpl_criar_planilha.winfo_exists():
            self.tpl_criar_planilha.lift()
            return

        self.tpl_criar_planilha = ttk.Toplevel(self.master)
        self.tpl_criar_planilha.title("Criar Nova Planilha de Desfazimento")
        self.tpl_criar_planilha.geometry("800x600")
        self.tpl_criar_planilha.transient(self.master)
        self.tpl_criar_planilha.position_center()
        self.tpl_criar_planilha.grab_set()

        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure('custom.TButton', font=("Inconsolata", 14), borderwidth=1, padding=(10, 10), background='white', foreground='#5bc0de')
        style.map('custom.TButton', bordercolor=[('!active', '#adb5bd'), ('active', '#5bc0de')], background=[('active', "#ececec"), ('!active', 'white')], relief=[('pressed', 'solid'), ('!pressed', 'solid')])

        frm_cabecalho = ttk.Frame(self.tpl_criar_planilha, style='Header.TFrame', padding=(10, 5))
        frm_cabecalho.pack(fill=X, side=TOP)

        if self.brasao:
            lbl_brasao = ttk.Label(frm_cabecalho, image=self.brasao, style='Header.TFrame')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))

        lbl_titulo = ttk.Label(frm_cabecalho, text="Criar Nova Planilha de Desfazimento", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black')
        lbl_titulo.pack(side=LEFT, expand=True, pady=5)

        frm_rodape = ttk.Frame(self.tpl_criar_planilha, padding=10)
        frm_rodape.pack(fill=X, side=BOTTOM)

        btn_voltar = ttk.Button(frm_rodape, text="<- Voltar", command=self.tpl_criar_planilha.destroy, bootstyle="primary-outline")
        btn_voltar.pack(side=LEFT, padx=30, pady=10)

        btn_criar_continuar = ttk.Button(frm_rodape, text="Criar e Continuar", command=self.confirmar_e_criar_arquivo, bootstyle="success")
        btn_criar_continuar.pack(side=RIGHT, padx=30, pady=10)

        frm_corpo = ttk.Frame(self.tpl_criar_planilha, padding=(40, 30))
        frm_corpo.pack(expand=True, fill=BOTH)

        lbl_nome = ttk.Label(frm_corpo, text="Nome da Planilha (sem extensão)", font=("Inconsolata", 12, "bold"))
        lbl_nome.pack(fill=X, anchor=W, pady=(0, 5))

        self.ent_nome = ttk.Entry(frm_corpo, font=("Inconsolata", 11))
        ano_atual = datetime.now().year
        self.ent_nome.insert(0, f"RELATÓRIO DE DESFAZIMENTO DE BENS MÓVEIS PATRIMONIAIS DE {ano_atual}")
        self.ent_nome.pack(fill=X, ipady=5, pady=(0, 20))
        
        lbl_processo = ttk.Label(frm_corpo, text="Número do Processo", font=("Inconsolata", 12, "bold"))
        lbl_processo.pack(fill=X, anchor=W, pady=(0, 5))
        self.ent_processo = ttk.Entry(frm_corpo, font=("Inconsolata", 11))
        self.ent_processo.insert(0, f"23107.000000/{ano_atual}-00")
        self.ent_processo.pack(fill=X, ipady=5, pady=(0, 20))

        lbl_data = ttk.Label(frm_corpo, text="Data da Planilha", font=("Inconsolata", 12, "bold"))
        lbl_data.pack(fill=X, anchor=W, pady=(0, 5))
        self.date_entry = ttk.DateEntry(frm_corpo, bootstyle="info", dateformat="%d/%m/%Y")
        self.date_entry.pack(fill=X, ipady=2, pady=(0, 20))
        lbl_pasta = ttk.Label(frm_corpo, text="Pasta de Salvamento", font=("Inconsolata", 12, "bold"))
        lbl_pasta.pack(fill=X, anchor=W, pady=(0, 5))
        frm_pasta = ttk.Frame(frm_corpo)
        frm_pasta.pack(fill=X, pady=(0, 25))
        self.ent_pasta = ttk.Entry(frm_pasta, font=("Inconsolata", 11))
        self.ent_pasta.pack(side=LEFT, fill=X, expand=True, ipady=5)
        btn_selecionar = ttk.Button(frm_pasta, text="Selecionar Pasta", bootstyle="info-outline", style='custom.TButton', command=self.selecionar_pasta)
        btn_selecionar.pack(side=LEFT, padx=(5, 0))

    def selecionar_pasta(self):
        """Abre uma caixa de diálogo para selecionar uma pasta."""
        caminho = filedialog.askdirectory(title="Selecione uma pasta para salvar")
        if caminho:
            self.ent_pasta.delete(0, END)
            self.ent_pasta.insert(0, caminho)

    def confirmar_e_criar_arquivo(self):
        """Valida, cria o registro no BD, cria o ficheiro .xlsx, regista a planilha no BD e abre a tela de edição."""
        nome_arquivo = self.ent_nome.get().strip()
        pasta_destino = self.ent_pasta.get().strip()
        numero_processo = self.ent_processo.get().strip()
        data_selecionada = self.date_entry.entry.get()
        
        if not all([nome_arquivo, pasta_destino, numero_processo, data_selecionada]):
            Messagebox.show_error(title="Erro de Validação", message="Todos os campos são obrigatórios.")
            return

        try:
            data_formatada_bd = datetime.strptime(data_selecionada, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            Messagebox.show_error(title="Erro de Data", message="Formato de data inválido. Use DD/MM/AAAA.")
            return
            
        novo_desfazimento_id = self.db.criar_novo_desfazimento(numero_processo, data_formatada_bd)
        
        if novo_desfazimento_id is None: return

        caminho_completo = os.path.join(pasta_destino, f"{nome_arquivo}.xlsx")
        
        if os.path.exists(caminho_completo):
            resposta = Messagebox.yesno(title="Ficheiro Existente", message=f"O ficheiro '{nome_arquivo}.xlsx' já existe.\nDeseja sobrescrevê-lo?")
            if not resposta: return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            cabecalho = ['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO']
            sheet.append(cabecalho)
            
            # Cria uma nova aba (sheet) para guardar o ID
            id_sheet = workbook.create_sheet(title="sap_ufac_meta")
            id_sheet['A1'] = "id_desfazimento"
            id_sheet['B1'] = novo_desfazimento_id  # Salva o ID retornado pelo banco
            
            # Oculta a aba para o usuário não ver
            id_sheet.sheet_state = 'hidden'
            # --- FIM DO CÓDIGO NOVO ---
            
            workbook.save(caminho_completo)
        except Exception as e:
            Messagebox.show_error(title="Erro ao Criar Ficheiro", message=f"Não foi possível criar o ficheiro:\n{e}")
            return

        # --- Regista a planilha no banco de dados IMEDIATAMENTE ---
        self.db.salvar_ou_atualizar_planilha_finalizada(
            id_desfazimento=novo_desfazimento_id,
            nome_planilha=nome_arquivo,
            caminho=caminho_completo,
            total_tombos=0 # A planilha começa com 0 tombos
        )

        # --- NOVO: Define esta planilha como a ativa no menu principal ---
        info_nova_planilha = {
            'id_desfazimento': novo_desfazimento_id,
            'caminho': caminho_completo,
            'nome': nome_arquivo
        }
        self.menu_principal.definir_planilha_ativa(info_nova_planilha)
        
        self.tpl_criar_planilha.destroy()
        
        tela_de_edicao = EdicaoPlanilha(
            self.master, 
            nome_arquivo, 
            caminho_arquivo_aberto=caminho_completo, 
            dados_iniciais=[],
            db_controller=self.db,
            id_desfazimento=novo_desfazimento_id
        )
        tela_de_edicao.exibir_tela()
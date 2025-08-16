import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
import openpyxl

# Importa a classe da tela de edição
from pl_des_edit import EdicaoPlanilha

class CriarPlanilha:
    def __init__(self, master):
        self.master = master
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
        self.tpl_criar_planilha.grab_set()

        # Configuração da UI (cabeçalho, rodapé, corpo, etc.)...
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure(
            'custom.TButton', 
            font=("Inconsolata", 14),
            borderwidth=1,
            padding=(10, 10),
            background='white',
            foreground='#5bc0de'
        )
        style.map('custom.TButton',
            bordercolor=[('!active', '#adb5bd'), ('active', '#5bc0de')],
            background=[('active', "#ececec"), ('!active', 'white')],
            relief=[('pressed', 'solid'), ('!pressed', 'solid')]
        )

        frm_cabecalho = ttk.Frame(self.tpl_criar_planilha, style='Header.TFrame', padding=(10, 5))
        frm_cabecalho.pack(fill=X, side=TOP)

        if self.brasao:
            lbl_brasao = ttk.Label(frm_cabecalho, image=self.brasao, style='Header.TFrame')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))

        lbl_titulo = ttk.Label(
            frm_cabecalho, text="Criar Nova Planilha de Desfazimento",
            font=("Inconsolata", 18, "bold"), background='#5bc0de', foreground='black'
        )
        lbl_titulo.pack(side=LEFT, expand=True, pady=5)

        frm_rodape = ttk.Frame(self.tpl_criar_planilha, padding=10)
        frm_rodape.pack(fill=X, side=BOTTOM)

        btn_voltar = ttk.Button(
            frm_rodape, text="<- Voltar",
            command=self.tpl_criar_planilha.destroy, bootstyle="light-outline", style='custom.TButton'
        )
        btn_voltar.pack(side=LEFT)

        btn_criar_continuar = ttk.Button(
            frm_rodape, text="Criar e Continuar",
            command=self.confirmar_e_criar_arquivo, bootstyle="info", style='custom.TButton'
        )
        btn_criar_continuar.pack(side=RIGHT)

        frm_corpo = ttk.Frame(self.tpl_criar_planilha, padding=(40, 30))
        frm_corpo.pack(expand=True, fill=BOTH)

        lbl_nome = ttk.Label(frm_corpo, text="Nome da Planilha (sem extensão)", font=("Inconsolata", 12, "bold"))
        lbl_nome.pack(fill=X, anchor=W, pady=(0, 5))

        self.ent_nome = ttk.Entry(frm_corpo, font=("Inconsolata", 11))
        ano_atual = datetime.now().year
        self.ent_nome.insert(0, f"RELATÓRIO DE DESFAZIMENTO DE BENS MÓVEIS PATRIMONIAIS DE {ano_atual}")
        self.ent_nome.pack(fill=X, ipady=5, pady=(0, 20))

        # ... (restante dos widgets do formulário)
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
        # ... (checkboxes)

    def selecionar_pasta(self):
        """Abre uma caixa de diálogo para selecionar uma pasta."""
        caminho = filedialog.askdirectory(title="Selecione uma pasta para salvar")
        if caminho:
            self.ent_pasta.delete(0, END)
            self.ent_pasta.insert(0, caminho)

    def confirmar_e_criar_arquivo(self):
        """Valida, pede confirmação, cria o arquivo .xlsx e abre a tela de edição."""
        nome_arquivo = self.ent_nome.get()
        pasta_destino = self.ent_pasta.get()
        
        if not nome_arquivo or not pasta_destino:
            Messagebox.show_error(title="Erro de Validação", message="O Nome da Planilha e a Pasta de Salvamento são obrigatórios.")
            return
            
        caminho_completo = os.path.join(pasta_destino, f"{nome_arquivo}.xlsx")
        
        if os.path.exists(caminho_completo):
            resposta_overwrite = Messagebox.yesno(title="Arquivo Existente", 
                                                    message=f"O arquivo '{nome_arquivo}.xlsx' já existe.\nDeseja sobrescrevê-lo?")
            if not resposta_overwrite:
                return

        try:
            # Cria um novo arquivo Excel em branco com o cabeçalho
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            cabecalho = ['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 
                        'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO']
            sheet.append(cabecalho)
            workbook.save(caminho_completo)
        except Exception as e:
            Messagebox.show_error(title="Erro ao Criar Arquivo", message=f"Não foi possível criar o arquivo:\n{e}")
            return

        # Fecha a janela atual e abre a de edição
        self.tpl_criar_planilha.destroy()
        tela_de_edicao = EdicaoPlanilha(self.master, nome_arquivo, caminho_arquivo_aberto=caminho_completo, dados_iniciais=[])
        tela_de_edicao.exibir_tela()

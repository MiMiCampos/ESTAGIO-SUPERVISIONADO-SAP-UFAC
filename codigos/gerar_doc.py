import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
import openpyxl

# Importa as classes das telas que serão chamadas a partir desta
from visualizar_planilha import VisualizarPlanilha
from org_baixa import OrganizacaoBaixas

# ----- Dados Fictícios -----
def carregar_planilhas_ficticias():
    """
    Simula o carregamento de planilhas de um banco de dados.
    Cada planilha é um dicionário que contém seus metadados e seu conteúdo completo.
    """
    return [
        {
            "nome": "RELATÓRIO DE DESFAZIMENTO DE BENS MÓVEIS PATRIMONIAIS DE 2018",
            "data": "01/18 - 12/18", "tombos": 1000,
            "conteudo": [
                ['1', '1001', 'Cadeira de Escritório', '10/01/2015', 'NF-111', 'CCET', 'BOM', 'Doação'],
                ['2', '1002', 'Mesa de Reunião', '15/02/2016', 'NF-222', 'Administração', 'REGULAR', 'Leilão']
            ]
        },
        {
            "nome": "RELATÓRIO DE DESFAZIMENTO DE BENS MÓVEIS PATRIMONIAIS DE 2019",
            "data": "01/19 - 12/19", "tombos": 1500,
            "conteudo": [
                ['1', '2001', 'Projetor Epson', '20/03/2017', 'NF-333', 'CCET', 'IRRECUPERÁVEL', 'Descarte'],
                ['2', '2002', 'Computador Dell', '25/04/2018', 'NF-444', 'CCET', 'BOM', 'Doação']
            ]
        },
    ]

class GerarDocumentos():
    # Este __init__ é simples e compatível com a chamada do tela_menu.py
    def __init__(self, master):
        self.janela_mestra_geradoc = master
        self.toplevel_geradoc = None
        self.carregar_recursos_geradoc()

    def carregar_recursos_geradoc(self):
        """Carrega as imagens necessárias para esta tela."""
        try:
            imagem_brasao_geradoc = Image.open("imagens/brasao_UFAC.png").resize((40, 40))
            self.brasao_para_geradoc = ImageTk.PhotoImage(imagem_brasao_geradoc)
        except Exception as e:
            print(f"Erro ao carregar brasão para Gerar Documentos: {e}")
            self.brasao_para_geradoc = None

    def gerar_doc(self):
        """Cria e exibe a janela principal para a geração de documentos."""
        if self.toplevel_geradoc and self.toplevel_geradoc.winfo_exists():
            self.toplevel_geradoc.lift()
            return

        self.toplevel_geradoc = ttk.Toplevel(self.janela_mestra_geradoc)
        self.toplevel_geradoc.title("Gerar Documentos")
        self.toplevel_geradoc.geometry("1000x700")
        self.toplevel_geradoc.position_center()
        self.toplevel_geradoc.transient(self.janela_mestra_geradoc)
        self.toplevel_geradoc.grab_set()

        # --- Cabeçalho ---
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        frame_cabecalho_geradoc = ttk.Frame(self.toplevel_geradoc, style='Header.TFrame', padding=(10, 5))
        frame_cabecalho_geradoc.pack(fill=X, side=TOP)
        if self.brasao_para_geradoc:
            lbl_brasao = ttk.Label(frame_cabecalho_geradoc, image=self.brasao_para_geradoc, style='Header.TFrame')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))
        lbl_titulo = ttk.Label(frame_cabecalho_geradoc, text="Gerar Documentos", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black')
        lbl_titulo.pack(side=LEFT, expand=True, pady=5)

        # --- Rodapé ---
        frame_rodape_geradoc = ttk.Frame(self.toplevel_geradoc, padding=10)
        frame_rodape_geradoc.pack(fill=X, side=BOTTOM)
        btn_voltar = ttk.Button(frame_rodape_geradoc, text="<- Voltar", command=self.toplevel_geradoc.destroy, bootstyle="primary-outline")
        btn_voltar.pack(side=LEFT, padx=12)

        # --- Frame Principal ---
        frame_corpo_geradoc = ttk.Frame(self.toplevel_geradoc, padding=(20, 20))
        frame_corpo_geradoc.pack(expand=True, fill=BOTH)

        # --- Filtros e Pesquisa ---
        frame_filtros = ttk.Frame(frame_corpo_geradoc)
        frame_filtros.pack(fill=X, pady=(0, 15))
        ttk.Label(frame_filtros, text="Filtros (a implementar):").pack(anchor=W)

        # --- Lista de Planilhas ---
        frame_lista_planilhas = ttk.Labelframe(frame_corpo_geradoc, text="Todas as Planilhas", padding=10)
        frame_lista_planilhas.pack(expand=True, fill=BOTH)

        # Cabeçalho da lista
        frame_cabecalho_lista = ttk.Frame(frame_lista_planilhas)
        frame_cabecalho_lista.pack(fill=X, pady=(0, 5))
        ttk.Label(frame_cabecalho_lista, text="Todas as Planilhas", font=("Inconsolata", 12, "bold")).grid(row=0, column=0, sticky=W)
        ttk.Label(frame_cabecalho_lista, text="Data", font=("Inconsolata", 12, "bold")).grid(row=0, column=1, sticky=W, padx=10)
        ttk.Label(frame_cabecalho_lista, text="Tombos", font=("Inconsolata", 12, "bold")).grid(row=0, column=2, sticky=W, padx=10)
        ttk.Label(frame_cabecalho_lista, text="Ações", font=("Inconsolata", 12, "bold")).grid(row=0, column=3, sticky=W, padx=10)
        frame_cabecalho_lista.grid_columnconfigure(0, weight=4)
        frame_cabecalho_lista.grid_columnconfigure(1, weight=1)
        frame_cabecalho_lista.grid_columnconfigure(2, weight=1)
        frame_cabecalho_lista.grid_columnconfigure(3, weight=2)

        ttk.Separator(frame_lista_planilhas).pack(fill=X, pady=(0, 10))

        planilhas = carregar_planilhas_ficticias()
        for planilha in planilhas:
            self.criar_linha_planilha(frame_lista_planilhas, planilha)

    def criar_linha_planilha(self, parent, planilha_data):
        """Cria uma linha visual para uma planilha na lista."""
        frame_linha = ttk.Frame(parent)
        frame_linha.pack(fill=X, pady=5)

        ttk.Label(frame_linha, text=planilha_data['nome'], anchor=W).grid(row=0, column=0, sticky=EW)
        ttk.Label(frame_linha, text=planilha_data['data'], anchor=W).grid(row=0, column=1, sticky=EW, padx=10)
        ttk.Label(frame_linha, text=planilha_data['tombos'], anchor=W).grid(row=0, column=2, sticky=EW, padx=10)

        frame_acoes = ttk.Frame(frame_linha)
        frame_acoes.grid(row=0, column=3, sticky=EW, padx=10)
        
        btn_abrir = ttk.Button(frame_acoes, text="Abrir", bootstyle="link-info", command=lambda p=planilha_data: self.abrir_planilha_visualizacao(p))
        btn_abrir.pack(side=LEFT, padx=5)
        btn_download = ttk.Button(frame_acoes, text="Download", bootstyle="link-info", command=lambda p=planilha_data: self.download_planilha(p))
        btn_download.pack(side=LEFT, padx=5)
        btn_baixa = ttk.Button(frame_acoes, text="Baixa", bootstyle="link-info", command=lambda p=planilha_data: self.navegar_para_baixas(p))
        btn_baixa.pack(side=LEFT, padx=5)

        frame_linha.grid_columnconfigure(0, weight=4)
        frame_linha.grid_columnconfigure(1, weight=1)
        frame_linha.grid_columnconfigure(2, weight=1)
        frame_linha.grid_columnconfigure(3, weight=2)
    
    def abrir_planilha_visualizacao(self, planilha):
        """Abre a tela de visualização para a planilha selecionada."""
        tela_visualizar = VisualizarPlanilha(self.toplevel_geradoc, planilha['nome'], planilha['conteudo'])
        tela_visualizar.exibir_tela()

    def download_planilha(self, planilha):
        """Pede confirmação e baixa a planilha como .xlsx."""
        resposta = Messagebox.askyesno(title="Confirmar Download", message=f"Deseja baixar a planilha '{planilha['nome']}'?")
        if not resposta:
            return

        caminho_arquivo = filedialog.asksaveasfilename(
            title="Salvar planilha como...",
            defaultextension=".xlsx",
            initialfile=planilha['nome'],
            filetypes=[("Planilhas Excel", "*.xlsx")]
        )
        if not caminho_arquivo:
            return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Relatório"
            sheet.append(['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO'])
            for linha in planilha['conteudo']:
                sheet.append(linha)
            workbook.save(caminho_arquivo)
            Messagebox.ok(title="Sucesso", message=f"Planilha baixada com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            Messagebox.show_error(title="Erro", message=f"Não foi possível salvar o arquivo:\n{e}")

    def navegar_para_baixas(self, planilha):
        """Abre a tela de Organização de Baixas com os dados da planilha selecionada."""
        # ***** CORREÇÃO ABAIXO *****
        # 1. Destrói a janela atual para liberar o 'grab_set' completamente.
        self.toplevel_geradoc.destroy()
        
        # 2. Cria a nova tela passando a janela de menu principal como 'master',
        #    e não a janela que acabamos de destruir.
        tela_baixas = OrganizacaoBaixas(
            self.janela_mestra_geradoc, 
            nome_planilha=planilha['nome'], 
            dados_para_agrupar=planilha['conteudo']
        )
        tela_baixas.org_baixas()

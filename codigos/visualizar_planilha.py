import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from utils.excel_formatador import FormatadorExcel

class VisualizarPlanilha:
    def __init__(self, master, nome_planilha, dados_planilha):
        self.janela_mestra_visualizar = master
        self.nome_da_planilha_visualizada = nome_planilha
        self.dados_para_visualizar = dados_planilha
        self.toplevel_visualizar = None

    def exibir_tela(self):
        """Cria e exibe a janela de visualização da planilha."""
        if self.toplevel_visualizar and self.toplevel_visualizar.winfo_exists():
            self.toplevel_visualizar.lift()
            return

        self.toplevel_visualizar = ttk.Toplevel(self.janela_mestra_visualizar)
        self.toplevel_visualizar.title(f"Visualizando: {self.nome_da_planilha_visualizada}")
        self.toplevel_visualizar.geometry("1100x600")
        self.toplevel_visualizar.transient(self.janela_mestra_visualizar)
        self.toplevel_visualizar.grab_set()

        frame_rodape_visualizar = ttk.Frame(self.toplevel_visualizar, padding=10)
        frame_rodape_visualizar.pack(fill=X, side=BOTTOM)
        ttk.Button(frame_rodape_visualizar, text="<- Voltar", command=self.toplevel_visualizar.destroy, bootstyle="primary-outline").pack(side=LEFT)
        ttk.Button(frame_rodape_visualizar, text="Baixar Planilha (.xlsx)", command=self.baixar_planilha_visualizada, bootstyle="info").pack(side=RIGHT)

        frame_corpo_visualizar = ttk.Frame(self.toplevel_visualizar, padding=10)
        frame_corpo_visualizar.pack(expand=True, fill=BOTH)
        
        lbl_titulo_planilha = ttk.Label(
            frame_corpo_visualizar, 
            text=self.nome_da_planilha_visualizada,
            font=("Inconsolata", 14, "bold")
        )
        lbl_titulo_planilha.pack(anchor=W, pady=(0, 10))

        frame_tabela_visualizar = ttk.Frame(frame_corpo_visualizar)
        frame_tabela_visualizar.pack(expand=True, fill=BOTH)

        colunas = ('ordem', 'tombo', 'descricao', 'data_aq', 'doc_fiscal', 'unidade', 'classificacao', 'destino')
        tabela = ttk.Treeview(frame_tabela_visualizar, columns=colunas, show='headings', bootstyle="info")

        headings = ['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO']
        for col, head in zip(colunas, headings):
            tabela.heading(col, text=head)
        
        for linha in self.dados_para_visualizar:
            tabela.insert('', END, values=linha)

        scrollbar_y = ttk.Scrollbar(frame_tabela_visualizar, orient=VERTICAL, command=tabela.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela_visualizar, orient=HORIZONTAL, command=tabela.xview)
        tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        tabela.pack(expand=True, fill=BOTH)

    def baixar_planilha_visualizada(self):
        """Função para baixar a planilha que está sendo visualizada, com formatação centralizada."""
        caminho_arquivo = filedialog.asksaveasfilename(
            title="Salvar planilha como...",
            defaultextension=".xlsx",
            initialfile=self.nome_da_planilha_visualizada,
            filetypes=[("Planilhas Excel", "*.xlsx")]
        )
        if not caminho_arquivo:
            return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            
            # Usa a mesma função central para formatar
            FormatadorExcel.formatar_planilha_desfazimento(
                workbook, 
                sheet, 
                self.nome_da_planilha_visualizada, 
                self.dados_para_visualizar
            )

            workbook.save(caminho_arquivo)
            Messagebox.ok(title="Sucesso", message=f"Planilha baixada com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            Messagebox.show_error(title="Erro ao Salvar", message=f"Não foi possível salvar o ficheiro:\n{e}")
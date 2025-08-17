import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import openpyxl

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

        # --- Rodapé com botões ---
        frame_rodape_visualizar = ttk.Frame(self.toplevel_visualizar, padding=10)
        frame_rodape_visualizar.pack(fill=X, side=BOTTOM)
        ttk.Button(frame_rodape_visualizar, text="<- Voltar", command=self.toplevel_visualizar.destroy, bootstyle="light-outline").pack(side=LEFT)
        ttk.Button(frame_rodape_visualizar, text="Baixar Planilha (.xlsx)", command=self.baixar_planilha_visualizada, bootstyle="info").pack(side=RIGHT)

        # --- Tabela (Treeview) para exibir os dados ---
        frame_tabela_visualizar = ttk.Frame(self.toplevel_visualizar, padding=10)
        frame_tabela_visualizar.pack(expand=True, fill=BOTH)

        colunas = ('ordem', 'tombo', 'descricao', 'data_aq', 'doc_fiscal', 'unidade', 'classificacao', 'destino')
        tabela = ttk.Treeview(frame_tabela_visualizar, columns=colunas, show='headings', bootstyle="info")

        headings = ['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO']
        for col, head in zip(colunas, headings):
            tabela.heading(col, text=head)
        
        # Adiciona os dados na tabela
        for linha in self.dados_para_visualizar:
            tabela.insert('', END, values=linha)

        # Barras de rolagem
        scrollbar_y = ttk.Scrollbar(frame_tabela_visualizar, orient=VERTICAL, command=tabela.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela_visualizar, orient=HORIZONTAL, command=tabela.xview)
        tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        tabela.pack(expand=True, fill=BOTH)

    def baixar_planilha_visualizada(self):
        """Função para baixar a planilha que está sendo visualizada."""
        # Esta função é muito similar à da tela anterior
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
            sheet.title = "Relatório"
            sheet.append(['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO'])
            for linha in self.dados_para_visualizar:
                sheet.append(linha)
            workbook.save(caminho_arquivo)
            Messagebox.ok(title="Sucesso", message=f"Planilha baixada com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            Messagebox.show_error(title="Erro", message=f"Não foi possível salvar o arquivo:\n{e}")

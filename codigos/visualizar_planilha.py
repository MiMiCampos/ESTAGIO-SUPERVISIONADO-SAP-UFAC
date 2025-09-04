import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side

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
        ttk.Button(frame_rodape_visualizar, text="<- Voltar", command=self.toplevel_visualizar.destroy, bootstyle="light-outline").pack(side=LEFT)
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
        """Função para baixar a planilha que está sendo visualizada, com formatação completa."""
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
            sheet.title = "Relatório de Desfazimento"
            
            # 1. Adiciona e formata o título principal
            sheet.merge_cells('A1:H1')
            titulo_cell = sheet['A1']
            titulo_cell.value = self.nome_da_planilha_visualizada
            titulo_cell.font = Font(bold=True, size=14, name='Times New Roman')
            titulo_cell.alignment = Alignment(horizontal='center', vertical='center')

            # 2. Adiciona o cabeçalho dos dados
            cabecalho = ['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO']
            sheet.append(cabecalho)

            # 3. Adiciona os dados da planilha
            for linha in self.dados_para_visualizar:
                sheet.append(linha)

            # --- MUDANÇA PRINCIPAL: Estilos com quebra de linha e larguras fixas ---
            
            # 4. Define os estilos
            alinhamento_central_com_quebra = Alignment(horizontal='center', vertical='center', wrap_text=True)
            borda_fina = Border(left=Side(style='thin'), 
                                right=Side(style='thin'), 
                                top=Side(style='thin'), 
                                bottom=Side(style='thin'))
            fonte_cabecalho = Font(bold=True, size=12, name='Times New Roman')
            fonte_dados = Font(size=12, name='Times New Roman')
            
            # 5. Define larguras fixas para as colunas (A até H)
            larguras = {'A': 15, 'B': 15, 'C': 40, 'D': 20, 'E': 25, 'F': 40, 'G': 20, 'H': 20}
            for letra_coluna, largura in larguras.items():
                sheet.column_dimensions[letra_coluna].width = largura

            # 6. Formata o cabeçalho (linha 2)
            sheet.row_dimensions[2].height = 40 # Aumenta a altura da linha do cabeçalho
            for cell in sheet[2]:
                cell.alignment = alinhamento_central_com_quebra
                cell.border = borda_fina
                cell.font = fonte_cabecalho

            # 7. Formata as células de dados (a partir da linha 3)
            # O ajuste da altura da linha será automático por causa do wrap_text=True
            for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row):
                for cell in row:
                    cell.alignment = alinhamento_central_com_quebra
                    cell.border = borda_fina
                    cell.font = fonte_dados

            workbook.save(caminho_arquivo)
            Messagebox.ok(title="Sucesso", message=f"Planilha baixada com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            Messagebox.show_error(title="Erro ao Salvar", message=f"Não foi possível salvar o ficheiro:\n{e}")
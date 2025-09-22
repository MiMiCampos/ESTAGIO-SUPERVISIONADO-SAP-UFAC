import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
import openpyxl
from datetime import datetime
from openpyxl.styles import Font, Alignment, Border, Side
from utils.excel_formatador import FormatadorExcel
from utils.path_helper import resource_path

from visualizar_planilha import VisualizarPlanilha
from org_baixa import OrganizacaoBaixas

class GerarDocumentos():
    def __init__(self, master, db_controller):
        self.janela_mestra_geradoc = master
        self.db = db_controller
        self.toplevel_geradoc = None
        self.carregar_recursos_geradoc()

    def carregar_recursos_geradoc(self):
        """Carrega as imagens necessárias para esta tela."""
        try:
            imagem_brasao_geradoc = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
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
        # self.toplevel_geradoc.grab_set()

        frame_cabecalho_geradoc = ttk.Frame(self.toplevel_geradoc, bootstyle='info', padding=(10, 5))
        frame_cabecalho_geradoc.pack(fill=X, side=TOP)
        
        if self.brasao_para_geradoc:
            lbl_brasao = ttk.Label(frame_cabecalho_geradoc, image=self.brasao_para_geradoc, bootstyle='info')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))
            
        lbl_titulo = ttk.Label(frame_cabecalho_geradoc, text="Gerar Documentos", font=("Inconsolata", 16, "bold"), bootstyle='inverse-info', foreground='black')
        lbl_titulo.pack(side=LEFT, expand=True, pady=5)

        frame_rodape_geradoc = ttk.Frame(self.toplevel_geradoc, padding=10)
        frame_rodape_geradoc.pack(fill=X, side=BOTTOM)
        btn_voltar = ttk.Button(frame_rodape_geradoc, text="<- Voltar", command=self.toplevel_geradoc.destroy, bootstyle="primary-outline")
        btn_voltar.pack(side=LEFT, padx=12)

        frame_corpo_geradoc = ttk.Frame(self.toplevel_geradoc, padding=(20, 20))
        frame_corpo_geradoc.pack(expand=True, fill=BOTH)

        frame_filtros = ttk.Frame(frame_corpo_geradoc)
        frame_filtros.pack(fill=X, pady=(0, 15))
        ttk.Label(frame_filtros, text="Filtros (a implementar):").pack(anchor=W)

        frame_lista_planilhas = ttk.Labelframe(frame_corpo_geradoc, text="Todas as Planilhas", padding=10)
        frame_lista_planilhas.pack(expand=True, fill=BOTH)

        frame_cabecalho_lista = ttk.Frame(frame_lista_planilhas)
        frame_cabecalho_lista.pack(fill=X, pady=(0, 5))
        ttk.Label(frame_cabecalho_lista, text="Nome da Planilha", font=("Inconsolata", 12, "bold")).grid(row=0, column=0, sticky=W)
        ttk.Label(frame_cabecalho_lista, text="Data", font=("Inconsolata", 12, "bold")).grid(row=0, column=1, sticky=W, padx=10)
        ttk.Label(frame_cabecalho_lista, text="Tombos", font=("Inconsolata", 12, "bold")).grid(row=0, column=2, sticky=W, padx=10)
        ttk.Label(frame_cabecalho_lista, text="Ações", font=("Inconsolata", 12, "bold")).grid(row=0, column=3, sticky=W, padx=10)
        frame_cabecalho_lista.grid_columnconfigure(0, weight=4)
        frame_cabecalho_lista.grid_columnconfigure(1, weight=1)
        frame_cabecalho_lista.grid_columnconfigure(2, weight=1)
        frame_cabecalho_lista.grid_columnconfigure(3, weight=2)
        
        ttk.Separator(frame_lista_planilhas).pack(fill=X, pady=(0, 10))

        planilhas_do_banco = self.db.get_planilhas_finalizadas()
        if not planilhas_do_banco:
            ttk.Label(frame_lista_planilhas, text="Nenhuma planilha finalizada encontrada no banco de dados.").pack()
        else:
            for planilha in planilhas_do_banco:
                self.criar_linha_planilha(frame_lista_planilhas, planilha)

    def criar_linha_planilha(self, parent, planilha_data):
        """Cria uma linha visual para uma planilha na lista."""
        frame_linha = ttk.Frame(parent)
        frame_linha.pack(fill=X, pady=5)
        
        nome = planilha_data.get('nome_planilha', 'N/A')
        data_geracao = planilha_data.get('data_geracao', 'N/A')
        
        if isinstance(data_geracao, datetime):
            data_formatada = data_geracao.strftime('%d/%m/%Y')
        else:
            data_formatada = 'N/A'

        total_tombos = planilha_data.get('total_tombos', 0)

        ttk.Label(frame_linha, text=nome, anchor=W).grid(row=0, column=0, sticky=EW)
        ttk.Label(frame_linha, text=data_formatada, anchor=W).grid(row=0, column=1, sticky=EW, padx=10)
        ttk.Label(frame_linha, text=total_tombos, anchor=W).grid(row=0, column=2, sticky=EW, padx=10)

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
        """Busca os dados dos bens da planilha e abre a tela de visualização."""
        id_desfazimento = planilha.get('id_desfazimento')
        if id_desfazimento is None:
            Messagebox.show_error("Erro", "Não foi possível encontrar o ID de desfazimento para esta planilha.")
            return

        conteudo_planilha = self.db.get_bens_para_visualizacao(id_desfazimento)
        
        # Fecha a janela atual para focar na nova
        self.toplevel_geradoc.destroy()
        
        tela_visualizar = VisualizarPlanilha(self.janela_mestra_geradoc, planilha.get('nome_planilha'), conteudo_planilha)
        tela_visualizar.exibir_tela()

    def download_planilha(self, planilha):
        """Busca os dados da planilha e os salva em um ficheiro .xlsx usando o formatador central."""
        id_desfazimento = planilha.get('id_desfazimento')
        nome_planilha = planilha.get('nome_planilha', 'planilha_sem_nome')
        
        if id_desfazimento is None:
            Messagebox.show_error("Erro", "Não foi possível encontrar o ID de desfazimento para esta planilha.")
            return

        dados_para_baixar = self.db.get_bens_por_desfazimento(id_desfazimento)
        
        if not dados_para_baixar:
            Messagebox.show_info("Aviso", "Não há dados para baixar para esta planilha.")
            return

        caminho_arquivo = filedialog.asksaveasfilename(
            title="Salvar planilha como...",
            defaultextension=".xlsx",
            initialfile=nome_planilha,
            filetypes=[("Planilhas Excel", "*.xlsx")]
        )
        if not caminho_arquivo:
            return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            
            # Chama a função central para fazer todo o trabalho de formatação!
            FormatadorExcel.formatar_planilha_desfazimento(workbook, sheet, nome_planilha, dados_para_baixar)

            workbook.save(caminho_arquivo)
            Messagebox.ok(title="Sucesso", message=f"Planilha baixada com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            Messagebox.show_error(title="Erro ao Salvar", message=f"Não foi possível salvar o ficheiro:\n{e}")

    def navegar_para_baixas(self, planilha):
        """Busca os bens associados a esta planilha e navega para a tela de baixas."""

        id_desfazimento = planilha.get('id_desfazimento')
        numero_processo = planilha.get('numero_processo')

        if id_desfazimento is None:
            Messagebox.show_error("Erro", "Não foi possível encontrar o ID de desfazimento para esta planilha.")
            return

        dados_brutos_dos_bens = self.db.get_bens_por_desfazimento(id_desfazimento)
        if not dados_brutos_dos_bens:
            Messagebox.show_info("Aviso", "Nenhum bem associado a esta planilha foi encontrado para organizar a baixa.")
            return

        self.toplevel_geradoc.destroy()
        
        tela_baixas = OrganizacaoBaixas(
            self.janela_mestra_geradoc,
            nome_planilha=planilha.get('nome_planilha'),
            dados_para_agrupar=dados_brutos_dos_bens,
            numero_processo=numero_processo,
            id_desfazimento=id_desfazimento
        )
        tela_baixas.org_baixas()
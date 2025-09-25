import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import os
import subprocess
import sys
from datetime import datetime

class ConsultaDocumentos:
    def __init__(self, master, db_controller):
        self.janela_mestra = master
        self.db = db_controller
        self.toplevel = ttk.Toplevel(self.janela_mestra)
        self.toplevel.title("Consultar Documentos de Baixa Gerados")
        self.toplevel.geometry("1100x700")
        self.toplevel.position_center()
        
        self.criar_interface()

    def criar_interface(self):
        # --- Frame do Cabeçalho ---
        frame_cabecalho = ttk.Frame(self.toplevel, bootstyle='info', padding=(10, 10))
        frame_cabecalho.pack(fill=X)
        lbl_titulo = ttk.Label(
            frame_cabecalho, 
            text="Documentos de Baixa Gerados", 
            font=("Inconsolata", 16, "bold"), 
            bootstyle='inverse-info'
        )
        lbl_titulo.pack()

        # --- Frame Principal com a Lista ---
        frame_principal = ttk.Frame(self.toplevel, padding=20)
        frame_principal.pack(expand=True, fill=BOTH)

        sf = ScrolledFrame(frame_principal, autohide=True)
        sf.pack(fill=BOTH, expand=YES)
        
        # --- Busca os dados e preenche a lista ---
        documentos = self.db.get_documentos_gerados()

        if not documentos:
            ttk.Label(sf, text="Nenhum documento de baixa foi gerado ainda.", font=("Helvetica", 12)).pack(pady=20)
            return

        # Cabeçalho da lista
        frame_header = ttk.Frame(sf)
        frame_header.pack(fill=X, padx=10, pady=(0,5))
        
        # --- CORREÇÃO APLICADA AQUI ---
        ttk.Label(frame_header, text="Termo", font=("Helvetica", 10, "bold"), width=20).pack(side=LEFT)
        ttk.Label(frame_header, text="Data", font=("Helvetica", 10, "bold"), width=20).pack(side=LEFT)
        ttk.Label(frame_header, text="Processo", font=("Helvetica", 10, "bold"), width=25).pack(side=LEFT)
        ttk.Label(frame_header, text="Motivo", font=("Helvetica", 10, "bold")).pack(side=LEFT, fill=X, expand=True)
        ttk.Label(frame_header, text="Ações", font=("Helvetica", 10, "bold"), width=25).pack(side=RIGHT)
        ttk.Separator(sf).pack(fill=X, padx=10, pady=(0, 10))

        for doc in documentos:
            self.criar_linha_documento(sf, doc)

    def criar_linha_documento(self, parent, doc_data):
        frame_linha = ttk.Frame(parent)
        frame_linha.pack(fill=X, padx=10, pady=5)
        
        # Extrai e formata os dados
        termo = doc_data.get('numero_termo', 'N/A')
        data_geracao = doc_data.get('data_geracao')
        data_formatada = data_geracao.strftime('%d/%m/%Y %H:%M') if isinstance(data_geracao, datetime) else 'N/A'
        processo = doc_data.get('numero_processo', 'N/A')
        motivo = doc_data.get('motivo', 'N/A')
        caminho = doc_data.get('caminho_arquivo', '')

        # Cria os labels e botões
        ttk.Label(frame_linha, text=termo, width=20).pack(side=LEFT)
        ttk.Label(frame_linha, text=data_formatada, width=20).pack(side=LEFT)
        ttk.Label(frame_linha, text=processo, width=25).pack(side=LEFT)
        ttk.Label(frame_linha, text=motivo, anchor='w').pack(side=LEFT, fill=X, expand=True)

        frame_acoes = ttk.Frame(frame_linha, width=25)
        frame_acoes.pack(side=RIGHT)
        
        btn_abrir = ttk.Button(frame_acoes, text="Abrir Arquivo", bootstyle="info-outline", width=12,
                               command=lambda p=caminho: self._abrir_arquivo(p))
        btn_abrir.pack(side=LEFT, padx=(0,5))
        
        btn_pasta = ttk.Button(frame_acoes, text="Abrir Pasta", bootstyle="secondary-outline", width=10,
                               command=lambda p=caminho: self._abrir_pasta(p))
        btn_pasta.pack(side=LEFT)

    def _abrir_arquivo(self, caminho):
        if not caminho or not os.path.exists(caminho):
            Messagebox.show_warning("Arquivo não encontrado", f"O arquivo não existe mais no caminho original:\n{caminho}", parent=self.toplevel)
            return
        
        try:
            if sys.platform == "win32":
                os.startfile(caminho)
            elif sys.platform == "darwin": # macOS
                subprocess.run(["open", caminho])
            else: # linux
                subprocess.run(["xdg-open", caminho])
        except Exception as e:
            Messagebox.show_error("Erro", f"Não foi possível abrir o arquivo:\n{e}", parent=self.toplevel)

    def _abrir_pasta(self, caminho):
        if not caminho or not os.path.exists(caminho):
            Messagebox.show_warning("Caminho não encontrado", f"O caminho original do arquivo não foi encontrado:\n{caminho}", parent=self.toplevel)
            return

        pasta = os.path.dirname(caminho)
        try:
            if sys.platform == "win32":
                os.startfile(pasta)
            elif sys.platform == "darwin": # macOS
                subprocess.run(["open", pasta])
            else: # linux
                subprocess.run(["xdg-open", pasta])
        except Exception as e:
            Messagebox.show_error("Erro", f"Não foi possível abrir a pasta:\n{e}", parent=self.toplevel)
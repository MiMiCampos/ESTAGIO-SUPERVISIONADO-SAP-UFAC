import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import os
import subprocess
import sys
from datetime import datetime
from PIL import Image, ImageTk

class ConsultaDocumentos:
    def __init__(self, master, db_controller, id_desfazimento=None):
        self.janela_mestra = master
        self.db = db_controller
        self.id_desfazimento = id_desfazimento
        self.toplevel = ttk.Toplevel(self.janela_mestra)
        self.toplevel.title("Consultar Documentos de Baixa Gerados")
        # self.toplevel.geometry("1100x700")
        # self.toplevel.position_center()
        
        screen_width = self.toplevel.winfo_screenwidth()
        screen_height = self.toplevel.winfo_screenheight()
        self.toplevel.geometry(f"{screen_width}x{screen_height}+0+0")  

        self.brasao = None
        self.carregar_recursos()
        self.criar_interface()
    
    def carregar_recursos(self):
        """Carrega as imagens necessárias (apenas o brasão)."""
        try:
            # Ajuste o caminho da imagem se necessário, use resource_path se empacotado
            imagem_brasao = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(imagem_brasao)
        except Exception as e:
            print(f"Erro ao carregar imagem do brasão para ConsultaDocumentos: {e}")
            self.brasao = None

    def criar_interface(self):
        frame_cabecalho = ttk.Frame(self.toplevel, bootstyle='info', padding=(10, 10))
        frame_cabecalho.pack(fill=X)
        
        if self.brasao:
            lbl_brasao = ttk.Label(frame_cabecalho, image=self.brasao, bootstyle='info')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))
        
        lbl_titulo = ttk.Label(
            frame_cabecalho, text="Documentos de Baixa Gerados", 
            font=("Inconsolata", 16, "bold"), bootstyle='inverse-info'
        )
        lbl_titulo.pack()

        frame_principal = ttk.Frame(self.toplevel, padding=20)
        frame_principal.pack(expand=True, fill=BOTH)

        sf = ScrolledFrame(frame_principal, autohide=True)
        sf.pack(fill=BOTH, expand=YES)
        
        # --- LÓGICA DE BUSCA ATUALIZADA ---
        # Se um ID foi passado, busca os documentos filtrados. Senão, busca todos.
        if self.id_desfazimento:
            documentos = self.db.get_documentos_por_desfazimento(self.id_desfazimento)
            titulo_filtro = ttk.Label(sf, text=f"Exibindo documentos apenas da planilha selecionada.", bootstyle="secondary")
            titulo_filtro.pack(pady=(0, 10))
        else:
            documentos = self.db.get_documentos_gerados()

        if not documentos:
            msg = "Nenhum documento de baixa foi gerado para esta planilha." if self.id_desfazimento else "Nenhum documento de baixa foi gerado ainda."
            ttk.Label(sf, text=msg, font=("Helvetica", 12)).pack(pady=20)
        else:
            self.criar_lista_documentos(sf, documentos)

    def criar_lista_documentos(self, parent, documentos):
        frame_header = ttk.Frame(parent)
        frame_header.pack(fill=X, padx=10, pady=(0,5))
        
        ttk.Label(frame_header, text="Termo", font=("Helvetica", 10, "bold"), width=20).pack(side=LEFT)
        ttk.Label(frame_header, text="Data", font=("Helvetica", 10, "bold"), width=20).pack(side=LEFT)
        ttk.Label(frame_header, text="Processo", font=("Helvetica", 10, "bold"), width=25).pack(side=LEFT)
        ttk.Label(frame_header, text="Motivo", font=("Helvetica", 10, "bold")).pack(side=LEFT, fill=X, expand=True)
        ttk.Label(frame_header, text="Ações", font=("Helvetica", 10, "bold"), width=25).pack(side=RIGHT)
        ttk.Separator(parent).pack(fill=X, padx=10, pady=(0, 10))

        for doc in documentos:
            self.criar_linha_documento(parent, doc)

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
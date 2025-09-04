import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
import openpyxl

from pl_des_config import CriarPlanilha
from pl_des_edit import EdicaoPlanilha

class PlanilhaDesfazimento:
    def __init__(self, master, db_controller):
        self.janela = master
        self.db = db_controller
        self.tpl_planilha_des = None
        self.tela_de_criacao = CriarPlanilha(self.janela, self.db)
        self.carregar_recursos()
        
    def carregar_recursos(self):
        """Carrega a imagem do brasão."""
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
        except Exception:
            self.brasao = None

        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure('custom.TButton', font=("Inconsolata", 12), borderwidth=1, padding=(10, 10), background='white', foreground="#000000")
        style.map('custom.TButton', bordercolor=[('!active', '#adb5bd'), ('active', '#5bc0de')], background=[('active', "#ececec"), ('!active', 'white')], relief=[('pressed', 'solid'), ('!pressed', 'solid')])

    def planilha_des(self):
        """Cria e exibe a janela da Planilha de Desfazimento."""
        if self.tpl_planilha_des and self.tpl_planilha_des.winfo_exists():
            self.tpl_planilha_des.lift()
            return
        
        self.tpl_planilha_des = ttk.Toplevel(self.janela)
        self.tpl_planilha_des.title("Planilha de Desfazimento")
        self.tpl_planilha_des.geometry("800x600")
        self.tpl_planilha_des.position_center()
        self.tpl_planilha_des.transient(self.janela)
        self.tpl_planilha_des.grab_set()

        frm_cabecalho = ttk.Frame(self.tpl_planilha_des, style='Header.TFrame', padding=(10, 5))
        frm_cabecalho.pack(fill=X, side=TOP)

        if self.brasao:
            lbl_brasao = ttk.Label(frm_cabecalho, image=self.brasao)
            lbl_brasao.image = self.brasao 
            lbl_brasao.pack(side=LEFT, padx=10, pady=5)

        lbl_titulo = ttk.Label(frm_cabecalho, text="Planilha de Desfazimento", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black')
        lbl_titulo.pack(side=LEFT, expand=True, pady=5)

        frm_rodape = ttk.Frame(self.tpl_planilha_des, padding=10)
        frm_rodape.pack(fill=X, side=BOTTOM)

        btn_voltar = ttk.Button(frm_rodape, text="<- Voltar", command=self.tpl_planilha_des.destroy, bootstyle="primary-outline")
        btn_voltar.pack(side=LEFT, padx=40, pady=20)

        frm_corpo = ttk.Frame(self.tpl_planilha_des, padding=(50, 30))
        frm_corpo.pack(expand=True, fill=BOTH)

        lbl_pergunta = ttk.Label(frm_corpo, text="O que você quer fazer?", font=("Inconsolata", 14))
        lbl_pergunta.pack(anchor=W, pady=(0, 20))

        btn_criar = ttk.Button(frm_corpo, text="Criar Nova Planilha", style='custom.TButton', command=self.tela_de_criacao.criar)
        btn_criar.pack(fill=X, pady=5, ipady=10)

        btn_editar = ttk.Button(frm_corpo, text="Continuar Edição", style='custom.TButton', command=self.editar_planilha)
        btn_editar.pack(fill=X, pady=5, ipady=10)

    def editar_planilha(self):
        """
        Abre um seletor de ficheiros. Tenta ler o ID da aba oculta (método novo e robusto).
        Se não conseguir, tenta buscar pelo caminho do arquivo (método antigo, para compatibilidade).
        """
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione uma planilha para editar",
            filetypes=[("Planilhas Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )
        if not caminho_arquivo: return

        id_desfazimento_final = None
        dados_lidos = []
        
        try:
            workbook = openpyxl.load_workbook(caminho_arquivo)
            
            # --- TENTATIVA 1: MÉTODO NOVO (LER ID INTERNO) ---
            if "sap_ufac_meta" in workbook.sheetnames:
                id_sheet = workbook["sap_ufac_meta"]
                id_desfazimento_final = id_sheet['B1'].value

            # --- TENTATIVA 2: MÉTODO ANTIGO (COMPATIBILIDADE) ---
            # Se o ID não foi encontrado na aba, tenta o método antigo
            if id_desfazimento_final is None:
                print("DEBUG: Não encontrou ID interno, tentando compatibilidade por caminho de arquivo...")
                id_desfazimento_final = self.db.get_desfazimento_por_caminho_planilha(caminho_arquivo)

            # Se mesmo após as duas tentativas o ID não for encontrado, o arquivo é inválido.
            if id_desfazimento_final is None:
                messagebox.showerror("Processo não Encontrado", 
                                     "Não foi encontrado um processo de desfazimento associado a este ficheiro.\n\n"
                                     "Se for uma planilha antiga, seu registro pode não existir mais no banco com o caminho atual. "
                                     "Para novas planilhas, certifique-se de que foram salvas pelo sistema.")
                return

            # Continua a ler os dados da aba principal para exibir na tela
            sheet = workbook.active
            iterador_linhas = iter(sheet.rows)
            next(iterador_linhas) # Pula o cabeçalho
            for linha in iterador_linhas:
                dados_lidos.append([cell.value if cell.value is not None else "" for cell in linha])
        
        except Exception as e:
            messagebox.showerror(title="Erro de Leitura", message=f"Não foi possível ler o ficheiro Excel:\n{e}")
            return
            
        self.tpl_planilha_des.destroy()
        
        nome_planilha = os.path.basename(caminho_arquivo).replace('.xlsx', '')
        
        tela_edicao = EdicaoPlanilha(
            self.janela, 
            nome_planilha, 
            caminho_arquivo_aberto=caminho_arquivo, 
            dados_iniciais=dados_lidos,
            db_controller=self.db,
            id_desfazimento=id_desfazimento_final # Passa o ID encontrado (seja pelo método novo ou antigo)
        )
        tela_edicao.exibir_tela()
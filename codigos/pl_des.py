import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
# Importa a biblioteca para trabalhar com arquivos Excel
import openpyxl

# Importa as classes das telas seguintes
from pl_des_config import CriarPlanilha
from pl_des_edit import EdicaoPlanilha

class PlanilhaDesfazimento:
    def __init__(self, master):
        self.janela = master
        self.tpl_planilha_des = None # Mantém o controle da janela Toplevel
        self.carregar_recursos()
        
        # Instancia a tela de criação para ser chamada posteriormente
        self.tela_de_criacao = CriarPlanilha(self.janela)

    def carregar_recursos(self):
        """Carrega as imagens necessárias e define os estilos."""
        try:
            # Carrega o brasão da UFAC para o cabeçalho
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((40, 40))
            self.brasao = ImageTk.PhotoImage(brasao_img)
        except Exception as e:
            print(f"Erro ao carregar imagem do brasão: {e}")
            self.brasao = None

        # ----- Estilos Customizados -----
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure(
            'custom.TButton', 
            font=("Inconsolata", 14),
            borderwidth=1,
            padding=(10, 10),
            background='white',
            foreground="#000000"
        )
        style.map('custom.TButton',
            bordercolor=[('!active', '#adb5bd'), ('active', '#5bc0de')],
            background=[('active', "#ececec"), ('!active', 'white')],
            relief=[('pressed', 'solid'), ('!pressed', 'solid')],
        )

    def planilha_des(self):
        """Cria e exibe a janela da Planilha de Desfazimento."""
        if self.tpl_planilha_des and self.tpl_planilha_des.winfo_exists():
            self.tpl_planilha_des.lift()
            return

        # Evita criar múltiplas janelas se o botão for clicado várias vezes
        try:
            if self.tpl_planilha_des.winfo_exists():
                self.tpl_planilha_des.focus()
                return
        except AttributeError:
            pass
        
        self.tpl_planilha_des = ttk.Toplevel(self.janela)
        self.tpl_planilha_des.title("Planilha de Desfazimento")
        self.tpl_planilha_des.geometry("800x600")
        self.tpl_planilha_des.position_center()
        
        self.tpl_planilha_des.transient(self.janela)
        self.tpl_planilha_des.grab_set()

        # Cabeçalho, rodapé e corpo da janela...
        frm_cabecalho = ttk.Frame(self.tpl_planilha_des, style='Header.TFrame', padding=(10, 5))
        frm_cabecalho.pack(fill=X, side=TOP)

        if self.brasao:
            lbl_brasao = ttk.Label(frm_cabecalho, image=self.brasao, style='Header.TFrame')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))

        lbl_titulo = ttk.Label(
            frm_cabecalho, text="Planilha de Desfazimento",
            font=("Inconsolata", 18, "bold"), background='#5bc0de', foreground='black'
        )
        lbl_titulo.pack(side=LEFT, expand=True, pady=5)

        frm_rodape = ttk.Frame(self.tpl_planilha_des, padding=10)
        frm_rodape.pack(fill=X, side=BOTTOM)

        btn_voltar = ttk.Button(
            frm_rodape, text="<- Voltar",
            command=self.tpl_planilha_des.destroy, bootstyle="light-outline", style='custom.TButton'
        )
        btn_voltar.pack(side=LEFT)

        frm_corpo = ttk.Frame(self.tpl_planilha_des, padding=(50, 30))
        frm_corpo.pack(expand=True, fill=BOTH)

        lbl_pergunta = ttk.Label(
            frm_corpo, text="O que você quer fazer?",
            font=("Inconsolata", 15)
        )
        lbl_pergunta.pack(anchor=W, pady=(0, 20))

        # Botões de Ação
        btn_criar = ttk.Button(
            frm_corpo, text="Criar Nova Planilha",
            style='custom.TButton',
            command=self.tela_de_criacao.criar
        )
        btn_criar.pack(fill=X, pady=5, ipady=10)

        btn_editar = ttk.Button(
            frm_corpo, text="Continuar Edição",
            style='custom.TButton',
            command=self.editar_planilha # Comando chama a nova função
        )
        btn_editar.pack(fill=X, pady=5, ipady=10)

    def editar_planilha(self):
        """Abre um seletor de arquivos para carregar uma planilha XLSX."""
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione uma planilha para editar",
            filetypes=[("Planilhas Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )
        if not caminho_arquivo:
            return # Usuário cancelou

        dados_lidos = []
        try:
            # Carrega o arquivo Excel
            workbook = openpyxl.load_workbook(caminho_arquivo)
            sheet = workbook.active
            
            # Itera sobre as linhas da planilha, pulando o cabeçalho
            iterador_linhas = iter(sheet.rows)
            next(iterador_linhas)
            
            # Lê cada célula da linha e adiciona aos dados
            for linha in iterador_linhas:
                # Garante que valores nulos sejam lidos como strings vazias
                dados_lidos.append([cell.value if cell.value is not None else "" for cell in linha])

        except Exception as e:
            messagebox.show_error(title="Erro de Leitura", message=f"Não foi possível ler o arquivo Excel:\n{e}")
            return
            
        # Extrai o nome do arquivo para usar como título
        nome_planilha = os.path.basename(caminho_arquivo)
        
        # Fecha a janela atual e abre a de edição com os dados e o caminho do arquivo
        self.tpl_planilha_des.destroy()
        tela_edicao = EdicaoPlanilha(self.janela, nome_planilha, caminho_arquivo_aberto=caminho_arquivo, dados_iniciais=dados_lidos)
        tela_edicao.exibir_tela()

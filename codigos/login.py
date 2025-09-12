import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox
import hashlib

from tela_menu import MenuInicial

class TelaLogin:
    def __init__(self, master, db_controller):
        self.janela_login = master
        self.db = db_controller
        self.janela_login.title("SAP-UFAC - Acesso ao Sistema")
        self.janela_login.geometry("500x500")
        self.janela_login.position_center()
        self.janela_login.resizable(False, False)

        # Estilo
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')

        # Cabeçalho
        frm_cabecalho = ttk.Frame(self.janela_login, style='Header.TFrame', padding=10)
        frm_cabecalho.pack(fill=X)

        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
            lbl_brasao = ttk.Label(frm_cabecalho, image=self.brasao)
            lbl_brasao.pack(side=LEFT, padx=10)
        except Exception as e:
            print(f"Erro ao carregar brasão: {e}")

        lbl_titulo = ttk.Label(frm_cabecalho, text="Acesso ao Sistema", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black')
        lbl_titulo.pack(expand=True)

        # Corpo (onde ficam os campos de login)
        frm_corpo = ttk.Frame(self.janela_login, padding=40)
        frm_corpo.pack(expand=True, fill=BOTH)

        lbl_cpf = ttk.Label(frm_corpo, text="CPF", font=("Inconsolata", 12, "bold"))
        lbl_cpf.pack(fill=X, pady=(20, 5))
        self.ent_cpf = ttk.Entry(frm_corpo, font=("Inconsolata", 12))
        self.ent_cpf.pack(fill=X, ipady=5)

        lbl_senha = ttk.Label(frm_corpo, text="Senha", font=("Inconsolata", 12, "bold"))
        lbl_senha.pack(fill=X, pady=(20, 5))
        self.ent_senha = ttk.Entry(frm_corpo, font=("Inconsolata", 12), show="*")
        self.ent_senha.pack(fill=X, ipady=5)
        
        # Faz o login ao pressionar Enter na caixa de senha
        self.ent_senha.bind("<Return>", self.fazer_login)

        btn_login = ttk.Button(frm_corpo, text="Entrar", command=self.fazer_login, bootstyle="success")
        btn_login.pack(fill=X, ipady=8, pady=(40, 0))

    def fazer_login(self, event=None):
        cpf = self.ent_cpf.get().strip()
        senha = self.ent_senha.get().strip()

        if not cpf or not senha:
            Messagebox.show_warning("Campos Vazios", "Por favor, preencha o CPF e a senha.")
            return

        # Criptografa a senha digitada para comparar com a do banco
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        # O método verificar_usuario será criado no db_controller a seguir
        usuario = self.db.verificar_usuario(cpf, senha_hash)

        if usuario:
            print(f"Login bem-sucedido! Usuário: {usuario['nome_completo']}, Perfil: {usuario['perfil']}")
            
            # 1. Limpa todos os widgets (CPF, senha, botão, etc.) da janela de login
            for widget in self.janela_login.winfo_children():
                widget.destroy()
            
            # 2. Reutiliza a MESMA janela para carregar o menu principal
            from tela_menu import MenuInicial # Importa aqui para evitar dependência circular
            MenuInicial(self.janela_login, usuario)

        else:
            Messagebox.show_error("Falha no Login", "CPF ou senha inválidos.")
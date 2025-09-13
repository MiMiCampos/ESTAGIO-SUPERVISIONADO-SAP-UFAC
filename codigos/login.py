import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox
import hashlib

class TelaLogin:
    def __init__(self, master, db_controller):
        self.janela_login = master
        self.db = db_controller
        self.janela_login.title("SAP-UFAC - Acesso ao Sistema")
        self.janela_login.geometry("500x550")
        self.janela_login.position_center()
        self.janela_login.resizable(False, False)

        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')

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

        frm_corpo = ttk.Frame(self.janela_login, padding=40)
        frm_corpo.pack(expand=True, fill=BOTH)

        lbl_cpf = ttk.Label(frm_corpo, text="CPF", font=("Inconsolata", 12, "bold"))
        lbl_cpf.pack(fill=X, pady=(20, 5))
        self.ent_cpf = ttk.Entry(frm_corpo, font=("Inconsolata", 12))
        self.ent_cpf.pack(fill=X, ipady=5)
        self.ent_cpf.bind("<KeyRelease>", self._formatar_cpf)

        lbl_senha = ttk.Label(frm_corpo, text="Senha", font=("Inconsolata", 12, "bold"))
        lbl_senha.pack(fill=X, pady=(20, 5))
        self.ent_senha = ttk.Entry(frm_corpo, font=("Inconsolata", 12), show="*")
        self.ent_senha.pack(fill=X, ipady=5)
        self.ent_senha.bind("<Return>", self.fazer_login)

        btn_login = ttk.Button(frm_corpo, text="Entrar", command=self.fazer_login, bootstyle="success")
        btn_login.pack(fill=X, ipady=8, pady=(40, 0))

    def _formatar_cpf(self, event=None):
        texto_atual = self.ent_cpf.get()
        # Remove tudo que não for dígito
        numeros = "".join(filter(str.isdigit, texto_atual))
        
        # Limita a 11 dígitos
        numeros = numeros[:11]

        formatado = ""
        if len(numeros) > 9:
            formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
        elif len(numeros) > 6:
            formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
        elif len(numeros) > 3:
            formatado = f"{numeros[:3]}.{numeros[3:]}"
        else:
            formatado = numeros

        # Atualiza o campo de entrada sem disparar o evento novamente
        self.ent_cpf.delete(0, END)
        self.ent_cpf.insert(0, formatado)
        
        # Mantém o cursor no final do texto
        self.ent_cpf.icursor(END)

    def fazer_login(self, event=None):
        from tela_menu import MenuInicial # Importado aqui para evitar erro
        cpf = self.ent_cpf.get().strip()
        senha = self.ent_senha.get().strip()

        if not cpf or not senha:
            Messagebox.show_warning("Campos Vazios", "Por favor, preencha o CPF e a senha.")
            return

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        usuario = self.db.verificar_usuario(cpf, senha_hash)

        if usuario:
            # 1. Limpa a janela de login
            for widget in self.janela_login.winfo_children():
                widget.destroy()
            
            # 2. Reutiliza a mesma janela para o menu principal
            MenuInicial(self.janela_login, usuario)
        else:
            Messagebox.show_error("Falha no Login", "CPF ou senha inválidos.")
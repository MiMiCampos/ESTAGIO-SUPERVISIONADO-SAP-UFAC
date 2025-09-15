import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox
from utils.path_helper import resource_path

class Configuracoes():
    def __init__(self, master, db_controller):
        self.janela_mestra = master
        self.db = db_controller
        self.tpl_config = None
        
        self.tema_var = tk.StringVar()
        self.pasta_selecionada_var = tk.StringVar()
        self.formato_var = tk.StringVar()
        self.salvar_auto_var = tk.BooleanVar()
        self.lembrar_var = tk.BooleanVar()

    def _carregar_configuracoes(self):
        """Carrega as configurações do banco e atualiza os widgets."""
        configs = self.db.get_todas_configuracoes()
        
        self.tema_var.set(configs.get('tema', 'Claro'))
        self.pasta_selecionada_var.set(configs.get('pasta_padrao', 'Nenhuma pasta selecionada'))
        self.formato_var.set(configs.get('formato_padrao', '.pdf'))
        self.salvar_auto_var.set(configs.get('salvar_auto', '1') == '1')
        self.lembrar_var.set(configs.get('lembrar_configs', '1') == '1')
        
        style = ttk.Style()
        style.theme_use('litera' if self.tema_var.get() == 'Claro' else 'darkly')

    def _salvar_configuracoes(self):
        """Pega os valores dos widgets, salva no banco e aplica o tema em tempo real."""
        try:
            self.db.set_configuracao('tema', self.tema_var.get())
            self.db.set_configuracao('pasta_padrao', self.pasta_selecionada_var.get())
            self.db.set_configuracao('formato_padrao', self.formato_var.get())
            self.db.set_configuracao('salvar_auto', '1' if self.salvar_auto_var.get() else '0')
            self.db.set_configuracao('lembrar_configs', '1' if self.lembrar_var.get() else '0')
            
            # --- LÓGICA CORRIGIDA E MAIS ROBUSTA ---
            tema_selecionado = self.tema_var.get()
            nome_tema_ttk = 'litera' if tema_selecionado == 'Claro' else 'darkly'
            
            # Pega a instância de estilo GLOBAL da aplicação e aplica o tema.
            # Isso afeta todas as janelas e é mais seguro.
            style = ttk.Style()
            style.theme_use(nome_tema_ttk)

            Messagebox.ok("Sucesso", "Configurações salvas com sucesso!", parent=self.tpl_config)
            self.tpl_config.destroy()
        except Exception as e:
            Messagebox.show_error("Erro", f"Ocorreu um erro ao salvar as configurações:\n{e}", parent=self.tpl_config)

    def selecionar_pasta(self):
        caminho_pasta = filedialog.askdirectory(title="Selecione a pasta padrão")
        if caminho_pasta:
            self.pasta_selecionada_var.set(caminho_pasta)

    def configuracao(self):
        if self.tpl_config and self.tpl_config.winfo_exists():
            self.tpl_config.focus()
            return

        self.tpl_config = ttk.Toplevel(self.janela_mestra)
        self.tpl_config.title("Configurações")
        self.tpl_config.geometry("800x600")
        self.tpl_config.position_center()
        self.tpl_config.transient(self.janela_mestra)

        self._carregar_configuracoes()

        style = ttk.Style()
        style.configure('MyHeader.TFrame', background='#5bc0de')
        
        cabecalho_frame = ttk.Frame(self.tpl_config, style='MyHeader.TFrame', padding=10)
        cabecalho_frame.pack(fill=X)
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
            ttk.Label(cabecalho_frame, image=self.brasao, style='MyHeader.TFrame').pack(side=LEFT, padx=10)
        except: pass
        ttk.Label(cabecalho_frame, text="Configurações do Sistema", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black').pack(expand=True)
        
        frame_principal = ttk.Frame(self.tpl_config, padding=30)
        frame_principal.pack(fill=BOTH, expand=True)
        frame_config = ttk.Labelframe(frame_principal, text="Opções", padding=20)
        frame_config.pack(fill=BOTH, expand=True)
        frame_config.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame_config, text="Tema", font=("Inclusive Sans", 12)).grid(row=1, column=0, sticky='w', pady=10)
        combo_tema = ttk.Combobox(frame_config, values=['Claro', 'Escuro'], state="readonly", textvariable=self.tema_var)
        combo_tema.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(frame_config, text="Pasta padrão para salvar planilhas e documentos", font=("Inclusive Sans", 12)).grid(row=2, column=0, sticky='w', pady=10)
        btn_pasta = ttk.Button(frame_config, text="Selecionar pasta", command=self.selecionar_pasta, bootstyle="secondary-outline")
        btn_pasta.grid(row=2, column=1, sticky='ew', padx=5)
        ttk.Label(frame_config, textvariable=self.pasta_selecionada_var, font=("Inclusive Sans", 9), bootstyle="secondary").grid(row=3, column=0, columnspan=2, sticky='w')

        ttk.Label(frame_config, text="Formato padrão de documentos", font=("Inclusive Sans", 12)).grid(row=4, column=0, sticky='w', pady=10)
        combo_formato = ttk.Combobox(frame_config, values=['.pdf', '.docx'], state="readonly", textvariable=self.formato_var)
        combo_formato.grid(row=4, column=1, sticky='ew', padx=5)

        ttk.Label(frame_config, text="Salvar automaticamente após adicionar tombos", font=("Inclusive Sans", 12)).grid(row=5, column=0, sticky='w', pady=10)
        check_salvar_auto = ttk.Checkbutton(frame_config, bootstyle="round-toggle", variable=self.salvar_auto_var)
        check_salvar_auto.grid(row=5, column=1, sticky='e', padx=5)

        ttk.Label(frame_config, text="Lembrar configurações anteriores", font=("Inclusive Sans", 12)).grid(row=6, column=0, sticky='w', pady=10)
        check_lembrar = ttk.Checkbutton(frame_config, bootstyle="round-toggle", variable=self.lembrar_var)
        check_lembrar.grid(row=6, column=1, sticky='e', padx=5)

        frame_rodape = ttk.Frame(frame_principal, padding=(0, 20))
        frame_rodape.pack(fill=X, side=BOTTOM)
        ttk.Button(frame_rodape, text="<- Voltar", command=self.tpl_config.destroy, bootstyle="primary-outline").pack(side=LEFT)
        ttk.Button(frame_rodape, text="Salvar Configurações", command=self._salvar_configuracoes, bootstyle="success").pack(side=RIGHT)
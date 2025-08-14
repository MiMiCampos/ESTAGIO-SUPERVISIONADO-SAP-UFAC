import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class Configuracoes():
    def __init__(self, master):
        self.janela = master
    
    def configuracao(self):
        # Evita criar múltiplas janelas se o botão for clicado várias vezes
        try:
            if self.tpl_config.winfo_exists():
                self.tpl_config.focus()
                return
        except AttributeError:
            pass

        self.tpl_config = ttk.Toplevel(self.janela)
        self.tpl_config.title("Configurações")
        self.tpl_config.geometry("800x600")
        self.tpl_config.position_center()
        
        # ----- Instância do Style UMA VEZ no início -----
        style = ttk.Style()
        
        # ----- Estilo de cor customizada para o cabeçalho -----
        style.configure('MyHeader.TFrame', background='#5bc0de')
        
        # ----- Estilo customizado para as fontes dos botões -----
        style.configure(
            "Fonte.light.TButton", # Nome do estilo customizado, com o 'light', para continuar meio cinza
            font=("Inclusive Sans", 12))
        
        # ===== Estilo customizado para as fontes dos combobox =====
        # 1. Para a LISTA SUSPENSA (o menu que abre)
        self.janela.option_add('*TCombobox*Listbox.font', ('Inclusive Sans', 12))
        
        # 2. Para o CAMPO DE TEXTO (o que fica visível)
        style.configure(
            'TCombobox', # Aplicado diretamente ao tipo base
            font=('Inclusive Sans', 12))

        # ----- Cabeçalho azul claro -----
        self.cabecalho_frame = ttk.Frame(self.tpl_config)
        self.cabecalho_frame.pack(fill=X)
        self.cabecalho_frame.configure(style='MyHeader.TFrame')
    
        # ----- Inserindo o brasão da UFAC -----
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
            brasao_label = ttk.Label(self.cabecalho_frame, image=self.brasao)
            brasao_label.pack(side=LEFT, padx=10, pady=5)
        except:
            brasao_label = ttk.Label(self.cabecalho_frame, text="[BRASÃO]")
            brasao_label.pack(side=LEFT, padx=10, pady=5)
            
        # ----- Título da tela -----
        titulo = ttk.Label(
            self.cabecalho_frame,
            text="Configurações do Sistema",
            font=("Inconsolata", 15, "bold"),
            bootstyle=INVERSE,
            foreground='black',
            background='#5bc0de'
        )
        titulo.pack(expand=True, padx=10, pady=10)
        
        # ===== INÍCIO DA INTEGRAÇÃO DO CONTEÚDO DA TELA =====
        
        # ----- Frame principal para o conteúdo abaixo do cabeçalho -----
        frame_principal = ttk.Frame(self.tpl_config)
        frame_principal.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # ----- Labelframe para agrupar as opções com uma borda -----
        frame_config = ttk.Labelframe(frame_principal, text="", padding=20)
        frame_config.pack(fill=BOTH, expand=True)

        # Configurando o layout em grid para alinhar os itens
        frame_config.grid_columnconfigure(0, weight=1)  # Coluna dos textos (expande)
        frame_config.grid_columnconfigure(1, weight=0)  # Coluna dos botões (não expande)

        # ----- Opção 1: Importar documentos -----
        self.lbl_importar = ttk.Label(frame_config, 
            text="Importar documentos de tombos", 
            font=("Inclusive Sans", 12))
        self.lbl_importar.grid(row=0, column=0, sticky='w', pady=10)
        
        self.btn_importar = ttk.Button(frame_config,
            text="Importar",
            style="Fonte.light.TButton")
        self.btn_importar.grid(row=0, column=1, sticky='ew', padx=5)

        # ----- Opção 2: Tema -----
        self.lbl_tema = ttk.Label(frame_config, 
            text="Tema", 
            font=("Inclusive Sans", 12))
        self.lbl_tema.grid(row=1, column=0, sticky='w', pady=10)
        
        self.combo_tema = ttk.Combobox(frame_config, 
            values=['Claro', 'Escuro'], 
            state="readonly")
        self.combo_tema.set("Claro")
        self.combo_tema.grid(row=1, column=1, sticky='ew', padx=5)

        # ----- Opção 3: Pasta Padrão -----
        self.lbl_pasta = ttk.Label(frame_config, 
            text="Pasta padrão para salvar planilhas e documentos", font=("Inclusive Sans", 12))
        self.lbl_pasta.grid(row=2, column=0, sticky='w', pady=10)
        
        self.btn_pasta = ttk.Button(frame_config, 
            text="Selecionar pasta", 
            style="Fonte.light.TButton")
        self.btn_pasta.grid(row=2, column=1, sticky='ew', padx=5)

        # ----- Opção 4: Formato Padrão -----
        self.lbl_formato = ttk.Label(frame_config, 
            text="Formato padrão de documentos", 
            font=("Inclusive Sans", 12))
        self.lbl_formato.grid(row=3, column=0, sticky='w', pady=10)
        
        self.combo_formato = ttk.Combobox(frame_config, 
            values=['.pdf', '.docx', '.xlsx'], 
            state="readonly")
        self.combo_formato.set(".pdf")
        self.combo_formato.grid(row=3, column=1, sticky='ew', padx=5)

        # ----- Opção 5: Salvar Automaticamente (Switch) -----
        self.lbl_salvar_auto = ttk.Label(frame_config, 
            text="Salvar automaticamente após adicionar tombos", 
            font=("Inclusive Sans", 12))
        self.lbl_salvar_auto.grid(row=4, column=0, sticky='w', pady=10)
        
        self.check_salvar_auto = ttk.Checkbutton(frame_config,
            bootstyle="round-toggle")
        self.check_salvar_auto.invoke()
        self.check_salvar_auto.grid(row=4, column=1, sticky='e', padx=5, pady=10)

        # ----- Opção 6: Lembrar Configurações (Switch) -----
        self.lbl_lembrar = ttk.Label(frame_config, 
            text="Lembrar configurações anteriores", 
            font=("Inclusive Sans", 12))
        self.lbl_lembrar.grid(row=5, column=0, sticky='w', pady=10)
        
        self.check_lembrar = ttk.Checkbutton(frame_config, 
            bootstyle="round-toggle")
        self.check_lembrar.invoke()
        self.check_lembrar.grid(row=5, column=1, sticky='e', padx=5, pady=10)

        # ----- Botão de Voltar -----
        btn_voltar = ttk.Button(
            frame_principal,
            text="<- Voltar",
            bootstyle="primary-outline",
            command=self.tpl_config.destroy
        )
        btn_voltar.pack(side=LEFT, pady=(20, 0))

# ----- Bloco para Teste da Janela (PADRONIZADO) -----
if __name__ == "__main__":
    
    class AppTeste:
        def __init__(self, master):
            self.janela = master
            self.janela.title("App de Teste para Configurações")
            self.janela.geometry("400x200")
            
            self.tela_config = Configuracoes(self.janela)

            btn_abrir = ttk.Button(
                self.janela,
                text="Abrir Tela de Configurações",
                command=self.tela_config.configuracao,
                bootstyle="primary"
            )
            btn_abrir.pack(expand=True)

    janela_teste = ttk.Window(themename="litera")
    app = AppTeste(janela_teste)
    janela_teste.mainloop()
import ttkbootstrap as ttk
from banco_dados.db_controller import DBController
from login import TelaLogin
from tela_menu import MenuInicial

class AplicacaoPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("SAP-UFAC")
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        # self.root.withdraw()
        self.root.state('zoomed')
        
        self.db_conn = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
        
        if not self.db_conn.conn:
            self.root.destroy()
            return
            
        self._carregar_configuracoes_e_iniciar()

    def _carregar_configuracoes_e_iniciar(self):
        configs = self.db_conn.get_todas_configuracoes()
        tema_salvo = configs.get('tema', 'Claro')
        nome_tema_ttk = 'litera' if tema_salvo == 'Claro' else 'darkly'
        self.root.style.theme_use(nome_tema_ttk)
        self.mostrar_tela_login()
        
    def mostrar_tela_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Garante que a janela principal fique escondida
        self.root.withdraw()
        
        self.login_window = ttk.Toplevel(self.root)
        
        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()
        self.login_window.geometry(f"{screen_width}x{screen_height}+0+0")
        
        app_login = TelaLogin(self.login_window, self.db_conn, self.login_bem_sucedido)
    
    def login_bem_sucedido(self, dados_usuario):
        if self.login_window:
            self.login_window.destroy()

        self.root.deiconify()
        self.mostrar_tela_menu(dados_usuario)

    def mostrar_tela_menu(self, dados_usuario):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Passa a função de logout como um "aviso" para a TelaMenu
        self.menu = MenuInicial(self.root, self.db_conn, dados_usuario, self.fazer_logout)

    def fazer_logout(self):
        # O "chefe" (main.py) agora é responsável pelo logout
        print("INFO: Realizando logout e voltando para a tela de login.")
        self.mostrar_tela_login()
        
    def fechar_app(self):
        if self.db:
            self.db.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    # "Ancora" a instância da aplicação na janela principal para evitar o erro de imagem
    root.app = AplicacaoPrincipal(root)
    root.mainloop()
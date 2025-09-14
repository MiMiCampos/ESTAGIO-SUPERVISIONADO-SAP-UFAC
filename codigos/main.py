import ttkbootstrap as ttk
from banco_dados.db_controller import DBController
from login import TelaLogin
from tela_menu import MenuInicial

class AplicacaoPrincipal:
    def __init__(self, root):
        self.root = root
        self.db_conn = DBController(host="localhost", user="root", password="root", database="sap_ufac_db")
        
        # Garante que a conexão com o BD seja fechada ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self._fechar_aplicacao)

        if self.db_conn.conn:
            self._carregar_configuracoes_e_iniciar()
        else:
            # Se não conectar ao banco, exibe um erro e fecha.
            root.withdraw() # Esconde a janela principal antes de fechar
            ttk.dialogs.Messagebox.show_error("Erro Crítico", "Não foi possível conectar ao banco de dados. A aplicação será encerrada.")
            root.destroy()

    def _carregar_configuracoes_e_iniciar(self):
        """Carrega o tema salvo e mostra a tela de login."""
        configs = self.db_conn.get_todas_configuracoes()
        tema_salvo = configs.get('tema', 'Claro')
        themename = 'litera' if tema_salvo == 'Claro' else 'darkly'
        
        # Aplica o tema na janela principal
        style = ttk.Style(themename)
        self.root = style.master

        self.mostrar_tela_login()

    def _limpar_tela(self):
        """Remove todos os widgets da janela principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_tela_login(self):
        """Limpa a janela e exibe a tela de login."""
        self._limpar_tela()
        # Passa um método de "callback" para a tela de login saber o que fazer quando o login for bem-sucedido
        self.login_view = TelaLogin(self.root, self.db_conn, self.mostrar_tela_menu)

    def mostrar_tela_menu(self, dados_usuario):
        """Limpa a janela e exibe a tela de menu principal."""
        self._limpar_tela()
        self.menu_view = MenuInicial(self.root, self.db_conn, dados_usuario, self.mostrar_tela_login)

    def _fechar_aplicacao(self):
        """Fecha a conexão com o BD e encerra a aplicação."""
        if self.db_conn:
            self.db_conn.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = ttk.Window()
    app = AplicacaoPrincipal(root)
    root.mainloop()
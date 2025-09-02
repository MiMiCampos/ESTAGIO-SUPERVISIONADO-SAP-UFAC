import mysql.connector
from mysql.connector import errorcode
from ttkbootstrap.dialogs import Messagebox

class DBController:
    def __init__(self, host, user, password, database):
        """Tenta conectar ao banco de dados MySQL ao ser instanciado."""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            # dictionary = True faz com que os resultados venham como dicionários, o que é ótimo para a UI
            self.cursor = self.conn.cursor(dictionary=True) 
            print("Conexão com o banco de dados bem-sucedida!")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                Messagebox.show_error("Erro de Conexão", "Acesso negado. Verifique seu usuário e senha.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                Messagebox.show_error("Erro de Conexão", f"O banco de dados '{database}' não existe.")
            else:
                Messagebox.show_error("Erro de Conexão", f"Ocorreu um erro: {err}")
            self.conn = None
            self.cursor = None

    def get_bem_by_tombo(self, tombo):
        """Busca os detalhes de um bem pelo seu número de tombo."""
        if not self.conn:
            return None
        try:
            #JOIN usado para buscar os nomes da Unidade e do Servidor, não apenas os IDs
            query = """
                SELECT 
                    b.tombo, b.descricao, b.data_aquisicao, b.nota_fiscal,
                    u.nome_unidade, s.nome_servidor
                FROM Bem b
                LEFT JOIN Unidade u ON b.id_unidade = u.id_unidade
                LEFT JOIN Servidor s ON b.id_servidor = s.id_servidor
                WHERE b.tombo = %s
            """
            self.cursor.execute(query, (tombo,))
            return self.cursor.fetchone() # Retorna um único resultado como um dicionário
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar bem: {err}")
            return None

    def get_planilhas_finalizadas(self):
        """Busca todas as planilhas finalizadas para listar na tela 'Gerar Documentos'."""
        if not self.conn:
            return []
        try:
            query = "SELECT id_planilha, nome_planilha, data_geracao, total_tombos FROM PlanilhaFinalizada ORDER BY data_geracao DESC"
            self.cursor.execute(query)
            return self.cursor.fetchall() # Retorna uma lista de dicionários
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar planilhas: {err}")
            return []
            
    def salvar_planilha(self, nome_planilha, caminho, total_tombos, id_desfazimento):
        """Insere uma nova planilha finalizada no banco de dados."""
        if not self.conn:
            return None
        try:
            query = """
                INSERT INTO PlanilhaFinalizada 
                (nome_planilha, caminho_arquivo_planilha, data_geracao, total_tombos, id_desfazimento) 
                VALUES (%s, %s, NOW(), %s, %s)
            """
            self.cursor.execute(query, (nome_planilha, caminho, total_tombos, id_desfazimento))
            self.conn.commit() # Confirma a transação
            return self.cursor.lastrowid # Retorna o ID da planilha recém-criada
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro ao Salvar", f"Erro ao salvar planilha: {err}")
            self.conn.rollback() # Desfaz a transação em caso de erro
            return None

    # Adicione aqui outros métodos que você precisar (ex: para criar um desfazimento, atualizar um bem, etc.)

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexão com o banco de dados fechada.")
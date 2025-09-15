import mysql.connector
from mysql.connector import errorcode
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime, date

class DBController:
    # ... (todo o resto do seu código __init__, get_bem_by_tombo, etc., permanece igual) ...
    def __init__(self, host, user, password, database):
        """Tenta conectar ao banco de dados MySQL ao ser instanciado."""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
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
        """Busca os detalhes de um bem, incluindo seu status de desfazimento."""
        if not self.conn: return None
        try:
            query = """
                SELECT 
                    b.tombo, b.descricao, b.data_aquisicao, b.nota_fiscal,
                    b.id_desfazimento,
                    u.nome_unidade, s.nome_servidor
                FROM Bem b
                LEFT JOIN Unidade u ON b.id_unidade = u.id_unidade
                LEFT JOIN Servidor s ON b.id_servidor = s.id_servidor
                WHERE b.tombo = %s
            """
            self.cursor.execute(query, (tombo,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar bem: {err}")
            return None
            
    def associar_bem_a_desfazimento(self, tombo, id_desfazimento):
        """Atualiza um bem para associá-lo a um processo de desfazimento."""
        if not self.conn: return False
        try:
            query = """
                UPDATE Bem SET id_desfazimento = %s, classificacao = 'Irrecuperável', destinacao = 'Alienação/Leilão'
                WHERE tombo = %s
            """
            self.cursor.execute(query, (id_desfazimento, tombo))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Atualização", f"Não foi possível associar o bem:\n{err}")
            self.conn.rollback()
            return False

    def criar_novo_desfazimento(self, numero_processo, data_desfazimento):
        """Cria um novo registro de desfazimento e retorna seu ID."""
        if not self.conn: return None
        try:
            query = "INSERT INTO Desfazimento (numero_processo, data_desfazimento) VALUES (%s, %s)"
            self.cursor.execute(query, (numero_processo, data_desfazimento))
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                Messagebox.show_error("Processo Duplicado", f"O número de processo '{numero_processo}' já existe.")
            else:
                Messagebox.show_error("Erro no Banco de Dados", f"Não foi possível criar o processo de desfazimento:\n{err}")
            self.conn.rollback()
            return None

    def get_planilhas_finalizadas(self):
        """Busca todas as planilhas finalizadas, incluindo o número do processo associado."""
        if not self.conn: return []
        try:
            query = """
                SELECT 
                    pf.id_planilha, 
                    pf.nome_planilha, 
                    pf.data_geracao, 
                    pf.total_tombos, 
                    pf.id_desfazimento,
                    d.numero_processo
                FROM PlanilhaFinalizada pf
                JOIN Desfazimento d ON pf.id_desfazimento = d.id_desfazimento
                ORDER BY pf.data_geracao DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar planilhas: {err}")
            return []

    def get_bens_por_desfazimento(self, id_desfazimento):
        """Busca todos os bens associados a um id_desfazimento específico."""
        if not self.conn: return []
        try:
            # QUERY FINAL - Usa os nomes de coluna confirmados do seu BD
            query = """
                SELECT 
                    NULL as 'Nº DE ORDEM',
                    b.tombo AS 'TOMBO',
                    b.descricao AS 'DESCRIÇÃO DO BEM',
                    b.data_aquisicao AS 'DATA DA AQUISIÇÃO',
                    b.nota_fiscal AS 'DOCUMENTO FISCAL',
                    u.nome_unidade AS 'UNIDADE RESPONSÁVEL',
                    s.nome_servidor AS 'SERVIDOR RESPONSÁVEL',
                    b.classificacao AS 'CLASSIFICAÇÃO',
                    b.destinacao AS 'DESTINAÇÃO',
                    b.valor_aquisicao AS 'VALOR',
                    b.forma_ingresso AS 'FORMA_DE_INGRESSO'
                FROM Bem b
                LEFT JOIN Unidade u ON b.id_unidade = u.id_unidade
                LEFT JOIN Servidor s ON b.id_servidor = s.id_servidor
                WHERE b.id_desfazimento = %s
            """
            self.cursor.execute(query, (id_desfazimento,))
            resultados = self.cursor.fetchall()
            dados_formatados = []
            for i, row in enumerate(resultados):
                linha = list(row.values())
                linha[0] = i + 1
                # Formata a data se ela existir
                if isinstance(linha[3], date):
                    linha[3] = linha[3].strftime('%d/%m/%Y')
                # Formata o valor para o padrão monetário brasileiro
                if isinstance(linha[9], (float, int, str)):
                    try:
                        valor_numerico = float(linha[9])
                        linha[9] = f"{valor_numerico:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    except (ValueError, TypeError):
                        linha[9] = '0,00'
                dados_formatados.append(linha)
            return dados_formatados
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar bens da planilha:\n{err}")
            return []

    def get_bens_para_visualizacao(self, id_desfazimento):
        """Busca os bens para a tela de visualização (sem o nome do servidor)."""
        if not self.conn: return []
        try:
            query = """
                SELECT 
                    NULL as 'Nº DE ORDEM',
                    b.tombo AS 'TOMBO',
                    b.descricao AS 'DESCRIÇÃO DO BEM',
                    b.data_aquisicao AS 'DATA DA AQUISIÇÃO',
                    b.nota_fiscal AS 'DOCUMENTO FISCAL',
                    u.nome_unidade AS 'UNIDADE RESPONSÁVEL',
                    b.classificacao AS 'CLASSIFICAÇÃO',
                    b.destinacao AS 'DESTINAÇÃO'
                FROM Bem b
                LEFT JOIN Unidade u ON b.id_unidade = u.id_unidade
                WHERE b.id_desfazimento = %s
            """
            self.cursor.execute(query, (id_desfazimento,))
            resultados = self.cursor.fetchall()
            dados_formatados = []
            for i, row in enumerate(resultados):
                linha = list(row.values())
                linha[0] = i + 1
                if isinstance(linha[3], date):
                    linha[3] = linha[3].strftime('%d/%m/%Y')
                dados_formatados.append(linha)
            return dados_formatados
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar bens da planilha:\n{err}")
            return []

    def get_desfazimento_por_caminho_planilha(self, caminho_arquivo):
        """Busca o id_desfazimento a partir do caminho do arquivo salvo."""
        if not self.conn: return None
        try:
            query = "SELECT id_desfazimento FROM PlanilhaFinalizada WHERE caminho_arquivo_planilha = %s"
            self.cursor.execute(query, (caminho_arquivo,))
            resultado = self.cursor.fetchone()
            return resultado['id_desfazimento'] if resultado else None
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar desfazimento pela planilha: {err}")
            return None

    def salvar_ou_atualizar_planilha_finalizada(self, id_desfazimento, nome_planilha, caminho, total_tombos):
        """Cria ou atualiza o registro de uma planilha finalizada."""
        if not self.conn: return None
        try:
            query = """
                INSERT INTO PlanilhaFinalizada (id_desfazimento, nome_planilha, caminho_arquivo_planilha, data_geracao, total_tombos)
                VALUES (%s, %s, %s, NOW(), %s)
                ON DUPLICATE KEY UPDATE
                nome_planilha = VALUES(nome_planilha),
                caminho_arquivo_planilha = VALUES(caminho_arquivo_planilha),
                data_geracao = VALUES(data_geracao),
                total_tombos = VALUES(total_tombos)
            """
            self.cursor.execute(query, (id_desfazimento, nome_planilha, caminho, total_tombos))
            self.conn.commit()
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro ao Salvar", f"Erro ao salvar registro da planilha: {err}")
            self.conn.rollback()
            
    def get_ultima_planilha_criada(self):
        """Busca a planilha mais recente registrada no banco de dados."""
        if not self.conn: return None
        try:
            query = """
                SELECT id_desfazimento, nome_planilha, caminho_arquivo_planilha 
                FROM PlanilhaFinalizada 
                ORDER BY id_planilha DESC 
                LIMIT 1
            """
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            
            if resultado:
                return {
                    'id_desfazimento': resultado['id_desfazimento'],
                    'nome': resultado['nome_planilha'],
                    'caminho': resultado['caminho_arquivo_planilha']
                }
            return None
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar a última planilha: {err}")
            return None

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexão com o banco de dados fechada.")
            
    def verificar_usuario(self, cpf, senha_hash):
        """Verifica se um usuário com o CPF e hash de senha fornecidos existe."""
        if not self.conn: return None
        try:
            query = "SELECT id_usuario, nome_completo, perfil FROM Usuario WHERE cpf = %s AND senha_hash = %s"
            self.cursor.execute(query, (cpf, senha_hash))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Autenticação", f"Erro ao verificar usuário: {err}")
            return None
        
    def listar_usuarios(self):
        """Busca todos os usuários cadastrados."""
        if not self.conn: return []
        try:
            query = "SELECT id_usuario, nome_completo, cpf, perfil FROM Usuario"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao listar usuários: {err}")
            return []

    def cpf_existe(self, cpf, id_usuario_excluir=None):
        """Verifica se um CPF já existe no banco, opcionalmente ignorando um usuário."""
        if not self.conn: return False
        try:
            query = "SELECT id_usuario FROM Usuario WHERE cpf = %s"
            params = [cpf]
            if id_usuario_excluir:
                query += " AND id_usuario != %s"
                params.append(id_usuario_excluir)
            
            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Verificação", f"Erro ao verificar CPF: {err}")
            return True

    def cadastrar_usuario(self, nome, cpf, senha_hash, perfil):
        """Insere um novo usuário no banco de dados."""
        if not self.conn: return False
        try:
            query = "INSERT INTO Usuario (nome_completo, cpf, senha_hash, perfil) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (nome, cpf, senha_hash, perfil))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Cadastro", f"Não foi possível cadastrar o usuário:\n{err}")
            self.conn.rollback()
            return False

    def atualizar_usuario(self, id_usuario, nome, cpf, perfil):
        """Atualiza os dados de um usuário existente (não mexe na senha)."""
        if not self.conn: return False
        try:
            query = "UPDATE Usuario SET nome_completo = %s, cpf = %s, perfil = %s WHERE id_usuario = %s"
            self.cursor.execute(query, (nome, cpf, perfil, id_usuario))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Atualização", f"Não foi possível atualizar o usuário:\n{err}")
            self.conn.rollback()
            return False

    def deletar_usuario(self, id_usuario):
        """Remove um usuário do banco de dados."""
        if not self.conn: 
            return False
        try:
            query = "DELETE FROM Usuario WHERE id_usuario = %s"
            self.cursor.execute(query, (id_usuario,))
            if self.cursor.rowcount == 0:
                self.conn.rollback()
                Messagebox.show_warning("Aviso", "Nenhum usuário foi encontrado com o ID fornecido.")
                return False
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro ao Deletar", f"Não foi possível deletar o usuário:\n{err}")
            self.conn.rollback()
            return False
        
    def get_todos_servidores(self):
        """Busca o nome de todos os servidores cadastrados na tabela Servidor."""
        if not self.conn: return []
        try:
            query = "SELECT nome_servidor FROM Servidor ORDER BY nome_servidor ASC"
            self.cursor.execute(query)
            return [servidor['nome_servidor'] for servidor in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao listar servidores: {err}")
            return []

    # >>> NOVA FUNÇÃO ADICIONADA AQUI <<<
    def get_proximo_numero_termo(self):
        """Busca o próximo ID da tabela de documentos para gerar um número de termo sequencial."""
        if not self.conn: return "000000"
        try:
            # Esta query busca o próximo valor do AUTO_INCREMENT da tabela
            db_name = self.conn.database
            query = f"""
                SELECT AUTO_INCREMENT 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = '{db_name}' 
                AND TABLE_NAME = 'DocumentoDeBaixa'
            """
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            
            # Formata o número com 6 dígitos (ex: 1 -> "000001")
            proximo_id = resultado.get('AUTO_INCREMENT', 1) if resultado else 1
            return f"{proximo_id:06d}"
            
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar próximo número do termo: {err}")
            return "000000"
        
    # Adicione esta função dentro da classe DBController em db_controller.py

    def get_todas_configuracoes(self):
        """Busca todas as configurações da tabela Configuracao e retorna um dicionário."""
        if not self.conn:
            return {}  # Retorna um dicionário vazio se não houver conexão
        
        configs = {}
        try:
            query = "SELECT chave, valor FROM Configuracao"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            
            # Transforma a lista de resultados em um dicionário único (ex: {'tema': 'Claro'})
            for item in resultados:
                configs[item['chave']] = item['valor']
            
            return configs
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar configurações: {err}")
            return {}
        
    # Em db_controller.py, adicione esta função

    def get_processo_por_id_desfazimento(self, id_desfazimento):
        """Busca o número do processo usando o ID de desfazimento."""
        if not self.conn or not id_desfazimento:
            return None
        try:
            query = "SELECT numero_processo FROM Desfazimento WHERE id_desfazimento = %s"
            self.cursor.execute(query, (id_desfazimento,))
            resultado = self.cursor.fetchone()
            return resultado['numero_processo'] if resultado else None
        except mysql.connector.Error as err:
            Messagebox.show_error("Erro de Consulta", f"Erro ao buscar número do processo: {err}")
            return None
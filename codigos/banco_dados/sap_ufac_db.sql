-- EXCLUI O BANCO PERMANENTEMENTE:
DROP DATABASE IF EXISTS sap_ufac_db;

CREATE DATABASE sap_ufac_db;

USE sap_ufac_db;

-- TABELA DE UNIDADES:
CREATE TABLE Unidade (
    id_unidade INT PRIMARY KEY AUTO_INCREMENT,
    nome_unidade VARCHAR(255) NOT NULL UNIQUE,
    setor VARCHAR(255)
);

-- O comando TRUNCATE TABLE limpa a tabela antes de inserir os novos dados.
-- Evita duplicatas se o script for executado mais de uma vez.
TRUNCATE TABLE Unidade;

-- INSERÇÃO DAS UNIDADES:
INSERT INTO Unidade (nome_unidade, setor) VALUES
-- Centros Acadêmicos
('Centro de Ciências Exatas e Tecnológicas (CCET)', 'Acadêmico'),
('Centro de Ciências Biológicas e da Natureza (CCBN)', 'Acadêmico'),
('Centro de Ciências da Saúde e do Desporto (CCSD)', 'Acadêmico'),
('Centro de Educação, Letras e Artes (CELA)', 'Acadêmico'),
('Centro de Filosofia e Ciências Humanas (CFCH)', 'Acadêmico'),
('Centro de Ciências Jurídicas e Sociais Aplicadas (CCJSA)', 'Acadêmico'),

-- Coordenadorias de Cursos de Graduação (Exemplos)
('Coordenação do Curso de Sistemas de Informação', 'Coordenação de Curso'),
('Coordenação do Curso de Ciência da Computação', 'Coordenação de Curso'),
('Coordenação do Curso de Engenharia Civil', 'Coordenação de Curso'),
('Coordenação do Curso de Engenharia Elétrica', 'Coordenação de Curso'),
('Coordenação do Curso de Engenharia Florestal', 'Coordenação de Curso'),
('Coordenação do Curso de Medicina', 'Coordenação de Curso'),
('Coordenação do Curso de Direito', 'Coordenação de Curso'),
('Coordenação do Curso de Enfermagem', 'Coordenação de Curso'),
('Coordenação do Curso de Ciências Econômicas', 'Coordenação de Curso'),
('Coordenação do Curso de Pedagogia', 'Coordenação de Curso'),
('Coordenação do Curso de História', 'Coordenação de Curso'),
('Coordenação do Curso de Letras: Português', 'Coordenação de Curso'),
('Coordenação do Curso de Educação Física', 'Coordenação de Curso'),
('Coordenação do Curso de Psicologia', 'Coordenação de Curso'),
('Coordenação do Curso de Medicina Veterinária', 'Coordenação de Curso'),
('Coordenação do Curso de Agronomia', 'Coordenação de Curso'),
('Coordenação do Curso de Jornalismo', 'Coordenação de Curso'),
('Coordenação do Curso de Música', 'Coordenação de Curso'),
('Coordenação do Curso de Química', 'Coordenação de Curso'),
('Coordenação do Curso de Física', 'Coordenação de Curso'),
('Coordenação do Curso de Matemática', 'Coordenação de Curso'),

-- Pró-Reitorias e Diretorias (Estrutura Administrativa)
('Reitoria', 'Administrativo Superior'),
('Vice-Reitoria', 'Administrativo Superior'),
('Gabinete da Reitoria', 'Administrativo'),
('Pró-Reitoria de Graduação (PROGRAD)', 'Pró-Reitoria'),
('Pró-Reitoria de Pesquisa e Pós-Graduação (PROPEG)', 'Pró-Reitoria'),
('Pró-Reitoria de Extensão e Cultura (PROEX)', 'Pró-Reitoria'),
('Pró-Reitoria de Planejamento (PROPLAN)', 'Pró-Reitoria'),
('Pró-Reitoria de Administração (PROAD)', 'Pró-Reitoria'),
('Pró-Reitoria de Desenvolvimento e Gestão de Pessoas (PRODGEP)', 'Pró-Reitoria'),
('Pró-Reitoria de Assuntos Estudantis (PROAES)', 'Pró-Reitoria'),
('Diretoria de Sistemas de Informação (DSI)', 'Diretoria'),
('Diretoria de Comunicação (DECOM)', 'Diretoria'),
('Diretoria de Registro e Controle Acadêmico (DRCA)', 'Diretoria'),
('Diretoria de Apoio ao Desenvolvimento do Ensino (DIADE)', 'Diretoria'),
('Diretoria de Finanças e Contabilidade', 'Diretoria'),

-- Outras Unidades Administrativas e de Apoio
('Biblioteca Central', 'Apoio Acadêmico'),
('Prefeitura do Campus', 'Administrativo'),
('Hospital Universitário', 'Saúde'),
('Restaurante Universitário', 'Apoio Estudantil'),
('Assessoria de Cooperação Interinstitucional', 'Assessoria'),
('Procuradoria Federal', 'Jurídico'),
('Editora da UFAC (EDUFAC)', 'Apoio Acadêmico');

SELECT * FROM Unidade;

-- TABELA DE SERVIDORES:
CREATE TABLE Servidor (
    id_servidor INT PRIMARY KEY AUTO_INCREMENT,
    nome_servidor VARCHAR(255) NOT NULL,
    cargo_servidor VARCHAR(255),
    id_unidade INT NOT NULL,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade)
);

TRUNCATE TABLE Servidor;

-- INSERÇÃO DOS SERVIDORES:
INSERT INTO Servidor (nome_servidor, cargo_servidor, id_unidade) VALUES
('Adriana Lima da Silva', 'Professor Adjunto', 7),
('Bruno Costa de Almeida', 'Técnico Administrativo em Educação', 1),
('Carla Oliveira dos Santos', 'Analista de TI', 36),
('Diego Ferreira Martins', 'Coordenador de Curso', 9),
('Eduarda Ribeiro Gomes', 'Assistente Administrativo', 39),
('Fábio Pereira de Souza', 'Professor Titular', 11),
('Gabriela Rodrigues Alves', 'Secretária Acadêmica', 15),
('Heitor Barbosa Rocha', 'Diretor de Centro', 1),
('Isabela Azevedo Pinto', 'Técnico em Laboratório', 2),
('João Carlos de Medeiros', 'Professor Assistente', 13),
('Larissa Fernandes de Castro', 'Analista de Sistemas', 36),
('Marcos Vinícius Nogueira', 'Professor Adjunto', 17),
('Natália Correia Mendes', 'Assistente em Administração', 34),
('Otávio Monteiro da Cunha', 'Técnico em Contabilidade', 40),
('Patrícia Barros de Melo', 'Chefe de Departamento', 8),
('Rafael Tavares de Lima', 'Professor Adjunto', 21),
('Sofia Farias Cavalcanti', 'Psicóloga', 44),
('Thiago Viana de Andrade', 'Engenheiro Civil', 3),
('Yasmin Peixoto de Araújo', 'Bibliotecária', 41),
('Alexandre Magno Sampaio', 'Professor Titular', 5),
('Beatriz Vasconcelos de Aguiar', 'Técnico Administrativo', 33),
('Carlos Eduardo Portela', 'Professor Adjunto', 12),
('Daniela Matos de Albuquerque', 'Coordenadora Pedagógica', 16),
('Erickson Galvão de Lacerda', 'Analista de Redes', 36),
('Fernanda Guedes de Morais', 'Professora Assistente', 24),
('Gustavo Henrique Brandão', 'Assistente de TI', 36),
('Heloísa Dantas de Queiroz', 'Nutricionista', 43),
('Igor Valente de Freitas', 'Professor Adjunto', 26),
('Júlia Sales de Holanda', 'Técnica em Assuntos Educacionais', 33),
('Leonardo Bezerra de Menezes', 'Professor Titular', 7),
('Manuela Pires de Gusmão', 'Secretária Executiva', 29),
('Nicolas Drummond de Andrade', 'Professor Assistente', 14),
('Olívia Rabelo de Siqueira', 'Assistente Administrativo', 42),
('Pedro Paulo de Rezende', 'Coordenador de Pós-Graduação', 30),
('Quintino Bocaiúva de Oliveira', 'Professor Adjunto', 19),
('Rebeca Dorneles de Vasconcelos', 'Analista Financeiro', 40),
('Sérgio Amarante do Nascimento', 'Técnico em Edificações', 42),
('Tatiana Neves de Bragança', 'Professora Titular', 10),
('Ulisses Guimarães de Alencar', 'Professor Adjunto', 18),
('Vitória Régia de Assis', 'Assistente Social', 44),
('Washington Luís de Paula', 'Técnico Administrativo', 38),
('Xavier Fernandes do Prado', 'Professor Assistente', 20),
('Zélia Gattai de Faria', 'Coordenadora de Extensão', 31),
('Anderson de Abreu e Lima', 'Analista de Comunicação', 37),
('Bárbara de Cássia Penteado', 'Professora Adjunta', 22),
('Caio Fernando de Abreu', 'Técnico em Audiovisual', 37),
('Débora de Almeida Prado', 'Professora Assistente', 25),
('Elisa de Campos Vergal', 'Assistente de Biblioteca', 41),
('Felipe de Aquino Corrêa', 'Professor Titular', 4),
('Giovanna de Albuquerque Lins', 'Técnica Administrativa', 35),
('Hugo de Carvalho Ramos', 'Professor Adjunto', 27),
('Íris de Rezende Machado', 'Secretária', 1),
('Jorge de Lima e Silva', 'Coordenador Administrativo', 39),
('Kátia de Souza Leão', 'Professora Assistente', 6),
('Luan de Oliveira Bastos', 'Técnico de Manutenção', 42),
('Melissa de Arruda Botelho', 'Professora Adjunta', 2),
('Nelson de Sá e Benevides', 'Analista de Processos', 32),
('Oscar de Almeida Garrett', 'Professor Titular', 3),
('Pietra de Gusmão e Vasconcelos', 'Assistente de RH', 34),
('Ricardo de Albuquerque Maranhão', 'Professor Adjunto', 8),
('Simone de Beauvoir e Silva', 'Professora Assistente', 16),
('Teodoro de Sampaio e Melo', 'Técnico em Agropecuária', 22),
('Valentina de Andrade e Drummond', 'Professora Titular', 15),
('Vinícius de Moraes e Souza', 'Professor Adjunto', 18),
('William de Shakespeare e Oliveira', 'Técnico Administrativo', 30),
('Amanda da Costa Pereira', 'Professor Adjunto', 1),
('Bernardo Alves Ribeiro', 'Técnico em Informática', 36),
('Clara dos Santos Gomes', 'Assistente Administrativo', 33),
('Davi Martins Ferreira', 'Coordenador de Curso', 11),
('Elisa de Souza Lima', 'Professora Titular', 14),
('Francisco de Almeida Rocha', 'Professor Assistente', 23),
('Helena Barbosa de Castro', 'Secretária', 4),
('Ícaro de Azevedo Pinto', 'Técnico em Laboratório', 6),
('Joana de Medeiros Fernandes', 'Analista de Sistemas', 36),
('Lucas Nogueira Correia', 'Professor Adjunto', 9),
('Mariana Mendes da Cunha', 'Assistente em Administração', 39),
('Noah Monteiro de Barros', 'Técnico em Contabilidade', 40),
('Olga de Melo Tavares', 'Chefe de Seção', 10),
('Paulo de Lima Farias', 'Professor Adjunto', 12),
('Raquel de Andrade Cavalcanti', 'Psicóloga', 20),
('Samuel Viana de Araújo', 'Engenheiro Elétrico', 4),
('Tereza Peixoto Sampaio', 'Bibliotecária', 41),
('Vicente de Aguiar Vasconcelos', 'Professor Titular', 13),
('Alice Portela de Matos', 'Professora Assistente', 16),
('Benjamin de Albuquerque Galvão', 'Analista de Redes', 36),
('Cecília de Lacerda Guedes', 'Técnica Administrativa', 31),
('Dante de Morais Brandão', 'Professor Adjunto', 25),
('Esther de Queiroz Dantas', 'Nutricionista', 43),
('Félix de Freitas Valente', 'Técnico de Manutenção', 42),
('Gael de Holanda Sales', 'Professor Assistente', 27),
('Heloísa de Menezes Pires', 'Secretária Executiva', 28),
('Isaac de Andrade Drummond', 'Professor Titular', 19),
('Jasmim de Siqueira Rabelo', 'Assistente Administrativo', 38),
('Levi de Rezende Paulo', 'Coordenador Financeiro', 40),
('Miguel Bocaiúva de Vasconcelos', 'Professor Adjunto', 21);

SELECT * FROM Servidor;

-- TABELA DE PROCESSO DE DESFAZIMENTO:
CREATE TABLE Desfazimento (
    id_desfazimento INT PRIMARY KEY AUTO_INCREMENT,
    data_desfazimento DATE,
    numero_processo VARCHAR(100) UNIQUE
);

SELECT * FROM Desfazimento;

-- TABELA DE DOCUMENTOS DE BAIXA:
CREATE TABLE DocumentoDeBaixa (
    id_documento INT PRIMARY KEY AUTO_INCREMENT,
    numero_termo VARCHAR(20) NOT NULL,          -- Coluna que estava faltando para o número do termo (ex: "000123/2025")
    motivo VARCHAR(255),                        -- Coluna que estava faltando para o motivo da baixa
    data_geracao DATETIME,
    caminho_arquivo VARCHAR(512),               -- Nome da coluna corrigido para corresponder ao código Python
    id_desfazimento INT,
    FOREIGN KEY (id_desfazimento) REFERENCES Desfazimento(id_desfazimento)
    );

SELECT * FROM DocumentoDeBaixa;

-- TABELA DE BENS PATRIMONIAIS:
-- Cria a tabela 'Bem' com a estrutura completa e atualizada
CREATE TABLE Bem (
    tombo VARCHAR(10) PRIMARY KEY,
    descricao TEXT,
    data_aquisicao DATE,
    nota_fiscal VARCHAR(100),
    valor_aquisicao DECIMAL(10, 2) DEFAULT 0.00,  -- NOVO: Coluna para o valor de aquisição
    forma_ingresso VARCHAR(100),                  -- NOVO: Coluna para a forma de ingresso
    classificacao VARCHAR(100) NULL,
    destinacao VARCHAR(100) NULL,
    id_unidade INT,
    id_servidor INT,
    id_desfazimento INT NULL,
    id_documento INT NULL,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade),
    FOREIGN KEY (id_servidor) REFERENCES Servidor(id_servidor),
    FOREIGN KEY (id_desfazimento) REFERENCES Desfazimento(id_desfazimento),
    FOREIGN KEY (id_documento) REFERENCES DocumentoDeBaixa(id_documento)
);
UPDATE Bem SET 
    valor_aquisicao = ROUND(RAND() * (5000 - 150) + 150, 2), 
    forma_ingresso = 'Compra';

TRUNCATE TABLE Bem;

-- INSERÇÃO DOS BENS:
INSERT INTO Bem (tombo, descricao, data_aquisicao, nota_fiscal, classificacao, destinacao, id_unidade, id_servidor, id_desfazimento, id_documento) VALUES
('100100', 'Computador Desktop Dell OptiPlex 3080, Intel i5, 8GB RAM, 256GB SSD', '2022-03-15', 'NF-e 45678', NULL, NULL, 36, 3, NULL, NULL),
('100101', 'Monitor LED 23.8" Dell P2419H', '2022-03-15', 'NF-e 45678', NULL, NULL, 1, 8, NULL, NULL),
('100102', 'Cadeira de escritório giratória, preta, com braços', '2021-11-20', 'NF-e 33210', NULL, NULL, 34, 13, NULL, NULL),
('100103', 'Mesa de escritório 1.20m x 0.60m, cor carvalho', '2021-11-20', 'NF-e 33210', NULL, NULL, 39, 5, NULL, NULL),
('100104', 'Projetor Multimídia Epson PowerLite S41+', '2023-01-10', 'NF-e 51234', NULL, NULL, 4, 1, NULL, NULL),
('100105', 'Ar-condicionado Split 12.000 BTUs, Springer Midea', '2020-09-05', 'NF-e 20556', NULL, NULL, 7, 10, NULL, NULL),
('100106', 'Impressora a Laser HP LaserJet Pro M130fw', '2022-05-22', 'NF-e 47890', NULL, NULL, 36, 11, NULL, NULL),
('100107', 'Bebedouro de pressão, inox, Esmaltec', '2019-08-12', 'NF-e 15432', NULL, NULL, 42, 33, NULL, NULL),
('100108', 'Notebook Dell Vostro 15, Intel i7, 16GB RAM, 512GB SSD', '2023-02-28', 'NF-e 52001', NULL, NULL, 9, 4, NULL, NULL),
('100109', 'Armário de aço com 2 portas e 4 prateleiras', '2018-06-18', 'NF-e 10123', NULL, NULL, 38, 41, NULL, NULL),
('100110', 'Microscópio Biológico Binocular, aumento 1600x', '2021-04-10', 'NF-e 29876', NULL, NULL, 2, 9, NULL, NULL),
('100111', 'Quadro branco magnético 2.00m x 1.20m', '2022-08-01', 'NF-e 49123', NULL, NULL, 16, 23, NULL, NULL),
('100112', 'Cadeira universitária com prancheta fixa', '2020-02-15', 'NF-e 18990', NULL, NULL, 17, 12, NULL, NULL),
('100113', 'Longarina de 3 lugares para recepção, estofado azul', '2019-05-30', 'NF-e 14321', NULL, NULL, 29, 31, NULL, NULL),
('100114', 'Televisor Smart 50" 4K LG', '2023-04-05', 'NF-e 53112', NULL, NULL, 31, 43, NULL, NULL),
('100115', 'Fragmentadora de papel, 10 folhas, Secreta', '2021-07-25', 'NF-e 31456', NULL, NULL, 35, 51, NULL, NULL),
('100116', 'Nobreak SMS Manager III 1400VA', '2022-10-11', 'NF-e 50123', NULL, NULL, 36, 24, NULL, NULL),
('100117', 'Estante de aço para livros, 6 prateleiras', '2018-10-02', 'NF-e 12345', NULL, NULL, 41, 19, NULL, NULL),
('100118', 'Balança de precisão digital para laboratório, 0.01g', '2020-07-19', 'NF-e 19876', NULL, NULL, 26, 28, NULL, NULL),
('100119', 'Câmera DSLR Canon EOS Rebel T7+', '2022-11-30', 'NF-e 51009', NULL, NULL, 37, 44, NULL, NULL),
('100120', 'Mesa de reunião redonda, 1.20m de diâmetro', '2019-03-22', 'NF-e 13876', NULL, NULL, 30, 34, NULL, NULL),
('100121', 'Central Telefônica PABX Intelbras', '2020-01-15', 'NF-e 17654', NULL, NULL, 39, 5, NULL, NULL),
('100122', 'Fogão industrial 4 bocas, com forno', '2021-09-01', 'NF-e 32098', NULL, NULL, 44, 17, NULL, NULL),
('100123', 'Refrigerador Consul 342 litros, branco', '2022-06-10', 'NF-e 48002', NULL, NULL, 43, 27, NULL, NULL),
('100124', 'Macrômetro digital 0-25mm, Mitutoyo', '2023-03-01', 'NF-e 52555', NULL, NULL, 3, 18, NULL, NULL),
('100125', 'Osciloscópio digital 100MHz, Minipa', '2021-02-18', 'NF-e 28765', NULL, NULL, 4, 54, NULL, NULL),
('100200', 'Scanner de mesa HP ScanJet Pro 2500', '2022-09-14', 'NF-e 49871', NULL, NULL, 38, 41, NULL, NULL),

('20543', 'Cadeira fixa empilhável, modelo iso, azul', '2017-08-21', 'NF-e 8765', NULL, NULL, 32, 58, NULL, NULL),
('31298', 'Gaveteiro volante com 4 gavetas, branco', '2020-05-16', 'NF-e 19432', NULL, NULL, 34, 13, NULL, NULL),
('45876', 'Computador Desktop Lenovo ThinkCentre, i3, 4GB RAM', '2019-11-02', 'NF-e 16879', NULL, NULL, 8, 57, NULL, NULL),
('56123', 'Estabilizador de Tensão 1000VA, Ragtech', '2021-06-25', 'NF-e 31001', NULL, NULL, 36, 68, NULL, NULL),
('67345', 'Mesa para refeitório, 4 lugares, tampo de granito', '2018-04-11', 'NF-e 9987', NULL, NULL, 44, 86, NULL, NULL),
('78901', 'Aspirador de pó industrial, 1400W', '2022-02-10', 'NF-e 44321', NULL, NULL, 42, 37, NULL, NULL),
('89123', 'Carrinho de transporte de carga, plataforma, 300kg', '2019-10-15', 'NF-e 16432', NULL, NULL, 42, 33, NULL, NULL),
('91234', 'Esqueleto humano articulado em tamanho real, modelo anatômico', '2020-11-20', 'NF-e 22345', NULL, NULL, 3, 18, NULL, NULL),
('112233', 'Multímetro Digital Minipa ET-2042E', '2023-05-10', 'NF-e 54001', NULL, NULL, 10, 38, NULL, NULL),
('121212', 'Switch de rede 24 portas Gigabit, TP-Link', '2022-07-07', 'NF-e 48500', NULL, NULL, 36, 2, NULL, NULL),
('134567', 'Arquivo de aço com 4 gavetas, para pasta suspensa', '2017-05-19', 'NF-e 8123', NULL, NULL, 38, 41, NULL, NULL),
('150510', 'Sofá de 2 lugares, couro sintético preto', '2020-08-14', 'NF-e 20111', NULL, NULL, 29, 31, NULL, NULL),
('160789', 'Violão Clássico Nylon, Giannini', '2021-03-25', 'NF-e 29432', NULL, NULL, 24, 25, NULL, NULL),
('175321', 'Bateria de Agitadores Magnéticos com Aquecimento', '2022-10-05', 'NF-e 50021', NULL, NULL, 26, 28, NULL, NULL),
('180001', 'Cadeira de rodas simples, aço', '2019-01-20', 'NF-e 12987', NULL, NULL, 43, 27, NULL, NULL),
('199887', 'Maca hospitalar simples com rodízios', '2021-12-15', 'NF-e 34567', NULL, NULL, 3, 89, NULL, NULL),
('201020', 'Termômetro Infravermelho Digital', '2020-04-10', 'NF-e 19123', NULL, NULL, 14, 12, NULL, NULL),
('213456', 'Furadeira de impacto, 1/2", 750W, Bosch', '2022-08-20', 'NF-e 49321', NULL, NULL, 42, 37, NULL, NULL),
('224455', 'Mesa de desenho técnico A0 com régua paralela', '2018-09-12', 'NF-e 11876', NULL, NULL, 9, 4, NULL, NULL),
('235678', 'Podadora de grama a gasolina', '2021-10-30', 'NF-e 33001', NULL, NULL, 42, 33, NULL, NULL),
('250000', 'Caixa de som amplificada, 200W RMS, com microfone', '2023-06-01', 'NF-e 54500', NULL, NULL, 37, 46, NULL, NULL);

SELECT * FROM Bem;

-- TABELA DE PLANILHAS FINALIZADAS:
CREATE TABLE PlanilhaFinalizada (
    id_planilha INT PRIMARY KEY AUTO_INCREMENT,
    nome_planilha VARCHAR(255) NOT NULL,
    caminho_arquivo_planilha VARCHAR(512) NOT NULL,
    data_geracao DATETIME,
    total_tombos INT,
    id_desfazimento INT UNIQUE,
    FOREIGN KEY (id_desfazimento) REFERENCES Desfazimento(id_desfazimento)
);

SELECT * FROM PlanilhaFinalizada;

-- TABELA DE USUÁRIOS:
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome_completo VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE, -- Formato: 123.456.789-10
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('Administrador', 'Servidor', 'Estagiário') NOT NULL
);

-- INSERÇÃO DO USUÁRIO ADMINISTRADOR PADRÃO:
-- CPF: 000.000.000-00
-- Senha: admin
INSERT INTO Usuario (nome_completo, cpf, senha_hash, perfil) VALUES
('Administrador Padrão', '000.000.000-00', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Administrador');

SELECT * FROM Usuario;

-- TABELA DE CONFIGURAÇÕES:
CREATE TABLE Configuracao (
    chave VARCHAR(50) PRIMARY KEY,
    valor VARCHAR(255)
);

-- INSERÇÃO DOS VALORES PADRÃO:
INSERT INTO Configuracao (chave, valor) VALUES
('tema', 'Claro'),
('pasta_padrao', ''),
('formato_padrao', '.pdf'),
('salvar_auto', '1'), -- 1 para True (ligado), 0 para False (desligado)
('lembrar_configs', '1');

SELECT * FROM Configuracao;
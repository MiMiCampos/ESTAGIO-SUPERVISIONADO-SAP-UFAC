-- EXCLUI O BANCO PERMANENTEMENTE:
DROP DATABASE IF EXISTS sap_ufac_db;

CREATE DATABASE sap_ufac_db;

USE sap_ufac_db;

CREATE TABLE Unidade (
    id_unidade INT PRIMARY KEY AUTO_INCREMENT,
    nome_unidade VARCHAR(255) NOT NULL UNIQUE,
    setor VARCHAR(255)
);

CREATE TABLE Servidor (
    id_servidor INT PRIMARY KEY AUTO_INCREMENT,
    nome_servidor VARCHAR(255) NOT NULL,
    cargo_servidor VARCHAR(255),
    id_unidade INT NOT NULL,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade)
);

CREATE TABLE Desfazimento (
    id_desfazimento INT PRIMARY KEY AUTO_INCREMENT,
    data_desfazimento DATE,
    numero_processo VARCHAR(100) UNIQUE
);

CREATE TABLE DocumentoDeBaixa (
    id_documento INT PRIMARY KEY AUTO_INCREMENT,
    data_geracao DATETIME,
    caminho_arquivo_baixa VARCHAR(512), -- Caminhos de arquivo podem ser longos
    id_desfazimento INT,
    FOREIGN KEY (id_desfazimento) REFERENCES Desfazimento(id_desfazimento)
);

CREATE TABLE Bem (
    tombo VARCHAR(10) PRIMARY KEY,
    descricao TEXT,
    data_aquisicao DATE,
    nota_fiscal VARCHAR(100),
    classificacao VARCHAR(100),
    destinacao VARCHAR(100),
    id_unidade INT,
    id_servidor INT,
    id_desfazimento INT,
    id_documento INT,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade),
    FOREIGN KEY (id_servidor) REFERENCES Servidor(id_servidor),
    FOREIGN KEY (id_desfazimento) REFERENCES Desfazimento(id_desfazimento),
    FOREIGN KEY (id_documento) REFERENCES DocumentoDeBaixa(id_documento)
);

CREATE TABLE PlanilhaFinalizada (
    id_planilha INT PRIMARY KEY AUTO_INCREMENT,
    nome_planilha VARCHAR(255) NOT NULL,
    caminho_arquivo_planilha VARCHAR(512) NOT NULL,
    data_geracao DATETIME,
    total_tombos INT,
    id_desfazimento INT UNIQUE,
    FOREIGN KEY (id_desfazimento) REFERENCES Desfazimento(id_desfazimento)
);
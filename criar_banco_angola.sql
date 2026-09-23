CREATE TABLE pacientes (
    codigo SERIAL PRIMARY KEY,                        -- Código gerado automaticamente (AutoIncremento)
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE, -- Data automática de criação do registro
    nome_paciente VARCHAR(150) NOT NULL,              -- Nome completo do paciente
    sexo VARCHAR(15),                                 -- Masculino / Feminino
    data_nascimento DATE,                             -- Data de nascimento
    idade INT,                                        -- Idade fixa
    estado_civil VARCHAR(30),                         -- Estado civil
    profissao VARCHAR(100),                           -- Profissão
    naturalidade VARCHAR(100),                        -- Província/Município de nascimento
    bi_identidade VARCHAR(20) UNIQUE,                 -- Bilhete de Identidade (BI) de Angola
    nif VARCHAR(20) UNIQUE,                           -- Número de Identificação Fiscal (NIF)
    seguro_saude VARCHAR(100),                        -- Seguradoras locais (Ex: ENSA, Nossa Seguros)
    nome_pai VARCHAR(150),                            -- Nome completo do pai
    nome_mae VARCHAR(150),                            -- Nome completo da mãe
    endereco VARCHAR(200),                            -- Rua / Avenida / Distrito
    numero VARCHAR(10),                               -- Número da residência ou apartamento
    bairro VARCHAR(100),                              -- Bairro (Ex: Talatona, Maianga, Benfica)
    municipio VARCHAR(100),                           -- Município (Ex: Belas, Viana, Cazenga)
    provincia VARCHAR(50),                            -- Província (Ex: Luanda, Huambo, Benguela)
    telemovel_principal VARCHAR(28),                  -- Contacto telefónico principal (+244)
    telemovel_alternativo VARCHAR(28),                -- Contacto telefónico alternativo
    trabalho_empresa VARCHAR(158),                    -- Empresa onde trabalha
    observacoes_medicas TEXT,                         -- Alergias e anotações clínicas gerais
    foto_paciente BYTEA,                              -- Armazenamento binário da imagem do paciente
    
    -- NOVOS CAMPOS EXIGIDOS COMPILADOS NA TABELA:
    tipo_sanguineo VARCHAR(3),                        -- Grupo Sanguíneo (Ex: A+, O-)
    total_consultas INT DEFAULT 0,                    -- Registro do número de consultas feitas
    guias_solicitadas INT DEFAULT 0,                  -- Registro de guias médicas solicitadas
    data_consulta DATE                                -- Registro da data da consulta
);

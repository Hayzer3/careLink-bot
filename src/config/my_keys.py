import os
from dotenv import load_dotenv

load_dotenv()

# Só Gemini agora
GEMINI_API_KEY = "sua apy key"

# Configuração Oracle para funcionários
ORACLE_CONFIG = {
    'user': os.getenv('DB_USER', 'usuario'),
    'password': os.getenv('DB_PASSWORD', 'senha'), 
    'host': 'oracle.fiap.com.br',
    'port': 1521,
    'sid': 'ORCL'
}

DATABASE_SCHEMA = """
-- Schema do banco hospitalar (para funcionários)
TB_CAR_PACIENTE: id_paciente, nome_paciente, celular_paciente
TB_CAR_PROFISSIONAL_SAUDE: id_profissional, nome_profissional, especialidade_profissional  
TB_CAR_CONSULTA: id_consulta, id_paciente, id_profissional, data_agenda, status_consulta
TB_CAR_METRIC_ABSENT: percentual_absenteismo_geral, total_faltas
"""
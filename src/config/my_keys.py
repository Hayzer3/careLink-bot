import os

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', "AIzaSyBvb3WGdJfWX-4vT-whbi1Vh8KuoNgG4eA")

ORACLE_CONFIG = {
    'user': os.getenv('DB_USER', "rm566358"),
    'password': os.getenv('DB_PASSWORD', "fiap25"), 
    'host': os.getenv('DB_HOST', "oracle.fiap.com.br"),
    'port': 1521,
    'sid': os.getenv('DB_SID', "ORCL")
}

DATABASE_SCHEMA = """
TB_CAR_PACIENTE: id_paciente, nome_paciente, celular_paciente
TB_CAR_PROFISSIONAL_SAUDE: id_profissional, nome_profissional, especialidade_profissional  
TB_CAR_CONSULTA: id_consulta, id_paciente, id_profissional, data_agenda, status_consulta
"""
import os
from dotenv import load_dotenv

# Isso é novo!
# Ele vai procurar um arquivo .env e carregar as chaves de lá
# para dentro do 'os.getenv'
load_dotenv() 


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

ORACLE_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': 1521, 
    'sid': os.getenv('DB_SID')
}

DATABASE_SCHEMA = """
TB_CAR_PACIENTE: id_paciente, nome_paciente, celular_paciente
TB_CAR_PROFISSIONAL_SAUDE: id_profissional, nome_profissional, especialidade_profissional  
TB_CAR_CONSULTA: id_consulta, id_paciente, id_profissional, data_agenda, status_consulta
"""

# verificação para saber se tudo carregou
if not GEMINI_API_KEY or not ORACLE_CONFIG['user']:
    print("ERRO CRÍTICO: As variáveis de ambiente não foram carregadas.")
 
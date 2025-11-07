from langchain_google_genai import ChatGoogleGenerativeAI
from config.my_keys import GEMINI_API_KEY, DATABASE_SCHEMA
from utils.my_models import GEMINI_FLASH

class QueryGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=GEMINI_FLASH,
            temperature=0.1
        )
    
    def generate_sql_query(self, user_question):
        prompt = f"""
        Sistema hospitalar. Schema: {DATABASE_SCHEMA}
        
        Pergunta: {user_question}
        
        Gere SQL Oracle (apenas SELECT). Para faltas: status_consulta='FALTOU'
        IMPORTANTE: Não use ponto e vírgula (;) no final da query!

        Retorne só a query SQL:
        """
        
        try:
            response = self.llm.invoke(prompt)
            query = response.content.strip()
            query = query.rstrip(';')
            return query
        except Exception as e:
            print(f"Erro ao gerar query: {e}")
            return None
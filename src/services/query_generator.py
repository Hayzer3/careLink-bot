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
        
        REGRAS IMPORTANTES:
        - NÃO use ponto e vírgula (;) no final
        - NÃO use markdown (não use ```sql)
        - Apenas a query SQL pura, sem formatação
        
        Retorne só a query SQL:
        """
        
        try:
            response = self.llm.invoke(prompt)
            query = response.content.strip()
            query = query.replace('```sql', '').replace('```', '').strip()
            query = query.rstrip(';')
            
            print(f"Query após limpeza: {query}")
            return query
        except Exception as e:
            print(f"Erro ao gerar query: {e}")
            return None
from services.oracle_connector import OracleConnector
from services.query_generator import QueryGenerator
from services.gemini_client import GeminiClient

class DatabaseBot:
    def __init__(self):
        self.gemini = GeminiClient()  
        self.db = OracleConnector()
        self.query_gen = QueryGenerator()
    
    def handle_staff_message(self, user_id, message):
        """Processa perguntas de funcionários sobre dados do hospital"""
          # gera query SQL
      
        sql_query = self.query_gen.generate_sql_query(message)
        
        if not sql_query:
            return "Não consegui entender sua pergunta sobre os dados."
        
        print(f"Query gerada: {sql_query}")
        
        #Executa no banco
        resultados = self.db.execute_query(sql_query)
        #gera resposta natural
        resposta = self._generate_technical_response(message, resultados)
        
        return resposta
    
    def _generate_technical_response(self, pergunta, dados_banco):
        """gera resposta técnica para funcionários"""
        if not dados_banco:
            return "Não encontrei dados com esses critérios."
        
        prompt = f"""
        Você é assistente para FUNCIONÁRIOS do hospital. Seja direto e técnico.

        PERGUNTA: {pergunta}
        DADOS ENCONTRADOS: {dados_banco}

        Explique os dados de forma clara:
        """
        
        try:
            # usa o mesmo GeminiClient mas com prompt diferente
            resposta = self.gemini.llm.invoke(prompt)
            return resposta.content
        except Exception as e:
            return f"Erro: {str(e)}"
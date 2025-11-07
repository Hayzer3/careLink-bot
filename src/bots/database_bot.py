from services.oracle_connector import OracleConnector
from services.query_generator import QueryGenerator
from services.gemini_client import GeminiClient

class DatabaseBot:
    def __init__(self):
        self.gemini = GeminiClient()  
        self.db = OracleConnector()
        self.query_gen = QueryGenerator()
    
    def handle_staff_message(self, user_id, message):
        print(f"DatabaseBot: Processando mensagem - {message}")
        
        # gera query SQL
        sql_query = self.query_gen.generate_sql_query(message)
        
        if not sql_query:
            print("DatabaseBot: Não gerou query SQL")
            return "Não consegui entender sua pergunta sobre os dados."
        
        print(f"DatabaseBot: Query gerada - {sql_query}")
        
        # Executa no banco
        try:
            resultados = self.db.execute_query(sql_query)
            print(f"DatabaseBot: Resultados do banco - {resultados}")
        except Exception as db_error:
            print(f"DatabaseBot: Erro no banco - {db_error}")
            return f"Erro ao acessar o banco de dados: {str(db_error)}"
        
        # gera resposta natural
        resposta = self._generate_technical_response(message, resultados)
        
        return resposta
    
    def _generate_technical_response(self, pergunta, dados_banco):
        """Gera resposta técnica para funcionários"""
        if not dados_banco:
            return "Não encontrei dados com esses critérios."
        
        prompt = f"""
        Você é assistente para FUNCIONÁRIOS do hospital. A linguagem precisa ser simples, simplificada.

            REGRAS IMPORTANTES:
            - NÃO use markdown (não use **, #, ou qualquer formatação)
            - NÃO destaque palavras com negrito
            - Seja direto e natural, como numa conversa normal
            - Use português claro e simples

        PERGUNTA: {pergunta}
        DADOS ENCONTRADOS: {dados_banco}

        Explique os dados de forma clara:
        """
        
        try:
            resposta = self.gemini.llm.invoke(prompt)
            return resposta.content
        except Exception as e:
            return f"Erro: {str(e)}"
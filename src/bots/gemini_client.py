from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.prompts import prompt_baixa_afinidade

class GeminiClient:
    def __init__(self, api_key):
        self.llm = ChatGoogleGenerativeAI(
            api_key=api_key,
            model="gemini-1.5-pro",  # TROCA: gpt-pro por gemini-1.5-pro para evitar o erro 404
            temperature=0.7
        )
    
    def generate_response_for_elderly(self, pergunta, contexto=None):
        """Gera resposta ESPECIAL para idosos"""
        
        prompt_final = prompt_baixa_afinidade.format(pergunta=pergunta)
        
        if contexto:
            prompt_final += f"\nCONTEXTO DO MANUAL: {contexto}"
        
        try:
            resposta = self.llm.invoke(prompt_final)
            return resposta.content
        except Exception as e:
            return f"TENTE NOVAMENTE. DEU UM ERRINHO: {str(e)}"
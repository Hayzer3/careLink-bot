from langchain_google_genai import ChatGoogleGenerativeAI
from utils.prompts import prompt_baixa_afinidade
from utils.my_models import GEMINI_FLASH
from config.my_keys import GEMINI_API_KEY

class GeminiClient:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=GEMINI_FLASH,
            temperature=0.7
        )
    
    def generate_response_for_elderly(self, pergunta, contexto=None):
        # prepara o contexto para o prompt
        contexto_texto = ""
        if contexto:
            contexto_texto = f"CONTEXTO DO MANUAL: {contexto}"
        
        prompt_final = prompt_baixa_afinidade.format(
            pergunta=pergunta,
            contexto=contexto_texto
        )
        
        try:
            resposta = self.llm.invoke(prompt_final)
            return resposta.content
        except Exception as e:
            return f"Desculpe, tente novamente. Erro: {str(e)}"
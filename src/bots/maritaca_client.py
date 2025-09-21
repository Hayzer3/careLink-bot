import openai

class MaritacaClient:
    def __init__(self, api_key):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://chat.maritaca.ai/api"
        )
    
    def generate_response(self, prompt, context=None):
        messages = [
            {
                "role": "system", 
                "content": "Você é o CareLink, assistente digital do Hospital das Clínicas. "
                          "Seja empático, claro e objetivo. Use linguagem simples e acessível."
            },
            {"role": "user", "content": prompt}
        ]
        
        if context:
            messages.insert(1, {"role": "system", "content": f"Contexto: {context}"})
        
        try:
            response = self.client.chat.completions.create(
                model="sabia-3",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Desculpe, estou com dificuldades técnicas. Por favor, tente novamente mais tarde. ({str(e)})"
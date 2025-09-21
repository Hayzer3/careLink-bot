from src.bots.carelink_bot import CareLinkBot
from config.my_keys import MARITACA_API_KEY, GEMINI_API_KEY

def main():
    # Inicializar o bot CareLink com o manual PDF
    bot = CareLinkBot(
        maritaca_api_key=MARITACA_API_KEY,
        gemini_api_key=GEMINI_API_KEY,
        pdf_path="data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf"
    )
    
    # Exemplos de perguntas que serão respondidas baseadas no manual
    questions = [
        "Como faço para agendar uma teleconsulta?",
        "Quais são os requisitos para usar o portal do paciente?",
        "Como resetar minha senha?",
        "O que fazer se não consigo acessar minha consulta?"
    ]
    
    for question in questions:
        print(f"Paciente: {question}")
        response = bot.handle_message("12345", question)
        print(f"CareLink: {response}\n")

if __name__ == "__main__":
    main()
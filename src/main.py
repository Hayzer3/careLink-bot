from bots.carelink_bot import CareLinkBot
from config.my_keys import GEMINI_API_KEY  

def main():
    bot = CareLinkBot( 
        gemini_api_key=GEMINI_API_KEY,
        pdf_path="src/data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf",
    )
    
    questions = [
        "Quero agendar uma consulta!",
    ]
    
    for question in questions:
        print(f" Paciente: {question}")
        response = bot.handle_message("12345", question)
        print(f" CareLink: {response}\n")

if __name__ == "__main__":
    main()
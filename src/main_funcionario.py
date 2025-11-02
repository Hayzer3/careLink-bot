from bots.database_bot import DatabaseBot
from config.my_keys import GEMINI_API_KEY
#PARA TESTES!!
def main():
    bot = DatabaseBot()  
    
    questions = [
        "Quantos pacientes temos no sistema?",
    ]
    
    for question in questions:
        print(f" Funcionário: {question}")
        response = bot.handle_staff_message("func_001", question)
        print(f" Sistema: {response}\n")

if __name__ == "__main__":
    main()
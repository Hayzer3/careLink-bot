from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# add o src ao path para importar osmódulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from bots.database_bot import DatabaseBot

app = Flask(__name__)
CORS(app)  

# inicializa o bot
bot = DatabaseBot()

@app.route('/')
def root():
    return jsonify({"message": "CareLink Staff API está rodando!"})

@app.route('/api/staff-chat', methods=['POST'])
def staff_chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Campo 'message' é obrigatório"}), 400
        
        message = data['message']
        user_id = data.get('user_id', 'func_001')
        
        print(f" Mensagem recebida: {message}")
        
        response = bot.handle_staff_message(user_id, message)
        
        print(f" Resposta gerada: {response}")
        
        return jsonify({
            "response": response,
            "user_id": user_id,
            "success": True
        })
    
    except Exception as e:
        print(f"Erro na API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "CareLink Staff API"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
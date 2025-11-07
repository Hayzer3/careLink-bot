from flask import Flask, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bots.carelink_bot import CareLinkBot
from config.my_keys import GEMINI_API_KEY

app = Flask(__name__)

bot = CareLinkBot(
    gemini_api_key=GEMINI_API_KEY,
    pdf_path="data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf"
)

@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
def webhook_whatsapp():
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token', '')
        challenge = request.args.get('hub.challenge', '')
        if verify_token == 'carelink_token':
            return challenge
        return 'Token inválido', 403
    
    elif request.method == 'POST':
        try:
            data = request.json
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message = value['messages'][0]
                user_number = message['from']
                user_message = message.get('text', {}).get('body', '')
                
                if user_message:
                    resposta = bot.handle_message(user_number, user_message)
                    return jsonify({'status': 'success', 'resposta': resposta})
            
            return jsonify({'status': 'no_message'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.json
    pergunta = data.get('pergunta', '').strip()
    
    if not pergunta:
        return jsonify({'error': 'Forneça uma pergunta'}), 400
    
    resposta = bot.handle_message("api_user", pergunta)
    
    return jsonify({
        'pergunta': pergunta,
        'resposta': resposta,
        'status': 'success'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'online'})

@app.route('/')
def home():
    return '''
    <h1>CareLink Bot</h1>
    <p>Use POST /perguntar com {"pergunta": "sua pergunta"}</p>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
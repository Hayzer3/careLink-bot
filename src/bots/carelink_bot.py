from services.gemini_client import GeminiClient
from services.appointment_manager import AppointmentManager
from config.my_keys import GEMINI_API_KEY
from utils.semantic_searcher import SemanticSearcher


class CareLinkBot:
    def __init__(self, gemini_api_key=None, pdf_path=None):  # ← Torne o parâmetro opcional
        self.gemini_client = GeminiClient()  # ← REMOVA a passagem da key
        self.appointment_manager = AppointmentManager()
        self.has_manual = False

        # busca no manual
        if pdf_path:
            try:
                self.searcher = SemanticSearcher(pdf_path)
                self.has_manual = True
                print(" Manual do paciente carregado")
            except Exception as e:
                print(f"Erro ao carregar manual: {e}")
        else:
            print("Nenhum PDF informado — busca semântica desativada.")
    
    def handle_message(self, user_id, message):
        """Processa mensagem do paciente"""
        contexto = ""

        if self.has_manual:
            try:
                manual_context = self.searcher.search(message)
                if manual_context:
                    contexto = f"MANUAL DO SISTEMA: {manual_context}"
            except Exception as e:
                print(f"Erro na busca semântica: {e}")

        # verifica se é sobre agendamento
        if self._is_appointment_related(message):
            return self.appointment_manager.handle_appointment_request(user_id, message)

        # gera resposta via Gemini
        resposta = self.gemini_client.generate_response_for_elderly(
            pergunta=message,
            contexto=contexto
        )

        return resposta

    def _is_appointment_related(self, message):
        """Detecta se a mensagem é sobre agendamento"""
        keywords = ['agendar', 'consulta', 'marcar', 'horário', 'data', 'reagendar', 'cancelar']
        return any(keyword in message.lower() for keyword in keywords)

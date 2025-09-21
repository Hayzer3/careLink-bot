from src.bots.maritaca_client import MaritacaClient
from src.bots.gemini_analyzer import GeminiAnalyzer
from src.services.appointment_manager import AppointmentManager
from src.services.pdf_processor import PDFProcessor
from src.utils.semantic_searcher import SemanticSearcher
import re

class CareLinkBot:
    def __init__(self, maritaca_api_key, gemini_api_key, pdf_path):
        self.maritaca_client = MaritacaClient(api_key=maritaca_api_key)
        self.gemini_analyzer = GeminiAnalyzer(api_key=gemini_api_key)
        self.appointment_manager = AppointmentManager()
        self.searcher = SemanticSearcher(pdf_path)
    
    def handle_message(self, patient_id, message, image_data=None):
        # Primeiro busca no manual com busca semântica
        manual_info = self.searcher.search(message)
        
        # SE HOUVER IMAGEM: analisar primeiro
        if image_data:
            return self._handle_image_analysis(patient_id, image_data, message)
        
        # Se não houver imagem, processar texto normal
        if manual_info:
            context = "\n".join(manual_info[:3])
            return self.maritaca_client.generate_response(
                f"Baseado no manual do sistema, responda: {message}",
                context=context
            )
        
        # Processar outras intenções...
        return self._handle_text_intent(patient_id, message)
    
    def _handle_image_analysis(self, patient_id, image_data, message=""):
        """
        Processa screenshots do aplicativo enviadas pelos pacientes
        """
        # Analisar a imagem com Gemini
        analysis = self.gemini_analyzer.analyze_app_screenshot(image_data)
        
        # Extrair texto da imagem para buscar no manual
        extracted_text = self.gemini_analyzer.extract_text_from_image(image_data)
        
        # Buscar soluções no manual baseado no texto extraído
        manual_solutions = self.searcher.search(extracted_text)
        
        # Combinar análise da IA com soluções do manual
        if manual_solutions:
            context = f"Análise da imagem: {analysis}\n\nSoluções do manual: {' '.join(manual_solutions[:2])}"
        else:
            context = f"Análise da imagem: {analysis}"
        
        # Gerar resposta final usando Maritaca
        response = self.maritaca_client.generate_response(
            f"Um paciente enviou esta screenshot do aplicativo. {message}",
            context=context
        )
        
        return response
    
    def _handle_text_intent(self, patient_id, message):
        """Processa mensagens de texto normais"""
        intent = self._classify_intent(message)
        
        if "lembrete" in intent or "confirmar" in intent:
            return self._handle_appointment_confirmation(patient_id)
        elif "dúvida" in intent or "ajuda" in intent or "problema" in intent:
            return self._provide_guidance(message)
        elif "cancelar" in intent:
            return self._handle_cancellation(patient_id)
        else:
            return self.maritaca_client.generate_response(message)
    

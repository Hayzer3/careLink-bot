import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.documents = []
    
    def extract_text_from_pdf(self):
        """Extrai texto do PDF manual do sistema"""
        if not os.path.exists(self.pdf_path):
            print(f"Arquivo não encontrado: {self.pdf_path}")
            return ""
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ""

                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                
                return text
        except Exception as e:
            print(f"Erro ao ler PDF: {e}")
            return ""
    
    def create_knowledge_base(self):
        """Cria base de conhecimento a partir do PDF"""
        text = self.extract_text_from_pdf()
        
        if not text:
            print("Nenhum texto extraído do PDF")
            return []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        documents = text_splitter.split_text(text)
        
        print(f"Base de conhecimento criada com {len(documents)} segmentos")
        return documents

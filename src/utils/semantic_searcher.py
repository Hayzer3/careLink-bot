import numpy as np
from sentence_transformers import SentenceTransformer
from services.pdf_processor import PDFProcessor

class SemanticSearcher:
    def __init__(self, pdf_path):
        self.pdf_processor = PDFProcessor(pdf_path)
        self.documents = self.pdf_processor.create_knowledge_base()
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embeddings = self._create_embeddings()
    
    def _create_embeddings(self):
        """Cria os vetores de significado para todo o manual"""
        print("Criando embeddings para o manual...")
        return self.model.encode(self.documents)
    
    def search(self, query, top_k=3):
        """Encontra os trechos mais relevantes do manual"""

        query_embedding = self.model.encode([query])
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        return [self.documents[i] for i in top_indices]

if __name__ == "__main__":
    searcher = SemanticSearcher("src/data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf")
    
    perguntas_teste = [
        "Como agendar teleconsulta?",
        "Esqueci minha senha",
    ]
    
    for pergunta in perguntas_teste:
        print(f"\n Pergunta: {pergunta}")
        resultados = searcher.search(pergunta)
        print(f"Trechos encontrados: {len(resultados)}")
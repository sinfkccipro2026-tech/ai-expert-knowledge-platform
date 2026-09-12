"""Semantic Embedding Service"""
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """Generate embeddings for semantic search"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embedding(self, text):
        """Generate embedding for text"""
        return self.model.encode(text).tolist()
    
    def get_similarities(self, query_text, texts):
        """Calculate similarity scores"""
        query_embedding = self.model.encode(query_text)
        text_embeddings = self.model.encode(texts)
        
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity([query_embedding], text_embeddings)[0]
        
        return [(text, score) for text, score in zip(texts, similarities)]

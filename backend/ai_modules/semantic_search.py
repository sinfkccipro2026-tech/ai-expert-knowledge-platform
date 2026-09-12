"""Semantic Search with RAG"""
from backend.ai_modules.embedding_service import EmbeddingService

class SemanticSearch:
    """Perform semantic search on knowledge base"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def search_knowledge(self, query, knowledge_list, top_k=5):
        """Search knowledge using semantic similarity"""
        query_embedding = self.embedding_service.get_embedding(query)
        
        results = []
        for knowledge in knowledge_list:
            text = knowledge.get('text_content', '') or knowledge.get('summary', '')
            similarities = self.embedding_service.get_similarities(query, [text])
            score = similarities[0][1]
            
            results.append({
                'knowledge_id': knowledge.get('id'),
                'title': knowledge.get('title'),
                'similarity_score': float(score),
                'content': text[:200]
            })
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:top_k]

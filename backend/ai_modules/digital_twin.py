"""AI Digital Twin Engine"""
from backend.ai_modules.semantic_search import SemanticSearch
from backend.ai_modules.nlp_processor import NLPProcessor

class DigitalTwin:
    """AI representation of expert"""
    
    def __init__(self, expert_knowledge):
        self.expert_knowledge = expert_knowledge
        self.semantic_search = SemanticSearch()
        self.nlp = NLPProcessor()
    
    def answer_question(self, question):
        """Answer question using expert knowledge"""
        # Search relevant knowledge
        relevant_knowledge = self.semantic_search.search_knowledge(
            question,
            self.expert_knowledge,
            top_k=3
        )
        
        if not relevant_knowledge:
            return {
                'answer': 'I do not have information about this topic.',
                'confidence': 0.0,
                'sources': []
            }
        
        # Generate answer from top result
        top_result = relevant_knowledge[0]
        answer = f"Based on my knowledge about {top_result['title']}: {top_result['content']}"
        
        return {
            'answer': answer,
            'confidence': float(top_result['similarity_score']),
            'sources': [r['title'] for r in relevant_knowledge]
        }
    
    def get_related_topics(self, topic):
        """Get related topics"""
        results = self.semantic_search.search_knowledge(topic, self.expert_knowledge)
        return [r['title'] for r in results]

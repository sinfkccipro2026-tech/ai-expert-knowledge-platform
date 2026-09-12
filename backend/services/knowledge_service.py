"""Knowledge Management Service"""
from backend.app import db
from backend.models.knowledge import KnowledgeContent
from backend.models.user import Expert
from backend.ai_modules.nlp_processor import NLPProcessor
from datetime import datetime

class KnowledgeService:
    """Handle knowledge content management"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
    
    @staticmethod
    def create_knowledge(expert_id, title, description, content_type, tags, category, difficulty_level, text_content=None):
        """Create new knowledge content"""
        knowledge = KnowledgeContent(
            expert_id=expert_id,
            title=title,
            description=description,
            content_type=content_type,
            tags=tags,
            category=category,
            difficulty_level=difficulty_level,
            text_content=text_content,
            is_published=False
        )
        
        # Generate summary if text content exists
        if text_content:
            knowledge.summary = KnowledgeService.generate_summary(text_content)
            knowledge.key_points = KnowledgeService.extract_key_points(text_content)
        
        db.session.add(knowledge)
        db.session.commit()
        
        return knowledge.to_dict(), 201
    
    @staticmethod
    def get_knowledge(knowledge_id):
        """Get knowledge by ID"""
        knowledge = KnowledgeContent.query.get(knowledge_id)
        if not knowledge:
            return {'error': 'Knowledge not found'}, 404
        return {'knowledge': knowledge.to_dict()}, 200
    
    @staticmethod
    def get_expert_knowledge(expert_id):
        """Get all knowledge by expert"""
        knowledge_list = KnowledgeContent.query.filter_by(expert_id=expert_id).all()
        return {'knowledge': [k.to_dict() for k in knowledge_list]}, 200
    
    @staticmethod
    def publish_knowledge(knowledge_id):
        """Publish knowledge content"""
        knowledge = KnowledgeContent.query.get(knowledge_id)
        if not knowledge:
            return {'error': 'Knowledge not found'}, 404
        
        knowledge.is_published = True
        db.session.commit()
        
        return {'knowledge': knowledge.to_dict()}, 200
    
    @staticmethod
    def search_knowledge(query, category=None, difficulty=None):
        """Search knowledge content"""
        result = KnowledgeContent.query.filter_by(is_published=True)
        
        if category:
            result = result.filter_by(category=category)
        
        if difficulty:
            result = result.filter_by(difficulty_level=difficulty)
        
        knowledge_list = result.all()
        return {'knowledge': [k.to_dict() for k in knowledge_list]}, 200
    
    @staticmethod
    def generate_summary(text):
        """Generate summary from text"""
        sentences = text.split('.')
        summary_sentences = sentences[:min(3, len(sentences))]
        return '. '.join(summary_sentences)
    
    @staticmethod
    def extract_key_points(text):
        """Extract key points from text"""
        nlp = NLPProcessor()
        return nlp.extract_keywords(text, num_keywords=5)
    
    @staticmethod
    def like_knowledge(knowledge_id):
        """Like knowledge content"""
        knowledge = KnowledgeContent.query.get(knowledge_id)
        if not knowledge:
            return {'error': 'Knowledge not found'}, 404
        
        knowledge.likes_count += 1
        db.session.commit()
        
        return {'likes': knowledge.likes_count}, 200
    
    @staticmethod
    def rate_knowledge(knowledge_id, rating):
        """Rate knowledge content"""
        if rating < 1 or rating > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        knowledge = KnowledgeContent.query.get(knowledge_id)
        if not knowledge:
            return {'error': 'Knowledge not found'}, 404
        
        knowledge.rating = rating
        db.session.commit()
        
        return {'rating': knowledge.rating}, 200

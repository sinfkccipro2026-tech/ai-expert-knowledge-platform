"""Knowledge and Content Models"""
from backend.app import db
from datetime import datetime

class KnowledgeContent(db.Model):
    """Knowledge content model"""
    __tablename__ = 'knowledge_content'

    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50), nullable=False)  # document, video, audio, etc.
    file_url = db.Column(db.String(255))
    tags = db.Column(db.JSON)  # List of tags
    category = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    text_content = db.Column(db.LongText)  # Processed text
    summary = db.Column(db.Text)  # AI-generated summary
    key_points = db.Column(db.JSON)  # Key points extracted
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    expert = db.relationship('Expert', backref='knowledge_contents')

    def to_dict(self):
        return {
            'id': self.id,
            'expert_id': self.expert_id,
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type,
            'file_url': self.file_url,
            'tags': self.tags,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'summary': self.summary,
            'key_points': self.key_points,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'rating': self.rating,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat()
        }

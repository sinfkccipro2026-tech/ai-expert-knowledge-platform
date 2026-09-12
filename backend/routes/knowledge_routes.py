"""Knowledge Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User, Expert
from backend.models.knowledge import KnowledgeContent

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('', methods=['GET'])
def get_all_knowledge():
    """Get all published knowledge"""
    knowledge = KnowledgeContent.query.filter_by(is_published=True).all()
    return {'knowledge': [k.to_dict() for k in knowledge]}, 200


@knowledge_bp.route('/<int:knowledge_id>', methods=['GET'])
def get_knowledge(knowledge_id):
    """Get knowledge by ID"""
    knowledge = KnowledgeContent.query.get(knowledge_id)
    if not knowledge or not knowledge.is_published:
        return {'error': 'Knowledge not found'}, 404
    
    knowledge.views_count += 1
    db.session.commit()
    
    return {'knowledge': knowledge.to_dict()}, 200


@knowledge_bp.route('', methods=['POST'])
@jwt_required()
def upload_knowledge():
    """Upload new knowledge content"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'expert':
        return {'error': 'Not authorized'}, 403
    
    expert = Expert.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    
    knowledge = KnowledgeContent(
        expert_id=expert.id,
        title=data.get('title'),
        description=data.get('description'),
        content_type=data.get('content_type', 'document'),
        tags=data.get('tags', []),
        category=data.get('category'),
        difficulty_level=data.get('difficulty_level', 'Beginner'),
        is_published=False
    )
    
    db.session.add(knowledge)
    db.session.commit()
    
    return {'knowledge': knowledge.to_dict()}, 201


@knowledge_bp.route('/<int:knowledge_id>/publish', methods=['PUT'])
@jwt_required()
def publish_knowledge(knowledge_id):
    """Publish knowledge content"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'expert':
        return {'error': 'Not authorized'}, 403
    
    knowledge = KnowledgeContent.query.get(knowledge_id)
    if not knowledge:
        return {'error': 'Knowledge not found'}, 404
    
    if knowledge.expert.user_id != user_id:
        return {'error': 'Not authorized'}, 403
    
    knowledge.is_published = True
    db.session.commit()
    
    return {'knowledge': knowledge.to_dict()}, 200

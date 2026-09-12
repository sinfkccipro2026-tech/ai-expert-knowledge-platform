"""Expert Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User, Expert

expert_bp = Blueprint('experts', __name__)

@expert_bp.route('', methods=['GET'])
def get_experts():
    """Get all experts"""
    experts = Expert.query.all()
    return {'experts': [e.to_dict() for e in experts]}, 200


@expert_bp.route('/<int:expert_id>', methods=['GET'])
def get_expert(expert_id):
    """Get expert by ID"""
    expert = Expert.query.get(expert_id)
    if not expert:
        return {'error': 'Expert not found'}, 404
    return {'expert': expert.to_dict()}, 200


@expert_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_expert_profile():
    """Update expert profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'expert':
        return {'error': 'Not authorized'}, 403
    
    expert = Expert.query.filter_by(user_id=user_id).first()
    if not expert:
        return {'error': 'Expert profile not found'}, 404
    
    data = request.get_json()
    expert.specialization = data.get('specialization', expert.specialization)
    expert.industry = data.get('industry', expert.industry)
    expert.years_of_experience = data.get('years_of_experience', expert.years_of_experience)
    expert.skills = data.get('skills', expert.skills)
    
    db.session.commit()
    return {'expert': expert.to_dict()}, 200


@expert_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_expert_stats():
    """Get expert statistics"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'expert':
        return {'error': 'Not authorized'}, 403
    
    expert = Expert.query.filter_by(user_id=user_id).first()
    
    stats = {
        'students_mentored': expert.students_mentored,
        'total_knowledge': len(expert.knowledge_contents),
        'rating': expert.rating,
        'is_verified': expert.is_verified
    }
    
    return {'stats': stats}, 200

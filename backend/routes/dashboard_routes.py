"""Dashboard Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User, Expert, Student

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/expert', methods=['GET'])
@jwt_required()
def expert_dashboard():
    """Get expert dashboard"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'expert':
        return {'error': 'Not authorized'}, 403
    
    expert = Expert.query.filter_by(user_id=user_id).first()
    
    dashboard = {
        'name': f"{user.first_name} {user.last_name}",
        'students_mentored': expert.students_mentored,
        'rating': expert.rating,
        'verified': expert.is_verified,
        'specialization': expert.specialization
    }
    
    return {'dashboard': dashboard}, 200


@dashboard_bp.route('/student', methods=['GET'])
@jwt_required()
def student_dashboard():
    """Get student dashboard"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return {'error': 'Not authorized'}, 403
    
    student = Student.query.filter_by(user_id=user_id).first()
    
    dashboard = {
        'name': f"{user.first_name} {user.last_name}",
        'learning_hours': student.total_learning_hours,
        'certificates': student.certificates_earned,
        'mentors': len(student.expert_mentors),
        'major': student.major
    }
    
    return {'dashboard': dashboard}, 200

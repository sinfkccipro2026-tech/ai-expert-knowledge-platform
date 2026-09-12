"""Student Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User, Student

student_bp = Blueprint('students', __name__)

@student_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_student_profile():
    """Get student profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return {'error': 'Not authorized'}, 403
    
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {'error': 'Student profile not found'}, 404
    
    return {'student': student.to_dict()}, 200


@student_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_student_profile():
    """Update student profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return {'error': 'Not authorized'}, 403
    
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {'error': 'Student profile not found'}, 404
    
    data = request.get_json()
    student.education_level = data.get('education_level', student.education_level)
    student.major = data.get('major', student.major)
    student.skills = data.get('skills', student.skills)
    student.interests = data.get('interests', student.interests)
    student.career_goals = data.get('career_goals', student.career_goals)
    
    db.session.commit()
    return {'student': student.to_dict()}, 200


@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_student_dashboard():
    """Get student dashboard data"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return {'error': 'Not authorized'}, 403
    
    student = Student.query.filter_by(user_id=user_id).first()
    
    dashboard = {
        'total_learning_hours': student.total_learning_hours,
        'certificates_earned': student.certificates_earned,
        'mentors': len(student.expert_mentors),
        'current_level': student.career_goals
    }
    
    return {'dashboard': dashboard}, 200

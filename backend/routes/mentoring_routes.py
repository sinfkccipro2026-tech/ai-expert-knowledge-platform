"""Mentoring Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User, Expert, Student
from backend.models.mentoring import MentoringRelationship, MentoringSession

mentoring_bp = Blueprint('mentoring', __name__)

@mentoring_bp.route('/request', methods=['POST'])
@jwt_required()
def request_mentoring():
    """Request mentoring from expert"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return {'error': 'Not authorized'}, 403
    
    student = Student.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    expert_id = data.get('expert_id')
    
    expert = Expert.query.get(expert_id)
    if not expert:
        return {'error': 'Expert not found'}, 404
    
    mentoring = MentoringRelationship(
        expert_id=expert_id,
        student_id=student.id,
        learning_goals=data.get('learning_goals', []),
        focus_areas=data.get('focus_areas', [])
    )
    
    db.session.add(mentoring)
    db.session.commit()
    
    return {'mentoring': mentoring.to_dict()}, 201


@mentoring_bp.route('/<int:mentoring_id>', methods=['GET'])
@jwt_required()
def get_mentoring(mentoring_id):
    """Get mentoring relationship details"""
    mentoring = MentoringRelationship.query.get(mentoring_id)
    if not mentoring:
        return {'error': 'Mentoring not found'}, 404
    
    return {'mentoring': mentoring.to_dict()}, 200


@mentoring_bp.route('/<int:mentoring_id>/sessions', methods=['GET'])
def get_mentoring_sessions(mentoring_id):
    """Get all sessions for mentoring relationship"""
    sessions = MentoringSession.query.filter_by(mentoring_id=mentoring_id).all()
    return {'sessions': [s.to_dict() for s in sessions]}, 200


@mentoring_bp.route('/<int:mentoring_id>/sessions', methods=['POST'])
@jwt_required()
def create_mentoring_session(mentoring_id):
    """Create new mentoring session"""
    data = request.get_json()
    
    session = MentoringSession(
        mentoring_id=mentoring_id,
        session_title=data.get('session_title'),
        session_description=data.get('session_description'),
        scheduled_start=data.get('scheduled_start'),
        scheduled_end=data.get('scheduled_end')
    )
    
    db.session.add(session)
    db.session.commit()
    
    return {'session': session.to_dict()}, 201

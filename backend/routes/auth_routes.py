"""Authentication Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User, Expert, Student

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Missing required fields'}, 400
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'User already exists'}, 409
    
    user = User(
        username=data.get('username'),
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        role=data.get('role', 'student')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    if user.role == 'expert':
        expert = Expert(user_id=user.id)
        db.session.add(expert)
    elif user.role == 'student':
        student = Student(user_id=user.id)
        db.session.add(student)
    
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return {'user': user.to_dict(), 'access_token': access_token}, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Missing credentials'}, 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return {'error': 'Invalid credentials'}, 401
    
    access_token = create_access_token(identity=user.id)
    return {'user': user.to_dict(), 'access_token': access_token}, 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return {'user': user.to_dict()}, 200

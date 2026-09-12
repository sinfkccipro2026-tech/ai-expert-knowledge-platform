"""Authentication Service"""
from backend.app import db
from backend.models.user import User, Expert, Student
from flask_jwt_extended import create_access_token

class AuthService:
    """Handle authentication logic"""
    
    @staticmethod
    def register_user(username, email, password, first_name, last_name, role='student'):
        """Register new user"""
        if User.query.filter_by(email=email).first():
            return {'error': 'User already exists'}, 409
        
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create profile based on role
        if role == 'expert':
            expert = Expert(user_id=user.id)
            db.session.add(expert)
        elif role == 'student':
            student = Student(user_id=user.id)
            db.session.add(student)
        
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        return {'user': user.to_dict(), 'access_token': access_token}, 201
    
    @staticmethod
    def login_user(email, password):
        """Login user"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity=user.id)
        return {'user': user.to_dict(), 'access_token': access_token}, 200
    
    @staticmethod
    def verify_token(user_id):
        """Verify if user exists"""
        user = User.query.get(user_id)
        return user is not None
    
    @staticmethod
    def get_user(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        return user.to_dict() if user else None
    
    @staticmethod
    def update_password(user_id, old_password, new_password):
        """Update user password"""
        user = User.query.get(user_id)
        
        if not user or not user.check_password(old_password):
            return {'error': 'Invalid password'}, 401
        
        user.set_password(new_password)
        db.session.commit()
        
        return {'message': 'Password updated'}, 200

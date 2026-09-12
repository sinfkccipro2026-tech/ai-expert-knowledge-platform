"""User Models - Expert and Student"""
from backend.app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    """Base User model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='student')  # expert, student, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active
        }


class Expert(db.Model):
    """Expert profile model"""
    __tablename__ = 'experts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    years_of_experience = db.Column(db.Integer)
    specialization = db.Column(db.String(120))
    industry = db.Column(db.String(120))
    skills = db.Column(db.JSON)  # List of skills
    students_mentored = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='expert_profile')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'years_of_experience': self.years_of_experience,
            'specialization': self.specialization,
            'industry': self.industry,
            'skills': self.skills,
            'students_mentored': self.students_mentored,
            'rating': self.rating,
            'is_verified': self.is_verified
        }


class Student(db.Model):
    """Student profile model"""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    education_level = db.Column(db.String(50))
    major = db.Column(db.String(120))
    skills = db.Column(db.JSON)  # Current skills
    interests = db.Column(db.JSON)  # Career interests
    career_goals = db.Column(db.Text)
    total_learning_hours = db.Column(db.Integer, default=0)
    certificates_earned = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='student_profile')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'education_level': self.education_level,
            'major': self.major,
            'skills': self.skills,
            'interests': self.interests,
            'career_goals': self.career_goals,
            'total_learning_hours': self.total_learning_hours,
            'certificates_earned': self.certificates_earned
        }

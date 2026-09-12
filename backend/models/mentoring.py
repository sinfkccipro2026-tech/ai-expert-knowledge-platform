"""Mentoring and Connection Models"""
from backend.app import db
from datetime import datetime

class MentoringRelationship(db.Model):
    """Mentoring relationship between expert and student"""
    __tablename__ = 'mentoring_relationships'

    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed
    matching_score = db.Column(db.Float)  # AI-based matching score
    learning_goals = db.Column(db.JSON)  # Student's learning goals
    focus_areas = db.Column(db.JSON)  # Areas to focus on
    total_sessions = db.Column(db.Integer, default=0)
    rating_by_student = db.Column(db.Float)  # Student's rating
    rating_by_expert = db.Column(db.Float)  # Expert's rating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    expert = db.relationship('Expert', backref='student_mentorships')
    student = db.relationship('Student', backref='expert_mentors')

    def to_dict(self):
        return {
            'id': self.id,
            'expert_id': self.expert_id,
            'student_id': self.student_id,
            'status': self.status,
            'matching_score': self.matching_score,
            'learning_goals': self.learning_goals,
            'focus_areas': self.focus_areas,
            'total_sessions': self.total_sessions,
            'rating_by_student': self.rating_by_student,
            'rating_by_expert': self.rating_by_expert,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class MentoringSession(db.Model):
    """Individual mentoring session"""
    __tablename__ = 'mentoring_sessions'

    id = db.Column(db.Integer, primary_key=True)
    mentoring_id = db.Column(db.Integer, db.ForeignKey('mentoring_relationships.id'), nullable=False)
    session_title = db.Column(db.String(255))
    session_description = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    scheduled_start = db.Column(db.DateTime)
    scheduled_end = db.Column(db.DateTime)
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    session_notes = db.Column(db.Text)
    learning_outcome = db.Column(db.Text)
    feedback = db.Column(db.Text)
    recording_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mentoring = db.relationship('MentoringRelationship', backref='sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'mentoring_id': self.mentoring_id,
            'session_title': self.session_title,
            'status': self.status,
            'scheduled_start': self.scheduled_start.isoformat() if self.scheduled_start else None,
            'scheduled_end': self.scheduled_end.isoformat() if self.scheduled_end else None,
            'duration_minutes': self.duration_minutes,
            'learning_outcome': self.learning_outcome,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat()
        }

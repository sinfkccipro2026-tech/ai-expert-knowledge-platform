"""Mentor Matching Service"""
from backend.models.user import Expert, Student
from backend.models.mentoring import MentoringRelationship
from backend.app import db
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MentorMatchingService:
    """AI-based mentor matching algorithm"""
    
    @staticmethod
    def calculate_match_score(student, expert):
        """Calculate compatibility score between student and expert"""
        score = 0.0
        
        # Match by skills (30%)
        if student.skills and expert.skills:
            skill_overlap = len(set(student.skills) & set(expert.skills))
            skill_score = (skill_overlap / max(len(set(student.skills) | set(expert.skills)), 1)) * 0.3
            score += skill_score
        
        # Match by interests (25%)
        if student.interests and expert.expertise_areas:
            interest_overlap = len(set(student.interests) & set(expert.expertise_areas or []))
            interest_score = (interest_overlap / max(len(set(student.interests)), 1)) * 0.25
            score += interest_score
        
        # Experience bonus (20%)
        if expert.years_of_experience:
            exp_score = min((expert.years_of_experience / 30) * 0.2, 0.2)
            score += exp_score
        
        # Rating factor (15%)
        rating_score = (expert.rating / 5.0) * 0.15
        score += rating_score
        
        # Availability bonus (10%)
        score += 0.1 if not expert.is_verified else 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    @staticmethod
    def find_top_mentors(student_id, top_k=5):
        """Find top matching mentors for a student"""
        student = Student.query.get(student_id)
        if not student:
            return {'error': 'Student not found'}, 404
        
        # Get all experts
        experts = Expert.query.all()
        
        # Calculate match scores
        matches = []
        for expert in experts:
            score = MentorMatchingService.calculate_match_score(student, expert)
            matches.append({
                'expert_id': expert.id,
                'expert_name': expert.user.first_name + ' ' + expert.user.last_name,
                'specialization': expert.specialization,
                'rating': expert.rating,
                'students_mentored': expert.students_mentored,
                'matching_score': round(score, 3)
            })
        
        # Sort by matching score
        matches.sort(key=lambda x: x['matching_score'], reverse=True)
        
        return {'matches': matches[:top_k]}, 200
    
    @staticmethod
    def request_mentoring(student_id, expert_id, learning_goals=None, focus_areas=None):
        """Create mentoring request"""
        student = Student.query.get(student_id)
        expert = Expert.query.get(expert_id)
        
        if not student or not expert:
            return {'error': 'Student or Expert not found'}, 404
        
        # Check if relationship already exists
        existing = MentoringRelationship.query.filter_by(
            student_id=student_id,
            expert_id=expert_id
        ).first()
        
        if existing:
            return {'error': 'Mentoring relationship already exists'}, 409
        
        # Calculate match score
        match_score = MentorMatchingService.calculate_match_score(student, expert)
        
        mentoring = MentoringRelationship(
            expert_id=expert_id,
            student_id=student_id,
            matching_score=match_score,
            learning_goals=learning_goals or [],
            focus_areas=focus_areas or [],
            status='pending'
        )
        
        db.session.add(mentoring)
        db.session.commit()
        
        return {'mentoring': mentoring.to_dict()}, 201
    
    @staticmethod
    def accept_mentoring_request(mentoring_id):
        """Expert accepts mentoring request"""
        mentoring = MentoringRelationship.query.get(mentoring_id)
        if not mentoring:
            return {'error': 'Mentoring not found'}, 404
        
        mentoring.status = 'active'
        db.session.commit()
        
        return {'mentoring': mentoring.to_dict()}, 200
    
    @staticmethod
    def reject_mentoring_request(mentoring_id):
        """Expert rejects mentoring request"""
        mentoring = MentoringRelationship.query.get(mentoring_id)
        if not mentoring:
            return {'error': 'Mentoring not found'}, 404
        
        mentoring.status = 'cancelled'
        db.session.commit()
        
        return {'message': 'Mentoring request rejected'}, 200
    
    @staticmethod
    def get_student_mentors(student_id):
        """Get all active mentors for a student"""
        mentorships = MentoringRelationship.query.filter_by(
            student_id=student_id,
            status='active'
        ).all()
        
        mentors = []
        for m in mentorships:
            expert = m.expert
            mentors.append({
                'mentor_id': expert.id,
                'name': expert.user.first_name + ' ' + expert.user.last_name,
                'specialization': expert.specialization,
                'rating': expert.rating,
                'matching_score': m.matching_score,
                'sessions': len(m.sessions)
            })
        
        return {'mentors': mentors}, 200
    
    @staticmethod
    def get_expert_students(expert_id):
        """Get all students being mentored by expert"""
        mentorships = MentoringRelationship.query.filter_by(
            expert_id=expert_id,
            status='active'
        ).all()
        
        students = []
        for m in mentorships:
            student = m.student
            students.append({
                'student_id': student.id,
                'name': student.user.first_name + ' ' + student.user.last_name,
                'major': student.major,
                'learning_goals': m.learning_goals,
                'sessions': len(m.sessions)
            })
        
        return {'students': students}, 200

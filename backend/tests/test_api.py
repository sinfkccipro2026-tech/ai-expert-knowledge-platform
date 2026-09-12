"""Test API Endpoints"""
import unittest
import json
from backend.app import app, db
from backend.models.user import User, Expert, Student

class APITestCase(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    # Authentication Tests
    def test_user_registration(self):
        """Test user registration"""
        response = self.app.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'student'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertEqual(data['user']['email'], 'test@example.com')
    
    def test_user_login(self):
        """Test user login"""
        # First register
        self.app.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'first_name': 'Test',
                'last_name': 'User'
            }),
            content_type='application/json'
        )
        
        # Then login
        response = self.app.post('/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        response = self.app.post('/api/auth/login',
            data=json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
    
    # Health Check
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    # Expert Tests
    def test_get_all_experts(self):
        """Test getting all experts"""
        response = self.app.get('/api/experts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('experts', data)
    
    # Knowledge Tests
    def test_get_all_knowledge(self):
        """Test getting all knowledge"""
        response = self.app.get('/api/knowledge')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('knowledge', data)
    
    # Student Dashboard Tests
    def test_student_registration_creates_profile(self):
        """Test that student registration creates profile"""
        with app.app_context():
            response = self.app.post('/api/auth/register',
                data=json.dumps({
                    'username': 'student1',
                    'email': 'student@example.com',
                    'password': 'pass123',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'role': 'student'
                }),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 201)
            
            # Verify student profile was created
            user = User.query.filter_by(email='student@example.com').first()
            self.assertIsNotNone(user.student_profile)
    
    # Expert Registration Tests
    def test_expert_registration_creates_profile(self):
        """Test that expert registration creates profile"""
        with app.app_context():
            response = self.app.post('/api/auth/register',
                data=json.dumps({
                    'username': 'expert1',
                    'email': 'expert@example.com',
                    'password': 'pass123',
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'role': 'expert'
                }),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 201)
            
            # Verify expert profile was created
            user = User.query.filter_by(email='expert@example.com').first()
            self.assertIsNotNone(user.expert_profile)


if __name__ == '__main__':
    unittest.main()

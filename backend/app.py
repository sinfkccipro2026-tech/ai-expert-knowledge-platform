"""Main Flask Application"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:password@localhost:3306/expert_knowledge_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Import models
from backend.models.user import User, Expert, Student
from backend.models.knowledge import KnowledgeContent
from backend.models.mentoring import MentoringRelationship

# Import routes
from backend.routes.auth_routes import auth_bp
from backend.routes.expert_routes import expert_bp
from backend.routes.student_routes import student_bp
from backend.routes.knowledge_routes import knowledge_bp
from backend.routes.mentoring_routes import mentoring_bp
from backend.routes.ai_routes import ai_bp
from backend.routes.dashboard_routes import dashboard_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(expert_bp, url_prefix='/api/experts')
app.register_blueprint(student_bp, url_prefix='/api/students')
app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
app.register_blueprint(mentoring_bp, url_prefix='/api/mentoring')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'healthy'}, 200

@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'error': 'Server error'}, 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

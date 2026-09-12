ai-expert-knowledge-platform/
│
├── backend/                    # Flask Backend
│   ├── app.py                 # Main Flask app
│   ├── config.py              # Configuration
│   ├── requirements.txt
│   │
│   ├── models/
│   │   ├── user.py           # User, Expert, Student
│   │   ├── knowledge.py       # Knowledge content
│   │   └── mentoring.py       # Mentoring relationships
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── expert_routes.py
│   │   ├── student_routes.py
│   │   ├── knowledge_routes.py
│   │   ├── mentoring_routes.py
│   │   ├── ai_routes.py
│   │   └── dashboard_routes.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── knowledge_service.py
│   │   └── mentor_matching.py
│   │
│   ├── ai_modules/
│   │   ├── nlp_processor.py
│   │   ├── embedding_service.py
│   │   ├── semantic_search.py
│   │   ├── speech_processor.py
│   │   └── digital_twin.py
│   │
│   └── tests/
│       └── test_api.py
│
├── frontend/                  # React.js Frontend
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── Login.js
│   │   │   │   └── Signup.js
│   │   │   ├── expert/
│   │   │   │   ├── ExpertDashboard.js
│   │   │   │   └── KnowledgeUpload.js
│   │   │   ├── student/
│   │   │   │   ├── StudentDashboard.js
│   │   │   │   └── LearningPath.js
│   │   │   ├── knowledge/
│   │   │   │   ├── KnowledgeRepository.js
│   │   │   │   └── SearchBar.js
│   │   │   ├── mentoring/
│   │   │   │   ├── MentorMatching.js
│   │   │   │   └── MentoringSession.js
│   │   │   └── ai/
│   │   │       ├── DigitalTwin.js
│   │   │       └── ChatInterface.js
│   │   ├── services/
│   │   │   └── api.js
│   │   └── styles/
│   │       └── App.css
│   └── package.json
│
├── database/
│   └── schema.sql
│
├── docs/
│   ├── README.md
│   ├── API.md
│   ├── SETUP.md
│   └── ARCHITECTURE.md
│
├── .env.example
├── .gitignore
└── README.md

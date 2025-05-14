import unittest
from backend import create_app
from backend.models import db, User, ExerciseLog
from werkzeug.security import generate_password_hash
from datetime import datetime

class TestExerciseRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123'),
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()
        
        # Log in user for tests that require authentication
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id
        
    def tearDown(self):
        """Clean up resources after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_add_exercise_log(self):
        """Test adding a new exercise log through the route"""
        # Log in first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Add exercise log through the route
        response = self.client.post('/exercise_log', data={
            'exercise_type': 'Running',
            'duration': 30,
            'calories': 300,
            'date': datetime.utcnow().strftime('%Y-%m-%d')
        }, follow_redirects=True)
        
        # Verify response status
        self.assertEqual(response.status_code, 200)
        
        # Verify log was added to database
        log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.exercise_type, 'Running')
        self.assertEqual(log.duration, 30)
        self.assertEqual(log.calories, 300)
        
    def test_view_exercise_logs(self):
        """Test viewing exercise logs list"""
        # Log in first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Create some test logs
        log1 = ExerciseLog(
            user_id=self.user.id,
            exercise_type='Running',
            duration=30,
            calories=300,
            date=datetime.utcnow()
        )
        db.session.add(log1)
        db.session.commit()
        
        # Access the logs view
        response = self.client.get('/exercise_log')
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access protected routes"""
        # Create a new client without login
        client = self.app.test_client()
        
        # Try to access a protected route
        response = client.get('/exercise_log', follow_redirects=True)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 200)
        # Check if we're on the login page (implementation dependent)
        self.assertIn(b'id="login-form"', response.data)

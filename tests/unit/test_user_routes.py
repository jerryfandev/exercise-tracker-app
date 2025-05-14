import unittest
import json
from backend import create_app
from backend.models import db, User
from werkzeug.security import generate_password_hash

class TestUserRoutes(unittest.TestCase):
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
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123'),
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
    def tearDown(self):
        """Clean up resources after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_login_success(self):
        """Test successful login with valid credentials"""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['redirect'], '/dashboard')
        
    def test_login_failure(self):
        """Test login failure with invalid credentials"""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        
    def test_register_user(self):
        """Test user registration with valid data"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify user was created in database
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')
        
    def test_duplicate_username(self):
        """Test registration with an existing username"""
        response = self.client.post('/register', data={
            'username': 'testuser',  # Already exists
            'email': 'another@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check response indicates failure (implementation dependent)
        # self.assertIn(b'Username already exists', response.data)
        
        # Verify no new user was created
        users = User.query.filter_by(username='testuser').all()
        self.assertEqual(len(users), 1)  # Still only one user with this username

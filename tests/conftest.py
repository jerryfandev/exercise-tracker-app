import os
import sys
import unittest
from backend import create_app
from backend.models import db, User, ExerciseLog, Achievement

# Set test environment variables
os.environ["FLASK_ENV"] = "testing"

# Create test base class
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def create_test_user(self, username="testuser", email="test@example.com", password="password123"):
        """Create a test user"""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
        
    def login(self, username="testuser", password="password123"):
        """Login as test user"""
        return self.client.post('/main/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

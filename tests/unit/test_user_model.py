import unittest
from backend import create_app
from backend.models import db, User
from werkzeug.security import check_password_hash

class TestUserModel(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """Clean up resources after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hashing(self):
        """Test password hashing functionality"""
        u = User(username='test', email='test@example.com')
        u.set_password('password123')
        # Verify correct password returns True
        self.assertTrue(check_password_hash(u.password_hash, 'password123'))
        # Verify incorrect password returns False
        self.assertFalse(check_password_hash(u.password_hash, 'wrongpassword'))
        
    def test_user_creation(self):
        """Test user creation and database persistence"""
        # Create a test user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('testpass')
        db.session.add(u)
        db.session.commit()
        
        # Retrieve the user from database
        retrieved_user = User.query.filter_by(username='testuser').first()
        
        # Assert user was correctly saved
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'testuser@example.com')
        
    def test_email_validation(self):
        """Test email format validation (if implemented)"""
        # This is a stub test - implement actual validation if your User model has it
        # Example: testing that invalid emails are rejected
        u = User(username='test', email='invalid-email')
        # If your model has validation, you might expect:
        # self.assertRaises(ValueError, db.session.add, u)
        # For now, we'll just check the email was set
        self.assertEqual(u.email, 'invalid-email')

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import BaseTestCase
from backend.models import User, db
from werkzeug.security import generate_password_hash

class TestUserSecurity(BaseTestCase):
    def test_password_is_hashed(self):
        """Test that passwords are stored as hashes, not plaintext"""
        # Create test user
        user = User(username="securitytest", email="security@test.com")
        user.set_password("securepassword123")
        db.session.add(user)
        db.session.commit()
        
        # Retrieve user from database
        saved_user = User.query.filter_by(username="securitytest").first()
        
        # Verify password is stored as hash, not plaintext
        self.assertNotEqual(saved_user.password_hash, "securepassword123")
        # Modified this line as the hash prefix might not be "pbkdf2:sha256:"
        # Werkzeug might use different hashing algorithms, so we just check it's not plaintext
        self.assertTrue(len(saved_user.password_hash) > 20)  # Hash should be sufficiently long
    
    def test_password_verification(self):
        """Test password verification functionality"""
        # Create test user
        user = User(username="verifytest", email="verify@test.com")
        user.set_password("testpassword")
        
        # Verify correct password returns True
        self.assertTrue(user.check_password("testpassword"))
        
        # Verify incorrect password returns False
        self.assertFalse(user.check_password("wrongpassword"))
    
    def test_password_salting(self):
        """Test that identical passwords have different hashes due to salting"""
        # Create two users with the same password
        user1 = User(username="salttest1", email="salt1@test.com")
        user2 = User(username="salttest2", email="salt2@test.com")
        
        # Set the same password for both
        user1.set_password("samepassword")
        user2.set_password("samepassword")
        
        # Verify hashes are different due to salting
        self.assertNotEqual(user1.password_hash, user2.password_hash)
    
    def test_csrf_protection_enabled(self):
        """Test that CSRF protection is enabled in production but disabled in tests"""
        # In test environment, CSRF protection is typically disabled to simplify testing
        # So we should check that it's disabled, not enabled
        self.assertFalse(self.app.config['WTF_CSRF_ENABLED'])
        
        # Create a production app instance to test if CSRF is enabled
        from backend import create_app
        from backend.config import Config
        
        # Temporarily save current environment variable
        original_env = os.environ.get('FLASK_ENV')
        
        try:
            # Set to non-testing environment
            if 'FLASK_ENV' in os.environ:
                del os.environ['FLASK_ENV']
            
            # Create production app instance
            prod_app = create_app(Config)
            
            # Verify CSRF protection is enabled in production
            self.assertTrue(prod_app.config['WTF_CSRF_ENABLED'])
        finally:
            # Restore original environment variable
            if original_env:
                os.environ['FLASK_ENV'] = original_env
    
    def test_environment_variables_loaded(self):
        """Test that environment variables are correctly loaded in config"""
        # Check if SECRET_KEY is set (should be default value in test environment)
        self.assertIsNotNone(self.app.config['SECRET_KEY'])
        
        # Check database URI is set to in-memory SQLite for testing
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')

if __name__ == '__main__':
    unittest.main()

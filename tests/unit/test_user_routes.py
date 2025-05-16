
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import BaseTestCase
from backend.models import User, db

class TestUserRoutes(BaseTestCase):
    def test_register_success(self):
        """Test successful user registration"""
        response = self.client.post('/main/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify user was created in database
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_login_success(self):
        """Test successful login"""
        # Create a user
        self.create_test_user()
        
        # Submit login form
        response = self.client.post('/main/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Verify successful login
        self.assertEqual(response.status_code, 200)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # Create a user
        self.create_test_user()
        
        # Submit login form with wrong password
        response = self.client.post('/main/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        # Verify login failed but page loaded
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test logout functionality"""
        # Create and login a user
        self.create_test_user()
        self.login()
        
        # Logout
        response = self.client.get('/main/logout', follow_redirects=True)
        
        # Verify successful logout (page loads)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_access(self):
        """Test profile page access when logged in"""
        # Create and login a user
        self.create_test_user()
        self.login()
        
        # Access profile page
        response = self.client.get('/main/profile', follow_redirects=True)
        
        # Verify profile page loads
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
        self.assertEqual(len(users), 1)  # Still only one user with this username

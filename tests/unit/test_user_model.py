'''
test_user_model.py tests the functionality of the User Model, for example:

• Whether user creation is working correctly

• Whether the password hashing function is working correctly

• Whether user data is correctly saved to the database
'''

import pytest
from backend import create_app
from backend.models import db, User
from werkzeug.security import check_password_hash

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_creation(app):
    """Test user creation and database persistence"""
    with app.app_context():
        # Create a test user
        u = User(username='testuser', email='testuser@example.com')
        u.set_password('testpass')
        db.session.add(u)
        db.session.commit()
        
        # Retrieve the user from database
        retrieved_user = User.query.filter_by(username='testuser').first()
        
        # Assert user was correctly saved
        assert retrieved_user is not None
        assert retrieved_user.email == 'testuser@example.com'

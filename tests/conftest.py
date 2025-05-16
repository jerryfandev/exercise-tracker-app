import pytest
import os
import warnings # Import the warnings module for filtering warnings 
from backend import create_app
from backend.models import db

'''
Ignore DeprecationWarning such as time stampdatetime.utcnow()
If you want to keep the warnings, remove the following line.
'''
warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture(scope="session", autouse=True)
def app():
    """Create and configure a Flask app for testing."""
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    
    # Create the database and tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()

import pytest
import os
from backend import create_app
from backend.models import db

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
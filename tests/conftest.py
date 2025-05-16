import pytest
import os
import warnings # Import the warnings module for filtering warnings

import sys

# Ensure the backend module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app
from backend.models import db

'''
Ignore DeprecationWarning such as time stampdatetime.utcnow()
If you want to keep the warnings, remove the following line.
'''
warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture(scope="session", autouse=True)

def app():
    """Create and configure a Flask app instance for testing."""
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app

    # Teardown after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

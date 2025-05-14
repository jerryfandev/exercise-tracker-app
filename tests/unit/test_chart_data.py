import unittest
import json
from datetime import datetime, timedelta
from backend import create_app
from backend.models import db, User, ExerciseLog
from werkzeug.security import generate_password_hash

class TestChartData(unittest.TestCase):
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
        
        # Add workout log data for testing charts
        today = datetime.utcnow()
        for i in range(7):
            log = ExerciseLog(
                user_id=self.user.id,
                exercise_type='Running' if i % 2 == 0 else 'Cycling',
                duration=30 + i * 5,
                calories=300 + i * 50,
                date=today - timedelta(days=i)
            )
            db.session.add(log)
        db.session.commit()
        
        # Log in user for tests that require authentication
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
    def tearDown(self):
        """Clean up resources after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_chart_data_endpoint(self):
        """Test chart data API endpoint returns correct structure"""
        response = self.client.get('/charts')
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.data)
        
        # Validate data structures
        self.assertIn('bubble_data', data)
        self.assertTrue(isinstance(data['bubble_data'], list))
        self.assertGreaterEqual(len(data['bubble_data']), 7)  # Should have at least 7 entries
        
        # Validate the format of the first data entry
        first_item = data['bubble_data'][0]
        self.assertIn('x', first_item)  # Date
        self.assertIn('y', first_item)  # Duration
        self.assertIn('r', first_item)  # Calories (radius)
        
    def test_chart_data_filtering(self):
        """Test chart data filtering by date range (if implemented)"""
        # This is a stub test - implement if your API supports date filtering
        # Example: testing chart data for last 3 days
        
        end_date = datetime.utcnow().strftime('%Y-%m-%d')
        start_date = (datetime.utcnow() - timedelta(days=3)).strftime('%Y-%m-%d')
        
        response = self.client.get(f'/charts?start_date={start_date}&end_date={end_date}')
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.data)
        
        # Basic validation that we got some data
        self.assertIn('bubble_data', data)
        
    def test_empty_chart_data(self):
        """Test chart data response when no exercise logs exist"""
        # Create a new user with no logs
        new_user = User(
            username='emptyuser',
            email='empty@example.com',
            password_hash=generate_password_hash('password123'),
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Create a new client and log in as the new user
        client = self.app.test_client()
        client.post('/login', data={
            'username': 'emptyuser',
            'password': 'password123'
        })
        
        # Get chart data for user with no logs
        response = client.get('/charts')
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.data)
        
        # Verify empty data structure
        self.assertIn('bubble_data', data)
        self.assertTrue(all(item['y'] == 0 for item in data['bubble_data']))
        self.assertEqual(data['p7d_cal'], [0, 0, 0, 0, 0, 0, 0])

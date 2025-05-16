import unittest
import sys
import os
import json
from datetime import datetime, timedelta, UTC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import BaseTestCase
from backend.models import User, ExerciseLog, db

class TestChartData(BaseTestCase):
    def setUp(self):
        """Set up test environment"""
        super().setUp()
        # Create test user
        self.user = self.create_test_user()
        self.login()
        
        # Create some exercise logs with different dates
        today = datetime.now(UTC)
        
        # Create logs for the past 5 days
        for i in range(5):
            log_date = today - timedelta(days=i)
            log = ExerciseLog(
                user_id=self.user.id,
                exercise_type='running',
                duration=30 * (i + 1),  # Different durations
                calories=100 * (i + 1),  # Different calories
                date=log_date
            )
            db.session.add(log)
        
        db.session.commit()
    
    def test_chart_data_endpoint(self):
        """Test chart data endpoint returns correct data"""
        # Use the correct endpoint path - 'charts' instead of 'chart_data'
        response = self.client.get('/main/charts')
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains data
        data = json.loads(response.data)
        
        # Check for expected keys in the response
        # Based on the frontend/script/dashboard.js, we expect p7d_labels and p7d_cal
        self.assertIn('p7d_labels', data)
        self.assertIn('p7d_cal', data)
        
        # Verify we have 7 data points (for 7 days)
        self.assertEqual(len(data['p7d_labels']), 7)
        self.assertEqual(len(data['p7d_cal']), 7)
        
        # Check for bubble data which is used in the time chart
        self.assertIn('bubble_data', data)

if __name__ == '__main__':
        self.assertEqual(data['p7d_cal'], [0, 0, 0, 0, 0, 0, 0])

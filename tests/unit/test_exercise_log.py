import unittest
import sys
import os
from datetime import datetime, UTC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import BaseTestCase
from backend.models import User, ExerciseLog, db

class TestExerciseLog(BaseTestCase):
    def setUp(self):
        """Set up test environment"""
        super().setUp()
        # Create test user
        self.user = self.create_test_user()
    
    def test_create_exercise_log(self):
        """Test creating an exercise log"""
        # Create exercise log
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_type='running',
            duration=30,
            calories=300,
            date=datetime.now(UTC)
        )
        db.session.add(log)
        db.session.commit()
        
        # Verify log was created
        retrieved_log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(retrieved_log)
        self.assertEqual(retrieved_log.exercise_type, 'running')
        self.assertEqual(retrieved_log.duration, 30)
        self.assertEqual(retrieved_log.calories, 300)
    
    def test_exercise_log_relationship(self):
        """Test relationship between user and exercise logs"""
        # Create multiple exercise logs
        for i in range(3):
            log = ExerciseLog(
                user_id=self.user.id,
                exercise_type=f'activity{i}',
                duration=30 + i*10,
                calories=300 + i*50,
                date=datetime.now(UTC)
            )
            db.session.add(log)
        
        db.session.commit()
        
        # Verify user has correct number of logs
        logs = ExerciseLog.query.filter_by(user_id=self.user.id).all()
        self.assertEqual(len(logs), 3)
        
        # Verify log attributes
        self.assertEqual(logs[0].exercise_type, 'activity0')
        self.assertEqual(logs[1].exercise_type, 'activity1')
        self.assertEqual(logs[2].exercise_type, 'activity2')

if __name__ == '__main__':
        self.assertEqual(updated_log.calories, 500)

import unittest
from datetime import datetime, timedelta
from backend import create_app
from backend.models import db, User, ExerciseLog

class TestExerciseLog(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
        
    def tearDown(self):
        """Clean up resources after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_create_exercise_log(self):
        """Test creating a basic exercise log entry"""
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_type='Running',
            duration=30,
            calories=300,
            date=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # Verify record was created correctly
        saved_log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(saved_log)
        self.assertEqual(saved_log.exercise_type, 'Running')
        self.assertEqual(saved_log.duration, 30)
        self.assertEqual(saved_log.calories, 300)
        
    def test_retrieve_user_logs(self):
        """Test retrieving all logs for a specific user"""
        # Create multiple logs for the user
        today = datetime.utcnow()
        
        # Create 3 exercise logs with different dates
        for i in range(3):
            log = ExerciseLog(
                user_id=self.user.id,
                exercise_type=f'Activity {i}',
                duration=30 + i * 10,
                calories=200 + i * 50,
                date=today - timedelta(days=i)
            )
            db.session.add(log)
        db.session.commit()
        
        # Retrieve all logs for the user
        user_logs = ExerciseLog.query.filter_by(user_id=self.user.id).all()
        
        # Verify we got all 3 logs
        self.assertEqual(len(user_logs), 3)
        
    def test_update_exercise_log(self):
        """Test updating an existing exercise log"""
        # Create a log
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_type='Cycling',
            duration=45,
            calories=400,
            date=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # Update the log
        log_id = log.id
        saved_log = ExerciseLog.query.get(log_id)
        saved_log.duration = 60
        saved_log.calories = 500
        db.session.commit()
        
        # Verify updates were saved
        updated_log = ExerciseLog.query.get(log_id)
        self.assertEqual(updated_log.duration, 60)
        self.assertEqual(updated_log.calories, 500)

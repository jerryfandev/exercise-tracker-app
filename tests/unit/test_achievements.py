import unittest
import sys
import os
from datetime import datetime, UTC
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import BaseTestCase
from backend.models import User, ExerciseLog, Achievement, db

class TestAchievements(BaseTestCase):
    def setUp(self):
        """Set up test environment"""
        super().setUp()
        # Create test user
        self.user = self.create_test_user()
    
    def test_create_achievement(self):
        """Test creating an achievement"""
        # Create achievement
        achievement = Achievement(
            user_id=self.user.id,
            exercise_type="running",
            description="Completed your first running exercise",
            achieved_at=datetime.now(UTC)
        )
        db.session.add(achievement)
        db.session.commit()
        
        # Verify achievement was created
        retrieved_achievement = Achievement.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(retrieved_achievement)
        self.assertEqual(retrieved_achievement.exercise_type, "running")
        self.assertEqual(retrieved_achievement.description, "Completed your first running exercise")
    
    def test_user_achievements_relationship(self):
        """Test relationship between user and achievements"""
        # Create multiple achievements
        achievements = [
            Achievement(
                user_id=self.user.id,
                exercise_type="running",
                description="Completed your first running exercise",
                achieved_at=datetime.now(UTC)
            ),
            Achievement(
                user_id=self.user.id,
                exercise_type="all",
                description="Burned over 1000 calories in total",
                achieved_at=datetime.now(UTC)
            ),
            Achievement(
                user_id=self.user.id,
                exercise_type="yoga",
                description="Exercised for 5 days in a row",
                achieved_at=datetime.now(UTC)
            )
        ]
        
        for achievement in achievements:
            db.session.add(achievement)
        
        db.session.commit()
        
        # Verify user has correct number of achievements
        achievements_list = Achievement.query.filter_by(user_id=self.user.id).all()
        self.assertEqual(len(achievements_list), 3)
        
        # Verify achievement descriptions
        achievement_descriptions = [a.description for a in achievements_list]
        self.assertIn("Completed your first running exercise", achievement_descriptions)
        self.assertIn("Burned over 1000 calories in total", achievement_descriptions)
        self.assertIn("Exercised for 5 days in a row", achievement_descriptions)
        
        # Verify exercise types
        exercise_types = [a.exercise_type.lower() for a in achievements_list]
        self.assertIn("running", exercise_types)
        self.assertIn("all", exercise_types)
        self.assertIn("yoga", exercise_types)

if __name__ == '__main__':
    unittest.main()

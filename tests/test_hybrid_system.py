import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, patch
from src.api.recommendation_endpoint import HybridRecommendationSystem

class TestHybridSystem(unittest.TestCase):
    def setUp(self):
        # Patching YouTubeService and EmotionDetector before initialization
        self.youtube_patcher = patch('src.api.recommendation_endpoint.YouTubeService')
        self.emotion_patcher = patch('src.api.recommendation_endpoint.EmotionDetector')
        
        self.mock_youtube = self.youtube_patcher.start()
        self.mock_emotion = self.emotion_patcher.start()
        
        # Configure mock return values
        self.mock_youtube.return_value.search_and_enrich.return_value = [
            {
                'video_id': 'v1',
                'title': 'Yoga for Stress',
                'thumbnail': 'http://thumb.jpg',
                'views': 10000,
                'likes': 500,
                'channel_subscribers': 1000,
                'duration_minutes': 15.0,
                'published_days_ago': 10,
                'url': 'http://youtube.com/v1',
                'channel_name': 'YogaChannel'
            },
            {
                'video_id': 'v2',
                'title': 'Calm Breathing',
                'thumbnail': 'http://thumb2.jpg',
                'views': 2000,
                'likes': 100,
                'channel_subscribers': 500,
                'duration_minutes': 10.0,
                'published_days_ago': 20,
                'url': 'http://youtube.com/v2',
                'channel_name': 'CalmChannel'
            }
        ]
        self.mock_youtube.return_value.build_bio_query.return_value = "yoga for stress"
        self.mock_emotion.return_value.predict_emotion.return_value = ("stressed", 0.9, ["stress"])
        
        self.system = HybridRecommendationSystem()

    def tearDown(self):
        self.youtube_patcher.stop()
        self.emotion_patcher.stop()

    def test_flow(self):
        # 1. Get Recommendation
        # Signature: get_recommendations(user_input, user_id, just_ate, hour, max_results, top_n)
        response = self.system.get_recommendations(user_input='I feel stressed', user_id='user1')
        recs = response.get('recommendations', [])
        self.assertTrue(len(recs) > 0)
        
        # 2. Give Feedback
        # Signature: process_feedback(user_id, emotion, category, video_id, feedback, context, video_features)
        vid = recs[0]
        self.system.process_feedback(
            user_id='user1',
            emotion=response['emotion'],
            category='yoga',
            video_id=vid['video_id'],
            feedback='thumbs_up',
            context=vid['_context'],
            video_features=vid['features']
        )
        
        # 3. Check interaction count
        self.assertEqual(self.system.linucb.total_interactions, 1)
        
        # 4. Check user stats
        u_ctx = self.system.context_manager.get_user_context('user1')
        self.assertEqual(u_ctx['interaction_count'], 1)
        # Note: reward is 1.0, so success_rate should be 1.0 (if it was 0 initially)
        # In actual implementation, update_user_context(reward) adds reward to total and increments count.
        # success_rate = interaction_count / total_interactions? No, usually successes / total.
        # Let's check UserContextManager.

if __name__ == '__main__':
    unittest.main()

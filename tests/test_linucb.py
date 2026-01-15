import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rl.linucb_recommender import LinUCBRecommender

class TestLinUCB(unittest.TestCase):
    def setUp(self):
        self.recommender = LinUCBRecommender(context_dim=5, alpha=1.0)
        self.emotion = 'stressed'
        self.category = 'yoga'
        self.user_ctx = {} # Empty dummy

    def test_initialization(self):
        model = self.recommender.get_or_create_model(self.emotion, self.category)
        self.assertTrue(np.array_equal(model.A, np.identity(5)))
        self.assertTrue(np.all(model.b == 0))
        self.assertTrue(np.all(model.theta == 0))

    def test_selection_logic(self):
        # 2 Candidates
        # Candidate 1: features=[1, 0, 0, 0, 0] -> context logic will resize this if we use the helper
        # BUT we injected context_dim=5 manually, helper produces 19.
        # So we must verify IF using helper or raw.
        # The class helper 'build_context_vector' strictly produces 19 dims.
        # So we should use default dim=19 for integration style test.
        
        rec = LinUCBRecommender(context_dim=19)
        c1 = {'id': 'v1', 'features': [1, 1, 1, 1, 1]}
        c2 = {'id': 'v2', 'features': [0, 0, 0, 0, 0]}
        candidates = [c1, c2]
        
        # Initial state: theta=0, so UCB is purely exploration (alpha * sqrt(x A^-1 x))
        # Both have similar covariance (Identity). 
        # Score will be determined by norm of context vector.
        
        sel, scores = rec.select_video(candidates, 'stressed', 'yoga', {})
        self.assertIsNotNone(sel)
        self.assertEqual(len(scores), 2)

    def test_update_learning(self):
        # Manually verify update math
        # d=2 for simplicity
        rec = LinUCBRecommender(context_dim=2)
        model = rec.get_or_create_model('e', 'c')
        
        ctx = np.array([[1], [0]]) # x
        reward = 1.0
        
        rec.update('e', 'c', ctx, reward)
        
        # A should be I + [[1, 0], [0, 0]] = [[2, 0], [0, 1]]
        expected_A = np.array([[2., 0.], [0., 1.]])
        self.assertTrue(np.array_equal(model.A, expected_A))
        
        # b should be 0 + 1 * x = [[1], [0]]
        expected_b = np.array([[1.], [0.]])
        self.assertTrue(np.array_equal(model.b, expected_b))
        
        # Theta = A^-1 b = [[0.5, 0], [0, 1]] @ [[1], [0]] = [[0.5], [0]]
        expected_theta = np.array([[0.5], [0.]])
        self.assertTrue(np.array_equal(model.theta, expected_theta))

if __name__ == '__main__':
    unittest.main()

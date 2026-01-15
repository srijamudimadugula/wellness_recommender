import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.heuristic_ranker import HeuristicRanker

class TestHeuristicRanker(unittest.TestCase):
    def setUp(self):
        self.ranker = HeuristicRanker()
        self.candidates = [
            {'id': 'v1', 'features': [10.0, 0.8, 5000, 300, 1.0]}, # High quality
            {'id': 'v2', 'features': [2.0, 0.1, 10, 60, 0.0]}      # Low quality
        ]

    def test_score(self):
        scores = self.ranker.score(self.candidates)
        self.assertEqual(len(scores), 2)
        self.assertGreater(scores[0], scores[1])

    def test_get_score(self):
        score1 = self.ranker.get_score(self.candidates[0])
        score2 = self.ranker.get_score(self.candidates[1])
        self.assertGreater(score1, score2)

if __name__ == '__main__':
    unittest.main()

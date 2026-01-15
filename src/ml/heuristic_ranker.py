import numpy as np
import logging

class HeuristicRanker:
    """
    Simple baseline ranker using weighted combination of
    normalized popularity and engagement metrics.
    Replaces random stub until LightGBM model is ready.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def score(self, candidates):
        """
        Score a list of candidates based on heuristic logic.
        
        Args:
            candidates: List of dicts, each containing 'features'
                        Features expected: [views, engagement, subscribers, duration, recency]
                        
        Returns:
            List of float scores (0.0 to 1.0)
        """
        scores = []
        for vid in candidates:
            feats = vid.get('features', [])
            if len(feats) < 2:
                scores.append(0.5) # Default neutral score
                continue

            # Heuristic: 0.5 * normalized_views + 0.5 * engagement_ratio
            # Assuming feats[0] is log_views (0-10 range typically)
            # Assuming feats[1] is engagement_ratio (0-1 range)
            
            # Normalize log_views roughly to 0-1 (assuming max log_view ~ 15)
            # Note: In production, use the FeatureNormalizer for strict bounds.
            # Here we just want a rough signal.
            
            norm_views = min(feats[0] / 15.0, 1.0)
            engagement = min(max(feats[1], 0.0), 1.0)
            
            score = 0.5 * norm_views + 0.5 * engagement
            scores.append(score)
            
        return scores

    def get_score(self, vid: dict) -> float:
        """Calculate score for a single candidate."""
        feats = vid.get('features', [])
        if len(feats) < 2:
            return 0.5
        norm_views = min(feats[0] / 15.0, 1.0)
        engagement = min(max(feats[1], 0.0), 1.0)
        return 0.5 * norm_views + 0.5 * engagement

import logging
import numpy as np
from src.ml.heuristic_ranker import HeuristicRanker
from src.rl.linucb_recommender import LinUCBRecommender
from src.api.user_context_manager import UserContextManager
from src.ml.feature_normalizer import FeatureNormalizer
from src.ml.emotion_detector import EmotionDetector
from src.api.youtube_service import YouTubeService
from src.api.mock_youtube_service import MockYouTubeService

logger = logging.getLogger(__name__)

class HybridRecommendationSystem:
    def __init__(self, use_mock_youtube=False):
        """
        Initialize complete recommendation system with real or mock YouTube service.
        Automatically checks for YOUTUBE_API_KEY env var.
        """
        import os
        api_key = os.environ.get('YOUTUBE_API_KEY')
        
        # Fallback to mock if explicitly requested OR if no API key present
        if use_mock_youtube or not api_key:
            self.youtube = MockYouTubeService()
            mode = "Mock (Explicit)" if use_mock_youtube else "Mock (Fallback - No API Key)"
            logger.info(f"Using {mode} YouTubeService")
        else:
            self.youtube = YouTubeService()
            logger.info("Using real YouTubeService")
        
        self.emotion_detector = EmotionDetector()
        
        # ML components
        self.feature_normalizer = FeatureNormalizer()
        self.linucb = LinUCBRecommender(context_dim=19, alpha=1.0)
        self.context_manager = UserContextManager()
        self.heuristic_ranker = HeuristicRanker()
        
        # Load saved models
        try:
            self.linucb.load('./models/linucb_models.pkl')
            logger.info("Loaded existing LinUCB models")
        except FileNotFoundError:
            logger.info("Starting with fresh LinUCB models")

    def get_recommendations(self, 
                           user_input: str = "",
                           user_id: str = "seeker_01",
                           emotion: str = None,
                           candidates: list = None,
                           just_ate: bool = False,
                           hour: int = None,
                           max_results: int = 12, top_n: int = 4) -> dict:
        """
        Orchestrated pipeline with Bio-Context: NLP Detector -> Bio-Search -> Hybrid scoring.
        Allows manual emotion/candidate injection for testing/advanced flows.
        """
        # 1. Biological Context (Cloud-ready: Use injected hour or fallback to system)
        from datetime import datetime
        if hour is None:
            hour = datetime.now().hour
        if 5 <= hour < 11:
            phase = "morning"
        elif 11 <= hour < 16:
            phase = "midday"
        elif 16 <= hour < 19:
            phase = "afternoon"
        else:
            phase = "evening"
            
        # 2. Detect Emotion & Keywords (Unified NLP Bridge)
        confidence = 1.0
        keywords = []
        
        if emotion:
             system_emotion = emotion
             logger.info(f"Using provided emotion: {system_emotion}")
        else:
            system_emotion, confidence, keywords = self.emotion_detector.predict_emotion(user_input)
            
        logger.info(f"NLP: {system_emotion} | Phase: {phase} | Food Safety: {just_ate}")
        
        # 3. Search YouTube (Expanded with Keywords & Bio-Context)
        if candidates is not None:
             logger.info(f"Using {len(candidates)} provided candidates")
        else:
            query = self.youtube.build_bio_query(system_emotion, phase, just_ate, keywords)
            candidates = self.youtube.search_and_enrich(query, max_results=max_results)
        
        if not candidates:
            return {"emotion": system_emotion, "phase": phase, "recommendations": []}

        # 4. Scoring & Normalization
        user_ctx = self.context_manager.get_user_context(user_id)
        scored_vids = []
        
        # Prepare candidates
        processed_candidates = self._prepare_candidates(candidates)
        
        for vid in processed_candidates:
            # RL Context Vector (d=19, stable)
            ctx_vec = self.linucb.build_context_vector(system_emotion, 'yoga', vid['features'], user_ctx)
            
            # Hybrid Calculation
            rl_score, _ = self.linucb.get_ucb_score(system_emotion, 'yoga', ctx_vec)
            h_score = self.heuristic_ranker.get_score(vid)
            
            # Dynamic weighting: max 0.7 RL influence
            w = min(user_ctx.get('interaction_count', 0) / 20.0, 0.7)
            final_raw_score = (w * rl_score) + ((1 - w) * h_score) + vid.get('demo_boost', 0.0)
            
            # Sigmoid normalization
            match_percent = 1 / (1 + np.exp(-final_raw_score))
            
            vid.update({
                'match_score': round(float(match_percent * 100), 1),
                'score': float(final_raw_score),
                '_context': ctx_vec,
                'heuristic_score': float(h_score),
                'linucb_score': float(rl_score)
            })
            scored_vids.append(vid)

        return {
            "emotion": system_emotion,
            "confidence": confidence,
            "phase": phase,
            "just_ate": just_ate,
            "keywords": keywords,
            "recommendations": sorted(scored_vids, key=lambda x: x['score'], reverse=True)[:top_n],
            "metadata": {
                "w_rl": w,
                "user_id": user_id,
                "total_candidates": len(candidates)
            }
        }

    def _prepare_candidates(self, videos: list) -> list:
        """
        Transform YouTube video data into candidate format with normalized features.
        """
        prepared = []
        
        for video in videos:
            try:
                # Extract raw features
                views = video.get('views', 0)
                likes = video.get('likes', 0)
                subscribers = video.get('channel_subscribers', 0)
                duration = video.get('duration_minutes', 15.0)
                days_ago = video.get('published_days_ago', 180)
                
                # Compute features
                log_views = np.log1p(views)
                engagement = likes / max(views, 1)
                log_subs = np.log1p(subscribers)
                duration_norm = min(duration / 30.0, 1.0)  # Cap at 1.0
                recency = 1.0 / (days_ago + 1)
                
                # Create raw feature vector
                raw_features = np.array([
                    log_views,
                    engagement,
                    log_subs,
                    duration_norm,
                    recency
                ])
                
                # Normalize (or fit if first time)
                if not self.feature_normalizer.is_fitted:
                    # Collect all features first
                    all_raw = []
                    for v in videos:
                        try:
                            vw = v.get('views', 0)
                            lk = v.get('likes', 0)
                            sb = v.get('channel_subscribers', 0)
                            dr = v.get('duration_minutes', 15.0)
                            da = v.get('published_days_ago', 180)
                            
                            all_raw.append([
                                np.log1p(vw),
                                lk / max(vw, 1),
                                np.log1p(sb),
                                min(dr / 30.0, 1.0),
                                1.0 / (da + 1)
                            ])
                        except:
                            continue
                    
                    if all_raw:
                        self.feature_normalizer.fit(np.array(all_raw))
                        logger.info("Fitted feature normalizer on batch")
                
                # Transform features
                normalized_features = self.feature_normalizer.transform(raw_features)
                
                # Add to video dict
                video['features'] = normalized_features
                prepared.append(video)
                
            except Exception as e:
                logger.warning(f"Failed to process video {video.get('video_id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Prepared {len(prepared)} valid candidates")
        return prepared

    def _get_linucb_weight(self):
        """Determine weighting for hybrid ranking based on system maturity."""
        n_interactions = self.linucb.total_interactions
        if n_interactions < 50:
            return 0.2
        elif n_interactions < 200:
            return 0.5
        else:
            return 0.8
            
    def _hybrid_score_and_select(self, candidates, emotion, category, user_ctx, top_n):
        """Score candidates using Heuristic and LinUCB"""
        # 1. Score Heuristically (Quality)
        h_scores = self.heuristic_ranker.score(candidates)
        
        # 2. Score RL (Personalization)
        rl_scores = []
        for cand in candidates:
            ctx_vector = self.linucb.build_context_vector(emotion, category, cand['features'], user_ctx)
            score, _ = self.linucb.get_ucb_score(emotion, category, ctx_vector)
            rl_scores.append(score)
            
        # 3. Hybrid Weighing
        w_rl = self._get_linucb_weight()
        
        final_scores = []
        for i, (h, rl) in enumerate(zip(h_scores, rl_scores)):
            raw_score = w_rl * rl + (1 - w_rl) * h
            
            # Implementation: Sigmoid function to normalize 0-100%
            # Center it around typical score values if needed, otherwise standard sigmoid
            sigmoid_score = 1 / (1 + np.exp(-raw_score))
            match_pct = int(sigmoid_score * 100)
            
            final_scores.append(raw_score)
            candidates[i]['score'] = raw_score
            candidates[i]['match_score'] = match_pct
            candidates[i]['heuristic_score'] = h
            candidates[i]['linucb_score'] = rl
            candidates[i]['_context'] = user_ctx # Keep context for feedback
            
        # 4. Sort and Return
        ranked_indices = np.argsort(final_scores)[::-1]
        top_recs = [candidates[i] for i in ranked_indices[:top_n]]
        
        return top_recs

    def process_feedback(self, user_id, emotion, category, video_id, feedback, context=None, video_features=None):
        """
        Process user feedback.
        """
        # Map feedback
        if feedback == 'thumbs_up':
            reward = 1.0
        elif feedback == 'thumbs_down':
            reward = -1.0
        else:
            return {'status': 'ignored'}
            
        self.context_manager.update_user_context(user_id, reward)
        
        # Update LinUCB if features available
        if video_features is not None and context is not None:
             if isinstance(context, np.ndarray):
                 ctx_vector = context
             else:
                 ctx_vector = self.linucb.build_context_vector(emotion, category, video_features, context)
             self.linucb.update(emotion, category, ctx_vector, reward)
        
        return {
            'status': 'success',
            'reward': reward,
            'total_interactions': self.linucb.total_interactions,
            'linucb_weight': self._get_linucb_weight()
        }

    def detect_emotion_and_context(self, text):
        return self.emotion_detector.predict_emotion(text)

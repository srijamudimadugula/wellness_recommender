import numpy as np
import pickle
import os
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LinUCBModel:
    A: np.ndarray  # Design matrix
    b: np.ndarray  # Reward vector
    theta: np.ndarray  # Weights
    interaction_count: int = 0

class LinUCBRecommender:
    def __init__(self, context_dim: int = 19, alpha: float = 1.0):
        self.context_dim = context_dim
        self.alpha = alpha
        self.models: Dict[str, LinUCBModel] = {}
        self.total_interactions = 0
        
    def _get_key(self, emotion: str, category: str) -> str:
        return f"{emotion}_{category}"
        
    def _init_model(self) -> LinUCBModel:
        return LinUCBModel(
            A=np.identity(self.context_dim),
            b=np.zeros((self.context_dim, 1)),
            theta=np.zeros((self.context_dim, 1)),
            interaction_count=0
        )
        
    def get_or_create_model(self, emotion, category) -> LinUCBModel:
        key = self._get_key(emotion, category)
        if key not in self.models:
            self.models[key] = self._init_model()
        return self.models[key]

    def build_context_vector(self, emotion, category, video_features, user_context_dict):
        """Construct the 19-dim context vector."""
        # Emotion (7)
        emotions = ['stressed', 'sad', 'happy', 'anxious', 'tired', 'motivated', 'calm']
        emotion_vec = np.zeros(7)
        if emotion in emotions:
            emotion_vec[emotions.index(emotion)] = 1.0
        else:
            emotion_vec[6] = 1.0 # Default calm

        # Category (4)
        categories = ['exercise', 'yoga', 'meditation', 'reading']
        cat_vec = np.zeros(4)
        if category in categories:
            cat_vec[categories.index(category)] = 1.0
        else:
            cat_vec[1] = 1.0 # Default yoga
            
        # Video Features (5) - Expected to be normalized
        vid_vec = np.array(video_features[:5])
        
        # User Context (3)
        user_vec = np.array([
            user_context_dict.get('avg_feedback', 0.0),
            min(user_context_dict.get('interaction_count', 0) / 100.0, 1.0), # Normalize cap
            user_context_dict.get('success_rate', 0.0)
        ])
        
        context = np.concatenate([emotion_vec, cat_vec, vid_vec, user_vec])
        return context.reshape(-1, 1)

    def select_video(self, candidates, emotion, category, user_context) -> Tuple[Dict, List[float]]:
        model = self.get_or_create_model(emotion, category)
        A_inv = np.linalg.inv(model.A)
        
        ucb_scores = []
        best_score = -float('inf')
        selected_vid = None
        
        for vid in candidates:
            # Context
            ctx = self.build_context_vector(emotion, category, vid['features'], user_context)
            
            # UCB
            mean = (model.theta.T @ ctx).item()
            confidence = self.alpha * np.sqrt((ctx.T @ A_inv @ ctx).item())
            score = mean + confidence
            ucb_scores.append(score)
            
            # Store context temporarily for update convenience if this vid is chosen
            # Note: In real app, we usually recompute or cache by request_id
            vid['_temp_context'] = ctx
            
            if score > best_score:
                best_score = score
                selected_vid = vid
                
        return selected_vid, ucb_scores

    def get_ucb_score(self, emotion, category, context_vector) -> Tuple[float, float]:
        """Calculate UCB score with numerical stability fixes."""
        model = self.get_or_create_model(emotion, category)
        
        # NUMERICAL STABILITY: Use pinv for robust inversion
        A_inv = np.linalg.pinv(model.A)
        
        mean = (model.theta.T @ context_vector).item()
        
        # Exploration bonus with variance check
        var = context_vector.T @ A_inv @ context_vector
        uncertainty = self.alpha * np.sqrt(np.maximum(0, var.item()))
        
        return mean + uncertainty, uncertainty

    def update(self, emotion, category, context, reward):
        model = self.get_or_create_model(emotion, category)
        
        # LinUCB Update
        model.A += context @ context.T
        model.b += reward * context
        
        # NUMERICAL STABILITY: Use solve instead of direct inverse
        model.theta = np.linalg.solve(model.A, model.b)
        
        model.interaction_count += 1
        self.total_interactions += 1
        
        # Decay alpha
        if self.total_interactions > 100:
            self.alpha = max(0.1, self.alpha * 0.999)

    def save(self, path='./models/linucb_models.pkl'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            'models': self.models,
            'total_interactions': self.total_interactions,
            'alpha': self.alpha
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
            
    def load(self, path='./models/linucb_models.pkl'):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
            self.models = data['models']
            self.total_interactions = data['total_interactions']
            self.alpha = data['alpha']

    def get_statistics(self) -> Dict:
        """Return internal statistics for monitoring."""
        models_info = {}
        for key, model in self.models.items():
            models_info[key] = {
                'interactions': model.interaction_count,
                'weight_norm': np.linalg.norm(model.theta)
            }
            
        return {
            'total_interactions': self.total_interactions,
            'models_trained': len(self.models),
            'current_alpha': self.alpha,
            'model_details': models_info
        }

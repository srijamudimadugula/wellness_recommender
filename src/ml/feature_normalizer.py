import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import os

class FeatureNormalizer:
    def __init__(self, feature_dim=5):
        self.scaler = StandardScaler()
        self.feature_dim = feature_dim
        self.is_fitted = False

    def fit(self, features_matrix):
        """
        Fit the scaler on a corpus of video features.
        Args:
            features_matrix: np.ndarray of shape (n_samples, feature_dim)
        """
        if features_matrix.shape[1] != self.feature_dim:
            raise ValueError(f"Expected {self.feature_dim} features, got {features_matrix.shape[1]}")
        
        self.scaler.fit(features_matrix)
        self.is_fitted = True

    def transform(self, features_vector):
        """
        Normalize a single feature vector or batch.
        """
        if not self.is_fitted:
            # Fallback for cold start if not fitted: return as is or zero-mean roughly
            return np.array(features_vector)
            
        features_vector = np.array(features_vector)
        if features_vector.ndim == 1:
            features_vector = features_vector.reshape(1, -1)
            
        return self.scaler.transform(features_vector).flatten()

    def save(self, filepath='./models/feature_normalizer.pkl'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.scaler, f)

    def load(self, filepath='./models/feature_normalizer.pkl'):
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.scaler = pickle.load(f)
            self.is_fitted = True

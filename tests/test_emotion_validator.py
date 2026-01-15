import pytest
from src.ml.emotion_validator import EmotionValidator

class TestEmotionValidator:
    @pytest.fixture
    def validator(self):
        return EmotionValidator()

    def test_low_confidence_defaults_to_calm(self, validator):
        """Rule 1: Low confidence should default to calm"""
        emotion, conf = validator.validate("I am okay", "happy", 0.4, [])
        assert emotion == "calm"
        assert conf == 0.60

    def test_stress_keyword_override(self, validator):
        """Rule 2: Stress keywords should override other emotions"""
        text = "I feel overwhelmed with finals"
        emotion, conf = validator.validate(text, "sad", 0.65, [])
        assert emotion == "stressed"
        assert conf >= 0.75

    def test_neutral_phrase_detection(self, validator):
        """Rule 3: Neutral phrases should override to calm"""
        text = "Just a normal day, nothing special"
        emotion, conf = validator.validate(text, "happy", 0.9, [])
        assert emotion == "calm"
        assert conf == 0.80

    def test_anxiety_keyword_validation(self, validator):
        """Rule 4: Anxiety keywords should map to anxious"""
        text = "I am so scared of the results"
        emotion, conf = validator.validate(text, "fear", 0.8, [])
        assert emotion == "anxious" # 'scared' is in anxiety keywords
        
        text2 = "I am really worried"
        emotion2, conf2 = validator.validate(text2, "sad", 0.7, [])
        assert emotion2 == "anxious"

    def test_anger_false_positive_correction(self, validator):
        """Rule 5: Angry prediction without keywords should be downgraded"""
        # Case 1: No anger keywords, no stress keywords -> Calm
        text = "I am going to the store"
        emotion, conf = validator.validate(text, "angry", 0.8, [])
        assert emotion == "calm"
        assert conf == 0.65

        # Case 2: No anger keywords, but stress keywords -> Stressed
        text_stress = "I have a lot of pressure"
        emotion_s, conf_s = validator.validate(text_stress, "angry", 0.8, [])
        assert emotion_s == "stressed"
        assert conf_s == 0.80

    def test_happy_validation_sarcasm(self, validator):
        """Rule 6: Happy with sarcasm indicators should be sad/negated"""
        text = "I passed, but unfortunately I failed the other one"
        emotion, conf = validator.validate(text, "happy", 0.95, [])
        assert emotion == "sad"
        assert conf == 0.70

    def test_sadness_vs_stress_differentiation(self, validator):
        """Rule 7: Sadness with stress keywords should be stressed"""
        text = "I am sad because of the deadline"
        emotion, conf = validator.validate(text, "sad", 0.85, [])
        assert emotion == "stressed"
        assert conf == 0.85

    def test_high_confidence_preservation(self, validator):
        """Validation should not override valid high confidence predictions"""
        text = "I am absolutely Joyful and Thrilled!"
        emotion, conf = validator.validate(text, "happy", 0.95, [])
        assert emotion == "happy"
        assert conf == 0.95

    def test_keyword_boundary_matching(self, validator):
        """Test regex word boundaries"""
        # "mad" should not match "made"
        text = "I made a cake"
        emotion, conf = validator.validate(text, "angry", 0.8, []) 
        # If "mad" matched "made", and predicted was angry, it would keep angry.
        # But since "mad" should NOT match "made", it should fall through to Rule 5 (False positive anger) -> calm
        assert emotion == "calm" 

    def test_empty_input(self, validator):
        """Test empty input handling"""
        emotion, conf = validator.validate("", "calm", 0.5, [])
        assert emotion == "calm"


import re
import logging

logger = logging.getLogger(__name__)

class EmotionValidator:
    """
    Post-processing validation layer for emotion predictions.
    Catches model errors using keyword matching and confidence analysis.
    """
    
    def __init__(self):
        # Define keyword dictionaries for each emotion
        # Using word boundaries for more accurate matching
        self.stress_keywords = ['overwhelmed', 'stressed', 'pressure', 'exam', 'finals', 
                              'deadline', 'coursework', 'workload', 'busy', 'tired', 'exhausted']
        self.neutral_phrases = ['normal day', 'nothing special', 'okay', 'fine', 
                              'alright', 'regular', 'typical', 'nothing much']
        self.anxiety_keywords = ['worried', 'scared', 'nervous', 'afraid', 
                               'terrified', 'anxious', 'fear', 'panic']
        self.anger_keywords = ['furious', 'mad', 'hate', 'betrayed', 'angry', 
                             'rage', 'pissed', 'annoyed']
        self.sadness_keywords = ['sad', 'depressed', 'down', 'miserable', 'upset', 
                               'crying', 'heartbroken', 'devastated', 'hopeless']
        self.happy_keywords = ['excited', 'joyful', 'thrilled', 'amazing', 
                             'wonderful', 'great', 'fantastic', 'love', 'happy', 'good']
        self.sarcasm_indicators = ['but', 'however', 'unfortunately', 'sadly']
        
        # Compile regex patterns for optimization
        self.patterns = {
            'stress': self._compile_pattern(self.stress_keywords),
            'neutral': self._compile_pattern(self.neutral_phrases),
            'anxiety': self._compile_pattern(self.anxiety_keywords),
            'anger': self._compile_pattern(self.anger_keywords),
            'sadness': self._compile_pattern(self.sadness_keywords),
            'happy': self._compile_pattern(self.happy_keywords),
            'sarcasm': self._compile_pattern(self.sarcasm_indicators)
        }

    def _compile_pattern(self, keywords):
        """Create a compiled regex pattern for a list of keywords with word boundaries."""
        # Escape keywords just in case, though mostly alphanumeric
        escaped_keywords = [re.escape(k) for k in keywords]
        pattern_str = r'\b(' + '|'.join(escaped_keywords) + r')\b'
        return re.compile(pattern_str, re.IGNORECASE)

    def validate(self, text: str, predicted_emotion: str, 
                 confidence: float, keywords: list) -> tuple[str, float]:
        """
        Validate and correct emotion prediction.
        
        Args:
            text: Original user input
            predicted_emotion: Raw model prediction
            confidence: Model confidence score (0-1)
            keywords: Extracted keywords from KeyBERT (unused in logic but kept for interface consistency)
        
        Returns:
            (validated_emotion, validated_confidence)
        """
        if not text:
            return predicted_emotion, confidence
            
        text_lower = text.lower()
        
        # Rule 1: Stress detection override (High Priority)
        # Moved before confidence check to catch "overwhelmed" even if model is uncertain
        if self._has_match('stress', text_lower):
            if predicted_emotion not in ['stressed', 'anxious']:
                return 'stressed', max(confidence, 0.75)

        # Rule 2: Very low confidence -> default to calm
        if confidence < 0.6:
            return 'calm', 0.60
        
        # Rule 3: Neutral language detection
        if self._has_match('neutral', text_lower):
             # If it's explicitly neutral, override happy/sad/etc. 
            return 'calm', 0.80
        
        # Rule 4: Anxiety validation
        if self._has_match('anxiety', text_lower):
            if predicted_emotion != 'anxious':
                return 'anxious', max(confidence, 0.75)
        
        # Rule 5: Anger validation
        if predicted_emotion == 'angry':
            if not self._has_match('anger', text_lower):
                # False positive - likely calm or stressed
                if self._has_match('stress', text_lower):
                    return 'stressed', 0.70
                return 'calm', 0.65
            else:
                # True positive anger, but check for context switch ("but mostly tired")
                if self._has_match('sarcasm', text_lower) and self._has_match('stress', text_lower):
                    return 'stressed', 0.75
        
        # Rule 6: Happy validation (catch false positives)
        if predicted_emotion == 'happy':
            # Check for sarcasm or negative context
            if self._has_match('sarcasm', text_lower):
                return 'sad', 0.70
            # Check if text is actually neutral (redundant with Rule 3 but good for safety)
            if self._has_match('neutral', text_lower):
                return 'calm', 0.75
        
        # Rule 7: Sadness vs Stress differentiation
        if predicted_emotion == 'sad':
            if self._has_match('stress', text_lower):
                return 'stressed', confidence
        
        # No override needed
        return predicted_emotion, confidence
    
    def _has_match(self, category: str, text: str) -> bool:
        """Check if any keywords present in text using compiled regex"""
        return bool(self.patterns[category].search(text))

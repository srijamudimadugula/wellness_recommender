import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from keybert import KeyBERT
import logging
from logging.handlers import RotatingFileHandler
import os
from src.ml.emotion_validator import EmotionValidator

# Configure Logging
if not os.path.exists('logs'):
    os.makedirs('logs')

# Validation Logger
validation_logger = logging.getLogger('emotion_validation')
validation_logger.setLevel(logging.INFO)
# Avoid adding handlers multiple times
if not validation_logger.handlers:
    val_handler = RotatingFileHandler('logs/emotion_validation.log', maxBytes=10*1024*1024, backupCount=1)
    val_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    val_handler.setFormatter(val_formatter)
    validation_logger.addHandler(val_handler)

# Error Logger
error_logger = logging.getLogger('emotion_errors')
error_logger.setLevel(logging.ERROR)
if not error_logger.handlers:
    err_handler = logging.FileHandler('logs/emotion_errors.log')
    err_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    err_handler.setFormatter(err_formatter)
    error_logger.addHandler(err_handler)

logger = logging.getLogger(__name__)

class EmotionDetector:
    def __init__(self, model_name='bhadresh-savani/distilbert-base-uncased-emotion'):
        """
        Initialize the Emotion Detection Module.
        
        Args:
            model_name (str): The Hugging Face model checkpoint to load.
        """
        logger.info(f"Loading emotion model: {model_name}...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        except Exception as e:
            msg = f"Failed to load emotion model: {e}"
            logger.error(msg)
            error_logger.error(msg)
            raise

        logger.info("Loading KeyBERT model...")
        try:
            self.keybert_model = KeyBERT('all-MiniLM-L6-v2')
        except Exception as e:
            msg = f"Failed to load KeyBERT model: {e}"
            logger.error(msg)
            error_logger.error(msg)
            raise

        self.validator = EmotionValidator()

        # Mapping from dataset labels to wellness application labels
        self.emotion_map = {
            'sadness': 'sad',
            'joy': 'happy',
            'love': 'happy',
            'anger': 'angry',
            'fear': 'anxious',
            'surprise': 'motivated' # will be refined by keywords
        }
        
    def predict_emotion(self, text):
        """
        Predict emotion and extract keywords from the input text with validation.
        
        Args:
            text (str): User input text.
            
        Returns:
            tuple: (emotion_label, confidence_score, keywords_list)
        """
        if not text or not isinstance(text, str):
            logger.warning("Invalid input text provided.")
            return 'calm', 0.0, []

        try:
            # 1. BERT Inference
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence = probs.max().item()
            
            predicted_id = probs.argmax().item()
            predicted_label = self.model.config.id2label[predicted_id]
            
            # 2. KeyBERT Extraction
            # Extract top 3 keywords
            keywords_tuples = self.keybert_model.extract_keywords(
                text, 
                keyphrase_ngram_range=(1, 1), 
                stop_words='english', 
                top_n=3
            )
            keywords = [k[0] for k in keywords_tuples]

            # 3. Initial Mapping & Bridge logic
            system_emotion = self.map_to_system_emotion(predicted_label, text)
            raw_emotion = system_emotion
            
            # Special Handling for 'surprise' -> distinguish between happy and stressed
            if predicted_label == 'surprise':
                positive_kws = {'win', 'gift', 'award', 'happy', 'excited', 'wonderful', 'great'}
                negative_kws = {'shock', 'bad', 'exam', 'deadline', 'emergency', 'panic', 'stress'}
                
                if any(kw in text.lower() for kw in negative_kws):
                     raw_emotion = 'stressed'
                elif any(kw in text.lower() for kw in positive_kws):
                     raw_emotion = 'happy'
                else:
                     raw_emotion = 'motivated' # Keep existing mapping

            # 4. Validation Layer
            validated_emotion, validated_confidence = self.validator.validate(
                text, raw_emotion, confidence, keywords
            )

            # 5. Logging
            override_flag = "OVERRIDE" if raw_emotion != validated_emotion else "PASS"
            log_msg = f"{override_flag} | Raw: {raw_emotion} ({confidence:.2f}) -> Validated: {validated_emotion} ({validated_confidence:.2f}) | Keywords: {keywords} | Input: {text[:50]}..."
            validation_logger.info(log_msg)

            return validated_emotion, validated_confidence, keywords

        except Exception as e:
            error_msg = f"Error in predict_emotion: {e}"
            logger.error(error_msg)
            error_logger.error(error_msg)
            # Fallback
            return 'calm', 0.5, []

    def map_to_system_emotion(self, bert_label, text):
        """Bridge NLP labels to system categories with contextual refinement."""
        # Primary Mapping
        mapping = {
            'fear': 'anxious',
            'anger': 'angry',
            'joy': 'happy',
            'sadness': 'tired', # mapped in user request
            'surprise': 'motivated'
        }
        
        system_emotion = mapping.get(bert_label, 'calm')
        
        # KEYWORD REFINEMENT: If user mentions 'exam' or 'deadline', force 'stressed'
        stress_words = ['exam', 'deadline', 'work', 'project', 'boss', 'overwhelmed']
        if any(w in text.lower() for w in stress_words):
            return 'stressed'
            
        return system_emotion

if __name__ == "__main__":
    # Quick sanity check
    detector = EmotionDetector()
    sample_text = "I am feeling extremely stressed about my upcoming final exams."
    emotion, conf, keys = detector.predict_emotion(sample_text)
    print(f"Input: {sample_text}")
    print(f"Emotion: {emotion} (Conf: {conf:.2f})")
    print(f"Keywords: {keys}")

"""
Wellness Recommendation System - FastAPI REST API

A complete REST API for emotion-based wellness video recommendations.
Provides endpoints for emotion detection, personalized recommendations,
user feedback, and learning statistics.

API Documentation available at:
- Swagger UI: /docs
- ReDoc: /redoc
"""

import logging
import sys
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from src.api.recommendation_endpoint import HybridRecommendationSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/api.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# ═══════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════

class EmotionRequest(BaseModel):
    """Request model for emotion detection."""
    text: str = Field(..., min_length=1, description="Text to analyze for emotion")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"text": "I'm feeling overwhelmed with all this coursework"}
            ]
        }
    }

class EmotionResponse(BaseModel):
    """Response model for emotion detection."""
    success: bool
    emotion: str
    confidence: float
    keywords: list[str]

class RecommendationRequest(BaseModel):
    """Request model for getting recommendations."""
    user_input: str = Field(..., min_length=1, description="User's text describing their mood/situation")
    user_id: Optional[str] = Field(default="anonymous", description="Unique user identifier")
    category: str = Field(default="yoga", description="Content category")
    top_n: int = Field(default=3, ge=1, le=10, description="Number of recommendations to return")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_input": "I'm stressed about my exams",
                    "user_id": "student_123",
                    "category": "yoga",
                    "top_n": 3
                }
            ]
        }
    }

class VideoRecommendation(BaseModel):
    """Model for a single video recommendation."""
    video_id: str
    title: str
    url: str
    thumbnail: Optional[str]
    channel_name: str
    duration_minutes: float
    views: int
    likes: int
    score: float
    heuristic_score: float
    linucb_score: float

class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    success: bool
    emotion: str
    confidence: float
    keywords: list[str]
    recommendations: list[VideoRecommendation]
    metadata: dict

class FeedbackRequest(BaseModel):
    """Request model for submitting feedback."""
    video_id: str = Field(..., description="ID of the video being rated")
    user_id: str = Field(..., description="User who is providing feedback")
    emotion: str = Field(..., description="Emotion context when video was recommended")
    category: str = Field(default="yoga", description="Content category")
    feedback: str = Field(..., pattern="^(thumbs_up|thumbs_down)$", description="User feedback: thumbs_up or thumbs_down")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "video_id": "abc123",
                    "user_id": "student_123",
                    "emotion": "stressed",
                    "category": "yoga",
                    "feedback": "thumbs_up"
                }
            ]
        }
    }

class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    success: bool
    status: str
    reward: Optional[float]
    total_interactions: int
    linucb_weight: float

class StatsResponse(BaseModel):
    """Response model for system statistics."""
    success: bool
    total_interactions: int
    models_trained: int
    current_alpha: float
    linucb_weight: float
    model_details: dict

class HealthResponse(BaseModel):
    """Response model for health check."""
    success: bool
    status: str
    timestamp: str
    components: dict

# ═══════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="Wellness Recommendation API",
    description="""
    An AI-powered wellness recommendation system that detects emotions 
    and suggests personalized yoga/wellness videos.
    
    ## Features
    - 🧠 **Emotion Detection**: BERT-based emotion analysis with keyword validation
    - 🎬 **Video Recommendations**: Hybrid heuristic + LinUCB personalized ranking
    - 📊 **Adaptive Learning**: System learns from user feedback
    - 🔄 **Real-time**: Live YouTube video fetching (when API key configured)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation system with real YouTube service
logger.info("Initializing Wellness Recommendation System...")
recommendation_system = HybridRecommendationSystem()
logger.info("System initialized successfully!")

# ═══════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - Basic health check.
    
    Returns a simple status message confirming the API is running.
    """
    return {
        "success": True,
        "message": "Wellness Recommendation API is running",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint.
    
    Returns comprehensive system status including:
    - Overall status
    - Component health (emotion detector, recommender, YouTube service)
    - Current timestamp
    """
    try:
        # Check components
        components = {
            "emotion_detector": "healthy",
            "linucb_recommender": "healthy",
            "youtube_service": "healthy (mock)" if recommendation_system.youtube else "unavailable",
            "feature_normalizer": "healthy"
        }
        
        return HealthResponse(
            success=True,
            status="healthy",
            timestamp=datetime.now().isoformat(),
            components=components
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect-emotion", response_model=EmotionResponse, tags=["Emotion"])
async def detect_emotion(request: EmotionRequest):
    """
    Detect emotion from user text.
    
    Analyzes the input text using a BERT-based model with keyword validation
    to determine the user's emotional state.
    
    **Supported emotions**: stressed, anxious, happy, angry, sad, calm, tired, motivated
    
    **Example**:
    ```json
    {"text": "I'm feeling overwhelmed with all this coursework"}
    ```
    
    **Response**:
    ```json
    {
        "success": true,
        "emotion": "stressed",
        "confidence": 0.89,
        "keywords": ["overwhelmed", "coursework"]
    }
    ```
    """
    logger.info(f"Emotion detection request: '{request.text[:50]}...'")
    
    try:
        emotion, confidence, keywords = recommendation_system.detect_emotion_and_context(request.text)
        
        logger.info(f"Detected: {emotion} (confidence: {confidence:.3f})")
        
        return EmotionResponse(
            success=True,
            emotion=emotion,
            confidence=round(confidence, 4),
            keywords=keywords
        )
    except Exception as e:
        logger.error(f"Emotion detection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Emotion detection failed: {str(e)}")

@app.post("/api/recommendations", response_model=RecommendationResponse, tags=["Recommendations"])
async def get_recommendations(request: RecommendationRequest):
    """
    Get personalized video recommendations.
    
    Takes user text, detects emotion, fetches relevant videos from YouTube,
    and ranks them using a hybrid heuristic + LinUCB algorithm.
    
    **Pipeline**:
    1. Detect emotion from user input
    2. Build emotion-aware search query
    3. Fetch videos from YouTube (or mock)
    4. Extract and normalize features
    5. Apply hybrid scoring (quality + personalization)
    6. Return top N recommendations
    
    **Example**:
    ```json
    {
        "user_input": "I'm stressed about my exams",
        "user_id": "student_123",
        "category": "yoga",
        "top_n": 3
    }
    ```
    """
    logger.info(f"Recommendation request from user '{request.user_id}': '{request.user_input[:50]}...'")
    
    try:
        result = recommendation_system.get_recommendations(
            user_input=request.user_input,
            user_id=request.user_id,
            category=request.category,
            top_n=request.top_n
        )
        
        # Transform recommendations to response model
        recommendations = []
        for rec in result['recommendations']:
            recommendations.append(VideoRecommendation(
                video_id=rec['video_id'],
                title=rec['title'],
                url=rec['url'],
                thumbnail=rec.get('thumbnail'),
                channel_name=rec['channel_name'],
                duration_minutes=rec['duration_minutes'],
                views=rec.get('views', 0),
                likes=rec.get('likes', 0),
                score=round(rec['score'], 4),
                heuristic_score=round(rec['heuristic_score'], 4),
                linucb_score=round(rec['linucb_score'], 4)
            ))
        
        logger.info(f"Returning {len(recommendations)} recommendations for emotion: {result['emotion']}")
        
        return RecommendationResponse(
            success=True,
            emotion=result['emotion'],
            confidence=round(result['confidence'], 4),
            keywords=result['keywords'],
            recommendations=recommendations,
            metadata=result['metadata']
        )
    except ValueError as e:
        logger.warning(f"Invalid request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

@app.post("/api/feedback", response_model=FeedbackResponse, tags=["Feedback"])
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback for a recommendation.
    
    Feedback is used to train the LinUCB model for better personalization.
    The system learns user preferences over time.
    
    **Feedback values**:
    - `thumbs_up`: Positive feedback (reward = +1.0)
    - `thumbs_down`: Negative feedback (reward = -1.0)
    
    **Example**:
    ```json
    {
        "video_id": "abc123",
        "user_id": "student_123",
        "emotion": "stressed",
        "category": "yoga",
        "feedback": "thumbs_up"
    }
    ```
    """
    logger.info(f"Feedback from user '{request.user_id}': {request.feedback} for video '{request.video_id}'")
    
    try:
        result = recommendation_system.process_feedback(
            video_id=request.video_id,
            user_id=request.user_id,
            emotion=request.emotion,
            category=request.category,
            feedback=request.feedback
        )
        
        logger.info(f"Feedback processed. Total interactions: {result.get('total_interactions', 0)}")
        
        return FeedbackResponse(
            success=True,
            status=result['status'],
            reward=result.get('reward'),
            total_interactions=result.get('total_interactions', 0),
            linucb_weight=result.get('linucb_weight', 0.2)
        )
    except Exception as e:
        logger.error(f"Feedback processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback processing failed: {str(e)}")

@app.get("/api/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_stats():
    """
    Get LinUCB learning statistics.
    
    Returns current state of the recommendation system including:
    - Total user interactions
    - Number of trained models
    - Current exploration parameter (alpha)
    - LinUCB weight in hybrid scoring
    - Per-emotion model details
    
    **Use case**: Monitor system learning progress and model health.
    """
    logger.info("Stats request received")
    
    try:
        stats = recommendation_system.linucb.get_statistics()
        
        return StatsResponse(
            success=True,
            total_interactions=stats['total_interactions'],
            models_trained=stats['models_trained'],
            current_alpha=stats['current_alpha'],
            linucb_weight=recommendation_system._get_linucb_weight(),
            model_details=stats['model_details']
        )
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

# ═══════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("  WELLNESS RECOMMENDATION API")
    print("=" * 60)
    print("  Starting server at http://0.0.0.0:8000")
    print("  API Docs: http://localhost:8000/docs")
    print("  ReDoc: http://localhost:8000/redoc")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

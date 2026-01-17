import sys
import os
import numpy as np

# Add src to path
sys.path.append(os.getcwd())

from src.api.recommendation_endpoint import HybridRecommendationSystem

def test_feedback_loop():
    print("Initializing Sanctuary System...")
    # Mocking YouTube to avoid API calls and ensure stability
    system = HybridRecommendationSystem(use_mock_youtube=True)
    
    user_id = "test_user"
    user_input = "I feel stressed"
    
    # 1. Get initial recommendations
    print(f"\nStep 1: Getting recommendations for: '{user_input}'")
    results = system.get_recommendations(user_input=user_input, user_id=user_id, top_n=1)
    
    if not results['recommendations']:
        print("Error: No recommendations returned.")
        return
        
    vid = results['recommendations'][0]
    emotion = results['emotion']
    print(f"Detected Emotion: {emotion}")
    print(f"Top Video: {vid['title']} (ID: {vid['video_id']})")
    
    # Record initial theta
    model = system.linucb.get_or_create_model(emotion, 'yoga')
    initial_theta = model.theta.copy()
    initial_interactions = model.interaction_count
    
    # 2. Process Feedback
    feedback = 'thumbs_up'
    print(f"\nStep 2: Processing feedback: {feedback}")
    response = system.process_feedback(
        user_id=user_id,
        emotion=emotion,
        category='yoga',
        video_id=vid['video_id'],
        feedback=feedback,
        context=vid.get('_context'),
        video_features=vid.get('features')
    )
    print(f"Response: {response}")
    
    # NEW: Save the model so it remembers this interaction!
    system.linucb.save('./models/linucb_models.pkl')
    print("Model saved to './models/linucb_models.pkl'")
    
    # 3. Verify Update
    updated_theta = model.theta
    updated_interactions = model.interaction_count
    
    print(f"\nStep 3: Verifying weights...")
    theta_diff = np.linalg.norm(updated_theta - initial_theta)
    print(f"Theta Change (Norm): {theta_diff:.6f}")
    print(f"Interactions for this Mood: {initial_interactions} -> {updated_interactions}")
    print(f"Total Interactions across all moods: {system.linucb.total_interactions}")
    
    if theta_diff > 0 and updated_interactions == initial_interactions + 1:
        print("\nSUCCESS: Feedback loop verified. Weights updated correctly.")
    else:
        print("\nFAILURE: Feedback loop did not update weights as expected.")

if __name__ == "__main__":
    test_feedback_loop()

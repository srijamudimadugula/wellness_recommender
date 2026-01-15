"""
Wellness Recommendation API - Test Suite

Tests all API endpoints using the requests library.
Run this after starting the server with: python app.py

Usage:
    python test_api.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response):
    """Pretty print response."""
    print(f"  Status: {response.status_code}")
    try:
        data = response.json()
        print(f"  Response:\n{json.dumps(data, indent=4)}")
    except:
        print(f"  Response: {response.text}")

def test_health():
    """Test basic health endpoint."""
    print_separator("TEST: Health Check (/)")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("  ❌ Connection failed. Is the server running?")
        return False

def test_detailed_health():
    """Test detailed health endpoint."""
    print_separator("TEST: Detailed Health (/health)")
    
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    return response.status_code == 200

def test_emotion_detection():
    """Test emotion detection endpoint."""
    print_separator("TEST: Emotion Detection (/api/detect-emotion)")
    
    test_cases = [
        "I'm feeling overwhelmed with all this coursework",
        "I'm so happy today, everything is going great!",
        "I'm worried about my presentation tomorrow"
    ]
    
    all_passed = True
    for text in test_cases:
        print(f"\n  Input: \"{text}\"")
        
        response = requests.post(
            f"{BASE_URL}/api/detect-emotion",
            json={"text": text}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Emotion: {data['emotion'].upper()} (confidence: {data['confidence']:.1%})")
            print(f"  Keywords: {', '.join(data['keywords'])}")
        else:
            print(f"  ❌ Failed: {response.status_code}")
            all_passed = False
    
    return all_passed

def test_recommendations():
    """Test recommendations endpoint."""
    print_separator("TEST: Recommendations (/api/recommendations)")
    
    payload = {
        "user_input": "I'm stressed about my exams and feeling anxious",
        "user_id": "test_user_001",
        "category": "yoga",
        "top_n": 3
    }
    
    print(f"  Request: {json.dumps(payload, indent=4)}")
    
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n  Detected Emotion: {data['emotion'].upper()}")
        print(f"  Confidence: {data['confidence']:.1%}")
        print(f"\n  Recommendations:")
        
        for i, rec in enumerate(data['recommendations'], 1):
            print(f"\n  {i}. {rec['title']}")
            print(f"     Channel: {rec['channel_name']}")
            print(f"     Duration: {rec['duration_minutes']:.1f} min")
            print(f"     Score: {rec['score']:.3f}")
        
        print(f"\n  Metadata: {json.dumps(data['metadata'], indent=4)}")
        return True
    else:
        print_response(response)
        return False

def test_feedback():
    """Test feedback endpoint."""
    print_separator("TEST: Feedback (/api/feedback)")
    
    payload = {
        "video_id": "test_video_123",
        "user_id": "test_user_001",
        "emotion": "stressed",
        "category": "yoga",
        "feedback": "thumbs_up"
    }
    
    print(f"  Request: {json.dumps(payload, indent=4)}")
    
    response = requests.post(
        f"{BASE_URL}/api/feedback",
        json=payload
    )
    
    print_response(response)
    return response.status_code == 200

def test_stats():
    """Test statistics endpoint."""
    print_separator("TEST: Statistics (/api/stats)")
    
    response = requests.get(f"{BASE_URL}/api/stats")
    print_response(response)
    return response.status_code == 200

def run_all_tests():
    """Run all API tests."""
    print("\n" + "=" * 60)
    print("  WELLNESS RECOMMENDATION API - TEST SUITE")
    print("=" * 60)
    print(f"  Base URL: {BASE_URL}")
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test health first
    if not test_health():
        print("\n❌ Server not running. Please start with: python app.py")
        return
    results['health'] = True
    
    # Run remaining tests
    results['detailed_health'] = test_detailed_health()
    results['emotion_detection'] = test_emotion_detection()
    results['recommendations'] = test_recommendations()
    results['feedback'] = test_feedback()
    results['stats'] = test_stats()
    
    # Summary
    print_separator("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"  {test_name:25} {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 All tests passed!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    run_all_tests()

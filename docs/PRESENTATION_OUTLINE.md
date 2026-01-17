# Project Presentation Outline: Wellness Sanctuary

This document provides a professional 10-slide structure for your Google Slides presentation. Each slide includes a title, bullet points, and a visual suggestion.

---

## Slide 1: Title Slide
- **Title**: Wellness Sanctuary
- **Subtitle**: AI-Powered Adaptive Mindfulness Recommendation System
- **Details**: 
    - Student: M Srija
    - Mentor: Kartik Gupta
- **Visual**: Use the `wellness_sanctuary_ui_snapshot.png` as a background or side image.

---

## Slide 2: Problem Statement: The Discovery Crisis
- **Title**: The Problem: Why Current Search Fails Wellness
- **Content**:
    - **1. Decision Fatigue (Cognitive Load)**: In high-stress states, users have low mental energy. Scrolling through thousands of results actually *increases* stress rather than relieving it.
    - **2. The Semantic Gap**: Searching for emotions like *"I'm angry"* or *"I feel stressed"* returns literal content (news/rants) instead of the **relaxing relief** (Yoga/Meditation) the user needs.
    - **3. Keywords vs. Emotional Need**: Mainstream AI optimizes for *what you say* (keywords), but ignores *how you feel* (emotional intent), creating a barrier to immediate wellness.
- **Visual**: A split screen showing a "Confused/Stressed User" on one side (YouTube results) and a "Peaceful User" on the other (Wellness Sanctuary results).

---

## Slide 3: Our Solution (The Emotional Bridge)
- **Title**: Our Solution: The Emotional Bridge
- **Content**:
    - A "zero-search" interface for immediate relief.
    - Converts raw emotional text into precise recommendations.
    - Adaptive learning that fits the user's personal lifestyle.
- **Visual**: A simple graphic showing "Input: Mood" -> "Bridge" -> "Output: Peace."

---

## Slide 4: System Architecture
- **Title**: System Design: Hybrid Bayesian AI
- **Content**:
    - **Intake**: NLP-driven emotion detection.
    - **Refinement**: Stressor extraction using KeyBERT.
    - **Retrieval**: Real-time YouTube API integration.
    - **Personalization**: Bayesian Contextual Bandits (LinUCB).
- **Visual**: A high-level flowchart of the pipeline.

---

## Slide 5: NLP Module (Perception)
- **Title**: NLP: Understanding the User's Voice
- **Content**:
    - **DistilBERT**: High-speed emotion classification (6 classes).
    - **KeyBERT**: Identifying stressors (e.g., "deadlines", "exams").
    - **Rule-Based Safety**: Custom validators to ensure domain-specific jargon is caught accurately.
- **Visual**: A code snippet of a user input vs. the detected emotion/stressor label.

---

## Slide 6: Bayesian Personalization (Decision)
- **Title**: Bayesian RL: Linear Upper Confidence Bound (LinUCB)
- **Content**:
    - **Belief Updates**: Continually updates internal matrices (A & b) based on feedback.
    - **Exploration vs. Exploitation**: Balances "known favorites" with "new discoveries."
    - **19-Dim Context**: Real-time evaluation of emotion, time, and content metadata.
- **Visual**: A small graphic showing a 19-dimensional vector or the LinUCB score formula.

---

## Slide 7: Demo Snapshots
- **Title**: User Experience & Prototype
- **Content**:
    - Minimalist, spa-inspired Streamlit interface.
    - Smooth animations and calming sage-green aesthetic.
    - Interactive feedback loop (likes influence future rankings).
- **Visual**: **Embed `wellness_sanctuary_ui_snapshot.png` here.**

---

## Slide 8: Results & Performance
- **Title**: Results: Performance & Accuracy
- **Content**:
    - **NLP Accuracy**: 76.92% on system-aligned validation set.
    - **Latency**: End-to-end response in < 0.8 seconds.
    - **Learning Rate**: Personalization begins to converge after ~15 interactions.
- **Visual**: A bar chart or a "speedometer" graphic showing the 0.78s latency.

---

## Slide 9: Key Learnings
- **Title**: Technical Reflections & Challenges
- **Content**:
    - **Hybrid Power**: Combining Transformers with heuristics solves the "Cold Start" problem.
    - **Numerical Stability**: Using Pseudoinverse for stable Bayesian math.
    - **Feature Scaling**: Critical for stable matrix operations in RL.
- **Visual**: Icons representing "Challenge" and "Solution."

---

## Slide 10: Conclusion & Future Scope
- **Title**: The Road Ahead
- **Content**:
    - **Biometric Integration**: Moving to heart-rate-based passive detection.
    - **Persistent Profiles**: Scalable database for long-term Bayesian learning.
    - **Multilingual Support**: Expanding the NLP reach.
- **Visual**: A serene sunrise or a "Next Steps" roadmap graphic.

---

### AI Usage Disclosure
*This presentation and the underlying system were developed with assistance from Antigravity (Google Deepmind Assistant).*

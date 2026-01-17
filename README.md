# 🌿 Wellness Sanctuary Recommendation System

A premium, AI-powered wellness recommendation system that detects user emotions and curates personalized yoga and mindfulness content using a Hybrid Recommender System (Heuristic Ranking + LinUCB Reinforcement Learning).

## 🎓 Module E Project Submission

**Artifacts:**
- 📘 **Primary Submission (Notebook):** [`submission_notebook.ipynb`](./submission_notebook.ipynb)  *(Main Source of Truth)*
- 📄 **Project Report:** [`docs/PROJECT_REPORT.md`](./docs/PROJECT_REPORT.md)
- 📽️ **Demo Video:** [Link to be added]
- 📑 **Slides:** [Link to be added]

---

## ✨ Features

- **🧠 Emotion Detection**: Advanced BERT-based model (`distilbert-base-uncased-emotion`) to understand user sentiment (stressed, anxious, happy, tired, etc.).
- **🤖 Hybrid Recommendation Engine**:
  - **Heuristic Ranker**: Quality assurance based on views, engagement, and video metadata.
  - **LinUCB (Contextual Multi-Armed Bandit)**: Production-ready personalization with:
    - 🔒 **Thread-Safe Updates**: Concurrent user feedback without data corruption
    - 🧠 **Temporal Discounting** (`λ=0.99`): Human-like "forgetting" of older preferences
    - 📊 **Behavior-Based Reward Shaping**: Watch-time + explicit feedback → nuanced rewards
- **📱 Premium User Interface**: A calm, "Sanctuary" themed Streamlit web application.
- **🔌 REST API**: Full FastAPI backend for integration with other platforms.
- **🔄 Adaptability**: Works with a Mock YouTube Service (offline/dev) or the real YouTube Data API.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Optional] YouTube Data API Key (for live data)

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd wellness_recommender
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up Environment Variables:
   Create a `.env` file or set:
   ```bash
   export YOUTUBE_API_KEY="your_api_key_here"
   ```
   *Note: If no API key is provided, the system defaults to a mock service for demonstration and testing.*

---

## 🖥️ Running the Application

### 1. Web Interface (Streamlit)
The primary user interface.

### 1. Web Interface (Streamlit)
To run locally:
```bash
streamlit run streamlit_app.py
```
Access at: `http://localhost:8501` (Note: No Lock Icon/HTTPS locally)

### 2. Deployment (Streamlit Cloud) - **Recommended**
To get the secure **HTTPS Lock Icon**:
1. Push this code to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io).
3. Deploy the app from your repo.
4. **Important**: In "Advanced Settings" > "Secrets", add:
   ```toml
   YOUTUBE_API_KEY = "your_key_here"
   ```

### 2. Backend API (FastAPI)
For headless operation or integrations.

```bash
python app.py
```
- **API**: `http://localhost:8000`
- **Docs**: `http://localhost:8000/docs`

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run unit and integration tests
python -m pytest tests/

# Run specific integration test
python -m pytest tests/test_integration.py
```

### End-to-End API Test
To test the live API (ensure `app.py` is running first):
```bash
python tests/e2e_api_check.py
```

---

## 📂 Project Structure

```
wellness_recommender/
├── app.py                  # FastAPI Backend Entrypoint
├── streamlit_app.py        # Streamlit Frontend Entrypoint
├── requirements.txt        # Project Dependencies
├── README.md               # Project Documentation
├── assets/                 # Image assets for UI
├── models/                 # Saved ML models (LinUCB, Normalizers)
├── logs/                   # Application logs
├── src/
│   ├── api/
│   │   ├── recommendation_endpoint.py  # Main Orchestrator
│   │   ├── youtube_service.py          # YouTube API Client
│   │   ├── mock_youtube_service.py     # Mock Client for Dev/Test
│   │   └── ...
│   ├── ml/
│   │   ├── emotion_detector.py         # BERT Emotion Model
│   │   ├── feature_normalizer.py       # Feature Scaling
│   │   └── heuristic_ranker.py         # Baseline Ranker
│   └── rl/
│       └── linucb_recommender.py       # LinUCB Algorithm
└── tests/                  # Unit and Integration Tests
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Pydantic, Python 3.9+
- **Frontend**: Streamlit, Custom CSS
- **ML/AI**: PyTorch, Transformers (Hugging Face), Scikit-Learn
- **Algorithm**: Linear Upper Confidence Bound (LinUCB) for Contextual Bandits
- **Production**: Thread-safe locking, Temporal discounting, Behavior-based reward shaping

---

## 🔧 Production-Ready Architecture

### LinUCB Enhancements

| Feature | Description |
|---------|-------------|
| **Thread-Safe Locking** | `threading.Lock()` prevents race conditions during concurrent updates |
| **Temporal Discounting** | `lambda_forget=0.99` applies exponential decay to older preferences |
| **Reward Shaping** | `calculate_production_reward()` combines watch-time + explicit feedback |
| **Error Handling** | Matrix inversion failures gracefully reset without crashing |

### Reward Calculation

```python
# Example: 75% watch + thumbs_up = 0.75 reward
reward = calculate_production_reward(watch_time=45, total_duration=60, feedback_type='thumbs_up')
```

| Scenario | Reward |
|----------|--------|
| Watched 100%, thumbs up | **+1.0** |
| Watched 50%, no feedback | **+0.1** |
| Thumbs down (any watch) | **-1.5** |

---

## 🛡️ License

Private/Proprietary - Do not distribute without permission.

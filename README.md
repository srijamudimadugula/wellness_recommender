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
  - **LinUCB (Contextual Multi-Armed Bandit)**: Personalization algorithm that learns from user feedback in real-time.
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

```bash
streamlit run streamlit_app.py
```
Access at: `http://localhost:8501`

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

---

## 🛡️ License

Private/Proprietary - Do not distribute without permission.

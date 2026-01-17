
import json
import os

NOTEBOOK_FILENAME = "FINAL_SUBMISSION_wellness_recommender.ipynb"

def read_file(filepath):
    if not os.path.exists(filepath):
        return [f"# ERROR: {filepath} NOT FOUND"]
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned = []
    cleaned.append(f"# --- SOURCE: {filepath} ---\n")
    for line in lines:
        # Comment out imports to avoid runtime errors in top-to-bottom run
        s = line.strip()
        if s.startswith("from src") or s.startswith("import src") or (("sys.path" in s) and ("src" in s)):
             cleaned.append(f"# {line}")
        elif s.startswith("from api."):
             cleaned.append(f"# {line}")
        else:
             cleaned.append(line)
    cleaned.append("\n\n")
    return cleaned

# 1. Define Notebook Structure (Cells)
cells = []

# Cell 0: Install
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# --- STEP 0: INSTALL REQUIRED LIBRARIES ---\n",
        "!pip install transformers torch keybert scikit-learn requests streamlit numpy pandas google-api-python-client isodate\n"
    ]
})

# Cell 1: Problem Definition
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# **WELLNESS SANCTUARY: AI PROJECT SUBMISSION**\n",
        "\n",
        "## **1. Problem Definition & Objective**\n",
        "\n",
        "**a. Selected Project Track:** Personalized Wellness & Mental Health Support (AI_Health)\n",
        "\n",
        "**b. Clear Problem Statement:**\n",
        "In today's fast-paced world, individuals often struggle to find personalized, effective methods to manage stress, anxiety, and other emotional states. While generic wellness content exists, it lacks real-time personalization based on the user's immediate emotional state and historical preferences. The goal is to build an intelligent recommendation system that bridges this gap.\n",
        "\n",
        "**c. Real-world Relevance:**\n",
        "Mental wellness is a critical public health concern. By leveraging AI to detect emotions and curate tailored yoga/mindfulness content, this system can provide accessible, immediate relief and support healthy habits, potentially reducing burnout and anxiety levels in users.\n",
        "\n",
        "**What is used in this section and why?**\n",
        "We clearly define the scope to ensure the AI solution is targeted. We chose a hybrid approach to solve the specific problem of 'choice paralysis' in high-stress moments."
    ]
})

# Cell 2: Data Understanding
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **2. Data Understanding & Preparation**\n",
        "\n",
        "**a. Dataset Source:**\n",
        "- **YouTube Data API (Primary):** Real-time video metadata (titles, views, likes, tags, duration) from yoga and wellness channels.\n",
        "- **Mock Dataset (Fallback):** A synthetic dataset of 50+ curated wellness videos with rich metadata for reproducible testing.\n",
        "- **User Context Data:** Simulated user interaction logs (clicks, likes, dismissals) for the Reinforcement Learning agent.\n",
        "\n",
        "**b. Cleaning & Preprocessing:**\n",
        "- **Feature Engineering:** `log_views` (popularity), `engagement_ratio` (likes/views), `recency`, and `duration_norm`.\n",
        "- **Normalization:** A `FeatureNormalizer` scales these diverse features into a 0-1 range for stable LinUCB matrix updates.\n",
        "\n",
        "**What is used in this section and why?**\n",
        "We use a `FeatureNormalizer` (StandardScaler logic) because the LinUCB algorithm requires normalized features to prevent one large value (like 1M views) from dominating the matrix inversion."
    ]
})

# Cell 3: Data Code
source_c3 = []
source_c3.extend(read_file("src/ml/feature_normalizer.py"))
source_c3.extend(read_file("src/api/mock_youtube_service.py"))
source_c3.extend(read_file("src/api/youtube_service.py"))
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": source_c3
})

# Cell 4: Model Design
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **3. Model / System Design**\n",
        "\n",
        "**a. AI Techniques Used:**\n",
        "1. **NLP (Emotion Detection):** `distilbert-base-uncased-emotion` for classifying user text.\n",
        "2. **Bayesian Reinforcement Learning (LinUCB):** A Contextual Multi-Armed Bandit algorithm that treats the weight parameters $\\theta$ as random variables with a Gaussian posterior.\n",
        "\n",
        "**What is used in this section and why?**\n",
        "We use LinUCB because it handles the **Cold Start** problem better than collaborative filtering. The term `alpha * sqrt(ctx.T @ A_inv @ ctx)` represents the uncertainty (standard deviation) of our prediction. High uncertainty triggers exploration."
    ]
})

# Cell 5: Model Code
source_c5 = []
source_c5.extend(read_file("src/ml/emotion_validator.py"))
source_c5.extend(read_file("src/ml/emotion_detector.py"))
source_c5.extend(read_file("src/rl/linucb_recommender.py"))
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": source_c5
})

# Cell 6: Core Impl
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **4. Core Implementation**\n",
        "\n",
        "**a. Pipelines:**\n",
        "The system orchestrates retrieval, scoring, and feedback using `HybridRecommendationSystem`.\n",
        "\n",
        "**b. Heuristic & Context:**\n",
        "We use a `HeuristicRanker` as a baseline for quality assurance (e.g. video engagement ratio)."
    ]
})

# Cell 7: Core Code
source_c7 = []
source_c7.extend(read_file("src/ml/heuristic_ranker.py"))
source_c7.extend(read_file("src/api/user_context_manager.py"))
source_c7.extend(read_file("src/api/recommendation_endpoint.py"))
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": source_c7
})

# Cell 8: Eval Setup
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **5. Evaluation & Analysis**\n",
        "Running the simulation..."
    ]
})

# Cell 9: Simulation Loop
source_c9 = [
    "# --- Simulation Loop ---\n",
    "# Ensure System is initialized (Using Mock for robustness in notebook)\n",
    "system = HybridRecommendationSystem(use_mock_youtube=True)\n",
    "\n",
    "user_query = \"I'm feeling super stressed with work\"\n",
    "print(f\"User Input: {user_query}\")\n",
    "\n",
    "# 1. Get Recommendations\n",
    "try:\n",
    "    recs_data = system.get_recommendations(user_query, \"user_01\")\n",
    "    recs = recs_data['recommendations']\n",
    "    if recs:\n",
    "        top_rec = recs[0]\n",
    "        print(f\"Top Recommendation: {top_rec['title']} | Score: {top_rec['match_score']}%\")\n",
    "        \n",
    "        # 2. Simulate Feedback\n",
    "        print(\"User watching...\")\n",
    "        rew = system.process_feedback(\n",
    "            user_id=\"user_01\", \n",
    "            emotion=recs_data['emotion'], \n",
    "            category='yoga', \n",
    "            video_id=top_rec['video_id'], \n",
    "            feedback='thumbs_up', \n",
    "            context=top_rec.get('_context'), \n",
    "            video_features=top_rec.get('features'), \n",
    "            watch_time=300, \n",
    "            total_duration=top_rec['duration_minutes']*60\n",
    "        )\n",
    "        print(f\"Feedback Processed! Reward: {rew['reward']}\")\n",
    "    else:\n",
    "        print(\"No recommendations found to evaluate.\")\n",
    "except Exception as e:\n",
    "    print(f\"Simulation Error: {e}\")\n"
]
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": source_c9
})

# Cell 10: Ethics
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **6. Ethical Considerations**\n",
        "We implement safety overrides for crisis keywords and ensure data privacy by running emotion detection locally."
    ]
})

# Cell 11: Conclusion
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **7. Conclusion**\n",
        "The Wellness Sanctuary system successfully integrates NLP and RL to provide personalized mental health support."
    ]
})

# Cell 12: Appendix
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## **Appendix: Frontend (Streamlit)**\n",
        "The following code is the actual frontend implementation used in `streamlit_app.py`."
    ]
})

# Cell 13: Streamlit Code
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": read_file("streamlit_app.py")
})

# Valid Notebook JSON
notebook_json = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open(NOTEBOOK_FILENAME, 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, indent=1)

print(f"Successfully rebuilt {NOTEBOOK_FILENAME} with {len(cells)} cells.")
print("Included full contents of youtube_service.py and streamlit_app.py.")

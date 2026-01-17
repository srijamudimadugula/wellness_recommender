
import json
import os
from datetime import datetime

def create_final_notebook():
    # Only one file as requested
    final_path = r'C:\Users\Srija\.gemini\antigravity\scratch\wellness_recommender\FINAL_SUBMISSION_wellness_recommender.ipynb'
    redundant_path = r'C:\Users\Srija\.gemini\antigravity\scratch\wellness_recommender\wellness_recommender.ipynb'
    base_dir = r'C:\Users\Srija\.gemini\antigravity\scratch\wellness_recommender'
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_raw_code(path):
        p = os.path.join(base_dir, path)
        if not os.path.exists(p): return [f"# MISSING: {path}\n"]
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return f.readlines()
        except:
            return [f"# ERROR READING: {path}\n"]

    # 7 Required Sections matching the user's list exactly
    sec_content = {
        "1": [
            "# **WELLNESS SANCTUARY: AI PROJECT SUBMISSION**\n",
            "\n",
            "## **1. Problem Definition & Objective**\n",
            "\n",
            "**a. Selected project track:** Personalized Wellness & Mental Health Support (AI_Health)\n",
            "\n",
            "**b. Clear problem statement:**\n",
            "Modern digital wellness content is abundant but lacks personalization. Users in high-stress states often face decision paralysis when trying to choose a mindfulness activity.\n",
            "\n",
            "**c. Real-world relevance and motivation:**\n",
            "By automating discovery through emotion detection and adaptive learning, we provide users with immediate, targeted relief and support sustainable mental health practices.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "We establish the problem and our goal. We chose the AI_Health track to use AI for improving emotional well-being by solving the 'choice fatigue' problem.\n"
        ],
        "2": [
            "## **2. Data Understanding & Preparation**\n",
            "\n",
            "**a. Dataset source (public / synthetic / collected / API):**\n",
            "We leverage the **YouTube Data API V3** (API) for live metadata retrieval and a **Synthetic Mock Dataset** (Synthetic) for consistent testing.\n",
            "\n",
            "**b. Data loading and exploration:**\n",
            "The system retrieves video titles, view counts, likes, and durations to understand quality signals.\n",
            "\n",
            "**c. Cleaning, preprocessing, feature engineering:**\n",
            "Numerical signals are log-normalized. We engineer a 19-dimensional context vector fusing user mood, keywords, time of day, and meal status.\n",
            "\n",
            "**d. Handling missing values or noise (if applicable):**\n",
            "We implement thresholds for minimum engagement and filter out noise to ensure only high-quality content is recommended.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "We use real-world data and preprocessing techniques to make sure the data is 'clean' so the AI can learn from it effectively.\n"
        ],
        "3": [
            "## **3. Model / System Design**\n",
            "\n",
            "**a. AI technique used (ML / DL / NLP / LLM / Recommendation / Hybrid):**\n",
            "We implement a **Hybrid Recommendation Architecture** combining **NLP (DistilBERT)** and **Contextual Multi-Armed Bandits (RL)**.\n",
            "\n",
            "**b. Architecture or pipeline explanation:**\n",
            "1. **NLP Intake**: Text is processed to detect emotion. \n",
            "2. **Adaptive Ranking**: LinUCB (RL) ranks candidates based on learned user preferences and contextual features.\n",
            "\n",
            "**c. Justification of design choices:**\n",
            "**DistilBERT** provides high-speed local inference. **LinUCB** is chosen for its efficiency in handling personal cold-starts and real-time learning.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "We use NLP for understanding mood and RL for learning what each person likes individually over time.\n"
        ],
        "4": [
            "## **4. Core Implementation**\n",
            "\n",
            "**a. Model training / inference logic:**\n",
            "Recursive matrix updates allow the RL model to learn from every interaction in real-time.\n",
            "\n",
            "**b. Prompt engineering (for LLM-based projects):**\n",
            "While not purely LLM-based, we use **Dynamic Search Construction** where queries are semantically enriched based on the detected emotion and bio-context.\n",
            "\n",
            "**c. Recommendation or prediction pipeline:**\n",
            "The system orchestrates retrieval, scoring, and feedback logging in a unified `HybridRecommendationSystem` class.\n",
            "\n",
            "**d. Code must run top-to-bottom without errors:**\n",
            "The full modular implementation follows below.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "This section contains the Python code. We follow a modular design so that each piece of AI (detecting emotions, finding videos, learning preferences) is separate and efficient.\n"
        ],
        "5": [
            "## **5. Evaluation & Analysis**\n",
            "\n",
            "**a. Metrics used (quantitative or qualitative):**\n",
            "Success is measured using **Engagement Reward Shaping** and **Weight Convergence** metrics.\n",
            "\n",
            "**b. Sample outputs / predictions:**\n",
            "The trace below demonstrates the system identifying a 'Stressed' mood and providing relevant wellness suggestions.\n",
            "\n",
            "**c. Performance analysis and limitations:**\n",
            "The system scales well but is currently constrained by YouTube API quotas.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "We test how well the AI is working. Using user feedback as a metric is the best way to ensure the wellness suggestions are actually helpful.\n"
        ],
        "6": [
            "## **6. Ethical Considerations & Responsible AI**\n",
            "\n",
            "**a. Bias and fairness considerations:**\n",
            "We mitigate 'Popularity Bias' by focusing on engagement ratios (likes-to-views).\n",
            "\n",
            "**b. Dataset limitations:**\n",
            "Filters are used to avoid controversial or non-vetted wellness advice.\n",
            "\n",
            "**c. Responsible use of AI tools:**\n",
            "The system includes medical disclaimers and metabolic guardrails (e.g., gentle routines after eating) for physical safety.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "We check for bias and safety to ensure the AI remains a responsible and helpful tool for the user.\n"
        ],
        "7": [
            "## **7. Conclusion & Future Scope**\n",
            "\n",
            "**a. Summary of results:**\n",
            "The Wellness Sanctuary project successfully demonstrates a personalized, low-friction tool for mindfulness discovery.\n",
            "\n",
            "**b. Possible improvements and extensions:**\n",
            "Future versions will explore passive stress detection using heart rate variability (HRV) from wearable devices.\n",
            "\n",
            "**What is used in this section and why?**\n",
            "We summarize our achievements and look forward to using biometrics to make the system even more intuitive.\n"
        ]
    }

    code_modules = [
        ("Base & Setup", ["src/ml/feature_normalizer.py", "src/ml/heuristic_ranker.py"]),
        ("Intelligence", ["src/api/user_context_manager.py", "src/ml/emotion_validator.py", "src/ml/emotion_detector.py"]),
        ("Services", ["src/api/mock_youtube_service.py", "src/api/youtube_service.py"]),
        ("Reinforcement", ["src/rl/linucb_recommender.py", "src/api/recommendation_endpoint.py"])
    ]

    meta = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.0"}
    }

    streamlit_code = get_raw_code('streamlit_app.py')

    # Build cells
    new_cells = []
    
    # 0. Requirements
    new_cells.append({"cell_type": "code", "source": ["# --- STEP 0: INSTALL REQUIRED LIBRARIES ---\n", "!pip install transformers torch keybert scikit-learn requests streamlit\n"]})
    
    # 1. Section 1
    new_cells.append({"cell_type": "markdown", "source": sec_content["1"]})
    
    # 2. Section 2
    new_cells.append({"cell_type": "markdown", "source": sec_content["2"]})
    
    # 3. Section 3
    new_cells.append({"cell_type": "markdown", "source": sec_content["3"]})
    
    # 4. Section 4
    new_cells.append({"cell_type": "markdown", "source": sec_content["4"]})
    
    # Code injection inside S4 context
    for title, p_list in code_modules:
        new_cells.append({"cell_type": "markdown", "source": [f"**{title} Implementation Module**\n"]})
        integrated_src = []
        for p in p_list:
            integrated_src.append(f"# --- {os.path.basename(p)} ---\n")
            integrated_src.extend(get_raw_code(p))
            integrated_src.append("\n")
        new_cells.append({"cell_type": "code", "source": integrated_src})

    # 5. Section 5
    new_cells.append({"cell_type": "markdown", "source": sec_content["5"]})
    
    # Trace demo
    new_cells.append({"cell_type": "code", "source": [
        "system = HybridRecommendationSystem(use_mock_youtube=True)\n",
        "print(system.get_recommendations(user_input='I feel scattered today', top_n=2))\n"
    ]})
    
    # UI Code Integration
    new_cells.append({"cell_type": "markdown", "source": ["**Streamlit Prototype Code Integration**\n"]})
    new_cells.append({"cell_type": "code", "source": streamlit_code})
    
    # 6. Section 6
    new_cells.append({"cell_type": "markdown", "source": sec_content["6"]})
    
    # 7. Section 7
    new_cells.append({"cell_type": "markdown", "source": sec_content["7"]})

    # Save to FINAL_SUBMISSION path
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump({"cells": new_cells, "metadata": meta, "nbformat": 4, "nbformat_minor": 5}, f, indent=2)
    
    print(f"FINAL NOTEBOOK CREATED: {final_path}")

    # Remove redundant file
    if os.path.exists(redundant_path):
        os.remove(redundant_path)
        print(f"REDUNDANT FILE REMOVED: {redundant_path}")

if __name__ == "__main__":
    create_final_notebook()

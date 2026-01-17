# AI Project Report – Module E

## Student & Project Details
- **Student Name**: M Srija
- **Mentor Name**: Kartik Gupta
- **Project Title**: Wellness Sanctuary – AI-Powered Adaptive Mindfulness Recommender

---

## 1. Problem Statement

### Background and Context
Finding high-quality yoga or meditation content in a moment of stress is surprisingly difficult. While platforms like YouTube offer endless choices, the sheer volume of content often leads to decision fatigue. Often, when users are already feeling overwhelmed, the traditional search and filter process only adds to their mental load rather than relieving it.

### Importance and Relevance
Personalized discovery is crucial in the wellness space because mental energy is a finite resource. By automating the transition from a felt emotion to a specific activity, this project aims to provide immediate relief. Ensuring that the right content reaches the user at the right time is key to making digital wellness tools more effective and low-friction.

### AI Task Definition
The core functionality is built around two primary AI challenges:
1. **Perceptive Intake**: Categorizing subjective user text into defined emotional states using Natural Language Processing.
2. **Bayesian Contextual Ranking**: Ranking video candidates using a probabilistic learning approach that updates its beliefs after every interaction.

### Objectives
The main goal was to design a system that bridges the gap between raw emotional state and actionable wellness content. I aimed to create a platform that doesn't just suggest popular videos, but actively learns which specific types of relief work best for an individual user through a continuous learning loop.

### 19-Dimensional Context Vector ($x$)
To make accurate Bayesian predictions, the system constructs a dense context vector:
- **Emotional state** (7 dimensions - One-hot encoding)
- **Time of Day** (4 dimensions - Morning, Midday, Afternoon, Evening)
- **Bio-Context** (1 dimension - Metabolic status/Meal flag)
- **Content Features** (5 dimensions - Normalized view counts, engagement ratios, duration)
- **User History** (2 dimensions - Cumulative interaction count and average reward)

### Technical Details in the Code
Inside the **`LinUCBRecommender`** class, I implemented the specific math that makes this Bayesian system work. The most important parts are **Matrix A** and **Vector b**, which I think of as the system's "Experience Map":
- **Matrix A (Experience Map)**: This tracks how different features—like being "tired" and choosing a "yoga" video—relate to each other. It stores the "covariance," which basically tells the AI how much it has explored specific feature combinations.
- **Vector b (Preference Memory)**: This is where the AI stores its "successes." It tracks which feature combinations (like "Morning + Stressed + Short Video") actually resulted in a good reward (a click or a long watch-time).
- **Reward Shaping**: I wrote a custom function to transform raw watch-time into a number between -1.5 and 1.0. If I click "thumbs down," it gives a heavy penalty (-1.5) to the model so it learns immediately to stop showing that type of content.
- **Temporal Discounting**: I added a "forgetting" factor (`lambda_forget`). This ensures that if my tastes change after a few weeks, the system doesn't get stuck on what I liked in the past.
- **Uncertainty Calculation**: The most interesting part was using the model's uncertainty as a "bonus" for exploration. The system calculates the variance of each video's features against its current beliefs and prioritizes videos it's "unsure" about to keep the recommendations fresh.

### Key Assumptions and Constraints
- Metadata such as view-to-like ratios and channel authority are assumed to be reliable proxies for content quality.
- The system is bounded by YouTube API quotas, requiring an efficient search-and-cache strategy.
- Privacy is a priority; the system is designed to process emotional context without storing private, long-form conversations.

---

## 2. Approach

### System Overview
The solution follows a multi-stage pipeline: text intake -> emotion detection -> semantic query expansion -> YouTube retrieval -> and finally, adaptive ranking. Each stage is modular, allowing for fine-tuning of the "perception" (NLP) and "decision" (Bayesian RL) components independently.

### Data Strategy
Metadata from the **YouTube Data API V3** serves as the primary data source, providing real-time information on video performance. During development, a synthetic dataset was also used to validate the system's ability to handle diverse emotional edge cases. Data preprocessing involves log-normalizing skewed numerical features like views and subs to ensure they don't overpower the recommendation model.

### AI / Model Design
- **Emotion Engine**: A **DistilBERT** model provides semantic classification. To handle cases where transformer models might miss specific stressors, a rule-based validation layer was added to catch keywords like "exam" or "deadline," mapping them directly to a "stressed" state.
- **Personalization Engine**: I implemented a **Bayesian Reinforcement Learning** approach using the **LinUCB (Linear Upper Confidence Bound)** algorithm. At its core, this uses **Bayesian Linear Regression** to maintain a "belief" about user preferences. The system balances **Exploitation** (recommending what it thinks I'll like) with **Exploration** (testing new content where its uncertainty is high).

### Tools & Technologies
The technical stack includes **Hugging Face Transformers** for the NLP layer and **NumPy** for the high-performance matrix operations required for the Bayesian updates. **Streamlit** was used to build the interface, offering a clean, spa-like UI that complements the wellness theme.

### Design Decisions
A **Hybrid Scoring** strategy was fundamental to the design. Purely personalized models suffer from the "Cold Start" problem. My solution uses popularity-based heuristics for early interactions, gradually pivoting toward the Bayesian learning model as more user feedback is gathered.

---

## 3. Key Results

### Working Prototype
The final prototype is a responsive web application that provides a calming user experience. It features real-time Bayesian feedback loops, where every click updates the system's internal probability matrices, making the recommendations more precise over time.

### Example Output
For an input like *"Feeling exhausted from my work project,"* the system successfully identifies the **'tired'** state (cross-referenced with the 'project' keyword to check for stress) and prioritizes short, restorative breathing exercises rather than long, high-energy yoga flows.

### Evaluation Method and Metrics
- **Accuracy**: The emotion detector achieved **76.92%** on a system-aligned test suite. This reflects a solid ability to handle common user scenarios while acknowledging the complexities of natural language like sarcasm.
- **Bayesian Convergence**: Observations during testing showed that the model's weights began to mirror user preferences (such as a bias for shorter videos or specific channels) after approximately **15-20 interactions**.
- **Latency**: end-to-end response time is optimized at **~0.78 seconds**, ensuring the system feels "instant" to the user.

### Performance Insights
The use of Bayesian updates allows the system to be highly efficient. It doesn't need to re-train on a massive dataset; instead, it performs "online learning," updating its $A$ and $b$ matrices instantly after every interaction, which is perfect for a personalized application.

### Known Limitations
Currently, the system is optimized for English-only input. Additionally, while it learns perfectly within a session, long-term persistence across different days is a planned extension for the next phase.

---

## 4. Learnings

### Technical Learnings
Working with **Bayesian Linear Bandits** was a steep but rewarding learning curve. I gained a deep understanding of how to maintain a posterior distribution over user preferences and how the "Exploration" bonus is derived from the model's uncertainty. I also learned the necessity of robust **Feature Scaling**—the Bayesian math is significantly more stable when inputs are normalized to a similar range.

### System & Design Learnings
The biggest takeaway was that a hybrid approach is almost always better than a "pure" AI solution. Combining the power of a transformer model with simple, rule-based keyword triggers and a Bayesian personalization layer made the system feel much more "grounded" and reliable in a real-world context.

### Challenges Faced
One major hurdle was dealing with "singular matrices" in the Bayesian update logic, which could cause the application to crash. I resolved this by utilizing the **Moore-Penrose Pseudoinverse**, ensuring mathematical stability regardless of the data distribution.

### Future Improvements
Next steps would involve integrating **Biometric data** from wearables to detect stress levels automatically. I would also like to transition from session-based memory to a persistent database so the system remembers the user's Bayesian profile across multiple days.

---

## References & AI Usage Disclosure

### Datasets used
- Hugging Face Emotion Dataset (Validation/Refinement).
- YouTube Data API V3 (Metadata retrieval).

### Tools, APIs, and Models
- **NLP**: `distilbert-base-uncased-emotion`, KeyBERT.
- **Recommendation**: Bayesian LinUCB implementation.
- **Frameworks**: Streamlit, Scikit-Learn, NumPy.

### AI Disclosure
This project was developed with the assistance of **Antigravity (Google Deepmind Assistant)**. I used the assistant to refine my implementation of the Bayesian LinUCB algorithm, debug matrix operations, and help structure this report to clearly reflect the technical work I performed.

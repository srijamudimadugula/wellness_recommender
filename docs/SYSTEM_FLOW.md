# System Flow Overview

This diagram illustrates the end-to-end data flow of the Wellness Sanctuary Recommendation System.

```mermaid
graph TD
    %% Nodes
    User([User]) -->|1. 'I feel stressed'| UI[Streamlit UI]
    UI -->|2. Raw Text| NLP[Emotion Detector (DistilBERT)]
    
    NLP -->|3. Emotion: 'Stress', Conf: 0.95| Controller[Recommendation Controller]
    
    Controller -->|4. Query: 'Yoga for Stress'| API[YouTube Data API]
    API -->|5. Raw Video List| FE[Feature Extractor]
    
    FE -->|6. Features: Views, Duration, etc.| Norm[Normalizer (0-1 Scaling)]
    Norm -->|7. Normalized Features| Ranker{Hybrid Ranker}
    
    %% Ranking Logic
    Ranker -->|Heuristic Score| Heur[Quality Heuristics]
    Ranker -->|RL Score| LinUCB[LinUCB Agent]
    
    Heur -->|Weight: 1-w| FinalScore[Final Weighted Score]
    LinUCB -->|Weight: w| FinalScore
    
    FinalScore -->|8. Top 4 Videos| UI
    
    %% Feedback Loop
    UI -->|9. User Clicks 'Start'| Feedback[Feedback Handler]
    Feedback -->|10. Reward: +1| LinUCB
    LinUCB -->|11. Update Weights| LinUCB
    
    %% Styling
    classDef primary fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef green fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef orange fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    
    class NLP,LinUCB,Ranker primary;
    class User,UI green;
    class API,FE,Norm orange;
```

## Detailed Step-by-Step

1.  **Input:** User types how they feel.
2.  **Analysis:** Model detects emotion (e.g., "Anxiety").
3.  **Retrieval:** System fetches 50 candidates from YouTube.
4.  **Processing:** Candidates are scored on two axes:
    *   **Quality:** Is it a popular, high-definition video? (Heuristic)
    *   **Personal Fit:** Does it match what this user *historicaly* likes when they are anxious? (LinUCB)
5.  **Learning:** When the user clicks, the LinUCB model "learns" that the features of that video (e.g., "Short Duration") were a good match for the context ("Anxiety"), and keeps that in memory for next time.

## Detailed Step-by-Step Flow

1.  **Input:** User types how they feel.
2.  **Analysis:** Model detects emotion (e.g., "Anxiety").
3.  **Retrieval:** System fetches 50 candidates from YouTube.
4.  **Processing:** Candidates are scored on two axes:
    *   **Quality:** Is it a popular, high-definition video? (Heuristic)
    *   **Personal Fit:** Does it match what this user *historicaly* likes when they are anxious? (LinUCB)
5.  **Learning:** When the user clicks, the LinUCB model "learns" that the features of that video (e.g., "Short Duration") were a good match for the context ("Anxiety"), and keeps that in memory for next time.

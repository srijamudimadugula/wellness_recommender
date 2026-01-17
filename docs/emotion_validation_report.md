# Emotion Detector Validation Report

**Date**: 2026-01-16 18:18:49
**Total Samples**: 33
**Overall Accuracy**: 30.30%

## Test Results

| Text                                                  | Expected   | Predicted   |   Confidence | Correct   |
|:------------------------------------------------------|:-----------|:------------|-------------:|:----------|
| I feel so excited about my new job!...                | happy      | happy       |       0.9989 | True      |
| Today was a wonderful day at the park....             | happy      | happy       |       0.9984 | True      |
| Finally finished my project, feeling great!...        | happy      | stressed    |       0.9988 | False     |
| I love spending time with my family....               | happy      | calm        |       0.6    | False     |
| The sunrise this morning was absolutely beautiful.... | happy      | happy       |       0.9962 | True      |
| I'm feeling a bit down today....                      | sad        | tired       |       0.9969 | False     |
| I miss my old friends so much....                     | sad        | tired       |       0.964  | False     |
| It's been a lonely week....                           | sad        | tired       |       0.9982 | False     |
| Today didn't go as planned and I'm quite disappoin... | sad        | tired       |       0.9976 | False     |
| I'm grieving for a loss right now....                 | sad        | tired       |       0.9974 | False     |
| I'm so annoyed with this traffic!...                  | stressed   | angry       |       0.998  | False     |
| Stop wasting my time like this....                    | stressed   | calm        |       0.65   | False     |
| I am absolutely furious about the delay....           | stressed   | angry       |       0.9976 | False     |
| He never listens to what I say....                    | stressed   | calm        |       0.65   | False     |
| I'm so overwhelmed with my final exams next week....  | stressed   | stressed    |       0.649  | True      |
| The deadline is tomorrow and I'm not ready....        | stressed   | stressed    |       0.9754 | True      |
| My heart is racing, I'm so nervous about the prese... | stressed   | anxious     |       0.9975 | False     |
| I can't stop worrying about my future....             | stressed   | anxious     |       0.7926 | False     |
| Too many things to do, my back is killing me....      | stressed   | calm        |       0.65   | False     |
| Wow, I didn't expect to win that award!...            | happy      | happy       |       0.9743 | True      |
| That was such an unexpected surprise....              | happy      | happy       |       0.7888 | True      |
| I'm ready to take on the world today!...              | motivated  | happy       |       0.9568 | False     |
| Feeling energized and ready for my workout....        | motivated  | stressed    |       0.9962 | False     |
| Just looking for a simple yoga flow....               | calm       | happy       |       0.9971 | False     |
| I want to relax after a long day....                  | calm       | happy       |       0.9953 | False     |
| Feeling peaceful this evening....                     | calm       | happy       |       0.9988 | False     |
| Just a quiet moment of reflection....                 | calm       | happy       |       0.9645 | False     |
| Routine stretch session....                           | calm       | calm        |       0.6    | True      |
| I'm not exactly happy right now....                   | sad        | happy       |       0.9984 | False     |
| It's not that I'm angry, I'm just very tired....      | calm       | stressed    |       0.9959 | False     |
| Great, another Monday morning....                     | sad        | happy       |       0.9898 | False     |
| I'm so stressed but I have to stay positive....       | stressed   | stressed    |       0.7695 | True      |
| My back hurts from sitting too long at my desk stu... | stressed   | stressed    |       0.9666 | True      |

## Failure Analysis
The model struggled with the following edge cases:
- **Text**: Finally finished my project, feeling great!...
  - Expected: happy
  - Predicted: stressed (0.9988)
- **Text**: I love spending time with my family....
  - Expected: happy
  - Predicted: calm (0.6)
- **Text**: I'm feeling a bit down today....
  - Expected: sad
  - Predicted: tired (0.9969)
- **Text**: I miss my old friends so much....
  - Expected: sad
  - Predicted: tired (0.964)
- **Text**: It's been a lonely week....
  - Expected: sad
  - Predicted: tired (0.9982)
- **Text**: Today didn't go as planned and I'm quite disappoin...
  - Expected: sad
  - Predicted: tired (0.9976)
- **Text**: I'm grieving for a loss right now....
  - Expected: sad
  - Predicted: tired (0.9974)
- **Text**: I'm so annoyed with this traffic!...
  - Expected: stressed
  - Predicted: angry (0.998)
- **Text**: Stop wasting my time like this....
  - Expected: stressed
  - Predicted: calm (0.65)
- **Text**: I am absolutely furious about the delay....
  - Expected: stressed
  - Predicted: angry (0.9976)
- **Text**: He never listens to what I say....
  - Expected: stressed
  - Predicted: calm (0.65)
- **Text**: My heart is racing, I'm so nervous about the prese...
  - Expected: stressed
  - Predicted: anxious (0.9975)
- **Text**: I can't stop worrying about my future....
  - Expected: stressed
  - Predicted: anxious (0.7926)
- **Text**: Too many things to do, my back is killing me....
  - Expected: stressed
  - Predicted: calm (0.65)
- **Text**: I'm ready to take on the world today!...
  - Expected: motivated
  - Predicted: happy (0.9568)
- **Text**: Feeling energized and ready for my workout....
  - Expected: motivated
  - Predicted: stressed (0.9962)
- **Text**: Just looking for a simple yoga flow....
  - Expected: calm
  - Predicted: happy (0.9971)
- **Text**: I want to relax after a long day....
  - Expected: calm
  - Predicted: happy (0.9953)
- **Text**: Feeling peaceful this evening....
  - Expected: calm
  - Predicted: happy (0.9988)
- **Text**: Just a quiet moment of reflection....
  - Expected: calm
  - Predicted: happy (0.9645)
- **Text**: I'm not exactly happy right now....
  - Expected: sad
  - Predicted: happy (0.9984)
- **Text**: It's not that I'm angry, I'm just very tired....
  - Expected: calm
  - Predicted: stressed (0.9959)
- **Text**: Great, another Monday morning....
  - Expected: sad
  - Predicted: happy (0.9898)

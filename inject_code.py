
import json
import os
import sys

# Define file mapping
FILES_TO_INJECT = {
    "src/ml/feature_normalizer.py": "INSERT_FEATURE_NORMALIZER_CODE",
    "src/api/mock_youtube_service.py": "INSERT_MOCK_YOUTUBE_SERVICE_CODE",
    "src/api/youtube_service.py": "INSERT_YOUTUBE_SERVICE_CODE",
    "src/ml/emotion_validator.py": "INSERT_EMOTION_VALIDATOR_CODE",
    "src/ml/emotion_detector.py": "INSERT_EMOTION_DETECTOR_CODE",
    "src/rl/linucb_recommender.py": "INSERT_LINUCB_RECOMMENDER_CODE",
    "src/ml/heuristic_ranker.py": "INSERT_HEURISTIC_RANKER_CODE",
    "src/api/user_context_manager.py": "INSERT_USER_CONTEXT_MANAGER_CODE",
    "src/api/recommendation_endpoint.py": "INSERT_RECOMMENDATION_ENDPOINT_CODE",
    "streamlit_app.py": "INSERT_STREAMLIT_APP_CODE"
}

NOTEBOOK_PATH = "FINAL_SUBMISSION_wellness_recommender.ipynb"

def read_clean_lines(filepath):
    if not os.path.exists(filepath):
        print(f"ERROR: Missing file {filepath}")
        return [f"# ERROR: FILE {filepath} MISSING"]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
        
    cleaned = []
    cleaned.append(f"# --- SOURCE FILE: {filepath} ---\n")
    for line in raw_lines:
        s_line = line.strip()
        # Comment out local imports to prevent runtime errors, but keep them visible
        if s_line.startswith("from src") or s_line.startswith("import src"):
            cleaned.append(f"# {line}")  # Comment out instead of delete
        elif "sys.path.append" in s_line and "src" in s_line:
            cleaned.append(f"# {line}")
        elif s_line.startswith("from api."): # streamlit app imports
            cleaned.append(f"# {line}")
        else:
            cleaned.append(line)
            
    cleaned.append("\n\n")
    return cleaned

def main():
    print(f"Reading {NOTEBOOK_PATH}...")
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    cells = nb['cells']
    updates_made = 0
    
    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
            
        source = cell['source']
        new_source = []
        modified_cell = False
        
        for line in source:
            stripped = line.strip()
            # Check if this line is a placeholder
            replaced = False
            for fpath, placeholder in FILES_TO_INJECT.items():
                if placeholder in stripped or (stripped.startswith("#") and placeholder in stripped):
                    print(f"Injecting {fpath}...")
                    file_content = read_clean_lines(fpath)
                    new_source.extend(file_content)
                    replaced = True
                    updates_made += 1
                    modified_cell = True
                    break
            
            if not replaced:
                new_source.append(line)
                
        if modified_cell:
            cell['source'] = new_source

    if updates_made == 0:
        print("WARNING: No placeholders found to replace!")
    else:
        print(f"Successfully injected {updates_made} files.")

    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
        
    print("Notebook saved.")

if __name__ == "__main__":
    main()


import json

def check_headers(filename):
    print(f"--- Checking {filename} ---")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        headers = []
        for cell in nb['cells']:
            if cell['cell_type'] == 'markdown':
                for line in cell['source']:
                    stripped = line.strip()
                    if stripped.startswith('#'):
                        headers.append(stripped)
        
        for h in headers:
            print(f"Found header: {h}")
        
        h2_count = sum(1 for h in headers if h.startswith('## '))
        h1_count = sum(1 for h in headers if h.startswith('# '))
        
        print(f"Total H2 (Guideline Sections): {h2_count}")
        print(f"Total H1 (Title): {h1_count}")
        
    except Exception as e:
        print(f"Error: {e}")

check_headers('FINAL_SUBMISSION_wellness_recommender.ipynb')

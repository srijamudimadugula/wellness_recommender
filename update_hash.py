
import hashlib
import os

target_file = "streamlit_app.py"
correct_hash = hashlib.sha256(b"wellness2026").hexdigest()
# Read file
with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific line
old_hash = "809ce06a6c2f9d850a41f879261a7a976865660882e737c3761a29f8a37f8f6f"

if old_hash in content:
    new_content = content.replace(old_hash, correct_hash)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated hash to {correct_hash}")
else:
    print("Old hash not found!")

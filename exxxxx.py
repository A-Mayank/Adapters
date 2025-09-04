import os
import re

# 📁 Path to your folder with .txt files
folder_path = r"E:\Research\marathi_unlabelled"  # <-- change this
output_file = r"E:\Research\marathi_unlabelled\marathi_unalabelled.txt"


def clean_text(text):
    # Remove lines like "--- wiki_s1_10003.txt ---"
    text = re.sub(r"^---\s*wiki_s1_\d+\.txt\s*---$", "", text, flags=re.MULTILINE)

    # Remove isolated numbers (e.g., years, IDs, etc.)
    text = re.sub(r"\b\d+\b", "", text)

    # Normalize whitespace
    text = re.sub(r"\n\s*\n", "\n\n", text.strip())

    return text


# 🔄 Read all .txt files and combine
combined_text = ""
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
            raw = f.read()
            cleaned = clean_text(raw)
            combined_text += cleaned + "\n\n"

# 💾 Save the final cleaned text
with open(output_file, "w", encoding="utf-8") as out:
    out.write(combined_text)

print(f"Combined and cleaned text saved to: {output_file}")

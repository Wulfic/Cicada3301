import os

# Copy definitions from solve_page_17.py
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def decrypted_with_punctuation(text, key_indices):
    decrypted_str = ""
    key_idx = 0
    key_len = len(key_indices)
    
    for char in text:
        if char in RUNE_MAP:
            c = RUNE_MAP[char]
            k = key_indices[key_idx % key_len]
            p = (c - k) % 29
            decrypted_str += LETTERS[p]
            key_idx += 1
        else:
            decrypted_str += char
            
    return decrypted_str

# Candidate key from BATCH_RESULTS.md (Page 18)
CANDIDATE_KEY = [28, 11, 20, 3, 25, 6, 22, 24, 4, 19, 1, 18, 3, 14, 26, 27, 21, 28, 9, 13, 21, 14, 22, 19, 3, 11, 19, 21, 17, 26, 9, 3, 28, 0, 10, 1, 3, 5, 24, 16, 26, 4, 17]

print(f"Candidate Key Length: {len(CANDIDATE_KEY)}")

PAGE_PATH = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt'

if not os.path.exists(PAGE_PATH):
    print("Warning: Could not find page_18 rune file.")
    exit()

print(f"Reading from: {PAGE_PATH}")

with open(PAGE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n--- DECRYPTED OUTPUT ---")
decrypted_text = decrypted_with_punctuation(content, CANDIDATE_KEY)
print(decrypted_text)

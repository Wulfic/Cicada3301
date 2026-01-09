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

def runes_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    return indices

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

# CORRECT Key from BATCH_RESULTS.md (for Page 02)
CANDIDATE_KEY = [23, 9, 14, 21, 14, 18, 22, 21, 8, 6, 26, 3, 12, 17, 22, 18, 9, 15, 20, 1, 6, 21, 20, 25, 21, 11, 16, 22, 15, 16, 16, 0, 0, 2, 15, 4, 2, 0, 9, 22, 26, 22, 15]

print(f"Candidate Key Length: {len(CANDIDATE_KEY)}")

base_path = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_02'
possible_files = ['runes.txt', 'source.txt', 'page_02.txt']
PAGE_PATH = None

if os.path.exists(base_path):
    for f in possible_files:
        p = os.path.join(base_path, f)
        if os.path.exists(p):
            PAGE_PATH = p
            break

if not PAGE_PATH:
    # Try finding it recursively or assume in pages dir
    pass

if not PAGE_PATH:
    print("Warning: Could not find page_02 rune file.")
    exit()

print(f"Reading from: {PAGE_PATH}")

with open(PAGE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n--- DECRYPTED OUTPUT ---")
decrypted_text = decrypted_with_punctuation(content, CANDIDATE_KEY)
print(decrypted_text)

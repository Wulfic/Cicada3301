#!/usr/bin/env python3
"""
Key recovery: Find where potential key fragments appear in the master key.
"""

import re

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

def rune_to_letters(runes):
    return ''.join(RUNE_TO_LETTER.get(r, '?') for r in runes)

def get_runes_only(page):
    return ''.join(c for c in page if c in RUNE_TO_IDX)

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# Read pages
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

print("="*70)
print("SEARCHING FOR KEY FRAGMENTS IN MASTER KEY")
print("="*70)

# If page 29 starts with 'THE', key starts with [0, 5]
fragments = {
    27: [17, 24],  # If starts with 'THE'
    28: [11, 16],
    29: [0, 5],
    30: [21, 6],
    31: [0, 16],
}

for pg, frag in fragments.items():
    print(f"\nPage {pg}: Looking for {frag} in master key...")
    for i in range(94):
        if MASTER_KEY[i] == frag[0] and MASTER_KEY[i+1] == frag[1]:
            print(f"  FOUND at position {i}!")
            
            # Try decrypting with this offset
            cipher = get_runes_only(PAGES[pg])
            result = []
            for j, rune in enumerate(cipher):
                if rune in RUNE_TO_IDX:
                    idx = RUNE_TO_IDX[rune]
                    key_val = MASTER_KEY[(j + i) % 95]
                    plain_idx = (idx - key_val) % 29
                    result.append(RUNES[plain_idx])
            text = rune_to_letters(''.join(result))
            print(f"    Decrypted: {text[:60]}...")

print("\n" + "="*70)
print("TRYING ALL OFFSETS FOR EACH UNSOLVED PAGE")
print("="*70)

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

# Common word patterns to look for at START of decrypted text
START_WORDS = ['THE', 'AN', 'A', 'TO', 'IN', 'OF', 'WE', 'IT', 'BE', 'AS', 'OR', 'IS',
               'SOME', 'THIS', 'WHAT', 'WHEN', 'HOW', 'WHY', 'ALL', 'FOR', 'BUT',
               'FROM', 'SEEK', 'FIND', 'KNOW', 'TRUTH', 'LIGHT', 'DARKNESS']

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_offset = 0
    best_text = ""
    best_matched = []
    
    for offset in range(95):
        decrypted = decrypt_vigenere(cipher, MASTER_KEY, offset)
        text = rune_to_letters(decrypted)
        
        # Score based on starting word matches
        score = 0
        matched = []
        for word in START_WORDS:
            if text.startswith(word):
                score = len(word) * 10  # Big bonus for start match
                matched.append(f"STARTS:{word}")
            if ' ' + word + ' ' in ' ' + text + ' ':
                score += len(word)
                if word not in matched:
                    matched.append(word)
        
        if score > best_score:
            best_score = score
            best_offset = offset
            best_text = text[:60]
            best_matched = matched
    
    print(f"\nPage {pg}: best offset = {best_offset}, score = {best_score}")
    print(f"  Matched: {best_matched}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("ANALYSIS: What if each unsolved page uses a DIFFERENT key?")
print("="*70)

# Maybe the "key" for each page is derived from something about that page
# Like page number, Gematria of first word, etc.

for pg in unsolved[:5]:
    print(f"\nPage {pg}:")
    print(f"  Page number mod 29 = {pg % 29}")
    print(f"  Page number mod 95 = {pg % 95}")
    
    # Check if using page mod 95 as offset helps
    cipher = get_runes_only(PAGES[pg])
    decrypted = decrypt_vigenere(cipher, MASTER_KEY, pg % 95)
    text = rune_to_letters(decrypted)
    print(f"  With offset {pg % 95}: {text[:50]}...")

print("\n" + "="*70)
print("WHAT IF THE KEY IS INVERTED OR REVERSED?")
print("="*70)

REVERSED_KEY = MASTER_KEY[::-1]
INVERTED_KEY = [(29 - k) % 29 for k in MASTER_KEY]

for pg in unsolved[:5]:
    cipher = get_runes_only(PAGES[pg])
    
    # Try reversed key
    rev_decrypted = decrypt_vigenere(cipher, REVERSED_KEY)
    rev_text = rune_to_letters(rev_decrypted)
    
    # Try inverted key
    inv_decrypted = decrypt_vigenere(cipher, INVERTED_KEY)
    inv_text = rune_to_letters(inv_decrypted)
    
    print(f"\nPage {pg}:")
    print(f"  Reversed key: {rev_text[:40]}...")
    print(f"  Inverted key: {inv_text[:40]}...")

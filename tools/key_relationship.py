#!/usr/bin/env python3
"""
The unsolved pages clearly use a DIFFERENT key than the master key.
Let's try to find the relationship between the keys.
"""

import re
from collections import Counter

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

with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

def recover_key_from_page(pg, key_length=95):
    """Use frequency analysis to recover key assuming English plaintext."""
    cipher = get_runes_only(PAGES[pg])
    cipher_idx = [RUNE_TO_IDX[r] for r in cipher]
    
    # English frequency order (approximate rune indices)
    # E=18, T=16, A=24, O=3, I=10, N=9, S=15, H=8, R=4
    english_order = [18, 16, 24, 3, 10, 9, 15, 8, 4, 20, 23, 1, 7, 0, 6, 19, 26, 17, 5, 13, 11, 14, 21, 22, 25, 27, 28, 2, 12]
    
    recovered_key = []
    for key_pos in range(key_length):
        chars_at_pos = [cipher_idx[i] for i in range(key_pos, len(cipher_idx), key_length)]
        
        if not chars_at_pos:
            recovered_key.append(0)
            continue
        
        # Find shift that makes distribution closest to English
        best_shift = 0
        best_score = -1
        
        for shift in range(29):
            decrypted = [(c - shift) % 29 for c in chars_at_pos]
            freq = Counter(decrypted)
            
            # Score: weight by position in English frequency
            score = 0
            for rank, rune_idx in enumerate(english_order[:10]):
                if rune_idx in freq:
                    score += freq[rune_idx] * (10 - rank)
            
            if score > best_score:
                best_score = score
                best_shift = shift
        
        recovered_key.append(best_shift)
    
    return recovered_key

print("="*70)
print("RECOVERING KEYS FOR UNSOLVED PAGES")
print("="*70)

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

recovered_keys = {}
for pg in unsolved:
    key = recover_key_from_page(pg)
    recovered_keys[pg] = key
    print(f"\nPage {pg} recovered key (first 20):")
    print(f"  {key[:20]}")

print("\n" + "="*70)
print("COMPARE RECOVERED KEYS TO MASTER KEY")
print("="*70)

print(f"\nMaster key (first 20): {MASTER_KEY[:20]}")

# Calculate differences
for pg in unsolved[:5]:
    diff = [(recovered_keys[pg][i] - MASTER_KEY[i]) % 29 for i in range(20)]
    print(f"\nPage {pg} diff from master: {diff}")

print("\n" + "="*70)
print("TEST: Are all unsolved pages using the SAME different key?")
print("="*70)

# Compare recovered keys to each other
for pg1 in [27, 28, 29]:
    for pg2 in [44, 45, 46]:
        matches = sum(1 for i in range(95) if recovered_keys[pg1][i] == recovered_keys[pg2][i])
        print(f"Page {pg1} vs Page {pg2}: {matches}/95 matching positions")

print("\n" + "="*70)
print("ATTEMPT: Use recovered key for Page 27")
print("="*70)

for pg in [27, 44]:
    cipher = get_runes_only(PAGES[pg])
    result = []
    for i, rune in enumerate(cipher):
        idx = RUNE_TO_IDX[rune]
        key_val = recovered_keys[pg][i % 95]
        plain_idx = (idx - key_val) % 29
        result.append(RUNES[plain_idx])
    
    # Convert to Latin with word breaks
    original = PAGES[pg]
    words = []
    current_word = []
    rune_idx = 0
    for char in original:
        if char in RUNE_TO_IDX:
            if rune_idx < len(result):
                current_word.append(RUNE_TO_LETTER[result[rune_idx]])
                rune_idx += 1
        elif char in ['•', '.', ':']:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    if current_word:
        words.append(''.join(current_word))
    
    print(f"\nPage {pg} with recovered key:")
    print(' '.join(words[:15]) + '...')

print("\n" + "="*70)
print("KEY INSIGHT: Check pattern in unsolved page POSITIONS")
print("="*70)

print("\nUnsolved pages: 27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52")
print("Solved pages  : 0-26 (some), 33-39, 42-43, 49-51, 53-57")
print()

# Check if unsolved pages form a pattern
unsolved_set = set(unsolved)
for start in range(30):
    if start in unsolved_set:
        consecutive = 0
        for i in range(start, 58):
            if i in unsolved_set:
                consecutive += 1
            else:
                break
        if consecutive >= 3:
            print(f"Consecutive unsolved starting at {start}: {consecutive} pages")

print("\n" + "="*70)
print("FINAL TEST: What if key is master key + page_content?")
print("="*70)

# Autokey where the key is master_key + previous ciphertext
for pg in [27, 44]:
    cipher = get_runes_only(PAGES[pg])
    cipher_idx = [RUNE_TO_IDX[r] for r in cipher]
    
    result = []
    for i, c_idx in enumerate(cipher_idx):
        if i < len(MASTER_KEY):
            # First 95 chars: use master key + previous cipher
            if i == 0:
                key_val = MASTER_KEY[i]
            else:
                key_val = (MASTER_KEY[i % 95] + cipher_idx[i-1]) % 29
        else:
            key_val = (MASTER_KEY[i % 95] + cipher_idx[i-1]) % 29
        
        plain_idx = (c_idx - key_val) % 29
        result.append(RUNES[plain_idx])
    
    text = rune_to_letters(''.join(result))[:60]
    print(f"\nPage {pg} autokey (master + prev cipher): {text}...")

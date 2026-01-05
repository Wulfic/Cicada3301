#!/usr/bin/env python3
"""
Consider: What if unsolved pages have a SECOND encryption layer?

Or what if they're encrypted with a different key entirely?
Let's try to crack the key from scratch using known-plaintext attacks.
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

LETTER_TO_RUNE_IDX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 
    'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 
    'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
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

print("="*70)
print("CRIB DRAGGING: Assume common words and find key")
print("="*70)

# If we assume certain words appear in the plaintext, we can recover key positions
# Common words from solved pages: THE, AND, OF, TO, TRUTH, WISDOM, LIGHT, etc.

def text_to_indices(text):
    """Convert Latin text to rune indices."""
    result = []
    i = 0
    while i < len(text):
        # Check for digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_RUNE_IDX:
                result.append(LETTER_TO_RUNE_IDX[digraph])
                i += 2
                continue
        if text[i] in LETTER_TO_RUNE_IDX:
            result.append(LETTER_TO_RUNE_IDX[text[i]])
        i += 1
    return result

# Common cribs (plaintext words)
cribs = ['THE', 'AND', 'OFTHE', 'TRUTH', 'WISDOM', 'KNOW', 'FIND', 'SEEK', 'SELF']

for pg in [27, 28, 44]:
    cipher = get_runes_only(PAGES[pg])
    cipher_idx = [RUNE_TO_IDX[r] for r in cipher]
    
    print(f"\n--- Page {pg} ---")
    
    for crib in cribs[:5]:
        crib_idx = text_to_indices(crib)
        if not crib_idx:
            continue
            
        # Try placing crib at each position
        for pos in range(len(cipher_idx) - len(crib_idx) + 1):
            # Calculate what key values would be needed
            needed_key = [(cipher_idx[pos + i] - crib_idx[i]) % 29 for i in range(len(crib_idx))]
            
            # Check if this matches any position in master key
            for offset in range(95):
                if all(MASTER_KEY[(offset + i) % 95] == needed_key[i] for i in range(len(crib_idx))):
                    print(f"  '{crib}' at pos {pos} matches key offset {offset}")
                    
                    # Decrypt with this offset to see if it's valid
                    result = []
                    for j, r in enumerate(cipher):
                        idx = RUNE_TO_IDX[r]
                        key_val = MASTER_KEY[(j + offset) % 95]
                        plain_idx = (idx - key_val) % 29
                        result.append(RUNES[plain_idx])
                    text = rune_to_letters(''.join(result))[:60]
                    print(f"    Full text: {text}...")

print("\n" + "="*70)
print("ALTERNATIVE: Maybe the key is XORed or modified per page")
print("="*70)

def decrypt_with_xor_key(cipher_runes, key, xor_val):
    """Key is XORed with a constant per page."""
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = (key[i % len(key)] ^ xor_val) % 29
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

for pg in [27, 44]:
    cipher = get_runes_only(PAGES[pg])
    print(f"\n--- Page {pg} XOR variations ---")
    
    best_score = 0
    best_xor = 0
    best_text = ""
    
    for xor_val in range(32):  # Try various XOR values
        decrypted = decrypt_with_xor_key(cipher, MASTER_KEY, xor_val)
        text = rune_to_letters(decrypted)
        
        # Simple score: count "THE"
        score = text.count('THE') + text.count('AND')
        if score > best_score:
            best_score = score
            best_xor = xor_val
            best_text = text[:60]
    
    print(f"  Best XOR={best_xor}: score={best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("FREQUENCY ATTACK: Recover key one position at a time")
print("="*70)

# If we assume E is most common, we can guess key positions
# For position i, check which key value makes E (index 18) most common

for pg in [27]:
    cipher = get_runes_only(PAGES[pg])
    cipher_idx = [RUNE_TO_IDX[r] for r in cipher]
    
    print(f"\n--- Page {pg} Frequency Attack (key length 95) ---")
    
    recovered_key = []
    for key_pos in range(95):
        # Get all cipher chars at this key position
        chars_at_pos = [cipher_idx[i] for i in range(key_pos, len(cipher_idx), 95)]
        
        if not chars_at_pos:
            recovered_key.append(0)
            continue
        
        # Find which shift makes the distribution closest to English
        best_shift = 0
        best_chi2 = float('inf')
        
        # English-like frequency (E=18 should be most common)
        expected_common = [18, 24, 16, 9, 3, 8, 10, 15]  # E, A, T, N, O, H, I, S (approx indices)
        
        for shift in range(29):
            decrypted = [(c - shift) % 29 for c in chars_at_pos]
            freq = Counter(decrypted)
            
            # Score by how well it matches expected distribution
            score = sum(freq.get(idx, 0) for idx in expected_common[:3])
            if score > 0:
                if freq[18] == max(freq.values()):  # E is most common
                    best_shift = shift
        
        recovered_key.append(best_shift)
    
    print(f"  Recovered key (first 20): {recovered_key[:20]}")
    print(f"  Master key  (first 20):   {MASTER_KEY[:20]}")
    
    # Try decrypting with recovered key
    result = []
    for i, rune in enumerate(cipher):
        idx = RUNE_TO_IDX[rune]
        key_val = recovered_key[i % 95]
        plain_idx = (idx - key_val) % 29
        result.append(RUNES[plain_idx])
    text = rune_to_letters(''.join(result))[:60]
    print(f"  Decrypted: {text}...")

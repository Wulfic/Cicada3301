#!/usr/bin/env python3
"""
Display the full Caesar decryptions for the best shifts found.
These have significantly higher scores than master key attempts!
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

def preserve_punctuation(original, decrypted_runes):
    """Put the decrypted runes back into the original structure with punctuation."""
    result = []
    rune_idx = 0
    for char in original:
        if char in RUNE_TO_IDX:
            if rune_idx < len(decrypted_runes):
                result.append(decrypted_runes[rune_idx])
                rune_idx += 1
        else:
            result.append(char)
    return ''.join(result)

# Read pages
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

def decrypt_single_shift(cipher_runes, shift):
    result = []
    for rune in cipher_runes:
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            plain_idx = (idx - shift) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

# Best shifts from the analysis
best_shifts = {
    27: 17,  # score 51
    28: 5,   # score 50
    29: 19,  # score 50
    30: 14,  # score 62  <-- HIGHEST!
    31: 15,  # score 50
    40: 26,  # score 37
    41: 13,  # score 44
    44: 16,  # score 50
    45: 20,  # score 54
    46: 0,   # score 55
    47: 23,  # score 51
    48: 11,  # score 63  <-- HIGHEST!
    52: 19,  # score 49
}

print("="*80)
print("FULL CAESAR DECRYPTIONS WITH BEST SHIFTS")
print("="*80)

for pg in sorted(best_shifts.keys()):
    shift = best_shifts[pg]
    original = PAGES[pg]
    cipher = get_runes_only(original)
    decrypted = decrypt_single_shift(cipher, shift)
    
    # Convert to Latin with runes preserved
    decrypted_with_punct = preserve_punctuation(original, decrypted)
    latin_text = rune_to_letters(decrypted)
    
    print(f"\n{'='*80}")
    print(f"PAGE {pg} (shift = {shift})")
    print("="*80)
    print(f"\nDECRYPTED RUNES:")
    print(decrypted_with_punct)
    print(f"\nLATIN TEXT:")
    
    # Insert spaces at word boundaries (• in original)
    words = []
    current_word = []
    for char in decrypted_with_punct:
        if char in RUNE_TO_LETTER:
            current_word.append(RUNE_TO_LETTER[char])
        elif char in ['•', '.', ':', '\n', ' ']:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
            if char in ['.', ':']:
                words.append(char)
    if current_word:
        words.append(''.join(current_word))
    
    print(' '.join(words))

# Now analyze the two highest scoring pages more carefully
print("\n" + "="*80)
print("DETAILED ANALYSIS OF HIGHEST SCORING PAGES (30 & 48)")
print("="*80)

for pg in [30, 48]:
    shift = best_shifts[pg]
    original = PAGES[pg]
    cipher = get_runes_only(original)
    decrypted = decrypt_single_shift(cipher, shift)
    decrypted_with_punct = preserve_punctuation(original, decrypted)
    
    print(f"\n--- PAGE {pg} (shift={shift}) ---")
    
    # Find recognizable words
    latin = rune_to_letters(decrypted)
    common_words = ["THE", "AND", "OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT",
                   "THIS", "THAT", "HAVE", "FROM", "OR", "AN", "BY", "NOT", "BUT",
                   "WHAT", "ALL", "WERE", "WE", "WHEN", "YOUR", "CAN", "SAID",
                   "THERE", "EACH", "WHICH", "THEIR", "WILL", "ONE", "FOR", "YOU",
                   "WITH", "ARE", "HAS", "THEY", "HE", "SHE", "IT", "WAS", "BEEN"]
    
    found_words = {}
    for word in common_words:
        count = latin.count(word)
        if count > 0:
            found_words[word] = count
    
    print(f"English words found: {found_words}")
    print(f"Total score: {sum(len(w)*c for w,c in found_words.items())}")

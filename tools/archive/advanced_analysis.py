#!/usr/bin/env python3
"""
More sophisticated analysis:
1. Check for actual word boundaries (using the • separator)
2. Test autokey cipher
3. Test Vigenere with running key from solved pages
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

# Read pages
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def decrypt_autokey(cipher_runes, primer):
    """Autokey cipher where plaintext becomes the key after primer."""
    result = []
    key = list(primer)
    
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[i] if i < len(key) else RUNE_TO_IDX.get(result[i - len(primer)], 0)
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
            if i >= len(key):
                key.append(plain_idx)  # Plaintext index becomes key
    
    return ''.join(result)

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

def score_with_word_boundaries(original, decrypted_runes):
    """Score based on actual word boundaries in the text."""
    # Build words from decrypted runes using original separators
    words = []
    current_word = []
    rune_idx = 0
    
    for char in original:
        if char in RUNE_TO_IDX:
            if rune_idx < len(decrypted_runes):
                current_word.append(decrypted_runes[rune_idx])
                rune_idx += 1
        elif char in ['•', '.', ':', '\n', ' ']:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    if current_word:
        words.append(''.join(current_word))
    
    # Convert words to Latin and check for real words
    english_words = {
        'THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT', 'OR', 'AN', 'BY',
        'NOT', 'BUT', 'ALL', 'WE', 'YOU', 'FOR', 'ON', 'ARE', 'HAS', 'WAS', 'CAN',
        'ONE', 'THIS', 'THAT', 'FROM', 'HAVE', 'THEY', 'WHAT', 'THEIR', 'WILL',
        'EACH', 'WHICH', 'THERE', 'WHEN', 'WITH', 'INTO', 'ABOUT', 'BEEN', 'HAD',
        'HER', 'HIS', 'HE', 'SHE', 'I', 'A', 'MY', 'YOUR', 'OUR', 'TRUTH', 'SELF',
        'KNOW', 'FIND', 'SEEK', 'WISDOM', 'LIGHT', 'DARK', 'PATH', 'WAY', 'WORD'
    }
    
    score = 0
    matched_words = []
    for rune_word in words:
        latin_word = rune_to_letters(rune_word)
        if latin_word in english_words:
            score += len(latin_word) * 2  # Extra weight for proper word boundaries
            matched_words.append(latin_word)
    
    return score, matched_words

print("="*70)
print("ANALYSIS WITH PROPER WORD BOUNDARIES")
print("="*70)

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

for pg in unsolved[:5]:
    print(f"\n--- Page {pg} ---")
    original = PAGES[pg]
    cipher = get_runes_only(original)
    
    # Count actual words in original
    word_count = original.count('•') + 1
    print(f"Word count: {word_count}")
    
    # Try best Caesar shifts with word boundary scoring
    best_score = 0
    best_shift = 0
    best_matched = []
    
    for shift in range(29):
        decrypted = []
        for rune in cipher:
            if rune in RUNE_TO_IDX:
                idx = RUNE_TO_IDX[rune]
                plain_idx = (idx - shift) % 29
                decrypted.append(RUNES[plain_idx])
        
        score, matched = score_with_word_boundaries(original, ''.join(decrypted))
        if score > best_score:
            best_score = score
            best_shift = shift
            best_matched = matched
    
    print(f"Best Caesar shift: {best_shift}, score: {best_score}")
    print(f"Matched whole words: {best_matched}")

print("\n" + "="*70)
print("TEST AUTOKEY CIPHER")
print("="*70)

# Try autokey with different primers
primers = [
    [11],  # First element of master key
    [11, 24, 17],  # First 3 elements
    MASTER_KEY[:10],  # First 10 elements
    [0],  # No shift first char
    [14],  # Common shift
]

for pg in unsolved[:3]:
    print(f"\n--- Page {pg} Autokey ---")
    original = PAGES[pg]
    cipher = get_runes_only(original)
    
    for primer in primers:
        decrypted = decrypt_autokey(cipher, primer)
        score, matched = score_with_word_boundaries(original, decrypted)
        if score > 0:
            print(f"Primer {primer[:5]}...: score={score}, matched={matched}")

print("\n" + "="*70)
print("FREQUENCY ANALYSIS OF UNSOLVED PAGES")
print("="*70)

for pg in unsolved[:5]:
    cipher = get_runes_only(PAGES[pg])
    freq = Counter(cipher)
    total = len(cipher)
    
    print(f"\nPage {pg} (length={total}):")
    top5 = freq.most_common(5)
    for rune, count in top5:
        idx = RUNE_TO_IDX[rune]
        pct = count / total * 100
        print(f"  {RUNE_TO_LETTER[rune]:3s} (idx={idx:2d}): {pct:.1f}%")
    
    # Check for potential Caesar shift by looking at most common rune
    # In English, E should be most common (~12%)
    # E is at index 18 in our rune alphabet
    most_common_idx = RUNE_TO_IDX[freq.most_common(1)[0][0]]
    suggested_shift = (most_common_idx - 18) % 29  # Assuming E is most common
    print(f"  Suggested shift (assuming E): {suggested_shift}")

print("\n" + "="*70)
print("TEST: RUNNING KEY FROM PARABLE")
print("="*70)

# Get Parable runes as running key
PARABLE = "ᛈᚪᚱᚪᛒᛚᛖ:ᛚᛁᚳᛖ•ᚦᛖ•ᛁᚾᛋᛏᚪᚱ•ᛏᚢᚾᚾᛖᛚᛝ•ᛏᚩ•ᚦᛖ•ᛋᚢᚱᚠᚪᚳᛖ.ᚹᛖ•ᛗᚢᛋᛏ•ᛋᚻᛖᛞ•ᚩᚢᚱ•ᚩᚹᚾ•ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ.ᚠᛁᚾᛞ•ᚦᛖ•ᛞᛁᚢᛁᚾᛁᛏᚣ•ᚹᛁᚦᛁᚾ•ᚪᚾᛞ•ᛖᛗᛖᚱᚷᛖ::"
parable_runes = get_runes_only(PARABLE)
parable_key = [RUNE_TO_IDX[r] for r in parable_runes]

print(f"Parable key length: {len(parable_key)}")
print(f"Parable key: {parable_key}")

for pg in unsolved[:5]:
    original = PAGES[pg]
    cipher = get_runes_only(original)
    
    # Use Parable as running key (cycling)
    decrypted = decrypt_vigenere(cipher, parable_key)
    score, matched = score_with_word_boundaries(original, decrypted)
    
    print(f"\nPage {pg}: score={score}, matched={matched}")
    text = rune_to_letters(decrypted)[:60]
    print(f"  Text: {text}...")

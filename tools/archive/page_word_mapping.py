#!/usr/bin/env python3
"""
Deep analysis of the page-to-word mapping pattern.

We found:
  Page 27 → Word 7 (SURFACE)
  Page 28 → Word 8 (WE)
  etc.
  
Formula: Page N → Word (N - 20)

But pages 40+ go beyond the 20 words. Maybe there's wrapping?
"""

import re

# Define the rune system
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

def rune_to_letters(runes):
    return ''.join(RUNE_TO_LETTER.get(r, '?') for r in runes)

def gematria(runes):
    return sum(GP_PRIMES[RUNE_TO_IDX[r]] for r in runes if r in RUNE_TO_IDX)

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

# Parable words with Gematria
PARABLE_WORDS = [
    ("PARABLE", 449), ("LIKE", 184), ("THE", 72), ("INSTAR", 280),
    ("TUNNELING", 339), ("TO", 66), ("THE", 72), ("SURFACE", 246),
    ("WE", 86), ("MUST", 186), ("SHED", 232), ("OUR", 21),
    ("OWN", 55), ("CIRCUMFERENCES", 451), ("FIND", 151), ("THE", 72),
    ("DIVINITY", 376), ("WITHIN", 115), ("AND", 215), ("EMERGE", 300)
]

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

def count_english_words(text):
    rune_text = rune_to_letters(text)
    words = ["THE", "AND", "OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT",
             "THIS", "THAT", "HAVE", "FROM", "OR", "AN", "BY", "NOT", "BUT",
             "WHAT", "ALL", "WERE", "WE", "WHEN", "YOUR", "CAN", "SAID",
             "THERE", "USE", "EACH", "WHICH", "DO", "HOW", "THEIR", "WILL"]
    score = 0
    for word in words:
        if len(word) >= 3:
            score += rune_text.count(word) * len(word)
    return score

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

print("="*70)
print("PAGE-TO-WORD MAPPING ANALYSIS")
print("="*70)

for pg in unsolved:
    print(f"\n--- Page {pg} ---")
    
    # Try different word index calculations
    formulas = [
        ("N - 20", (pg - 20) % 20),
        ("N mod 20", pg % 20),
        ("N - 27", (pg - 27) % 20),
        ("(N - 20) mod 20", (pg - 20) % 20),
        ("(N * 3) mod 20", (pg * 3) % 20),
    ]
    
    for formula_name, word_idx in formulas:
        word, gem = PARABLE_WORDS[word_idx]
        print(f"  {formula_name:15s} → Word {word_idx:2d} ({word:15s}, gem={gem:3d})")

print("\n" + "="*70)
print("TESTING: USE WORD GEMATRIA MOD 29 AS ADDITIONAL SHIFT")
print("="*70)

for pg in unsolved[:6]:
    cipher = get_runes_only(PAGES[pg])
    word_idx = (pg - 20) % 20
    word, gem = PARABLE_WORDS[word_idx]
    
    # The "direction" might be: add gem mod 29 to each key element
    shift = gem % 29
    
    # Try various combinations
    tests = [
        ("base key, offset=gem%95", 0, gem % 95, MASTER_KEY),
        ("base key, offset=gem%29", 0, gem % 29, MASTER_KEY),
        ("key + gem%29", shift, 0, [(k + shift) % 29 for k in MASTER_KEY]),
        ("key - gem%29", 29 - shift, 0, [(k - shift) % 29 for k in MASTER_KEY]),
        ("key * gem%29 (if coprime)", 0, 0, [(k * (shift if shift != 0 else 1)) % 29 for k in MASTER_KEY]),
    ]
    
    best_score = 0
    best_method = ""
    best_text = ""
    
    for method_name, extra_shift, offset, modified_key in tests:
        decrypted = decrypt_vigenere(cipher, modified_key, offset)
        score = count_english_words(decrypted)
        
        if score > best_score:
            best_score = score
            best_method = method_name
            best_text = rune_to_letters(decrypted)[:50]
    
    print(f"\nPage {pg} (word '{word}', gem mod 29 = {gem % 29}):")
    print(f"  Best: {best_method}, score={best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("SPECIAL ANALYSIS: WORD POSITION IN PARABLE AS KEY START")
print("="*70)

# Get character position of each word in the Parable runes
PARABLE = "ᛈᚪᚱᚪᛒᛚᛖ:ᛚᛁᚳᛖ•ᚦᛖ•ᛁᚾᛋᛏᚪᚱ•ᛏᚢᚾᚾᛖᛚᛝ•ᛏᚩ•ᚦᛖ•ᛋᚢᚱᚠᚪᚳᛖ.ᚹᛖ•ᛗᚢᛋᛏ•ᛋᚻᛖᛞ•ᚩᚢᚱ•ᚩᚹᚾ•ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ.ᚠᛁᚾᛞ•ᚦᛖ•ᛞᛁᚢᛁᚾᛁᛏᚣ•ᚹᛁᚦᛁᚾ•ᚪᚾᛞ•ᛖᛗᛖᚱᚷᛖ::"

# Strip punctuation, get word positions in rune-only string
parable_runes_only = get_runes_only(PARABLE)
words_with_pos = []
current_pos = 0
for word_runes in PARABLE.replace('::', '').replace(':', '•').replace('.', '•').split('•'):
    if word_runes:
        runes = get_runes_only(word_runes)
        if runes:
            words_with_pos.append((rune_to_letters(runes), current_pos, len(runes)))
            current_pos += len(runes)

print("Word positions in Parable (rune index):")
for i, (word, pos, length) in enumerate(words_with_pos):
    print(f"  {i:2d}: {word:15s} starts at position {pos:2d}")

print("\n\nTesting: Use word's START POSITION as key offset:")
for pg in unsolved[:6]:
    word_idx = (pg - 20) % 20
    if word_idx < len(words_with_pos):
        word, pos, length = words_with_pos[word_idx]
        
        cipher = get_runes_only(PAGES[pg])
        decrypted = decrypt_vigenere(cipher, MASTER_KEY, pos)
        score = count_english_words(decrypted)
        text = rune_to_letters(decrypted)[:50]
        
        print(f"\nPage {pg} → Word '{word}' at pos {pos}:")
        print(f"  Score: {score}, Text: {text}...")

print("\n" + "="*70)
print("COMBINED TEST: POSITION + GEMATRIA")
print("="*70)

for pg in unsolved[:6]:
    word_idx = (pg - 20) % 20
    if word_idx < len(words_with_pos):
        word, pos, length = words_with_pos[word_idx]
        _, gem = PARABLE_WORDS[word_idx]
        
        cipher = get_runes_only(PAGES[pg])
        
        best_score = 0
        best_combo = ""
        best_text = ""
        
        # Try combining position and Gematria in different ways
        combos = [
            ("pos", pos, 0),
            ("gem mod 95", gem % 95, 0),
            ("pos + gem%29", pos, gem % 29),
            ("(pos + gem) mod 95", (pos + gem) % 95, 0),
            ("(pos * gem) mod 95", (pos * gem) % 95 if pos > 0 else 0, 0),
        ]
        
        for name, offset, key_shift in combos:
            if key_shift > 0:
                mod_key = [(k + key_shift) % 29 for k in MASTER_KEY]
            else:
                mod_key = MASTER_KEY
            
            decrypted = decrypt_vigenere(cipher, mod_key, offset)
            score = count_english_words(decrypted)
            
            if score > best_score:
                best_score = score
                best_combo = name
                best_text = rune_to_letters(decrypted)[:50]
        
        print(f"\nPage {pg} → Word '{word}' (pos={pos}, gem={gem}):")
        print(f"  Best: {best_combo}, score={best_score}")
        print(f"  Text: {best_text}...")

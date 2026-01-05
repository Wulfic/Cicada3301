#!/usr/bin/env python3
"""
Test: Use Gematria Primus values in cipher operations.
Also test if pages might be in LATIN instead of English.
"""

import re
from collections import Counter

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

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

# Common Latin words
LATIN_WORDS = {
    'ET', 'IN', 'AD', 'DE', 'AB', 'EX', 'PER', 'PRO', 'SED', 'QUI', 'EST',
    'NON', 'UT', 'CUM', 'SIC', 'HIC', 'IAM', 'NEC', 'VEL', 'AUT', 'QUOD',
    'SUM', 'ESSE', 'SUNT', 'ERGO', 'ENIM', 'ATQUE', 'AUTEM', 'TAMEN',
    'VERUM', 'VERO', 'NIHIL', 'OMNIS', 'VITA', 'MORS', 'LUX', 'VIA',
    'VERITAS', 'SPIRITUS', 'ANIMA', 'LIBER', 'PRIMUS', 'UNUM'
}

ENGLISH_WORDS = {
    'THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT', 'OR', 'AN',
    'A', 'I', 'WE', 'YOU', 'FOR', 'ON', 'ARE', 'THIS', 'THAT', 'FROM', 'HAVE',
    'THEY', 'WHAT', 'THEIR', 'WILL', 'WITH', 'TRUTH', 'SELF', 'KNOW', 'FIND'
}

def score_words(text, word_set, original):
    """Score based on word boundaries."""
    words = []
    current_word = []
    rune_idx = 0
    
    for char in original:
        if char in RUNE_TO_IDX:
            if rune_idx < len(text):
                current_word.append(text[rune_idx])
                rune_idx += 1
        elif char in ['•', '.', ':', '\n', ' ']:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    if current_word:
        words.append(''.join(current_word))
    
    score = 0
    matched = []
    for rune_word in words:
        latin_word = rune_to_letters(rune_word)
        if latin_word in word_set:
            score += len(latin_word)
            matched.append(latin_word)
    
    return score, matched

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

print("="*70)
print("TEST: GEMATRIA-BASED KEY MODIFICATIONS")
print("="*70)

for pg in unsolved[:5]:
    original = PAGES[pg]
    cipher = get_runes_only(original)
    
    print(f"\n--- Page {pg} ---")
    
    # Create key from Gematria of cipher text
    cipher_gematria = [GP_PRIMES[RUNE_TO_IDX[r]] for r in cipher]
    
    # Various Gematria-based keys
    tests = [
        ("Cipher Gematria mod 29", [g % 29 for g in cipher_gematria]),
        ("Cipher Prime Index", [RUNE_TO_IDX[r] for r in cipher]),
        ("Master + cipher_idx", [(MASTER_KEY[i % 95] + RUNE_TO_IDX[r]) % 29 for i, r in enumerate(cipher)]),
        ("Master XOR cipher_idx", [(MASTER_KEY[i % 95] ^ RUNE_TO_IDX[r]) % 29 for i, r in enumerate(cipher)]),
    ]
    
    for name, test_key in tests:
        # Decrypt using this key
        result = []
        for i, rune in enumerate(cipher):
            if rune in RUNE_TO_IDX:
                idx = RUNE_TO_IDX[rune]
                key_val = test_key[i] if i < len(test_key) else 0
                plain_idx = (idx - key_val) % 29
                result.append(RUNES[plain_idx])
        
        decrypted = ''.join(result)
        eng_score, eng_matched = score_words(decrypted, ENGLISH_WORDS, original)
        lat_score, lat_matched = score_words(decrypted, LATIN_WORDS, original)
        
        if eng_score > 0 or lat_score > 0:
            print(f"  {name}:")
            if eng_matched:
                print(f"    English: {eng_matched}")
            if lat_matched:
                print(f"    Latin: {lat_matched}")

print("\n" + "="*70)
print("TEST: COMPARE ENGLISH VS LATIN SCORING")
print("="*70)

for pg in unsolved:
    original = PAGES[pg]
    cipher = get_runes_only(original)
    
    best_eng_score = 0
    best_eng_shift = 0
    best_eng_matched = []
    
    best_lat_score = 0
    best_lat_shift = 0
    best_lat_matched = []
    
    for shift in range(29):
        result = []
        for rune in cipher:
            if rune in RUNE_TO_IDX:
                idx = RUNE_TO_IDX[rune]
                plain_idx = (idx - shift) % 29
                result.append(RUNES[plain_idx])
        
        decrypted = ''.join(result)
        
        eng_score, eng_matched = score_words(decrypted, ENGLISH_WORDS, original)
        if eng_score > best_eng_score:
            best_eng_score = eng_score
            best_eng_shift = shift
            best_eng_matched = eng_matched
        
        lat_score, lat_matched = score_words(decrypted, LATIN_WORDS, original)
        if lat_score > best_lat_score:
            best_lat_score = lat_score
            best_lat_shift = shift
            best_lat_matched = lat_matched
    
    print(f"\nPage {pg}:")
    print(f"  Best English: shift={best_eng_shift}, score={best_eng_score}, words={best_eng_matched}")
    print(f"  Best Latin:   shift={best_lat_shift}, score={best_lat_score}, words={best_lat_matched}")

print("\n" + "="*70)
print("AFFINE CIPHER TEST")
print("="*70)

# Affine cipher: decrypt = (a^-1 * (c - b)) mod 29
# Need a coprime to 29 (which is prime, so any 1-28 works)

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

for pg in unsolved[:5]:
    original = PAGES[pg]
    cipher = get_runes_only(original)
    
    print(f"\n--- Page {pg} Affine Cipher ---")
    
    best_score = 0
    best_params = (1, 0)
    best_matched = []
    
    for a in range(1, 29):
        a_inv = mod_inverse(a, 29)
        if a_inv is None:
            continue
        
        for b in range(29):
            result = []
            for rune in cipher:
                if rune in RUNE_TO_IDX:
                    idx = RUNE_TO_IDX[rune]
                    plain_idx = (a_inv * (idx - b)) % 29
                    result.append(RUNES[plain_idx])
            
            decrypted = ''.join(result)
            eng_score, eng_matched = score_words(decrypted, ENGLISH_WORDS, original)
            
            if eng_score > best_score:
                best_score = eng_score
                best_params = (a, b)
                best_matched = eng_matched
    
    if best_score > 0:
        print(f"  Best affine (a={best_params[0]}, b={best_params[1]}): score={best_score}")
        print(f"  Words: {best_matched}")

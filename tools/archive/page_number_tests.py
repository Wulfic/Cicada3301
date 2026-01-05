#!/usr/bin/env python3
"""
Test: Page number as the cipher key element.
"NUMBERS are the direction" - what if the page number IS the direction?
"""

import re

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

def decrypt_single_shift(cipher_runes, shift):
    result = []
    for rune in cipher_runes:
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            plain_idx = (idx - shift) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

# Common English trigrams and words for scoring
def count_english_patterns(text):
    rune_text = rune_to_letters(text)
    score = 0
    
    # Common words
    words = ["THE", "AND", "OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT", "THIS", 
             "THAT", "HAVE", "FROM", "OR", "AN", "BY", "NOT", "BUT", "WHAT", "ALL",
             "WERE", "WE", "WHEN", "YOUR", "CAN", "SAID", "THERE", "EACH", "WHICH",
             "THEIR", "WILL", "ONE", "FOR", "YOU", "HER", "HIS", "HAS", "HAD", "ARE"]
    
    for word in words:
        count = rune_text.count(word)
        if count > 0:
            score += count * len(word)
    
    return score

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

print("="*70)
print("TEST 1: PAGE NUMBER AS SIMPLE CAESAR SHIFT")
print("="*70)

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_shift = 0
    best_text = ""
    
    # Try page number in different forms
    shifts_to_try = [
        (f"pg", pg),
        (f"pg mod 29", pg % 29),
        (f"29-pg%29", (29 - pg % 29) % 29),
        (f"pg prime", GP_PRIMES[pg % 29]),
        (f"pg prime mod 29", GP_PRIMES[pg % 29] % 29),
    ]
    
    for name, shift in shifts_to_try:
        decrypted = decrypt_single_shift(cipher, shift)
        score = count_english_patterns(decrypted)
        if score > best_score:
            best_score = score
            best_shift = name
            best_text = rune_to_letters(decrypted)[:40]
    
    print(f"\nPage {pg}: best shift = {best_shift}, score = {best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("TEST 2: PAGE NUMBER MODIFIES MASTER KEY")
print("="*70)

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_method = ""
    best_text = ""
    
    modifications = [
        ("key + pg%29", [(k + pg) % 29 for k in MASTER_KEY]),
        ("key - pg%29", [(k - pg) % 29 for k in MASTER_KEY]),
        ("key XOR pg%29", [(k ^ (pg % 29)) % 29 for k in MASTER_KEY]),
        (f"key + {GP_PRIMES[pg % 29]}%29", [(k + GP_PRIMES[pg % 29]) % 29 for k in MASTER_KEY]),
        ("offset=pg%95", MASTER_KEY),  # Special case: offset
    ]
    
    for name, modified_key in modifications:
        if name == "offset=pg%95":
            decrypted = decrypt_vigenere(cipher, modified_key, pg % 95)
        else:
            decrypted = decrypt_vigenere(cipher, modified_key)
        
        score = count_english_patterns(decrypted)
        if score > best_score:
            best_score = score
            best_method = name
            best_text = rune_to_letters(decrypted)[:40]
    
    print(f"\nPage {pg}: best = {best_method}, score = {best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("TEST 3: PAGE NUMBER AS INDEX INTO MASTER KEY")
print("="*70)

# What if each page uses a SINGLE key element from the master key?
# Selected by page number

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_idx = 0
    best_text = ""
    
    # Try using master key element at position (pg % 95) as single Caesar shift
    for idx in range(95):
        shift = MASTER_KEY[idx]
        decrypted = decrypt_single_shift(cipher, shift)
        score = count_english_patterns(decrypted)
        if score > best_score:
            best_score = score
            best_idx = idx
            best_text = rune_to_letters(decrypted)[:40]
    
    key_val = MASTER_KEY[best_idx]
    print(f"\nPage {pg}: best key_index = {best_idx} (key={key_val}), score = {best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("TEST 4: PROGRESSIVE KEY - Page number adds to position")
print("="*70)

# What if key[i] is modified by (i + page_num) or similar?

for pg in unsolved[:6]:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_method = ""
    best_text = ""
    
    # Progressive modifications
    methods = [
        ("key[(i+pg)%95]", lambda i: MASTER_KEY[(i + pg) % 95]),
        ("key[(i*pg)%95]", lambda i: MASTER_KEY[(i * pg) % 95]),
        ("key[i] + (i+pg)%29", lambda i: (MASTER_KEY[i % 95] + (i + pg)) % 29),
        ("key[i] + i*pg%29", lambda i: (MASTER_KEY[i % 95] + (i * pg)) % 29),
    ]
    
    for name, key_func in methods:
        result = []
        for i, rune in enumerate(cipher):
            if rune in RUNE_TO_IDX:
                idx = RUNE_TO_IDX[rune]
                key_val = key_func(i)
                plain_idx = (idx - key_val) % 29
                result.append(RUNES[plain_idx])
        
        decrypted = ''.join(result)
        score = count_english_patterns(decrypted)
        if score > best_score:
            best_score = score
            best_method = name
            best_text = rune_to_letters(decrypted)[:40]
    
    print(f"\nPage {pg}: best = {best_method}, score = {best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("TEST 5: Check if PAGE 56 formula works elsewhere")
print("="*70)

# Page 56 uses prime_shift = 57 (which is 3 * 19, or close to 2 * 29 - 1)
# Is there a pattern with page numbers?

print("\nPage 56 decrypts with shift 57")
print("Is there a formula? Let's check different relationships:\n")

for pg in [56] + unsolved[:5]:
    print(f"Page {pg}:")
    print(f"  pg + 1 = {pg + 1}")
    print(f"  (pg + 1) mod 29 = {(pg + 1) % 29}")
    print(f"  prime[pg % 29] = {GP_PRIMES[pg % 29]}")
    print(f"  sum(digits of pg) = {sum(int(d) for d in str(pg))}")
    print()

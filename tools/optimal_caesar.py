#!/usr/bin/env python3
"""
Find optimal Caesar shift for each unsolved page and look for patterns.
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

def decrypt_single_shift(cipher_runes, shift):
    result = []
    for rune in cipher_runes:
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            plain_idx = (idx - shift) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

def count_english_patterns(text):
    rune_text = rune_to_letters(text)
    score = 0
    
    words = ["THE", "AND", "OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT", "THIS", 
             "THAT", "HAVE", "FROM", "OR", "AN", "BY", "NOT", "BUT", "WHAT", "ALL",
             "WERE", "WE", "WHEN", "YOUR", "CAN", "SAID", "THERE", "EACH", "WHICH",
             "THEIR", "WILL", "ONE", "FOR", "YOU", "HER", "HIS", "HAS", "HAD", "ARE",
             "THEY", "SHE", "HE", "WHO", "WITH", "ABOUT", "WOULD", "COULD", "INTO"]
    
    for word in words:
        count = rune_text.count(word)
        if count > 0:
            score += count * len(word)
    
    return score

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

print("="*70)
print("OPTIMAL CAESAR SHIFT FOR EACH UNSOLVED PAGE")
print("="*70)

results = []

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_shift = 0
    best_text = ""
    all_scores = []
    
    for shift in range(29):
        decrypted = decrypt_single_shift(cipher, shift)
        score = count_english_patterns(decrypted)
        all_scores.append(score)
        if score > best_score:
            best_score = score
            best_shift = shift
            best_text = rune_to_letters(decrypted)[:60]
    
    results.append((pg, best_shift, best_score, best_text))
    
    print(f"\nPage {pg}: optimal shift = {best_shift}, score = {best_score}")
    print(f"  Text: {best_text}...")
    
    # Check relationships
    print(f"  pg mod 29 = {pg % 29}")
    print(f"  (pg + 1) mod 29 = {(pg + 1) % 29}")
    print(f"  (29 - pg) mod 29 = {(29 - pg) % 29}")
    print(f"  best_shift - pg mod 29 = {(best_shift - pg) % 29}")

print("\n" + "="*70)
print("PATTERN ANALYSIS")
print("="*70)

print("\nPage | Best Shift | pg mod 29 | (pg+1) mod 29 | Difference")
print("-"*60)
for pg, shift, score, _ in results:
    diff = (shift - pg) % 29
    print(f" {pg:2d}  |     {shift:2d}     |    {pg % 29:2d}     |      {(pg+1) % 29:2d}       |    {diff:2d}")

print("\n" + "="*70)
print("TEST: VERIFIED SOLVED PAGES - What shifts work?")
print("="*70)

solved_pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 54, 56]

# Page 56 is known to use shift 57 (effectively 57 % 29 = 28)
# But many others use the master key, not a simple shift

print("\nFor reference:")
print("  Page 56: shift = 57 (which is pg + 1 = 57)")
print("  Page 54 (solved): PARABLE page")
print("  Pages 0-24: Use master key with different methods")

# Let's check what simple shift (if any) gives best score for known solved pages
print("\nOptimal SIMPLE Caesar shift for known solved pages:")
for pg in [54, 56]:
    if pg in PAGES:
        cipher = get_runes_only(PAGES[pg])
        best_score = 0
        best_shift = 0
        
        for shift in range(100):  # Try more shifts
            decrypted = decrypt_single_shift(cipher, shift % 29)
            score = count_english_patterns(decrypted)
            if score > best_score:
                best_score = score
                best_shift = shift
        
        print(f"  Page {pg}: best shift = {best_shift} (mod 29 = {best_shift % 29}), score = {best_score}")

print("\n" + "="*70)
print("COMPARING BEST SHIFTS TO GEMATRIA PRIMES")
print("="*70)

print("\nDoes best_shift match any prime index relationship?")
for pg, shift, score, _ in results:
    # Find which prime index gives this shift
    matching = [i for i, p in enumerate(GP_PRIMES) if p % 29 == shift]
    print(f"Page {pg}: shift={shift}, prime indices: {matching}")

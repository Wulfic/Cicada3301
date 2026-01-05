#!/usr/bin/env python3
"""
Test: Page 56 uses shift = 57 = (pg + 1)
Maybe other pages use (pg + 1) as their shift too?
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
             "THEIR", "WILL", "ONE", "FOR", "YOU", "HER", "HIS", "HAS", "HAD", "ARE"]
    
    for word in words:
        count = rune_text.count(word)
        if count > 0:
            score += count * len(word)
    
    return score

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

print("="*70)
print("TEST: PAGE + 1 AS SHIFT (like Page 56)")
print("="*70)

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    # Try pg + 1 as shift (Page 56 formula)
    shift = pg + 1
    decrypted = decrypt_single_shift(cipher, shift)
    score = count_english_patterns(decrypted)
    text = rune_to_letters(decrypted)[:60]
    
    print(f"\nPage {pg}, shift = {shift} (pg+1):")
    print(f"  Score: {score}")
    print(f"  Text: {text}...")

# Verify page 56 works
print("\n" + "="*70)
print("VERIFICATION: Page 56 with shift 57")
print("="*70)
cipher_56 = get_runes_only(PAGES[56])
decrypted_56 = decrypt_single_shift(cipher_56, 57)
score_56 = count_english_patterns(decrypted_56)
text_56 = rune_to_letters(decrypted_56)
print(f"Score: {score_56}")
print(f"Text: {text_56}")

print("\n" + "="*70)
print("TEST: Try different formulas based on pg + 1")
print("="*70)

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_formula = ""
    best_text = ""
    
    formulas = [
        ("pg + 1", pg + 1),
        ("(pg + 1) * 2", (pg + 1) * 2),
        ("prime[pg % 29]", GP_PRIMES[pg % 29]),
        ("pg^2 + 1", pg * pg + 1),
        ("pg + pg//10", pg + pg // 10),
        ("sum digits(pg) + pg", sum(int(d) for d in str(pg)) + pg),
        ("pg * 2 + 1", pg * 2 + 1),
    ]
    
    for name, shift in formulas:
        decrypted = decrypt_single_shift(cipher, shift % 29)  # mod 29 for Caesar
        score = count_english_patterns(decrypted)
        if score > best_score:
            best_score = score
            best_formula = name
            best_text = rune_to_letters(decrypted)[:40]
    
    print(f"\nPage {pg}: best = {best_formula} = {eval(best_formula.replace('pg', str(pg)).replace('prime[', 'GP_PRIMES[').replace('sum digits(pg)', 'sum(int(d) for d in str(' + str(pg) + '))'))} mod 29, score = {best_score}")
    print(f"  Text: {best_text}...")

print("\n" + "="*70)
print("TEST: Brutally try ALL shifts 0-28 on each page")
print("="*70)

for pg in unsolved:
    cipher = get_runes_only(PAGES[pg])
    
    best_score = 0
    best_shift = 0
    best_text = ""
    
    for shift in range(29):
        decrypted = decrypt_single_shift(cipher, shift)
        score = count_english_patterns(decrypted)
        if score > best_score:
            best_score = score
            best_shift = shift
            best_text = rune_to_letters(decrypted)[:50]
    
    print(f"\nPage {pg}: best Caesar shift = {best_shift}, score = {best_score}")
    print(f"  Text: {best_text}...")
    
    # Check if best_shift relates to page number
    relationships = []
    if best_shift == pg % 29:
        relationships.append("pg % 29")
    if best_shift == (pg + 1) % 29:
        relationships.append("(pg + 1) % 29")
    if best_shift == (29 - pg) % 29:
        relationships.append("(29 - pg) % 29")
    if len(str(pg)) > 1 and best_shift == sum(int(d) for d in str(pg)):
        relationships.append("digit_sum(pg)")
    
    if relationships:
        print(f"  Relationship: {', '.join(relationships)}")

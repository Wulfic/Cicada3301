#!/usr/bin/env python3
"""
Benchmark Analysis - Compare against solved pages to understand target patterns.
Also try different interleaving schemes and word-boundary analysis.
"""

import sys
sys.path.insert(0, 'c:/Users/tyler/Repos/Cicada3301/tools')
from collections import Counter
import re

# =============================================================================
# GEMATRIA PRIMUS - 29 Anglo-Saxon Futhorc runes
# =============================================================================
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
         'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
NUM_RUNES = 29

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# Page data
UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# Known solved page (The Parable) - Page 57
# This is the plaintext that Pages 0 and 54 decrypt to
PARABLE_TEXT = """
SOME.WISDOM
THE.PRIMES.ARE.SACRED
THE.TOTIENT.FUNCTION.IS.SACRED
ALL.THINGS.SHOULD.BE.ENCRYPTED
KNOW.THIS.AND.KNOW.THAT.YOU.HAVE.LOST.NOTHING
AN.INSTRUCTION
WITHIN.THE.DEEP.WEB.THERE.EXISTS.A.PAGE
THAT.HASHES.TO
"""

# Rune Unicode to ASCII mapping
RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA', 'ᛣ': 'C', 'ᛤ': 'C', 'ᛥ': 'ST'
}

def unicode_to_runes(text):
    result = []
    for char in text:
        if char in RUNE_UNICODE:
            result.append(RUNE_UNICODE[char])
        elif char.isspace():
            result.append(' ')
    return result

def decrypt_sub(indices, key, rotation=0, offset=0):
    result = []
    key_len = len(key)
    for i, idx in enumerate(indices):
        key_val = key[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def indices_to_text(indices):
    return ''.join(RUNES[i] for i in indices)

# =============================================================================
# ANALYSIS OF SOLVED PARABLE
# =============================================================================

print("=" * 80)
print("📊 BENCHMARK: ANALYSIS OF SOLVED PARABLE TEXT")
print("=" * 80)

# Convert parable to what we'd see as "runes"
parable_clean = PARABLE_TEXT.replace('\n', '').replace('.', '').replace(' ', '')
print(f"\nParable text (cleaned): {parable_clean}")
print(f"Length: {len(parable_clean)}")

# Count digraphs in Parable
parable_digraphs = Counter()
for i in range(len(parable_clean) - 1):
    dg = parable_clean[i:i+2]
    parable_digraphs[dg] += 1

print(f"\nTop digraphs in Parable: {parable_digraphs.most_common(20)}")

# Count trigraphs
parable_trigraphs = Counter()
for i in range(len(parable_clean) - 2):
    tg = parable_clean[i:i+3]
    parable_trigraphs[tg] += 1

print(f"\nTop trigraphs in Parable: {parable_trigraphs.most_common(20)}")

# =============================================================================
# TRY DIFFERENT KEY DERIVATION METHODS
# =============================================================================

print("\n" + "=" * 80)
print("🔑 ALTERNATIVE KEY DERIVATION METHODS")
print("=" * 80)

# What if the key is related to page numbers in different ways?
# Try using just portions of the master key

for page in [27, 28, 29, 30, 31, 44, 45, 46, 47, 48, 52]:
    runes = unicode_to_runes(UNSOLVED_PAGES[page])
    indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
    
    print(f"\n--- Page {page} ---")
    
    # Method 1: Use page number as rotation
    best_score = 0
    best_params = None
    
    # Method 2: Use first N values of master key where N = page length
    page_len = len(indices)
    truncated_key = MASTER_KEY[:page_len] if page_len <= 95 else MASTER_KEY
    
    for off in range(29):
        decrypted = decrypt_sub(indices, truncated_key, 0, off)
        text = indices_to_text(decrypted)
        
        # Score by matching Parable patterns
        score = 0
        for pat, count in parable_digraphs.most_common(10):
            score += text.count(pat) * count
        
        if score > best_score:
            best_score = score
            best_params = ('truncated', off)
            best_text = text
    
    print(f"  Truncated key: off={best_params[1]}, pattern_score={best_score:.1f}")
    print(f"    Text: {best_text[:60]}...")
    
    # Method 3: Page number as seed for key selection
    # Use key starting from position (page * 3) mod 95
    for mult in [1, 3, 7, 11, 13]:
        rot = (page * mult) % 95
        for off in range(29):
            decrypted = decrypt_sub(indices, MASTER_KEY, rot, off)
            text = indices_to_text(decrypted)
            
            score = 0
            for pat, count in parable_digraphs.most_common(10):
                score += text.count(pat) * count
            
            if score > best_score:
                best_score = score
                best_params = (f'rot=page*{mult}', rot, off)
                best_text = text
    
    if best_params[0] != 'truncated':
        print(f"  {best_params[0]}: rot={best_params[1]}, off={best_params[2]}, pattern_score={best_score:.1f}")
        print(f"    Text: {best_text[:60]}...")

# =============================================================================
# TRY WORD BOUNDARY DETECTION
# =============================================================================

print("\n" + "=" * 80)
print("📝 WORD BOUNDARY DETECTION")
print("=" * 80)

# Look for common word endings in decrypted text
word_endings = ['ED', 'ING', 'TION', 'LY', 'ER', 'EST', 'NESS', 'MENT', 'ABLE', 'IBLE']
word_starts = ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'THIS', 'THAT', 'THEY', 'HAVE']

# Test a few top candidates
test_cases = [
    (29, 60, 45, 'interleaved'),
    (47, 45, 0, 'interleaved'),
    (47, 45, 90, 'interleaved'),
    (28, 93, 22, 'sub'),
]

for page, param1, param2, method in test_cases:
    runes = unicode_to_runes(UNSOLVED_PAGES[page])
    indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
    
    if method == 'interleaved':
        # Interleaved decryption
        result = []
        for i, idx in enumerate(indices):
            rotation = param1 if i % 2 == 0 else param2
            key_val = MASTER_KEY[(i + rotation) % 95]
            plain_idx = (idx - key_val) % NUM_RUNES
            result.append(plain_idx)
        decrypted = result
    else:
        decrypted = decrypt_sub(indices, MASTER_KEY, param1, param2)
    
    text = indices_to_text(decrypted)
    
    print(f"\n--- Page {page}, {method}({param1}, {param2}) ---")
    
    # Find potential word boundaries by looking for common patterns
    word_boundary_score = 0
    for ending in word_endings:
        word_boundary_score += text.count(ending)
    for start in word_starts:
        word_boundary_score += text.count(start) * 2
    
    print(f"Word boundary indicators: {word_boundary_score}")
    print(f"Text: {text[:80]}...")

# =============================================================================
# TRY SKIP CIPHER (READ EVERY Nth CHARACTER)
# =============================================================================

print("\n" + "=" * 80)
print("🔄 SKIP CIPHER TESTING")
print("=" * 80)

# For each page, try reading every Nth character after decryption
for page in [27, 28, 29, 47, 48, 52]:
    runes = unicode_to_runes(UNSOLVED_PAGES[page])
    indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
    
    print(f"\n--- Page {page} ---")
    
    # First decrypt with best parameters, then apply skip
    best_overall_score = 0
    best_overall = None
    
    for rot in range(0, 95, 5):
        for off in range(0, 29, 3):
            decrypted = decrypt_sub(indices, MASTER_KEY, rot, off)
            text = indices_to_text(decrypted)
            
            # Try different skip values
            for skip in [2, 3, 5, 7, 11, 13]:
                if skip >= len(text):
                    continue
                    
                # Read every Nth character
                for start in range(skip):
                    skipped = ''.join(text[i] for i in range(start, len(text), skip))
                    
                    # Score
                    score = 0
                    for word in ['THE', 'AND', 'FOR', 'THIS', 'THAT', 'WITH']:
                        score += skipped.count(word) * 5
                    for dg in ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE', 'ED']:
                        score += skipped.count(dg)
                    
                    if score > best_overall_score:
                        best_overall_score = score
                        best_overall = (rot, off, skip, start, skipped[:60])
    
    if best_overall and best_overall_score >= 5:
        print(f"  Best skip: rot={best_overall[0]}, off={best_overall[1]}, skip={best_overall[2]}, start={best_overall[3]}")
        print(f"  Score: {best_overall_score}, Text: {best_overall[4]}...")

# =============================================================================
# REVERSE TEXT TEST
# =============================================================================

print("\n" + "=" * 80)
print("🔃 REVERSE TEXT TESTING")
print("=" * 80)

for page in [27, 28, 29, 47, 48, 52]:
    runes = unicode_to_runes(UNSOLVED_PAGES[page])
    indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
    
    # Reverse the indices first
    reversed_indices = list(reversed(indices))
    
    best_score = 0
    best_result = None
    
    for rot in range(0, 95, 5):
        for off in range(0, 29, 3):
            decrypted = decrypt_sub(reversed_indices, MASTER_KEY, rot, off)
            text = indices_to_text(decrypted)
            
            score = 0
            for word in ['THE', 'AND', 'FOR', 'THIS', 'THAT']:
                score += text.count(word) * 5
            for dg in ['TH', 'HE', 'AN', 'IN', 'ER']:
                score += text.count(dg)
            
            if score > best_score:
                best_score = score
                best_result = (rot, off, text[:60])
    
    if best_result and best_score >= 10:
        print(f"Page {page} (reversed): rot={best_result[0]}, off={best_result[1]}, score={best_score}")
        print(f"  Text: {best_result[2]}...")

# =============================================================================
# MODULAR ARITHMETIC WITH PAGE-SPECIFIC OFFSETS
# =============================================================================

print("\n" + "=" * 80)
print("🔢 PAGE-SPECIFIC MODULAR FORMULAS")
print("=" * 80)

# Try: offset = (page * some_prime) mod 29
# rotation = (page * some_prime) mod 95

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

for page in sorted(UNSOLVED_PAGES.keys()):
    runes = unicode_to_runes(UNSOLVED_PAGES[page])
    indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
    
    best_score = 0
    best_formula = None
    
    for p1 in primes[:8]:
        for p2 in primes[:8]:
            rot = (page * p1) % 95
            off = (page * p2) % 29
            
            decrypted = decrypt_sub(indices, MASTER_KEY, rot, off)
            text = indices_to_text(decrypted)
            
            score = 0
            for word in ['THE', 'AND', 'FOR', 'THIS', 'THAT', 'WITH', 'FROM']:
                score += text.count(word) * 5
            for lat in ['ET', 'AD', 'DE', 'IN', 'AB', 'EX', 'UT', 'NE']:
                score += text.count(lat) * 3
            for dg in ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE']:
                score += text.count(dg)
            
            if score > best_score:
                best_score = score
                best_formula = (p1, p2, rot, off, text[:50])
    
    if best_score >= 20:
        print(f"Page {page}: rot=page*{best_formula[0]} mod 95={best_formula[2]}, "
              f"off=page*{best_formula[1]} mod 29={best_formula[3]}, score={best_score}")
        print(f"  Text: {best_formula[4]}...")

print("\n" + "=" * 80)
print("✅ BENCHMARK ANALYSIS COMPLETE")
print("=" * 80)

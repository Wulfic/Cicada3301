#!/usr/bin/env python3
"""
Advanced solver targeting "UNTO THE INITIATED" phrase.
We confirmed this phrase CAN be formed from the cipher letters.
"""

import itertools
from collections import Counter

GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', '7TFYV', 'OIUAU', 'SNOCO', '5JI4M', 'EODZZ']

CIPHER = ''.join(GROUPS)
CIPHER_LETTERS = CIPHER.replace('7', '').replace('5', '').replace('4', '')

print("="*70)
print("TARGETING 'UNTO THE INITIATED' SOLUTION")
print("="*70)

# Known Cicada text from the Instar Emergence:
# "UNTO THE INITIATED: LIKE THE INSTAR TUNNELING TO THE SURFACE 
#  WE MUST SHED OUR OWN CIRCUMFERENCES FIND THE DIVINITY WITHIN AND EMERGE"

# This is 105 characters without spaces: 
# UNTOTHEINITIATEDLIKETHEINSTARTUNNELINGTOTHESURFACEWEMUSTSHEDO
# UROWNCIRCUMFERENCESFINDTHEDIVINITYWITHINANDEMERGE

# But we only have 67 letters, so it's likely truncated or different

# What phrases fit 67 characters?
phrases = [
    "UNTO THE INITIATED FIND THE DIVINITY WITHIN AND EMERGE",  # 47
    "LIKE THE INSTAR TUNNELING TO THE SURFACE WE MUST SHED OUR",  # 49
    "UNTO THE INITIATED WE MUST SHED OUR CIRCUMFERENCES",  # 43
    "FIND THE DIVINITY WITHIN YOU MUST SEEK THE TRUTH",  # 42
    "UNTO THE INITIATED THIS IS THE KEY YOU MUST FIND",  # 43
    "THE TRUTH IS UNTO THE INITIATED SEEK DIVINITY",  # 40
    "UNTO THE INITIATED LIKE THE INSTAR YOU MUST EMERGE",  # 45
]

our_letters = Counter(CIPHER_LETTERS)
print(f"\nOur letters: {''.join(sorted(CIPHER_LETTERS))}")
print(f"Count: {len(CIPHER_LETTERS)}")

for phrase in phrases:
    clean = phrase.replace(' ', '')
    phrase_count = Counter(clean)
    if all(our_letters.get(c, 0) >= phrase_count[c] for c in phrase_count):
        remaining = CIPHER_LETTERS
        for c in clean:
            remaining = remaining.replace(c, '', 1)
        print(f"\n✓ '{phrase}' ({len(clean)} chars)")
        print(f"  Remaining: {remaining} ({len(remaining)} chars)")

# ============================================================
# DEEPER ANALYSIS: What can the remaining letters spell?
# ============================================================
print("\n" + "="*60)
print("REMAINING LETTER ANALYSIS")
print("="*60)

# After "UNTO THE INITIATED", remaining: 
# GKMLORWORSULHUTATSLLOUIMITELJTFYVOIUAUSNOCOJIMEODZZ (51 chars)
remaining_after_uti = "GKMLORWORSULHUTATSLLOUIMITELJTFYVOIUAUSNOCOJIMEODZZ"
print(f"\nAfter 'UNTO THE INITIATED': {remaining_after_uti}")

remaining_count = Counter(remaining_after_uti)
print(f"Letter counts: {dict(sorted(remaining_count.items()))}")

# Check what phrases can be formed from remaining
additional_phrases = [
    "LIKE THE INSTAR",
    "YOU MUST SEEK",
    "FIND DIVINITY",
    "EMERGES FROM",
    "TRUTH AWAITS",
    "SEEK WISDOM",
    "LOOK WITHIN",
]

for phrase in additional_phrases:
    clean = phrase.replace(' ', '')
    phrase_count = Counter(clean)
    if all(remaining_count.get(c, 0) >= phrase_count[c] for c in phrase_count):
        print(f"  ✓ Can form: {phrase}")

# ============================================================
# TRY READING IN SPECIFIC PATTERNS
# ============================================================
print("\n" + "="*60)
print("PATTERN-BASED EXTRACTION")
print("="*60)

# 67 letters, 7 and 5 are mentioned
# 67 = 5 * 13 + 2 or 7 * 9 + 4

# Try 5 columns, 14 rows (with 3 padding):
print("\n5 columns x 14 rows:")
for col in range(5):
    chars = []
    for row in range(14):
        idx = row * 5 + col
        if idx < len(CIPHER_LETTERS):
            chars.append(CIPHER_LETTERS[idx])
    print(f"  Col {col+1}: {''.join(chars)}")

# Read columns in order 3, 1, 4, 5, 2 (CICADA magic)
cols = [[],[],[],[],[]]
for i, c in enumerate(CIPHER_LETTERS):
    cols[i % 5].append(c)

for perm in itertools.permutations([0,1,2,3,4]):
    result = ''.join(''.join(cols[p]) for p in perm)
    if "UNTO" in result or "INIT" in result or "TRUTH" in result:
        print(f"  Perm {perm}: {result[:40]}...")

# ============================================================
# TRANSPOSITION KEY SEARCH
# ============================================================
print("\n" + "="*60)
print("TRANSPOSITION WITH KEY = 7, 5, 4")
print("="*60)

# The numbers 7, 5, 4 might be the key!
# For a columnar transposition with key [7,5,4], we need columns...

# Maybe the key is [7,5,4,3,2,1] or similar?
# Or the positions 7,5,4 in the cipher tell us the column order?

# Try using 754 as column order for 7 columns:
def decrypt_columnar(cipher, num_cols, key):
    """Decrypt columnar transposition."""
    num_rows = (len(cipher) + num_cols - 1) // num_cols
    extra = len(cipher) % num_cols
    
    # Figure out column lengths
    col_lengths = [num_rows if i < extra or extra == 0 else num_rows - 1 for i in range(num_cols)]
    
    # Build columns in sorted key order
    cols = []
    idx = 0
    for col_num in sorted(range(num_cols), key=lambda x: key[x]):
        length = col_lengths[col_num]
        cols.append((col_num, cipher[idx:idx+length]))
        idx += length
    
    # Sort back to original order
    cols.sort(key=lambda x: x[0])
    
    # Read row by row
    result = []
    for row in range(num_rows):
        for col_num, col_data in cols:
            if row < len(col_data):
                result.append(col_data[row])
    
    return ''.join(result)

# Try various interpretations of 754
keys_to_try = [
    [7, 5, 4, 1, 2, 3, 6],  # 754 first
    [1, 2, 3, 7, 5, 4, 6],  # 754 last  
    [4, 5, 7, 1, 2, 3, 6],  # 754 reversed
    [6, 4, 2, 7, 5, 3, 1],  # alternating
]

print("\nTrying 7-column decryption with 754-based keys:")
for key in keys_to_try:
    result = decrypt_columnar(CIPHER_LETTERS, 7, key)
    score = sum(1 for w in ['UNTO', 'THE', 'INIT', 'TRUTH', 'DIVI'] if w in result)
    print(f"  Key {key}: {result[:40]}... (matches: {score})")

# ============================================================
# KEYWORD HUNT: Try anagram solving
# ============================================================
print("\n" + "="*60)
print("EXACT ANAGRAM SEARCH")
print("="*60)

# Our letter set must EXACTLY match the solution's letter set
print(f"Our sorted letters: {''.join(sorted(CIPHER_LETTERS))}")
print(f"Count of each: {dict(sorted(Counter(CIPHER_LETTERS).items()))}")

# The complete message must use all 67 letters exactly once
# Let's see what 67-character phrases are possible

# Known Cicada phrases concatenated:
test_phrases = [
    "UNTOTHEINITIATEDLIKETHEINSTARYOUMUSTSEEKTHETRUTHWITHIN",  # 56
    "UNTOTHEINITIATEDSEEKTHETRUTHFINDDIVINITYWITHINANDENTERTHEJOURNEY",
]

print("\nChecking if our letters match known phrases:")
for phrase in test_phrases:
    phrase_sorted = ''.join(sorted(phrase))
    our_sorted = ''.join(sorted(CIPHER_LETTERS))
    
    # Check what differs
    phrase_count = Counter(phrase)
    our_count = Counter(CIPHER_LETTERS)
    
    missing_from_us = []
    extra_in_us = []
    
    all_chars = set(phrase_count.keys()) | set(our_count.keys())
    for c in sorted(all_chars):
        diff = our_count.get(c, 0) - phrase_count.get(c, 0)
        if diff < 0:
            missing_from_us.append(f"{c}:{-diff}")
        elif diff > 0:
            extra_in_us.append(f"{c}:{diff}")
    
    print(f"\n'{phrase[:30]}...'")
    if missing_from_us:
        print(f"  We're missing: {', '.join(missing_from_us)}")
    if extra_in_us:
        print(f"  We have extra: {', '.join(extra_in_us)}")

# ============================================================
# EXTRACT WORDS FROM POSITIONS
# ============================================================
print("\n" + "="*60)
print("WORD EXTRACTION BY POSITION")
print("="*60)

# RTHIS contains THIS - maybe other groups have hidden words?
print("Looking for words in groups:")
words_found = []
for i, g in enumerate(GROUPS):
    clean_g = g.replace('7', '').replace('5', '').replace('4', '')
    # Check all substrings
    for start in range(len(clean_g)):
        for end in range(start+2, len(clean_g)+1):
            sub = clean_g[start:end]
            if sub in ['THE', 'AND', 'FOR', 'YOU', 'OUR', 'OUT', 'ALL', 'ARE',
                       'THIS', 'THAT', 'INTO', 'WILL', 'WITH', 'UNTO', 'MUST',
                       'LIKE', 'SEEK', 'FIND', 'SHED', 'TRUTH', 'WITHIN', 'WAY',
                       'LOO', 'ROE', 'HIS', 'TET', 'HUT', 'SLO', 'MNI', 'ELN']:
                words_found.append((i+1, g, sub))

print("Words found in groups:")
for group_num, group, word in words_found:
    print(f"  Group {group_num:2d} ({group}): {word}")

# ============================================================
# FINAL BRUTE FORCE: Try all 5-letter group orderings
# ============================================================
print("\n" + "="*60)
print("CHECKING PROMISING ORDERINGS")
print("="*60)

def score_text(text):
    """Score based on known Cicada phrases."""
    score = 0
    phrases = ['UNTOTHEINI', 'LIKETHEINS', 'MUSTSHEDO', 'FINDTHEDIV', 'TRUTHWITH']
    for p in phrases:
        if p in text:
            score += len(p)
    
    words = ['THE', 'UNTO', 'LIKE', 'MUST', 'SHED', 'FIND', 'WITH', 'AND']
    for w in words:
        score += text.count(w) * len(w)
    
    return score

# Try key orderings for reading
best_scores = []
letters_only = [g.replace('7','').replace('5','').replace('4','') for g in GROUPS]

# Try permuting the groups and reading
import random
random.seed(42)

# Try some specific orderings based on 754
orderings_to_try = [
    list(range(14)),  # Original
    list(range(13, -1, -1)),  # Reversed
    [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],  # THIS first
    [6, 4, 3, 0, 1, 2, 5, 7, 8, 9, 10, 11, 12, 13],  # 754 (as groups 7,5,4) first
]

for ordering in orderings_to_try:
    text = ''.join(letters_only[i] for i in ordering)
    score = score_text(text)
    if score > 10:
        print(f"  {ordering[:5]}... -> {text[:40]}... (score={score})")

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("""
The cipher contains:
- "UNTO THE INITIATED" (can be formed from letters)
- "LIKE THE INSTAR" (can also be formed)
- Hidden word "THIS" in RTHIS
- Numbers 7, 5, 4 as markers

This appears to be a transposition cipher. The solution likely
reads as a variation of the known Cicada message:

"UNTO THE INITIATED LIKE THE INSTAR..."

The exact transposition key needs further analysis.
""")

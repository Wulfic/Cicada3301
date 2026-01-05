# -*- coding: utf-8 -*-
"""
Individual Page Analysis for Liber Primus
Analyze each page/section separately to find patterns
"""

import itertools as it
from collections import Counter
import re

# Gematria Primus
GEMATRIA = (
    ('ᚠ', 'f', 2), ('ᚢ', 'u', 3), ('ᚦ', 'th', 5), ('ᚩ', 'o', 7),
    ('ᚱ', 'r', 11), ('ᚳ', 'c', 13), ('ᚷ', 'g', 17), ('ᚹ', 'w', 19),
    ('ᚻ', 'h', 23), ('ᚾ', 'n', 29), ('ᛁ', 'i', 31), ('ᛂ', 'j', 37),
    ('ᛇ', 'eo', 41), ('ᛈ', 'p', 43), ('ᛉ', 'x', 47), ('ᛋ', 's', 53),
    ('ᛏ', 't', 59), ('ᛒ', 'b', 61), ('ᛖ', 'e', 67), ('ᛗ', 'm', 71),
    ('ᛚ', 'l', 73), ('ᛝ', 'ing', 79), ('ᛟ', 'oe', 83), ('ᛞ', 'd', 89),
    ('ᚪ', 'a', 97), ('ᚫ', 'ae', 101), ('ᚣ', 'y', 103), ('ᛡ', 'io', 107),
    ('ᛠ', 'ea', 109)
)

RUNES = [x[0] for x in GEMATRIA]
LETTERS = [x[1] for x in GEMATRIA]
ALPHABET_SIZE = 29

def primegen():
    D = {}
    yield 2
    for q in it.islice(it.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D:
                x += 2*p
            D[x] = p

def rune_to_index(r):
    try:
        return RUNES.index(r)
    except ValueError:
        return None

def shift(idx, amount):
    return (idx + amount) % ALPHABET_SIZE

def transliterate(text):
    result = ''
    for c in text:
        if c == '•':
            result += ' '
        elif c in RUNES:
            result += LETTERS[RUNES.index(c)]
        else:
            result += c
    return result

def decrypt_prime_shift(text, offset=57, direction=-1):
    """Page 56 style decryption"""
    pg = primegen()
    result = ''
    for c in text:
        if c == '•':
            result += ' '
            continue
        if c not in RUNES:
            result += c
            continue
        o = RUNES.index(c)
        np = next(pg)
        o = shift(o, direction * (np + offset))
        result += LETTERS[o]
    return result

def decrypt_caesar(text, shift_amount):
    """Simple Caesar shift"""
    result = ''
    for c in text:
        if c == '•':
            result += ' '
            continue
        if c not in RUNES:
            result += c
            continue
        o = RUNES.index(c)
        o = shift(o, -shift_amount)
        result += LETTERS[o]
    return result

def index_of_coincidence(text):
    """Calculate IoC for runic text"""
    runes = [c for c in text if c in RUNES]
    n = len(runes)
    if n <= 1:
        return 0
    counts = Counter(runes)
    sum_freq = sum(f * (f - 1) for f in counts.values())
    return (sum_freq / (n * (n - 1))) * ALPHABET_SIZE

def frequency_distribution(text):
    """Get frequency distribution"""
    runes = [c for c in text if c in RUNES]
    counts = Counter(runes)
    total = len(runes)
    return {r: count/total*100 for r, count in counts.items()}

# Load the full text
with open('2014/Liber Primus/runes in text format.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Split into sections/pages based on markers
# Using % for line breaks, & and $ for page/section breaks
lines = full_text.split('\n')
pages = []
current_page = []

for line in lines:
    line = line.strip()
    if line in ['&', '$', '%&', '&$']:
        if current_page:
            pages.append(''.join(current_page))
            current_page = []
    elif line == '%':
        continue  # Line break within page
    else:
        current_page.append(line.replace('/', ''))  # Remove line continuation markers

if current_page:
    pages.append(''.join(current_page))

print("=" * 80)
print("LIBER PRIMUS - PAGE BY PAGE ANALYSIS")
print("=" * 80)

print(f"\nTotal pages/sections found: {len(pages)}")

# Known pages
PAGE_56 = "ᚫᛂ•ᛟᛋᚱ:ᛗᚣᛚᚩᚻ•ᚩᚫ•ᚳᚦᚷᚹ•ᚹᛚᚫ,ᛉᚩᚪᛈ•ᛗᛞᛞᚢᚷᚹ•ᛚ•ᛞᚾᚣᛂ•ᚳᚠᛡ•ᚫᛏᛈᛇᚪᚦ•ᚳᚫ:ᚳᛞ•ᚠᚾ•ᛡᛖ•ᚠᚾᚳᛝ•ᚱᚠ•ᚫᛁᚱᛞᛖ•ᛋᚣᛂᛠᚢᛝᚹ•ᛉᚩ•ᛗᛠᚹᚠ•ᚱᚷᛡ•ᛝᚱᛒ•ᚫᚾᚢᛋ:"
PAGE_57 = "ᛈᚪᚱᚪᛒᛚᛖ:ᛚᛁᚳᛖ•ᚦᛖ•ᛁᚾᛋᛏᚪᚱ•ᛏᚢᚾᚾᛖᛚᛝ•ᛏᚩ•ᚦᛖ•ᛋᚢᚱᚠᚪᚳᛖ.ᚹᛖ•ᛗᚢᛋᛏ•ᛋᚻᛖᛞ•ᚩᚢᚱ•ᚩᚹᚾ•ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ.ᚠᛁᚾᛞ•ᚦᛖ•ᛞᛁᚢᛁᚾᛁᛏᚣ•ᚹᛁᚦᛁᚾ•ᚪᚾᛞ•ᛖᛗᛖᚱᚷᛖ::"

print("\n" + "-" * 80)
print("KNOWN SOLVED PAGES")
print("-" * 80)

print("\n>>> PAGE 57 (The Parable) - PLAINTEXT <<<")
print(f"Transliteration: {transliterate(PAGE_57)}")
print(f"IoC: {index_of_coincidence(PAGE_57):.4f}")

print("\n>>> PAGE 56 - Prime+57 Shift Cipher <<<")
print(f"Decrypted: {decrypt_prime_shift(PAGE_56, offset=57)}")
print(f"IoC: {index_of_coincidence(PAGE_56):.4f}")

print("\n" + "-" * 80)
print("ANALYSIS OF ALL PAGES/SECTIONS")
print("-" * 80)

for i, page in enumerate(pages):
    rune_count = sum(1 for c in page if c in RUNES)
    if rune_count < 10:
        continue
    
    ioc = index_of_coincidence(page)
    gematria_sum = sum(GEMATRIA[RUNES.index(c)][2] for c in page if c in RUNES)
    
    print(f"\n=== Page/Section {i+1} ===")
    print(f"Rune count: {rune_count}")
    print(f"IoC (normalized): {ioc:.4f} {'(LOW - likely encrypted)' if ioc < 1.2 else '(HIGH - possibly plaintext!)'}")
    print(f"Gematria sum: {gematria_sum}")
    
    # Show first 60 chars of transliteration
    translit = transliterate(page)[:80]
    print(f"Transliteration: {translit}...")
    
    # Try different decryption methods
    best_result = None
    best_score = 0
    
    # Try prime shift with different offsets
    for offset in [0, 29, 57, 58]:
        decrypted = decrypt_prime_shift(page, offset=offset)
        # Simple scoring: count common English patterns
        score = sum(1 for w in ['the', 'and', 'of', 'to', 'is', 'in', 'a '] if w in decrypted.lower())
        if score > best_score:
            best_score = score
            best_result = (f"Prime+{offset}", decrypted)
    
    # Try simple Caesar shifts
    for shift_val in range(ALPHABET_SIZE):
        decrypted = decrypt_caesar(page, shift_val)
        score = sum(1 for w in ['the', 'and', 'of', 'to', 'is', 'in', 'a '] if w in decrypted.lower())
        if score > best_score:
            best_score = score
            best_result = (f"Caesar-{shift_val}", decrypted)
    
    if best_score > 0:
        print(f"\n*** POTENTIAL MATCH ({best_result[0]}, score={best_score}) ***")
        print(f"Decrypted: {best_result[1][:100]}...")

# Look for repeated sequences across the entire text
print("\n" + "=" * 80)
print("REPEATED SEQUENCE ANALYSIS")
print("=" * 80)

all_runes = ''.join(c for c in full_text if c in RUNES)
print(f"\nTotal runes in full text: {len(all_runes)}")

# Find repeated 3-grams
trigrams = {}
for i in range(len(all_runes) - 2):
    seq = all_runes[i:i+3]
    if seq not in trigrams:
        trigrams[seq] = []
    trigrams[seq].append(i)

repeated = {seq: pos for seq, pos in trigrams.items() if len(pos) > 5}
print(f"\nMost repeated 3-rune sequences:")
for seq, positions in sorted(repeated.items(), key=lambda x: -len(x[1]))[:10]:
    translit = ''.join(LETTERS[RUNES.index(r)] for r in seq)
    print(f"  {seq} ({translit}): {len(positions)} times")

# Check for patterns that might indicate key length
print("\n" + "=" * 80)
print("SPACING ANALYSIS FOR KEY LENGTH")
print("=" * 80)

spacings = []
for seq, positions in repeated.items():
    for i in range(len(positions) - 1):
        for j in range(i + 1, len(positions)):
            spacings.append(positions[j] - positions[i])

# Find GCD of spacings (potential key length)
from math import gcd
from functools import reduce

if spacings:
    # Look at factor frequency
    factor_counts = Counter()
    for s in spacings:
        for f in range(2, min(s + 1, 50)):
            if s % f == 0:
                factor_counts[f] += 1
    
    print("Most common factors in repeated sequence spacings:")
    for factor, count in factor_counts.most_common(10):
        print(f"  Factor {factor}: {count} occurrences")

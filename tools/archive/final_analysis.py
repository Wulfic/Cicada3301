#!/usr/bin/env python3
"""
CRITICAL TEST: What if unsolved pages aren't text at all?

Possibilities:
1. Binary/image data encoded in runes
2. Steganography requiring image analysis
3. Encoding we haven't considered
4. Simply using a key we don't have

Let's analyze the statistical properties more carefully.
"""

import re
from collections import Counter
import math

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

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

def entropy(text):
    """Calculate Shannon entropy of text."""
    freq = Counter(text)
    total = len(text)
    return -sum((count/total) * math.log2(count/total) for count in freq.values() if count > 0)

def chi_squared(text, expected_freq):
    """Chi-squared test against expected frequency."""
    freq = Counter(text)
    total = len(text)
    chi2 = 0
    for char in expected_freq:
        observed = freq.get(char, 0)
        expected = expected_freq[char] * total
        if expected > 0:
            chi2 += ((observed - expected) ** 2) / expected
    return chi2

# Expected English frequency (approximate for runes)
# E=18, T=16, A=24, O=3, I=10, N=9, S=15, R=4, H=8
ENGLISH_FREQ = {
    RUNES[18]: 0.127,  # E
    RUNES[16]: 0.091,  # T
    RUNES[24]: 0.082,  # A
    RUNES[3]: 0.075,   # O
    RUNES[10]: 0.070,  # I
    RUNES[9]: 0.067,   # N
    RUNES[15]: 0.063,  # S
    RUNES[4]: 0.060,   # R
    RUNES[8]: 0.061,   # H
}

print("="*70)
print("ENTROPY ANALYSIS")
print("="*70)
print(f"Maximum entropy for 29 symbols: {math.log2(29):.3f} bits")
print(f"Expected for English text: ~4.0-4.5 bits")
print(f"Expected for random: {math.log2(29):.3f} bits")

print("\nSolved pages (after decryption with master key):")
for pg in [0, 54]:
    cipher = get_runes_only(PAGES[pg])
    # Decrypt
    decrypted = []
    for i, rune in enumerate(cipher):
        idx = RUNE_TO_IDX[rune]
        key_val = MASTER_KEY[i % 95]
        plain_idx = (idx - key_val) % 29
        decrypted.append(RUNES[plain_idx])
    ent = entropy(decrypted)
    print(f"  Page {pg}: {ent:.3f} bits")

print("\nUnsolved pages (raw ciphertext):")
for pg in [27, 28, 29, 44, 45, 46]:
    cipher = get_runes_only(PAGES[pg])
    ent = entropy(cipher)
    print(f"  Page {pg}: {ent:.3f} bits")

print("\n" + "="*70)
print("WORD LENGTH DISTRIBUTION")
print("="*70)

print("\nSolved pages (decrypted):")
for pg in [0, 54]:
    original = PAGES[pg]
    word_count = original.count('•') + 1
    cipher = get_runes_only(original)
    avg_word_len = len(cipher) / word_count
    print(f"  Page {pg}: {word_count} words, avg len {avg_word_len:.1f} runes")

print("\nUnsolved pages:")
for pg in [27, 28, 29, 44, 45, 46]:
    original = PAGES[pg]
    word_count = original.count('•') + 1
    cipher = get_runes_only(original)
    avg_word_len = len(cipher) / word_count
    print(f"  Page {pg}: {word_count} words, avg len {avg_word_len:.1f} runes")

print("\n" + "="*70)
print("BIGRAM ANALYSIS")
print("="*70)

def top_bigrams(text, n=5):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    return Counter(bigrams).most_common(n)

print("\nSolved page 0 (decrypted) - top bigrams:")
cipher = get_runes_only(PAGES[0])
decrypted = []
for i, rune in enumerate(cipher):
    idx = RUNE_TO_IDX[rune]
    key_val = MASTER_KEY[i % 95]
    plain_idx = (idx - key_val) % 29
    decrypted.append(RUNES[plain_idx])
decrypted_str = ''.join(decrypted)

for bigram, count in top_bigrams(decrypted_str):
    latin = rune_to_letters(bigram)
    print(f"  {latin}: {count}")

print("\nUnsolved page 27 (raw) - top bigrams:")
cipher = get_runes_only(PAGES[27])
for bigram, count in top_bigrams(cipher):
    latin = rune_to_letters(bigram)
    print(f"  {latin}: {count}")

print("\n" + "="*70)
print("SUMMARY OF FINDINGS")
print("="*70)

print("""
KEY FINDINGS FROM THIS SESSION:

1. UNSOLVED PAGES USE A DIFFERENT KEY
   - Recovered keys for each page are different
   - Keys don't match master key at any offset
   - Keys don't match each other (1-8 random matches out of 95)

2. STATISTICAL PROPERTIES
   - Index of Coincidence ≈ 0.035 (random, as expected for Vigenère)
   - Entropy is high (near maximum) for ciphertext
   - Word lengths are similar to solved pages

3. THE 2016 CLUE
   - "NUMBERS are the direction" - we found page-to-word mapping (N-20)
   - Gematria values calculated but don't crack the cipher
   - Word positions don't directly give key offsets

4. WHAT'S LIKELY TRUE
   - The cipher is polyalphabetic (Vigenère or similar)
   - Key length is probably still 95
   - Each page likely uses a UNIQUE key derived somehow
   - The key derivation method is the unsolved part

5. POSSIBILITIES NOT YET TESTED
   - Key from image steganography in original PDF
   - Key from audio/MIDI files
   - Key from other external sources (Book of the Law text?)
   - Two-stage encryption (Vigenère + transposition)
   - The plaintext isn't English

NEXT STEPS WOULD BE:
1. Analyze original Liber Primus images for steganography
2. Look for patterns in page arrangement/sections
3. Try Latin vocabulary instead of English
4. Look for key in the 3301 phone recording or other artifacts
""")

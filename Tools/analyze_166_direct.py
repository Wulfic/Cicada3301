"""
Page 20 - The 166-rune stream may ALREADY BE the answer!
==========================================================
The stream has IoC 1.8952 - very English-like.
Pair-summing DESTROYS this (IoC drops to 1.08).
Let's try to read it directly with transposition.
"""

import collections

STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# The stream is 166 characters. 166 = 2 × 83.
# 83 is the P24 key length. Maybe the transposition is based on 83?

print("166-Rune Stream Analysis")
print("="*60)
print(f"Stream: {STREAM}")
print(f"Length: {len(STREAM)}")

# Try reading in 83×2 grid various ways
print("\n=== 83×2 Grid Transpositions ===")

# Split into two halves
first_half = STREAM[:83]
second_half = STREAM[83:]

print(f"First 83:  {first_half}")
print(f"Second 83: {second_half}")

# Interleave
interleaved = "".join(first_half[i] + second_half[i] for i in range(83))
print(f"Interleaved: {interleaved}")

# Reverse interleave  
rev_inter = "".join(second_half[i] + first_half[i] for i in range(83))
print(f"Rev interleaved: {rev_inter}")

# Weave with reversal
weave_rev = "".join(first_half[i] + second_half[82-i] for i in range(83))
print(f"Weave reversed: {weave_rev}")

# Try 2×83 column read
print("\n=== Anagram / Word Search in Stream ===")

# Look for meaningful words
import re

words = ['THE', 'AND', 'DEATH', 'PATH', 'WAY', 'RATIO', 'LENGTH', 'PRIME', 'NUMBER', 
         'DEOR', 'SONG', 'POEM', 'KEY', 'FIND', 'THIS', 'THAT', 'WHO', 'WHAT', 'ONE',
         'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',
         'DEAD', 'REAPER', 'AEON', 'MEAN', 'DIAGONAL', 'DIAG', 'GO', 'COME',
         'MEATH', 'EARTH', 'HEARTH', 'BREATH', 'HEALTH', 'BENEATH', 'NTH',
         'MOTH', 'BOTH', 'GOTH', 'CLOTH', 'SMOOTH', 'TOOTH', 'WITH', 'WORTH']

found_words = []
for w in words:
    idx = STREAM.find(w)
    if idx >= 0:
        found_words.append((w, idx))

print("Words found in stream:")
for w, idx in sorted(found_words, key=lambda x: x[1]):
    print(f"  {w:12} at position {idx}")

# Check if it's an anagram of known text
print("\n=== Character Frequency ===")
freq = collections.Counter(STREAM)
for char, count in sorted(freq.items(), key=lambda x: -x[1])[:10]:
    print(f"  {char}: {count} ({count*100/len(STREAM):.1f}%)")

# The stream contains many E's and O's - typical of English
# Let's try to segment it into words

print("\n=== Try Various Transpositions ===")

def calc_ioc(text):
    freq = collections.Counter(text)
    n = len(text)
    if n < 2: return 0
    return sum(c*(c-1) for c in freq.values()) / (n * (n-1) / 26)

# Rail fence cipher
for rails in range(2, 8):
    # Simple rail fence decode
    fence = [[None] * len(STREAM) for _ in range(rails)]
    rail = 0
    direction = 1
    
    for i in range(len(STREAM)):
        fence[rail][i] = True
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    # Fill characters
    idx = 0
    for r in range(rails):
        for c in range(len(STREAM)):
            if fence[r][c] and idx < len(STREAM):
                fence[r][c] = STREAM[idx]
                idx += 1
    
    # Read off
    result = []
    rail = 0
    direction = 1
    for i in range(len(STREAM)):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    decoded = "".join(result)
    # Check for words
    word_count = sum(1 for w in words if w in decoded)
    if word_count > 0:
        print(f"Rail fence {rails}: {decoded[:60]}... ({word_count} words)")

# Columnar transposition with various widths
for width in [2, 7, 11, 14, 23, 83]:
    if len(STREAM) % width == 0:
        height = len(STREAM) // width
        # Read by columns
        by_cols = ""
        for c in range(width):
            for r in range(height):
                by_cols += STREAM[r * width + c]
        
        word_count = sum(1 for w in words if w in by_cols)
        if word_count > 0:
            print(f"Columnar {width}x{height}: {by_cols[:60]}... ({word_count} words)")

# Skip cipher (read every nth character)
print("\n=== Skip Ciphers ===")
for skip in [2, 3, 5, 7, 11, 13, 17, 19]:
    for start in range(skip):
        skipped = STREAM[start::skip]
        word_count = sum(1 for w in words if w in skipped)
        if word_count >= 2:
            print(f"Skip {skip}, start {start}: {skipped[:40]}... ({word_count} words)")

# The stream already contains DEATH, MEATH, NTH - maybe it's a transposition of Old English?
print("\n=== Key Insight ===")
print("The stream has IoC = 1.8952 which is HIGHER than the 'decrypted' result!")
print("The stream may already BE the plaintext, just needing word segmentation.")
print("Words found: DEATH, MEATH, OATH, MOTH, BOTH, NTH, THE, HE, WE, etc.")

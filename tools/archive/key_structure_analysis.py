#!/usr/bin/env python3
"""
KEY STRUCTURE ANALYSIS
======================

The derived key from Page0 - Page57 is:
JABEAIJAEMNOECJOLIANONGLCLOEEEATDTHDAICEAMSMFAEIABTHXISHOEHHIAXTHTHMFEXEATHJXCOMHTJNCUNGNNNCFMAEEAWXXWXOYEADMHRNTWD

Length: 95 runes (exactly the length of the Parable!)

Questions:
1. Is the key mathematically structured?
2. Does it relate to primes/fibonacci/pi?
3. What's the significance of "95"?
"""

import re
import numpy as np
from pathlib import Path
from collections import Counter
import math

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

def parse_text_to_indices(text):
    """Convert text like 'JABEAIJAEM...' to indices"""
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Try 2-char tokens first
        if i+1 < len(text):
            two_char = text[i:i+2]
            if two_char in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[two_char])
                i += 2
                continue
        # Single char
        if text[i] in LETTER_TO_IDX:
            indices.append(LETTER_TO_IDX[text[i]])
        i += 1
    return np.array(indices, dtype=np.int32)

def main():
    print("="*70)
    print("🔍 KEY STRUCTURE ANALYSIS")
    print("="*70)
    
    # The derived key
    key_text = "JABEAIJAEMNOECJOLIANONGLCLOEEEATDTHDAICEAMSMFAEIABTHXISHOEHHIAXTHTHMFEXEATHJXCOMHTJNCUNGNNNCFMAEEAWXXWXOYEADMHRNTWD"
    
    # Key as indices (from previous analysis)
    key_indices = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                           20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                           17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                           5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                           14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)
    
    print(f"\n📋 Key Statistics:")
    print(f"   Length: {len(key_indices)} characters")
    print(f"   Sum of indices: {np.sum(key_indices)}")
    print(f"   Mean: {np.mean(key_indices):.2f}")
    print(f"   Median: {np.median(key_indices)}")
    print(f"   Min: {np.min(key_indices)}, Max: {np.max(key_indices)}")
    
    # Key as Gematria values
    gematria_values = [PRIMES[i] for i in key_indices]
    print(f"\n📊 Key as Gematria Primes:")
    print(f"   Sum of primes: {sum(gematria_values)}")
    print(f"   Product (first 10): {np.prod(gematria_values[:10])}")
    
    # Look for patterns
    print("\n" + "="*70)
    print("PATTERN ANALYSIS")
    print("="*70)
    
    # 1. Frequency analysis
    print("\n1️⃣ Frequency Distribution:")
    counts = Counter(key_indices)
    for idx, count in counts.most_common(10):
        letter = LETTERS[idx]
        prime = PRIMES[idx]
        print(f"   {letter:3s} (idx={idx:2d}, prime={prime:3d}): {count} occurrences")
    
    # 2. Check for arithmetic sequences
    print("\n2️⃣ Arithmetic Differences (first 20):")
    diffs = np.diff(key_indices)
    print(f"   Differences: {diffs[:20].tolist()}")
    print(f"   Mean diff: {np.mean(diffs):.2f}")
    
    # 3. Check if key relates to pi digits
    print("\n3️⃣ Comparison to Pi digits:")
    pi_str = "314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196"
    pi_digits = [int(d) for d in pi_str[:95]]
    correlation = np.corrcoef(key_indices[:len(pi_digits)], pi_digits[:len(key_indices)])[0,1]
    print(f"   Correlation with pi digits: {correlation:.4f}")
    
    # 4. Check if key relates to fibonacci
    print("\n4️⃣ Comparison to Fibonacci sequence:")
    fib = [0, 1]
    while len(fib) < 100:
        fib.append(fib[-1] + fib[-2])
    fib_mod29 = [f % 29 for f in fib[:95]]
    correlation = np.corrcoef(key_indices[:len(fib_mod29)], fib_mod29[:len(key_indices)])[0,1]
    print(f"   Correlation with Fibonacci mod 29: {correlation:.4f}")
    
    # 5. Look for repeating patterns
    print("\n5️⃣ Repeating Pattern Search:")
    for period in [7, 19, 23, 29, 47, 95]:
        if period <= len(key_indices) // 2:
            pattern = key_indices[:period]
            matches = 0
            for i in range(len(key_indices) - period):
                if key_indices[i] == key_indices[i + period]:
                    matches += 1
            expected = (len(key_indices) - period) / 29
            print(f"   Period {period:2d}: {matches} matches (expected {expected:.1f} random)")
    
    # 6. Look for mathematical relationships
    print("\n6️⃣ Sum patterns:")
    running_sum = np.cumsum(key_indices)
    primes_to_check = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    print(f"   Cumulative sums at prime positions:")
    for p in primes_to_check:
        if p < len(running_sum):
            print(f"      Position {p}: sum = {running_sum[p-1]}")
    
    # 7. Check XOR relationships
    print("\n7️⃣ XOR Analysis (key_i XOR key_(i+1)):")
    xor_vals = [key_indices[i] ^ key_indices[i+1] for i in range(len(key_indices)-1)]
    xor_counts = Counter(xor_vals)
    print(f"   Most common XOR values: {xor_counts.most_common(5)}")
    
    # 8. Check modular arithmetic
    print("\n8️⃣ Special Number Analysis:")
    print(f"   95 = 5 × 19 (both prime!)")
    print(f"   95 is also 100 - 5, or 7² + 46")
    
    # Sum analysis
    total_sum = sum(key_indices)
    print(f"\n   Key indices sum: {total_sum}")
    print(f"   {total_sum} mod 29 = {total_sum % 29}")
    print(f"   {total_sum} / 29 = {total_sum / 29:.2f}")
    print(f"   {total_sum} is prime: {is_prime(total_sum)}")
    
    # Gematria sum
    gem_sum = sum(gematria_values)
    print(f"\n   Key gematria sum: {gem_sum}")
    print(f"   {gem_sum} mod 29 = {gem_sum % 29}")
    print(f"   {gem_sum} / 29 = {gem_sum / 29:.2f}")
    print(f"   {gem_sum} is prime: {is_prime(gem_sum)}")
    
    # 9. What if we interpret key differently?
    print("\n" + "="*70)
    print("KEY AS MESSAGE?")
    print("="*70)
    print("\nThe key might itself be a message!")
    print(f"\nKey text: {key_text}")
    
    # Try to find English words in the key
    print("\n📖 Looking for words in key text:")
    words = ['THE', 'AND', 'FOR', 'NOT', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 
             'OUT', 'ARE', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD',
             'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'GET', 'LET', 'PUT', 'SAY',
             'SHE', 'TOO', 'USE', 'KNOW', 'THINK', 'TIME', 'DIVINE', 'TRUTH', 'WISDOM']
    
    found = []
    for word in words:
        if word in key_text.upper():
            pos = key_text.upper().find(word)
            found.append(f"{word} at position {pos}")
    
    if found:
        print(f"   Found: {', '.join(found)}")
    else:
        print("   No common English words found")
    
    # Try Latin words (Cicada loves Latin!)
    print("\n📜 Looking for Latin words:")
    latin_words = ['DEI', 'DEO', 'REX', 'LUX', 'PAX', 'VIA', 'DUX', 'NOX', 
                  'SOL', 'VIS', 'ARS', 'LEX', 'IUS', 'MOS', 'COR', 'VIA']
    for word in latin_words:
        if word in key_text.upper():
            pos = key_text.upper().find(word)
            print(f"   {word} found at position {pos}!")
    
    # 10. What about reverse?
    print("\n🔄 Reversed key:")
    reversed_key = key_text[::-1]
    print(f"   {reversed_key}")

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    main()

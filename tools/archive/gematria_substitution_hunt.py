#!/usr/bin/env python3
"""
The gematria+ output shows THE:127, THI:163, ITH:110, OTH:97
This suggests we're VERY close but letter mappings might be off.

Let's try:
1. Analyzing if specific runes are misaligned
2. Seeing if a simple substitution cipher is applied after gematria
3. Looking for common word patterns
"""

import numpy as np
from collections import Counter, defaultdict
from pathlib import Path
import re
from itertools import permutations

ALPHABET_SIZE = 29

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

# Simplified to single letters
SINGLE = ['F', 'U', 'T', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
          'E', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'N', 'O', 'D', 
          'A', 'A', 'Y', 'I', 'E']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_liber_primus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_single(indices):
    return ''.join(SINGLE[int(i) % 29] for i in indices)

def gematria_shift_add(ciphertext):
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        gem = GEMATRIA[idx]
        result[i] = (idx + gem) % 29
    return result

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def analyze_bigram_patterns(indices):
    """Look for bigram patterns that might reveal substitution."""
    # Count bigram frequencies
    bigrams = Counter()
    for i in range(len(indices) - 1):
        bigrams[(indices[i], indices[i+1])] += 1
    
    print("\n" + "="*60)
    print("TOP 20 RUNE BIGRAMS (numeric indices)")
    print("="*60)
    
    for bg, count in bigrams.most_common(20):
        letter1 = SINGLE[bg[0]]
        letter2 = SINGLE[bg[1]]
        print(f"  {bg[0]},{bg[1]} ({letter1}{letter2}): {count}")
    
    return bigrams

def try_vigenere_on_gematria(gematria_result, max_key_len=8):
    """Try Vigenere with short keys on gematria result."""
    print("\n" + "="*60)
    print("TRYING VIGENERE ON GEMATRIA+ RESULT")
    print("="*60)
    
    best_ioc = 0
    best_key = None
    
    for key_len in range(2, max_key_len + 1):
        # For each key position, find best shift
        best_key_attempt = []
        
        for pos in range(key_len):
            # Get every key_len-th character starting at pos
            subset = gematria_result[pos::key_len]
            
            # Try each shift
            best_shift = 0
            best_shift_ioc = 0
            
            for shift in range(29):
                shifted = (subset - shift) % 29
                ioc = compute_ioc_normalized(shifted)
                if ioc > best_shift_ioc:
                    best_shift_ioc = ioc
                    best_shift = shift
            
            best_key_attempt.append(best_shift)
        
        # Apply best key
        decrypted = np.zeros_like(gematria_result)
        for i, idx in enumerate(gematria_result):
            decrypted[i] = (idx - best_key_attempt[i % key_len]) % 29
        
        ioc = compute_ioc_normalized(decrypted)
        
        if ioc > 1.6:
            text = indices_to_single(decrypted[:100])
            print(f"\nKey len {key_len}: IoC={ioc:.4f}, Key={best_key_attempt}")
            print(f"  {text}")
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_key = best_key_attempt

def try_atbash_variant(gematria_result):
    """Try Atbash-like reverse substitution."""
    print("\n" + "="*60)
    print("TRYING ATBASH-STYLE REVERSALS")
    print("="*60)
    
    # Standard atbash: i -> 28 - i
    atbash = (28 - gematria_result) % 29
    ioc = compute_ioc_normalized(atbash)
    print(f"\nAtbash (28-i): IoC={ioc:.4f}")
    print(f"  {indices_to_single(atbash[:100])}")
    
    # ROT-like variations
    for shift in range(1, 15):
        shifted = (gematria_result + shift) % 29
        text = indices_to_single(shifted[:200])
        the_count = text.count('THE')
        if the_count > 5:
            print(f"\nShift +{shift}: IoC={compute_ioc_normalized(shifted):.4f}, THE={the_count}")
            print(f"  {text[:80]}")

def analyze_word_positions(lp_text, gematria_result):
    """Look at word boundaries and what runes they correspond to."""
    print("\n" + "="*60)
    print("WORD BOUNDARY ANALYSIS")
    print("="*60)
    
    # Split by word markers
    word_starts = []
    word_ends = []
    
    rune_idx = 0
    prev_was_rune = False
    
    for char in lp_text:
        if char in RUNE_TO_IDX:
            if not prev_was_rune and rune_idx > 0:
                word_starts.append(rune_idx)
            prev_was_rune = True
            rune_idx += 1
        else:
            if prev_was_rune and rune_idx > 0:
                word_ends.append(rune_idx - 1)
            prev_was_rune = False
    
    # Get first letters of words
    first_runes = Counter()
    for start in word_starts:
        if start < len(gematria_result):
            first_runes[gematria_result[start]] += 1
    
    print("\nMost common first runes of words after gematria+:")
    for rune_idx, count in first_runes.most_common(10):
        print(f"  {SINGLE[rune_idx]}: {count}")
    
    # In English, most common first letters are T, A, O, S, W, I
    # Let's see if we can match them

def score_english_like(text):
    """Score how English-like a text is."""
    common_words = {'THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT'}
    words = text.split()
    
    score = 0
    for word in words:
        if word in common_words:
            score += 10
    
    # Bigram scoring
    common_bigrams = {'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND'}
    for i in range(len(text) - 1):
        if text[i:i+2] in common_bigrams:
            score += 1
    
    return score

def try_autokey_on_gematria(gematria_result):
    """Try autokey cipher on gematria result."""
    print("\n" + "="*60)
    print("TRYING AUTOKEY ON GEMATRIA+ RESULT")
    print("="*60)
    
    for primer in range(29):
        decrypted = np.zeros_like(gematria_result)
        decrypted[0] = (gematria_result[0] - primer) % 29
        
        for i in range(1, len(gematria_result)):
            decrypted[i] = (gematria_result[i] - decrypted[i-1]) % 29
        
        ioc = compute_ioc_normalized(decrypted)
        
        if ioc > 1.5:
            text = indices_to_single(decrypted[:100])
            the_count = text.count('THE')
            print(f"\nPrimer {primer} ({SINGLE[primer]}): IoC={ioc:.4f}, THE={the_count}")
            print(f"  {text[:80]}")

def try_beaufort(gematria_result):
    """Try Beaufort cipher variant (like Vigenere but different)."""
    print("\n" + "="*60)
    print("TRYING BEAUFORT VARIANT")
    print("="*60)
    
    # Beaufort: P = K - C (mod n) vs Vigenere: C = P + K (mod n)
    # So if gematria output is 'ciphertext', try: P = K - Gem
    
    for key in range(29):
        result = (key - gematria_result) % 29
        ioc = compute_ioc_normalized(result)
        text = indices_to_single(result[:100])
        the_count = text.count('THE')
        
        if ioc > 1.7 or the_count > 3:
            print(f"\nKey {key}: IoC={ioc:.4f}, THE={the_count}")
            print(f"  {text}")

def main():
    print("="*70)
    print("DEEP INVESTIGATION OF GEMATRIA+ OUTPUT")
    print("="*70)
    
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    lp_text = load_liber_primus(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    gematria_result = gematria_shift_add(lp_indices)
    
    print(f"\nTotal runes: {len(lp_indices)}")
    print(f"Gematria+ IoC: {compute_ioc_normalized(gematria_result):.4f}")
    
    simple = indices_to_single(gematria_result[:200])
    print(f"\nFirst 200 chars (simplified):\n{simple}")
    
    # Analysis methods
    analyze_bigram_patterns(gematria_result)
    try_atbash_variant(gematria_result)
    try_autokey_on_gematria(gematria_result)
    try_beaufort(gematria_result)
    try_vigenere_on_gematria(gematria_result, max_key_len=6)
    analyze_word_positions(lp_text, gematria_result)
    
    # Let's also check: what if we apply gematria TWICE?
    print("\n" + "="*60)
    print("DOUBLE GEMATRIA APPLICATION")
    print("="*60)
    
    double_gematria = gematria_shift_add(gematria_result)
    ioc = compute_ioc_normalized(double_gematria)
    print(f"Double gematria+ IoC: {ioc:.4f}")
    print(f"  {indices_to_single(double_gematria[:100])}")
    
    triple_gematria = gematria_shift_add(double_gematria)
    ioc = compute_ioc_normalized(triple_gematria)
    print(f"Triple gematria+ IoC: {ioc:.4f}")
    print(f"  {indices_to_single(triple_gematria[:100])}")

if __name__ == "__main__":
    main()

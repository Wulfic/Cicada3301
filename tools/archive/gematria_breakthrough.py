#!/usr/bin/env python3
"""
Gematria Self-Shift Breakthrough Investigation
================================================
The gematria self-shift cipher produces IoC ~1.72 (English-like!)
This shifts each rune by its own gematria prime value mod 29.

Let's investigate this fully.
"""

import numpy as np
from collections import Counter
from pathlib import Path

# =============================================================================
# CONSTANTS
# =============================================================================

ALPHABET_SIZE = 29

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

# Gematria primes (F=2, U=3, TH=5, ... EA=109)
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_liber_primus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_RUNE[int(i) % 29] for i in indices)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def gematria_self_shift(ciphertext, direction=-1):
    """
    Shift each rune by its OWN gematria value mod 29.
    direction=-1: subtract (decrypt)
    direction=+1: add (encrypt)
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        gem = GEMATRIA[idx]
        result[i] = (idx + direction * gem) % 29
    return result

def gematria_cumulative_self_shift(ciphertext):
    """
    Shift each rune by the cumulative sum of its own gematria values.
    """
    result = np.zeros_like(ciphertext)
    cumsum = 0
    for i, idx in enumerate(ciphertext):
        gem = GEMATRIA[idx]
        cumsum = (cumsum + gem) % 29
        result[i] = (idx - cumsum) % 29
    return result

def print_frequency(indices, title="Frequency"):
    """Print frequency analysis."""
    counts = Counter(indices)
    total = len(indices)
    print(f"\n{title}:")
    print(f"{'Rune':<6} {'Eng':<5} {'Count':<6} {'%':<6}")
    print("-" * 25)
    for idx, count in counts.most_common():
        print(f"{IDX_TO_RUNE[idx]:<6} {LETTERS[idx]:<5} {count:<6} {count/total*100:.2f}%")

def analyze_gematria_shift_mapping():
    """
    Understand exactly what the gematria self-shift does.
    """
    print("="*60)
    print("GEMATRIA SELF-SHIFT MAPPING")
    print("="*60)
    print("\nFor each rune, shift by its gematria value mod 29:")
    print(f"{'Rune':<6} {'Eng':<5} {'Gem':<6} {'Gem%29':<8} {'Maps to':<6}")
    print("-" * 40)
    
    for i in range(29):
        gem = GEMATRIA[i]
        gem_mod = gem % 29
        new_idx = (i - gem_mod) % 29  # Decryption direction
        print(f"{RUNES[i]:<6} {LETTERS[i]:<5} {gem:<6} {gem_mod:<8} {RUNES[new_idx]:<6} ({LETTERS[new_idx]})")

def extract_words_with_separators(text, indices, decrypted):
    """
    Extract words preserving the structure.
    """
    result = []
    current_word = []
    dec_idx = 0
    
    for char in text:
        if char in RUNE_TO_IDX:
            current_word.append(LETTERS[decrypted[dec_idx]])
            dec_idx += 1
        elif char in '•-/:%&$. \n':
            if current_word:
                result.append(''.join(current_word))
                current_word = []
            if char == '•':
                result.append(' ')
            elif char == '-':
                result.append('-')
            elif char in '/%\n':
                result.append(' ')
            elif char == ':':
                result.append(' ')
        
        if dec_idx >= len(decrypted):
            break
    
    if current_word:
        result.append(''.join(current_word))
    
    return ''.join(result)

def main():
    print("="*70)
    print("GEMATRIA SELF-SHIFT BREAKTHROUGH INVESTIGATION")
    print("="*70)
    
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    if not lp_path.exists():
        print(f"Error: Could not find {lp_path}")
        return
    
    lp_text = load_liber_primus(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    print(f"\nLoaded {len(lp_indices)} runes")
    print(f"Original IoC: {compute_ioc_normalized(lp_indices):.4f}")
    
    # Understand the mapping
    analyze_gematria_shift_mapping()
    
    # Apply gematria self-shift to full text
    print("\n" + "="*60)
    print("APPLYING GEMATRIA SELF-SHIFT")
    print("="*60)
    
    decrypted = gematria_self_shift(lp_indices)
    print(f"\nDecrypted IoC: {compute_ioc_normalized(decrypted):.4f}")
    
    # Show first 200 runes
    print(f"\nFirst 200 characters (English transliteration):")
    eng = indices_to_english(decrypted[:200])
    print(eng)
    
    # Show frequency comparison
    print_frequency(lp_indices[:500], "Original frequency (first 500)")
    print_frequency(decrypted[:500], "Decrypted frequency (first 500)")
    
    # Extract words with separators
    print("\n" + "="*60)
    print("TEXT WITH WORD SEPARATORS")
    print("="*60)
    result = extract_words_with_separators(lp_text[:2000], lp_indices[:500], decrypted[:500])
    print(result)
    
    # Try variations
    print("\n" + "="*60)
    print("TESTING VARIATIONS")
    print("="*60)
    
    # Try adding instead of subtracting
    dec_add = gematria_self_shift(lp_indices, direction=1)
    print(f"\nAdd instead of subtract:")
    print(f"IoC: {compute_ioc_normalized(dec_add):.4f}")
    print(indices_to_english(dec_add[:100]))
    
    # Try cumulative
    dec_cum = gematria_cumulative_self_shift(lp_indices)
    print(f"\nCumulative gematria:")
    print(f"IoC: {compute_ioc_normalized(dec_cum):.4f}")
    print(indices_to_english(dec_cum[:100]))
    
    # Look for common English patterns in the decrypted text
    print("\n" + "="*60)
    print("LOOKING FOR ENGLISH PATTERNS")
    print("="*60)
    
    eng_full = indices_to_english(decrypted)
    
    # Common English words/patterns
    patterns = ['THE', 'AND', 'THAT', 'WITH', 'FOR', 'ARE', 'THIS', 'FROM',
                'INSTAR', 'CICADA', 'PRIME', 'WISDOM', 'TRUTH', 'SEEK',
                'AN', 'WE', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT',
                'ING', 'TION', 'NESS', 'MENT', 'ABLE']
    
    for pattern in patterns:
        count = eng_full.count(pattern)
        if count > 0:
            print(f"  '{pattern}': found {count} times")
            # Show context for first few occurrences
            idx = eng_full.find(pattern)
            if idx >= 0:
                start = max(0, idx - 10)
                end = min(len(eng_full), idx + len(pattern) + 10)
                print(f"    Context: ...{eng_full[start:end]}...")
    
    # Save decrypted text to file
    output_path = Path(__file__).parent / "gematria_decrypted.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("GEMATRIA SELF-SHIFT DECRYPTION OF LIBER PRIMUS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Method: Shift each rune by -(gematria_value mod 29)\n")
        f.write(f"IoC: {compute_ioc_normalized(decrypted):.4f}\n\n")
        f.write("DECRYPTED TEXT:\n")
        f.write("-" * 60 + "\n")
        f.write(eng_full)
        f.write("\n\n")
        f.write("WITH WORD SEPARATORS:\n")
        f.write("-" * 60 + "\n")
        full_result = extract_words_with_separators(lp_text, lp_indices, decrypted)
        f.write(full_result)
    
    print(f"\n\nDecrypted text saved to: {output_path}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

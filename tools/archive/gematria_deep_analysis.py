#!/usr/bin/env python3
"""
Deep dive into gematria shift findings.
Testing both directions and analyzing the output.
"""

import numpy as np
from collections import Counter
from pathlib import Path

ALPHABET_SIZE = 29

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_liber_primus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def gematria_shift(ciphertext, direction=-1):
    """
    Shift each rune by its OWN gematria value mod 29.
    """
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        gem = GEMATRIA[idx]
        result[i] = (idx + direction * gem) % 29
    return result

def extract_with_spaces(text, decrypted):
    """Extract text preserving word boundaries."""
    result = []
    dec_idx = 0
    
    for char in text:
        if char in RUNE_TO_IDX:
            if dec_idx < len(decrypted):
                result.append(LETTERS[decrypted[dec_idx]])
                dec_idx += 1
        elif char == '•':
            result.append(' ')
        elif char in '-':
            result.append('-')
        elif char in '/%\n':
            result.append('\n')
        elif char == ':':
            result.append(':')
        elif char == '.':
            result.append('.')
    
    return ''.join(result)

def main():
    print("="*70)
    print("GEMATRIA SHIFT DEEP ANALYSIS")
    print("="*70)
    
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    lp_text = load_liber_primus(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    print(f"\nTotal runes: {len(lp_indices)}")
    print(f"Original IoC: {compute_ioc_normalized(lp_indices):.4f}")
    
    # Test SUBTRACT direction (decrypt if encrypted with add)
    print("\n" + "="*60)
    print("SUBTRACT DIRECTION: plaintext[i] = cipher[i] - gematria[cipher[i]]")
    print("="*60)
    dec_sub = gematria_shift(lp_indices, direction=-1)
    print(f"IoC: {compute_ioc_normalized(dec_sub):.4f}")
    
    # With word separators
    text_sub = extract_with_spaces(lp_text, dec_sub)
    print("\nFirst 500 chars:")
    print(text_sub[:500])
    
    # Test ADD direction (decrypt if encrypted with subtract)
    print("\n" + "="*60)
    print("ADD DIRECTION: plaintext[i] = cipher[i] + gematria[cipher[i]]")
    print("="*60)
    dec_add = gematria_shift(lp_indices, direction=+1)
    print(f"IoC: {compute_ioc_normalized(dec_add):.4f}")
    
    text_add = extract_with_spaces(lp_text, dec_add)
    print("\nFirst 500 chars:")
    print(text_add[:500])
    
    # Look for readable English words
    print("\n" + "="*60)
    print("ANALYZING FOR READABLE WORDS")
    print("="*60)
    
    # Common English words to search for
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
        'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS',
        'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'DID', 'GET',
        'LET', 'SAY', 'SHE', 'TOO', 'USE', 'THAT', 'WITH', 'HAVE', 'THIS',
        'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'COME', 'COULD',
        'EACH', 'FIND', 'FIRST', 'GOOD', 'INTO', 'JUST', 'KNOW', 'LIKE',
        'LONG', 'LOOK', 'MADE', 'MAKE', 'MORE', 'MUST', 'NAME', 'NEED',
        'SEEK', 'SELF', 'TRUE', 'PATH', 'LIGHT', 'DARK', 'MIND', 'SOUL',
        'WISDOM', 'TRUTH', 'DIVINE', 'CICADA', 'PRIME', 'INSTAR'
    ]
    
    print("\nSubtract direction word search:")
    text_sub_clean = text_sub.replace('\n', ' ').replace('-', ' ').upper()
    for word in common_words:
        if ' ' + word + ' ' in text_sub_clean or text_sub_clean.startswith(word + ' ') or text_sub_clean.endswith(' ' + word):
            count = text_sub_clean.count(word)
            print(f"  Found '{word}': {count} times")
    
    print("\nAdd direction word search:")
    text_add_clean = text_add.replace('\n', ' ').replace('-', ' ').upper()
    for word in common_words:
        if ' ' + word + ' ' in text_add_clean or text_add_clean.startswith(word + ' ') or text_add_clean.endswith(' ' + word):
            count = text_add_clean.count(word)
            print(f"  Found '{word}': {count} times")
    
    # Analyze the distribution more carefully
    print("\n" + "="*60)
    print("FREQUENCY ANALYSIS")
    print("="*60)
    
    # English letter frequencies (approximate)
    english_freq = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
        'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
        'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
        'P': 1.9, 'B': 1.5
    }
    
    # Map our rune letters to single letters for comparison
    letter_map = {
        'F': 'F', 'U': 'U', 'TH': 'T', 'O': 'O', 'R': 'R', 'C': 'C',
        'G': 'G', 'W': 'W', 'H': 'H', 'N': 'N', 'I': 'I', 'J': 'J',
        'EO': 'E', 'P': 'P', 'X': 'X', 'S': 'S', 'T': 'T', 'B': 'B',
        'E': 'E', 'M': 'M', 'L': 'L', 'NG': 'N', 'OE': 'O', 'D': 'D',
        'A': 'A', 'AE': 'A', 'Y': 'Y', 'IA': 'I', 'EA': 'E'
    }
    
    # Check if the high IoC decryption might be a secondary cipher
    print("\nThe gematria self-shift produces high IoC (~1.78)")
    print("This suggests the original text was processed through this transform.")
    print("\nBut the output doesn't look like readable English.")
    print("This could mean:")
    print("  1. The text was first encrypted with standard cipher, THEN gematria-transformed")
    print("  2. The gematria transform is just part of the puzzle")
    print("  3. There's an additional layer we haven't found yet")
    
    # Try combining with Page 56 method
    print("\n" + "="*60)
    print("COMBINING GEMATRIA SHIFT WITH PAGE 56 METHOD")
    print("="*60)
    
    # Generate primes
    def sieve_primes(n):
        upper = max(15, int(n * (np.log(n) + np.log(np.log(n)))) + 100) if n >= 6 else 15
        sieve = np.ones(upper + 1, dtype=bool)
        sieve[0] = sieve[1] = False
        for i in range(2, int(upper**0.5) + 1):
            if sieve[i]:
                sieve[i*i::i] = False
        return np.where(sieve)[0][:n]
    
    primes = sieve_primes(len(lp_indices) + 100)
    
    # First apply gematria shift, then prime shift
    for offset in [0, 29, 57, 58]:
        step1 = gematria_shift(lp_indices, direction=-1)
        step2 = np.zeros_like(step1)
        for i, idx in enumerate(step1):
            shift = (primes[i] + offset) % 29
            step2[i] = (idx - shift) % 29
        
        ioc = compute_ioc_normalized(step2)
        eng = indices_to_english(step2[:50])
        print(f"  Gematria(-) then Prime(+{offset}): IoC={ioc:.4f} | {eng}...")
    
    # Try reverse order
    for offset in [0, 29, 57]:
        step1 = np.zeros_like(lp_indices)
        for i, idx in enumerate(lp_indices):
            shift = (primes[i] + offset) % 29
            step1[i] = (idx - shift) % 29
        step2 = gematria_shift(step1, direction=-1)
        
        ioc = compute_ioc_normalized(step2)
        eng = indices_to_english(step2[:50])
        print(f"  Prime(+{offset}) then Gematria(-): IoC={ioc:.4f} | {eng}...")

if __name__ == "__main__":
    main()

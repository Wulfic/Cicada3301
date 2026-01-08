#!/usr/bin/env python3
"""
PRIME VALUE BASED DECRYPTION
============================

Based on the 2016 Cicada clue:
"its words are the map, their meaning is the road, and their numbers are the direction"

Key insights:
1. "their numbers" = the PRIME VALUES of runes, not just indices
2. Shifting final 'F' to beginning reveals Fibonacci prime values (cyclic structure)
3. 59-rune sections (17th prime) may indicate structural layers
4. The even distribution in ciphertext causes TH anomaly when decrypting with indices

This tool tests decryption using prime values instead of indices.
"""

import os
import sys
from collections import Counter
from pathlib import Path
import math

# ============================================================================
# CONSTANTS
# ============================================================================

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}

# The PRIME VALUES for each rune (index -> prime)
PRIME_VALUES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Reverse: prime value -> index
PRIME_TO_INDEX = {p: i for i, p in enumerate(PRIME_VALUES)}

# Fibonacci numbers and Fibonacci primes
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
FIBONACCI_PRIMES = [2, 3, 5, 13, 89, 233, 1597]  # Fibonacci numbers that are also prime

# Primes list for reference
PRIMES_LIST = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
               67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]

# ============================================================================
# LOAD ORIGINAL RUNES (not first-layer output)
# ============================================================================

def load_page_runes(page_num):
    """Load original runes from page files"""
    base_path = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}" / "runes.txt"
    if base_path.exists():
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Extract only runes, ignore formatting
        runes = [c for c in content if c in RUNE_TO_INDEX]
        return runes
    return None

def runes_to_indices(runes):
    """Convert runes to indices"""
    return [RUNE_TO_INDEX[r] for r in runes]

def runes_to_primes(runes):
    """Convert runes to their prime values"""
    return [PRIME_VALUES[RUNE_TO_INDEX[r]] for r in runes]

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices if 0 <= i < 29)

def indices_to_runes(indices):
    """Convert indices back to runes"""
    return "".join(INDEX_TO_RUNE[i] for i in indices if 0 <= i < 29)

# ============================================================================
# PRIME-BASED DECRYPTION
# ============================================================================

def decrypt_with_prime_key(cipher_indices, key_primes, operation='sub'):
    """
    Decrypt using prime values as key.
    
    Instead of: plaintext = (cipher_idx - key_idx) mod 29
    Try: plaintext = (cipher_prime - key_prime) mod some_value
    
    Or convert key_primes to indices first.
    """
    # Convert key primes to indices
    key_indices = []
    for p in key_primes:
        if p in PRIME_TO_INDEX:
            key_indices.append(PRIME_TO_INDEX[p])
        else:
            # Find closest prime in our alphabet
            closest = min(PRIME_VALUES, key=lambda x: abs(x - p))
            key_indices.append(PRIME_TO_INDEX[closest])
    
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if operation == 'sub':
            plaintext.append((c - k) % 29)
        else:
            plaintext.append((c + k) % 29)
    
    return plaintext

def decrypt_prime_arithmetic(cipher_indices, key_primes, modulus=29):
    """
    Decrypt using actual prime arithmetic.
    
    cipher_prime - key_prime, then map result back to alphabet.
    """
    plaintext = []
    for i, c_idx in enumerate(cipher_indices):
        c_prime = PRIME_VALUES[c_idx]
        k_prime = key_primes[i % len(key_primes)]
        
        # Try different operations
        result = (c_prime - k_prime) % modulus
        
        # Map back to index (result might not be a valid prime)
        # Use result as direct index
        plaintext.append(result % 29)
    
    return plaintext

def decrypt_prime_to_prime(cipher_indices, key_primes):
    """
    Decrypt where result should also be a prime value.
    
    plaintext_prime = cipher_prime XOR key_prime (for primes)
    Or: find prime such that (plain_prime + key_prime) mod X = cipher_prime
    """
    plaintext = []
    for i, c_idx in enumerate(cipher_indices):
        c_prime = PRIME_VALUES[c_idx]
        k_prime = key_primes[i % len(key_primes)]
        
        # Try subtraction in prime space
        target = c_prime - k_prime
        
        # Find closest prime in our alphabet
        if target in PRIME_TO_INDEX:
            plaintext.append(PRIME_TO_INDEX[target])
        else:
            # Wrap around or find closest
            if target < 2:
                target = target + 109  # Wrap using largest prime
            if target > 109:
                target = target - 109
            
            if target in PRIME_TO_INDEX:
                plaintext.append(PRIME_TO_INDEX[target])
            else:
                closest = min(PRIME_VALUES, key=lambda x: abs(x - target))
                plaintext.append(PRIME_TO_INDEX[closest])
    
    return plaintext

# ============================================================================
# FIBONACCI-BASED KEYS
# ============================================================================

def generate_fibonacci_key(length):
    """Generate key using Fibonacci sequence mod 29"""
    key = []
    a, b = 1, 1
    for _ in range(length):
        key.append(a % 29)
        a, b = b, a + b
    return key

def generate_fibonacci_prime_key(length):
    """Generate key using Fibonacci primes"""
    # Map Fibonacci primes to our alphabet
    fib_prime_indices = []
    for fp in FIBONACCI_PRIMES:
        if fp in PRIME_TO_INDEX:
            fib_prime_indices.append(PRIME_TO_INDEX[fp])
    
    # Repeat to fill length
    key = []
    for i in range(length):
        key.append(fib_prime_indices[i % len(fib_prime_indices)])
    return key

# ============================================================================
# 59-RUNE SECTION ANALYSIS
# ============================================================================

def analyze_59_sections(runes):
    """
    Analyze text in 59-rune sections (17th prime).
    The clue suggests this may reveal structural patterns.
    """
    indices = runes_to_indices(runes)
    sections = []
    
    for i in range(0, len(indices), 59):
        section = indices[i:i+59]
        if len(section) >= 30:  # Only analyze substantial sections
            sections.append({
                'start': i,
                'indices': section,
                'text': indices_to_text(section),
                'length': len(section)
            })
    
    return sections

def cyclic_shift_analysis(indices, shift_amount):
    """
    Apply cyclic shift (moving characters from end to beginning).
    The clue mentions shifting final 'F' to beginning.
    """
    shifted = indices[-shift_amount:] + indices[:-shift_amount]
    return shifted

# ============================================================================
# SCORING
# ============================================================================

def score_english(text):
    """Score English-likeness"""
    text = text.upper()
    score = 0.0
    
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8,
    }
    
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
    }
    
    keywords = {
        'WISDOM': 50, 'TRUTH': 50, 'DIVINE': 50, 'EMERGE': 50,
        'INSTAR': 60, 'CIRCUMFERENCE': 70, 'KNOWLEDGE': 50,
        'SEEK': 40, 'FIND': 40, 'PATH': 40, 'WITHIN': 45,
        'WARNING': 40, 'LIBER': 50, 'PRIMUS': 50,
    }
    
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    for kw, bonus in keywords.items():
        score += text.count(kw) * bonus
    
    return score

def get_th_frequency(text):
    """Calculate TH frequency"""
    text = text.upper()
    th_count = text.count('TH')
    return (th_count / max(1, len(text) - 1)) * 100

# ============================================================================
# KEY GENERATION FROM WORDS USING PRIME VALUES
# ============================================================================

def word_to_prime_key(word):
    """
    Convert a word to a key using prime values.
    "their numbers are the direction"
    """
    word = word.upper()
    key_primes = []
    i = 0
    while i < len(word):
        matched = False
        for length in [2, 1]:
            if i + length <= len(word):
                segment = word[i:i+length]
                if segment in LETTER_TO_INDEX:
                    idx = LETTER_TO_INDEX[segment]
                    key_primes.append(PRIME_VALUES[idx])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return key_primes

def word_to_index_key(word):
    """Convert a word to indices"""
    word = word.upper()
    key = []
    i = 0
    while i < len(word):
        matched = False
        for length in [2, 1]:
            if i + length <= len(word):
                segment = word[i:i+length]
                if segment in LETTER_TO_INDEX:
                    key.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return key

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def analyze_page_with_prime_keys(page_num):
    """
    Analyze a page using prime-based decryption approaches.
    """
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - PRIME VALUE ANALYSIS")
    print(f"{'='*70}")
    
    runes = load_page_runes(page_num)
    if not runes:
        print(f"Could not load runes for page {page_num}")
        return
    
    indices = runes_to_indices(runes)
    primes = runes_to_primes(runes)
    
    print(f"Rune count: {len(runes)}")
    print(f"59-rune sections: {len(runes) // 59} complete + {len(runes) % 59} remainder")
    
    # Baseline (no decryption)
    baseline_text = indices_to_text(indices)
    baseline_score = score_english(baseline_text)
    print(f"\nBaseline (raw): score {baseline_score:.2f}")
    print(f"Text: {baseline_text[:80]}...")
    
    results = []
    
    # Test 1: Words as keys using prime values
    test_words = [
        "DIVINITY", "WISDOM", "TRUTH", "PRIMUS", "LIBER", "PATH",
        "INSTAR", "EMERGE", "CIRCUMFERENCE", "FIND", "SEEK", "WITHIN",
        "FIBONACCI", "PRIME", "WAY", "MAP", "ROAD", "DIRECTION",
        "WORDS", "MEANING", "NUMBERS", "BEWARE", "VERIFY",
    ]
    
    print(f"\n--- Testing word keys with prime values ---")
    
    for word in test_words:
        key_primes = word_to_prime_key(word)
        key_indices = word_to_index_key(word)
        
        if not key_primes:
            continue
        
        # Method 1: Use prime values, convert to indices for decryption
        for op in ['sub', 'add']:
            plain = decrypt_with_prime_key(indices, key_primes, op)
            text = indices_to_text(plain)
            score = score_english(text)
            th_freq = get_th_frequency(text)
            
            results.append({
                'method': f'prime_key_{op}',
                'word': word,
                'score': score,
                'th_freq': th_freq,
                'text': text
            })
        
        # Method 2: Direct index-based (for comparison)
        for op in ['sub', 'add']:
            plain = []
            for i, c in enumerate(indices):
                k = key_indices[i % len(key_indices)]
                if op == 'sub':
                    plain.append((c - k) % 29)
                else:
                    plain.append((c + k) % 29)
            text = indices_to_text(plain)
            score = score_english(text)
            th_freq = get_th_frequency(text)
            
            results.append({
                'method': f'index_key_{op}',
                'word': word,
                'score': score,
                'th_freq': th_freq,
                'text': text
            })
    
    # Test 2: Fibonacci-based keys
    print(f"\n--- Testing Fibonacci keys ---")
    
    fib_key = generate_fibonacci_key(len(indices))
    for op in ['sub', 'add']:
        plain = []
        for i, c in enumerate(indices):
            k = fib_key[i]
            if op == 'sub':
                plain.append((c - k) % 29)
            else:
                plain.append((c + k) % 29)
        text = indices_to_text(plain)
        score = score_english(text)
        
        results.append({
            'method': f'fibonacci_{op}',
            'word': 'FIBONACCI_SEQ',
            'score': score,
            'th_freq': get_th_frequency(text),
            'text': text
        })
    
    # Test 3: Fibonacci prime key
    fib_prime_key = generate_fibonacci_prime_key(len(indices))
    for op in ['sub', 'add']:
        plain = []
        for i, c in enumerate(indices):
            k = fib_prime_key[i]
            if op == 'sub':
                plain.append((c - k) % 29)
            else:
                plain.append((c + k) % 29)
        text = indices_to_text(plain)
        score = score_english(text)
        
        results.append({
            'method': f'fib_prime_{op}',
            'word': 'FIBONACCI_PRIMES',
            'score': score,
            'th_freq': get_th_frequency(text),
            'text': text
        })
    
    # Test 4: Cyclic shifts
    print(f"\n--- Testing cyclic shifts ---")
    
    for shift in [1, 59, len(indices) // 2]:
        shifted = cyclic_shift_analysis(indices, shift)
        text = indices_to_text(shifted)
        score = score_english(text)
        
        results.append({
            'method': f'cyclic_shift_{shift}',
            'word': f'SHIFT_{shift}',
            'score': score,
            'th_freq': get_th_frequency(text),
            'text': text
        })
    
    # Test 5: Prime arithmetic on cipher
    print(f"\n--- Testing prime arithmetic ---")
    
    for word in ['DIVINITY', 'PRIMUS', 'PATH', 'TRUTH']:
        key_primes = word_to_prime_key(word)
        if key_primes:
            plain = decrypt_prime_to_prime(indices, key_primes)
            text = indices_to_text(plain)
            score = score_english(text)
            
            results.append({
                'method': 'prime_arithmetic',
                'word': word,
                'score': score,
                'th_freq': get_th_frequency(text),
                'text': text
            })
    
    # Sort and display top results
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n{'='*70}")
    print(f"TOP 15 RESULTS FOR PAGE {page_num}")
    print(f"{'='*70}")
    
    for i, r in enumerate(results[:15]):
        improvement = r['score'] - baseline_score
        print(f"{i+1:2}. {r['method']:20} {r['word']:15} score={r['score']:7.2f} "
              f"({'+' if improvement >= 0 else ''}{improvement:7.2f}) TH={r['th_freq']:5.2f}%")
        if i < 3:
            print(f"    Text: {r['text'][:70]}...")
    
    return results

def analyze_59_structure(page_num):
    """
    Analyze the 59-rune section structure.
    """
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - 59-RUNE SECTION ANALYSIS")
    print(f"{'='*70}")
    
    runes = load_page_runes(page_num)
    if not runes:
        return
    
    indices = runes_to_indices(runes)
    sections = analyze_59_sections(runes)
    
    print(f"Total runes: {len(runes)}")
    print(f"Complete 59-rune sections: {len(runes) // 59}")
    print(f"Remainder: {len(runes) % 59} runes")
    
    for i, section in enumerate(sections):
        print(f"\nSection {i+1} (pos {section['start']}-{section['start']+section['length']}):")
        print(f"  Raw text: {section['text'][:60]}...")
        
        # Try decrypting each section independently
        # Use position-based key (section index)
        for key_val in range(29):
            plain = [(idx - key_val) % 29 for idx in section['indices']]
            text = indices_to_text(plain)
            score = score_english(text)
            if score > 100:
                print(f"  Key {key_val} ({LETTERS[key_val]}): score {score:.0f} - {text[:40]}...")

def test_ring_structure(page_num):
    """
    Test if the text has a ring/cyclic structure.
    "Shifting final F to beginning reveals Fibonacci primes"
    """
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - RING STRUCTURE TEST")
    print(f"{'='*70}")
    
    runes = load_page_runes(page_num)
    if not runes:
        return
    
    indices = runes_to_indices(runes)
    
    # Find positions of 'F' (index 0)
    f_positions = [i for i, idx in enumerate(indices) if idx == 0]
    print(f"F rune positions: {f_positions}")
    
    # Test shifting from each F position
    best_results = []
    
    for f_pos in f_positions:
        # Shift so this F is at the beginning
        shift_amount = len(indices) - f_pos
        shifted = indices[-shift_amount:] + indices[:-shift_amount]
        
        # Check if first few positions now follow Fibonacci pattern
        fib_check = []
        for i, fib_val in enumerate(FIBONACCI[:10]):
            if fib_val < len(shifted):
                fib_check.append((fib_val, shifted[fib_val], LETTERS[shifted[fib_val]]))
        
        text = indices_to_text(shifted)
        score = score_english(text)
        
        print(f"\nShift by {shift_amount} (F from pos {f_pos} to start):")
        print(f"  Fibonacci positions: {fib_check[:5]}")
        print(f"  Score: {score:.2f}")
        print(f"  Text: {text[:60]}...")
        
        best_results.append({
            'shift': shift_amount,
            'f_pos': f_pos,
            'score': score,
            'text': text
        })
    
    return best_results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prime value based Liber Primus analysis")
    parser.add_argument('--page', type=int, default=0, help='Page number')
    parser.add_argument('--all', action='store_true', help='Analyze all pages 0-4')
    parser.add_argument('--sections', action='store_true', help='Analyze 59-rune sections')
    parser.add_argument('--ring', action='store_true', help='Test ring structure')
    
    args = parser.parse_args()
    
    if args.all:
        for page in range(5):
            analyze_page_with_prime_keys(page)
    elif args.sections:
        analyze_59_structure(args.page)
    elif args.ring:
        test_ring_structure(args.page)
    else:
        analyze_page_with_prime_keys(args.page)

#!/usr/bin/env python3
"""
Liber Primus Master Solver
==========================

A comprehensive cipher analysis tool that incorporates all known findings
and tests systematic key hypotheses based on Cicada 3301 clues.

Key Insights Incorporated:
1. Page 56 formula: -(gematria + 57) mod 29
2. IoC ≈ 1.0 indicates running-key or polyalphabetic cipher
3. Pages 0 and 54 are IDENTICAL (structural clue)
4. "Circumference" from Parable - may hint at pi/fibonacci

Author: Cicada Solving Session 2026
"""

import re
import math
import numpy as np
from collections import Counter
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# =============================================================================
# RUNE SYSTEM
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Bidirectional mappings
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}
LETTER_TO_IDX = {l: i for i, l in enumerate(LETTERS)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
PRIME_TO_IDX = {p: i for i, p in enumerate(PRIMES)}

# English frequency for scoring (approximate 29-letter mapping)
ENGLISH_FREQ = {
    'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7, 'F': 2.2,
    'G': 2.0, 'H': 6.1, 'I': 7.0, 'J': 0.15, 'L': 4.0, 'M': 2.4,
    'N': 6.7, 'O': 7.5, 'P': 1.9, 'R': 6.0, 'S': 6.3, 'T': 9.1,
    'U': 2.8, 'W': 2.4, 'X': 0.15, 'Y': 2.0
}

# Common patterns for validation
COMMON_BIGRAMS = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
COMMON_TRIGRAMS = ['THE', 'AND', 'ING', 'ENT', 'ION', 'HER', 'FOR', 'THA']
CICADA_WORDS = ['INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'SURFACE', 'CIRCUMFERENCE',
                'WITHIN', 'SHED', 'PRIME', 'WISDOM', 'TRUTH', 'CICADA', 'LIBER', 'PRIMUS',
                'ENLIGHTEN', 'CONSCIOUSNESS', 'SEEK', 'FIND', 'DEEP', 'WEB']

# =============================================================================
# DATA LOADING
# =============================================================================
def load_all_pages() -> Dict[int, str]:
    """Load all Liber Primus pages from RuneSolver.py"""
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    
    return pages

def load_self_reliance() -> str:
    """Load Self-Reliance text for running key tests"""
    path = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\Self-Reliance.txt")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        # Convert to uppercase, keep only letters
        return ''.join(c for c in text.upper() if c.isalpha())
    except FileNotFoundError:
        return ""

# =============================================================================
# MATHEMATICAL KEY GENERATORS
# =============================================================================
def generate_pi_key(length: int) -> List[int]:
    """Generate key from pi digits mod 29"""
    # Pi digits (first 1000)
    pi_str = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
    key = []
    for i in range(min(length, len(pi_str))):
        key.append(int(pi_str[i]) % 29)
    # Extend if needed by cycling
    while len(key) < length:
        key.extend(key[:length - len(key)])
    return key[:length]

def generate_fibonacci_key(length: int) -> List[int]:
    """Generate key from Fibonacci sequence mod 29"""
    fib = [1, 1]
    for i in range(length):
        fib.append(fib[-1] + fib[-2])
    return [f % 29 for f in fib[:length]]

def generate_prime_key(length: int) -> List[int]:
    """Generate key from consecutive primes mod 29"""
    primes = []
    n = 2
    while len(primes) < length:
        if all(n % p != 0 for p in primes if p * p <= n):
            primes.append(n)
        n += 1
    return [p % 29 for p in primes[:length]]

def text_to_gematria_key(text: str) -> List[int]:
    """Convert text to gematria values mod 29"""
    # Map common letters to our 29-rune system
    SIMPLE_MAP = {
        'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6,
        'H': 8, 'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9,
        'O': 3, 'P': 13, 'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1,
        'V': 1, 'W': 7, 'X': 14, 'Y': 26, 'Z': 15
    }
    key = []
    for c in text.upper():
        if c in SIMPLE_MAP:
            key.append(SIMPLE_MAP[c])
    return key

def generate_circumference_keys(length: int) -> Dict[str, List[int]]:
    """Generate various keys based on 'circumference' hint"""
    keys = {}
    
    # The word CIRCUMFERENCE as gematria
    keys['CIRCUMFERENCE_word'] = text_to_gematria_key('CIRCUMFERENCE')
    if len(keys['CIRCUMFERENCE_word']) < length:
        # Repeat to fill
        mult = (length // len(keys['CIRCUMFERENCE_word'])) + 1
        keys['CIRCUMFERENCE_word'] = (keys['CIRCUMFERENCE_word'] * mult)[:length]
    
    # Pi digits (circumference = 2*pi*r, pi is key)
    keys['pi_digits'] = generate_pi_key(length)
    
    # Fibonacci (related to golden ratio, circles, spirals)
    keys['fibonacci'] = generate_fibonacci_key(length)
    
    # 2*pi approximated
    keys['two_pi'] = [(int(x * 2) % 29) for x in generate_pi_key(length)]
    
    # Primes (gematria primus)
    keys['primes'] = generate_prime_key(length)
    
    # Combined: pi + fibonacci
    fib_key = generate_fibonacci_key(length)
    pi_key = generate_pi_key(length)
    keys['pi_plus_fib'] = [(p + f) % 29 for p, f in zip(pi_key, fib_key)]
    
    return keys

# =============================================================================
# CONVERSION UTILITIES
# =============================================================================
def runes_to_indices(runes: str) -> np.ndarray:
    """Convert rune string to numpy array of indices"""
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices: np.ndarray) -> str:
    """Convert indices to letter representation"""
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def indices_to_runes(indices: np.ndarray) -> str:
    """Convert indices back to runes"""
    return ''.join(IDX_TO_RUNE[i % 29] for i in indices)

# =============================================================================
# CIPHER OPERATIONS
# =============================================================================
def decrypt_vigenere(ciphertext_idx: np.ndarray, key: List[int]) -> np.ndarray:
    """Vigenère decryption: plaintext = (cipher - key) mod 29"""
    key_arr = np.array(key * ((len(ciphertext_idx) // len(key)) + 1), dtype=np.int32)[:len(ciphertext_idx)]
    return (ciphertext_idx - key_arr) % 29

def decrypt_running_key(ciphertext_idx: np.ndarray, running_key_idx: np.ndarray) -> np.ndarray:
    """Running key decryption"""
    min_len = min(len(ciphertext_idx), len(running_key_idx))
    return (ciphertext_idx[:min_len] - running_key_idx[:min_len]) % 29

def decrypt_page56_style(indices: np.ndarray, offset: int = 57) -> np.ndarray:
    """Page 56 formula: -(gematria + offset) mod 29"""
    result = []
    for i, idx in enumerate(indices):
        prime = PRIMES[i % 29]  # Cycle through primes
        shift = (prime + offset) % 29
        result.append((idx - shift) % 29)
    return np.array(result, dtype=np.int32)

def decrypt_autokey(ciphertext_idx: np.ndarray, primer: List[int]) -> np.ndarray:
    """Autokey cipher where plaintext extends the key"""
    result = []
    key = list(primer)
    for i, c in enumerate(ciphertext_idx):
        if i < len(primer):
            decrypted = (c - key[i]) % 29
        else:
            decrypted = (c - result[i - len(primer)]) % 29
        result.append(decrypted)
    return np.array(result, dtype=np.int32)

# =============================================================================
# SCORING FUNCTIONS
# =============================================================================
def calculate_ioc(indices: np.ndarray) -> float:
    """Calculate Index of Coincidence"""
    n = len(indices)
    if n < 2:
        return 0.0
    
    counts = np.bincount(indices, minlength=29)
    numerator = np.sum(counts * (counts - 1))
    denominator = n * (n - 1)
    
    return (numerator / denominator) * 29 if denominator > 0 else 0.0

def score_english_likeness(text: str) -> float:
    """Score how English-like a text is (0-100 scale)"""
    score = 0.0
    text_upper = text.upper()
    
    # 1. Common word bonus (max 40 points)
    word_score = 0
    common_words = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS', 
                    'BUT', 'FROM', 'THEY', 'WILL', 'ALL', 'WOULD', 'THERE', 'THEIR']
    for word in common_words:
        word_score += text_upper.count(word) * len(word)
    score += min(word_score, 40)
    
    # 2. Cicada vocabulary bonus (max 30 points)
    cicada_score = 0
    for word in CICADA_WORDS:
        if word in text_upper:
            cicada_score += len(word) * 3
    score += min(cicada_score, 30)
    
    # 3. Bigram frequency (max 15 points)
    bigram_score = 0
    for bg in COMMON_BIGRAMS:
        bigram_score += text_upper.count(bg)
    score += min(bigram_score * 2, 15)
    
    # 4. Trigram frequency (max 15 points)
    trigram_score = 0
    for tg in COMMON_TRIGRAMS:
        trigram_score += text_upper.count(tg) * 2
    score += min(trigram_score, 15)
    
    # Penalties
    # Too many consonants in a row
    consonants = 'BCDFGHJKLMNPQRSTVWXZ'
    vowels = 'AEIOU'
    max_cons_run = 0
    curr_cons_run = 0
    for c in text_upper:
        if c in consonants:
            curr_cons_run += 1
            max_cons_run = max(max_cons_run, curr_cons_run)
        else:
            curr_cons_run = 0
    if max_cons_run > 5:
        score -= (max_cons_run - 5) * 2
    
    return max(score, 0)

def evaluate_decryption(plaintext_idx: np.ndarray, min_length: int = 50) -> Dict:
    """Comprehensive evaluation of a decryption attempt"""
    text = indices_to_text(plaintext_idx)
    
    return {
        'text': text[:200],  # First 200 chars for display
        'ioc': calculate_ioc(plaintext_idx),
        'english_score': score_english_likeness(text),
        'length': len(text),
        'has_the': 'THE' in text.upper(),
        'has_and': 'AND' in text.upper(),
        'has_cicada': any(w in text.upper() for w in CICADA_WORDS)
    }

# =============================================================================
# ATTACK FUNCTIONS
# =============================================================================
def attack_with_circumference_keys(page_runes: str, verbose: bool = True) -> List[Dict]:
    """Test all circumference-based keys on a page"""
    results = []
    indices = runes_to_indices(page_runes)
    length = len(indices)
    
    keys = generate_circumference_keys(length)
    
    if verbose:
        print(f"\n{'='*60}")
        print("CIRCUMFERENCE KEY ATTACK")
        print(f"{'='*60}")
    
    for key_name, key in keys.items():
        # Test Vigenère decryption
        decrypted = decrypt_vigenere(indices, key)
        result = evaluate_decryption(decrypted)
        result['key_name'] = key_name
        result['method'] = 'vigenere'
        results.append(result)
        
        # Test with addition instead of subtraction
        decrypted_add = (indices + np.array(key[:length], dtype=np.int32)) % 29
        result_add = evaluate_decryption(decrypted_add)
        result_add['key_name'] = f"{key_name}_add"
        result_add['method'] = 'vigenere_add'
        results.append(result_add)
    
    # Sort by English score
    results.sort(key=lambda x: x['english_score'] + x['ioc'] * 10, reverse=True)
    
    if verbose:
        print(f"\nTop 5 Results:")
        for r in results[:5]:
            print(f"\n{r['key_name']} ({r['method']}):")
            print(f"  IoC: {r['ioc']:.4f} | Score: {r['english_score']:.1f}")
            print(f"  Text: {r['text'][:80]}...")
    
    return results

def attack_with_running_key(page_runes: str, key_text: str, verbose: bool = True) -> Dict:
    """Attack using a running key (another text)"""
    cipher_idx = runes_to_indices(page_runes)
    key_idx = np.array(text_to_gematria_key(key_text), dtype=np.int32)
    
    if len(key_idx) < len(cipher_idx):
        print(f"Warning: Key text shorter than ciphertext ({len(key_idx)} < {len(cipher_idx)})")
    
    decrypted = decrypt_running_key(cipher_idx, key_idx)
    result = evaluate_decryption(decrypted)
    result['key_name'] = 'running_key'
    result['method'] = 'running_key'
    result['key_length_used'] = min(len(cipher_idx), len(key_idx))
    
    if verbose:
        print(f"\n{'='*60}")
        print("RUNNING KEY ATTACK (Self-Reliance)")
        print(f"{'='*60}")
        print(f"IoC: {result['ioc']:.4f} | Score: {result['english_score']:.1f}")
        print(f"Text: {result['text'][:100]}...")
    
    return result

def attack_page56_variants(page_runes: str, verbose: bool = True) -> List[Dict]:
    """Test Page 56 formula with various offsets"""
    results = []
    indices = runes_to_indices(page_runes)
    
    if verbose:
        print(f"\n{'='*60}")
        print("PAGE 56 FORMULA VARIANTS")
        print(f"{'='*60}")
    
    for offset in range(0, 120, 1):  # Test offsets 0-119
        decrypted = decrypt_page56_style(indices, offset)
        result = evaluate_decryption(decrypted)
        result['offset'] = offset
        result['method'] = 'page56_style'
        results.append(result)
    
    # Sort by score
    results.sort(key=lambda x: x['english_score'] + x['ioc'] * 10, reverse=True)
    
    if verbose:
        print(f"\nTop 5 Offsets:")
        for r in results[:5]:
            print(f"\nOffset {r['offset']}:")
            print(f"  IoC: {r['ioc']:.4f} | Score: {r['english_score']:.1f}")
            print(f"  Text: {r['text'][:80]}...")
    
    return results

def analyze_duplicate_pages(pages: Dict[int, str], verbose: bool = True) -> Dict:
    """Analyze the Pages 0 and 54 duplicate phenomenon"""
    if 0 not in pages or 54 not in pages:
        return {'error': 'Pages 0 or 54 not found'}
    
    page0 = runes_to_indices(pages[0])
    page54 = runes_to_indices(pages[54])
    
    if verbose:
        print(f"\n{'='*60}")
        print("DUPLICATE PAGES ANALYSIS (0 & 54)")
        print(f"{'='*60}")
    
    # Confirm they're identical
    identical = np.array_equal(page0, page54)
    
    if verbose:
        print(f"Pages are identical: {identical}")
        print(f"Length: {len(page0)} runes each")
    
    # Calculate difference with other pages
    interesting = []
    for pg_num, pg_runes in pages.items():
        if pg_num in [0, 54, 57]:  # Skip duplicates and plaintext
            continue
        
        pg_idx = runes_to_indices(pg_runes)
        if len(pg_idx) == len(page0):
            diff = (page0 - pg_idx) % 29
            diff_ioc = calculate_ioc(diff)
            diff_text = indices_to_text(diff)
            score = score_english_likeness(diff_text)
            
            if score > 10 or diff_ioc > 1.2:
                interesting.append({
                    'page': pg_num,
                    'diff_ioc': diff_ioc,
                    'english_score': score,
                    'sample': diff_text[:50]
                })
    
    if verbose and interesting:
        print(f"\nInteresting page differences (XOR with Page 0):")
        for item in sorted(interesting, key=lambda x: x['english_score'], reverse=True)[:5]:
            print(f"  Page {item['page']}: IoC={item['diff_ioc']:.3f}, Score={item['english_score']:.1f}")
            print(f"    Sample: {item['sample']}")
    
    return {
        'identical': identical,
        'length': len(page0),
        'interesting_diffs': interesting
    }

# =============================================================================
# MAIN ANALYSIS
# =============================================================================
def main():
    print("="*70)
    print("LIBER PRIMUS MASTER SOLVER")
    print("="*70)
    
    # Load data
    print("\nLoading pages...")
    pages = load_all_pages()
    print(f"Loaded {len(pages)} pages")
    
    self_reliance = load_self_reliance()
    print(f"Loaded Self-Reliance: {len(self_reliance)} characters")
    
    # Select a test page (Page 0 - first encrypted page)
    test_page = pages.get(0, "")
    if not test_page:
        print("Error: Could not load Page 0")
        return
    
    print(f"\nTest page: Page 0 ({len(test_page)} runes)")
    
    # Run attacks
    print("\n" + "="*70)
    print("RUNNING ATTACKS ON PAGE 0")
    print("="*70)
    
    # 1. Circumference keys
    circ_results = attack_with_circumference_keys(test_page)
    
    # 2. Running key with Self-Reliance
    if self_reliance:
        running_result = attack_with_running_key(test_page, self_reliance)
    
    # 3. Page 56 formula variants
    p56_results = attack_page56_variants(test_page)
    
    # 4. Duplicate page analysis
    dup_analysis = analyze_duplicate_pages(pages)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    all_results = circ_results + p56_results
    if self_reliance:
        all_results.append(running_result)
    
    # Find best result
    best = max(all_results, key=lambda x: x['english_score'] + x['ioc'] * 10)
    
    print(f"\nBest result across all methods:")
    print(f"  Method: {best.get('method', 'unknown')}")
    print(f"  Key: {best.get('key_name', 'N/A')}")
    print(f"  Offset: {best.get('offset', 'N/A')}")
    print(f"  IoC: {best['ioc']:.4f}")
    print(f"  English Score: {best['english_score']:.1f}")
    print(f"  Text: {best['text'][:100]}...")
    
    # Check if any result looks promising
    promising = [r for r in all_results if r['english_score'] > 20 or r['ioc'] > 1.3]
    if promising:
        print(f"\n⚠️ FOUND {len(promising)} PROMISING RESULTS!")
        for p in promising[:3]:
            print(f"  - {p.get('key_name', p.get('offset', 'unknown'))}: Score={p['english_score']:.1f}, IoC={p['ioc']:.4f}")
    else:
        print("\n❌ No highly promising results found with these methods.")
        print("   Consider: Multi-layer encryption, different running key texts,")
        print("   or the key derivation method may be more complex.")

if __name__ == "__main__":
    main()

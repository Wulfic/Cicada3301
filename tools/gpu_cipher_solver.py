#!/usr/bin/env python3
"""
GPU-Accelerated Liber Primus Cipher Solver

Uses CuPy/NumPy for fast parallel computation of cipher variants.
Tests thousands of key combinations to find readable plaintext.

Key insight: IoC of ~1.0 suggests flat distribution, meaning either:
1. Running key cipher (plaintext as key)
2. Autokey cipher  
3. Multi-layer encryption
4. One-time pad style

This tool tests ALL these possibilities systematically.
"""

import re
import sys
import time
from collections import Counter
from itertools import product
import warnings
warnings.filterwarnings('ignore')

import numpy as np

# Try to import CuPy for GPU acceleration
USE_GPU = False
cp = np  # Default to NumPy

try:
    import cupy as cupy_module
    # Test if CUDA is actually working
    _ = cupy_module.zeros(1)
    cp = cupy_module
    USE_GPU = True
    print("✓ GPU acceleration enabled (CuPy/CUDA)")
except ImportError:
    print("⚠ CuPy not installed - using CPU (NumPy)")
except Exception as e:
    print(f"⚠ CuPy available but CUDA error: {e} - using CPU")

# =============================================================================
# RUNE DATA
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

# English letter frequency (approximate, mapped to 29-char runic alphabet)
# This is adapted from standard English frequencies
ENGLISH_FREQ_ORDER = [18, 16, 24, 3, 9, 15, 4, 8, 20, 23, 0, 7, 6, 13, 1, 17, 5, 26, 14, 12, 19, 11, 21, 10, 28, 25, 27, 22, 2]  # E, T, A, O, N, S, R, H, L, D, ...

# Common English words for scoring (runic letter equivalents)
COMMON_WORDS = [
    'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'YOU', 'THIS', 'BUT',
    'HIS', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE', 'OR', 'AN', 'WILL',
    'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'SO', 'UP', 'OUT',
    'IF', 'ABOUT', 'WHO', 'GET', 'WHICH', 'GO', 'ME', 'WHEN', 'MAKE', 'CAN',
    'LIKE', 'TIME', 'NO', 'JUST', 'HIM', 'KNOW', 'TAKE', 'PEOPLE', 'INTO', 'YEAR',
    'YOUR', 'GOOD', 'SOME', 'COULD', 'THEM', 'SEE', 'OTHER', 'THAN', 'THEN', 'NOW',
    'LOOK', 'ONLY', 'COME', 'ITS', 'OVER', 'THINK', 'ALSO', 'BACK', 'AFTER', 'USE',
    'TWO', 'HOW', 'OUR', 'WORK', 'FIRST', 'WELL', 'WAY', 'EVEN', 'NEW', 'WANT',
    'BECAUSE', 'ANY', 'THESE', 'GIVE', 'DAY', 'MOST', 'US'
]

# Cicada-specific vocabulary
CICADA_WORDS = [
    'INSTAR', 'PARABLE', 'EMERGE', 'DIVINITY', 'WITHIN', 'SURFACE', 'SHED',
    'CIRCUMFERENCE', 'DEEP', 'WEB', 'PRIME', 'WISDOM', 'TRUTH', 'SEEK',
    'FIND', 'CICADA', 'LIBER', 'PRIMUS', 'CONSCIOUSNESS', 'ENLIGHTEN',
    'KNOWLEDGE', 'CIPHER', 'SECRET', 'HIDDEN', 'MESSAGE', 'DECODE',
    'UNDERSTAND', 'LEARN', 'GROW', 'TRANSFORM', 'BECOME', 'REVEAL'
]

# =============================================================================
# DATA LOADING
# =============================================================================
def load_pages():
    """Load all pages from RuneSolver.py"""
    data_file = r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py"
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        # Extract only valid runes
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    return pages

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def runes_to_indices(runes):
    """Convert rune string to numpy array of indices"""
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    """Convert indices back to text"""
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def calculate_ioc_batch(data_batch):
    """Calculate IoC for a batch of decryption attempts (GPU optimized)"""
    if USE_GPU:
        data_batch = cp.asarray(data_batch)
    
    n = data_batch.shape[1]
    if n < 2:
        return np.zeros(data_batch.shape[0])
    
    # Count frequencies for each attempt
    batch_size = data_batch.shape[0]
    counts = np.zeros((batch_size, 29), dtype=np.float32)
    
    for i in range(29):
        counts[:, i] = np.sum(data_batch == i, axis=1)
    
    # Calculate IoC
    numerator = np.sum(counts * (counts - 1), axis=1)
    denominator = n * (n - 1)
    ioc = (numerator / denominator) * 29
    
    if USE_GPU:
        return cp.asnumpy(ioc)
    return ioc

def score_text(text):
    """Score text for English-likeness"""
    score = 0
    text_upper = text.upper()
    
    # Score common words
    for word in COMMON_WORDS:
        if word in text_upper:
            score += len(word) * 2
    
    # Score Cicada-specific words (higher weight)
    for word in CICADA_WORDS:
        if word in text_upper:
            score += len(word) * 5
    
    # Penalize unusual patterns
    # Consecutive consonants (too many)
    consonant_run = 0
    vowels = set('AEIOU')
    for c in text_upper:
        if c.isalpha() and c not in vowels:
            consonant_run += 1
            if consonant_run > 5:
                score -= 2
        else:
            consonant_run = 0
    
    # Penalize too many repeated characters
    for i in range(len(text_upper) - 2):
        if text_upper[i] == text_upper[i+1] == text_upper[i+2]:
            score -= 3
    
    return score

# =============================================================================
# CIPHER METHODS (Vectorized)
# =============================================================================

def batch_shift_decrypt(indices, shifts):
    """Decrypt with multiple shift values in parallel"""
    n = len(indices)
    num_shifts = len(shifts)
    
    # Create result matrix
    results = np.zeros((num_shifts, n), dtype=np.int32)
    
    for i, shift in enumerate(shifts):
        results[i] = (indices - shift) % 29
    
    return results

def vigenere_decrypt_batch(indices, keys):
    """Decrypt with multiple Vigenere keys in parallel"""
    n = len(indices)
    num_keys = len(keys)
    
    results = np.zeros((num_keys, n), dtype=np.int32)
    
    for i, key in enumerate(keys):
        key_len = len(key)
        key_expanded = np.tile(key, (n // key_len + 1))[:n]
        results[i] = (indices - key_expanded) % 29
    
    return results

def autokey_decrypt_batch(indices, primers):
    """Decrypt with multiple autokey primers in parallel"""
    n = len(indices)
    num_primers = len(primers)
    
    results = np.zeros((num_primers, n), dtype=np.int32)
    
    for i, primer in enumerate(primers):
        result = []
        key = list(primer)
        for j, c in enumerate(indices):
            if j < len(primer):
                decrypted = (c - key[j]) % 29
            else:
                decrypted = (c - result[j - len(primer)]) % 29
            result.append(decrypted)
        results[i] = result
    
    return results

def running_key_decrypt(indices, key_indices):
    """Decrypt using a running key (another text)"""
    n = min(len(indices), len(key_indices))
    return (indices[:n] - key_indices[:n]) % 29

def gematria_self_decrypt(indices):
    """Each rune decrypted by previous rune's gematria"""
    result = [indices[0]]
    for i in range(1, len(indices)):
        prev_gem = PRIMES[indices[i-1]]
        decrypted = (indices[i] - prev_gem) % 29
        result.append(decrypted)
    return np.array(result, dtype=np.int32)

def progressive_prime_decrypt(indices, start_offset=0, prime_multiplier=1, add_constant=0):
    """Page 56-style prime shift with variants"""
    result = []
    for i, idx in enumerate(indices):
        prime_index = (start_offset + i) % 29
        prime = PRIMES[prime_index]
        shift = (prime * prime_multiplier + add_constant)
        decrypted = (idx - shift) % 29
        result.append(decrypted)
    return np.array(result, dtype=np.int32)

def affine_decrypt(indices, a, b):
    """Affine cipher: P = a^-1 * (C - b) mod 29"""
    # Need modular inverse of a mod 29
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None
    
    a_inv = mod_inverse(a, 29)
    if a_inv is None:
        return indices  # Invalid 'a', return unchanged
    
    return (a_inv * (indices - b)) % 29

# =============================================================================
# BRUTE FORCE SEARCH
# =============================================================================

def exhaustive_shift_search(indices, verbose=True):
    """Test all 29 shift values"""
    if verbose:
        print("\n=== EXHAUSTIVE SHIFT SEARCH ===")
    
    shifts = list(range(29))
    results = batch_shift_decrypt(indices, shifts)
    iocs = calculate_ioc_batch(results)
    
    best_results = []
    for i, (shift, ioc) in enumerate(zip(shifts, iocs)):
        text = indices_to_text(results[i])
        word_score = score_text(text[:200])
        best_results.append((ioc + word_score/100, shift, text[:60], ioc))
    
    best_results.sort(reverse=True)
    
    if verbose:
        for score, shift, text, ioc in best_results[:5]:
            print(f"Shift {shift:2d}: IoC={ioc:.4f}, score={score:.4f}: {text}")
    
    return best_results

def exhaustive_vigenere_search(indices, max_key_len=5, verbose=True):
    """Test Vigenere keys up to a certain length"""
    if verbose:
        print(f"\n=== VIGENERE SEARCH (key len 2-{max_key_len}) ===")
    
    all_results = []
    
    for key_len in range(2, max_key_len + 1):
        # Find optimal key for each position
        best_key = []
        for pos in range(key_len):
            column = indices[pos::key_len]
            best_ioc = 0
            best_shift = 0
            for shift in range(29):
                shifted = (column - shift) % 29
                ioc = calculate_ioc_batch(shifted.reshape(1, -1))[0]
                if ioc > best_ioc:
                    best_ioc = ioc
                    best_shift = shift
            best_key.append(best_shift)
        
        # Decrypt with best key
        key_expanded = np.tile(best_key, (len(indices) // key_len + 1))[:len(indices)]
        decrypted = (indices - key_expanded) % 29
        overall_ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
        text = indices_to_text(decrypted)
        word_score = score_text(text[:200])
        
        key_text = indices_to_text(best_key)
        all_results.append((overall_ioc + word_score/100, key_len, best_key, key_text, text[:60], overall_ioc))
    
    all_results.sort(reverse=True)
    
    if verbose:
        for score, key_len, key, key_text, text, ioc in all_results[:5]:
            print(f"Key len {key_len}, key={key_text}: IoC={ioc:.4f}: {text}")
    
    return all_results

def test_affine_cipher(indices, verbose=True):
    """Test all valid affine cipher combinations"""
    if verbose:
        print("\n=== AFFINE CIPHER SEARCH ===")
    
    # 'a' must be coprime with 29 (29 is prime, so any a from 1-28 works)
    results = []
    
    for a in range(1, 29):
        for b in range(29):
            decrypted = affine_decrypt(indices, a, b)
            ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
            
            if ioc > 1.3:  # Only track promising results
                text = indices_to_text(decrypted)
                word_score = score_text(text[:200])
                results.append((ioc + word_score/100, a, b, text[:60], ioc))
    
    results.sort(reverse=True)
    
    if verbose:
        for score, a, b, text, ioc in results[:5]:
            print(f"Affine (a={a}, b={b}): IoC={ioc:.4f}: {text}")
    
    return results

def test_progressive_prime(indices, verbose=True):
    """Test Page 56-style progressive prime shifts"""
    if verbose:
        print("\n=== PROGRESSIVE PRIME SEARCH ===")
    
    results = []
    
    # Test various constants added to prime
    for add_constant in range(-60, 120):
        for prime_mult in [1, -1]:
            for start_offset in range(29):
                decrypted = progressive_prime_decrypt(
                    indices, 
                    start_offset=start_offset,
                    prime_multiplier=prime_mult,
                    add_constant=add_constant
                )
                ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
                
                if ioc > 1.4:
                    text = indices_to_text(decrypted)
                    word_score = score_text(text[:200])
                    results.append((
                        ioc + word_score/100, 
                        start_offset, 
                        prime_mult, 
                        add_constant, 
                        text[:60],
                        ioc
                    ))
    
    results.sort(reverse=True)
    
    if verbose:
        for score, start, mult, const, text, ioc in results[:5]:
            print(f"Prime(start={start}, mult={mult:+d}, const={const:+d}): IoC={ioc:.4f}: {text}")
    
    return results

def test_running_key(encrypted_indices, key_source_indices, verbose=True):
    """Test running key cipher using known text as key"""
    if verbose:
        print("\n=== RUNNING KEY TEST ===")
    
    results = []
    
    # Try different key offsets
    for offset in range(min(50, len(key_source_indices))):
        key = key_source_indices[offset:]
        decrypted = running_key_decrypt(encrypted_indices, key)
        
        if len(decrypted) < 10:
            continue
            
        ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
        text = indices_to_text(decrypted)
        word_score = score_text(text[:200])
        
        results.append((ioc + word_score/100, offset, text[:60], ioc))
    
    # Also try subtracting in reverse (Beaufort style)
    for offset in range(min(50, len(key_source_indices))):
        key = key_source_indices[offset:]
        n = min(len(encrypted_indices), len(key))
        decrypted = (key[:n] - encrypted_indices[:n]) % 29
        
        if len(decrypted) < 10:
            continue
            
        ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
        text = indices_to_text(decrypted)
        word_score = score_text(text[:200])
        
        results.append((ioc + word_score/100, 1000 + offset, text[:60], ioc))  # Use 1000+ for reverse
    
    results.sort(reverse=True)
    
    if verbose:
        for score, offset, text, ioc in results[:5]:
            offset_str = f"rev_{offset-1000}" if offset >= 1000 else str(offset)
            print(f"Offset {offset_str}: IoC={ioc:.4f}: {text}")
    
    return results

def test_autokey(indices, verbose=True):
    """Test autokey cipher with various primers"""
    if verbose:
        print("\n=== AUTOKEY CIPHER SEARCH ===")
    
    results = []
    
    # Try single-character primers
    for primer in range(29):
        decrypted = autokey_decrypt_batch(indices, [[primer]])[0]
        ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
        text = indices_to_text(decrypted)
        word_score = score_text(text[:200])
        
        results.append((ioc + word_score/100, [primer], text[:60], ioc))
    
    # Try two-character primers
    for p1 in range(29):
        for p2 in range(29):
            primer = [p1, p2]
            decrypted = autokey_decrypt_batch(indices, [primer])[0]
            ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
            
            if ioc > 1.3:
                text = indices_to_text(decrypted)
                word_score = score_text(text[:200])
                results.append((ioc + word_score/100, primer, text[:60], ioc))
    
    results.sort(reverse=True)
    
    if verbose:
        for score, primer, text, ioc in results[:5]:
            primer_text = indices_to_text(primer)
            print(f"Primer '{primer_text}': IoC={ioc:.4f}: {text}")
    
    return results

def test_gematria_variants(indices, verbose=True):
    """Test gematria-based shift variants"""
    if verbose:
        print("\n=== GEMATRIA VARIANT SEARCH ===")
    
    results = []
    
    # Self-shift
    decrypted = gematria_self_decrypt(indices)
    ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
    text = indices_to_text(decrypted)
    word_score = score_text(text[:200])
    results.append((ioc + word_score/100, "self-shift", text[:60], ioc))
    
    # Forward shift (next rune's gematria)
    result = []
    for i in range(len(indices) - 1):
        next_gem = PRIMES[indices[i+1]]
        decrypted_char = (indices[i] - next_gem) % 29
        result.append(decrypted_char)
    result.append(indices[-1])  # Last char unshifted
    decrypted = np.array(result, dtype=np.int32)
    ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
    text = indices_to_text(decrypted)
    word_score = score_text(text[:200])
    results.append((ioc + word_score/100, "forward-shift", text[:60], ioc))
    
    # XOR with gematria (mod 29)
    for offset in range(-29, 30):
        result = []
        for i, idx in enumerate(indices):
            gem = PRIMES[idx]
            decrypted_char = (idx ^ (gem + offset)) % 29
            result.append(decrypted_char)
        decrypted = np.array(result, dtype=np.int32)
        ioc = calculate_ioc_batch(decrypted.reshape(1, -1))[0]
        
        if ioc > 1.3:
            text = indices_to_text(decrypted)
            word_score = score_text(text[:200])
            results.append((ioc + word_score/100, f"xor-gem+{offset}", text[:60], ioc))
    
    results.sort(reverse=True)
    
    if verbose:
        for score, method, text, ioc in results[:5]:
            print(f"{method}: IoC={ioc:.4f}: {text}")
    
    return results

# =============================================================================
# MAIN SOLVER
# =============================================================================

def comprehensive_solve(page_indices, parable_indices=None, verbose=True):
    """Run all solving methods on a page"""
    all_results = []
    
    # Basic shift search
    shift_results = exhaustive_shift_search(page_indices, verbose=verbose)
    all_results.extend([("shift", r) for r in shift_results])
    
    # Vigenere search
    vig_results = exhaustive_vigenere_search(page_indices, max_key_len=6, verbose=verbose)
    all_results.extend([("vigenere", r) for r in vig_results])
    
    # Affine cipher
    affine_results = test_affine_cipher(page_indices, verbose=verbose)
    all_results.extend([("affine", r) for r in affine_results])
    
    # Progressive prime
    prime_results = test_progressive_prime(page_indices, verbose=verbose)
    all_results.extend([("prime", r) for r in prime_results])
    
    # Autokey
    autokey_results = test_autokey(page_indices, verbose=verbose)
    all_results.extend([("autokey", r) for r in autokey_results])
    
    # Gematria variants
    gem_results = test_gematria_variants(page_indices, verbose=verbose)
    all_results.extend([("gematria", r) for r in gem_results])
    
    # Running key with PARABLE if available
    if parable_indices is not None:
        rk_results = test_running_key(page_indices, parable_indices, verbose=verbose)
        all_results.extend([("running_key", r) for r in rk_results])
    
    return all_results

def main():
    print("="*70)
    print("GPU-ACCELERATED LIBER PRIMUS SOLVER")
    print("="*70)
    
    start_time = time.time()
    
    # Load pages
    pages = load_pages()
    print(f"\nLoaded {len(pages)} pages")
    
    # Get PARABLE text (Page 57) as potential running key
    parable_indices = None
    if 57 in pages:
        parable_indices = runes_to_indices(pages[57])
        print(f"PARABLE text: {len(parable_indices)} runes available as running key")
    
    # Focus on pages with most potential
    priority_pages = [55, 42, 53, 32, 49, 28]  # Ranked by decryption potential
    
    best_overall = []
    
    for page_num in priority_pages:
        if page_num not in pages:
            continue
            
        print(f"\n{'='*70}")
        print(f"ANALYZING PAGE {page_num}")
        print(f"{'='*70}")
        
        page_indices = runes_to_indices(pages[page_num])
        print(f"Page {page_num}: {len(page_indices)} runes")
        
        results = comprehensive_solve(page_indices, parable_indices, verbose=True)
        
        # Get best results for this page
        sorted_results = sorted(
            [(method, r[0], r[-2] if len(r) > 2 else r[1], r[-1]) 
             for method, r in results if len(r) > 0],
            key=lambda x: x[1],
            reverse=True
        )
        
        for method, score, text, ioc in sorted_results[:3]:
            best_overall.append((score, page_num, method, text, ioc))
    
    # Summary
    print("\n" + "="*70)
    print("TOP RESULTS ACROSS ALL PAGES")
    print("="*70)
    
    best_overall.sort(reverse=True)
    for score, page, method, text, ioc in best_overall[:20]:
        print(f"Page {page:2d} [{method:12s}]: IoC={ioc:.4f}, score={score:.4f}: {text[:50]}")
    
    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.2f}s")
    
    # Look for English words in top results
    print("\n" + "="*70)
    print("LOOKING FOR ENGLISH PATTERNS")
    print("="*70)
    
    for score, page, method, text, ioc in best_overall[:10]:
        # Check for common English words
        found_words = []
        text_upper = text.upper()
        for word in COMMON_WORDS + CICADA_WORDS:
            if word in text_upper:
                found_words.append(word)
        
        if found_words:
            print(f"Page {page} [{method}]: Found words: {', '.join(found_words)}")
            print(f"  Text: {text}")

if __name__ == "__main__":
    main()

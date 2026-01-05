#!/usr/bin/env python3
"""
GPU-Accelerated Liber Primus Cipher Cracker
=============================================
Uses CuPy/Numba for massively parallel brute force attacks on the
unsolved Cicada 3301 Liber Primus.

Attacks implemented:
1. Prime shift with variable offsets (Page 56 method generalization)
2. Vigenère with all possible key lengths
3. Hill cipher 2x2 matrix (29^4 = ~700k combinations)
4. Autokey cipher variations
5. Running key with LP text as key

Author: Cicada Solver
"""

import numpy as np
from collections import Counter
from pathlib import Path
import math
import time
import sys

# Try to import GPU libraries
try:
    import cupy as cp
    # Test if CUDA actually works
    _ = cp.array([1, 2, 3]) + 1
    HAS_CUPY = True
    print("✓ CuPy available - GPU acceleration enabled")
except Exception:
    cp = np
    HAS_CUPY = False
    print("✗ CuPy/CUDA not available - using CPU (NumPy)")

try:
    from numba import cuda, jit
    HAS_NUMBA = True
    print("✓ Numba available")
except ImportError:
    HAS_NUMBA = False
    print("✗ Numba not available")

# =============================================================================
# CONSTANTS
# =============================================================================

ALPHABET_SIZE = 29

# Rune Unicode to index mapping
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

# English letter equivalents
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

# Prime sequence for prime-shift cipher
def sieve_primes(n):
    """Generate first n primes."""
    if n < 1:
        return []
    upper = max(15, int(n * (math.log(n) + math.log(math.log(n)))) + 100) if n >= 6 else 15
    sieve = np.ones(upper + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(upper**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return np.where(sieve)[0][:n]

PRIMES = sieve_primes(20000)

# English bigram log-probabilities (for scoring)
# From standard English corpus - higher = more common
COMMON_BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.20, 'OF': 1.17,
    'ED': 1.17, 'IS': 1.13, 'IT': 1.12, 'AL': 1.09, 'AR': 1.07,
    'ST': 1.05, 'TO': 1.04, 'NT': 1.04, 'NG': 0.95, 'SE': 0.93,
    'HA': 0.93, 'AS': 0.87, 'OU': 0.87, 'IO': 0.83, 'LE': 0.83,
    'VE': 0.83, 'CO': 0.79, 'ME': 0.79, 'DE': 0.76, 'HI': 0.76,
    'RI': 0.73, 'RO': 0.73, 'IC': 0.70, 'NE': 0.69, 'EA': 0.69,
    'RA': 0.69, 'CE': 0.65
}

# =============================================================================
# TEXT LOADING AND CONVERSION
# =============================================================================

def load_liber_primus(filepath):
    """Load and extract runes from Liber Primus."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def text_to_indices(text):
    """Convert runic text to numpy array of indices."""
    indices = [RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX]
    return np.array(indices, dtype=np.int32)

def indices_to_text(indices):
    """Convert indices back to runic text."""
    return ''.join(IDX_TO_RUNE[int(i) % 29] for i in indices)

def indices_to_english(indices):
    """Convert indices to English letters."""
    result = []
    for i in indices:
        result.append(LETTERS[int(i) % 29])
    return ''.join(result)

# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

def compute_ioc(indices):
    """Compute Index of Coincidence."""
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return sum_ni / (n * (n - 1))

def compute_ioc_normalized(indices):
    """Compute normalized IoC (1.0 = random for 29 symbols)."""
    return compute_ioc(indices) * ALPHABET_SIZE

def score_bigrams(indices):
    """Score based on English bigram frequencies."""
    if len(indices) < 2:
        return 0.0
    
    score = 0.0
    count = 0
    for i in range(len(indices) - 1):
        bg = LETTERS[indices[i]] + LETTERS[indices[i+1]]
        if bg in COMMON_BIGRAMS:
            score += COMMON_BIGRAMS[bg]
            count += 1
    
    return score / (len(indices) - 1) if len(indices) > 1 else 0

def combined_score(indices):
    """Combined scoring: IoC + bigram frequency."""
    ioc = compute_ioc_normalized(indices)
    bigram = score_bigrams(indices)
    # Weight IoC heavily - we want it to increase from ~1.0 toward ~1.7
    return ioc * 10 + bigram

# =============================================================================
# CIPHER OPERATIONS (NumPy/CuPy)
# =============================================================================

def prime_shift_decrypt(ciphertext, offset, xp=np):
    """
    Prime shift decryption (Page 56 method generalization).
    plaintext[i] = ciphertext[i] - (prime[i] + offset) mod 29
    """
    n = len(ciphertext)
    primes = xp.asarray(PRIMES[:n])
    shifts = (primes + offset) % 29
    return (ciphertext - shifts) % 29

def caesar_shift(ciphertext, shift, xp=np):
    """Simple Caesar shift."""
    return (ciphertext - shift) % 29

def vigenere_decrypt(ciphertext, key, xp=np):
    """Vigenère cipher decryption."""
    key_len = len(key)
    key_stream = xp.tile(key, (len(ciphertext) // key_len + 1))[:len(ciphertext)]
    return (ciphertext - key_stream) % 29

def autokey_decrypt(ciphertext, primer_idx, xp=np):
    """
    Autokey cipher decryption.
    Key = primer + plaintext
    """
    n = len(ciphertext)
    plaintext = xp.zeros(n, dtype=xp.int32)
    plaintext[0] = (ciphertext[0] - primer_idx) % 29
    
    for i in range(1, n):
        plaintext[i] = (ciphertext[i] - plaintext[i-1]) % 29
    
    return plaintext

def hill_2x2_decrypt(ciphertext, matrix, xp=np):
    """
    Hill cipher decryption with 2x2 matrix.
    Must compute modular inverse of matrix.
    """
    # Ensure even length
    if len(ciphertext) % 2 != 0:
        ciphertext = xp.append(ciphertext, [0])
    
    n = len(ciphertext)
    pairs = ciphertext.reshape(-1, 2)
    
    # Compute matrix inverse mod 29
    a, b, c, d = matrix.flatten()
    det = (a * d - b * c) % 29
    
    # Find modular multiplicative inverse of determinant
    det_inv = pow(int(det), -1, 29)
    
    # Adjugate matrix
    inv_matrix = xp.array([[d, -b], [-c, a]], dtype=xp.int32)
    inv_matrix = (det_inv * inv_matrix) % 29
    
    # Decrypt
    plaintext_pairs = (pairs @ inv_matrix.T) % 29
    return plaintext_pairs.flatten()[:n]

def running_key_decrypt(ciphertext, key, xp=np):
    """Running key cipher - subtract key from ciphertext mod 29."""
    key_len = len(key)
    if len(ciphertext) > key_len:
        # Extend key by repeating
        key = xp.tile(key, (len(ciphertext) // key_len + 1))[:len(ciphertext)]
    return (ciphertext - key[:len(ciphertext)]) % 29

# =============================================================================
# BRUTE FORCE ATTACKS
# =============================================================================

def attack_prime_shift(ciphertext, offset_range=range(0, 500)):
    """
    Brute force prime shift with different offsets.
    """
    print(f"\n{'='*60}")
    print("PRIME SHIFT ATTACK (Page 56 method generalization)")
    print(f"{'='*60}")
    print(f"Testing offsets: {offset_range.start} to {offset_range.stop-1}")
    
    xp = cp if HAS_CUPY else np
    cipher_gpu = xp.asarray(ciphertext)
    
    results = []
    
    for offset in offset_range:
        plaintext = prime_shift_decrypt(cipher_gpu, offset, xp)
        
        if HAS_CUPY:
            plaintext_cpu = cp.asnumpy(plaintext)
        else:
            plaintext_cpu = plaintext
        
        ioc = compute_ioc_normalized(plaintext_cpu)
        score = combined_score(plaintext_cpu)
        
        results.append((offset, ioc, score, plaintext_cpu))
        
        if ioc > 1.2:  # Promising result
            eng = indices_to_english(plaintext_cpu[:50])
            print(f"  Offset {offset:3d}: IoC={ioc:.4f} score={score:.2f} | {eng}...")
    
    # Sort by score
    results.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nTop 5 results:")
    for offset, ioc, score, pt in results[:5]:
        eng = indices_to_english(pt[:60])
        print(f"  Offset {offset:3d}: IoC={ioc:.4f} score={score:.2f}")
        print(f"    {eng}...")
    
    return results

def attack_vigenere(ciphertext, max_key_length=15):
    """
    Brute force Vigenère with different key lengths.
    For each length, try to find the best key.
    """
    print(f"\n{'='*60}")
    print("VIGENÈRE ATTACK")
    print(f"{'='*60}")
    print(f"Testing key lengths: 1 to {max_key_length}")
    
    xp = cp if HAS_CUPY else np
    cipher_gpu = xp.asarray(ciphertext)
    n = len(ciphertext)
    
    results = []
    
    for key_len in range(1, max_key_length + 1):
        # For each position in the key, find the shift that gives best IoC
        best_key = []
        
        for pos in range(key_len):
            # Extract every key_len-th character starting at pos
            column = ciphertext[pos::key_len]
            
            # Try each shift
            best_shift = 0
            best_ioc = 0
            
            for shift in range(29):
                shifted = (column - shift) % 29
                ioc = compute_ioc_normalized(shifted)
                if ioc > best_ioc:
                    best_ioc = ioc
                    best_shift = shift
            
            best_key.append(best_shift)
        
        # Decrypt with found key
        key = xp.array(best_key, dtype=xp.int32)
        plaintext = vigenere_decrypt(cipher_gpu, key, xp)
        
        if HAS_CUPY:
            plaintext_cpu = cp.asnumpy(plaintext)
        else:
            plaintext_cpu = plaintext
        
        ioc = compute_ioc_normalized(plaintext_cpu)
        score = combined_score(plaintext_cpu)
        
        key_str = ''.join(LETTERS[k] for k in best_key)
        results.append((key_len, key_str, ioc, score, plaintext_cpu))
        
        eng = indices_to_english(plaintext_cpu[:40])
        print(f"  Len {key_len:2d}: IoC={ioc:.4f} key={key_str[:20]:20s} | {eng}...")
    
    results.sort(key=lambda x: x[3], reverse=True)
    return results

def attack_hill_2x2(ciphertext, sample_size=500):
    """
    Brute force 2x2 Hill cipher.
    29^4 = 707,281 possible matrices, but only ~1/29 are invertible.
    """
    print(f"\n{'='*60}")
    print("HILL CIPHER 2x2 ATTACK")
    print(f"{'='*60}")
    print(f"Testing all 29^4 = 707,281 matrices (checking invertibility)")
    
    xp = cp if HAS_CUPY else np
    cipher_sample = ciphertext[:sample_size]  # Use sample for speed
    
    results = []
    tested = 0
    start_time = time.time()
    
    for a in range(29):
        for b in range(29):
            for c in range(29):
                for d in range(29):
                    # Check if matrix is invertible (det != 0 and coprime to 29)
                    det = (a * d - b * c) % 29
                    if det == 0 or math.gcd(det, 29) != 1:
                        continue
                    
                    tested += 1
                    matrix = np.array([[a, b], [c, d]], dtype=np.int32)
                    
                    try:
                        plaintext = hill_2x2_decrypt(cipher_sample, matrix, np)
                        ioc = compute_ioc_normalized(plaintext)
                        
                        if ioc > 1.3:  # Promising
                            score = combined_score(plaintext)
                            results.append(((a, b, c, d), ioc, score, plaintext))
                            eng = indices_to_english(plaintext[:30])
                            print(f"  Matrix [{a},{b};{c},{d}]: IoC={ioc:.4f} | {eng}...")
                    except:
                        continue
        
        # Progress update
        if (a + 1) % 5 == 0:
            elapsed = time.time() - start_time
            print(f"  Progress: {((a+1)/29*100):.0f}% ({tested} matrices tested, {elapsed:.1f}s)")
    
    print(f"\nTested {tested} invertible matrices in {time.time()-start_time:.1f}s")
    
    results.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nTop 5 results:")
    for matrix, ioc, score, pt in results[:5]:
        eng = indices_to_english(pt[:50])
        print(f"  Matrix {matrix}: IoC={ioc:.4f} score={score:.2f}")
        print(f"    {eng}...")
    
    return results

def attack_autokey(ciphertext):
    """
    Autokey cipher attack - try each possible primer.
    """
    print(f"\n{'='*60}")
    print("AUTOKEY CIPHER ATTACK")
    print(f"{'='*60}")
    print(f"Testing all 29 primer values")
    
    results = []
    
    for primer in range(29):
        plaintext = autokey_decrypt(ciphertext, primer, np)
        ioc = compute_ioc_normalized(plaintext)
        score = combined_score(plaintext)
        
        results.append((primer, ioc, score, plaintext))
        
        eng = indices_to_english(plaintext[:50])
        print(f"  Primer {LETTERS[primer]:3s}: IoC={ioc:.4f} score={score:.2f} | {eng}...")
    
    results.sort(key=lambda x: x[2], reverse=True)
    return results

def attack_running_key_with_lp(ciphertext, lp_text):
    """
    Try using other parts of Liber Primus as the running key.
    """
    print(f"\n{'='*60}")
    print("RUNNING KEY ATTACK (using LP as key source)")
    print(f"{'='*60}")
    
    lp_indices = text_to_indices(lp_text)
    n = len(ciphertext)
    
    results = []
    
    # Try different starting positions in the LP as key
    for start in range(0, len(lp_indices) - n, n // 2):
        key = lp_indices[start:start + n]
        if len(key) < n:
            continue
        
        plaintext = running_key_decrypt(ciphertext, key, np)
        ioc = compute_ioc_normalized(plaintext)
        score = combined_score(plaintext)
        
        results.append((start, ioc, score, plaintext))
        
        if ioc > 1.2:
            eng = indices_to_english(plaintext[:50])
            print(f"  Start {start:5d}: IoC={ioc:.4f} score={score:.2f} | {eng}...")
    
    results.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nTop 5 results:")
    for start, ioc, score, pt in results[:5]:
        eng = indices_to_english(pt[:60])
        print(f"  Key start {start}: IoC={ioc:.4f} score={score:.2f}")
        print(f"    {eng}...")
    
    return results

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("LIBER PRIMUS GPU-ACCELERATED CIPHER CRACKER")
    print("="*70)
    
    # Load Liber Primus
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    if not lp_path.exists():
        print(f"Error: Could not find {lp_path}")
        return
    
    print(f"\nLoading: {lp_path}")
    lp_text = load_liber_primus(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    print(f"Total runes: {len(lp_indices)}")
    print(f"Baseline IoC: {compute_ioc_normalized(lp_indices):.4f}")
    
    # Work on a sample for faster testing
    sample_size = 1000
    sample = lp_indices[:sample_size]
    print(f"\nUsing first {sample_size} runes for attacks...")
    
    # Run attacks
    print("\n" + "#"*70)
    print("# RUNNING ATTACKS")
    print("#"*70)
    
    # 1. Prime shift attack
    prime_results = attack_prime_shift(sample, range(0, 200))
    
    # 2. Vigenère attack
    vigenere_results = attack_vigenere(sample, max_key_length=12)
    
    # 3. Autokey attack
    autokey_results = attack_autokey(sample)
    
    # 4. Hill cipher attack (this takes longer)
    hill_results = attack_hill_2x2(sample, sample_size=400)
    
    # 5. Running key with LP as source
    running_results = attack_running_key_with_lp(sample, lp_text)
    
    print("\n" + "="*70)
    print("ATTACK SUMMARY")
    print("="*70)
    
    all_results = []
    
    if prime_results:
        best = prime_results[0]
        all_results.append(("Prime Shift", best[0], best[1], best[2]))
    
    if vigenere_results:
        best = vigenere_results[0]
        all_results.append(("Vigenère", best[1], best[2], best[3]))
    
    if autokey_results:
        best = autokey_results[0]
        all_results.append(("Autokey", best[0], best[1], best[2]))
    
    if hill_results:
        best = hill_results[0]
        all_results.append(("Hill 2x2", best[0], best[1], best[2]))
    
    if running_results:
        best = running_results[0]
        all_results.append(("Running Key", best[0], best[1], best[2]))
    
    all_results.sort(key=lambda x: x[3], reverse=True)
    
    print("\nBest results from each attack:")
    for name, param, ioc, score in all_results:
        print(f"  {name:15s}: param={param}, IoC={ioc:.4f}, score={score:.2f}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

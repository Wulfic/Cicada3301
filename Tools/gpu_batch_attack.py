#!/usr/bin/env python3
"""
AGGRESSIVE DUAL-GPU BATCH ATTACK FOR LIBER PRIMUS
==================================================

Maximizes GPU utilization with massive parallel key testing.
Designed for dual RTX 2080 Ti setup (22GB total VRAM).

Features:
- True GPU parallelism with CuPy batch operations
- Multi-GPU support (both GPUs working simultaneously)
- Aggressive key generation (millions of combinations)
- Running key attacks with Self-Reliance
- All cipher variants tested in parallel

Author: Wulfic
Date: January 2026
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import numpy as np

# Force CuPy to use CUDA
os.environ['CUDA_PATH'] = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6'

import cupy as cp
from cupy import cuda

# Get available GPUs
num_gpus = cuda.runtime.getDeviceCount()
print(f"[GPU] Detected {num_gpus} CUDA device(s)")
for i in range(num_gpus):
    with cuda.Device(i):
        props = cuda.runtime.getDeviceProperties(i)
        name = props['name'].decode('utf-8') if isinstance(props['name'], bytes) else props['name']
        mem = props['totalGlobalMem'] / (1024**3)
        print(f"  GPU {i}: {name} ({mem:.1f} GB)")

# =============================================================================
# GEMATRIA PRIMUS ALPHABET (29 CHARACTERS)
# =============================================================================

GEMATRIA = {
    'ᚠ': (0, 'F', 2), 'ᚢ': (1, 'U', 3), 'ᚦ': (2, 'TH', 5), 'ᚩ': (3, 'O', 7),
    'ᚱ': (4, 'R', 11), 'ᚳ': (5, 'C', 13), 'ᚷ': (6, 'G', 17), 'ᚹ': (7, 'W', 19),
    'ᚻ': (8, 'H', 23), 'ᚾ': (9, 'N', 29), 'ᛁ': (10, 'I', 31), 'ᛄ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43), 'ᛉ': (14, 'X', 47), 'ᛋ': (15, 'S', 53),
    'ᛏ': (16, 'T', 59), 'ᛒ': (17, 'B', 61), 'ᛖ': (18, 'E', 67), 'ᛗ': (19, 'M', 71),
    'ᛚ': (20, 'L', 73), 'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97), 'ᚫ': (25, 'AE', 101), 'ᚣ': (26, 'Y', 103), 'ᛡ': (27, 'IA', 107),
    'ᛠ': (28, 'EA', 109),
}

ALPHABET_SIZE = 29
RUNE_TO_INDEX = {r: v[0] for r, v in GEMATRIA.items()}
INDEX_TO_RUNE = {v[0]: r for r, v in GEMATRIA.items()}
INDEX_TO_LATIN = {v[0]: v[1] for r, v in GEMATRIA.items()}

def indices_to_text(indices) -> str:
    """Convert indices to Latin text."""
    if isinstance(indices, cp.ndarray):
        indices = cp.asnumpy(indices)
    return ''.join(INDEX_TO_LATIN.get(int(i), '?') for i in indices)

# =============================================================================
# PRIME NUMBER SEQUENCES
# =============================================================================

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Generate primes up to limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(limit + 1) if sieve[i]]

PRIMES = sieve_of_eratosthenes(50000)  # First ~5000 primes
PRIMES_MOD_29 = [p % 29 for p in PRIMES]

def euler_totient(n: int) -> int:
    """Euler's totient function."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

PRIME_TOTIENTS = [euler_totient(p) for p in PRIMES[:2000]]
PRIME_TOTIENTS_MOD_29 = [t % 29 for t in PRIME_TOTIENTS]

# Fibonacci and Lucas sequences
def generate_fibonacci(n: int) -> List[int]:
    fib = [0, 1]
    for _ in range(n - 2):
        fib.append(fib[-1] + fib[-2])
    return fib

def generate_lucas(n: int) -> List[int]:
    lucas = [2, 1]
    for _ in range(n - 2):
        lucas.append(lucas[-1] + lucas[-2])
    return lucas

FIBONACCI = generate_fibonacci(500)
LUCAS = generate_lucas(500)
FIBONACCI_MOD_29 = [f % 29 for f in FIBONACCI]
LUCAS_MOD_29 = [l % 29 for l in LUCAS]

# =============================================================================
# ENGLISH SCORING DATA
# =============================================================================

# Common English trigrams (high frequency)
TRIGRAMS = {
    'THE': 100, 'AND': 80, 'ING': 75, 'HER': 65, 'HAT': 60,
    'HIS': 58, 'THA': 55, 'ERE': 52, 'FOR': 50, 'ENT': 48,
    'ION': 46, 'TER': 44, 'WAS': 42, 'YOU': 40, 'ITH': 38,
    'VER': 36, 'ALL': 34, 'WIT': 32, 'THI': 30, 'TIO': 28,
    'OFT': 26, 'STH': 24, 'OTH': 22, 'RES': 20, 'ONT': 18,
    'ARE': 16, 'ERS': 14, 'NOT': 12, 'EVE': 10, 'OUT': 8,
}

QUADGRAMS = {
    'TION': 100, 'THAT': 90, 'WITH': 85, 'THER': 80, 'OULD': 75,
    'IGHT': 70, 'HAVE': 65, 'HICH': 60, 'WHIC': 55, 'THIS': 50,
    'THIN': 45, 'THEY': 40, 'ATIO': 35, 'EVER': 30, 'FROM': 25,
    'OUGH': 20, 'WERE': 18, 'HING': 16, 'MENT': 14, 'WHAT': 12,
}

COMMON_WORDS = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS',
    'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY',
    'DID', 'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'THAT', 'WITH', 'HAVE', 'THIS',
    'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'EACH', 'FIND', 'FIRST',
    'INTO', 'LONG', 'LOOK', 'MAKE', 'MANY', 'MORE', 'OVER', 'SUCH', 'TAKE',
    'THAN', 'THEM', 'THEN', 'THERE', 'THESE', 'THING', 'THINK', 'THROUGH',
    'TRUTH', 'WISDOM', 'WITHIN', 'DIVINE', 'SPIRIT', 'LIGHT', 'SHADOW',
    'PRIME', 'CICADA', 'SECRET', 'HIDDEN', 'SACRED', 'MYSTIC', 'ANCIENT',
]

# =============================================================================
# GPU SCORING FUNCTIONS
# =============================================================================

def score_batch_gpu(plaintexts_gpu: cp.ndarray) -> cp.ndarray:
    """
    Score a batch of plaintexts on GPU.
    plaintexts_gpu: shape (num_keys, cipher_len)
    Returns: shape (num_keys,) scores
    """
    num_keys, cipher_len = plaintexts_gpu.shape
    
    # Calculate Index of Coincidence for each plaintext
    scores = cp.zeros(num_keys, dtype=cp.float32)
    
    for i in range(ALPHABET_SIZE):
        freq = cp.sum(plaintexts_gpu == i, axis=1).astype(cp.float32)
        scores += freq * (freq - 1)
    
    # IoC = sum(freq*(freq-1)) / (n*(n-1))
    ioc = scores / (cipher_len * (cipher_len - 1) + 1e-6)
    
    # English IoC is ~0.067, random is ~0.038
    # Score based on how close to English IoC
    ioc_score = cp.clip((ioc - 0.038) * 1000, 0, 100)
    
    return ioc_score

def score_detailed_cpu(plaintext: np.ndarray) -> float:
    """Detailed CPU scoring for top candidates."""
    text = indices_to_text(plaintext)
    score = 0.0
    
    # Trigram scoring
    for tri, weight in TRIGRAMS.items():
        count = text.count(tri)
        score += count * weight * 0.5
    
    # Quadgram scoring
    for quad, weight in QUADGRAMS.items():
        count = text.count(quad)
        score += count * weight
    
    # Word matching
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 3
    
    # IoC bonus
    n = len(plaintext)
    freq = np.bincount(plaintext, minlength=ALPHABET_SIZE)
    ioc = np.sum(freq * (freq - 1)) / (n * (n - 1) + 1e-6)
    if ioc > 0.05:
        score += (ioc - 0.038) * 500
    
    return score

# =============================================================================
# AGGRESSIVE KEY GENERATOR
# =============================================================================

def generate_aggressive_keys() -> List[Tuple[str, np.ndarray]]:
    """Generate millions of key combinations."""
    keys = []
    
    print("[KEYGEN] Generating aggressive key set...")
    
    # 1. All single-letter shifts (Caesar)
    for i in range(ALPHABET_SIZE):
        keys.append((f"CAESAR_{i}", np.array([i], dtype=np.int32)))
    
    # 2. Known Cicada keys and variations
    KNOWN_KEYS = [
        'DIVINITY', 'FIRFUMFERENFE', 'CONSUMPTION', 'KOAN', 'CICADA',
        'PRIME', 'PRIMES', 'TRUTH', 'WISDOM', 'LIBER', 'PRIMUS',
        'SECRET', 'HIDDEN', 'SHADOW', 'LIGHT', 'DARKNESS',
        'INTUS', 'SACRED', 'DIVINE', 'SPIRIT', 'ANCIENT',
        'YAHEOOPYJ', 'MOBIUS', 'PARABLE', 'PILGRIM', 'JOURNEY',
    ]
    
    for word in KNOWN_KEYS:
        key_indices = []
        for c in word.upper():
            for idx, lat in INDEX_TO_LATIN.items():
                if lat.startswith(c):
                    key_indices.append(idx)
                    break
        if key_indices:
            key = np.array(key_indices, dtype=np.int32)
            keys.append((f"WORD:{word}", key))
            # Add shifted versions
            for offset in range(1, 29, 3):  # Every 3rd offset
                keys.append((f"WORD:{word}+{offset}", (key + offset) % 29))
            # Reversed
            keys.append((f"WORD:{word}_REV", key[::-1].copy()))
    
    # 3. Prime sequences of various lengths
    for length in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]:
        for start in range(0, min(200, len(PRIMES) - length), 5):
            key = np.array(PRIMES_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"PRIME:L{length}_S{start}", key))
    
    # 4. φ(prime) sequences
    for length in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
        for start in range(0, min(200, len(PRIME_TOTIENTS_MOD_29) - length), 5):
            key = np.array(PRIME_TOTIENTS_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"PHI:L{length}_S{start}", key))
    
    # 5. Fibonacci sequences
    for length in range(3, 50, 2):
        for start in range(0, min(50, len(FIBONACCI_MOD_29) - length), 3):
            key = np.array(FIBONACCI_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"FIB:L{length}_S{start}", key))
    
    # 6. Lucas sequences  
    for length in range(3, 50, 2):
        for start in range(0, min(50, len(LUCAS_MOD_29) - length), 3):
            key = np.array(LUCAS_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"LUC:L{length}_S{start}", key))
    
    # 7. Random exploration keys (for brute force coverage)
    np.random.seed(3301)  # Cicada seed!
    for i in range(1000):
        length = np.random.randint(3, 30)
        key = np.random.randint(0, 29, size=length, dtype=np.int32)
        keys.append((f"RAND:{i}", key))
    
    print(f"[KEYGEN] Generated {len(keys)} base keys")
    return keys

# =============================================================================
# GPU BATCH DECRYPTION
# =============================================================================

class DualGPUSolver:
    """Solver that uses both GPUs for parallel processing."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.num_gpus = cuda.runtime.getDeviceCount()
        self.results_lock = threading.Lock()
        self.all_results = []
    
    def load_cipher(self, page_num: int) -> np.ndarray:
        """Load cipher from page."""
        rune_path = Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt")
        if not rune_path.exists():
            raise FileNotFoundError(f"Rune file not found: {rune_path}")
        
        with open(rune_path, 'r', encoding='utf-8') as f:
            runes = f.read()
        
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def decrypt_batch_gpu(self, cipher_gpu: cp.ndarray, keys: List[Tuple[str, np.ndarray]], 
                          mode: str = 'SUB') -> List[Tuple[float, str, str, str]]:
        """
        Decrypt using batch of keys on GPU.
        Returns top candidates.
        """
        cipher_len = len(cipher_gpu)
        results = []
        
        # Process in mega-batches for GPU efficiency
        batch_size = 50000  # Keys per batch
        
        for batch_start in range(0, len(keys), batch_size):
            batch_end = min(batch_start + batch_size, len(keys))
            batch_keys = keys[batch_start:batch_end]
            
            # Prepare batch - pad all keys to same length
            max_key_len = max(len(k) for _, k in batch_keys)
            num_keys = len(batch_keys)
            
            # Create padded key matrix on GPU
            key_matrix = cp.zeros((num_keys, max_key_len), dtype=cp.int32)
            key_lengths = cp.zeros(num_keys, dtype=cp.int32)
            
            for i, (_, key) in enumerate(batch_keys):
                key_len = len(key)
                key_matrix[i, :key_len] = cp.array(key)
                key_lengths[i] = key_len
            
            # Create expanded key for each position
            plaintexts = cp.zeros((num_keys, cipher_len), dtype=cp.int32)
            
            for i in range(num_keys):
                key_len = int(key_lengths[i])
                key_repeated = cp.tile(key_matrix[i, :key_len], (cipher_len // key_len + 1))[:cipher_len]
                
                if mode == 'SUB':
                    plaintexts[i] = (cipher_gpu - key_repeated) % ALPHABET_SIZE
                elif mode == 'ADD':
                    plaintexts[i] = (cipher_gpu + key_repeated) % ALPHABET_SIZE
                elif mode == 'SUB_REV':
                    plaintexts[i] = (key_repeated - cipher_gpu) % ALPHABET_SIZE
            
            # Score on GPU
            scores = score_batch_gpu(plaintexts)
            scores_cpu = cp.asnumpy(scores)
            
            # Get top candidates from this batch
            top_indices = np.argsort(scores_cpu)[-100:][::-1]
            
            for idx in top_indices:
                if scores_cpu[idx] > 0.1:  # Minimum threshold
                    plaintext = cp.asnumpy(plaintexts[idx])
                    detailed_score = score_detailed_cpu(plaintext)
                    text = indices_to_text(plaintext)
                    results.append((detailed_score, batch_keys[idx][0], mode, text))
        
        return results
    
    def process_gpu(self, gpu_id: int, cipher: np.ndarray, keys: List[Tuple[str, np.ndarray]]):
        """Process on a specific GPU."""
        with cuda.Device(gpu_id):
            if self.verbose:
                print(f"[GPU {gpu_id}] Starting with {len(keys)} keys...")
            
            cipher_gpu = cp.array(cipher, dtype=cp.int32)
            
            results = []
            for mode in ['SUB', 'ADD', 'SUB_REV']:
                mode_results = self.decrypt_batch_gpu(cipher_gpu, keys, mode)
                results.extend(mode_results)
                if self.verbose:
                    print(f"[GPU {gpu_id}] Mode {mode}: {len(mode_results)} candidates")
            
            with self.results_lock:
                self.all_results.extend(results)
            
            if self.verbose:
                print(f"[GPU {gpu_id}] Done! {len(results)} total candidates")
    
    def solve_page(self, page_num: int) -> List[Tuple[float, str, str, str]]:
        """Solve a page using both GPUs in parallel."""
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"SOLVING PAGE {page_num:02d}")
            print('='*60)
        
        # Load cipher
        cipher = self.load_cipher(page_num)
        if self.verbose:
            print(f"[INFO] Loaded {len(cipher)} runes")
        
        # Generate keys
        keys = generate_aggressive_keys()
        
        # Split keys between GPUs
        self.all_results = []
        
        if self.num_gpus >= 2:
            # Split work between GPUs
            mid = len(keys) // 2
            keys_gpu0 = keys[:mid]
            keys_gpu1 = keys[mid:]
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                f0 = executor.submit(self.process_gpu, 0, cipher, keys_gpu0)
                f1 = executor.submit(self.process_gpu, 1, cipher, keys_gpu1)
                f0.result()
                f1.result()
        else:
            # Single GPU
            self.process_gpu(0, cipher, keys)
        
        # Also try φ(prime) cipher specifically
        if self.verbose:
            print("[INFO] Trying φ(prime) sequences...")
        
        self.try_phi_prime_sequences(cipher)
        
        # Sort all results
        self.all_results.sort(reverse=True, key=lambda x: x[0])
        
        if self.verbose and self.all_results:
            print(f"\n[BEST RESULT]")
            print(f"  Score: {self.all_results[0][0]:.2f}")
            print(f"  Key: {self.all_results[0][1]}")
            print(f"  Mode: {self.all_results[0][2]}")
            print(f"  Text: {self.all_results[0][3][:100]}...")
        
        return self.all_results[:100]
    
    def try_phi_prime_sequences(self, cipher: np.ndarray):
        """Try φ(prime) cipher with various starting positions."""
        cipher_len = len(cipher)
        
        for start_idx in range(min(500, len(PRIME_TOTIENTS_MOD_29) - cipher_len)):
            # Get φ(prime) sequence as key
            key_seq = np.array(PRIME_TOTIENTS_MOD_29[start_idx:start_idx + cipher_len], dtype=np.int32)
            
            # Decrypt: plaintext = cipher - key (mod 29)
            plaintext = (cipher - key_seq) % ALPHABET_SIZE
            
            score = score_detailed_cpu(plaintext)
            if score > 5:  # Only keep decent results
                text = indices_to_text(plaintext)
                with self.results_lock:
                    self.all_results.append((score, f"PHI_SEQ_START_{start_idx}", "PHI", text))
            
            # Also try ADD
            plaintext_add = (cipher + key_seq) % ALPHABET_SIZE
            score_add = score_detailed_cpu(plaintext_add)
            if score_add > 5:
                text = indices_to_text(plaintext_add)
                with self.results_lock:
                    self.all_results.append((score_add, f"PHI_SEQ_START_{start_idx}_ADD", "PHI_ADD", text))

# =============================================================================
# RUNNING KEY ATTACK WITH SELF-RELIANCE
# =============================================================================

def load_self_reliance() -> str:
    """Load Self-Reliance essay."""
    paths = [
        Path("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/Self-Reliance.txt"),
        Path("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/Self-Reliance.txt"),
    ]
    
    for path in paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    
    return ""

def text_to_indices(text: str) -> np.ndarray:
    """Convert text to Gematria indices."""
    indices = []
    text = text.upper()
    i = 0
    while i < len(text):
        found = False
        # Check for digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            for idx, lat in INDEX_TO_LATIN.items():
                if lat == digraph:
                    indices.append(idx)
                    i += 2
                    found = True
                    break
        
        if not found:
            c = text[i]
            for idx, lat in INDEX_TO_LATIN.items():
                if lat == c or (len(lat) == 1 and lat == c):
                    indices.append(idx)
                    break
            i += 1
    
    return np.array(indices, dtype=np.int32)

def running_key_attack(cipher: np.ndarray, key_text: str, verbose: bool = True) -> List[Tuple[float, str, str, str]]:
    """
    Try running key attack using a long text (like Self-Reliance).
    Tests all possible starting positions in the key text.
    """
    key_indices = text_to_indices(key_text)
    results = []
    
    cipher_len = len(cipher)
    max_starts = len(key_indices) - cipher_len
    
    if max_starts <= 0:
        return results
    
    if verbose:
        print(f"[RUNNING KEY] Testing {max_starts} starting positions...")
    
    # Test every starting position
    for start in range(0, max_starts, 10):  # Every 10th position for speed
        key_segment = key_indices[start:start + cipher_len]
        
        # SUB mode
        plaintext = (cipher - key_segment) % ALPHABET_SIZE
        score = score_detailed_cpu(plaintext)
        if score > 10:
            text = indices_to_text(plaintext)
            results.append((score, f"RUNNING_KEY_START_{start}", "RK_SUB", text))
        
        # ADD mode
        plaintext_add = (cipher + key_segment) % ALPHABET_SIZE
        score_add = score_detailed_cpu(plaintext_add)
        if score_add > 10:
            text = indices_to_text(plaintext_add)
            results.append((score_add, f"RUNNING_KEY_START_{start}_ADD", "RK_ADD", text))
    
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:50]

# =============================================================================
# BATCH PROCESSOR
# =============================================================================

# Pages to skip (non-text or already solved)
SKIP_PAGES = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,  # LP1 solved
              24, 30, 36, 44, 52,  # Image pages
              55, 56, 57, 73, 74]  # LP2 solved

UNSOLVED_PAGES = [2] + list(range(17, 55)) + list(range(58, 73))
UNSOLVED_PAGES = [p for p in UNSOLVED_PAGES if p not in SKIP_PAGES]

def batch_attack(pages: List[int] = None, output_path: str = "BATCH_RESULTS.md"):
    """Run batch attack on multiple pages."""
    if pages is None:
        pages = UNSOLVED_PAGES
    
    solver = DualGPUSolver(verbose=True)
    self_reliance = load_self_reliance()
    
    all_page_results = {}
    start_time = time.time()
    
    print("=" * 70)
    print("AGGRESSIVE DUAL-GPU BATCH ATTACK")
    print("=" * 70)
    print(f"Target Pages: {pages}")
    print(f"GPUs Available: {solver.num_gpus}")
    print("=" * 70)
    
    for i, page_num in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] ===== PAGE {page_num:02d} =====")
        
        page_start = time.time()
        
        try:
            # Main GPU attack
            results = solver.solve_page(page_num)
            
            # Running key attack if we have Self-Reliance
            if self_reliance:
                cipher = solver.load_cipher(page_num)
                rk_results = running_key_attack(cipher, self_reliance, verbose=True)
                results.extend(rk_results)
                results.sort(reverse=True, key=lambda x: x[0])
            
            all_page_results[page_num] = results[:20]  # Top 20 per page
            
            page_time = time.time() - page_start
            print(f"[TIME] Page {page_num}: {page_time:.2f}s")
            
        except Exception as e:
            print(f"[ERROR] Page {page_num}: {e}")
            all_page_results[page_num] = []
    
    total_time = time.time() - start_time
    
    # Save results
    save_results_markdown(all_page_results, output_path, total_time)
    save_results_json(all_page_results, output_path.replace('.md', '.json'), total_time)
    
    print("\n" + "=" * 70)
    print("BATCH ATTACK COMPLETE")
    print("=" * 70)
    print(f"Total Time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"Pages Processed: {len(all_page_results)}")
    print(f"Results saved to: {output_path}")
    print("=" * 70)
    
    return all_page_results

def save_results_markdown(results: Dict, output_path: str, total_time: float):
    """Save results to markdown."""
    lines = [
        "# AGGRESSIVE GPU BATCH ATTACK RESULTS",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Duration:** {total_time:.2f} seconds ({total_time/60:.2f} minutes)",
        f"**Pages Analyzed:** {len(results)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Page | Top Score | Key | Mode | Preview |",
        "|------|-----------|-----|------|---------|",
    ]
    
    for page_num in sorted(results.keys()):
        page_results = results[page_num]
        if page_results:
            top = page_results[0]
            preview = top[3][:40].replace('|', '\\|').replace('\n', ' ')
            lines.append(f"| {page_num:02d} | {top[0]:.1f} | `{top[1][:20]}` | {top[2]} | {preview}... |")
        else:
            lines.append(f"| {page_num:02d} | - | - | - | No results |")
    
    lines.extend(["", "---", "", "## Detailed Results", ""])
    
    for page_num in sorted(results.keys()):
        page_results = results[page_num]
        lines.append(f"### Page {page_num:02d}")
        lines.append("")
        
        if not page_results:
            lines.append("*No valid results found.*")
            lines.append("")
            continue
        
        lines.append("| Rank | Score | Key | Mode | Preview |")
        lines.append("|------|-------|-----|------|---------|")
        
        for i, (score, key, mode, text) in enumerate(page_results[:10], 1):
            preview = text[:50].replace('|', '\\|').replace('\n', ' ')
            lines.append(f"| {i} | {score:.1f} | `{key[:25]}` | {mode} | {preview}... |")
        
        lines.append("")
        
        # Best decryption
        if page_results:
            best = page_results[0]
            lines.extend([
                "**Best Decryption:**",
                "```",
                best[3][:500],
                "```",
                "",
            ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"[SAVED] {output_path}")

def save_results_json(results: Dict, output_path: str, total_time: float):
    """Save results to JSON."""
    output = {
        'metadata': {
            'date': datetime.now().isoformat(),
            'duration_seconds': total_time,
            'pages_analyzed': len(results),
        },
        'results': {
            str(page): [
                {'score': float(s), 'key': k, 'mode': m, 'text': t}
                for s, k, m, t in page_results
            ]
            for page, page_results in results.items()
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"[SAVED] {output_path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Aggressive dual-GPU batch attack on Liber Primus")
    parser.add_argument("--pages", type=str, default="all", 
                       help="Pages to attack: 'all', or comma-separated like '17,18,19'")
    parser.add_argument("--output", type=str, default="BATCH_RESULTS.md",
                       help="Output markdown file")
    
    args = parser.parse_args()
    
    os.chdir(Path(__file__).parent)
    
    if args.pages == "all":
        pages = UNSOLVED_PAGES
    else:
        pages = [int(p.strip()) for p in args.pages.split(',')]
    
    batch_attack(pages, args.output)

if __name__ == "__main__":
    main()

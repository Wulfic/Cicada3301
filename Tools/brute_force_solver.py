#!/usr/bin/env python3
"""
BRUTE FORCE SOLVER FOR CICADA 3301 / LIBER PRIMUS
==================================================

GPU-accelerated (CuPy) and parallel (multiprocessing) brute force tool.
Tries all feasible cipher combinations including offsets, directions, etc.

Features:
- GPU acceleration via CuPy (falls back to NumPy if no GPU)
- Parallel CPU processing via multiprocessing
- Multiple cipher types: Vigenère, Autokey, Running Key, Caesar, φ(prime)
- All offset variations (0-28)
- Forward/backward/reversed operations
- Multiple scoring methods: trigrams, quadgrams, word matching, IoC

Author: Wulfic
Date: January 2026
"""

import os
import sys
import time
import argparse
import json
from typing import List, Tuple, Dict, Optional, Callable, Any
from pathlib import Path
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
import multiprocessing as mp

# Try to import CuPy for GPU acceleration
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print("[INFO] CuPy detected - GPU acceleration ENABLED")
except ImportError:
    GPU_AVAILABLE = False
    print("[INFO] CuPy not found - using CPU with NumPy")

import numpy as np

# Import master dictionary
from master_dictionary import (
    ALPHABET_SIZE, RUNE_TO_INDEX, INDEX_TO_RUNE, INDEX_TO_LATIN,
    PRIMES, PRIME_TOTIENTS_MOD_29, PRIMES_MOD_29,
    FIBONACCI_MOD_29, LUCAS_MOD_29,
    ALL_KEYS, KNOWN_KEYS, CICADA_TERM_KEYS, SELF_RELIANCE_WORD_KEYS,
    TRIGRAMS, BIGRAMS, QUADGRAMS, COMMON_ENGLISH_WORDS,
    text_to_key, generate_prime_sequence_key, generate_fibonacci_key,
    generate_lucas_key, reverse_key, shift_key, invert_key,
    PRIME_KEY_LENGTHS, OFFSETS,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class Config:
    """Configuration for brute force solver."""
    # Processing
    use_gpu: bool = GPU_AVAILABLE
    num_workers: int = max(1, mp.cpu_count() - 1)
    batch_size: int = 10000  # Keys per batch for GPU
    
    # Key generation
    min_key_length: int = 1
    max_key_length: int = 100
    try_all_offsets: bool = True
    try_reversed: bool = True
    try_inverted: bool = True
    
    # Scoring
    min_score_threshold: float = 0.0
    top_results: int = 100
    
    # Output
    verbose: bool = True
    output_file: Optional[str] = None

# =============================================================================
# CIPHER IMPLEMENTATIONS
# =============================================================================

def vigenere_decrypt_np(cipher: np.ndarray, key: np.ndarray) -> np.ndarray:
    """Vigenère decrypt using NumPy: plaintext = (cipher - key) mod 29"""
    key_repeated = np.tile(key, (len(cipher) // len(key) + 1))[:len(cipher)]
    return (cipher - key_repeated) % ALPHABET_SIZE

def vigenere_encrypt_np(plaintext: np.ndarray, key: np.ndarray) -> np.ndarray:
    """Vigenère encrypt using NumPy: cipher = (plaintext + key) mod 29"""
    key_repeated = np.tile(key, (len(plaintext) // len(key) + 1))[:len(plaintext)]
    return (plaintext + key_repeated) % ALPHABET_SIZE

def autokey_decrypt_np(cipher: np.ndarray, key: np.ndarray) -> np.ndarray:
    """Autokey cipher decrypt: key is extended with plaintext."""
    plaintext = np.zeros(len(cipher), dtype=np.int32)
    full_key = list(key)
    
    for i in range(len(cipher)):
        k = full_key[i] if i < len(full_key) else plaintext[i - len(key)]
        plaintext[i] = (cipher[i] - k) % ALPHABET_SIZE
        if i >= len(key):
            pass  # Already used plaintext
        elif i + len(key) < len(cipher):
            full_key.append(plaintext[i])
    
    return plaintext

def running_key_decrypt_np(cipher: np.ndarray, running_text: np.ndarray) -> np.ndarray:
    """Running key cipher: key is as long as the message from source text."""
    key = running_text[:len(cipher)]
    return (cipher - key) % ALPHABET_SIZE

def caesar_decrypt_np(cipher: np.ndarray, shift: int) -> np.ndarray:
    """Caesar shift decrypt."""
    return (cipher - shift) % ALPHABET_SIZE

def phi_prime_decrypt_np(cipher: np.ndarray, start_idx: int = 0, 
                          literal_f_positions: List[int] = None) -> np.ndarray:
    """φ(prime) cipher decrypt: (cipher[i] - φ(prime[key_idx])) mod 29"""
    plaintext = np.zeros(len(cipher), dtype=np.int32)
    literal_f = set(literal_f_positions) if literal_f_positions else set()
    
    key_idx = 0
    for i in range(len(cipher)):
        if i in literal_f:
            plaintext[i] = 0  # F = index 0
        else:
            phi_val = PRIME_TOTIENTS_MOD_29[start_idx + key_idx]
            plaintext[i] = (cipher[i] - phi_val) % ALPHABET_SIZE
            key_idx += 1
    
    return plaintext

# =============================================================================
# GPU IMPLEMENTATIONS (CuPy)
# =============================================================================

if GPU_AVAILABLE:
    def vigenere_decrypt_batch_gpu(cipher: cp.ndarray, keys: List[cp.ndarray]) -> List[cp.ndarray]:
        """Batch Vigenère decrypt on GPU."""
        results = []
        for key in keys:
            key_repeated = cp.tile(key, (len(cipher) // len(key) + 1))[:len(cipher)]
            plaintext = (cipher - key_repeated) % ALPHABET_SIZE
            results.append(plaintext)
        return results
    
    def score_batch_gpu(plaintexts: List[cp.ndarray], trigram_scores: cp.ndarray) -> cp.ndarray:
        """Batch scoring on GPU using trigram lookup."""
        scores = cp.zeros(len(plaintexts), dtype=cp.float32)
        for i, pt in enumerate(plaintexts):
            # Convert to host for scoring (trigrams are complex)
            pt_host = cp.asnumpy(pt)
            scores[i] = score_text_trigrams(pt_host)
        return scores

# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

def indices_to_text(indices: np.ndarray) -> str:
    """Convert array of indices to Latin text."""
    return ''.join(INDEX_TO_LATIN.get(int(i), '?') for i in indices)

def score_text_trigrams(indices: np.ndarray) -> float:
    """Score text using trigram frequency matching."""
    text = indices_to_text(indices)
    if len(text) < 3:
        return 0.0
    
    score = 0.0
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in TRIGRAMS:
            score += TRIGRAMS[trigram]
    
    # Normalize by length
    return score / max(1, len(text) - 2)

def score_text_quadgrams(indices: np.ndarray) -> float:
    """Score text using quadgram frequency matching."""
    text = indices_to_text(indices)
    if len(text) < 4:
        return 0.0
    
    score = 0.0
    for i in range(len(text) - 3):
        quadgram = text[i:i+4]
        if quadgram in QUADGRAMS:
            score += QUADGRAMS[quadgram]
    
    return score / max(1, len(text) - 3)

def score_text_words(indices: np.ndarray, min_word_len: int = 3) -> float:
    """Score text by counting known English words found."""
    text = indices_to_text(indices)
    score = 0.0
    
    # Check for common words
    for word in COMMON_ENGLISH_WORDS:
        if len(word) >= min_word_len and word in text:
            score += len(word) * 2  # Longer words score more
    
    return score / max(1, len(text))

def score_index_of_coincidence(indices: np.ndarray) -> float:
    """Calculate Index of Coincidence."""
    n = len(indices)
    if n < 2:
        return 0.0
    
    freq = np.bincount(indices, minlength=ALPHABET_SIZE)
    ioc = np.sum(freq * (freq - 1)) / (n * (n - 1))
    return ioc

def score_combined(indices: np.ndarray, weights: Tuple[float, float, float, float] = (1.0, 1.0, 0.5, 0.3)) -> float:
    """Combined scoring using multiple methods."""
    tri_score = score_text_trigrams(indices) * weights[0]
    quad_score = score_text_quadgrams(indices) * weights[1]
    word_score = score_text_words(indices) * weights[2]
    ioc_score = (score_index_of_coincidence(indices) - 0.0345) * 100 * weights[3]  # Boost above random
    
    return tri_score + quad_score + word_score + max(0, ioc_score)

# =============================================================================
# KEY GENERATOR
# =============================================================================

def generate_all_keys(config: Config) -> List[Tuple[str, np.ndarray]]:
    """Generate all keys to try."""
    keys = []
    
    # 1. Known keys from dictionary
    for name, key in ALL_KEYS.items():
        if key and config.min_key_length <= len(key) <= config.max_key_length:
            keys.append((f"DICT:{name}", np.array(key, dtype=np.int32)))
    
    # 2. Prime sequence keys
    for length in PRIME_KEY_LENGTHS:
        if config.min_key_length <= length <= config.max_key_length:
            for start_idx in range(min(50, len(PRIMES) - length)):
                key = np.array([PRIMES_MOD_29[start_idx + i] for i in range(length)], dtype=np.int32)
                keys.append((f"PRIME_SEQ:len{length}_start{start_idx}", key))
    
    # 3. φ(prime) sequence keys
    for length in PRIME_KEY_LENGTHS:
        if config.min_key_length <= length <= config.max_key_length:
            for start_idx in range(min(50, len(PRIME_TOTIENTS_MOD_29) - length)):
                key = np.array([PRIME_TOTIENTS_MOD_29[start_idx + i] for i in range(length)], dtype=np.int32)
                keys.append((f"PHI_PRIME:len{length}_start{start_idx}", key))
    
    # 4. Fibonacci keys
    for length in range(config.min_key_length, min(50, config.max_key_length)):
        for start_idx in range(min(20, len(FIBONACCI_MOD_29) - length)):
            key = np.array([FIBONACCI_MOD_29[start_idx + i] for i in range(length)], dtype=np.int32)
            keys.append((f"FIB:len{length}_start{start_idx}", key))
    
    # 5. Lucas keys
    for length in range(config.min_key_length, min(50, config.max_key_length)):
        for start_idx in range(min(20, len(LUCAS_MOD_29) - length)):
            key = np.array([LUCAS_MOD_29[start_idx + i] for i in range(length)], dtype=np.int32)
            keys.append((f"LUCAS:len{length}_start{start_idx}", key))
    
    # 6. Add offset variations if requested
    if config.try_all_offsets:
        base_keys = keys.copy()
        for name, key in base_keys:
            if not name.startswith("DICT:"):  # Don't add offsets to dict words (too many)
                continue
            for offset in range(1, ALPHABET_SIZE):  # Skip 0 (already included)
                shifted_key = (key + offset) % ALPHABET_SIZE
                keys.append((f"{name}+offset{offset}", shifted_key))
    
    # 7. Add reversed keys if requested
    if config.try_reversed:
        base_keys = keys.copy()
        for name, key in base_keys:
            if "REV" not in name:  # Avoid double-reversing
                keys.append((f"{name}_REV", key[::-1].copy()))
    
    # 8. Add inverted keys if requested
    if config.try_inverted:
        base_keys = keys.copy()
        for name, key in base_keys:
            if "INV" not in name:
                inverted = (ALPHABET_SIZE - key) % ALPHABET_SIZE
                keys.append((f"{name}_INV", inverted))
    
    return keys

# =============================================================================
# CIPHER MODES TO TRY
# =============================================================================

CIPHER_MODES = [
    ("SUB", lambda c, k: (c - k) % ALPHABET_SIZE),      # Vigenère subtract
    ("ADD", lambda c, k: (c + k) % ALPHABET_SIZE),      # Vigenère add
    ("SUB_REV", lambda c, k: (k - c) % ALPHABET_SIZE),  # Reverse subtract
]

# =============================================================================
# PARALLEL WORKER FUNCTION
# =============================================================================

def worker_try_key(args: Tuple[str, np.ndarray, np.ndarray, str]) -> Tuple[str, str, float, str]:
    """Worker function to try a single key with a cipher mode."""
    key_name, key, cipher, mode_name = args
    
    # Apply cipher mode
    if mode_name == "SUB":
        key_repeated = np.tile(key, (len(cipher) // len(key) + 1))[:len(cipher)]
        plaintext = (cipher - key_repeated) % ALPHABET_SIZE
    elif mode_name == "ADD":
        key_repeated = np.tile(key, (len(cipher) // len(key) + 1))[:len(cipher)]
        plaintext = (cipher + key_repeated) % ALPHABET_SIZE
    elif mode_name == "SUB_REV":
        key_repeated = np.tile(key, (len(cipher) // len(key) + 1))[:len(cipher)]
        plaintext = (key_repeated - cipher) % ALPHABET_SIZE
    else:
        return (key_name, mode_name, 0.0, "")
    
    # Score the result
    score = score_combined(plaintext)
    text = indices_to_text(plaintext)
    
    return (key_name, mode_name, score, text)

def worker_try_caesar(args: Tuple[int, np.ndarray]) -> Tuple[int, float, str]:
    """Worker for Caesar shift."""
    shift, cipher = args
    plaintext = (cipher - shift) % ALPHABET_SIZE
    score = score_combined(plaintext)
    text = indices_to_text(plaintext)
    return (shift, score, text)

def worker_try_autokey(args: Tuple[str, np.ndarray, np.ndarray]) -> Tuple[str, float, str]:
    """Worker for autokey cipher."""
    key_name, key, cipher = args
    plaintext = autokey_decrypt_np(cipher, key)
    score = score_combined(plaintext)
    text = indices_to_text(plaintext)
    return (key_name, score, text)

# =============================================================================
# MAIN SOLVER CLASS
# =============================================================================

class BruteForceSolver:
    """Main brute force solver class."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.results: List[Tuple[float, str, str, str]] = []  # (score, key_name, mode, text)
        
    def load_cipher(self, page_num: int) -> np.ndarray:
        """Load cipher text from a page."""
        rune_path = Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt")
        
        if not rune_path.exists():
            raise FileNotFoundError(f"Rune file not found: {rune_path}")
        
        with open(rune_path, 'r', encoding='utf-8') as f:
            runes = f.read()
        
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def load_cipher_from_file(self, filepath: str) -> np.ndarray:
        """Load cipher from a file path."""
        with open(filepath, 'r', encoding='utf-8') as f:
            runes = f.read()
        
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def solve_vigenere_parallel(self, cipher: np.ndarray, keys: List[Tuple[str, np.ndarray]]) -> List[Tuple[float, str, str, str]]:
        """Solve using parallel Vigenère attack."""
        results = []
        
        # Prepare all tasks
        tasks = []
        for key_name, key in keys:
            for mode_name, _ in CIPHER_MODES:
                tasks.append((key_name, key, cipher, mode_name))
        
        if self.config.verbose:
            print(f"[INFO] Running {len(tasks)} Vigenère combinations with {self.config.num_workers} workers...")
        
        # Run in parallel
        with ProcessPoolExecutor(max_workers=self.config.num_workers) as executor:
            futures = [executor.submit(worker_try_key, task) for task in tasks]
            
            for i, future in enumerate(as_completed(futures)):
                try:
                    key_name, mode_name, score, text = future.result()
                    if score >= self.config.min_score_threshold:
                        results.append((score, key_name, mode_name, text))
                except Exception as e:
                    if self.config.verbose:
                        print(f"[ERROR] Task failed: {e}")
                
                # Progress update
                if self.config.verbose and (i + 1) % 10000 == 0:
                    print(f"[PROGRESS] {i + 1}/{len(tasks)} completed...")
        
        # Sort by score descending
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:self.config.top_results]
    
    def solve_caesar_parallel(self, cipher: np.ndarray) -> List[Tuple[float, str, str, str]]:
        """Try all Caesar shifts."""
        results = []
        
        tasks = [(shift, cipher) for shift in range(ALPHABET_SIZE)]
        
        with ProcessPoolExecutor(max_workers=self.config.num_workers) as executor:
            futures = [executor.submit(worker_try_caesar, task) for task in tasks]
            
            for future in as_completed(futures):
                shift, score, text = future.result()
                results.append((score, f"CAESAR_SHIFT_{shift}", "SUB", text))
        
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:self.config.top_results]
    
    def solve_autokey_parallel(self, cipher: np.ndarray, keys: List[Tuple[str, np.ndarray]]) -> List[Tuple[float, str, str, str]]:
        """Try autokey cipher with various seed keys."""
        results = []
        
        # Only use shorter keys for autokey (seed)
        short_keys = [(n, k) for n, k in keys if len(k) <= 20]
        tasks = [(key_name, key, cipher) for key_name, key in short_keys]
        
        if self.config.verbose:
            print(f"[INFO] Running {len(tasks)} autokey combinations...")
        
        with ProcessPoolExecutor(max_workers=self.config.num_workers) as executor:
            futures = [executor.submit(worker_try_autokey, task) for task in tasks]
            
            for future in as_completed(futures):
                key_name, score, text = future.result()
                results.append((score, key_name, "AUTOKEY", text))
        
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:self.config.top_results]
    
    def solve_phi_prime(self, cipher: np.ndarray, max_start_idx: int = 100) -> List[Tuple[float, str, str, str]]:
        """Try φ(prime) sequences with various starting indices."""
        results = []
        
        for start_idx in range(max_start_idx):
            # Try without literal F handling
            plaintext = phi_prime_decrypt_np(cipher, start_idx)
            score = score_combined(plaintext)
            text = indices_to_text(plaintext)
            results.append((score, f"PHI_PRIME_START_{start_idx}", "PHI", text))
            
            # Try with each position as potential literal F
            for f_pos in range(min(len(cipher), 100)):
                plaintext = phi_prime_decrypt_np(cipher, start_idx, [f_pos])
                score = score_combined(plaintext)
                if score > self.config.min_score_threshold:
                    text = indices_to_text(plaintext)
                    results.append((score, f"PHI_PRIME_START_{start_idx}_LITF_{f_pos}", "PHI_LITF", text))
        
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:self.config.top_results]
    
    def solve_gpu_batch(self, cipher: np.ndarray, keys: List[Tuple[str, np.ndarray]]) -> List[Tuple[float, str, str, str]]:
        """GPU-accelerated batch solving."""
        if not GPU_AVAILABLE:
            print("[WARNING] GPU not available, falling back to CPU")
            return self.solve_vigenere_parallel(cipher, keys)
        
        results = []
        cipher_gpu = cp.array(cipher, dtype=cp.int32)
        
        batch_size = self.config.batch_size
        total_batches = (len(keys) + batch_size - 1) // batch_size
        
        if self.config.verbose:
            print(f"[INFO] Running GPU batch processing: {len(keys)} keys in {total_batches} batches...")
        
        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            end = min(start + batch_size, len(keys))
            batch_keys = keys[start:end]
            
            for key_name, key in batch_keys:
                key_gpu = cp.array(key, dtype=cp.int32)
                
                for mode_name, _ in CIPHER_MODES:
                    key_repeated = cp.tile(key_gpu, (len(cipher_gpu) // len(key_gpu) + 1))[:len(cipher_gpu)]
                    
                    if mode_name == "SUB":
                        plaintext_gpu = (cipher_gpu - key_repeated) % ALPHABET_SIZE
                    elif mode_name == "ADD":
                        plaintext_gpu = (cipher_gpu + key_repeated) % ALPHABET_SIZE
                    else:
                        plaintext_gpu = (key_repeated - cipher_gpu) % ALPHABET_SIZE
                    
                    # Move to CPU for scoring
                    plaintext = cp.asnumpy(plaintext_gpu)
                    score = score_combined(plaintext)
                    
                    if score >= self.config.min_score_threshold:
                        text = indices_to_text(plaintext)
                        results.append((score, key_name, mode_name, text))
            
            if self.config.verbose and (batch_idx + 1) % 10 == 0:
                print(f"[PROGRESS] Batch {batch_idx + 1}/{total_batches} completed...")
        
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:self.config.top_results]
    
    def solve_all(self, cipher: np.ndarray) -> Dict[str, List[Tuple[float, str, str, str]]]:
        """Run all solving methods and combine results."""
        all_results = {}
        
        # Generate keys
        if self.config.verbose:
            print("[INFO] Generating key combinations...")
        keys = generate_all_keys(self.config)
        if self.config.verbose:
            print(f"[INFO] Generated {len(keys)} key combinations")
        
        # 1. Caesar shifts (quick)
        if self.config.verbose:
            print("\n[PHASE 1] Caesar shifts...")
        all_results['caesar'] = self.solve_caesar_parallel(cipher)
        
        # 2. Vigenère with all keys
        if self.config.verbose:
            print("\n[PHASE 2] Vigenère cipher...")
        if self.config.use_gpu and GPU_AVAILABLE:
            all_results['vigenere'] = self.solve_gpu_batch(cipher, keys)
        else:
            all_results['vigenere'] = self.solve_vigenere_parallel(cipher, keys)
        
        # 3. Autokey cipher
        if self.config.verbose:
            print("\n[PHASE 3] Autokey cipher...")
        all_results['autokey'] = self.solve_autokey_parallel(cipher, keys)
        
        # 4. φ(prime) sequences
        if self.config.verbose:
            print("\n[PHASE 4] φ(prime) sequences...")
        all_results['phi_prime'] = self.solve_phi_prime(cipher)
        
        return all_results
    
    def print_results(self, results: Dict[str, List[Tuple[float, str, str, str]]], top_n: int = 10):
        """Print top results from each method."""
        print("\n" + "=" * 80)
        print("BRUTE FORCE RESULTS")
        print("=" * 80)
        
        for method, method_results in results.items():
            print(f"\n{'=' * 40}")
            print(f"METHOD: {method.upper()}")
            print(f"{'=' * 40}")
            
            for i, (score, key_name, mode, text) in enumerate(method_results[:top_n]):
                print(f"\n[{i+1}] Score: {score:.2f}")
                print(f"    Key: {key_name}")
                print(f"    Mode: {mode}")
                print(f"    Text: {text[:100]}..." if len(text) > 100 else f"    Text: {text}")
    
    def save_results(self, results: Dict[str, List[Tuple[float, str, str, str]]], filepath: str):
        """Save results to JSON file."""
        output = {}
        for method, method_results in results.items():
            output[method] = [
                {"score": score, "key": key_name, "mode": mode, "text": text}
                for score, key_name, mode, text in method_results
            ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        
        print(f"[INFO] Results saved to {filepath}")

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Brute force solver for Liber Primus")
    parser.add_argument("--page", type=int, help="Page number to solve (e.g., 17)")
    parser.add_argument("--file", type=str, help="Path to rune file to solve")
    parser.add_argument("--workers", type=int, default=mp.cpu_count() - 1, help="Number of parallel workers")
    parser.add_argument("--no-gpu", action="store_true", help="Disable GPU acceleration")
    parser.add_argument("--top", type=int, default=20, help="Number of top results per method")
    parser.add_argument("--output", type=str, help="Output JSON file path")
    parser.add_argument("--min-key-len", type=int, default=1, help="Minimum key length")
    parser.add_argument("--max-key-len", type=int, default=100, help="Maximum key length")
    parser.add_argument("--quick", action="store_true", help="Quick mode: fewer key variations")
    
    args = parser.parse_args()
    
    # Configure
    config = Config(
        use_gpu=not args.no_gpu and GPU_AVAILABLE,
        num_workers=args.workers,
        top_results=args.top,
        min_key_length=args.min_key_len,
        max_key_length=args.max_key_len,
        try_all_offsets=not args.quick,
        try_reversed=not args.quick,
        try_inverted=not args.quick,
        output_file=args.output,
    )
    
    print("=" * 60)
    print("LIBER PRIMUS BRUTE FORCE SOLVER")
    print("=" * 60)
    print(f"GPU Acceleration: {'ENABLED' if config.use_gpu else 'DISABLED'}")
    print(f"Parallel Workers: {config.num_workers}")
    print(f"Key Length Range: {config.min_key_length} - {config.max_key_length}")
    print(f"Quick Mode: {args.quick}")
    print("=" * 60)
    
    # Initialize solver
    solver = BruteForceSolver(config)
    
    # Load cipher
    try:
        if args.page:
            print(f"\n[INFO] Loading page {args.page}...")
            cipher = solver.load_cipher(args.page)
        elif args.file:
            print(f"\n[INFO] Loading file {args.file}...")
            cipher = solver.load_cipher_from_file(args.file)
        else:
            # Default to page 17 (first unsolved page in bulk)
            print("\n[INFO] No page specified, using page 17 as default...")
            cipher = solver.load_cipher(17)
        
        print(f"[INFO] Loaded cipher with {len(cipher)} runes")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    
    # Run solver
    start_time = time.time()
    results = solver.solve_all(cipher)
    elapsed = time.time() - start_time
    
    print(f"\n[INFO] Completed in {elapsed:.2f} seconds")
    
    # Print and save results
    solver.print_results(results, top_n=args.top)
    
    if args.output:
        solver.save_results(results, args.output)

if __name__ == "__main__":
    main()

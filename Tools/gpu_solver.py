#!/usr/bin/env python3
"""
GPU ACCELERATED SOLVER - Using Numba CUDA Kernels
==================================================

This module provides true GPU parallelization using Numba CUDA kernels.
Falls back to CPU with Numba JIT if no GPU is available.

Author: Wulfic
Date: January 2026
"""

import os
import sys
import time
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

# Try to import Numba for JIT/CUDA
try:
    from numba import jit, prange, cuda
    NUMBA_AVAILABLE = True
    try:
        cuda.detect()
        CUDA_AVAILABLE = True
        print("[INFO] Numba CUDA detected - GPU kernels ENABLED")
    except:
        CUDA_AVAILABLE = False
        print("[INFO] Numba available but no CUDA GPU - using CPU JIT")
except ImportError:
    NUMBA_AVAILABLE = False
    CUDA_AVAILABLE = False
    print("[INFO] Numba not found - using pure Python (slower)")

from master_dictionary import (
    ALPHABET_SIZE, RUNE_TO_INDEX, INDEX_TO_LATIN,
    PRIMES_MOD_29, PRIME_TOTIENTS_MOD_29,
    ALL_KEYS, text_to_key
)

# =============================================================================
# SCORING CONSTANTS (as numpy arrays for GPU)
# =============================================================================

# Create trigram lookup table
# We'll use a flat array indexed by (a*29*29 + b*29 + c)
TRIGRAM_WEIGHTS = {
    'THE': 100, 'AND': 80, 'ING': 75, 'HER': 60, 'THA': 60, 'ERE': 50,
    'FOR': 50, 'ENT': 45, 'ION': 45, 'TER': 40, 'WAS': 40, 'YOU': 40,
    'ITH': 35, 'VER': 35, 'ALL': 35, 'WIT': 35, 'THI': 35, 'TIO': 35,
}

# Letter to index for scoring (simplified single-char only)
LETTER_TO_IDX = {
    'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'D': 23,
    'A': 24, 'Y': 26
}

def create_trigram_table() -> np.ndarray:
    """Create a lookup table for trigram scoring."""
    table = np.zeros(29 * 29 * 29, dtype=np.float32)
    
    for trigram, weight in TRIGRAM_WEIGHTS.items():
        if len(trigram) != 3:
            continue
        # Map trigram to indices (simplified)
        try:
            a = LETTER_TO_IDX.get(trigram[0], -1)
            b = LETTER_TO_IDX.get(trigram[1], -1)
            c = LETTER_TO_IDX.get(trigram[2], -1)
            if a >= 0 and b >= 0 and c >= 0:
                idx = a * 29 * 29 + b * 29 + c
                table[idx] = weight
        except:
            pass
    
    return table

TRIGRAM_TABLE = create_trigram_table()

# =============================================================================
# CPU JIT FUNCTIONS (Numba accelerated)
# =============================================================================

if NUMBA_AVAILABLE:
    @jit(nopython=True, parallel=True, cache=True)
    def vigenere_decrypt_batch_jit(cipher: np.ndarray, keys: np.ndarray, 
                                    key_lengths: np.ndarray) -> np.ndarray:
        """
        Batch Vigenère decrypt with JIT compilation.
        
        cipher: 1D array of cipher indices
        keys: 2D array [num_keys, max_key_len] of key values (padded)
        key_lengths: 1D array of actual key lengths
        
        Returns: 2D array [num_keys, len(cipher)] of plaintexts
        """
        num_keys = len(key_lengths)
        cipher_len = len(cipher)
        results = np.empty((num_keys, cipher_len), dtype=np.int32)
        
        for k in prange(num_keys):
            key_len = key_lengths[k]
            for i in range(cipher_len):
                key_val = keys[k, i % key_len]
                results[k, i] = (cipher[i] - key_val) % 29
        
        return results
    
    @jit(nopython=True, parallel=True, cache=True)
    def score_plaintexts_jit(plaintexts: np.ndarray, 
                             trigram_table: np.ndarray) -> np.ndarray:
        """
        Score multiple plaintexts using trigram lookup.
        
        plaintexts: 2D array [num_texts, text_len]
        trigram_table: 1D array of trigram weights
        
        Returns: 1D array of scores
        """
        num_texts, text_len = plaintexts.shape
        scores = np.zeros(num_texts, dtype=np.float32)
        
        for t in prange(num_texts):
            score = 0.0
            for i in range(text_len - 2):
                a = plaintexts[t, i]
                b = plaintexts[t, i + 1]
                c = plaintexts[t, i + 2]
                idx = a * 29 * 29 + b * 29 + c
                if 0 <= idx < len(trigram_table):
                    score += trigram_table[idx]
            scores[t] = score / max(1, text_len - 2)
        
        return scores
    
    @jit(nopython=True, cache=True)
    def autokey_decrypt_jit(cipher: np.ndarray, seed: np.ndarray) -> np.ndarray:
        """Autokey cipher decrypt with JIT."""
        cipher_len = len(cipher)
        seed_len = len(seed)
        plaintext = np.empty(cipher_len, dtype=np.int32)
        
        for i in range(cipher_len):
            if i < seed_len:
                key_val = seed[i]
            else:
                key_val = plaintext[i - seed_len]
            plaintext[i] = (cipher[i] - key_val) % 29
        
        return plaintext
    
    @jit(nopython=True, parallel=True, cache=True)
    def caesar_all_shifts_jit(cipher: np.ndarray) -> np.ndarray:
        """Try all 29 Caesar shifts."""
        cipher_len = len(cipher)
        results = np.empty((29, cipher_len), dtype=np.int32)
        
        for shift in prange(29):
            for i in range(cipher_len):
                results[shift, i] = (cipher[i] - shift) % 29
        
        return results

# =============================================================================
# CUDA KERNELS (if available)
# =============================================================================

if CUDA_AVAILABLE:
    @cuda.jit
    def vigenere_decrypt_kernel(cipher, keys, key_lengths, results):
        """
        CUDA kernel for Vigenère decrypt.
        
        Each thread handles one (key, position) pair.
        """
        # Thread ID
        key_idx, pos = cuda.grid(2)
        
        if key_idx < keys.shape[0] and pos < cipher.shape[0]:
            key_len = key_lengths[key_idx]
            key_val = keys[key_idx, pos % key_len]
            results[key_idx, pos] = (cipher[pos] - key_val) % 29
    
    @cuda.jit
    def score_trigrams_kernel(plaintexts, trigram_table, scores):
        """
        CUDA kernel for trigram scoring.
        
        Each thread handles one plaintext.
        """
        text_idx = cuda.grid(1)
        
        if text_idx < plaintexts.shape[0]:
            score = 0.0
            text_len = plaintexts.shape[1]
            
            for i in range(text_len - 2):
                a = plaintexts[text_idx, i]
                b = plaintexts[text_idx, i + 1]
                c = plaintexts[text_idx, i + 2]
                idx = a * 29 * 29 + b * 29 + c
                if 0 <= idx < trigram_table.shape[0]:
                    score += trigram_table[idx]
            
            scores[text_idx] = score / max(1, text_len - 2)
    
    @cuda.jit
    def caesar_kernel(cipher, results):
        """CUDA kernel for Caesar shifts. Each block handles one shift."""
        shift, pos = cuda.grid(2)
        
        if shift < 29 and pos < cipher.shape[0]:
            results[shift, pos] = (cipher[pos] - shift) % 29

# =============================================================================
# GPU SOLVER CLASS
# =============================================================================

class GPUSolver:
    """GPU-accelerated solver using Numba CUDA or JIT."""
    
    def __init__(self, use_gpu: bool = True):
        self.use_gpu = use_gpu and CUDA_AVAILABLE
        self.use_jit = NUMBA_AVAILABLE
        
    def load_cipher(self, page_num: int) -> np.ndarray:
        """Load cipher from page."""
        rune_path = Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt")
        with open(rune_path, 'r', encoding='utf-8') as f:
            runes = f.read()
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def prepare_keys(self, keys_dict: Dict[str, List[int]], 
                      max_key_len: int = 100) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare keys for batch processing."""
        key_names = []
        keys_list = []
        key_lengths = []
        
        for name, key in keys_dict.items():
            if key and len(key) <= max_key_len:
                key_names.append(name)
                # Pad key to max length
                padded = np.zeros(max_key_len, dtype=np.int32)
                padded[:len(key)] = key
                keys_list.append(padded)
                key_lengths.append(len(key))
        
        keys_array = np.array(keys_list, dtype=np.int32)
        lengths_array = np.array(key_lengths, dtype=np.int32)
        
        return keys_array, lengths_array, key_names
    
    def solve_vigenere_gpu(self, cipher: np.ndarray, 
                            keys: np.ndarray, 
                            key_lengths: np.ndarray,
                            key_names: List[str]) -> List[Tuple[float, str, str]]:
        """Solve using GPU Vigenère."""
        num_keys = len(key_lengths)
        cipher_len = len(cipher)
        
        print(f"[GPU] Processing {num_keys} keys on GPU...")
        
        # Allocate device memory
        d_cipher = cuda.to_device(cipher)
        d_keys = cuda.to_device(keys)
        d_key_lengths = cuda.to_device(key_lengths)
        d_results = cuda.device_array((num_keys, cipher_len), dtype=np.int32)
        
        # Configure kernel
        threads_per_block = (16, 64)
        blocks_x = (num_keys + threads_per_block[0] - 1) // threads_per_block[0]
        blocks_y = (cipher_len + threads_per_block[1] - 1) // threads_per_block[1]
        blocks = (blocks_x, blocks_y)
        
        # Launch decryption kernel
        vigenere_decrypt_kernel[blocks, threads_per_block](
            d_cipher, d_keys, d_key_lengths, d_results
        )
        
        # Score results
        d_trigrams = cuda.to_device(TRIGRAM_TABLE)
        d_scores = cuda.device_array(num_keys, dtype=np.float32)
        
        threads = 256
        blocks_score = (num_keys + threads - 1) // threads
        score_trigrams_kernel[blocks_score, threads](d_results, d_trigrams, d_scores)
        
        # Copy results back
        results = d_results.copy_to_host()
        scores = d_scores.copy_to_host()
        
        # Format results
        output = []
        for i in range(num_keys):
            text = ''.join(INDEX_TO_LATIN.get(int(idx), '?') for idx in results[i])
            output.append((float(scores[i]), key_names[i], text))
        
        # Sort by score
        output.sort(reverse=True, key=lambda x: x[0])
        return output
    
    def solve_vigenere_jit(self, cipher: np.ndarray,
                            keys: np.ndarray,
                            key_lengths: np.ndarray,
                            key_names: List[str]) -> List[Tuple[float, str, str]]:
        """Solve using JIT-compiled CPU code."""
        print(f"[JIT] Processing {len(key_lengths)} keys with parallel JIT...")
        
        # Decrypt all
        results = vigenere_decrypt_batch_jit(cipher, keys, key_lengths)
        
        # Score all
        scores = score_plaintexts_jit(results, TRIGRAM_TABLE)
        
        # Format output
        output = []
        for i in range(len(key_names)):
            text = ''.join(INDEX_TO_LATIN.get(int(idx), '?') for idx in results[i])
            output.append((float(scores[i]), key_names[i], text))
        
        output.sort(reverse=True, key=lambda x: x[0])
        return output
    
    def solve_caesar_gpu(self, cipher: np.ndarray) -> List[Tuple[float, int, str]]:
        """Try all Caesar shifts on GPU."""
        cipher_len = len(cipher)
        
        if self.use_gpu:
            d_cipher = cuda.to_device(cipher)
            d_results = cuda.device_array((29, cipher_len), dtype=np.int32)
            
            threads = (1, 256)
            blocks = (29, (cipher_len + 255) // 256)
            caesar_kernel[blocks, threads](d_cipher, d_results)
            
            results = d_results.copy_to_host()
        elif self.use_jit:
            results = caesar_all_shifts_jit(cipher)
        else:
            results = np.array([[(c - s) % 29 for c in cipher] for s in range(29)])
        
        # Score and format
        output = []
        for shift in range(29):
            text = ''.join(INDEX_TO_LATIN.get(int(idx), '?') for idx in results[shift])
            score = float(np.sum([TRIGRAM_TABLE[results[shift, i] * 841 + results[shift, i+1] * 29 + results[shift, i+2]] 
                                   for i in range(cipher_len - 2)]))
            output.append((score / cipher_len, shift, text))
        
        output.sort(reverse=True, key=lambda x: x[0])
        return output
    
    def solve(self, cipher: np.ndarray, max_key_len: int = 50) -> Dict[str, List]:
        """Run full solve."""
        results = {}
        
        # Prepare keys
        print("[INFO] Preparing keys...")
        keys, lengths, names = self.prepare_keys(ALL_KEYS, max_key_len)
        print(f"[INFO] Prepared {len(names)} keys")
        
        # Caesar
        print("\n[PHASE 1] Caesar shifts...")
        start = time.time()
        results['caesar'] = self.solve_caesar_gpu(cipher)
        print(f"[INFO] Caesar completed in {time.time() - start:.2f}s")
        
        # Vigenère
        print("\n[PHASE 2] Vigenère cipher...")
        start = time.time()
        if self.use_gpu:
            results['vigenere'] = self.solve_vigenere_gpu(cipher, keys, lengths, names)
        elif self.use_jit:
            results['vigenere'] = self.solve_vigenere_jit(cipher, keys, lengths, names)
        else:
            print("[WARNING] No acceleration available, this will be slow...")
            results['vigenere'] = []
        print(f"[INFO] Vigenère completed in {time.time() - start:.2f}s")
        
        return results
    
    def print_results(self, results: Dict, top_n: int = 10):
        """Print top results."""
        print("\n" + "=" * 80)
        print("GPU SOLVER RESULTS")
        print("=" * 80)
        
        for method, data in results.items():
            print(f"\n{'=' * 40}")
            print(f"METHOD: {method.upper()}")
            print(f"{'=' * 40}")
            
            for i, item in enumerate(data[:top_n]):
                if method == 'caesar':
                    score, shift, text = item
                    print(f"\n[{i+1}] Score: {score:.2f}, Shift: {shift}")
                else:
                    score, key_name, text = item
                    print(f"\n[{i+1}] Score: {score:.2f}, Key: {key_name}")
                print(f"    Text: {text[:100]}..." if len(text) > 100 else f"    Text: {text}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="GPU-accelerated solver")
    parser.add_argument("--page", type=int, default=17, help="Page number")
    parser.add_argument("--no-gpu", action="store_true", help="Disable GPU")
    parser.add_argument("--top", type=int, default=20, help="Top results")
    parser.add_argument("--max-key-len", type=int, default=50, help="Max key length")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("GPU ACCELERATED SOLVER")
    print("=" * 60)
    print(f"CUDA Available: {CUDA_AVAILABLE}")
    print(f"Numba JIT Available: {NUMBA_AVAILABLE}")
    print("=" * 60)
    
    solver = GPUSolver(use_gpu=not args.no_gpu)
    
    print(f"\n[INFO] Loading page {args.page}...")
    cipher = solver.load_cipher(args.page)
    print(f"[INFO] Loaded {len(cipher)} runes")
    
    start = time.time()
    results = solver.solve(cipher, args.max_key_len)
    elapsed = time.time() - start
    
    print(f"\n[INFO] Total time: {elapsed:.2f}s")
    solver.print_results(results, args.top)

if __name__ == "__main__":
    main()

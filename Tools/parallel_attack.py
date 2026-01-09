#!/usr/bin/env python3
"""
AGGRESSIVE PARALLEL CPU BATCH ATTACK FOR LIBER PRIMUS
======================================================

Maximizes CPU utilization with aggressive parallel key testing.
Uses all CPU cores for maximum throughput.

Features:
- Aggressive parallel processing (all cores)
- Massive key generation (millions of combinations)
- Running key attacks with Self-Reliance
- All cipher variants tested
- Smart scoring with English detection

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
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

import numpy as np

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
    return ''.join(INDEX_TO_LATIN.get(int(i), '?') for i in indices)

# =============================================================================
# PRIME NUMBER SEQUENCES
# =============================================================================

def sieve_of_eratosthenes(limit: int) -> List[int]:
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(limit + 1) if sieve[i]]

PRIMES = sieve_of_eratosthenes(50000)
PRIMES_MOD_29 = [p % 29 for p in PRIMES]

def euler_totient(n: int) -> int:
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
# ENGLISH SCORING
# =============================================================================

TRIGRAMS = {
    'THE': 100, 'AND': 80, 'ING': 75, 'HER': 65, 'HAT': 60, 'HIS': 58,
    'THA': 55, 'ERE': 52, 'FOR': 50, 'ENT': 48, 'ION': 46, 'TER': 44,
    'WAS': 42, 'YOU': 40, 'ITH': 38, 'VER': 36, 'ALL': 34, 'WIT': 32,
    'THI': 30, 'TIO': 28, 'OFT': 26, 'STH': 24, 'OTH': 22, 'RES': 20,
    'ONT': 18, 'ARE': 16, 'ERS': 14, 'NOT': 12, 'EVE': 10, 'OUT': 8,
}

QUADGRAMS = {
    'TION': 100, 'THAT': 90, 'WITH': 85, 'THER': 80, 'OULD': 75,
    'IGHT': 70, 'HAVE': 65, 'HICH': 60, 'WHIC': 55, 'THIS': 50,
    'THIN': 45, 'THEY': 40, 'ATIO': 35, 'EVER': 30, 'FROM': 25,
}

COMMON_WORDS = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS',
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
    'THERE', 'THESE', 'THING', 'THINK', 'THROUGH', 'TRUTH', 'WISDOM',
    'WITHIN', 'DIVINE', 'SPIRIT', 'LIGHT', 'SHADOW', 'PRIME', 'CICADA',
    'SECRET', 'HIDDEN', 'SACRED', 'MYSTIC', 'ANCIENT', 'INTUS',
]

def score_text(plaintext: np.ndarray) -> float:
    """Score plaintext for English-likeness."""
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
            score += len(word) * 5
    
    # IoC bonus
    n = len(plaintext)
    if n > 1:
        freq = np.bincount(plaintext, minlength=ALPHABET_SIZE)
        ioc = np.sum(freq * (freq - 1)) / (n * (n - 1))
        if ioc > 0.05:
            score += (ioc - 0.038) * 500
    
    return score

# =============================================================================
# KEY GENERATION
# =============================================================================

KNOWN_WORDS = [
    'DIVINITY', 'FIRFUMFERENFE', 'CONSUMPTION', 'KOAN', 'CICADA',
    'PRIME', 'PRIMES', 'TRUTH', 'WISDOM', 'LIBER', 'PRIMUS',
    'SECRET', 'HIDDEN', 'SHADOW', 'LIGHT', 'DARKNESS', 'INTUS',
    'SACRED', 'DIVINE', 'SPIRIT', 'ANCIENT', 'YAHEOOPYJ', 'MOBIUS',
    'PARABLE', 'PILGRIM', 'JOURNEY', 'INSTAR', 'EMERGENCE', 'MYSTERY',
    'CIPHER', 'RUNE', 'RUNES', 'GEMATRIA', 'TOTIENT', 'FIBONACCI',
    'COMMAND', 'OBEY', 'QUESTION', 'ANSWER', 'SEEK', 'FIND',
]

def word_to_key(word: str) -> np.ndarray:
    """Convert word to key indices."""
    indices = []
    word = word.upper()
    for c in word:
        for idx, lat in INDEX_TO_LATIN.items():
            if lat == c or (len(lat) > 1 and lat[0] == c):
                indices.append(idx)
                break
    return np.array(indices, dtype=np.int32) if indices else None

def generate_all_keys() -> List[Tuple[str, np.ndarray]]:
    """Generate all keys to try."""
    keys = []
    
    # 1. Caesar shifts
    for i in range(ALPHABET_SIZE):
        keys.append((f"CAESAR_{i}", np.array([i], dtype=np.int32)))
    
    # 2. Known words and variations
    for word in KNOWN_WORDS:
        key = word_to_key(word)
        if key is not None and len(key) > 0:
            keys.append((f"W:{word}", key))
            keys.append((f"W:{word}_REV", key[::-1].copy()))
            for offset in [1, 3, 7, 11, 13]:
                keys.append((f"W:{word}+{offset}", (key + offset) % 29))
    
    # 3. Prime sequences
    for length in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]:
        for start in range(0, min(300, len(PRIMES_MOD_29) - length), 3):
            key = np.array(PRIMES_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"P:L{length}S{start}", key))
    
    # 4. φ(prime) sequences
    for length in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]:
        for start in range(0, min(300, len(PRIME_TOTIENTS_MOD_29) - length), 3):
            key = np.array(PRIME_TOTIENTS_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"PHI:L{length}S{start}", key))
    
    # 5. Fibonacci sequences
    for length in range(3, 60, 2):
        for start in range(0, min(60, len(FIBONACCI_MOD_29) - length), 2):
            key = np.array(FIBONACCI_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"FIB:L{length}S{start}", key))
    
    # 6. Lucas sequences
    for length in range(3, 60, 2):
        for start in range(0, min(60, len(LUCAS_MOD_29) - length), 2):
            key = np.array(LUCAS_MOD_29[start:start+length], dtype=np.int32)
            keys.append((f"LUC:L{length}S{start}", key))
    
    # 7. Random keys for exploration
    np.random.seed(3301)
    for i in range(2000):
        length = np.random.randint(3, 50)
        key = np.random.randint(0, 29, size=length, dtype=np.int32)
        keys.append((f"RND:{i}", key))
    
    print(f"[KEYGEN] Generated {len(keys)} keys")
    return keys

# =============================================================================
# CIPHER WORKER
# =============================================================================

def try_key(args: Tuple[str, np.ndarray, np.ndarray, str]) -> Tuple[float, str, str, str]:
    """Worker to try a single key."""
    key_name, key, cipher, mode = args
    
    key_len = len(key)
    cipher_len = len(cipher)
    key_repeated = np.tile(key, (cipher_len // key_len + 1))[:cipher_len]
    
    if mode == 'SUB':
        plaintext = (cipher - key_repeated) % ALPHABET_SIZE
    elif mode == 'ADD':
        plaintext = (cipher + key_repeated) % ALPHABET_SIZE
    else:  # SUB_REV
        plaintext = (key_repeated - cipher) % ALPHABET_SIZE
    
    score = score_text(plaintext)
    text = indices_to_text(plaintext) if score > 5 else ""
    
    return (score, key_name, mode, text)

def try_phi_sequence(args: Tuple[int, np.ndarray, str]) -> Tuple[float, str, str, str]:
    """Worker for φ(prime) sequence decryption."""
    start_idx, cipher, mode = args
    cipher_len = len(cipher)
    
    if start_idx + cipher_len > len(PRIME_TOTIENTS_MOD_29):
        return (0.0, "", "", "")
    
    key_seq = np.array(PRIME_TOTIENTS_MOD_29[start_idx:start_idx + cipher_len], dtype=np.int32)
    
    if mode == 'SUB':
        plaintext = (cipher - key_seq) % ALPHABET_SIZE
    else:
        plaintext = (cipher + key_seq) % ALPHABET_SIZE
    
    score = score_text(plaintext)
    text = indices_to_text(plaintext) if score > 5 else ""
    
    return (score, f"PHI_START_{start_idx}", f"PHI_{mode}", text)

# =============================================================================
# RUNNING KEY ATTACK
# =============================================================================

def text_to_indices(text: str) -> np.ndarray:
    """Convert text to Gematria indices."""
    indices = []
    text = text.upper()
    i = 0
    while i < len(text):
        found = False
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
                    found = True
                    break
            i += 1
    return np.array(indices, dtype=np.int32)

def try_running_key(args: Tuple[int, np.ndarray, np.ndarray, str]) -> Tuple[float, str, str, str]:
    """Worker for running key attack."""
    start, cipher, key_indices, mode = args
    cipher_len = len(cipher)
    
    if start + cipher_len > len(key_indices):
        return (0.0, "", "", "")
    
    key_segment = key_indices[start:start + cipher_len]
    
    if mode == 'SUB':
        plaintext = (cipher - key_segment) % ALPHABET_SIZE
    else:
        plaintext = (cipher + key_segment) % ALPHABET_SIZE
    
    score = score_text(plaintext)
    text = indices_to_text(plaintext) if score > 5 else ""
    
    return (score, f"RK_START_{start}", f"RK_{mode}", text)

# =============================================================================
# MAIN SOLVER
# =============================================================================

class AggressiveSolver:
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
        self.self_reliance_indices = None
        self._load_self_reliance()
    
    def _load_self_reliance(self):
        """Load Self-Reliance text."""
        paths = [
            Path("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/research/Self-Reliance.txt"),
            Path("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/Self-Reliance.txt"),
            Path("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/Self-Reliance.txt"),
        ]
        for path in paths:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.self_reliance_indices = text_to_indices(text)
                print(f"[INFO] Loaded Self-Reliance: {len(self.self_reliance_indices)} indices")
                return
        print("[WARN] Self-Reliance not found")
    
    def load_cipher(self, page_num: int) -> np.ndarray:
        """Load cipher from page."""
        rune_path = Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt")
        if not rune_path.exists():
            raise FileNotFoundError(f"Rune file not found: {rune_path}")
        
        with open(rune_path, 'r', encoding='utf-8') as f:
            runes = f.read()
        
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def solve_page(self, page_num: int) -> List[Tuple[float, str, str, str]]:
        """Solve a single page with all attacks."""
        print(f"\n{'='*60}")
        print(f"[PAGE {page_num:02d}] AGGRESSIVE ATTACK")
        print('='*60)
        
        cipher = self.load_cipher(page_num)
        print(f"[INFO] Loaded {len(cipher)} runes")
        
        all_results = []
        
        # 1. Dictionary/Key attack
        print("[PHASE 1] Dictionary + Key attack...")
        keys = generate_all_keys()
        
        tasks = []
        for key_name, key in keys:
            for mode in ['SUB', 'ADD', 'SUB_REV']:
                tasks.append((key_name, key, cipher, mode))
        
        print(f"[INFO] Running {len(tasks)} key combinations with {self.num_workers} workers...")
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(try_key, task) for task in tasks]
            for i, future in enumerate(as_completed(futures)):
                result = future.result()
                if result[0] > 5:  # Only keep meaningful results
                    all_results.append(result)
                if (i + 1) % 50000 == 0:
                    print(f"[PROGRESS] {i + 1}/{len(tasks)} completed...")
        
        print(f"[PHASE 1] Found {len(all_results)} candidates")
        
        # 2. φ(prime) sequence attack
        print("[PHASE 2] φ(prime) sequence attack...")
        phi_tasks = []
        max_start = min(1000, len(PRIME_TOTIENTS_MOD_29) - len(cipher))
        for start in range(max_start):
            for mode in ['SUB', 'ADD']:
                phi_tasks.append((start, cipher, mode))
        
        print(f"[INFO] Testing {len(phi_tasks)} φ(prime) sequences...")
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(try_phi_sequence, task) for task in phi_tasks]
            for future in as_completed(futures):
                result = future.result()
                if result[0] > 5:
                    all_results.append(result)
        
        # 3. Running key attack with Self-Reliance
        if self.self_reliance_indices is not None and len(self.self_reliance_indices) > len(cipher):
            print("[PHASE 3] Running key attack (Self-Reliance)...")
            max_starts = len(self.self_reliance_indices) - len(cipher)
            
            rk_tasks = []
            for start in range(0, max_starts, 5):  # Every 5th position
                for mode in ['SUB', 'ADD']:
                    rk_tasks.append((start, cipher, self.self_reliance_indices, mode))
            
            print(f"[INFO] Testing {len(rk_tasks)} running key positions...")
            
            with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
                futures = [executor.submit(try_running_key, task) for task in rk_tasks]
                for future in as_completed(futures):
                    result = future.result()
                    if result[0] > 5:
                        all_results.append(result)
        
        # Sort results
        all_results.sort(reverse=True, key=lambda x: x[0])
        
        if all_results:
            print(f"\n[BEST] Score: {all_results[0][0]:.1f}")
            print(f"       Key: {all_results[0][1]}")
            print(f"       Mode: {all_results[0][2]}")
            print(f"       Text: {all_results[0][3][:80]}...")
        else:
            print("[WARN] No candidates found!")
        
        return all_results[:50]

# =============================================================================
# BATCH PROCESSOR
# =============================================================================

SKIP_PAGES = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,  # LP1 solved
              24, 30, 36, 44, 52,  # Image pages
              55, 56, 57, 73, 74]  # LP2 solved

UNSOLVED_PAGES = [2] + list(range(17, 55)) + list(range(58, 73))
UNSOLVED_PAGES = [p for p in UNSOLVED_PAGES if p not in SKIP_PAGES]

def batch_attack(pages: List[int] = None, output_path: str = "BATCH_RESULTS.md"):
    """Run batch attack on multiple pages."""
    if pages is None:
        pages = UNSOLVED_PAGES
    
    solver = AggressiveSolver()
    all_page_results = {}
    start_time = time.time()
    
    print("=" * 70)
    print("AGGRESSIVE PARALLEL BATCH ATTACK")
    print("=" * 70)
    print(f"Target Pages: {len(pages)}")
    print(f"Workers: {solver.num_workers}")
    print("=" * 70)
    
    for i, page_num in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] Processing Page {page_num:02d}")
        
        page_start = time.time()
        
        try:
            results = solver.solve_page(page_num)
            all_page_results[page_num] = results
        except Exception as e:
            print(f"[ERROR] Page {page_num}: {e}")
            all_page_results[page_num] = []
        
        page_time = time.time() - page_start
        print(f"[TIME] Page {page_num}: {page_time:.1f}s")
    
    total_time = time.time() - start_time
    
    # Save results
    save_results(all_page_results, output_path, total_time)
    
    print("\n" + "=" * 70)
    print("BATCH ATTACK COMPLETE")
    print("=" * 70)
    print(f"Total Time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"Pages: {len(all_page_results)}")
    print(f"Results: {output_path}")
    print("=" * 70)

def save_results(results: Dict, output_path: str, total_time: float):
    """Save results to markdown."""
    lines = [
        "# AGGRESSIVE BATCH ATTACK RESULTS",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Duration:** {total_time:.1f}s ({total_time/60:.1f} min)",
        f"**Pages:** {len(results)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Page | Score | Key | Mode | Preview |",
        "|------|-------|-----|------|---------|",
    ]
    
    for page_num in sorted(results.keys()):
        page_results = results[page_num]
        if page_results:
            top = page_results[0]
            preview = top[3][:35].replace('|', '\\|').replace('\n', ' ')
            lines.append(f"| {page_num:02d} | {top[0]:.1f} | `{top[1][:18]}` | {top[2]} | {preview}... |")
        else:
            lines.append(f"| {page_num:02d} | - | - | - | No results |")
    
    lines.extend(["", "---", "", "## Details", ""])
    
    for page_num in sorted(results.keys()):
        page_results = results[page_num]
        lines.append(f"### Page {page_num:02d}")
        lines.append("")
        
        if not page_results:
            lines.append("*No results.*\n")
            continue
        
        for i, (score, key, mode, text) in enumerate(page_results[:5], 1):
            lines.append(f"**{i}. Score: {score:.1f}** | Key: `{key}` | Mode: {mode}")
            lines.append(f"```\n{text[:300]}\n```\n")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # Also save JSON
    json_path = output_path.replace('.md', '.json')
    json_data = {
        'metadata': {'date': datetime.now().isoformat(), 'duration': total_time},
        'results': {str(p): [{'score': s, 'key': k, 'mode': m, 'text': t} 
                             for s, k, m, t in r] for p, r in results.items()}
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"[SAVED] {output_path}")
    print(f"[SAVED] {json_path}")

def main():
    parser = argparse.ArgumentParser(description="Aggressive parallel batch attack")
    parser.add_argument("--pages", type=str, default="all")
    parser.add_argument("--output", type=str, default="BATCH_RESULTS.md")
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()
    
    os.chdir(Path(__file__).parent)
    
    if args.pages == "all":
        pages = UNSOLVED_PAGES
    else:
        pages = [int(p.strip()) for p in args.pages.split(',')]
    
    batch_attack(pages, args.output)

if __name__ == "__main__":
    main()

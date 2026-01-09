#!/usr/bin/env python3
"""
RUNNING KEY SOLVER - Specialized for Self-Reliance and other text sources
==========================================================================

This module implements running key cipher attacks using text sources like
Emerson's Self-Reliance as the key stream.

Author: Wulfic
Date: January 2026
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
import numpy as np

from master_dictionary import (
    ALPHABET_SIZE, RUNE_TO_INDEX, INDEX_TO_LATIN,
    TRIGRAMS, QUADGRAMS, SELF_RELIANCE_TEXT, text_to_key
)

# =============================================================================
# RUNNING KEY CIPHER
# =============================================================================

def prepare_running_key_source(text: str) -> np.ndarray:
    """Prepare a text source for use as running key."""
    # Convert to uppercase, remove non-alphabetic
    clean = ''.join(c for c in text.upper() if c.isalpha())
    # Convert to indices
    return np.array(text_to_key(clean), dtype=np.int32)

def running_key_decrypt(cipher: np.ndarray, key_source: np.ndarray, 
                        start_offset: int = 0, mode: str = "SUB") -> np.ndarray:
    """Decrypt using running key cipher with offset into source."""
    key = key_source[start_offset:start_offset + len(cipher)]
    if len(key) < len(cipher):
        # Wrap around if needed
        repeats = (len(cipher) // len(key_source)) + 1
        key_source_extended = np.tile(key_source, repeats)
        key = key_source_extended[start_offset:start_offset + len(cipher)]
    
    if mode == "SUB":
        return (cipher - key) % ALPHABET_SIZE
    elif mode == "ADD":
        return (cipher + key) % ALPHABET_SIZE
    elif mode == "SUB_REV":
        return (key - cipher) % ALPHABET_SIZE
    else:
        return (cipher - key) % ALPHABET_SIZE

def indices_to_text(indices: np.ndarray) -> str:
    """Convert indices to Latin text."""
    return ''.join(INDEX_TO_LATIN.get(int(i), '?') for i in indices)

def score_text(indices: np.ndarray) -> float:
    """Score text using trigrams and quadgrams."""
    text = indices_to_text(indices)
    if len(text) < 4:
        return 0.0
    
    score = 0.0
    # Trigrams
    for i in range(len(text) - 2):
        tri = text[i:i+3]
        if tri in TRIGRAMS:
            score += TRIGRAMS[tri]
    
    # Quadgrams (weighted higher)
    for i in range(len(text) - 3):
        quad = text[i:i+4]
        if quad in QUADGRAMS:
            score += QUADGRAMS[quad] * 1.5
    
    return score / len(text)

# =============================================================================
# WORKER FUNCTIONS
# =============================================================================

def worker_try_offset(args: Tuple[int, np.ndarray, np.ndarray, str]) -> Tuple[int, str, float, str]:
    """Worker to try a specific offset."""
    offset, cipher, key_source, mode = args
    plaintext = running_key_decrypt(cipher, key_source, offset, mode)
    score = score_text(plaintext)
    text = indices_to_text(plaintext)
    return (offset, mode, score, text)

# =============================================================================
# MAIN SOLVER
# =============================================================================

class RunningKeySolver:
    """Solver for running key cipher."""
    
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
        self.sources = {}
        self._prepare_sources()
    
    def _prepare_sources(self):
        """Prepare all text sources."""
        # Self-Reliance
        if SELF_RELIANCE_TEXT:
            self.sources['SELF_RELIANCE'] = prepare_running_key_source(SELF_RELIANCE_TEXT)
        
        # Known plaintext from solved pages
        solved_texts = [
            ("PAGE_01", "AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETRUETESTTHEKNOWLEDGEFINDYOURTRUTHEXPERIENCEYOURDEATHDONOTEDITORCHANGETHISBOOKORTHEMESSAGECONTAINEDWITHINEITHERTHEWORDSORTHEIRNUMBERSFORALLISSACRED"),
            ("PAGE_03", "WELCOMEPILGRIMTOTHEGREATJOURNEYTOWARDTHEENDOFALLTHINGSITISNOTANEASYTRIPBUTFORTHOSEWHOFINDTHEIRWAYHEREISANECESSARYONEALONGTHEWAYYOUWILLFINDANENDTOALLSTRUGGLEANDSUFFERINGYOURINNOCENCEYOURILLUSIONSYOURCERTAINTYANDYOURREALTYULTIMATELYYOUWILLDISCOVERANENDTOSELF"),
            ("PAGE_05", "SOMEWISDOMTHEPRIMESARESACREDTHETOTIENTFUNCTIONISSACREDALLDIVISIONSARENOTEQUALSOMEARETRUERANDTHESEARETHEDIVISIONSBETWEENZEROANDONE"),
        ]
        
        for name, text in solved_texts:
            self.sources[name] = prepare_running_key_source(text)
        
        # Concatenate all solved pages as potential source
        all_solved = "".join(text for _, text in solved_texts)
        self.sources['ALL_SOLVED'] = prepare_running_key_source(all_solved)
    
    def load_cipher(self, page_num: int) -> np.ndarray:
        """Load cipher from page."""
        rune_path = Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt")
        with open(rune_path, 'r', encoding='utf-8') as f:
            runes = f.read()
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def solve(self, cipher: np.ndarray, source_name: str = None, 
              max_offset: int = None) -> List[Tuple[str, int, str, float, str]]:
        """
        Solve running key cipher.
        Returns: List of (source_name, offset, mode, score, text)
        """
        results = []
        
        sources_to_try = {source_name: self.sources[source_name]} if source_name else self.sources
        
        for src_name, key_source in sources_to_try.items():
            max_off = max_offset or (len(key_source) - len(cipher))
            if max_off <= 0:
                max_off = 1
            
            print(f"[INFO] Trying source: {src_name} with {max_off} offsets...")
            
            tasks = []
            for offset in range(max_off):
                for mode in ["SUB", "ADD", "SUB_REV"]:
                    tasks.append((offset, cipher, key_source, mode))
            
            with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
                futures = [executor.submit(worker_try_offset, task) for task in tasks]
                
                for future in as_completed(futures):
                    offset, mode, score, text = future.result()
                    results.append((src_name, offset, mode, score, text))
            
            print(f"[INFO] Completed {len(tasks)} offset/mode combinations for {src_name}")
        
        # Sort by score
        results.sort(key=lambda x: x[3], reverse=True)
        return results
    
    def print_top_results(self, results: List[Tuple[str, int, str, float, str]], 
                          top_n: int = 20):
        """Print top results."""
        print("\n" + "=" * 80)
        print("RUNNING KEY RESULTS")
        print("=" * 80)
        
        for i, (source, offset, mode, score, text) in enumerate(results[:top_n]):
            print(f"\n[{i+1}] Score: {score:.2f}")
            print(f"    Source: {source}, Offset: {offset}, Mode: {mode}")
            print(f"    Text: {text[:100]}..." if len(text) > 100 else f"    Text: {text}")

# =============================================================================
# CHAINED PLAINTEXT SOLVER
# =============================================================================

class ChainedPlaintextSolver:
    """
    Try using the plaintext of one page as the key for another.
    If pages are meant to be decrypted in sequence, this would work.
    """
    
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
    
    def load_cipher(self, page_num: int) -> np.ndarray:
        """Load cipher from page."""
        rune_path = Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt")
        with open(rune_path, 'r', encoding='utf-8') as f:
            runes = f.read()
        indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
        return np.array(indices, dtype=np.int32)
    
    def try_chain(self, source_page: int, target_page: int) -> List[Tuple[int, str, float, str]]:
        """
        Try using source_page runes as key for target_page.
        """
        source_cipher = self.load_cipher(source_page)
        target_cipher = self.load_cipher(target_page)
        
        results = []
        max_offset = max(1, len(source_cipher) - len(target_cipher))
        
        for offset in range(min(max_offset, 500)):  # Limit offsets
            for mode in ["SUB", "ADD", "SUB_REV"]:
                key = source_cipher[offset:offset + len(target_cipher)]
                if len(key) < len(target_cipher):
                    continue
                
                if mode == "SUB":
                    plaintext = (target_cipher - key) % ALPHABET_SIZE
                elif mode == "ADD":
                    plaintext = (target_cipher + key) % ALPHABET_SIZE
                else:
                    plaintext = (key - target_cipher) % ALPHABET_SIZE
                
                score = score_text(plaintext)
                text = indices_to_text(plaintext)
                results.append((offset, mode, score, text))
        
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:50]

# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Running key solver for Liber Primus")
    parser.add_argument("--page", type=int, default=17, help="Page number to solve")
    parser.add_argument("--source", type=str, help="Specific source to use (e.g., SELF_RELIANCE)")
    parser.add_argument("--max-offset", type=int, default=1000, help="Maximum offset to try")
    parser.add_argument("--top", type=int, default=20, help="Number of top results to show")
    parser.add_argument("--chain-from", type=int, help="Try chaining from this page number")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RUNNING KEY / CHAINED PLAINTEXT SOLVER")
    print("=" * 60)
    
    if args.chain_from:
        # Chained plaintext mode
        print(f"\n[MODE] Chained Plaintext: Page {args.chain_from} -> Page {args.page}")
        solver = ChainedPlaintextSolver()
        results = solver.try_chain(args.chain_from, args.page)
        
        print("\n" + "=" * 60)
        print(f"TOP RESULTS (Page {args.chain_from} as key for Page {args.page})")
        print("=" * 60)
        
        for i, (offset, mode, score, text) in enumerate(results[:args.top]):
            print(f"\n[{i+1}] Score: {score:.2f}, Offset: {offset}, Mode: {mode}")
            print(f"    Text: {text[:100]}..." if len(text) > 100 else f"    Text: {text}")
    else:
        # Running key mode
        print(f"\n[MODE] Running Key: Page {args.page}")
        solver = RunningKeySolver()
        
        cipher = solver.load_cipher(args.page)
        print(f"[INFO] Loaded page {args.page}: {len(cipher)} runes")
        
        results = solver.solve(cipher, args.source, args.max_offset)
        solver.print_top_results(results, args.top)

if __name__ == "__main__":
    main()

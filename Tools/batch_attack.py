#!/usr/bin/env python3
"""
BATCH ATTACK - LIBER PRIMUS FULL ASSAULT
========================================

Runs comprehensive brute force attacks on ALL unsolved pages using
dual RTX 2080 Ti GPUs and parallel CPU processing.

Unsolved Pages:
- LP1: Page 02 (title page)
- LP2: Pages 17-54 (37 pages - the "Deep Web" segment)
- LP2: Pages 58-72 (15 pages)
Total: 54 unsolved pages

Author: Wulfic
Date: January 2026
"""

import os
import sys
import time
import json
import argparse
import multiprocessing as mp
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any

import numpy as np

# Add LiberPrimus to path
LP_DIR = Path(__file__).parent
sys.path.insert(0, str(LP_DIR))

from master_dictionary import (
    ALPHABET_SIZE, RUNE_TO_INDEX, INDEX_TO_RUNE, INDEX_TO_LATIN,
    ALL_KEYS, KNOWN_KEYS, CICADA_TERM_KEYS, SELF_RELIANCE_WORD_KEYS,
    TRIGRAMS, QUADGRAMS, COMMON_ENGLISH_WORDS,
)

from brute_force_solver import (
    BruteForceSolver, Config,
    vigenere_decrypt_np, autokey_decrypt_np, phi_prime_decrypt_np,
    score_combined, indices_to_text,
)

# Try to import GPU modules
try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# =============================================================================
# UNSOLVED PAGES CONFIGURATION
# =============================================================================

# All unsolved pages in Liber Primus
UNSOLVED_PAGES = (
    [2] +                     # LP1: Title page
    list(range(17, 55)) +     # LP2: Pages 17-54 (38 pages)
    list(range(58, 73))       # LP2: Pages 58-72 (15 pages)
)  # Total: 54 pages

# Non-text pages (images/diagrams only - skip these)
NON_TEXT_PAGES = [2, 24, 30, 36, 44, 52]  # Primarily image/diagram pages

# Pages with very short rune content (may need special handling)
SHORT_PAGES = []

# Priority pages (known to have partial solutions or high interest)
PRIORITY_PAGES = [17, 18, 19, 20, 71]

# =============================================================================
# BATCH ATTACK RESULTS
# =============================================================================

class BatchResults:
    """Container for batch attack results."""
    
    def __init__(self):
        self.results: Dict[int, Dict] = {}
        self.start_time: float = 0
        self.end_time: float = 0
        self.errors: Dict[int, str] = {}
    
    def add_result(self, page_num: int, result: Dict):
        """Add results for a page."""
        self.results[page_num] = result
    
    def add_error(self, page_num: int, error: str):
        """Record an error for a page."""
        self.errors[page_num] = error
    
    def get_top_candidates(self, page_num: int, top_n: int = 5) -> List[Dict]:
        """Get top candidates for a page across all methods."""
        if page_num not in self.results:
            return []
        
        all_candidates = []
        for method, method_results in self.results[page_num].items():
            if method in ['metadata', 'error']:
                continue
            for result in method_results[:top_n]:
                all_candidates.append({
                    'method': method,
                    **result
                })
        
        # Sort by score descending
        all_candidates.sort(key=lambda x: x.get('score', 0), reverse=True)
        return all_candidates[:top_n]
    
    def to_markdown(self, output_path: str):
        """Export results to markdown format."""
        lines = [
            "# BATCH ATTACK RESULTS",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Duration:** {self.end_time - self.start_time:.2f} seconds",
            f"**Pages Processed:** {len(self.results)}",
            f"**Errors:** {len(self.errors)}",
            "",
            "---",
            "",
        ]
        
        # Summary table
        lines.extend([
            "## Summary",
            "",
            "| Page | Top Score | Top Key | Top Method | Preview |",
            "|------|-----------|---------|------------|---------|",
        ])
        
        for page_num in sorted(self.results.keys()):
            top_candidates = self.get_top_candidates(page_num, 1)
            if top_candidates:
                top = top_candidates[0]
                preview = top.get('text', '')[:40].replace('|', '\\|')
                lines.append(
                    f"| {page_num:02d} | {top.get('score', 0):.2f} | "
                    f"`{top.get('key', 'N/A')[:20]}` | {top.get('method', 'N/A')} | "
                    f"{preview}... |"
                )
            else:
                lines.append(f"| {page_num:02d} | - | - | - | No results |")
        
        lines.extend(["", "---", ""])
        
        # Detailed results per page
        lines.append("## Detailed Results")
        lines.append("")
        
        for page_num in sorted(self.results.keys()):
            lines.append(f"### Page {page_num:02d}")
            lines.append("")
            
            if page_num in self.errors:
                lines.append(f"**ERROR:** {self.errors[page_num]}")
                lines.append("")
                continue
            
            top_candidates = self.get_top_candidates(page_num, 10)
            
            if not top_candidates:
                lines.append("*No valid results found.*")
                lines.append("")
                continue
            
            lines.append("| Rank | Score | Method | Key | Text Preview |")
            lines.append("|------|-------|--------|-----|--------------|")
            
            for i, candidate in enumerate(top_candidates, 1):
                key = candidate.get('key', 'N/A')[:25]
                text = candidate.get('text', '')[:50].replace('|', '\\|').replace('\n', ' ')
                lines.append(
                    f"| {i} | {candidate.get('score', 0):.2f} | "
                    f"{candidate.get('method', 'N/A')} | `{key}` | {text}... |"
                )
            
            lines.append("")
            
            # Show best full text
            if top_candidates:
                best = top_candidates[0]
                lines.extend([
                    "**Best Decryption Attempt:**",
                    "```",
                    best.get('text', 'N/A')[:500],
                    "```",
                    "",
                ])
        
        # Error summary
        if self.errors:
            lines.extend([
                "---",
                "",
                "## Errors",
                "",
            ])
            for page_num, error in sorted(self.errors.items()):
                lines.append(f"- **Page {page_num:02d}:** {error}")
            lines.append("")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"[INFO] Results saved to {output_path}")
    
    def to_json(self, output_path: str):
        """Export results to JSON format."""
        output = {
            'metadata': {
                'date': datetime.now().isoformat(),
                'duration_seconds': self.end_time - self.start_time,
                'pages_processed': len(self.results),
                'errors': len(self.errors),
            },
            'results': self.results,
            'errors': self.errors,
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        
        print(f"[INFO] JSON results saved to {output_path}")

# =============================================================================
# BATCH PROCESSOR
# =============================================================================

class BatchProcessor:
    """Processes multiple pages in batch mode."""
    
    def __init__(self, config: Config, verbose: bool = True):
        self.config = config
        self.verbose = verbose
        self.solver = BruteForceSolver(config)
        self.batch_results = BatchResults()
    
    def process_page(self, page_num: int) -> Dict:
        """Process a single page and return results."""
        result = {
            'metadata': {
                'page': page_num,
                'timestamp': datetime.now().isoformat(),
            }
        }
        
        try:
            # Load cipher
            cipher = self.solver.load_cipher(page_num)
            result['metadata']['rune_count'] = len(cipher)
            
            if len(cipher) < 10:
                result['metadata']['status'] = 'skipped_short'
                return result
            
            # Run all solving methods
            if self.verbose:
                print(f"\n[PAGE {page_num:02d}] Processing {len(cipher)} runes...")
            
            page_results = self.solver.solve_all(cipher)
            
            # Convert to JSON-serializable format
            for method, method_results in page_results.items():
                result[method] = [
                    {'score': float(score), 'key': key, 'mode': mode, 'text': text}
                    for score, key, mode, text in method_results[:20]  # Top 20 per method
                ]
            
            result['metadata']['status'] = 'success'
            
        except FileNotFoundError as e:
            result['metadata']['status'] = 'file_not_found'
            result['error'] = str(e)
            
        except Exception as e:
            result['metadata']['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def run_batch(self, pages: List[int] = None) -> BatchResults:
        """Run batch attack on specified pages."""
        if pages is None:
            pages = UNSOLVED_PAGES
        
        # Filter out non-text pages
        pages = [p for p in pages if p not in NON_TEXT_PAGES]
        
        print("=" * 70)
        print("LIBER PRIMUS BATCH ATTACK")
        print("=" * 70)
        print(f"Target Pages: {len(pages)}")
        print(f"GPU Acceleration: {'ENABLED' if self.config.use_gpu else 'DISABLED'}")
        print(f"Parallel Workers: {self.config.num_workers}")
        print(f"Pages: {pages}")
        print("=" * 70)
        
        self.batch_results = BatchResults()
        self.batch_results.start_time = time.time()
        
        for i, page_num in enumerate(pages, 1):
            print(f"\n{'=' * 50}")
            print(f"[{i}/{len(pages)}] Processing Page {page_num:02d}")
            print('=' * 50)
            
            page_start = time.time()
            
            try:
                result = self.process_page(page_num)
                self.batch_results.add_result(page_num, result)
                
                # Print quick summary
                top_candidates = []
                for method, method_results in result.items():
                    if method in ['metadata', 'error']:
                        continue
                    if method_results:
                        top = method_results[0]
                        top_candidates.append({
                            'method': method,
                            **top
                        })
                
                top_candidates.sort(key=lambda x: x.get('score', 0), reverse=True)
                
                if top_candidates:
                    best = top_candidates[0]
                    print(f"\n[BEST] Score: {best['score']:.2f}")
                    print(f"       Key: {best['key']}")
                    print(f"       Method: {best['method']}")
                    print(f"       Text: {best['text'][:80]}...")
                else:
                    print("\n[WARN] No valid results found")
                
            except Exception as e:
                self.batch_results.add_error(page_num, str(e))
                print(f"\n[ERROR] Page {page_num}: {e}")
            
            page_elapsed = time.time() - page_start
            print(f"\n[TIME] Page {page_num} completed in {page_elapsed:.2f}s")
        
        self.batch_results.end_time = time.time()
        
        total_elapsed = self.batch_results.end_time - self.batch_results.start_time
        print("\n" + "=" * 70)
        print("BATCH ATTACK COMPLETE")
        print("=" * 70)
        print(f"Total Time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)")
        print(f"Pages Processed: {len(self.batch_results.results)}")
        print(f"Errors: {len(self.batch_results.errors)}")
        print("=" * 70)
        
        return self.batch_results

# =============================================================================
# HIGH-VALUE TARGET ATTACKS
# =============================================================================

def attack_priority_pages(config: Config) -> BatchResults:
    """Focus attack on high-priority unsolved pages."""
    processor = BatchProcessor(config, verbose=True)
    return processor.run_batch(PRIORITY_PAGES)

def attack_deep_web_segment(config: Config) -> BatchResults:
    """Attack the 'Deep Web' segment (pages 17-54)."""
    deep_web_pages = list(range(17, 55))
    deep_web_pages = [p for p in deep_web_pages if p not in NON_TEXT_PAGES]
    
    processor = BatchProcessor(config, verbose=True)
    return processor.run_batch(deep_web_pages)

def attack_all_unsolved(config: Config) -> BatchResults:
    """Full assault on all unsolved pages."""
    processor = BatchProcessor(config, verbose=True)
    return processor.run_batch(UNSOLVED_PAGES)

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Batch attack on all unsolved Liber Primus pages"
    )
    parser.add_argument(
        "--pages", type=str, default="all",
        help="Pages to attack: 'all', 'priority', 'deepweb', or comma-separated (e.g., '17,18,19')"
    )
    parser.add_argument(
        "--output", type=str, default="Analysis/Outputs/BATCH_RESULTS.md",
        help="Output markdown file (default: Analysis/Outputs/BATCH_RESULTS.md)"
    )
    parser.add_argument(
        "--json", type=str, default=None,
        help="Optional JSON output file"
    )
    parser.add_argument(
        "--workers", type=int, default=max(1, mp.cpu_count() - 1),
        help="Number of parallel workers"
    )
    parser.add_argument(
        "--no-gpu", action="store_true",
        help="Disable GPU acceleration"
    )
    parser.add_argument(
        "--top", type=int, default=20,
        help="Number of top results per method per page"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Quick mode: fewer key variations"
    )
    
    args = parser.parse_args()
    
    # Configure solver
    config = Config(
        use_gpu=not args.no_gpu and GPU_AVAILABLE,
        num_workers=args.workers,
        top_results=args.top,
        try_all_offsets=not args.quick,
        try_reversed=not args.quick,
        try_inverted=not args.quick,
    )
    
    # Determine which pages to attack
    if args.pages == "all":
        results = attack_all_unsolved(config)
    elif args.pages == "priority":
        results = attack_priority_pages(config)
    elif args.pages == "deepweb":
        results = attack_deep_web_segment(config)
    else:
        # Parse comma-separated page numbers
        try:
            pages = [int(p.strip()) for p in args.pages.split(',')]
            processor = BatchProcessor(config, verbose=True)
            results = processor.run_batch(pages)
        except ValueError:
            print(f"[ERROR] Invalid page specification: {args.pages}")
            sys.exit(1)
    
    # Save results
    output_path = LP_DIR / args.output
    results.to_markdown(str(output_path))
    
    if args.json:
        json_path = LP_DIR / args.json
        results.to_json(str(json_path))
    
    print(f"\n[DONE] Results saved to {output_path}")

if __name__ == "__main__":
    main()

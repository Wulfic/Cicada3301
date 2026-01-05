#!/usr/bin/env python3
"""
COMPREHENSIVE BATCH KEY ATTACK
==============================

Tests MANY different key transformations against ALL pages simultaneously.
Collects all results for analysis.

Strategies tested:
1. All 95 rotations of master key
2. All 29 offset additions to key
3. Combined rotation + offset (95 × 29 = 2755 combinations per page)
4. Reversed key
5. Negated key (29 - key)
6. XOR instead of subtraction
7. Position-based key modifications
8. Interleaved keys
"""

import re
import numpy as np
from pathlib import Path
from collections import defaultdict
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

# Common English and Cicada words (weighted by importance)
ENGLISH_WORDS = {
    # High value (3 points per char)
    'PARABLE': 3, 'INSTAR': 3, 'DIVINITY': 3, 'EMERGE': 3, 'CIRCUMFERENCE': 3,
    'WISDOM': 3, 'TRUTH': 3, 'PRIME': 3, 'SACRED': 3, 'DIVINE': 3,
    # Medium value (2 points per char)
    'THE': 2, 'AND': 2, 'THAT': 2, 'HAVE': 2, 'WITH': 2, 'THIS': 2,
    'FROM': 2, 'THEY': 2, 'WILL': 2, 'WHAT': 2, 'WHEN': 2, 'KNOW': 2,
    'WITHIN': 2, 'SURFACE': 2, 'TUNNELING': 2,
    # Standard value (1 point per char)
    'AN': 1, 'BE': 1, 'IT': 1, 'IS': 1, 'TO': 1, 'OF': 1, 'IN': 1, 
    'HE': 1, 'WE': 1, 'OR': 1, 'FOR': 1, 'NOT': 1, 'ALL': 1, 'CAN': 1,
    'HER': 1, 'WAS': 1, 'ONE': 1, 'OUR': 1, 'YOU': 1, 'ARE': 1, 'BUT': 1,
}

# Master key from breakthrough
MASTER_KEY = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                       20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                       17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                       5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                       14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)

KEY_LEN = len(MASTER_KEY)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def score_english(text):
    """Score text for English word content"""
    text_upper = text.upper()
    score = 0
    words_found = []
    
    for word, weight in ENGLISH_WORDS.items():
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word) * weight
            words_found.append(f"{word}({count})")
    
    return score, words_found

def extend_key(key, length):
    """Extend key to match target length by tiling"""
    return np.tile(key, (length // len(key) + 1))[:length]

def load_all_pages():
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
            pages[page_num] = runes_to_indices(runes_only)
    return pages

def test_key_on_page(page_idx, key, operation='sub'):
    """Apply key to page with specified operation"""
    extended = extend_key(key, len(page_idx))
    
    if operation == 'sub':
        decrypted = (page_idx - extended) % 29
    elif operation == 'add':
        decrypted = (page_idx + extended) % 29
    elif operation == 'xor':
        decrypted = page_idx ^ extended
        decrypted = decrypted % 29
    else:
        decrypted = (page_idx - extended) % 29
    
    text = indices_to_text(decrypted)
    score, words = score_english(text)
    return score, words, text

def batch_test_page(pg_num, pg_idx, results_queue):
    """Test all key variations on a single page"""
    page_results = []
    
    # Skip known solved pages
    if pg_num in [0, 54, 56, 57]:
        return pg_num, []
    
    # Strategy 1: All 95 rotations with subtraction
    for rotation in range(KEY_LEN):
        rotated_key = np.roll(MASTER_KEY, rotation)
        score, words, text = test_key_on_page(pg_idx, rotated_key, 'sub')
        if score >= 40:
            page_results.append({
                'strategy': 'rotation',
                'params': {'rotation': rotation},
                'score': score,
                'words': words[:8],
                'text': text[:100]
            })
    
    # Strategy 2: All 29 offsets
    for offset in range(29):
        offset_key = (MASTER_KEY + offset) % 29
        score, words, text = test_key_on_page(pg_idx, offset_key, 'sub')
        if score >= 40:
            page_results.append({
                'strategy': 'offset',
                'params': {'offset': offset},
                'score': score,
                'words': words[:8],
                'text': text[:100]
            })
    
    # Strategy 3: Reversed key
    reversed_key = MASTER_KEY[::-1]
    score, words, text = test_key_on_page(pg_idx, reversed_key, 'sub')
    if score >= 40:
        page_results.append({
            'strategy': 'reversed',
            'params': {},
            'score': score,
            'words': words[:8],
            'text': text[:100]
        })
    
    # Strategy 4: Negated key
    negated_key = (29 - MASTER_KEY) % 29
    score, words, text = test_key_on_page(pg_idx, negated_key, 'sub')
    if score >= 40:
        page_results.append({
            'strategy': 'negated',
            'params': {},
            'score': score,
            'words': words[:8],
            'text': text[:100]
        })
    
    # Strategy 5: XOR operation (all rotations)
    for rotation in range(KEY_LEN):
        rotated_key = np.roll(MASTER_KEY, rotation)
        score, words, text = test_key_on_page(pg_idx, rotated_key, 'xor')
        if score >= 40:
            page_results.append({
                'strategy': 'xor_rotation',
                'params': {'rotation': rotation},
                'score': score,
                'words': words[:8],
                'text': text[:100]
            })
    
    # Strategy 6: Addition instead of subtraction
    for rotation in range(KEY_LEN):
        rotated_key = np.roll(MASTER_KEY, rotation)
        score, words, text = test_key_on_page(pg_idx, rotated_key, 'add')
        if score >= 40:
            page_results.append({
                'strategy': 'add_rotation',
                'params': {'rotation': rotation},
                'score': score,
                'words': words[:8],
                'text': text[:100]
            })
    
    # Strategy 7: Page number as key modifier
    page_modifier = pg_num % 29
    modified_key = (MASTER_KEY + page_modifier) % 29
    score, words, text = test_key_on_page(pg_idx, modified_key, 'sub')
    if score >= 40:
        page_results.append({
            'strategy': 'page_modifier',
            'params': {'modifier': page_modifier},
            'score': score,
            'words': words[:8],
            'text': text[:100]
        })
    
    # Strategy 8: Combined rotation + page number offset
    for rotation in [pg_num % KEY_LEN, (pg_num * 2) % KEY_LEN, (pg_num * 3) % KEY_LEN]:
        rotated_key = np.roll(MASTER_KEY, rotation)
        for offset in [pg_num % 29, (pg_num * 2) % 29]:
            offset_key = (rotated_key + offset) % 29
            score, words, text = test_key_on_page(pg_idx, offset_key, 'sub')
            if score >= 40:
                page_results.append({
                    'strategy': 'combined_page',
                    'params': {'rotation': rotation, 'offset': offset},
                    'score': score,
                    'words': words[:8],
                    'text': text[:100]
                })
    
    # Strategy 9: Double key (apply key twice)
    double_key = (MASTER_KEY * 2) % 29
    score, words, text = test_key_on_page(pg_idx, double_key, 'sub')
    if score >= 40:
        page_results.append({
            'strategy': 'double_key',
            'params': {},
            'score': score,
            'words': words[:8],
            'text': text[:100]
        })
    
    # Strategy 10: Half key (divide by 2, using modular inverse)
    # 2 * 15 = 30 ≡ 1 (mod 29), so inverse of 2 is 15
    half_key = (MASTER_KEY * 15) % 29
    score, words, text = test_key_on_page(pg_idx, half_key, 'sub')
    if score >= 40:
        page_results.append({
            'strategy': 'half_key',
            'params': {},
            'score': score,
            'words': words[:8],
            'text': text[:100]
        })
    
    return pg_num, page_results

def main():
    print("="*70)
    print("🔬 COMPREHENSIVE BATCH KEY ATTACK")
    print("="*70)
    
    start_time = time.time()
    
    pages = load_all_pages()
    skip_pages = [0, 54, 56, 57]
    test_pages = {k: v for k, v in pages.items() if k not in skip_pages}
    
    print(f"\n📊 Testing {len(test_pages)} pages")
    print(f"   Strategies per page: ~{95 + 29 + 95 + 95 + 6} key variants")
    print(f"   Threshold for reporting: score >= 40")
    print("\n⏳ Processing...")
    
    all_results = {}
    
    for pg_num, pg_idx in sorted(test_pages.items()):
        pg_num, results = batch_test_page(pg_num, pg_idx, None)
        if results:
            all_results[pg_num] = results
        print(f"   Page {pg_num:2d}: {len(results)} promising results", end='\r')
    
    elapsed = time.time() - start_time
    print(f"\n\n✅ Completed in {elapsed:.1f} seconds")
    
    # Organize results by score
    print("\n" + "="*70)
    print("📊 RESULTS BY PAGE (sorted by best score)")
    print("="*70)
    
    page_best = {}
    for pg_num, results in all_results.items():
        if results:
            best = max(results, key=lambda x: x['score'])
            page_best[pg_num] = best
    
    for pg_num in sorted(page_best.keys(), key=lambda x: -page_best[x]['score']):
        best = page_best[pg_num]
        print(f"\n📄 Page {pg_num}: Best Score = {best['score']}")
        print(f"   Strategy: {best['strategy']}")
        print(f"   Params: {best['params']}")
        print(f"   Words: {', '.join(best['words'][:6])}")
        print(f"   Text: {best['text'][:80]}...")
    
    # Detailed breakdown of top results
    print("\n" + "="*70)
    print("🏆 TOP 20 RESULTS (All Strategies)")
    print("="*70)
    
    all_flat = []
    for pg_num, results in all_results.items():
        for r in results:
            all_flat.append((pg_num, r))
    
    all_flat.sort(key=lambda x: -x[1]['score'])
    
    for i, (pg_num, result) in enumerate(all_flat[:20]):
        print(f"\n{i+1:2d}. Page {pg_num} - Score {result['score']}")
        print(f"    Strategy: {result['strategy']} {result['params']}")
        print(f"    Words: {', '.join(result['words'][:6])}")
        print(f"    Text: {result['text'][:70]}...")
    
    # Strategy effectiveness summary
    print("\n" + "="*70)
    print("📈 STRATEGY EFFECTIVENESS SUMMARY")
    print("="*70)
    
    strategy_counts = defaultdict(list)
    for pg_num, results in all_results.items():
        for r in results:
            strategy_counts[r['strategy']].append(r['score'])
    
    print("\n   Strategy               | Count | Avg Score | Max Score")
    print("   " + "-"*55)
    for strategy in sorted(strategy_counts.keys(), key=lambda x: -max(strategy_counts[x])):
        scores = strategy_counts[strategy]
        print(f"   {strategy:22s} | {len(scores):5d} | {np.mean(scores):9.1f} | {max(scores):9d}")
    
    # Export results for further analysis
    print("\n" + "="*70)
    print("💾 EXPORTING DETAILED RESULTS")
    print("="*70)
    
    output_file = Path(r"C:\Users\tyler\Repos\Cicada3301\tools\batch_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("BATCH KEY ATTACK RESULTS\n")
        f.write("=" * 70 + "\n\n")
        
        for pg_num in sorted(all_results.keys()):
            results = sorted(all_results[pg_num], key=lambda x: -x['score'])
            f.write(f"\n{'='*70}\n")
            f.write(f"PAGE {pg_num}\n")
            f.write(f"{'='*70}\n")
            
            for r in results:
                f.write(f"\nStrategy: {r['strategy']} | Params: {r['params']} | Score: {r['score']}\n")
                f.write(f"Words: {', '.join(r['words'])}\n")
                f.write(f"Text: {r['text']}\n")
    
    print(f"\n   Results saved to: {output_file}")
    
    return all_results

if __name__ == "__main__":
    results = main()

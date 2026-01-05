#!/usr/bin/env python3
"""
INTENSIVE BATCH ATTACK - COMBINED ROTATION + OFFSET
====================================================

Based on initial results, we test ALL 95 rotations × ALL 29 offsets = 2755 combinations per page.
This is computationally intensive but will find the best possible key transformations.
"""

import re
import numpy as np
from pathlib import Path
from collections import defaultdict
import time

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

ENGLISH_WORDS = {
    'PARABLE': 4, 'INSTAR': 4, 'DIVINITY': 4, 'EMERGE': 4, 'CIRCUMFERENCE': 4,
    'WISDOM': 4, 'TRUTH': 4, 'PRIME': 4, 'SACRED': 4, 'DIVINE': 4,
    'WITHIN': 3, 'SURFACE': 3, 'TUNNELING': 3, 'SHED': 3,
    'THE': 2, 'AND': 2, 'THAT': 2, 'HAVE': 2, 'WITH': 2, 'THIS': 2,
    'FROM': 2, 'THEY': 2, 'WILL': 2, 'WHAT': 2, 'WHEN': 2, 'KNOW': 2,
    'AN': 1, 'BE': 1, 'IT': 1, 'IS': 1, 'TO': 1, 'OF': 1, 'IN': 1, 
    'HE': 1, 'WE': 1, 'OR': 1, 'FOR': 1, 'NOT': 1, 'ALL': 1, 'CAN': 1,
    'HER': 1, 'WAS': 1, 'ONE': 1, 'OUR': 1, 'YOU': 1, 'ARE': 1, 'BUT': 1,
}

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

def test_all_combinations(pg_num, pg_idx):
    """Test all 95×29 = 2755 rotation+offset combinations"""
    best_results = []
    
    for rotation in range(KEY_LEN):
        rotated = np.roll(MASTER_KEY, rotation)
        
        for offset in range(29):
            key = (rotated + offset) % 29
            extended = extend_key(key, len(pg_idx))
            
            # Test subtraction
            decrypted_sub = (pg_idx - extended) % 29
            text_sub = indices_to_text(decrypted_sub)
            score_sub, words_sub = score_english(text_sub)
            
            if score_sub >= 60:
                best_results.append({
                    'operation': 'sub',
                    'rotation': rotation,
                    'offset': offset,
                    'score': score_sub,
                    'words': words_sub[:8],
                    'text': text_sub
                })
            
            # Test XOR
            decrypted_xor = (pg_idx ^ extended) % 29
            text_xor = indices_to_text(decrypted_xor)
            score_xor, words_xor = score_english(text_xor)
            
            if score_xor >= 60:
                best_results.append({
                    'operation': 'xor',
                    'rotation': rotation,
                    'offset': offset,
                    'score': score_xor,
                    'words': words_xor[:8],
                    'text': text_xor
                })
    
    return best_results

def main():
    print("="*70)
    print("🔥 INTENSIVE BATCH ATTACK")
    print("="*70)
    
    start_time = time.time()
    
    pages = load_all_pages()
    skip_pages = [0, 54, 56, 57]
    test_pages = {k: v for k, v in pages.items() if k not in skip_pages}
    
    print(f"\n📊 Testing {len(test_pages)} pages")
    print(f"   Combinations per page: {KEY_LEN} × 29 × 2 = {KEY_LEN * 29 * 2}")
    print(f"   Total tests: {len(test_pages) * KEY_LEN * 29 * 2:,}")
    print(f"   Threshold: score >= 60")
    print("\n⏳ Processing...")
    
    all_results = {}
    
    for pg_num, pg_idx in sorted(test_pages.items()):
        results = test_all_combinations(pg_num, pg_idx)
        if results:
            all_results[pg_num] = results
        print(f"   Page {pg_num:2d}: {len(results):3d} results (score ≥60)", end='\r')
    
    elapsed = time.time() - start_time
    print(f"\n\n✅ Completed in {elapsed:.1f} seconds")
    
    # Show best result per page
    print("\n" + "="*70)
    print("📊 BEST RESULT PER PAGE")
    print("="*70)
    
    page_bests = []
    for pg_num, results in all_results.items():
        if results:
            best = max(results, key=lambda x: x['score'])
            page_bests.append((pg_num, best))
    
    page_bests.sort(key=lambda x: -x[1]['score'])
    
    for pg_num, best in page_bests:
        print(f"\n📄 Page {pg_num}: Score = {best['score']}")
        print(f"   Op={best['operation']}, Rot={best['rotation']}, Off={best['offset']}")
        print(f"   Words: {', '.join(best['words'][:6])}")
        print(f"   Text: {best['text'][:80]}...")
    
    # Show ALL results with score >= 80 (potential solutions)
    print("\n" + "="*70)
    print("🎯 HIGH CONFIDENCE RESULTS (Score >= 80)")
    print("="*70)
    
    high_confidence = []
    for pg_num, results in all_results.items():
        for r in results:
            if r['score'] >= 80:
                high_confidence.append((pg_num, r))
    
    if high_confidence:
        high_confidence.sort(key=lambda x: -x[1]['score'])
        for pg_num, r in high_confidence:
            print(f"\n🏆 Page {pg_num}: Score = {r['score']}")
            print(f"   Operation: {r['operation']}")
            print(f"   Rotation: {r['rotation']}, Offset: {r['offset']}")
            print(f"   Words: {', '.join(r['words'])}")
            print(f"   Full text: {r['text']}")
    else:
        print("\n   No results with score >= 80 found.")
        print("   Best scores are in the 60-79 range.")
    
    # Summary statistics
    print("\n" + "="*70)
    print("📈 SUMMARY STATISTICS")
    print("="*70)
    
    all_scores = []
    for pg_num, results in all_results.items():
        for r in results:
            all_scores.append(r['score'])
    
    if all_scores:
        print(f"\n   Total qualifying results: {len(all_scores)}")
        print(f"   Score range: {min(all_scores)} - {max(all_scores)}")
        print(f"   Average score: {np.mean(all_scores):.1f}")
        
        # Count by score bracket
        brackets = {
            '60-69': len([s for s in all_scores if 60 <= s < 70]),
            '70-79': len([s for s in all_scores if 70 <= s < 80]),
            '80-89': len([s for s in all_scores if 80 <= s < 90]),
            '90-99': len([s for s in all_scores if 90 <= s < 100]),
            '100+': len([s for s in all_scores if s >= 100]),
        }
        print(f"\n   Score distribution:")
        for bracket, count in brackets.items():
            if count > 0:
                print(f"      {bracket}: {count}")
    
    # Export detailed results
    output_file = Path(r"C:\Users\tyler\Repos\Cicada3301\tools\intensive_batch_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("INTENSIVE BATCH RESULTS (All rotation+offset combinations)\n")
        f.write("=" * 70 + "\n\n")
        
        for pg_num, best in page_bests:
            f.write(f"\n{'='*70}\n")
            f.write(f"PAGE {pg_num} - Best Score: {best['score']}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Operation: {best['operation']}\n")
            f.write(f"Rotation: {best['rotation']}, Offset: {best['offset']}\n")
            f.write(f"Words: {', '.join(best['words'])}\n")
            f.write(f"Text: {best['text']}\n")
            
            # Also write all results for this page
            if pg_num in all_results:
                f.write(f"\nAll results for page {pg_num}:\n")
                for r in sorted(all_results[pg_num], key=lambda x: -x['score'])[:10]:
                    f.write(f"  Score={r['score']}, Op={r['operation']}, Rot={r['rotation']}, Off={r['offset']}\n")
    
    print(f"\n   Results saved to: {output_file}")
    
    return all_results, page_bests

if __name__ == "__main__":
    results, bests = main()

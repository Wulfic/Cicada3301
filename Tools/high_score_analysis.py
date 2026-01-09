#!/usr/bin/env python3
"""
Targeted Analysis of High-Score Pages
Pages 25, 50, 32, 40, 20 showed high scores (>1000) in batch attack but weren't verified
Let's investigate these more closely
"""

import os
from collections import Counter

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LETTER = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E',
    19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

COMMON_WORDS = {'THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'AS', 'WITH', 'WAS', 
                'HIS', 'BE', 'AT', 'BY', 'THIS', 'HAD', 'NOT', 'ARE', 'BUT', 'FROM',
                'DIVINITY', 'WITHIN', 'PRIMES', 'SACRED', 'PILGRIM', 'WISDOM', 'TRUTH',
                'WE', 'AN', 'THAT', 'THEY', 'WILL', 'ALL', 'EACH', 'WHICH', 'THEIR',
                'THERE', 'WHAT', 'ABOUT', 'WHEN', 'MAKE', 'LIKE', 'TIME', 'JUST', 'WHO',
                'KNOW', 'MASTER', 'STUDENT', 'KOAN', 'BELIEVE', 'NOTHING', 'BOOK'}

def load_runes(page_num):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_file = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if not os.path.exists(rune_file):
        return None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    runes = [c for c in content if c in RUNE_TO_INDEX]
    return runes

def caesar_decrypt(runes, shift, reverse=False):
    """Apply Caesar shift (subtract shift value)"""
    if reverse:
        runes = list(reversed(runes))
    
    result = []
    for rune in runes:
        idx = RUNE_TO_INDEX[rune]
        new_idx = (idx - shift) % 29
        result.append(INDEX_TO_LETTER[new_idx])
    
    return ''.join(result)

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        count = text.count(word)
        score += len(word) * len(word) * count  # Longer words worth more
    return score

def calculate_ioc(text):
    counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))

def main():
    print("=" * 70)
    print("TARGETED ANALYSIS: HIGH-SCORE PAGES FROM BATCH ATTACK")
    print("=" * 70)
    
    # High-score pages identified in BREAKTHROUGH_DISCOVERIES.md
    target_pages = [25, 50, 32, 40, 20]
    
    for page_num in target_pages:
        runes = load_runes(page_num)
        if not runes:
            print(f"\nPage {page_num}: No runes found")
            continue
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} ({len(runes)} runes)")
        print("=" * 70)
        
        # Test all 29 Caesar shifts, both normal and reversed
        best_results = []
        
        for shift in range(29):
            for reverse in [False, True]:
                text = caesar_decrypt(runes, shift, reverse)
                score = score_text(text)
                ioc = calculate_ioc(text)
                mode = "REV" if reverse else "NOR"
                
                if score > 100 or ioc > 0.06:
                    best_results.append((shift, mode, score, ioc, text[:100]))
        
        # Sort by score
        best_results.sort(key=lambda x: -x[2])
        
        if best_results:
            print("\nTop results:")
            for shift, mode, score, ioc, preview in best_results[:5]:
                print(f"  Shift {shift:2} {mode}: Score={score:4}, IoC={ioc:.4f}")
                print(f"    {preview}")
        
        # Also check direct gematria (CAESAR_0)
        direct = caesar_decrypt(runes, 0, False)
        direct_score = score_text(direct)
        direct_ioc = calculate_ioc(direct)
        print(f"\n  Direct Gematria (CAESAR_0): Score={direct_score}, IoC={direct_ioc:.4f}")
        print(f"    {direct[:100]}")
    
    print("\n" + "=" * 70)
    print("CHECKING PREVIOUSLY SOLVED PAGES FOR REFERENCE")
    print("=" * 70)
    
    # Check pages 59, 63, 64, 68 which were solved
    for page_num in [59, 63, 64, 68]:
        runes = load_runes(page_num)
        if not runes:
            continue
        
        print(f"\nPage {page_num} ({len(runes)} runes):")
        
        # Find best shift
        best = (0, 0, 0, "", False)
        for shift in range(29):
            for reverse in [False, True]:
                text = caesar_decrypt(runes, shift, reverse)
                score = score_text(text)
                if score > best[1]:
                    best = (shift, score, calculate_ioc(text), text[:80], reverse)
        
        mode = "REV" if best[4] else "NOR"
        print(f"  Best: CAESAR_{best[0]} {mode} | Score={best[1]}, IoC={best[2]:.4f}")
        print(f"  Text: {best[3]}")

if __name__ == '__main__':
    main()

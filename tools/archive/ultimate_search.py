#!/usr/bin/env python3
"""
ULTIMATE EXHAUSTIVE SEARCH
Test every possible single-layer decryption with fine granularity.
Focus on finding the absolute best results across all combinations.
Uses multiprocessing for speed.
"""

import multiprocessing as mp
from itertools import product
from collections import Counter
import time

RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# English letter frequency (approximate)
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3,
    'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
    'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0
}

# Map runes to approximate English equivalents
RUNE_TO_ENGLISH = {
    'F': 'F', 'U': 'U', 'TH': 'TH', 'O': 'O', 'R': 'R', 'C': 'K', 'G': 'G',
    'W': 'W', 'H': 'H', 'N': 'N', 'I': 'I', 'J': 'J', 'EO': 'IO', 'P': 'P',
    'X': 'X', 'S': 'S', 'T': 'T', 'B': 'B', 'E': 'E', 'M': 'M', 'L': 'L',
    'NG': 'NG', 'OE': 'OE', 'D': 'D', 'A': 'A', 'AE': 'AE', 'Y': 'Y', 'IA': 'IA',
    'EA': 'EA'
}

COMMON_WORDS = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAS',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HIM', 'HIS', 'HOW',
    'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY', 'DID',
    'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'WILL', 'WHAT',
    'WHEN', 'YOUR', 'SOME', 'THEM', 'INTO', 'WHICH', 'THERE', 'THEIR', 'ABOUT',
    'WOULD', 'COULD', 'OTHER', 'THESE', 'FIRST', 'BEING', 'THING', 'THOSE',
    'TRUTH', 'LIGHT', 'WISDOM', 'DIVINE', 'SACRED', 'WITHIN', 'KNOWLEDGE',
    'IS', 'IT', 'AS', 'AT', 'BE', 'WE', 'OR', 'AN', 'NO', 'SO', 'IF', 'MY',
    'UP', 'TO', 'GO', 'ME', 'HE', 'BY', 'IN', 'ON', 'OF', 'DO'
}

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i % 29] for i in indices)

def score_text(text):
    """Score based on English word frequency."""
    score = 0
    text_upper = text.upper()
    
    # Word scoring
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word) * 2
    
    # Bigram scoring
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 
               'NG', 'OF', 'OR', 'TO', 'IT', 'IS', 'OU', 'AR', 'AS', 'AL',
               'TE', 'SE', 'EA', 'TI', 'VE', 'HA', 'WI', 'HI', 'ES', 'ST']
    for bg in bigrams:
        score += text_upper.count(bg) * 0.5
    
    return score

def test_params(args):
    """Test a specific combination of parameters."""
    page_num, rotation, offset, method, indices = args
    
    decrypted = []
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + offset) % len(MASTER_KEY)]
        if method == 'sub':
            dec = (idx - key_val - rotation) % 29
        elif method == 'xor':
            dec = (idx ^ key_val ^ rotation) % 29
        elif method == 'add':
            dec = (idx + key_val + rotation) % 29
        elif method == 'neg_sub':
            dec = (key_val - idx - rotation) % 29
        elif method == 'neg_xor':
            dec = (key_val ^ idx ^ rotation) % 29
        decrypted.append(dec)
    
    text = indices_to_text(decrypted)
    score = score_text(text)
    
    if score > 100:
        return {
            'page': page_num,
            'method': method,
            'rotation': rotation,
            'offset': offset,
            'score': score,
            'text': text[:100]
        }
    return None

def main():
    print("=" * 80)
    print("🚀 ULTIMATE EXHAUSTIVE SINGLE-LAYER SEARCH")
    print("=" * 80)
    print("Testing ALL rotation/offset combinations for each method...")
    print()
    
    start_time = time.time()
    
    all_results = []
    
    methods = ['sub', 'xor', 'add', 'neg_sub', 'neg_xor']
    
    for page_num in [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]:
        indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
        
        print(f"📄 Page {page_num} ({len(indices)} chars)...", end=" ", flush=True)
        
        # Generate all parameter combinations
        params_list = []
        for method in methods:
            for rotation in range(29):
                for offset in range(len(MASTER_KEY)):
                    params_list.append((page_num, rotation, offset, method, indices))
        
        # Process (single-threaded for simplicity)
        page_results = []
        for params in params_list:
            result = test_params(params)
            if result:
                page_results.append(result)
        
        if page_results:
            page_results.sort(key=lambda x: x['score'], reverse=True)
            best = page_results[0]
            print(f"Best: {best['score']:.1f} ({best['method']} r={best['rotation']} o={best['offset']})")
            all_results.extend(page_results[:10])  # Keep top 10 per page
        else:
            print("No results above 100")
    
    elapsed = time.time() - start_time
    print(f"\n⏱️ Search completed in {elapsed:.1f} seconds")
    
    # Sort all results
    all_results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n" + "=" * 80)
    print("📊 TOP 30 RESULTS (SINGLE-LAYER)")
    print("=" * 80)
    
    for i, r in enumerate(all_results[:30]):
        print(f"\n{i+1}. Page {r['page']} | {r['method']} r={r['rotation']} o={r['offset']} | Score: {r['score']:.1f}")
        print(f"   {r['text'][:80]}...")
    
    # Now test double-layer with the best single-layer results
    print("\n" + "=" * 80)
    print("🔄 TESTING DOUBLE-LAYER ON BEST RESULTS")
    print("=" * 80)
    
    double_results = []
    
    for base in all_results[:20]:  # Take top 20 single-layer results
        page_num = base['page']
        indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
        
        # Apply first layer
        first_layer = []
        for i, idx in enumerate(indices):
            key_val = MASTER_KEY[(i + base['offset']) % len(MASTER_KEY)]
            if base['method'] == 'sub':
                dec = (idx - key_val - base['rotation']) % 29
            elif base['method'] == 'xor':
                dec = (idx ^ key_val ^ base['rotation']) % 29
            elif base['method'] == 'add':
                dec = (idx + key_val + base['rotation']) % 29
            elif base['method'] == 'neg_sub':
                dec = (key_val - idx - base['rotation']) % 29
            elif base['method'] == 'neg_xor':
                dec = (key_val ^ idx ^ base['rotation']) % 29
            first_layer.append(dec)
        
        # Try second layer
        for method2 in ['sub', 'xor', 'add']:
            for rot2 in range(0, 29, 2):  # Step by 2
                for off2 in range(0, len(MASTER_KEY), 5):  # Step by 5
                    decrypted = []
                    for i, idx in enumerate(first_layer):
                        key_val = MASTER_KEY[(i + off2) % len(MASTER_KEY)]
                        if method2 == 'sub':
                            dec = (idx - key_val - rot2) % 29
                        elif method2 == 'xor':
                            dec = (idx ^ key_val ^ rot2) % 29
                        elif method2 == 'add':
                            dec = (idx + key_val + rot2) % 29
                        decrypted.append(dec)
                    
                    text = indices_to_text(decrypted)
                    score = score_text(text)
                    
                    if score > 150:
                        double_results.append({
                            'page': page_num,
                            'method1': base['method'],
                            'rot1': base['rotation'],
                            'off1': base['offset'],
                            'method2': method2,
                            'rot2': rot2,
                            'off2': off2,
                            'score': score,
                            'text': text[:100]
                        })
    
    if double_results:
        double_results.sort(key=lambda x: x['score'], reverse=True)
        print(f"\nFound {len(double_results)} double-layer results above 150:")
        for i, r in enumerate(double_results[:20]):
            print(f"\n{i+1}. Page {r['page']} | {r['method1']}→{r['method2']} | Score: {r['score']:.1f}")
            print(f"   r1={r['rot1']} o1={r['off1']} r2={r['rot2']} o2={r['off2']}")
            print(f"   {r['text'][:70]}...")
    else:
        print("\nNo double-layer results above 150")
    
    print("\n✅ Ultimate search complete!")

if __name__ == "__main__":
    main()

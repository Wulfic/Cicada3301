#!/usr/bin/env python3
"""
EXHAUSTIVE DOUBLE XOR - Fine-grained search on best pages.
Page 28 showed 45% word coverage with double XOR.
"""

import time
from collections import Counter

# =============================================================================
# CONSTANTS
# =============================================================================
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
         'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
NUM_RUNES = 29

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

PAGES = {
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# Extended word list for scoring
WORDS = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'WAS', 'ONE',
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
    'THERE', 'THEIR', 'ABOUT', 'WOULD', 'THESE', 'OTHER', 'COULD', 'WRITE',
    'WHICH', 'SHALL', 'BEING', 'THING', 'THINK', 'WHERE', 'RIGHT', 'GREAT',
    'AN', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 'ME', 'MY',
    'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE', 'HIS', 'HER', 'HAD',
    'SAY', 'DID', 'HIM', 'HAS', 'WHO', 'MAY', 'ITS', 'OUR', 'OUT', 'NOW', 'OLD',
    'READ', 'HERE', 'KNOW', 'TAKE', 'COME', 'MADE', 'FIND', 'ONLY', 'INTO',
    # Cicada-relevant
    'WISDOM', 'TRUTH', 'LIGHT', 'SEEK', 'SELF', 'PATH', 'WORD',
]

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i] for i in indices)

def decrypt_xor(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = ((idx - offset) ^ key_val) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_sub(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def score_text(text):
    """Score by word matches."""
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word) * 3
    # Digraph bonus
    for dg in ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE', 'ED', 'ND', 'HA', 'AT', 'EN', 'EA', 'NG', 'OF']:
        score += text.count(dg) * 0.5
    return score

def word_coverage(text):
    """Calculate what percentage of text can be covered by words."""
    covered = set()
    for word in WORDS:
        idx = 0
        while idx < len(text):
            pos = text.find(word, idx)
            if pos == -1:
                break
            for i in range(pos, pos + len(word)):
                covered.add(i)
            idx = pos + 1
    return len(covered) / len(text) * 100 if text else 0

# =============================================================================
# EXHAUSTIVE SEARCH
# =============================================================================

def exhaustive_double_xor(page_num, indices, step1=3, step2=3):
    """Exhaustive double XOR search."""
    best_results = []
    total = (95 // step1) * 29 * (95 // step2) * 29
    tested = 0
    
    for rot1 in range(0, 95, step1):
        for off1 in range(29):
            dec1 = decrypt_xor(indices, rot1, off1)
            
            for rot2 in range(0, 95, step2):
                for off2 in range(29):
                    dec2 = decrypt_xor(dec1, rot2, off2)
                    text = indices_to_text(dec2)
                    score = score_text(text)
                    
                    tested += 1
                    
                    if score >= 100:
                        coverage = word_coverage(text)
                        best_results.append({
                            'rot1': rot1, 'off1': off1,
                            'rot2': rot2, 'off2': off2,
                            'score': score,
                            'coverage': coverage,
                            'text': text
                        })
    
    return best_results

def exhaustive_xor_sub(page_num, indices, step1=3, step2=3):
    """Exhaustive XOR then SUB search."""
    best_results = []
    
    for rot1 in range(0, 95, step1):
        for off1 in range(29):
            dec1 = decrypt_xor(indices, rot1, off1)
            
            for rot2 in range(0, 95, step2):
                for off2 in range(29):
                    dec2 = decrypt_sub(dec1, rot2, off2)
                    text = indices_to_text(dec2)
                    score = score_text(text)
                    
                    if score >= 100:
                        coverage = word_coverage(text)
                        best_results.append({
                            'method': 'xor_sub',
                            'rot1': rot1, 'off1': off1,
                            'rot2': rot2, 'off2': off2,
                            'score': score,
                            'coverage': coverage,
                            'text': text
                        })
    
    return best_results

def fine_tune_around_best(page_num, indices, base_rot1, base_off1, base_rot2, base_off2):
    """Fine-tune with step 1 around the best result."""
    best_results = []
    
    for rot1 in range(max(0, base_rot1 - 3), min(95, base_rot1 + 4)):
        for off1 in range(29):
            dec1 = decrypt_xor(indices, rot1, off1)
            
            for rot2 in range(max(0, base_rot2 - 3), min(95, base_rot2 + 4)):
                for off2 in range(29):
                    dec2 = decrypt_xor(dec1, rot2, off2)
                    text = indices_to_text(dec2)
                    score = score_text(text)
                    coverage = word_coverage(text)
                    
                    if score >= 100 or coverage >= 40:
                        best_results.append({
                            'rot1': rot1, 'off1': off1,
                            'rot2': rot2, 'off2': off2,
                            'score': score,
                            'coverage': coverage,
                            'text': text
                        })
    
    return best_results

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔥 EXHAUSTIVE DOUBLE XOR SEARCH")
    print("=" * 80)
    
    for page_num, page_text in PAGES.items():
        indices = unicode_to_indices(page_text)
        
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}")
        print("="*60)
        
        # Phase 1: Coarse search
        print("\n📊 Phase 1: Coarse double XOR (step=3)...")
        start = time.time()
        results = exhaustive_double_xor(page_num, indices, step1=3, step2=3)
        print(f"  Found {len(results)} results (score >= 100) in {time.time()-start:.1f}s")
        
        if results:
            # Sort by coverage
            results.sort(key=lambda x: -x['coverage'])
            best = results[0]
            
            print(f"\n  Best by coverage:")
            print(f"    Params: rot1={best['rot1']}, off1={best['off1']}, rot2={best['rot2']}, off2={best['off2']}")
            print(f"    Score: {best['score']:.1f}, Coverage: {best['coverage']:.1f}%")
            print(f"    Text: {best['text'][:100]}")
            
            # Phase 2: Fine-tune around best
            print(f"\n📊 Phase 2: Fine-tuning around best (step=1)...")
            start = time.time()
            fine_results = fine_tune_around_best(
                page_num, indices, 
                best['rot1'], best['off1'], 
                best['rot2'], best['off2']
            )
            print(f"  Found {len(fine_results)} results in {time.time()-start:.1f}s")
            
            if fine_results:
                fine_results.sort(key=lambda x: -x['coverage'])
                best_fine = fine_results[0]
                
                print(f"\n  Best after fine-tuning:")
                print(f"    Params: rot1={best_fine['rot1']}, off1={best_fine['off1']}, rot2={best_fine['rot2']}, off2={best_fine['off2']}")
                print(f"    Score: {best_fine['score']:.1f}, Coverage: {best_fine['coverage']:.1f}%")
                print(f"    Text: {best_fine['text']}")
        
        # Also try XOR → SUB
        print("\n📊 Phase 3: XOR → SUB (step=5)...")
        start = time.time()
        results = exhaustive_xor_sub(page_num, indices, step1=5, step2=5)
        print(f"  Found {len(results)} results in {time.time()-start:.1f}s")
        
        if results:
            results.sort(key=lambda x: -x['coverage'])
            best = results[0]
            print(f"\n  Best XOR→SUB:")
            print(f"    Params: rot1={best['rot1']}, off1={best['off1']}, rot2={best['rot2']}, off2={best['off2']}")
            print(f"    Score: {best['score']:.1f}, Coverage: {best['coverage']:.1f}%")
            print(f"    Text: {best['text'][:100]}")
    
    print("\n" + "=" * 80)
    print("🎯 EXHAUSTIVE SEARCH COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

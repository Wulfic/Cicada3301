#!/usr/bin/env python3
"""
Test Caesar shifts on the acrostic and every-7th-rune extractions
"""

import os
from collections import Counter
import re

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
                'THERE', 'WHAT', 'ABOUT', 'WHEN', 'MAKE', 'LIKE', 'TIME', 'JUST',
                'KNOW', 'TAKE', 'PEOPLE', 'INTO', 'YEAR', 'YOUR', 'GOOD', 'SOME',
                'COULD', 'THEM', 'SEE', 'OTHER', 'THAN', 'THEN', 'NOW', 'LOOK'}

def load_page_content(page_num):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_file = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if not os.path.exists(rune_file):
        return None, None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    runes = [c for c in content if c in RUNE_TO_INDEX]
    return content, runes

def shift_indices(indices, shift):
    """Apply Caesar shift to indices"""
    return [(idx - shift) % 29 for idx in indices]

def indices_to_text(indices):
    return ''.join([INDEX_TO_LETTER[idx] for idx in indices])

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        count = text.count(word)
        score += len(word) * 10 * count
    return score

def main():
    print("=" * 70)
    print("CAESAR SHIFT ANALYSIS ON EXTRACTED PATTERNS")
    print("=" * 70)
    
    # Load page 18
    content, runes = load_page_content(18)
    if not runes:
        print("Could not load page 18")
        return
    
    # Get acrostic (first letter of each word)
    words = re.split(r'[-.\s•&§\n]+', content)
    acrostic_indices = []
    for word in words:
        word_runes = [c for c in word if c in RUNE_TO_INDEX]
        if word_runes:
            acrostic_indices.append(RUNE_TO_INDEX[word_runes[0]])
    
    # Get every 7th rune
    seventh_indices = [RUNE_TO_INDEX[runes[i]] for i in range(0, len(runes), 7)]
    
    print(f"\nPage 18 Acrostic: {len(acrostic_indices)} chars")
    print(f"Original: {indices_to_text(acrostic_indices)}")
    
    print("\n" + "=" * 70)
    print("CAESAR SHIFTS ON ACROSTIC")
    print("=" * 70)
    
    best_acrostic = (0, 0, "")
    for shift in range(29):
        shifted = shift_indices(acrostic_indices, shift)
        text = indices_to_text(shifted)
        score = score_text(text)
        if score > best_acrostic[1]:
            best_acrostic = (shift, score, text)
        if score > 0 or shift < 5:
            print(f"Shift {shift:2}: Score={score:3} | {text[:60]}")
    
    print(f"\nBest acrostic: Shift={best_acrostic[0]}, Score={best_acrostic[1]}")
    print(f"Text: {best_acrostic[2]}")
    
    print("\n" + "=" * 70)
    print("CAESAR SHIFTS ON EVERY 7TH RUNE")
    print("=" * 70)
    
    print(f"\nEvery 7th rune: {len(seventh_indices)} chars")
    print(f"Original: {indices_to_text(seventh_indices)}")
    
    best_seventh = (0, 0, "")
    for shift in range(29):
        shifted = shift_indices(seventh_indices, shift)
        text = indices_to_text(shifted)
        score = score_text(text)
        if score > best_seventh[1]:
            best_seventh = (shift, score, text)
        if score > 0 or shift < 5:
            print(f"Shift {shift:2}: Score={score:3} | {text[:60]}")
    
    print(f"\nBest 7th: Shift={best_seventh[0]}, Score={best_seventh[1]}")
    print(f"Text: {best_seventh[2]}")
    
    print("\n" + "=" * 70)
    print("ALL PAGES COMBINED - ACROSTIC WITH SHIFTS")
    print("=" * 70)
    
    # Load all pages
    all_acrostic = []
    for page_num in range(18, 55):
        content, runes = load_page_content(page_num)
        if runes:
            words = re.split(r'[-.\s•&§\n]+', content)
            for word in words:
                word_runes = [c for c in word if c in RUNE_TO_INDEX]
                if word_runes:
                    all_acrostic.append(RUNE_TO_INDEX[word_runes[0]])
    
    print(f"\nTotal acrostic: {len(all_acrostic)} chars")
    
    best_all = (0, 0, "")
    for shift in range(29):
        shifted = shift_indices(all_acrostic, shift)
        text = indices_to_text(shifted)
        score = score_text(text)
        if score > best_all[1]:
            best_all = (shift, score, text[:200])
        print(f"Shift {shift:2}: Score={score:4} | {text[:60]}")
    
    print(f"\nBest overall: Shift={best_all[0]}, Score={best_all[1]}")
    print(f"Text: {best_all[2]}")
    
    print("\n" + "=" * 70)
    print("TESTING ATBASH ON ACROSTIC")
    print("=" * 70)
    
    # Atbash: 0->28, 1->27, etc
    atbash = [28 - idx for idx in all_acrostic]
    text = indices_to_text(atbash)
    score = score_text(text)
    print(f"Atbash: Score={score}")
    print(f"Text: {text[:100]}")
    
    # Atbash + shift
    for shift in range(1, 10):
        shifted = shift_indices(atbash, shift)
        text = indices_to_text(shifted)
        score = score_text(text)
        if score > 0:
            print(f"Atbash + Shift {shift}: Score={score}")
            print(f"  {text[:80]}")

if __name__ == '__main__':
    main()

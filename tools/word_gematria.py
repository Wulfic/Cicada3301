#!/usr/bin/env python3
"""
WORD-BASED ANALYSIS WITH ORIGINAL BOUNDARIES
=============================================

Using the original text format with word separators.
"Numbers are the direction" - Gematria values may determine word reading order.
"""

import re
from pathlib import Path
import numpy as np

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def word_score(text):
    score = 0
    words = {
        'THE': 9, 'AND': 9, 'THAT': 12, 'HAVE': 12, 'FOR': 9, 'NOT': 9, 'WITH': 12, 'THIS': 12,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
        'BEING': 15, 'SELF': 12, 'SOUL': 12, 'YOU': 9, 'YOUR': 12, 'MIND': 12, 'KNOW': 12,
        'ONE': 9, 'ALL': 9, 'WAY': 9, 'ING': 6, 'TION': 9, 'THERE': 15, 'THEIR': 15, 'THEY': 12,
        'FROM': 12, 'WHICH': 15, 'WOULD': 15, 'WHEN': 12, 'WHAT': 12, 'WERE': 12, 'THEN': 12,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

def parse_pages_with_words():
    """Parse pages keeping word boundaries"""
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\2014\Liber Primus\runes in text format.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by page boundaries (% or $)
    pages = {}
    current_lines = []
    page_num = 0
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line in ['%', '$', '&']:
            if current_lines:
                # Parse page content
                page_content = ' '.join(current_lines)
                # Split by - and clean
                words = [w.strip() for w in page_content.replace('/', ' ').split('-') if w.strip()]
                # Keep only words with runes
                rune_words = []
                for w in words:
                    runes_only = ''.join(c for c in w if c in RUNE_TO_IDX)
                    if runes_only:
                        rune_words.append(runes_only)
                if rune_words:
                    pages[page_num] = rune_words
                current_lines = []
                page_num += 1
        else:
            # Remove line ending markers
            line = line.replace('/', '').strip()
            if line:
                current_lines.append(line)
    
    # Don't forget last page
    if current_lines:
        page_content = ' '.join(current_lines)
        words = [w.strip() for w in page_content.replace('/', ' ').split('-') if w.strip()]
        rune_words = []
        for w in words:
            runes_only = ''.join(c for c in w if c in RUNE_TO_IDX)
            if runes_only:
                rune_words.append(runes_only)
        if rune_words:
            pages[page_num] = rune_words
    
    return pages

def main():
    pages_with_words = parse_pages_with_words()
    
    print("="*70)
    print("WORD-BASED GEMATRIA ANALYSIS")
    print("="*70)
    
    # Map raw page indices to actual page numbers 
    # The unsolved pages based on research are approximately:
    # 27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52
    
    # First, let's find pages with similar word counts/structures
    print("\n--- Page Word Counts ---")
    for pg_num in sorted(pages_with_words.keys())[:30]:
        words = pages_with_words[pg_num]
        total_runes = sum(len(w) for w in words)
        print(f"Page {pg_num}: {len(words)} words, {total_runes} runes")
    
    # Now test word reordering by Gematria
    print("\n" + "="*70)
    print("TESTING WORD REORDERING BY GEMATRIA")
    print("="*70)
    
    best_results = []
    
    # Test on pages with significant content (adjust indices based on mapping)
    test_pages = list(range(10, 35))  # Test a range of pages
    
    for pg_idx in test_pages:
        if pg_idx not in pages_with_words:
            continue
            
        words = pages_with_words[pg_idx]
        if len(words) < 10:
            continue
        
        # Calculate Gematria sum for each word
        word_data = []
        for i, word in enumerate(words):
            indices = runes_to_indices(word)
            gem_sum = sum(GEMATRIA[idx] for idx in indices)
            word_data.append((i, word, gem_sum))
        
        # METHOD 1: Sort by Gematria sum (ascending)
        sorted_words = sorted(word_data, key=lambda x: x[2])
        reordered_runes = ''.join(w[1] for w in sorted_words)
        idx = runes_to_indices(reordered_runes)
        n = len(idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 120:
            best_results.append((score, pg_idx, "Gematria ASC + key", text[:60]))
        
        # METHOD 2: Sort by Gematria sum (descending)
        sorted_words = sorted(word_data, key=lambda x: -x[2])
        reordered_runes = ''.join(w[1] for w in sorted_words)
        idx = runes_to_indices(reordered_runes)
        n = len(idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 120:
            best_results.append((score, pg_idx, "Gematria DESC + key", text[:60]))
        
        # METHOD 3: Sort by Gematria sum mod 29 (prime wrap)
        sorted_words = sorted(word_data, key=lambda x: x[2] % 29)
        reordered_runes = ''.join(w[1] for w in sorted_words)
        idx = runes_to_indices(reordered_runes)
        n = len(idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 120:
            best_results.append((score, pg_idx, "Gematria mod29 + key", text[:60]))
        
        # METHOD 4: Use first rune Gematria as position
        sorted_words = sorted(word_data, key=lambda x: GEMATRIA[runes_to_indices(x[1])[0]])
        reordered_runes = ''.join(w[1] for w in sorted_words)
        idx = runes_to_indices(reordered_runes)
        n = len(idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 120:
            best_results.append((score, pg_idx, "First rune Gematria + key", text[:60]))
        
        # METHOD 5: Sort by word length
        sorted_words = sorted(word_data, key=lambda x: len(x[1]))
        reordered_runes = ''.join(w[1] for w in sorted_words)
        idx = runes_to_indices(reordered_runes)
        n = len(idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 120:
            best_results.append((score, pg_idx, "Word length ASC + key", text[:60]))
    
    # Test word-level decryption (apply key to each word separately)
    print("\n" + "="*70)
    print("WORD-LEVEL DECRYPTION (key per word)")
    print("="*70)
    
    for pg_idx in test_pages:
        if pg_idx not in pages_with_words:
            continue
            
        words = pages_with_words[pg_idx]
        if len(words) < 10:
            continue
        
        # Apply key to each word, using word position to offset key
        decrypted_words = []
        key_offset = 0
        
        for word in words:
            idx = runes_to_indices(word)
            n = len(idx)
            # Use word's Gematria sum as key offset
            word_gem_sum = sum(GEMATRIA[i] for i in idx)
            offset = word_gem_sum % 95  # Offset into master key
            key_slice = np.roll(MASTER_KEY, -offset)[:n]
            decrypted_idx = (idx - key_slice) % 29
            decrypted_words.append(indices_to_text(decrypted_idx))
        
        text = ''.join(decrypted_words)
        score = word_score(text)
        
        if score >= 100:
            print(f"Page {pg_idx} word-level decrypt: {score}")
            print(f"  {text[:80]}")
            best_results.append((score, pg_idx, "Word-level (Gematria offset)", text[:60]))
    
    # Print best results
    print("\n" + "="*70)
    print("BEST RESULTS")
    print("="*70)
    
    best_results.sort(reverse=True)
    for score, pg, method, text in best_results[:15]:
        print(f"Score {score}: Page {pg} - {method}")
        print(f"  {text}")
    
    # Test interleaving based on Gematria
    print("\n" + "="*70)
    print("INTERLEAVED READING BY GEMATRIA")
    print("="*70)
    
    for pg_idx in test_pages:
        if pg_idx not in pages_with_words:
            continue
            
        words = pages_with_words[pg_idx]
        if len(words) < 10:
            continue
        
        # Split words into two groups by Gematria parity
        even_gem = []
        odd_gem = []
        
        for word in words:
            idx = runes_to_indices(word)
            gem_sum = sum(GEMATRIA[i] for i in idx)
            if gem_sum % 2 == 0:
                even_gem.append(word)
            else:
                odd_gem.append(word)
        
        # Interleave: even first, then odd
        interleaved = even_gem + odd_gem
        reordered_runes = ''.join(interleaved)
        idx = runes_to_indices(reordered_runes)
        n = len(idx)
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score >= 120:
            print(f"Page {pg_idx} even/odd Gematria interleave: {score}")
            print(f"  {text[:80]}")

if __name__ == "__main__":
    main()

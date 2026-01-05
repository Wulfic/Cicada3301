#!/usr/bin/env python3
"""
VISUAL LAYOUT ANALYSIS - Looking at actual page structure
==========================================================

The runes text file shows:
- `-` = word separator
- `/` = line ending
- `%` = page boundary
- `&` = section break
- `$` = chapter/major section break

Let's analyze the VISUAL structure of each unsolved page.
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

def load_raw_pages():
    """Load pages with their original formatting"""
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\2014\Liber Primus\runes in text format.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by page markers (% or $ followed by possible whitespace)
    # Actually let's be smarter - look for page numbers
    pages_raw = {}
    
    lines = content.split('\n')
    current_page = []
    page_num = 0
    
    for line in lines:
        if '%' in line or '$' in line:
            if current_page:
                pages_raw[page_num] = '\n'.join(current_page)
                current_page = []
                page_num += 1
        current_page.append(line)
    
    if current_page:
        pages_raw[page_num] = '\n'.join(current_page)
    
    return pages_raw

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
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

def analyze_page_structure(raw_text):
    """Analyze the visual structure of a page"""
    lines = [l for l in raw_text.split('\n') if l.strip()]
    
    # Count runes per line (excluding markers)
    line_rune_counts = []
    line_word_counts = []
    
    for line in lines:
        runes_only = ''.join(c for c in line if c in RUNE_TO_IDX)
        words = line.split('-')
        line_rune_counts.append(len(runes_only))
        line_word_counts.append(len([w for w in words if w.strip()]))
    
    return {
        'lines': len(lines),
        'rune_counts': line_rune_counts,
        'word_counts': line_word_counts,
        'total_runes': sum(line_rune_counts),
        'total_words': sum(line_word_counts)
    }

def main():
    # Load the raw format to see visual structure
    raw_pages = load_raw_pages()
    
    print("="*70)
    print("VISUAL PAGE STRUCTURE ANALYSIS")
    print("="*70)
    
    # Focus on unsolved pages (adjusted indices based on raw parsing)
    for pg_num in range(min(40, len(raw_pages))):
        if pg_num not in raw_pages:
            continue
            
        raw = raw_pages[pg_num]
        structure = analyze_page_structure(raw)
        
        # Only show pages with significant content
        if structure['total_runes'] > 100:
            print(f"\n--- Raw Page Index {pg_num} ---")
            print(f"Lines: {structure['lines']}")
            print(f"Total runes: {structure['total_runes']}")
            print(f"Runes per line: {structure['rune_counts'][:10]}...")
            
            # Check if consistent line width
            if structure['rune_counts']:
                avg = np.mean(structure['rune_counts'])
                std = np.std(structure['rune_counts'])
                print(f"Avg runes/line: {avg:.1f} ± {std:.1f}")
    
    # Now load from RuneSolver to get mapped page numbers
    print("\n" + "="*70)
    print("LOADING FROM RUNESOLVER FOR CORRECT PAGE MAPPING")
    print("="*70)
    
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        pages[page_num] = page_text  # Keep original with spaces/separators
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
            
        raw = pages[pg_num]
        runes_only = ''.join(c for c in raw if c in RUNE_TO_IDX)
        
        # Try to find word boundaries
        words = raw.split(' ')
        word_lens = [len(''.join(c for c in w if c in RUNE_TO_IDX)) for w in words if w]
        
        print(f"\nPage {pg_num}:")
        print(f"  Total runes: {len(runes_only)}")
        print(f"  Words: {len(word_lens)}")
        if word_lens:
            print(f"  Word lengths: {word_lens[:20]}...")
            print(f"  Avg word len: {np.mean(word_lens):.1f}")
    
    # Test reading by WORD boundaries
    print("\n" + "="*70)
    print("READING BY WORD GEMATRIA")
    print("="*70)
    
    for pg_num in [27, 30, 31]:
        if pg_num not in pages:
            continue
            
        raw = pages[pg_num]
        words = [w for w in raw.split(' ') if w.strip()]
        
        # Calculate Gematria sum for each word
        word_data = []
        for i, word in enumerate(words):
            runes_only = ''.join(c for c in word if c in RUNE_TO_IDX)
            if runes_only:
                indices = runes_to_indices(runes_only)
                gem_sum = sum(GEMATRIA[idx] for idx in indices)
                word_data.append((i, word, len(runes_only), gem_sum, runes_only))
        
        # Sort words by Gematria sum
        sorted_by_gem = sorted(word_data, key=lambda x: x[3])
        
        # Read in Gematria order
        reordered_runes = ''.join(w[4] for w in sorted_by_gem)
        reordered_idx = runes_to_indices(reordered_runes)
        n = len(reordered_idx)
        
        # Apply master key
        key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
        decrypted = (reordered_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"\nPage {pg_num} - Words sorted by Gematria sum + key: {score}")
        print(f"  {text[:80]}")
        
        # Reverse sort (high to low)
        sorted_by_gem_rev = sorted(word_data, key=lambda x: -x[3])
        reordered_runes = ''.join(w[4] for w in sorted_by_gem_rev)
        reordered_idx = runes_to_indices(reordered_runes)
        decrypted = (reordered_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} - Words sorted by Gematria (DESC) + key: {score}")
        print(f"  {text[:80]}")
        
        # Sort by word position's Gematria value
        # "Numbers are the direction" - position determined by first rune's Gematria
        sorted_by_first = sorted(word_data, key=lambda x: GEMATRIA[runes_to_indices(x[4])[0]] if x[4] else 0)
        reordered_runes = ''.join(w[4] for w in sorted_by_first)
        reordered_idx = runes_to_indices(reordered_runes)
        decrypted = (reordered_idx - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} - Words sorted by first rune Gematria + key: {score}")
        print(f"  {text[:80]}")

    # Test reading every Nth word
    print("\n" + "="*70)
    print("SKIP READING (every Nth word)")
    print("="*70)
    
    for pg_num in [27, 30]:
        if pg_num not in pages:
            continue
            
        raw = pages[pg_num]
        words = [w for w in raw.split(' ') if w.strip()]
        
        for skip in [2, 3, 5, 7, 11, 13]:
            # Read every skip-th word
            selected = words[::skip]
            reordered_runes = ''.join(''.join(c for c in w if c in RUNE_TO_IDX) for w in selected)
            if len(reordered_runes) < 30:
                continue
                
            reordered_idx = runes_to_indices(reordered_runes)
            n = len(reordered_idx)
            key_ext = np.tile(MASTER_KEY, (n // 95 + 1))[:n]
            decrypted = (reordered_idx - key_ext) % 29
            text = indices_to_text(decrypted)
            score = word_score(text)
            
            if score >= 30:
                print(f"Page {pg_num} skip={skip}: {score} | {text[:50]}")

if __name__ == "__main__":
    main()

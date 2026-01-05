#!/usr/bin/env python3
"""
KNOWN PLAINTEXT ATTACK - USING SOLVED PAGES
=============================================

We know the plaintext of Pages 0 and 54 ("An End" and "Parable").
Let's use these patterns to find the correct cipher for unsolved pages.
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Known Anglo-Saxon rune texts (from Cicada lore)
KNOWN_TEXTS = {
    # From solved pages - the "Parable" starts with these words
    'PARABLE': 'DIVINITY IS NOT WISDOM AND WISDOM IS NOT INTELLIGENCE BUT THE SURFACE CIRCUMFERENCE',
    'INSTAR': 'LIKE THE INSTAR EMERGENCE',
    'SHED': 'SHED THEIR SKIN TO EMERGE',
}

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

def text_to_indices(text):
    """Convert uppercase text to rune indices"""
    result = []
    i = 0
    while i < len(text):
        matched = False
        for length in [2, 1]:  # Try 2-char letters first (TH, NG, etc.)
            if i + length <= len(text):
                substr = text[i:i+length]
                if substr in LETTER_TO_IDX:
                    result.append(LETTER_TO_IDX[substr])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1  # Skip spaces and unknown chars
    return np.array(result, dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

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
            pages[page_num] = runes_only
    return pages

def word_score(text):
    score = 0
    words = {
        'THE': 9, 'AND': 9, 'THAT': 12, 'HAVE': 12, 'FOR': 9, 'NOT': 9, 'WITH': 12, 'THIS': 12,
        'AN': 6, 'BE': 6, 'IT': 6, 'IS': 6, 'TO': 6, 'OF': 6, 'IN': 6, 'HE': 6, 'WE': 6, 'OR': 6,
        'AS': 6, 'AT': 6, 'BY': 6, 'IF': 6, 'NO': 6, 'SO': 6, 'ON': 6, 'UP': 6, 'MY': 6, 'DO': 6,
        'INSTAR': 18, 'PARABLE': 21, 'DIVINITY': 24, 'EMERGE': 18, 'CIRCUMFERENCE': 39,
        'WITHIN': 18, 'SURFACE': 21, 'SHED': 12, 'PRIME': 15, 'TRUTH': 15, 'WISDOM': 18,
        'FROM': 12, 'ARE': 9, 'BUT': 9, 'ONE': 9, 'ALL': 9, 'OUT': 9, 'THEIR': 15, 'THEY': 12,
    }
    for word, pts in words.items():
        score += text.count(word) * pts
    return score

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

def main():
    print("="*70)
    print("KNOWN PLAINTEXT ATTACK")
    print("="*70)
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Convert known texts to indices
    print("\nKnown text patterns (as rune indices):")
    for name, text in KNOWN_TEXTS.items():
        clean = text.replace(' ', '')
        indices = text_to_indices(clean)
        print(f"{name}: {clean[:40]}... → {list(indices[:15])}...")
    
    # Try to find where these patterns might match in the ciphertext
    # using the master key at various offsets
    
    print("\n" + "="*70)
    print("TESTING IF KNOWN TEXTS MATCH MASTER KEY DECRYPTION")
    print("="*70)
    
    # Take the first 20 chars of PARABLE as a crib
    parable_start = 'DIVINITYISNOTWISDOMANDWISDOMISNOTINTELLIGENCE'
    crib = text_to_indices(parable_start)
    print(f"\nCrib (Parable start): {parable_start[:40]}")
    print(f"As indices: {list(crib[:20])}")
    
    # For each unsolved page, check if there's an offset where
    # applying the master key gives something close to our crib
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        for offset in range(len(MASTER_KEY)):
            key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
            
            # Try Vigenère decryption
            dec = (pg_idx - key) % 29
            text = indices_to_text(dec)
            
            # Check for key phrases
            if 'DIVINITY' in text or 'WISDOM' in text or 'INTELLIGENCE' in text:
                print(f"\n*** Page {pg_num} offset={offset} contains key phrase! ***")
                print(f"    {text[:80]}")
            
            # XOR
            dec = (pg_idx ^ key) % 29
            text = indices_to_text(dec)
            
            if 'DIVINITY' in text or 'WISDOM' in text or 'INTELLIGENCE' in text:
                print(f"\n*** Page {pg_num} offset={offset} (XOR) contains key phrase! ***")
                print(f"    {text[:80]}")
    
    # Also try with common phrase patterns
    print("\n" + "="*70)
    print("SEARCHING FOR COMMON PHRASE PATTERNS")
    print("="*70)
    
    phrases = ['BEHOLD', 'WITHIN', 'THROUGH', 'BETWEEN', 'BENEATH', 'BEYOND']
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        best_matches = []
        
        for offset in range(len(MASTER_KEY)):
            key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
            
            for method in ['vig', 'xor']:
                if method == 'vig':
                    dec = (pg_idx - key) % 29
                else:
                    dec = (pg_idx ^ key) % 29
                
                text = indices_to_text(dec)
                
                for phrase in phrases:
                    if phrase in text:
                        best_matches.append((offset, method, phrase, text[:80]))
        
        if best_matches:
            print(f"\nPage {pg_num}:")
            for offset, method, phrase, text in best_matches:
                print(f"  offset={offset:2d} {method}: found '{phrase}' → {text}")
    
    # Try raw decryption (no transposition) with just Vigenère at different offsets
    print("\n" + "="*70)
    print("STRAIGHT VIGENÈRE (NO TRANSPOSITION)")
    print("="*70)
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        n = len(pg_idx)
        
        best = (0, 0, "")
        
        for offset in range(len(MASTER_KEY)):
            key = np.tile(np.roll(MASTER_KEY, -offset), (n // len(MASTER_KEY) + 1))[:n]
            dec = (pg_idx - key) % 29
            text = indices_to_text(dec)
            score = word_score(text)
            
            if score > best[0]:
                best = (score, offset, text)
        
        print(f"Page {pg_num}: best offset={best[1]:2d} | Score: {best[0]}")
        print(f"  {best[2][:80]}")

if __name__ == "__main__":
    main()

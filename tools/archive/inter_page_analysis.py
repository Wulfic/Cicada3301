#!/usr/bin/env python3
"""
INTER-PAGE RELATIONSHIP ANALYSIS

We know: Page0 - Page57 = Master Key
This was the breakthrough for deriving the key.

What if other pages have similar relationships?
- Page N - Page M = Key for something?
- Page N XOR Page M = Something?

Let's systematically look at inter-page relationships.
"""

import re
from pathlib import Path
import numpy as np

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def pages_to_indices(page_runes):
    return [rune_to_idx(r) for r in page_runes]

def word_score(text):
    WORDS = {'THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 
             'ARE', 'FOR', 'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE',
             'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST', 'SURFACE', 'TUNNEL', 
             'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME', 'NOT', 'END', 'SEEK', 
             'FIND', 'YOU', 'YOUR', 'WAY', 'PATH', 'LIGHT', 'SELF', 'WILL', 'CAN',
             'SACRED', 'TRUTH', 'WISDOM', 'KNOWLEDGE', 'BEING', 'ALL'}
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word)
    return score

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("INTER-PAGE RELATIONSHIP ANALYSIS")
    print("=" * 70)
    
    # Get all page lengths
    print("\nPage lengths:")
    for pg in sorted(pages.keys())[:20]:
        print(f"  Page {pg}: {len(pages[pg])} runes")
    
    # Look for pages with matching lengths
    print("\n" + "=" * 70)
    print("PAGES WITH MATCHING LENGTHS")
    print("=" * 70)
    
    length_groups = {}
    for pg_num, runes in pages.items():
        n = len(runes)
        if n not in length_groups:
            length_groups[n] = []
        length_groups[n].append(pg_num)
    
    for length, pgs in sorted(length_groups.items()):
        if len(pgs) > 1:
            print(f"  Length {length}: Pages {pgs}")
    
    # The master key derivation: Page0 - Page57 (mod 29)
    print("\n" + "=" * 70)
    print("VERIFYING PAGE 0 - PAGE 57 = MASTER KEY")
    print("=" * 70)
    
    p0 = pages_to_indices(pages[0])
    p57 = pages_to_indices(pages[57])
    
    # Compute difference
    min_len = min(len(p0), len(p57))
    diff = [(p0[i] - p57[i]) % 29 for i in range(min_len)]
    print(f"Page 0 length: {len(p0)}")
    print(f"Page 57 length: {len(p57)}")
    print(f"Difference (first 20): {diff[:20]}")
    print(f"Sum of difference: {sum(diff)}")
    
    # Try using this difference as key to decrypt other pages
    key = diff
    
    print("\n" + "=" * 70)
    print("USING (Page0 - Page57) AS KEY FOR OTHER PAGES")
    print("=" * 70)
    
    for pg_num in [27, 28, 29, 30, 31, 40, 41]:
        if pg_num not in pages:
            continue
        
        cipher = pages_to_indices(pages[pg_num])
        
        # Decrypt
        decrypted = []
        for i, c in enumerate(cipher):
            k = key[i % len(key)]
            p = (c - k) % 29
            decrypted.append(idx_to_letter(p))
        
        text = ''.join(decrypted)
        score = word_score(text)
        
        print(f"\nPage {pg_num}: score={score}")
        print(f"  {text[:60]}...")
    
    # What if we use PAGE as the target to decode?
    # Page 27 - Page X = Key → Use Key to decrypt Page Y
    print("\n" + "=" * 70)
    print("TRYING PAGE N - PAGE 57 = KEY FOR PAGE N")
    print("(Like how Page 0 - Page 57 = Key for Page 0)")
    print("=" * 70)
    
    p57_indices = pages_to_indices(pages[57])
    
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        pg_indices = pages_to_indices(pages[pg_num])
        pg_len = len(pg_indices)
        
        # Extend Page 57 by repeating
        p57_extended = [p57_indices[i % len(p57_indices)] for i in range(pg_len)]
        
        # Compute PageN - Page57
        key_n = [(pg_indices[i] - p57_extended[i]) % 29 for i in range(pg_len)]
        
        # Use this key to decrypt PageN itself (should give Page57 text repeated)
        decrypted = []
        for i, c in enumerate(pg_indices):
            k = key_n[i % len(key_n)]
            p = (c - k) % 29
            decrypted.append(idx_to_letter(p))
        
        text = ''.join(decrypted)
        
        # This should just give us the Parable repeated - but what's the KEY itself?
        key_text = ''.join(idx_to_letter(k) for k in key_n[:50])
        
        print(f"\nPage {pg_num}:")
        print(f"  Key (Page{pg_num} - Page57): {key_text}...")
        print(f"  Key sum: {sum(key_n)}")
        print(f"  If used as key for Page{pg_num}: {text[:50]}...")
        
        # Maybe this KEY can decrypt another page?
        for other_pg in [0, 1, 2]:
            if other_pg == pg_num or other_pg not in pages:
                continue
            
            other_indices = pages_to_indices(pages[other_pg])
            decrypted2 = []
            for i, c in enumerate(other_indices):
                k = key_n[i % len(key_n)]
                p = (c - k) % 29
                decrypted2.append(idx_to_letter(p))
            
            t2 = ''.join(decrypted2)
            score2 = word_score(t2)
            if score2 > 50:
                print(f"    Decrypts Page{other_pg}: score={score2}, {t2[:40]}...")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AFFINE KEY TRANSFORMATION - DEEP ANALYSIS

Best results from previous test:
- Page 28: a=5, b=19, offset=47, score=33
- Page 52: a=25, b=12, offset=8, score=36

Let's find the affine parameters for all unsolved pages and look for patterns.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

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

def word_score(text):
    WORDS = {'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
             'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
             'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
             'YOU', 'WE', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
             'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
             'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR',
             'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def decrypt_affine(cipher, a, b, offset):
    """Decrypt using affine-transformed key: key'[i] = (a * key[i] + b) mod 29"""
    affine_key = [(a * k + b) % 29 for k in MASTER_KEY]
    result = []
    for i, c in enumerate(cipher):
        k = affine_key[(i + offset) % 95]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def main():
    pages = load_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("=" * 80)
    print("FINDING BEST AFFINE PARAMETERS FOR ALL UNSOLVED PAGES")
    print("=" * 80)
    
    results = {}
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_config = None
        best_text = ""
        
        for a in range(1, 29):
            for b in range(29):
                for offset in range(95):
                    text = decrypt_affine(cipher, a, b, offset)
                    score = word_score(text)
                    
                    if score > best_score:
                        best_score = score
                        best_config = (a, b, offset)
                        best_text = text
        
        results[pg_num] = (best_config, best_score, best_text)
        a, b, offset = best_config
        
        print(f"Page {pg_num}: a={a:2}, b={b:2}, offset={offset:2}, score={best_score:2}")
        print(f"  Text: {best_text[:80]}...")
        print()
    
    print("\n" + "=" * 80)
    print("PATTERN ANALYSIS")
    print("=" * 80)
    
    # Look for relationships between page number and (a, b, offset)
    print("\nPage | a | b | offset | pg%29 | a*pg%29 | b*pg%29 | a+b | a*b%29")
    print("-" * 75)
    for pg_num, (config, score, _) in sorted(results.items()):
        a, b, offset = config
        print(f"{pg_num:4} | {a:2} | {b:2} | {offset:3}   | {pg_num%29:2}   | {(a*pg_num)%29:2}      | {(b*pg_num)%29:2}      | {a+b:3} | {(a*b)%29:2}")
    
    print("\n" + "=" * 80)
    print("INTERESTING RELATIONSHIPS")
    print("=" * 80)
    
    for pg_num, (config, score, _) in sorted(results.items()):
        a, b, offset = config
        
        # Check various relationships
        relationships = []
        
        # Is a related to page number?
        if a == pg_num % 29:
            relationships.append("a = pg mod 29")
        if a == (29 - pg_num) % 29:
            relationships.append("a = -pg mod 29")
        for mult in range(1, 10):
            if a == (pg_num * mult) % 29:
                relationships.append(f"a = {mult}*pg mod 29")
                break
        
        # Is b related to page number?
        if b == pg_num % 29:
            relationships.append("b = pg mod 29")
        if b == (29 - pg_num) % 29:
            relationships.append("b = -pg mod 29")
        for mult in range(1, 10):
            if b == (pg_num * mult) % 29:
                relationships.append(f"b = {mult}*pg mod 29")
                break
        
        # Is offset related?
        if offset == pg_num:
            relationships.append("offset = pg")
        if offset == pg_num % 95:
            relationships.append("offset = pg mod 95")
        if offset == (95 - pg_num) % 95:
            relationships.append("offset = -pg mod 95")
        
        # Check if a, b are related to each other
        if (a + b) % 29 == pg_num % 29:
            relationships.append("(a+b) mod 29 = pg mod 29")
        if (a * b) % 29 == pg_num % 29:
            relationships.append("(a*b) mod 29 = pg mod 29")
        
        rel_str = ", ".join(relationships) if relationships else "no obvious relationship"
        print(f"Page {pg_num}: {rel_str}")
    
    print("\n" + "=" * 80)
    print("VERIFY: CHECK IF PAGE 0 WORKS WITH a=1, b=0 (IDENTITY)")
    print("=" * 80)
    
    if 0 in pages:
        cipher = [rune_to_idx(r) for r in pages[0][:95]]  # First 95 runes
        for offset in range(10):
            text = decrypt_affine(cipher, 1, 0, offset)
            score = word_score(text)
            if score >= 50:
                print(f"Page 0: a=1, b=0, offset={offset}, score={score}")
                print(f"  {text[:80]}...")
    
    print("\n" + "=" * 80)
    print("BEST CANDIDATES - FULL TEXT")
    print("=" * 80)
    
    # Show full text for highest scoring pages
    sorted_results = sorted(results.items(), key=lambda x: x[1][1], reverse=True)
    for pg_num, (config, score, text) in sorted_results[:3]:
        a, b, offset = config
        print(f"\n=== Page {pg_num}: a={a}, b={b}, offset={offset}, score={score} ===")
        # Print with word boundaries marked
        print(text)

if __name__ == "__main__":
    main()

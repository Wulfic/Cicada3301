#!/usr/bin/env python3
"""
PARABLE AS RUNNING KEY - Page Number as Starting Position

2016 clue: "Its words are the map, their meaning is the road, 
           and their NUMBERS are the direction."

THEORY: 
- The Parable (Page 57) IS the running key
- Each page starts at position (page_number * some_factor) mod 95
- "Numbers are the direction" = the page number determines WHERE in the key to start
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# The Parable as rune indices (the key)
PARABLE = "PARABLELIKETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def letter_to_idx(letter):
    if letter in LETTERS:
        return LETTERS.index(letter)
    return -1

def text_to_key(text):
    """Convert text to key indices (handling digraphs)"""
    key = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            two = text[i:i+2].upper()
            if two in LETTERS:
                key.append(LETTERS.index(two))
                i += 2
                continue
        one = text[i].upper()
        if one in LETTERS:
            key.append(LETTERS.index(one))
        i += 1
    return key

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
    """Enhanced scoring with more English words"""
    WORDS = {'THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 
             'ARE', 'FOR', 'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 
             'BY', 'THEIR', 'ALL', 'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 
             'PARABLE', 'INSTAR', 'LIKE', 'UNTO', 'WISDOM', 'TRUTH', 'KNOWLEDGE', 
             'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST', 'SURFACE', 'TUNNEL', 
             'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME', 'NOT', 'END', 'SEEK', 
             'FIND', 'YOU', 'YOUR', 'WAY', 'PATH', 'LIGHT', 'DARK', 'SELF', 'WILL', 
             'CAN', 'MAY', 'SHALL', 'HAVE', 'HAS', 'HAD', 'BEEN', 'WAS', 'WERE',
             'BEING', 'HAVING', 'DO', 'DOES', 'DID', 'DONE', 'DOING', 'WHEN', 'IF',
             'THEN', 'THAN', 'WHO', 'HOW', 'WHY', 'WHERE', 'FIRST', 'OUR', 'HIS',
             'HER', 'ITS', 'HE', 'SHE', 'HIM', 'US', 'THEM', 'THESE', 'THOSE'}
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word)
    return score

def main():
    pages = load_pages()
    parable_key = text_to_key(PARABLE)
    key_len = len(parable_key)
    
    print("=" * 70)
    print("PARABLE AS RUNNING KEY - PAGE NUMBER AS OFFSET")
    print("=" * 70)
    print(f"Parable key length: {key_len}")
    print(f"Parable key (first 20): {parable_key[:20]}")
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Theory 1: Start position = page_number * multiplier
    print("\n" + "=" * 70)
    print("THEORY 1: offset = (page_number * multiplier) mod key_length")
    print("=" * 70)
    
    for pg_num in unsolved[:5]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        
        print(f"\nPage {pg_num}:")
        best_score = 0
        best_config = None
        
        for mult in range(1, 20):
            offset = (pg_num * mult) % key_len
            
            result = []
            for i, r in enumerate(cipher):
                c_idx = rune_to_idx(r)
                if c_idx < 0:
                    continue
                k = parable_key[(i + offset) % key_len]
                plain_idx = (c_idx - k) % 29
                result.append(idx_to_letter(plain_idx))
            
            text = ''.join(result)
            score = word_score(text)
            if score > best_score:
                best_score = score
                best_config = (mult, offset, text)
        
        if best_config:
            mult, offset, text = best_config
            print(f"  Best: mult={mult}, offset={offset}, score={best_score}")
            print(f"  Text: {text[:55]}...")

    # Theory 2: Start at page prime's position
    print("\n" + "=" * 70)
    print("THEORY 2: offset = prime[page_number] mod key_length")
    print("=" * 70)
    
    for pg_num in unsolved[:5]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        
        if pg_num < len(PRIMES):
            offset = PRIMES[pg_num] % key_len
        else:
            offset = 0
        
        result = []
        for i, r in enumerate(cipher):
            c_idx = rune_to_idx(r)
            if c_idx < 0:
                continue
            k = parable_key[(i + offset) % key_len]
            plain_idx = (c_idx - k) % 29
            result.append(idx_to_letter(plain_idx))
        
        text = ''.join(result)
        score = word_score(text)
        print(f"Page {pg_num}: prime[{pg_num}]={PRIMES[pg_num] if pg_num < len(PRIMES) else 'N/A'}, offset={offset}")
        print(f"  Score: {score}, Text: {text[:55]}...")

    # Theory 3: Brute force all offsets
    print("\n" + "=" * 70)
    print("THEORY 3: Brute force all offsets")
    print("=" * 70)
    
    for pg_num in unsolved[:5]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        
        best_score = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(key_len):
            result = []
            for i, r in enumerate(cipher):
                c_idx = rune_to_idx(r)
                if c_idx < 0:
                    continue
                k = parable_key[(i + offset) % key_len]
                plain_idx = (c_idx - k) % 29
                result.append(idx_to_letter(plain_idx))
            
            text = ''.join(result)
            score = word_score(text)
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = text
        
        print(f"Page {pg_num}: best offset={best_offset}, score={best_score}")
        print(f"  Text: {best_text[:55]}...")

    # Theory 4: Gematria sum of page runes as offset
    print("\n" + "=" * 70)
    print("THEORY 4: offset = sum(cipher_gematria) mod key_length")
    print("=" * 70)
    
    for pg_num in unsolved[:5]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        
        # Sum of gematria values for the page
        gem_sum = sum(PRIMES[rune_to_idx(r)] for r in cipher if rune_to_idx(r) >= 0)
        offset = gem_sum % key_len
        
        result = []
        for i, r in enumerate(cipher):
            c_idx = rune_to_idx(r)
            if c_idx < 0:
                continue
            k = parable_key[(i + offset) % key_len]
            plain_idx = (c_idx - k) % 29
            result.append(idx_to_letter(plain_idx))
        
        text = ''.join(result)
        score = word_score(text)
        print(f"Page {pg_num}: gematria_sum={gem_sum}, offset={offset}")
        print(f"  Score: {score}, Text: {text[:55]}...")

if __name__ == "__main__":
    main()

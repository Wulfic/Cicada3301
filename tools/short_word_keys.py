#!/usr/bin/env python3
"""
TEST SHORTER WORD-BASED KEYS

What if each unsolved page uses a specific Parable WORD as its Vigenère key?
The 2016 clue says "their NUMBERS are the direction" - 
maybe the page number tells us WHICH WORD to use as the key.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# All words from the Parable
PARABLE_WORDS = ["PARABLE", "LIKE", "THE", "INSTAR", "TUNNELNG", "TO", 
                 "SURFACE", "WE", "MUST", "SHED", "OUR", "OWN", 
                 "CIRCUMFERENCES", "FIND", "DIUINITY", "WITHIN", "AND", "EMERGE"]

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def word_to_key(word):
    """Convert a word to a key (list of rune indices)"""
    key = []
    i = 0
    word = word.upper()
    while i < len(word):
        # Try 2-char combinations first (TH, NG, etc.)
        if i + 1 < len(word):
            two = word[i:i+2]
            if two in LETTERS:
                key.append(LETTERS.index(two))
                i += 2
                continue
        # Single char
        one = word[i]
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

def decrypt(cipher_runes, key):
    """Vigenère decrypt with the given key"""
    result = []
    for i, r in enumerate(cipher_runes):
        c_idx = rune_to_idx(r)
        if c_idx < 0:
            continue
        k = key[i % len(key)]
        plain_idx = (c_idx - k) % 29
        result.append(idx_to_letter(plain_idx))
    return ''.join(result)

def word_score(text):
    """Score based on English word detection"""
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST',
             'SURFACE', 'TUNNEL', 'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME', 'NOT', 
             'END', 'SEEK', 'FIND', 'YOU', 'YOUR', 'WAY', 'PATH', 'LIGHT', 'DARK', 'SELF',
             'WILL', 'CAN', 'MAY', 'SHALL', 'HAVE', 'HAS', 'HAD', 'BEEN', 'WAS', 'WERE',
             'BEING', 'HAVING', 'DO', 'DOES', 'DID', 'DONE', 'DOING']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word)
    return score

def main():
    pages = load_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("=" * 70)
    print("TESTING EACH PARABLE WORD AS KEY FOR EACH PAGE")
    print("=" * 70)
    
    # Print word keys for reference
    print("\nParable word keys:")
    for i, word in enumerate(PARABLE_WORDS):
        key = word_to_key(word)
        key_sum = sum(key)
        print(f"  {i:2d}. {word:16s} → key={key}, sum={key_sum}")
    
    print("\n" + "=" * 70)
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        print(f"\nPage {pg_num} ({len(cipher)} runes):")
        
        results = []
        for word in PARABLE_WORDS:
            key = word_to_key(word)
            if not key:
                continue
            decrypted = decrypt(cipher, key)
            score = word_score(decrypted)
            results.append((score, word, decrypted))
        
        # Sort by score, show top 3
        results.sort(reverse=True)
        for score, word, text in results[:3]:
            print(f"  {word:16s}: score={score:3d}, {text[:45]}...")

    print("\n" + "=" * 70)
    print("TRYING GEMATRIA SUM OF WORD AS OFFSET INTO MASTER KEY")
    print("=" * 70)
    
    MASTER_KEY = [
        11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
        20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
        17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
        5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
        14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
    ]
    
    # Theory: Use page number to select word, word's Gematria sum to select key offset
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        word_idx = (pg_num - 20) % len(PARABLE_WORDS)
        word = PARABLE_WORDS[word_idx]
        word_key = word_to_key(word)
        
        # Calculate Gematria sum of the word
        gematria_sum = sum(PRIMES[k] for k in word_key)
        offset = gematria_sum % 95
        
        print(f"\nPage {pg_num}: Word='{word}', Gematria sum={gematria_sum}, offset={offset}")
        
        # Use master key starting at offset
        result = []
        for i, r in enumerate(cipher):
            c_idx = rune_to_idx(r)
            if c_idx < 0:
                continue
            k = MASTER_KEY[(i + offset) % 95]
            plain_idx = (c_idx - k) % 29
            result.append(idx_to_letter(plain_idx))
        
        text = ''.join(result)
        score = word_score(text)
        print(f"  Score: {score}, Text: {text[:55]}...")

    print("\n" + "=" * 70)
    print("TRYING PAGE NUMBER'S PRIME AS OFFSET")
    print("=" * 70)
    
    # Theory: The page number maps to a prime which gives the offset
    for pg_num in [27, 28, 29, 30, 31]:
        if pg_num not in pages:
            continue
        
        cipher = pages[pg_num]
        
        # Page number as prime index
        if pg_num < len(PRIMES):
            page_prime = PRIMES[pg_num]
            offset = page_prime % 95
            
            result = []
            for i, r in enumerate(cipher):
                c_idx = rune_to_idx(r)
                if c_idx < 0:
                    continue
                k = MASTER_KEY[(i + offset) % 95]
                plain_idx = (c_idx - k) % 29
                result.append(idx_to_letter(plain_idx))
            
            text = ''.join(result)
            score = word_score(text)
            print(f"Page {pg_num}: prime[{pg_num}]={page_prime}, offset={offset}, score={score}")
            print(f"  Text: {text[:55]}...")

if __name__ == "__main__":
    main()

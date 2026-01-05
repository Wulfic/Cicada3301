#!/usr/bin/env python3
"""
CHECK ALL SOLVED PAGES

According to the docs, Pages 56 and 57 are solved.
Let's see what other pages might be usable as key sources.
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
             'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN',
             'LIKE', 'TUNNELING', 'CIRCUMFERENCE', 'COMMAND', 'EYES', 'DEAD',
             'STILL', 'SEE', 'REMAIN', 'AWAKE', 'ABANDON', 'SHED', 'SKIN',
             'BEFORE', 'BODY', 'COVERED', 'SOME'}
    score = 0
    for word in WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
    return score

def decrypt_with_key(cipher_indices, key, offset=0):
    """Decrypt cipher using given key with offset"""
    result = []
    key_len = len(key)
    for i, c in enumerate(cipher_indices):
        k = key[(i + offset) % key_len]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def main():
    pages = load_pages()
    
    print("=" * 80)
    print("PAGE 57 (PARABLE) - THE KNOWN PLAINTEXT")
    print("=" * 80)
    
    page57_indices = [rune_to_idx(r) for r in pages[57]]
    page57_text = ''.join(idx_to_letter(idx) for idx in page57_indices)
    print(f"Length: {len(page57_indices)}")
    print(f"Text: {page57_text}")
    
    print("\n" + "=" * 80)
    print("PAGE 56 DECRYPTION (Prime Shift Method)")
    print("=" * 80)
    
    # Page 56 uses -(prime + 57) mod 29 shift
    if 56 in pages:
        cipher = pages[56]
        result = []
        prime_idx = 0
        
        for r in cipher:
            idx = rune_to_idx(r)
            if idx >= 0:
                shift = -(PRIMES[prime_idx] + 57) % 29
                decrypted = (idx + shift) % 29
                result.append(idx_to_letter(decrypted))
                prime_idx = (prime_idx + 1) % len(PRIMES)
        
        text = ''.join(result)
        print(f"Decrypted (prime shift): {text[:150]}...")
    
    print("\n" + "=" * 80)
    print("TRYING EACH SOLVED PAGE AS KEY SOURCE FOR UNSOLVED PAGES")
    print("=" * 80)
    
    # Get potential key source pages (those that might be solved or semi-solved)
    # According to the document, Page 0's first 95 chars decrypt correctly
    
    page0_first95 = [rune_to_idx(r) for r in pages[0][:95]]
    
    # Also try using the raw Page 0 data as a key
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Try different pages as running keys
    potential_keys = {
        'Page57 (Parable)': page57_indices,
        'Page0 first95': page0_first95,
        'Master Key': MASTER_KEY,
    }
    
    for key_name, key in potential_keys.items():
        print(f"\n--- Using {key_name} (len={len(key)}) ---")
        
        for pg_num in unsolved[:4]:  # Test first 4
            if pg_num not in pages:
                continue
            
            cipher = [rune_to_idx(r) for r in pages[pg_num]]
            
            best_score = 0
            best_offset = 0
            best_text = ""
            
            for offset in range(len(key)):
                text = decrypt_with_key(cipher, key, offset)
                score = word_score(text)
                
                if score > best_score:
                    best_score = score
                    best_offset = offset
                    best_text = text[:60]
            
            if best_score >= 10:
                print(f"  Page {pg_num}: offset={best_offset}, score={best_score}")
                print(f"    {best_text}...")
    
    print("\n" + "=" * 80)
    print("CHECKING IF ANY OTHER PAGES MIGHT BE SEMI-SOLVED")
    print("=" * 80)
    
    # Try decrypting each page with master key and check score
    for pg_num in sorted(pages.keys()):
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        best_score = 0
        best_offset = 0
        best_text = ""
        
        for offset in range(95):
            text = decrypt_with_key(cipher, MASTER_KEY, offset)
            score = word_score(text)
            
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = text
        
        # Calculate what fraction of the page matches known words
        if best_score >= 30:  # Threshold for "interesting"
            print(f"Page {pg_num}: offset={best_offset}, score={best_score}")
            print(f"  {best_text[:80]}...")
            
            # Check how many positions of master key match
            ext_key = [MASTER_KEY[(i + best_offset) % 95] for i in range(len(cipher))]
            derived_key = [(cipher[i] - page57_indices[i % 95]) % 29 for i in range(min(95, len(cipher)))]
            matches = sum(1 for i in range(min(95, len(cipher))) if ext_key[i] == derived_key[i])
            print(f"  Key matches: {matches}/95")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
VERIFY PAGE 0 DECRYPTION AND COMPARE TO OTHER PAGES

The test showed Page 0 decrypts perfectly with a=1, b=0.
Let's see the full output and understand why other pages don't work.
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

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

def decrypt_affine(cipher_indices, a, b, offset):
    """Decrypt using affine-transformed key: key'[i] = (a * key[i] + b) mod 29"""
    affine_key = [(a * k + b) % 29 for k in MASTER_KEY]
    result = []
    for i, c in enumerate(cipher_indices):
        k = affine_key[(i + offset) % 95]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def main():
    pages = load_pages()
    
    print("=" * 80)
    print("PAGE 0 FULL DECRYPTION (a=1, b=0, offset=0)")
    print("=" * 80)
    
    cipher = [rune_to_idx(r) for r in pages[0]]
    text = decrypt_affine(cipher, 1, 0, 0)
    
    # Print in chunks of 80
    for i in range(0, len(text), 80):
        print(text[i:i+80])
    
    print(f"\nTotal length: {len(text)} characters")
    
    print("\n" + "=" * 80)
    print("COMPARING KEY DERIVATION METHODS")
    print("=" * 80)
    
    # Key from Page0 - Page57 should equal master key
    page0 = [rune_to_idx(r) for r in pages[0][:95]]
    page57 = [rune_to_idx(r) for r in pages[57]]
    
    derived_key = [(page0[i] - page57[i]) % 29 for i in range(95)]
    
    print("\nDerived key (Page0 - Page57):")
    print(derived_key)
    print("\nMaster key:")
    print(MASTER_KEY)
    print("\nMatch:", derived_key == MASTER_KEY)
    
    print("\n" + "=" * 80)
    print("CHECKING KEY DIFFERENCES FOR UNSOLVED PAGES")
    print("=" * 80)
    
    # For each unsolved page, compute Page_unsolved - Page57 (extended)
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        n = len(cipher)
        
        # Extend page57 to match length
        extended_p57 = [page57[i % 95] for i in range(n)]
        
        # Compute difference
        page_key = [(cipher[i] - extended_p57[i]) % 29 for i in range(n)]
        
        # Extend master key for comparison
        extended_master = [MASTER_KEY[i % 95] for i in range(n)]
        
        # Count matches at each offset
        best_match = 0
        best_offset = 0
        for offset in range(95):
            shifted_master = [MASTER_KEY[(i + offset) % 95] for i in range(n)]
            matches = sum(1 for i in range(n) if page_key[i] == shifted_master[i])
            if matches > best_match:
                best_match = matches
                best_offset = offset
        
        match_pct = best_match / n * 100
        print(f"Page {pg_num}: {n} chars, best key match = {best_match}/{n} ({match_pct:.1f}%) at offset {best_offset}")
        
        # Show the first 30 values of derived key vs master key at best offset
        if pg_num == 28:  # Example page
            shifted = [MASTER_KEY[(i + best_offset) % 95] for i in range(30)]
            print(f"  Page key (first 30): {page_key[:30]}")
            print(f"  Master at offset {best_offset}: {shifted}")
    
    print("\n" + "=" * 80)
    print("HYPOTHESIS: MAYBE THE PARABLE TEXT IS DIFFERENT PER PAGE?")
    print("=" * 80)
    
    # What if unsolved pages aren't encrypted PARABLE, but different text?
    # Let's see what plaintext would make the key match master key
    
    for pg_num in [28]:  # Test one page
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        n = len(cipher)
        
        # If C = P + K, then P = C - K
        # Using master key at different offsets
        for offset in [0, 13]:  # offset 13 was best for word matches
            plaintext_indices = [(cipher[i] - MASTER_KEY[(i + offset) % 95]) % 29 for i in range(n)]
            plaintext = ''.join(idx_to_letter(p) for p in plaintext_indices)
            
            # Compare to parable
            parable_ext = ''.join(idx_to_letter(page57[i % 95]) for i in range(n))
            
            # Count letter matches (not caring about position)
            cipher_text = ''.join(idx_to_letter(c) for c in cipher)
            
            print(f"\nPage {pg_num} at offset {offset}:")
            print(f"  Decrypted: {plaintext[:80]}...")
            print(f"  Parable:   {parable_ext[:80]}...")
            
            # Check if it's an anagram of parable
            from collections import Counter
            plain_counter = Counter(plaintext)
            parable_counter = Counter(parable_ext[:len(plaintext)])
            
            common = sum((plain_counter & parable_counter).values())
            print(f"  Common letters with Parable: {common}/{len(plaintext)}")

if __name__ == "__main__":
    main()

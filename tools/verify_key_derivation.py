#!/usr/bin/env python3
"""
VERIFY KEY DERIVATION
=====================

There's a discrepancy between:
1. The stored MASTER_KEY used in all our analysis
2. The key actually derived from Page0 - Page57

Let's trace this step by step to find the correct key.
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

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

# The stored master key that we've been using
STORED_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def main():
    print("="*70)
    print("VERIFY KEY DERIVATION")
    print("="*70)
    
    pages = load_all_pages()
    
    # Get Page 0 and Page 57 (Parable)
    page0_runes = pages[0]
    page57_runes = pages[57]
    
    print(f"\n1. PAGE DATA:")
    print(f"   Page 0 runes: {len(page0_runes)} characters")
    print(f"   Page 57 runes: {len(page57_runes)} characters")
    print(f"   Stored key length: {len(STORED_KEY)}")
    
    # Convert to indices
    page0_idx = runes_to_indices(page0_runes)
    page57_idx = runes_to_indices(page57_runes)
    
    print(f"\n2. AS INDICES:")
    print(f"   Page 0: {len(page0_idx)} indices")
    print(f"   Page 57: {len(page57_idx)} indices")
    
    print(f"\n   Page 0 first 20 indices:  {page0_idx[:20].tolist()}")
    print(f"   Page 57 first 20 indices: {page57_idx[:20].tolist()}")
    
    # Derive key: Key = (Page0 - Page57) mod 29
    min_len = min(len(page0_idx), len(page57_idx))
    derived_key = (page0_idx[:min_len] - page57_idx[:min_len]) % 29
    
    print(f"\n3. DERIVED KEY (Page0 - Page57 mod 29):")
    print(f"   Length: {len(derived_key)}")
    print(f"   First 20: {derived_key[:20].tolist()}")
    print(f"   Sum: {sum(derived_key)}")
    print(f"   As text: {indices_to_text(derived_key[:50])}...")
    
    print(f"\n4. STORED MASTER KEY:")
    print(f"   Length: {len(STORED_KEY)}")
    print(f"   First 20: {STORED_KEY[:20]}")
    print(f"   Sum: {sum(STORED_KEY)}")
    print(f"   As text: {indices_to_text(STORED_KEY[:50])}...")
    
    print(f"\n5. COMPARISON:")
    stored_arr = np.array(STORED_KEY)
    if len(derived_key) >= len(stored_arr):
        match = np.array_equal(derived_key[:len(stored_arr)], stored_arr)
    else:
        match = np.array_equal(derived_key, stored_arr[:len(derived_key)])
    print(f"   Keys match: {match}")
    
    # Find differences
    if not match:
        print(f"\n   DIFFERENCES:")
        compare_len = min(len(derived_key), len(STORED_KEY))
        for i in range(compare_len):
            if derived_key[i] != STORED_KEY[i]:
                print(f"     Position {i}: derived={derived_key[i]}, stored={STORED_KEY[i]}")
                if i > 5:
                    print(f"     ... (showing first 6 differences)")
                    break
    
    # Now let's verify: which key actually decrypts Page 0 to the Parable?
    print("\n" + "="*70)
    print("6. VERIFICATION: Which key decrypts Page 0 to Page 57?")
    print("="*70)
    
    # Using derived key
    extended_derived = np.tile(derived_key, (len(page0_idx) // len(derived_key) + 1))[:len(page0_idx)]
    decrypted_derived = (page0_idx - extended_derived) % 29
    text_derived = indices_to_text(decrypted_derived)
    
    # Using stored key  
    extended_stored = np.tile(stored_arr, (len(page0_idx) // len(stored_arr) + 1))[:len(page0_idx)]
    decrypted_stored = (page0_idx - extended_stored) % 29
    text_stored = indices_to_text(decrypted_stored)
    
    # Expected
    expected_text = indices_to_text(page57_idx)
    
    print(f"\n   Expected (Page 57):  {expected_text[:80]}...")
    print(f"\n   With derived key:    {text_derived[:80]}...")
    print(f"\n   With stored key:     {text_stored[:80]}...")
    
    # Check matches
    print(f"\n   Derived key matches Page 57: {text_derived.startswith(expected_text[:50])}")
    print(f"   Stored key matches Page 57:  {text_stored.startswith(expected_text[:50])}")
    
    # Now what about the key text "JABEAIJAEM..."
    print("\n" + "="*70)
    print("7. THE 'JABEAIJAEM' KEY TEXT")
    print("="*70)
    
    key_text = "JABEAIJAEMNOECJOLIANONGLCLOEEEATDTHDAICEAMSMFAEIABTHXISHOEHHIAXTHTHMFEXEATHJXCOMHTJNCUNGNNNCFMAEEAWXXWXOYEADMHRNTWD"
    
    # Parse this text to indices
    key_parsed = []
    i = 0
    while i < len(key_text):
        # Try 2-char tokens first
        if i+1 < len(key_text):
            two_char = key_text[i:i+2].upper()
            if two_char in ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA']:
                idx = LETTERS.index(two_char)
                key_parsed.append(idx)
                i += 2
                continue
        # Single char
        char = key_text[i].upper()
        if char in 'FUORCGWHNIJPXSTBEMLD':
            idx = LETTERS.index(char)
            key_parsed.append(idx)
        elif char == 'A':
            key_parsed.append(24)  # A = 24
        elif char == 'Y':
            key_parsed.append(26)  # Y = 26
        i += 1
    
    print(f"   Key text: {key_text}")
    print(f"   Parsed length: {len(key_parsed)}")
    print(f"   First 20: {key_parsed[:20]}")
    print(f"   Sum: {sum(key_parsed)}")
    
    # Compare all three
    print("\n" + "="*70)
    print("8. ALL THREE KEYS COMPARED")
    print("="*70)
    
    print(f"\n   Derived (Page0 - Page57): {derived_key[:20].tolist()}")
    print(f"   Stored MASTER_KEY:        {STORED_KEY[:20]}")
    print(f"   Parsed from 'JABEA...':   {key_parsed[:20]}")
    
    # Maybe the issue is in how the key text was parsed?
    # Let me reverse: what text does the stored key produce?
    print("\n   Stored key as text: {indices_to_text(STORED_KEY[:95])}")
    print("   Derived key as text: {indices_to_text(derived_key[:95])}")
    
    # Wait - maybe Page 57 indices are different than we think
    print("\n" + "="*70)
    print("9. PAGE 57 INSPECTION")
    print("="*70)
    
    print(f"\n   Raw runes (first 50): {page57_runes[:50]}")
    print(f"   As indices (first 20): {page57_idx[:20].tolist()}")
    print(f"   As text: {indices_to_text(page57_idx[:30])}")
    
    # Does Page 57 start with "PARABLE LIKE THE INSTAR"?
    expected_start = "PARABLELIKETHEINSTAR"
    page57_text = indices_to_text(page57_idx)
    print(f"\n   Page 57 text starts: {page57_text[:30]}")
    print(f"   Expected start: {expected_start}")
    print(f"   Match: {page57_text.startswith(expected_start)}")
    
    # What if we need to add instead of subtract?
    print("\n" + "="*70)
    print("10. TEST DIFFERENT OPERATIONS")
    print("="*70)
    
    # Key = Page0 - Page57 gives us the key for: Plaintext = Cipher - Key
    # But what if: Key = Page57 - Page0 for: Plaintext = Cipher + Key ?
    
    alt_key = (page57_idx[:min_len] - page0_idx[:min_len]) % 29
    print(f"\n   Alt key (Page57 - Page0): {alt_key[:20].tolist()}")
    print(f"   Alt key sum: {sum(alt_key)}")
    
    # Verify alt key
    extended_alt = np.tile(alt_key, (len(page0_idx) // len(alt_key) + 1))[:len(page0_idx)]
    decrypted_alt = (page0_idx + extended_alt) % 29  # ADD instead of subtract
    text_alt = indices_to_text(decrypted_alt)
    print(f"   Decrypt with ADD: {text_alt[:80]}...")

if __name__ == "__main__":
    main()

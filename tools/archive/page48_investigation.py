#!/usr/bin/env python3
"""
PAGE 48 INVESTIGATION
=====================

We discovered Pages 0, 48, and 54 all have distance sum = 1331 from Parable!

1331 = 11³ (eleven cubed!)

Let's investigate if Page 48 is also related to the Parable.
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

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

def main():
    print("="*70)
    print("🔍 PAGE 48 INVESTIGATION")
    print("="*70)
    
    pages = load_all_pages()
    page_arrays = {num: runes_to_indices(text) for num, text in pages.items()}
    
    p0 = page_arrays[0]
    p48 = page_arrays[48]
    p54 = page_arrays[54]
    p57 = page_arrays[57]
    
    print(f"\n📊 Page Lengths:")
    print(f"   Page 0:  {len(p0)} runes")
    print(f"   Page 48: {len(p48)} runes")
    print(f"   Page 54: {len(p54)} runes")
    print(f"   Page 57: {len(p57)} runes")
    
    # Key from Page 0 - Page 57
    key_from_0 = (p0[:len(p57)] - p57) % 29
    
    # Key from Page 48 - Page 57
    key_from_48 = (p48[:len(p57)] - p57) % 29
    
    print(f"\n📋 Keys derived from subtracting Parable:")
    print(f"\n   Key from Page 0:")
    print(f"   Sum: {np.sum(key_from_0)}")
    print(f"   Text: {indices_to_text(key_from_0)}")
    
    print(f"\n   Key from Page 48:")
    print(f"   Sum: {np.sum(key_from_48)}")
    print(f"   Text: {indices_to_text(key_from_48)}")
    
    # Are they the same key?
    print(f"\n🔑 Are the keys identical?")
    print(f"   Identical: {np.array_equal(key_from_0, key_from_48)}")
    
    if not np.array_equal(key_from_0, key_from_48):
        diff = (key_from_48 - key_from_0) % 29
        print(f"   Difference: {diff.tolist()}")
        print(f"   Unique differences: {len(set(diff))}")
        if len(set(diff)) == 1:
            print(f"   UNIFORM SHIFT by: {diff[0]}")
    
    # What if we try to decrypt Page 48 with key from Page 0?
    print("\n" + "="*70)
    print("DECRYPT PAGE 48 WITH KEY FROM PAGE 0")
    print("="*70)
    
    extended_key = np.tile(key_from_0, (len(p48) // len(key_from_0) + 1))[:len(p48)]
    decrypted = (p48 - extended_key) % 29
    text = indices_to_text(decrypted)
    
    print(f"\n   Result: {text}")
    
    # Count words
    words = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
             'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
             'PARABLE', 'INSTAR', 'EMERGE', 'DIVINITY', 'CIRCUMFERENCE']
    
    found = []
    for word in words:
        if word in text.upper():
            found.append(word)
    print(f"   Words found: {found}")
    
    # Now let's look at Page 48 relationship to Pages 0 and 54
    print("\n" + "="*70)
    print("RELATIONSHIP BETWEEN PAGES 0, 48, 54")
    print("="*70)
    
    # Page 48 - Page 0 (first 95)
    diff_48_0 = (p48[:len(p57)] - p0[:len(p57)]) % 29
    print(f"\n   Page48 - Page0 (first 95):")
    print(f"   Sum: {np.sum(diff_48_0)}")
    print(f"   Unique values: {len(set(diff_48_0))}")
    if len(set(diff_48_0)) == 1:
        print(f"   UNIFORM SHIFT: {diff_48_0[0]}")
    else:
        print(f"   Difference: {indices_to_text(diff_48_0)}")
    
    # Maybe Page 48 encrypts DIFFERENT plaintext with the SAME key?
    print("\n" + "="*70)
    print("WHAT PLAINTEXT IS PAGE 48 ENCRYPTING?")
    print("="*70)
    
    # If Page 48 uses the same key as Pages 0/54...
    plaintext_48 = (p48 - extended_key[:len(p48)]) % 29
    print(f"\n   Decrypted Page 48 (using Page 0 key):")
    print(f"   {indices_to_text(plaintext_48)}")
    
    # But what if the plaintext for Page 48 is also known?
    # Let's check if it's actually the same as Page 0 but with different key
    print("\n" + "="*70)
    print("ALTERNATIVE: SAME PLAINTEXT, DIFFERENT KEY?")
    print("="*70)
    
    # If Page 48 has same plaintext as Pages 0/54 (repeated Parable)...
    # Then key_48 = Page48 - Parable_repeated
    parable_repeated = np.tile(p57, (len(p48) // len(p57) + 1))[:len(p48)]
    key_48_if_parable = (p48 - parable_repeated) % 29
    
    print(f"\n   If Page 48 plaintext = Parable repeated:")
    print(f"   Key would be: {indices_to_text(key_48_if_parable)}")
    print(f"   Key sum: {np.sum(key_48_if_parable)}")
    
    # Compare this key to key from Page 0
    key_0_extended = np.tile(key_from_0, (len(p48) // len(key_from_0) + 1))[:len(p48)]
    key_diff = (key_48_if_parable - key_0_extended) % 29
    
    print(f"\n   Difference from Page 0 key:")
    print(f"   Sum: {np.sum(key_diff)}")
    print(f"   Unique values: {len(set(key_diff))}")
    
    # Print some statistics about the relationship
    print("\n" + "="*70)
    print("NUMERICAL RELATIONSHIPS")
    print("="*70)
    
    print(f"\n   Page numbers: 0, 48, 54, 57")
    print(f"   Differences:")
    print(f"      48 - 0 = 48")
    print(f"      54 - 0 = 54")
    print(f"      54 - 48 = 6")
    print(f"      57 - 54 = 3")
    print(f"      57 - 48 = 9")
    print(f"      57 - 0 = 57")
    
    print(f"\n   Interesting:")
    print(f"      48 = 3 × 16 = 3 × 2⁴")
    print(f"      54 = 2 × 27 = 2 × 3³")
    print(f"      57 = 3 × 19")
    print(f"      6 = 2 × 3")
    print(f"      3, 6, 9 pattern!")
    
    print(f"\n   1331 = 11³ = (Page distance sum)")
    print(f"   1331 mod 48 = {1331 % 48}")
    print(f"   1331 mod 54 = {1331 % 54}")
    print(f"   1331 mod 57 = {1331 % 57}")

if __name__ == "__main__":
    main()

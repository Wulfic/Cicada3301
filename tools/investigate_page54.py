#!/usr/bin/env python3
"""
INVESTIGATE PAGE 54 AND OTHER POTENTIAL PARABLE COPIES

Page 0 and Page 54 both decrypt perfectly with the master key!
Are there more pages that are copies of the Parable?
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
    page57_indices = [rune_to_idx(r) for r in pages[57]]
    
    print("=" * 80)
    print("COMPARING PAGES 0, 54, AND 57")
    print("=" * 80)
    
    for pg_num in [0, 54]:
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        print(f"\n=== PAGE {pg_num} ===")
        print(f"Length: {len(cipher)} runes")
        
        # Decrypt first 95 with master key
        text = decrypt_with_key(cipher[:95], MASTER_KEY, 0)
        print(f"First 95 decrypted: {text}")
        
        # Check if it's exactly the Parable
        parable_text = ''.join(idx_to_letter(idx) for idx in page57_indices)
        if text == parable_text:
            print("  ✓ EXACT MATCH with Page 57 (Parable)")
        else:
            print("  ✗ Does NOT exactly match Page 57")
        
        # What about the rest?
        if len(cipher) > 95:
            rest = decrypt_with_key(cipher[95:], MASTER_KEY, 0)
            print(f"Characters 96-{len(cipher)}: {rest[:80]}...")
    
    print("\n" + "=" * 80)
    print("CHECKING ALL PAGES FOR PARABLE PATTERN (FIRST 95 CHARS)")
    print("=" * 80)
    
    parable_text = ''.join(idx_to_letter(idx) for idx in page57_indices)
    
    for pg_num in sorted(pages.keys()):
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        if len(cipher) < 95:
            continue
        
        # Check at all offsets
        for offset in range(95):
            text = decrypt_with_key(cipher[:95], MASTER_KEY, offset)
            if text == parable_text:
                print(f"Page {pg_num} at offset {offset}: MATCHES PARABLE exactly!")
                break
    
    print("\n" + "=" * 80)
    print("RAW RUNE COMPARISON: PAGES 0 vs 54")
    print("=" * 80)
    
    page0_runes = pages[0][:95]
    page54_runes = pages[54][:95]
    
    print(f"Page 0 first 95:  {page0_runes}")
    print(f"Page 54 first 95: {page54_runes}")
    
    if page0_runes == page54_runes:
        print("\n✓ Pages 0 and 54 have IDENTICAL first 95 runes!")
    else:
        # Count differences
        diffs = sum(1 for i in range(95) if page0_runes[i] != page54_runes[i])
        print(f"\nDifferences in first 95 runes: {diffs}")
        for i in range(min(95, len(page0_runes), len(page54_runes))):
            if page0_runes[i] != page54_runes[i]:
                print(f"  Position {i}: Page0='{page0_runes[i]}' vs Page54='{page54_runes[i]}'")
    
    print("\n" + "=" * 80)
    print("HYPOTHESIS: UNSOLVED PAGES ENCRYPT DIFFERENT PLAINTEXT")
    print("=" * 80)
    
    # What if we derive keys by subtracting PAGE 0's PLAINTEXT from unsolved pages?
    # The pattern:
    #   Page0 = Parable + MasterKey
    #   PageN = PlaintextN + KeyN
    # 
    # If PlaintextN is NOT the Parable, then:
    #   PageN - Parable = KeyN' ≠ MasterKey
    #
    # But what if PlaintextN is DIFFERENT text but KeyN = MasterKey?
    #   Then PageN = PlaintextN + MasterKey
    #   So PlaintextN = PageN - MasterKey
    
    print("\nDecrypting unsolved pages assuming they use MasterKey but different plaintext:")
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        cipher = [rune_to_idx(r) for r in pages[pg_num]]
        
        # Try decrypting with master key at different offsets
        for offset in range(95):
            text = decrypt_with_key(cipher, MASTER_KEY, offset)
            
            # Check for English-like patterns
            # Look for common 3-letter sequences
            trigrams = {}
            for i in range(len(text) - 2):
                tri = text[i:i+3]
                trigrams[tri] = trigrams.get(tri, 0) + 1
            
            # Check if any common English trigrams appear
            common = sum(trigrams.get(t, 0) for t in ['THE', 'AND', 'ING', 'ENT', 'ION', 'TIO', 'FOR', 'OUR', 'ERE'])
            
            if common >= 3:
                print(f"\nPage {pg_num} offset {offset}: {common} common trigrams")
                print(f"  {text[:80]}...")
                break

if __name__ == "__main__":
    main()

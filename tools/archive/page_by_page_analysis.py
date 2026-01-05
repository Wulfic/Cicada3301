#!/usr/bin/env python3
"""
Key discovery: The runes file contains BOTH encrypted and decrypted pages!
Page 18 (IoC 1.82) appears to be plaintext.

Let's properly identify which pages are encrypted vs decrypted,
and then focus analysis only on the encrypted pages.
"""

import numpy as np
from collections import Counter
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

def load_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def analyze_all_pages():
    """Analyze each page individually."""
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    lp_text = load_file(lp_path)
    
    # Split by & (page marker)
    pages = lp_text.split('&')
    
    print("="*80)
    print("PAGE-BY-PAGE ANALYSIS")
    print("="*80)
    print(f"\nTotal pages found: {len(pages)}")
    print(f"\nLegend:")
    print("  IoC > 1.5: LIKELY DECRYPTED or simple substitution")
    print("  IoC ~ 1.0: ENCRYPTED (polyalphabetic/stream)")
    print()
    print(f"{'Page':<6} {'Runes':<8} {'IoC':<8} {'Status':<15} {'Sample'}")
    print("-" * 80)
    
    encrypted_pages = []
    decrypted_pages = []
    
    for i, page in enumerate(pages):
        runes = text_to_indices(page)
        n = len(runes)
        
        if n < 5:
            continue
        
        ioc = compute_ioc_normalized(runes)
        english = indices_to_english(runes[:40])
        
        if ioc > 1.5:
            status = "DECRYPTED"
            decrypted_pages.append(i)
        else:
            status = "ENCRYPTED"
            encrypted_pages.append(i)
        
        print(f"{i:<6} {n:<8} {ioc:<8.4f} {status:<15} {english}...")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nDecrypted pages (IoC > 1.5): {decrypted_pages}")
    print(f"Encrypted pages (IoC ~ 1.0): {encrypted_pages}")
    print(f"\nTotal encrypted: {len(encrypted_pages)}")
    print(f"Total decrypted: {len(decrypted_pages)}")
    
    # Combine all encrypted pages
    print("\n" + "="*80)
    print("COMBINED ENCRYPTED PAGES ANALYSIS")
    print("="*80)
    
    encrypted_text = ""
    encrypted_indices = []
    
    for i in encrypted_pages:
        page_text = pages[i]
        encrypted_text += page_text
        page_indices = text_to_indices(page_text)
        encrypted_indices.extend(page_indices.tolist())
    
    encrypted_indices = np.array(encrypted_indices, dtype=np.int32)
    
    print(f"\nTotal encrypted runes: {len(encrypted_indices)}")
    print(f"Combined encrypted IoC: {compute_ioc_normalized(encrypted_indices):.4f}")
    
    # Show frequency distribution for encrypted only
    print("\nFrequency distribution of encrypted pages:")
    counts = Counter(encrypted_indices)
    for idx, count in counts.most_common():
        pct = count / len(encrypted_indices) * 100
        bar = "*" * int(pct * 5)
        print(f"  {LETTERS[idx]:<3}: {count:4d} ({pct:5.2f}%) {bar}")
    
    return encrypted_pages, decrypted_pages, pages

def analyze_decrypted_content(decrypted_pages, pages):
    """Show what the decrypted pages say."""
    print("\n" + "="*80)
    print("DECRYPTED PAGE CONTENT")
    print("="*80)
    
    for i in decrypted_pages:
        runes = text_to_indices(pages[i])
        english = indices_to_english(runes)
        
        print(f"\n--- Page {i} ---")
        # Add spaces based on original word boundaries
        text = pages[i]
        result = []
        rune_idx = 0
        
        for char in text:
            if char in RUNE_TO_IDX:
                result.append(LETTERS[runes[rune_idx]])
                rune_idx += 1
            elif char == '-':
                result.append(' ')
            elif char == '/':
                result.append('\n')
            elif char == '.':
                result.append('. ')
        
        readable = ''.join(result)
        print(readable[:500])

def main():
    encrypted_pages, decrypted_pages, pages = analyze_all_pages()
    analyze_decrypted_content(decrypted_pages, pages)

if __name__ == "__main__":
    main()

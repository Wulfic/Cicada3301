#!/usr/bin/env python3
"""
Focus on the "ADD" direction finding - "THE" appears 93 times!
This suggests we're on the right track but need one more transformation.
"""

import numpy as np
from collections import Counter
from pathlib import Path
import re

ALPHABET_SIZE = 29

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

# Single letter simplified mapping
SIMPLE_LETTERS = ['F', 'U', 'T', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                  'E', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'N', 'O', 'D', 
                  'A', 'A', 'Y', 'I', 'E']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_liber_primus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def indices_to_simple(indices):
    return ''.join(SIMPLE_LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def gematria_shift_add(ciphertext):
    """Add gematria value to each rune."""
    result = np.zeros_like(ciphertext)
    for i, idx in enumerate(ciphertext):
        gem = GEMATRIA[idx]
        result[i] = (idx + gem) % 29
    return result

def extract_with_spaces(text, decrypted):
    """Extract text preserving word boundaries."""
    result = []
    dec_idx = 0
    
    for char in text:
        if char in RUNE_TO_IDX:
            if dec_idx < len(decrypted):
                result.append(LETTERS[decrypted[dec_idx]])
                dec_idx += 1
        elif char == '•':
            result.append(' ')
        elif char in '-':
            result.append(' ')
        elif char in '/%\n':
            result.append(' ')
        elif char == ':':
            result.append(':')
        elif char == '.':
            result.append('.')
    
    return ''.join(result)

def try_caesar_on_gematria_result(gematria_result):
    """Try Caesar shifts on the gematria-shifted result."""
    print("\n" + "="*60)
    print("TRYING CAESAR SHIFTS ON GEMATRIA+ RESULT")
    print("="*60)
    
    for shift in range(29):
        shifted = (gematria_result - shift) % 29
        eng = indices_to_english(shifted[:100])
        
        # Count "THE"
        the_count = eng.count('THE')
        and_count = eng.count('AND')
        
        if the_count > 5 or and_count > 2:
            print(f"\nShift {shift}: THE={the_count}, AND={and_count}")
            print(f"  {eng}")

def try_substitution_mapping(decrypted):
    """
    The output has THE 93 times. 
    But maybe the letter mappings are off.
    Try to find patterns.
    """
    print("\n" + "="*60)
    print("ANALYZING PATTERNS IN GEMATRIA+ OUTPUT")
    print("="*60)
    
    eng = indices_to_english(decrypted)
    
    # Find all 3-letter sequences
    trigrams = Counter()
    for i in range(len(eng) - 2):
        trigrams[eng[i:i+3]] += 1
    
    print("\nTop 20 trigrams:")
    for tg, count in trigrams.most_common(20):
        print(f"  {tg}: {count}")
    
    # The most common trigram should be THE
    # What maps to THE in our output?
    print(f"\n'THE' count: {trigrams.get('THE', 0)}")
    
    # Look for words
    print("\nSearching for English words in spaces-separated text...")

def analyze_pages_separately(lp_text, lp_indices, gematria_decrypted):
    """Analyze each page separately."""
    print("\n" + "="*60)
    print("ANALYZING PAGES SEPARATELY")
    print("="*60)
    
    # Split by page markers
    pages = lp_text.split('&')
    
    idx_start = 0
    for i, page in enumerate(pages[:5]):  # First 5 pages
        if not page.strip():
            continue
            
        page_indices = text_to_indices(page)
        n = len(page_indices)
        
        if n == 0:
            continue
        
        page_decrypted = gematria_decrypted[idx_start:idx_start + n]
        idx_start += n
        
        ioc = compute_ioc_normalized(page_decrypted)
        eng = indices_to_english(page_decrypted[:100])
        
        print(f"\nPage {i}: {n} runes, IoC={ioc:.4f}")
        print(f"  {eng}...")

def main():
    print("="*70)
    print("GEMATRIA ADD DIRECTION - 'THE' INVESTIGATION")
    print("="*70)
    
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    lp_text = load_liber_primus(lp_path)
    lp_indices = text_to_indices(lp_text)
    
    # Apply gematria add
    gematria_result = gematria_shift_add(lp_indices)
    
    print(f"\nTotal runes: {len(lp_indices)}")
    print(f"Original IoC: {compute_ioc_normalized(lp_indices):.4f}")
    print(f"Gematria+ IoC: {compute_ioc_normalized(gematria_result):.4f}")
    
    # Full text
    text_add = extract_with_spaces(lp_text, gematria_result)
    
    print("\n" + "="*60)
    print("FIRST 1000 CHARS OF GEMATRIA+ OUTPUT")
    print("="*60)
    print(text_add[:1000])
    
    # Count common words
    print("\n" + "="*60)
    print("WORD FREQUENCY ANALYSIS")
    print("="*60)
    
    # Clean and count words
    words = text_add.split()
    word_counts = Counter(words)
    
    print("\nTop 30 most common 'words':")
    for word, count in word_counts.most_common(30):
        print(f"  {word}: {count}")
    
    # Look for THE specifically
    the_positions = [m.start() for m in re.finditer(r'\bTH[EI]\b', text_add)]
    print(f"\n'THE/THI' found at {len(the_positions)} positions")
    
    # Show contexts where THE appears
    print("\nContexts for 'THE':")
    for pos in the_positions[:10]:
        start = max(0, pos - 20)
        end = min(len(text_add), pos + 25)
        print(f"  ...{text_add[start:end]}...")
    
    # Try substitution analysis
    try_substitution_mapping(gematria_result)
    
    # Caesar on result
    try_caesar_on_gematria_result(gematria_result[:500])
    
    # Analyze pages separately  
    analyze_pages_separately(lp_text, lp_indices, gematria_result)
    
    # Save to file for manual analysis
    output_path = Path(__file__).parent / "gematria_add_output.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("GEMATRIA ADD DIRECTION OUTPUT\n")
        f.write("="*60 + "\n\n")
        f.write("Method: For each rune, new_rune = rune + gematria(rune) mod 29\n\n")
        f.write(text_add)
    
    print(f"\n\nFull output saved to: {output_path}")

if __name__ == "__main__":
    main()

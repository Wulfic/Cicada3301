#!/usr/bin/env python3
"""
RUNNING KEY ATTACK WITH SELF-RELIANCE
======================================

The IoC analysis shows pages 18-54 have IoC ~0.034 (essentially random).
This is consistent with a RUNNING KEY cipher where the key is as long as the plaintext.

Self-Reliance by Emerson is explicitly referenced in solved pages:
- Page 56: "shed our circumferences" (from Self-Reliance: "we shall be forced to take with shame our own opinion")
- Page 03: "the great journey" theme

This script attempts running key decryption using Self-Reliance text.

Author: Wulfic
"""

import os
from pathlib import Path

# Gematria Primus mapping
GEMATRIA = {
    'ᚠ': (0, 'F'),    'ᚢ': (1, 'U'),    'ᚦ': (2, 'TH'),
    'ᚩ': (3, 'O'),    'ᚱ': (4, 'R'),    'ᚳ': (5, 'C'),
    'ᚷ': (6, 'G'),    'ᚹ': (7, 'W'),    'ᚻ': (8, 'H'),
    'ᚾ': (9, 'N'),    'ᛁ': (10, 'I'),   'ᛂ': (11, 'J'),
    'ᛄ': (11, 'J'),   'ᛇ': (12, 'EO'),  'ᛈ': (13, 'P'),
    'ᛉ': (14, 'X'),   'ᛋ': (15, 'S'),   'ᛏ': (16, 'T'),
    'ᛒ': (17, 'B'),   'ᛖ': (18, 'E'),   'ᛗ': (19, 'M'),
    'ᛚ': (20, 'L'),   'ᛝ': (21, 'NG'),  'ᛟ': (22, 'OE'),
    'ᛞ': (23, 'D'),   'ᚪ': (24, 'A'),   'ᚫ': (25, 'AE'),
    'ᚣ': (26, 'Y'),   'ᛡ': (27, 'IA'),  'ᛠ': (28, 'EA')
}

RUNE_TO_IDX = {k: v[0] for k, v in GEMATRIA.items()}
IDX_TO_LATIN = {v[0]: v[1] for k, v in GEMATRIA.items()}

# Latin to index mapping
LATIN_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

MOD = 29

def load_page(page_num):
    """Load runes from page file"""
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    rune_file = page_dir / "runes.txt"
    if not rune_file.exists():
        return None
    with open(rune_file, 'r', encoding='utf-8') as f:
        return f.read()

def load_self_reliance():
    """Load Self-Reliance text"""
    script_dir = Path(__file__).parent
    sr_file = script_dir.parent / "reference" / "research" / "Self-Reliance.txt"
    if not sr_file.exists():
        return None
    with open(sr_file, 'r', encoding='utf-8') as f:
        return f.read()

def text_to_indices(text):
    """Convert English text to indices for running key"""
    indices = []
    text = text.upper()
    i = 0
    while i < len(text):
        # Handle digraphs
        if i + 1 < len(text):
            dg = text[i:i+2]
            if dg == 'TH':
                indices.append(2); i += 2; continue
            elif dg == 'NG':
                indices.append(21); i += 2; continue
            elif dg == 'EA':
                indices.append(28); i += 2; continue
            elif dg == 'IA':
                indices.append(27); i += 2; continue
            elif dg == 'EO':
                indices.append(12); i += 2; continue
            elif dg == 'OE':
                indices.append(22); i += 2; continue
            elif dg == 'AE':
                indices.append(25); i += 2; continue
        
        # Single char
        if text[i] in LATIN_TO_IDX:
            indices.append(LATIN_TO_IDX[text[i]])
        i += 1
    
    return indices

def indices_to_latin(indices):
    """Convert indices to Latin text"""
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def score_english(text):
    """Score text for English-likeness"""
    BIGRAMS = {
        'TH': 15, 'HE': 12, 'IN': 11, 'ER': 10, 'AN': 10, 'RE': 9, 'ON': 9,
        'AT': 8, 'EN': 8, 'ND': 8, 'TI': 8, 'ES': 8, 'OR': 8, 'TE': 7,
        'OF': 7, 'ED': 7, 'IS': 7, 'IT': 7, 'AL': 7, 'AR': 7, 'ST': 7,
    }
    
    COMMON_WORDS = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL'}
    
    CICADA_WORDS = {'DIVINITY', 'CIRCUMFERENCE', 'PILGRIM', 'SACRED', 'PRIMES', 
                    'TOTIENT', 'WITHIN', 'DEEP', 'WEB', 'INSTAR', 'EMERGENCE',
                    'WISDOM', 'TRUTH', 'BELIEF', 'PARABLE', 'KOAN', 'WARNING'}
    
    score = 0
    text = text.upper().replace('-', ' ')
    
    # Bigram score
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        if bg in BIGRAMS:
            score += BIGRAMS[bg]
    
    # Word score
    words = text.split()
    for word in words:
        if word in COMMON_WORDS:
            score += 50
        if word in CICADA_WORDS:
            score += 200  # Cicada-specific words are very valuable
    
    return score

def running_key_decrypt(cipher, key, mode='SUB'):
    """Decrypt using running key cipher"""
    result = []
    for i in range(min(len(cipher), len(key))):
        c = cipher[i]
        k = key[i]
        if mode == 'SUB':
            p = (c - k) % MOD
        elif mode == 'ADD':
            p = (c + k) % MOD
        elif mode == 'SUB_REV':
            p = (k - c) % MOD
        else:
            p = c
        result.append(p)
    return result

def main():
    print("=" * 80)
    print("RUNNING KEY ATTACK WITH SELF-RELIANCE")
    print("=" * 80)
    
    # Load Self-Reliance
    sr_text = load_self_reliance()
    if not sr_text:
        print("ERROR: Could not load Self-Reliance.txt")
        return
    
    # Clean and convert to key
    sr_clean = ''.join(c for c in sr_text if c.isalpha() or c.isspace())
    sr_key = text_to_indices(sr_clean)
    print(f"Self-Reliance key length: {len(sr_key)} indices")
    print(f"First 50 key values: {sr_key[:50]}")
    
    # Test pages
    test_pages = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    for page_num in test_pages:
        print(f"\n{'='*80}")
        print(f"PAGE {page_num}")
        print(f"{'='*80}")
        
        rune_text = load_page(page_num)
        if not rune_text:
            print(f"  Could not load page {page_num}")
            continue
        
        # Extract cipher indices
        cipher = [RUNE_TO_IDX[c] for c in rune_text if c in RUNE_TO_IDX]
        print(f"  Cipher length: {len(cipher)}")
        
        # Try different starting positions in Self-Reliance
        best_results = []
        
        for start_offset in range(0, min(5000, len(sr_key) - len(cipher)), 100):
            key_slice = sr_key[start_offset:start_offset + len(cipher)]
            
            for mode in ['SUB', 'ADD', 'SUB_REV']:
                result = running_key_decrypt(cipher, key_slice, mode)
                text = indices_to_latin(result)
                score = score_english(text)
                
                if score > 200:
                    best_results.append((mode, start_offset, score, text[:80]))
        
        # Sort and display
        best_results.sort(key=lambda x: x[2], reverse=True)
        
        if best_results:
            print(f"\n  TOP RESULTS:")
            for mode, offset, score, preview in best_results[:5]:
                print(f"    [{score:>6.1f}] {mode:10s} offset={offset:5d}")
                print(f"            {preview}")
        else:
            print("    No promising results with Self-Reliance key")
        
        # Also try with the key starting at specific thematic points
        print("\n  Testing thematic starting points...")
        
        # Find key phrases in Self-Reliance
        sr_upper = sr_text.upper()
        thematic_starts = [
            ("TRUST THYSELF", sr_upper.find("TRUST THYSELF")),
            ("ENVY IS IGNORANCE", sr_upper.find("ENVY IS IGNORANCE")),
            ("NOTHING IS AT LAST SACRED", sr_upper.find("NOTHING IS AT LAST SACRED")),
            ("CIRCUMFERENCE", sr_upper.find("CIRCUMFERENCE")),
            ("DIVINE", sr_upper.find("DIVINE")),
        ]
        
        for phrase, pos in thematic_starts:
            if pos == -1:
                continue
            
            # Convert position to key index (approximate)
            key_start = len([c for c in sr_upper[:pos] if c.isalpha()])
            
            if key_start + len(cipher) > len(sr_key):
                continue
            
            key_slice = sr_key[key_start:key_start + len(cipher)]
            
            for mode in ['SUB', 'ADD']:
                result = running_key_decrypt(cipher, key_slice, mode)
                text = indices_to_latin(result)
                score = score_english(text)
                
                if score > 100:
                    print(f"    [{score:>6.1f}] {phrase[:20]:20s} + {mode}")
                    print(f"            {text[:80]}")

if __name__ == '__main__':
    main()

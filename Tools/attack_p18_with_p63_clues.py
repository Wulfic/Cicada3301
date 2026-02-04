#!/usr/bin/env python3
"""
Attack Page 18 using clues from Page 63 grid

Page 63 contains a mysterious grid with "18" appearing twice:
- Row 2: AETHEREAL BUFFER SUOID CARNAL 18
- Row 4: 18 ANALOGUOID MOURNFUL AETHEREAL

This script tests these terms as Vigenère keys for Page 18's body.
"""

import os
from collections import Counter

# Gematria Primus mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X',
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

def text_to_indices(text):
    """Convert English text to Gematria indices."""
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Check digraphs
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph == 'TH': result.append(2); i += 2; continue
            if digraph == 'EO': result.append(12); i += 2; continue
            if digraph == 'NG': result.append(21); i += 2; continue
            if digraph == 'OE': result.append(22); i += 2; continue
            if digraph == 'AE': result.append(25); i += 2; continue
            if digraph == 'IA' or digraph == 'IO': result.append(27); i += 2; continue
            if digraph == 'EA': result.append(28); i += 2; continue
        # Single chars
        c = text[i]
        idx_map = {'F':0,'U':1,'O':3,'R':4,'C':5,'K':5,'G':6,'W':7,'H':8,'N':9,
                   'I':10,'J':11,'P':13,'X':14,'S':15,'T':16,'B':17,'E':18,'M':19,
                   'L':20,'D':23,'A':24,'Y':26}
        if c in idx_map:
            result.append(idx_map[c])
        i += 1
    return result

def load_runes_with_structure(filepath):
    """Load runes, preserving line structure, return body only (skip title)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # First line is title, rest is body
    title_line = lines[0] if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    
    title_indices = [RUNE_MAP[c] for c in title_line if c in RUNE_MAP]
    body_indices = []
    for line in body_lines:
        for c in line:
            if c in RUNE_MAP:
                body_indices.append(RUNE_MAP[c])
    
    return title_indices, body_indices

def calc_ioc(indices):
    """Calculate Index of Coincidence for 29-letter alphabet."""
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    """Convert indices to Latin letters."""
    return ''.join(LATIN_TABLE[i] for i in indices)

def vigenere_decrypt(cipher, key, mode='sub'):
    """Decrypt with Vigenère cipher."""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        elif mode == 'add':
            result.append((c + k) % 29)
        elif mode == 'beaufort':
            result.append((k - c) % 29)
    return result

def score_english(text):
    """Score text based on English-like patterns."""
    score = 0
    # Common English words
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                    'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HIS', 'HAS',
                    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM',
                    'THEY', 'BEEN', 'CALL', 'FIRST', 'SOME', 'WHO', 'ITS',
                    'CIRCUMFERENCE', 'DIVINITY', 'SACRED', 'PRIMES', 'WISDOM',
                    'WITHIN', 'BEING', 'PILGRIMAGE', 'PILGRIM', 'SEEK', 'PATH']
    for word in common_words:
        if word in text:
            score += len(word) * 10
    # Penalize unlikely patterns
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in ['XXX', 'QQQ', 'ZZZ', 'JJJ', 'VVV']:
            score -= 50
    return score

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p18_path = os.path.join(repo, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    title, body = load_runes_with_structure(p18_path)
    print(f"Page 18 Title: {len(title)} runes")
    print(f"Page 18 Body: {len(body)} runes")
    
    # Page 63 grid terms to test as keys
    # Adjacent to "18" in the grid:
    grid_keys = {
        # Row 2: ... CARNAL 18
        'CARNAL': text_to_indices('CARNAL'),
        'SUOID': text_to_indices('SUOID'),
        'BUFFER': text_to_indices('BUFFER'),
        'AETHEREAL': text_to_indices('AETHEREAL'),
        
        # Row 4: 18 ANALOGUOID ...
        'ANALOG': text_to_indices('ANALOG'),
        'ANALOGUOID': text_to_indices('ANALOGUOID'),
        'MOURNFUL': text_to_indices('MOURNFUL'),
        
        # Other grid terms
        'SHADOWS': text_to_indices('SHADOWS'),
        'OBSCURA': text_to_indices('OBSCURA'),
        'FORM': text_to_indices('FORM'),
        'MOBIUS': text_to_indices('MOBIUS'),
        'CABAL': text_to_indices('CABAL'),
        'VOID': text_to_indices('VOID'),  # Could be hidden in SUOID
        
        # Combined terms
        'AETHEREAL_CABAL': text_to_indices('AETHEREALCABAL'),
        'CARNAL_ANALOG': text_to_indices('CARNAL') + text_to_indices('ANALOG'),
        
        # Number-based keys from grid (mod 29)
        'NUMBERS_ROW1': [272 % 29, 138 % 29, 131 % 29, 151 % 29],  # [11, 22, 15, 6]
        'NUMBERS_272138': [2, 7, 2, 1, 3, 8],  # Digits as indices
        
        # Reversed SUOID
        'DIOUS': text_to_indices('DIOUS'),
        
        # Other possible interpretations
        'ODIOUS': text_to_indices('ODIOUS'),  # SUOID anagram?
    }
    
    # Also test known working keys for reference
    known_keys = {
        'DIVINITY': text_to_indices('DIVINITY'),
        'FIRFUMFERENFE': text_to_indices('FIRFUMFERENFE'),
        'YAHEOOPYJ': text_to_indices('YAHEOOPYJ'),
    }
    
    all_keys = {**grid_keys, **known_keys}
    
    results = []
    
    for key_name, key in all_keys.items():
        if not key:
            continue
        for mode in ['sub', 'add', 'beaufort']:
            decrypted = vigenere_decrypt(body, key, mode)
            ioc = calc_ioc(decrypted)
            latin = indices_to_latin(decrypted)
            eng_score = score_english(latin)
            results.append({
                'key': key_name,
                'mode': mode,
                'ioc': ioc,
                'eng_score': eng_score,
                'preview': latin[:80],
                'key_len': len(key)
            })
    
    # Sort by IoC first, then by English score
    results.sort(key=lambda x: (x['ioc'], x['eng_score']), reverse=True)
    
    print("\n" + "="*90)
    print("RESULTS (sorted by IoC + English score)")
    print("="*90)
    
    for r in results[:20]:
        print(f"\n[{r['key']}] Mode: {r['mode']}, Key Len: {r['key_len']}")
        print(f"  IoC: {r['ioc']:.4f}, Eng Score: {r['eng_score']}")
        print(f"  Preview: {r['preview']}")
    
    # Identify potential hits
    print("\n" + "="*90)
    print("POTENTIAL HITS (IoC > 1.3 or Eng Score > 50)")
    print("="*90)
    hits = [r for r in results if r['ioc'] > 1.3 or r['eng_score'] > 50]
    for r in hits:
        print(f"\n*** [{r['key']}] Mode: {r['mode']} ***")
        print(f"IoC: {r['ioc']:.4f}, Eng Score: {r['eng_score']}")
        print(f"Full preview: {r['preview']}")

if __name__ == '__main__':
    main()

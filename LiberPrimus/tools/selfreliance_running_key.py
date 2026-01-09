#!/usr/bin/env python3
"""
SELF-RELIANCE RUNNING KEY ATTACK

Hypothesis: The unsolved pages (17-55) may use Emerson's Self-Reliance 
essay as a running key. This is suggested by:
1. Page 56 references "circumferences" - a word from Self-Reliance
2. The solved pages contain philosophical themes matching Emerson
3. Standard Vigenère attacks fail, suggesting a non-repeating key

This script tries different starting positions in Self-Reliance
as the running key for each unsolved page.
"""

import os
from pathlib import Path

# Gematria Primus alphabet
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {}
for i, L in enumerate(LETTERS):
    LETTER_TO_IDX[L] = i
    if len(L) == 1:
        LETTER_TO_IDX[L.lower()] = i

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

# Common English words for scoring
COMMON_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
    'WE', 'THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 
    'WAS', 'ONE', 'OUR', 'OUT', 'ARE', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY',
    'NEW', 'NOW', 'OLD', 'SAY', 'SHE', 'TOO', 'TWO', 'WAY', 'WHO', 'YET',
    'THY', 'YEA', 'NAY', 'FIND', 'PATH', 'SEEK', 'TRUTH', 'LIGHT', 'WITHIN',
    'SELF', 'SOUL', 'MAN', 'MEN', 'MUST', 'WITH', 'THIS', 'THAT', 'FROM', 
    'HAVE', 'BEEN', 'WILL', 'WHAT', 'WHEN', 'YOUR', 'EACH', 'EVERY', 'WHICH',
    'THERE', 'THEIR', 'THESE', 'OTHER', 'WOULD', 'COULD', 'SHOULD', 'BEING',
    'THING', 'THINGS', 'KNOW', 'KNOWLEDGE', 'WISDOM', 'PARABLE', 'KOAN',
    'INSTRUCTION', 'WARNING', 'WELCOME', 'PILGRIM', 'JOURNEY', 'SACRED',
    'PRIMES', 'DIVINITY', 'CIRCUMFERENCE', 'INSTAR', 'EMERGE', 'SURFACE',
    'RELIANCE', 'TRUST', 'NATURE', 'GENIUS', 'CONFORMITY', 'NONCONFORMIST'
}

def load_self_reliance():
    """Load Self-Reliance essay from reference folder."""
    script_dir = Path(__file__).parent
    sr_path = script_dir.parent / "reference" / "research" / "Self-Reliance.txt"
    
    if not sr_path.exists():
        print(f"Self-Reliance not found at {sr_path}")
        return None
    
    with open(sr_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Clean up: remove punctuation, keep only letters
    cleaned = ''.join(c.upper() for c in text if c.isalpha())
    return cleaned

def text_to_indices(text):
    """Convert English text to Gematria indices."""
    result = []
    i = 0
    text = text.upper()
    
    # Define digraphs in order of preference
    digraphs = ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO']
    
    while i < len(text):
        matched = False
        
        # Try digraphs first
        for digraph in digraphs:
            if text[i:i+len(digraph)] == digraph:
                if digraph in LETTER_TO_IDX:
                    result.append(LETTER_TO_IDX[digraph])
                    i += len(digraph)
                    matched = True
                    break
        
        if not matched:
            char = text[i]
            if char in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[char])
            elif char == 'K':
                result.append(LETTER_TO_IDX['C'])  # K = C in Gematria
            elif char == 'Q':
                result.append(LETTER_TO_IDX['C'])  # Q = C
            elif char == 'V':
                result.append(LETTER_TO_IDX['U'])  # V = U
            elif char == 'Z':
                result.append(LETTER_TO_IDX['S'])  # Z = S
            i += 1
    
    return result

def indices_to_text(indices):
    """Convert indices back to text."""
    return ''.join(LETTERS[i] for i in indices)

def load_page_runes(page_num):
    """Load runes from a page."""
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None, None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        rune_text = f.read()
    
    # Parse to indices (cipher)
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    # Also parse word boundaries
    words = []
    current = []
    for c in rune_text:
        if c in RUNE_MAP:
            current.append(RUNE_MAP[c])
        elif c in '-. \n\r/':
            if current:
                words.append(current)
                current = []
    if current:
        words.append(current)
    
    return cipher, words

def decrypt_sub(cipher, key_indices):
    """Decrypt using SUB mod 29."""
    plain = []
    for i in range(len(cipher)):
        k = key_indices[i % len(key_indices)]
        plain.append((cipher[i] - k) % 29)
    return plain

def decrypt_add(cipher, key_indices):
    """Decrypt using ADD mod 29 (reverse of SUB)."""
    plain = []
    for i in range(len(cipher)):
        k = key_indices[i % len(key_indices)]
        plain.append((cipher[i] + k) % 29)
    return plain

def score_plaintext(plain_indices, word_boundaries):
    """Score plaintext by English word matches."""
    score = 0
    words_found = []
    
    pos = 0
    for word_cipher in word_boundaries:
        wlen = len(word_cipher)
        if pos + wlen > len(plain_indices):
            break
        
        word_text = indices_to_text(plain_indices[pos:pos+wlen])
        
        if word_text in COMMON_WORDS:
            score += len(word_text) * 100
            words_found.append(word_text)
        elif len(word_text) <= 3:
            # Partial credit for short words that look English-ish
            if all(c in 'AEIOUY' or c in 'THNG' for c in word_text[:2]):
                score += 5
        
        pos += wlen
    
    return score, words_found

def test_self_reliance_key(page_num, sr_text, sr_indices, max_offsets=1000):
    """Test Self-Reliance as running key with different starting positions."""
    
    cipher, words = load_page_runes(page_num)
    if cipher is None:
        return None
    
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - Testing Self-Reliance Running Key")
    print(f"Cipher length: {len(cipher)}")
    print("=" * 70)
    
    best_results = []
    
    for offset in range(0, min(max_offsets, len(sr_indices) - len(cipher))):
        key_slice = sr_indices[offset:offset + len(cipher)]
        
        if len(key_slice) < len(cipher):
            break
        
        # Try both SUB and ADD
        for op_name, decrypt_func in [('SUB', decrypt_sub), ('ADD', decrypt_add)]:
            plain = decrypt_func(cipher, key_slice)
            score, found = score_plaintext(plain, words)
            
            if score > 0:
                best_results.append({
                    'offset': offset,
                    'operation': op_name,
                    'score': score,
                    'words': found,
                    'preview': indices_to_text(plain[:80]),
                    'key_preview': sr_text[offset:offset+50]
                })
    
    # Sort by score
    best_results.sort(key=lambda x: x['score'], reverse=True)
    
    # Show top 10
    print("\nTop 10 results:")
    for i, r in enumerate(best_results[:10]):
        print(f"\n{i+1}. Offset {r['offset']} ({r['operation']}) - Score: {r['score']}")
        print(f"   Words found: {', '.join(r['words'][:8])}")
        print(f"   Preview: {r['preview'][:60]}...")
        print(f"   Key starts: '{r['key_preview']}'...")
    
    return best_results[:10] if best_results else None

def main():
    print("SELF-RELIANCE RUNNING KEY ATTACK")
    print("=" * 70)
    
    # Load Self-Reliance
    sr_text = load_self_reliance()
    if not sr_text:
        return
    
    print(f"Loaded Self-Reliance: {len(sr_text)} characters")
    
    # Convert to indices
    sr_indices = text_to_indices(sr_text)
    print(f"Converted to {len(sr_indices)} Gematria indices")
    print(f"First 50 chars: {sr_text[:50]}")
    
    # Test on unsolved pages
    unsolved_pages = [17, 18, 19, 20, 21, 22, 23, 24, 25]
    
    all_results = {}
    for page_num in unsolved_pages:
        results = test_self_reliance_key(page_num, sr_text, sr_indices, max_offsets=2000)
        if results:
            all_results[page_num] = results
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - Best matches per page")
    print("=" * 70)
    
    for page_num, results in all_results.items():
        if results and results[0]['score'] > 200:
            print(f"\nPage {page_num}: Score {results[0]['score']}")
            print(f"  Offset: {results[0]['offset']}")
            print(f"  Words: {results[0]['words']}")

if __name__ == '__main__':
    main()

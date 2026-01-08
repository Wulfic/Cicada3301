#!/usr/bin/env python3
"""
AUTOKEY CIPHER ATTACK (Version 2)

The autokey cipher uses plaintext as part of the running key:
- Start with a primer (seed key)
- Each subsequent key character is the previous plaintext character

Formula: 
  plain[i] = (cipher[i] - key[i]) mod 29
  key[0...n] = primer + plain[0...len-n]

This is much harder to crack because the key depends on the plaintext itself.
"""

import os
from pathlib import Path
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

ENGLISH_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
    'WE', 'THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 
    'WAS', 'ONE', 'OUR', 'OUT', 'ARE', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY',
    'NEW', 'NOW', 'OLD', 'SAY', 'SHE', 'TOO', 'TWO', 'WAY', 'WHO', 'YET',
    'THY', 'YEA', 'NAY', 'FIND', 'PATH', 'SEEK', 'TRUTH', 'LIGHT', 'WITHIN',
    'DIVINITY', 'EMERGE', 'SURFACE', 'PARABLE', 'INSTAR', 'CIRCUMFERENCE',
    'MUST', 'SHED', 'WITH', 'THIS', 'THAT', 'FROM', 'HAVE', 'BEEN', 'WILL',
    'EACH', 'MAKE', 'LIKE', 'THEM', 'THEN', 'THAN', 'ONLY', 'OVER', 'INTO',
    'HATH', 'DOTH', 'THOU', 'THEE', 'THINE', 'SHALL', 'WISDOM', 'KNOWLEDGE'
}

def load_runes(page_num):
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_rune_stream(rune_text):
    return [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]

def parse_words(rune_text):
    words = []
    current_word = []
    for char in rune_text:
        if char in RUNE_MAP:
            current_word.append(RUNE_MAP[char])
        elif char in '-. \n\r':
            if current_word:
                words.append(current_word)
                current_word = []
    if current_word:
        words.append(current_word)
    return words

def text_to_indices(text):
    result = []
    i = 0
    while i < len(text):
        for digraph in ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO']:
            if text[i:i+len(digraph)].upper() == digraph:
                result.append(LETTER_TO_IDX[digraph])
                i += len(digraph)
                break
        else:
            if text[i].upper() in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[text[i].upper()])
            i += 1
    return result

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def autokey_decrypt(cipher, primer_indices):
    """Decrypt using autokey cipher."""
    plain = []
    
    for i in range(len(cipher)):
        if i < len(primer_indices):
            key = primer_indices[i]
        else:
            key = plain[i - len(primer_indices)]
        
        plain_char = (cipher[i] - key) % 29
        plain.append(plain_char)
    
    return plain

def score_decryption(plain_indices, words):
    """Score based on recognized English words."""
    score = 0
    found_words = []
    
    pos = 0
    for word_cipher in words:
        word_len = len(word_cipher)
        if pos + word_len > len(plain_indices):
            break
        word_plain = plain_indices[pos:pos+word_len]
        word_text = indices_to_text(word_plain)
        
        if word_text.upper() in ENGLISH_WORDS:
            score += len(word_text) * 100
            found_words.append(word_text)
        
        pos += word_len
    
    return score, found_words

def try_primers(page_num):
    """Try various primers on a page."""
    
    rune_text = load_runes(page_num)
    if not rune_text:
        return []
    
    cipher = parse_rune_stream(rune_text)
    words = parse_words(rune_text)
    
    primers_text = [
        'DIVINITY', 'PARABLE', 'INSTAR', 'EMERGE', 'WITHIN', 'SURFACE',
        'CIRCUMFERENCE', 'TRUTH', 'WISDOM', 'KNOWLEDGE', 'LIGHT', 'PATH',
        'SEEK', 'FIND', 'PRIMES', 'CICADA', 'PILGRIM', 'JOURNEY',
        'THE', 'AND', 'FOR', 'THAT', 'THIS', 'WITH',
        'A', 'I', 'IN', 'OF', 'TO', 'BE', 'PI', 'PHI', 'E'
    ]
    
    # Also single runes
    for letter in LETTERS:
        primers_text.append(letter)
    
    results = []
    
    for primer_text in primers_text:
        try:
            primer_idx = text_to_indices(primer_text)
            if not primer_idx:
                continue
            plain = autokey_decrypt(cipher, primer_idx)
            score, found = score_decryption(plain, words)
            
            if score > 0:
                results.append({
                    'primer': primer_text,
                    'score': score,
                    'words': found,
                    'preview': indices_to_text(plain[:50])
                })
        except Exception as e:
            pass
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def main():
    print("=" * 70)
    print("AUTOKEY CIPHER ATTACK")
    print("=" * 70)
    
    for page_num in [8, 9, 10, 43, 51, 45]:
        print(f"\n{'='*70}")
        print(f"PAGE {page_num}")
        print("=" * 70)
        
        results = try_primers(page_num)
        
        if results:
            for r in results[:5]:
                print(f"\nPrimer: {r['primer']}")
                print(f"  Score: {r['score']}")
                print(f"  Words: {', '.join(r['words'][:10])}")
                print(f"  Preview: {r['preview']}")
        else:
            print("No English words found with any primer")

if __name__ == '__main__':
    main()

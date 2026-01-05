#!/usr/bin/env python3
"""
FIND ENGLISH WORDS IN DECRYPTED PAGES

The analysis shows "THE" and "THEO" appearing multiple times in Page 28.
Let's search for all English word occurrences at different offsets.
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

# English words to search for
ENGLISH_WORDS = [
    'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 'THERE',
    'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL', 'EACH',
    'MAKE', 'LIKE', 'INTO', 'TIME', 'VERY', 'JUST', 'KNOW', 'TAKE', 'COME',
    'COULD', 'GOOD', 'SOME', 'THEM', 'THESE', 'THEN', 'NOW', 'WAY', 'MAY',
    'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 'SHED',
    'CIRCUMFERENCE', 'TUNNEL', 'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED',
    'PRIMES', 'TOTIENT', 'FUNCTION', 'COMMAND', 'INSTRUCTION', 'CONSUME',
    'YOU', 'WE', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
    'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT', 'CAN',
    'FOR', 'ARE', 'BUT', 'HIS', 'HER', 'ITS', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY'
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

def decrypt_with_offset(cipher_indices, offset):
    """Decrypt using master key at given offset"""
    result = []
    for i, c in enumerate(cipher_indices):
        k = MASTER_KEY[(i + offset) % 95]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def find_words(text, words):
    """Find all occurrences of words in text"""
    found = []
    for word in words:
        pos = 0
        while True:
            pos = text.find(word, pos)
            if pos == -1:
                break
            found.append((pos, word))
            pos += 1
    return sorted(found)

def main():
    pages = load_pages()
    
    print("=" * 70)
    print("SEARCHING FOR ENGLISH WORDS IN DECRYPTED PAGES")
    print("=" * 70)
    
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    for pg_num in unsolved:
        if pg_num not in pages:
            continue
        
        cipher_indices = [rune_to_idx(r) for r in pages[pg_num]]
        
        print(f"\n{'='*60}")
        print(f"PAGE {pg_num}")
        print(f"{'='*60}")
        
        best_offset = None
        best_words = []
        
        for offset in range(95):
            text = decrypt_with_offset(cipher_indices, offset)
            found = find_words(text, ENGLISH_WORDS)
            
            # Score: longer words are worth more
            score = sum(len(w) for _, w in found)
            
            if len(found) >= 3:  # At least 3 word matches
                if not best_offset or score > sum(len(w) for _, w in best_words):
                    best_offset = offset
                    best_words = found
        
        if best_words:
            text = decrypt_with_offset(cipher_indices, best_offset)
            print(f"Best offset: {best_offset}")
            print(f"Words found: {[(pos, w) for pos, w in best_words[:10]]}")
            print(f"Text: {text[:80]}...")
            
            # Show context around found words
            print("\nWord contexts:")
            for pos, word in best_words[:5]:
                start = max(0, pos - 10)
                end = min(len(text), pos + len(word) + 10)
                context = text[start:end]
                word_start = pos - start
                print(f"  ...{context[:word_start]}[{word}]{context[word_start+len(word):]}")
        else:
            # Show best single word findings
            print("No cluster of words found. Checking individual best matches...")
            for offset in range(95):
                text = decrypt_with_offset(cipher_indices, offset)
                for word in ['DIVINITY', 'PARABLE', 'WISDOM', 'SACRED', 'TRUTH', 'KNOWLEDGE']:
                    if word in text:
                        pos = text.find(word)
                        print(f"  Offset {offset}: Found '{word}' at position {pos}")
                        context = text[max(0,pos-10):pos+len(word)+10]
                        print(f"    Context: ...{context}...")

    print("\n" + "=" * 70)
    print("DETAILED ANALYSIS OF PAGE 28 (best candidate)")
    print("=" * 70)
    
    if 28 in pages:
        cipher = [rune_to_idx(r) for r in pages[28]]
        
        print("\nSearching ALL offsets for word-rich decryptions...")
        results = []
        
        for offset in range(95):
            text = decrypt_with_offset(cipher, offset)
            found = find_words(text, ENGLISH_WORDS)
            score = sum(len(w) for _, w in found)
            unique_words = set(w for _, w in found)
            results.append((score, offset, found, text, unique_words))
        
        results.sort(reverse=True)
        
        print("\nTop 5 word-rich offsets:")
        for score, offset, found, text, unique_words in results[:5]:
            print(f"\nOffset {offset}: score={score}, unique words={len(unique_words)}")
            print(f"  Words: {list(unique_words)}")
            print(f"  Text: {text[:70]}...")

if __name__ == "__main__":
    main()

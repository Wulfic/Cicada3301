#!/usr/bin/env python3
"""
DETAILED PAGE 28 ANALYSIS

Page 28 at offset 13 shows: "OEWTHEAAEMTHOXOIOLYCBXXBBREA..."
This has THE scattered throughout. Let's analyze more deeply.
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

def decrypt_with_offset(cipher_indices, offset):
    result = []
    for i, c in enumerate(cipher_indices):
        k = MASTER_KEY[(i + offset) % 95]
        p = (c - k) % 29
        result.append(idx_to_letter(p))
    return ''.join(result)

def find_words(text, min_len=3):
    """Find all English words in text at all positions"""
    # Extended word list
    WORDS = {
        'THE', 'AND', 'THAT', 'THIS', 'WITH', 'FROM', 'WHICH', 'THEIR', 
        'HAVE', 'BEEN', 'WERE', 'THEY', 'WHAT', 'WHEN', 'YOUR', 'WILL',
        'PARABLE', 'INSTAR', 'DIVINITY', 'WITHIN', 'EMERGE', 'SURFACE', 
        'WISDOM', 'TRUTH', 'KNOWLEDGE', 'SACRED', 'PRIMES', 'TOTIENT',
        'YOU', 'ALL', 'ONE', 'SELF', 'BEING', 'FIND', 'OUR', 'OWN',
        'UNTO', 'UPON', 'FIRST', 'LAST', 'END', 'BEGIN', 'MUST', 'NOT',
        'ARE', 'BUT', 'HAS', 'HAD', 'WHO', 'HOW', 'WHY', 'CAN', 'FOR',
        'THERE', 'COME', 'TIME', 'IDEA', 'EGOS', 'THEN', 'DIVINE', 'REBORN',
        'LIKE', 'TUNNELING', 'CIRCUMFERENCE', 'COMMAND', 'EYES', 'DEAD',
        'STILL', 'SEE', 'REMAIN', 'AWAKE', 'ABANDON', 'SHED', 'SKIN',
        'BEFORE', 'BODY', 'COVERED', 'SOME', 'EACH', 'MANY', 'TIMES',
        'HEAR', 'THEM', 'THEE', 'THINE', 'HERE', 'WE', 'OF'
    }
    
    found = []
    for word in WORDS:
        if len(word) >= min_len:
            idx = 0
            while True:
                pos = text.find(word, idx)
                if pos == -1:
                    break
                found.append((pos, word))
                idx = pos + 1
    
    return sorted(found)

def main():
    pages = load_pages()
    
    print("=" * 80)
    print("PAGE 28 DETAILED ANALYSIS")
    print("=" * 80)
    
    cipher = [rune_to_idx(r) for r in pages[28]]
    text = decrypt_with_offset(cipher, 13)
    
    print(f"Length: {len(text)} characters")
    print(f"\nFull decrypted text:")
    
    # Print with position markers every 50 chars
    for i in range(0, len(text), 50):
        chunk = text[i:i+50]
        print(f"{i:3}: {chunk}")
    
    print("\n" + "-" * 60)
    print("WORDS FOUND:")
    print("-" * 60)
    
    words_found = find_words(text)
    for pos, word in words_found:
        # Show context
        start = max(0, pos - 5)
        end = min(len(text), pos + len(word) + 5)
        context = text[start:end]
        word_start = pos - start
        highlighted = context[:word_start] + f"[{word}]" + context[word_start + len(word):]
        print(f"  Position {pos:3}: '{word}' -> ...{highlighted}...")
    
    print("\n" + "=" * 80)
    print("TRYING TO RECONSTRUCT SENTENCES")
    print("=" * 80)
    
    # Mark word positions
    word_mask = [False] * len(text)
    for pos, word in words_found:
        for i in range(pos, min(pos + len(word), len(text))):
            word_mask[i] = True
    
    # Calculate coverage
    coverage = sum(word_mask) / len(text) * 100
    print(f"English word coverage: {coverage:.1f}%")
    
    # Try to read just the English words
    current_pos = 0
    sentence_parts = []
    for pos, word in words_found:
        if pos >= current_pos:
            sentence_parts.append(word)
            current_pos = pos + len(word)
    
    print(f"\nExtracted words in sequence: {' '.join(sentence_parts)}")
    
    print("\n" + "=" * 80)
    print("COMPARING WITH OTHER OFFSETS")
    print("=" * 80)
    
    # Try a few offsets and compare word coverage
    for offset in [0, 1, 13, 59, 91]:
        text = decrypt_with_offset(cipher, offset)
        words_found = find_words(text)
        total_chars = sum(len(w) for _, w in words_found)
        
        print(f"Offset {offset:2}: {len(words_found):2} word occurrences, {total_chars:3} chars covered")
        if len(words_found) > 0:
            words_str = ', '.join(w for _, w in words_found[:10])
            print(f"  Words: {words_str}{'...' if len(words_found) > 10 else ''}")
    
    print("\n" + "=" * 80)
    print("LETTER FREQUENCY ANALYSIS")
    print("=" * 80)
    
    text = decrypt_with_offset(cipher, 13)
    
    # Count letters
    from collections import Counter
    counter = Counter(text.replace('TH', '').replace('NG', '').replace('EA', '').replace('OE', '').replace('AE', '').replace('IA', '').replace('EO', ''))
    
    # Expected English frequencies (rough)
    expected = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 
                'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
                'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5}
    
    print("\nActual frequencies vs Expected English:")
    total = len(text)
    for letter in sorted(counter, key=counter.get, reverse=True)[:15]:
        actual = counter[letter] / total * 100
        exp = expected.get(letter, 0)
        diff = actual - exp
        print(f"  {letter}: {actual:5.1f}% (expected: {exp:5.1f}%, diff: {diff:+5.1f}%)")

if __name__ == "__main__":
    main()

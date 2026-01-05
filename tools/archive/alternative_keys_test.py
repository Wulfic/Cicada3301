#!/usr/bin/env python3
"""
ALTERNATIVE KEY SOURCES
=======================

Try deriving keys from OTHER sources:
1. Self-Reliance by Emerson (extracted earlier)
2. The Parable itself as key
3. Page 56 formula application
4. Prime sequences
5. Fibonacci sequences
6. Pi digits
"""

import re
import numpy as np
from pathlib import Path
import math

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

# The Parable text
PARABLE = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

# Pi digits
PI_DIGITS = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"

# Fibonacci sequence mod 29
def get_fibonacci(n):
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return [f % 29 for f in fib]

# Self-Reliance excerpt (first few hundred chars)
SELF_RELIANCE = """THEREISATIMEINEDUCATIONWHENONEARRIVESATTHECONVICTIONTHATENVISTHEIMITATIONISSUICIDE
THATONEMUSTACCEPTHIMSELFFORHISBETTERFORBETTERASNOPORTIONTHOUGHABROADTHEGOODOFTHEUNIVERSEIS
TENDINGTHEEYEWASPLACEDWHEREONERAYSHOULDFALLTHATITMIGHTEMPATHIZEANDTELLOFTHEPARTICULARAY"""

def text_to_indices(text):
    """Convert text to indices, handling 2-char runes"""
    indices = []
    i = 0
    text = text.upper().replace(' ', '')
    while i < len(text):
        if i+1 < len(text):
            two_char = text[i:i+2]
            if two_char in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[two_char])
                i += 2
                continue
        if text[i] in LETTER_TO_IDX:
            indices.append(LETTER_TO_IDX[text[i]])
        i += 1
    return np.array(indices, dtype=np.int32)

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def extend_key(key, length):
    return np.tile(key, (length // len(key) + 1))[:length]

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
            pages[page_num] = runes_to_indices(runes_only)
    return pages

def score_english(text):
    ENGLISH_WORDS = {
        'PARABLE': 4, 'INSTAR': 4, 'DIVINITY': 4, 'EMERGE': 4, 'CIRCUMFERENCE': 4,
        'WISDOM': 4, 'TRUTH': 4, 'PRIME': 4, 'SACRED': 4, 'DIVINE': 4,
        'WITHIN': 3, 'SURFACE': 3, 'TUNNELING': 3, 'SHED': 3,
        'THE': 2, 'AND': 2, 'THAT': 2, 'HAVE': 2, 'WITH': 2, 'THIS': 2,
        'AN': 1, 'BE': 1, 'IT': 1, 'IS': 1, 'TO': 1, 'OF': 1, 'IN': 1, 
        'HE': 1, 'WE': 1, 'OR': 1, 'FOR': 1, 'NOT': 1, 'ALL': 1,
    }
    text_upper = text.upper()
    score = 0
    words_found = []
    for word, weight in ENGLISH_WORDS.items():
        count = text_upper.count(word)
        if count > 0:
            score += count * len(word) * weight
            words_found.append(f"{word}({count})")
    return score, words_found

def main():
    print("="*70)
    print("🔬 ALTERNATIVE KEY SOURCES TEST")
    print("="*70)
    
    pages = load_all_pages()
    skip_pages = [0, 54, 56, 57]
    test_pages = {k: v for k, v in pages.items() if k not in skip_pages}
    
    # Generate different keys
    keys = {}
    
    # 1. Parable as key
    keys['parable'] = text_to_indices(PARABLE)
    print(f"\n1. Parable key: {len(keys['parable'])} chars")
    
    # 2. Self-Reliance as key
    keys['self_reliance'] = text_to_indices(SELF_RELIANCE)
    print(f"2. Self-Reliance key: {len(keys['self_reliance'])} chars")
    
    # 3. Pi digits as key
    pi_key = np.array([int(d) % 29 for d in PI_DIGITS], dtype=np.int32)
    keys['pi_digits'] = pi_key
    print(f"3. Pi digits key: {len(keys['pi_digits'])} chars")
    
    # 4. Fibonacci mod 29
    keys['fibonacci'] = np.array(get_fibonacci(200), dtype=np.int32)
    print(f"4. Fibonacci key: {len(keys['fibonacci'])} chars")
    
    # 5. Prime sequence mod 29
    primes_extended = []
    n = 2
    while len(primes_extended) < 200:
        if all(n % p != 0 for p in range(2, int(n**0.5) + 1)):
            primes_extended.append(n % 29)
        n += 1
    keys['primes'] = np.array(primes_extended, dtype=np.int32)
    print(f"5. Primes key: {len(keys['primes'])} chars")
    
    # 6. "CIRCUMFERENCE" repeated
    keys['circumference'] = text_to_indices("CIRCUMFERENCE" * 20)
    print(f"6. CIRCUMFERENCE key: {len(keys['circumference'])} chars")
    
    # 7. "DIVINITYWITHIN" repeated
    keys['divinity'] = text_to_indices("DIVINITYWITHIN" * 15)
    print(f"7. DIVINITY key: {len(keys['divinity'])} chars")
    
    # 8. 2*pi digits
    two_pi_str = "62831853071795864769252867665590057683943387987502116419498891846156328125724179972560696506842341359"
    keys['two_pi'] = np.array([int(d) % 29 for d in two_pi_str], dtype=np.int32)
    print(f"8. 2π digits key: {len(keys['two_pi'])} chars")
    
    print("\n" + "="*70)
    print("TESTING ALL KEYS ON ALL PAGES")
    print("="*70)
    
    all_results = []
    
    for key_name, key in keys.items():
        print(f"\n--- Key: {key_name} ---")
        
        for pg_num, pg_idx in sorted(test_pages.items()):
            # Extend key
            ext_key = extend_key(key, len(pg_idx))
            
            # Try subtraction
            decrypted_sub = (pg_idx - ext_key) % 29
            text_sub = indices_to_text(decrypted_sub)
            score_sub, words_sub = score_english(text_sub)
            
            if score_sub >= 50:
                all_results.append({
                    'key': key_name,
                    'page': pg_num,
                    'op': 'sub',
                    'score': score_sub,
                    'words': words_sub[:6],
                    'text': text_sub[:80]
                })
                print(f"  Page {pg_num} (sub): Score={score_sub}, {', '.join(words_sub[:4])}")
            
            # Try XOR
            decrypted_xor = (pg_idx ^ ext_key) % 29
            text_xor = indices_to_text(decrypted_xor)
            score_xor, words_xor = score_english(text_xor)
            
            if score_xor >= 50:
                all_results.append({
                    'key': key_name,
                    'page': pg_num,
                    'op': 'xor',
                    'score': score_xor,
                    'words': words_xor[:6],
                    'text': text_xor[:80]
                })
                print(f"  Page {pg_num} (xor): Score={score_xor}, {', '.join(words_xor[:4])}")
            
            # Try addition
            decrypted_add = (pg_idx + ext_key) % 29
            text_add = indices_to_text(decrypted_add)
            score_add, words_add = score_english(text_add)
            
            if score_add >= 50:
                all_results.append({
                    'key': key_name,
                    'page': pg_num,
                    'op': 'add',
                    'score': score_add,
                    'words': words_add[:6],
                    'text': text_add[:80]
                })
                print(f"  Page {pg_num} (add): Score={score_add}, {', '.join(words_add[:4])}")
    
    # Summary
    print("\n" + "="*70)
    print("🏆 TOP RESULTS BY ALTERNATIVE KEYS")
    print("="*70)
    
    all_results.sort(key=lambda x: -x['score'])
    
    for r in all_results[:20]:
        print(f"\n{r['key'].upper()} on Page {r['page']} ({r['op']}): Score {r['score']}")
        print(f"   Words: {', '.join(r['words'])}")
        print(f"   Text: {r['text']}...")
    
    # Key effectiveness
    print("\n" + "="*70)
    print("📈 KEY EFFECTIVENESS SUMMARY")
    print("="*70)
    
    from collections import defaultdict
    key_scores = defaultdict(list)
    for r in all_results:
        key_scores[r['key']].append(r['score'])
    
    for key_name in sorted(key_scores.keys(), key=lambda x: -max(key_scores[x]) if key_scores[x] else 0):
        scores = key_scores[key_name]
        if scores:
            print(f"   {key_name:20s}: {len(scores):3d} results, max={max(scores)}, avg={np.mean(scores):.1f}")

if __name__ == "__main__":
    main()

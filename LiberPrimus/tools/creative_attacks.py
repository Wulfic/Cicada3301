#!/usr/bin/env python3
"""
CREATIVE LIBER PRIMUS ATTACKS

Thinking outside the box with multiple approaches:
1. Use solved page keywords as Vigenère keys
2. Try totient-based decryption (Page 05 hint)
3. Book cipher using solved pages as source
4. Combined keyword autokey
"""

import os
from pathlib import Path
from itertools import product

# Gematria Primus
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

# Prime values for each rune (from Gematria Primus)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Euler's totient for primes: φ(p) = p - 1
TOTIENTS = [p - 1 for p in PRIMES]

# Keywords from solved pages
SOLVED_KEYWORDS = [
    'DIVINITY',
    'FIRFUMFERENFE', 
    'CIRCUMFERENCE',
    'INSTAR',
    'PILGRIM',
    'SACRED',
    'PRIMES',
    'TOTIENT',
    'PARABLE',
    'WISDOM',
    'KOAN',
    'CICADA',
    'CONSUMPTION',
    'INTERCONNECTEDNESS',
    'WARNING',
    'WELCOME',
    'JOURNEY',
    'END',
    'TRUTH',
    'EMERGE',
    'SURFACE',
]

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
    'SOME', 'END', 'LIKE', 'INTO', 'THROUGH', 'GREAT', 'TOWARD'
}

def text_to_indices(text):
    """Convert text to Gematria indices."""
    result = []
    i = 0
    text = text.upper()
    digraphs = ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO']
    
    while i < len(text):
        matched = False
        for digraph in digraphs:
            if text[i:i+len(digraph)] == digraph and digraph in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[digraph])
                i += len(digraph)
                matched = True
                break
        
        if not matched:
            char = text[i]
            if char in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[char])
            elif char == 'K':
                result.append(LETTER_TO_IDX['C'])
            elif char == 'Q':
                result.append(LETTER_TO_IDX['C'])
            elif char == 'V':
                result.append(LETTER_TO_IDX['U'])
            elif char == 'Z':
                result.append(LETTER_TO_IDX['S'])
            i += 1
    
    return result

def indices_to_text(indices):
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
    
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    
    words = []
    current = []
    for c in rune_text:
        if c in RUNE_MAP:
            current.append(RUNE_MAP[c])
        elif c in '-. \n\r/•':
            if current:
                words.append(current)
                current = []
    if current:
        words.append(current)
    
    return cipher, words

def decrypt_vigenere(cipher, key_indices):
    """Standard Vigenère decryption (SUB mod 29)."""
    return [(c - key_indices[i % len(key_indices)]) % 29 for i, c in enumerate(cipher)]

def decrypt_vigenere_add(cipher, key_indices):
    """Reverse Vigenère (ADD mod 29)."""
    return [(c + key_indices[i % len(key_indices)]) % 29 for i, c in enumerate(cipher)]

def decrypt_totient(cipher):
    """
    Use totient values as key: p[i] = (c[i] - φ(prime[i])) mod 29
    Based on Page 05: "THE TOTIENT FUNCTION IS SACRED"
    """
    plain = []
    for i, c in enumerate(cipher):
        # Use sequential primes' totients
        totient = TOTIENTS[i % len(TOTIENTS)]
        plain.append((c - totient) % 29)
    return plain

def decrypt_prime_index(cipher):
    """Use prime indices as key."""
    plain = []
    for i, c in enumerate(cipher):
        # Prime at position i
        prime = PRIMES[i % len(PRIMES)]
        plain.append((c - (prime % 29)) % 29)
    return plain

def decrypt_autokey(cipher, primer):
    """Autokey cipher where key extends with plaintext."""
    plain = []
    primer_indices = text_to_indices(primer)
    
    for i, c in enumerate(cipher):
        if i < len(primer_indices):
            k = primer_indices[i]
        else:
            k = plain[i - len(primer_indices)]
        plain.append((c - k) % 29)
    
    return plain

def score_plaintext(plain_indices, word_boundaries):
    """Score by counting English words."""
    score = 0
    words_found = []
    
    pos = 0
    for word_indices in word_boundaries:
        wlen = len(word_indices)
        if pos + wlen > len(plain_indices):
            break
        
        word_text = indices_to_text(plain_indices[pos:pos+wlen])
        
        if word_text in COMMON_WORDS:
            score += len(word_text) * 100
            words_found.append(word_text)
        
        pos += wlen
    
    return score, words_found

def test_all_approaches(page_num):
    """Test multiple approaches on a page."""
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - CREATIVE ATTACK SUITE")
    print("=" * 70)
    
    cipher, words = load_page_runes(page_num)
    if cipher is None:
        print("Could not load page")
        return
    
    print(f"Cipher length: {len(cipher)}, Words: {len(words)}")
    
    results = []
    
    # 1. Test all solved keywords as Vigenère keys
    print("\n--- Testing Solved Keywords ---")
    for keyword in SOLVED_KEYWORDS:
        key_indices = text_to_indices(keyword)
        if not key_indices:
            continue
        
        for op_name, decrypt_fn in [('SUB', decrypt_vigenere), ('ADD', decrypt_vigenere_add)]:
            plain = decrypt_fn(cipher, key_indices)
            score, found = score_plaintext(plain, words)
            
            if score > 0 or len(found) > 0:
                results.append({
                    'method': f'Vigenère-{op_name}',
                    'key': keyword,
                    'score': score,
                    'words': found,
                    'preview': indices_to_text(plain[:50])
                })
    
    # 2. Test totient-based decryption
    print("--- Testing Totient Function ---")
    plain = decrypt_totient(cipher)
    score, found = score_plaintext(plain, words)
    results.append({
        'method': 'Totient',
        'key': 'φ(prime[i])',
        'score': score,
        'words': found,
        'preview': indices_to_text(plain[:50])
    })
    
    # 3. Test prime index decryption
    print("--- Testing Prime Index ---")
    plain = decrypt_prime_index(cipher)
    score, found = score_plaintext(plain, words)
    results.append({
        'method': 'PrimeIndex',
        'key': 'prime[i] mod 29',
        'score': score,
        'words': found,
        'preview': indices_to_text(plain[:50])
    })
    
    # 4. Test autokey with keywords as primer
    print("--- Testing Autokey ---")
    for keyword in ['DIVINITY', 'FIRFUMFERENFE', 'INSTAR', 'CICADA', 'PARABLE', 'THE', 'WARNING']:
        plain = decrypt_autokey(cipher, keyword)
        score, found = score_plaintext(plain, words)
        
        if score > 0:
            results.append({
                'method': 'Autokey',
                'key': keyword,
                'score': score,
                'words': found,
                'preview': indices_to_text(plain[:50])
            })
    
    # Sort and display results
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n--- TOP RESULTS ---")
    for i, r in enumerate(results[:15]):
        if r['score'] > 0:
            print(f"\n{i+1}. {r['method']} / Key: {r['key']}")
            print(f"   Score: {r['score']}")
            print(f"   Words: {', '.join(r['words'][:10])}")
            print(f"   Preview: {r['preview']}")
    
    return results

def main():
    print("CREATIVE LIBER PRIMUS ATTACK SUITE")
    print("=" * 70)
    
    # Test on unsolved pages
    for page_num in [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 40, 50]:
        results = test_all_approaches(page_num)

if __name__ == '__main__':
    main()

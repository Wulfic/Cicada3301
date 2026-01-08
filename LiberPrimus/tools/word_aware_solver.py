#!/usr/bin/env python3
"""
COMPREHENSIVE WORD-AWARE SOLVER
================================

Key insights combined:
1. Hyphens (-) in runes = word boundaries in English
2. IP pattern ([10,13]) works well on Pages 2-4
3. Pages contain hints for solving other pages
4. "THE PRIMES ARE SACRED" / "THE TOTIENT FUNCTION IS SACRED"
5. Magic square sum 1033 (prime), 1033 mod 29 = 18 = E

Strategy:
- Decrypt preserving word boundaries
- Try multiple key combinations
- Score based on real English word matches
"""

import os
import re
from collections import Counter
import math

# ============================================================================
# GEMATRIA PRIMUS
# ============================================================================

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
LETTERS = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"]
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}
INDEX_TO_LETTER = {i: L for i, L in enumerate(LETTERS)}

RUNE_DATA = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛂ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

KEY_LENGTHS = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

# English word list (common + archaic)
ENGLISH_WORDS = {
    # Common short words
    'A', 'I', 'OF', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'AT', 'BY', 'WE', 'AN', 'OR', 'ON', 'IF', 'NO', 'SO', 'DO', 'UP', 'HE', 'ME', 'MY',
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GOD', 'WAY', 'MAY', 'SAY', 'END', 'LAW', 'OWN',
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'FIND', 'MANY', 'MOST', 'SOME', 'THAN', 'THEM', 'THEN', 'WHAT', 'WHEN', 'EACH', 'SELF', 'PATH', 'MUST', 'LIKE', 'MAKE', 'ONLY', 'OVER', 'SUCH', 'INTO', 'KNOW', 'JUST', 'COME', 'GOOD', 'ALSO',
    'THEIR', 'WHICH', 'THERE', 'THESE', 'WOULD', 'ABOUT', 'COULD', 'OTHER', 'BEING', 'TRUTH', 'THING', 'WORLD', 'GREAT', 'FIRST', 'AFTER', 'THOSE', 'NEVER', 'WHERE', 'EVERY', 'SHALL', 'UNDER',
    # Archaic/Old English
    'THOU', 'THEE', 'THY', 'THINE', 'HATH', 'DOTH', 'GOETH', 'DOETH', 'SAITH', 'SEEKETH', 'FINDETH', 'COMETH', 'SPEAKETH',
    'UNTO', 'UPON', 'THENCE', 'HENCE', 'WHENCE', 'WHILST', 'AMONGST', 'VERILY', 'FORSOOTH', 'BEHOLD', 'HEREIN', 'THEREIN', 'WHEREIN',
    # Cicada themes
    'WISDOM', 'DIVINE', 'SACRED', 'SPIRIT', 'WITHIN', 'EMERGE', 'INSTAR', 'PILGRIM', 'JOURNEY', 'SEEKER', 'CIPHER', 'SECRET', 'HIDDEN', 'PRIMUS', 'LIBER', 'CICADA', 'DIVINITY', 'CIRCUMFERENCE', 'INSTRUCTION',
    # From solved pages
    'WELCOME', 'TOWARD', 'THINGS', 'REALITY', 'OUTSIDE', 'SHADOWS', 'VOID', 'CARNAL', 'AETHEREAL', 'BUFFERS', 'OBSCURA', 'FORM', 'MOBIUS', 'ANALOG', 'MOURNFUL', 'CABAL',
    'CONSUMPTION', 'PRESERVATION', 'ADHERENCE', 'PRIMALITY', 'INTELLIGENCE', 'HOLY', 'KOAN', 'MASTER', 'STUDENT'
}

def euler_totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def text_to_indices(text):
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        matched = False
        for length in [2, 1]:
            if i + length <= len(text):
                segment = text[i:i+length]
                if segment in LETTER_TO_INDEX:
                    indices.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return indices

def indices_to_text(indices):
    return "".join(INDEX_TO_LETTER.get(i, '?') for i in indices)

def parse_rune_file_with_words(filepath):
    """Parse runes preserving word boundaries"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    words = []
    current_word = []
    global_pos = 0
    
    for char in content:
        if char in RUNE_DATA:
            current_word.append((RUNE_DATA[char], global_pos))
            global_pos += 1
        elif char in '-\n ':
            if current_word:
                words.append({
                    'indices': [c[0] for c in current_word],
                    'positions': [c[1] for c in current_word],
                    'start': current_word[0][1]
                })
                current_word = []
        # Skip other markers like . & $ /
    
    if current_word:
        words.append({
            'indices': [c[0] for c in current_word],
            'positions': [c[1] for c in current_word],
            'start': current_word[0][1]
        })
    
    return words

def decrypt_word(word_data, key_length, second_key=None, second_op='add'):
    """Decrypt a single word"""
    indices = word_data['indices']
    positions = word_data['positions']
    
    # First layer: SUB with position-based key
    first_layer = [(idx - (pos % key_length)) % 29 for idx, pos in zip(indices, positions)]
    
    # Second layer if provided
    if second_key:
        result = []
        for i, (idx, pos) in enumerate(zip(first_layer, positions)):
            k = second_key[pos % len(second_key)]
            if second_op == 'add':
                result.append((idx + k) % 29)
            else:
                result.append((idx - k) % 29)
        return result
    
    return first_layer

def score_word_match(text):
    """Check if text matches an English word"""
    text = text.upper()
    if text in ENGLISH_WORDS:
        return len(text) * 10  # Longer words score more
    # Partial match bonus for starts
    for word in ENGLISH_WORDS:
        if word.startswith(text) and len(text) >= 3:
            return len(text) * 2
    return 0

def find_best_key_for_page(words, key_length, page_num):
    """Try various keys and find best match"""
    
    # Keys to try
    test_keys = [
        (None, None, "No second layer"),
        ([10, 13], 'add', "IP add"),
        ([13, 10], 'add', "PI add"),
        ([10, 13], 'sub', "IP sub"),
        ([13, 10], 'sub', "PI sub"),
    ]
    
    # Add totient-based keys
    phi_key = [euler_totient(i+1) % 29 for i in range(key_length)]
    test_keys.append((phi_key[:20], 'add', "Totient(1..20) add"))
    
    # Add prime-1 keys (totient of primes)
    prime_totient = [(p-1) % 29 for p in PRIMES]
    test_keys.append((prime_totient[:20], 'add', "Prime totient add"))
    
    # Add magic square related
    test_keys.append(([18], 'add', "E shift (1033 mod 29)"))
    
    # Words from solved pages as keys
    for word in ['SHADOWS', 'VOID', 'FORM', 'WISDOM', 'SACRED', 'DIVINITY', 'PILGRIM']:
        w_key = text_to_indices(word)
        test_keys.append((w_key, 'add', f"{word} add"))
        test_keys.append((w_key, 'sub', f"{word} sub"))
    
    results = []
    
    for key, op, name in test_keys:
        total_score = 0
        word_matches = []
        all_text = []
        
        for word_data in words:
            decrypted = decrypt_word(word_data, key_length, key, op)
            text = indices_to_text(decrypted)
            all_text.append(text)
            
            score = score_word_match(text)
            if score > 0:
                word_matches.append(text)
            total_score += score
        
        full_text = ' '.join(all_text)
        the_count = full_text.count('THE')
        
        results.append({
            'name': name,
            'score': total_score,
            'matches': word_matches[:10],
            'the_count': the_count,
            'sample': full_text[:100]
        })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("COMPREHENSIVE WORD-AWARE SOLVER")
    print("=" * 70)
    print()
    print("Key insight: Hyphen-separated rune groups = English words")
    print()
    
    for page_num in range(5):
        rune_path = os.path.join(base_path, '..', 'pages', f'page_{page_num:02d}', 'runes.txt')
        if not os.path.exists(rune_path):
            continue
        
        key_length = KEY_LENGTHS[page_num]
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} (key length: {key_length})")
        print("=" * 70)
        
        words = parse_rune_file_with_words(rune_path)
        print(f"Word count: {len(words)}")
        print(f"Word lengths: {[len(w['indices']) for w in words[:15]]}...")
        
        results = find_best_key_for_page(words, key_length, page_num)
        
        print(f"\nTop 5 keys by word match score:")
        for i, r in enumerate(results[:5]):
            print(f"  {i+1}. {r['name']}: score={r['score']}, THE={r['the_count']}")
            if r['matches']:
                print(f"      Matches: {r['matches'][:5]}")
        
        # Show best result details
        best = results[0]
        print(f"\nBest ({best['name']}):")
        print(f"  Sample: {best['sample']}...")
        
        # Also show the actual decrypted words
        print(f"\nFirst 20 words with best key:")
        words_text = []
        for word_data in words[:20]:
            if best['name'] == "No second layer":
                decrypted = decrypt_word(word_data, key_length, None, None)
            else:
                # Parse key from name
                key_name = best['name'].split()[0]
                op = 'add' if 'add' in best['name'] else 'sub'
                if key_name == 'IP':
                    key = [10, 13]
                elif key_name == 'PI':
                    key = [13, 10]
                else:
                    key = text_to_indices(key_name) if key_name not in ['No', 'E', 'Totient(1..20)', 'Prime'] else None
                decrypted = decrypt_word(word_data, key_length, key, op)
            text = indices_to_text(decrypted)
            marker = " <-- MATCH" if text in ENGLISH_WORDS else ""
            words_text.append(f"  {text}{marker}")
        
        for wt in words_text:
            print(wt)

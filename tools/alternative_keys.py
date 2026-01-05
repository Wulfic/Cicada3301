#!/usr/bin/env python3
"""
ALTERNATIVE KEY ANALYSIS - Test if each page uses a different key
derived from page number, or if there's a keyword-based cipher.
Also test known Cicada phrases as potential keys.
"""

import json
from collections import Counter

# =============================================================================
# CONSTANTS
# =============================================================================
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
         'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
NUM_RUNES = 29

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# Known Cicada phrases to try as keys
CICADA_PHRASES = [
    "CICADA",
    "DIVINITY",
    "PRIMES",
    "INSTAR",
    "EMERGE",
    "THREETHREEOHONE",  # 3301
    "LIBER",
    "PRIMUS",
    "LIBERPRIMUS",
    "WISDOM",
    "PARABLE",
    "PILGRIM",
    "INSTRUCTION",
    "CONSUMPTION",
    "COMMAND",
    "CIRCUMFERENCE",
    "SELFDIVINITY",
    "ENLIGHTEN",
]

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i] for i in indices)

def text_to_indices(text):
    """Convert text (like CICADA) to rune indices."""
    indices = []
    i = 0
    while i < len(text):
        # Check for multi-character runes first
        if i + 2 <= len(text) and text[i:i+2] in RUNE_TO_IDX:
            indices.append(RUNE_TO_IDX[text[i:i+2]])
            i += 2
        elif text[i] in RUNE_TO_IDX:
            indices.append(RUNE_TO_IDX[text[i]])
            i += 1
        else:
            i += 1  # Skip unknown characters
    return indices

def score_text(text):
    """Score text by word matches."""
    words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
             'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'OLD', 'SEE',
             'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
             'THERE', 'THEIR', 'ABOUT', 'WOULD', 'THESE', 'OTHER', 'WORDS', 'COULD']
    score = 0
    for word in words:
        count = text.count(word)
        if count > 0:
            score += count * len(word) * 3
    return score

# =============================================================================
# KEY DERIVATION TESTS
# =============================================================================

def test_page_number_key():
    """Test if each page uses a key derived from page number."""
    print("=" * 80)
    print("🔑 TEST: PAGE NUMBER AS KEY MODIFIER")
    print("=" * 80)
    
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        best_score = 0
        best_params = None
        best_text = ""
        
        # Test 1: Page number as rotation offset
        for off in range(29):
            dec = []
            for i, idx in enumerate(indices):
                key_val = MASTER_KEY[(i + page) % 95]  # Use page number as rotation
                plain_idx = (idx - key_val - off) % NUM_RUNES
                dec.append(plain_idx)
            
            text_out = indices_to_text(dec)
            score = score_text(text_out)
            if score > best_score:
                best_score = score
                best_params = {'type': 'page_rotation', 'off': off}
                best_text = text_out
        
        # Test 2: Page number XOR with key
        for rot in range(0, 95, 5):
            for off in range(29):
                dec = []
                for i, idx in enumerate(indices):
                    key_val = (MASTER_KEY[(i + rot) % 95] + page) % 29  # Add page to key
                    plain_idx = (idx - key_val - off) % NUM_RUNES
                    dec.append(plain_idx)
                
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                if score > best_score:
                    best_score = score
                    best_params = {'type': 'page_add_key', 'rot': rot, 'off': off}
                    best_text = text_out
        
        # Test 3: Page number multiplied with position
        for rot in range(0, 95, 5):
            for off in range(29):
                dec = []
                for i, idx in enumerate(indices):
                    key_val = MASTER_KEY[(i * page) % 95]
                    plain_idx = (idx - key_val - off) % NUM_RUNES
                    dec.append(plain_idx)
                
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                if score > best_score:
                    best_score = score
                    best_params = {'type': 'page_mult_pos', 'off': off}
                    best_text = text_out
        
        results.append({
            'page': page, 'score': best_score, 
            'params': best_params, 'text': best_text[:80]
        })
        
        if best_score > 30:
            print(f"\nPage {page}: score={best_score}")
            print(f"  Params: {best_params}")
            print(f"  Text: {best_text[:80]}")
    
    return results

def test_keyword_cipher():
    """Test Vigenère-style cipher with known Cicada phrases as keys."""
    print("\n" + "=" * 80)
    print("🔑 TEST: KEYWORD-BASED CIPHER")
    print("=" * 80)
    
    results = []
    
    for keyword in CICADA_PHRASES:
        key_indices = text_to_indices(keyword)
        if len(key_indices) < 2:
            continue
        
        key_len = len(key_indices)
        
        for page, text in UNSOLVED_PAGES.items():
            indices = unicode_to_indices(text)
            
            # Try subtraction with keyword
            dec = []
            for i, idx in enumerate(indices):
                key_val = key_indices[i % key_len]
                plain_idx = (idx - key_val) % NUM_RUNES
                dec.append(plain_idx)
            
            text_out = indices_to_text(dec)
            score = score_text(text_out)
            
            if score >= 30:
                results.append({
                    'page': page, 'keyword': keyword, 
                    'score': score, 'text': text_out[:80]
                })
                print(f"\n✓ Page {page} + '{keyword}': score={score}")
                print(f"  Text: {text_out[:80]}")
            
            # Try XOR with keyword
            dec = []
            for i, idx in enumerate(indices):
                key_val = key_indices[i % key_len]
                plain_idx = (idx ^ key_val) % NUM_RUNES
                dec.append(plain_idx)
            
            text_out = indices_to_text(dec)
            score = score_text(text_out)
            
            if score >= 30:
                results.append({
                    'page': page, 'keyword': keyword, 'method': 'xor',
                    'score': score, 'text': text_out[:80]
                })
                print(f"\n✓ Page {page} + '{keyword}' (XOR): score={score}")
                print(f"  Text: {text_out[:80]}")
    
    return results

def test_keyword_plus_master():
    """Test combining keyword with master key."""
    print("\n" + "=" * 80)
    print("🔑 TEST: KEYWORD + MASTER KEY COMBINATION")
    print("=" * 80)
    
    results = []
    
    for keyword in CICADA_PHRASES[:5]:  # Test top 5 keywords
        key_indices = text_to_indices(keyword)
        if len(key_indices) < 2:
            continue
        
        keyword_len = len(key_indices)
        
        for page, text in UNSOLVED_PAGES.items():
            indices = unicode_to_indices(text)
            
            for rot in range(0, 95, 10):
                # Combine keyword and master key
                dec = []
                for i, idx in enumerate(indices):
                    master_val = MASTER_KEY[(i + rot) % 95]
                    keyword_val = key_indices[i % keyword_len]
                    combined_key = (master_val + keyword_val) % 29
                    plain_idx = (idx - combined_key) % NUM_RUNES
                    dec.append(plain_idx)
                
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                
                if score >= 40:
                    results.append({
                        'page': page, 'keyword': keyword, 'rot': rot,
                        'score': score, 'text': text_out[:80]
                    })
                    print(f"\n✓ Page {page} + '{keyword}' + rot={rot}: score={score}")
                    print(f"  Text: {text_out[:80]}")
    
    return results

def test_fibonacci_key():
    """Test Fibonacci sequence as key modifier."""
    print("\n" + "=" * 80)
    print("🔑 TEST: FIBONACCI SEQUENCE AS KEY")
    print("=" * 80)
    
    # Generate Fibonacci mod 29
    fib = [1, 1]
    for i in range(200):
        fib.append((fib[-1] + fib[-2]) % 29)
    
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        for fib_start in range(0, 100, 10):
            for off in range(29):
                dec = []
                for i, idx in enumerate(indices):
                    fib_val = fib[fib_start + i]
                    plain_idx = (idx - fib_val - off) % NUM_RUNES
                    dec.append(plain_idx)
                
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                
                if score >= 40:
                    results.append({
                        'page': page, 'fib_start': fib_start, 'off': off,
                        'score': score, 'text': text_out[:80]
                    })
                    print(f"\n✓ Page {page} + Fib[{fib_start}:] + off={off}: score={score}")
                    print(f"  Text: {text_out[:80]}")
    
    return results

def test_prime_sequence_key():
    """Test prime number sequence as key."""
    print("\n" + "=" * 80)
    print("🔑 TEST: PRIME SEQUENCE AS KEY")
    print("=" * 80)
    
    # Generate primes
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [p % 29 for p in range(2, 500) if is_prime(p)]
    
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        for prime_start in range(0, 50, 5):
            for off in range(29):
                dec = []
                for i, idx in enumerate(indices):
                    prime_val = primes[prime_start + i] if (prime_start + i) < len(primes) else 0
                    plain_idx = (idx - prime_val - off) % NUM_RUNES
                    dec.append(plain_idx)
                
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                
                if score >= 40:
                    results.append({
                        'page': page, 'prime_start': prime_start, 'off': off,
                        'score': score, 'text': text_out[:80]
                    })
                    print(f"\n✓ Page {page} + Primes[{prime_start}:] + off={off}: score={score}")
                    print(f"  Text: {text_out[:80]}")
    
    return results

def test_gematria_primus_key():
    """Test using Gematria Primus values as key."""
    print("\n" + "=" * 80)
    print("🔑 TEST: GEMATRIA PRIMUS VALUES AS KEY")
    print("=" * 80)
    
    # Gematria Primus: each rune maps to a prime number
    GEMATRIA_PRIMUS = {
        'F': 2, 'U': 3, 'TH': 5, 'O': 7, 'R': 11, 'C': 13, 'G': 17, 'W': 19,
        'H': 23, 'N': 29, 'I': 31, 'J': 37, 'EO': 41, 'P': 43, 'X': 47, 'S': 53,
        'T': 59, 'B': 61, 'E': 67, 'M': 71, 'L': 73, 'NG': 79, 'OE': 83, 'D': 89,
        'A': 97, 'AE': 101, 'Y': 103, 'IA': 107, 'EA': 109
    }
    
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        for off in range(29):
            dec = []
            for i, idx in enumerate(indices):
                # Use Gematria value of the corresponding key position
                key_rune = RUNES[MASTER_KEY[i % 95]]
                gematria_val = GEMATRIA_PRIMUS.get(key_rune, 0) % 29
                plain_idx = (idx - gematria_val - off) % NUM_RUNES
                dec.append(plain_idx)
            
            text_out = indices_to_text(dec)
            score = score_text(text_out)
            
            if score >= 40:
                results.append({
                    'page': page, 'off': off,
                    'score': score, 'text': text_out[:80]
                })
                print(f"\n✓ Page {page} Gematria + off={off}: score={score}")
                print(f"  Text: {text_out[:80]}")
    
    return results

# =============================================================================
# MAIN
# =============================================================================

def main():
    all_results = []
    
    print("\n" + "=" * 80)
    print("🔬 ALTERNATIVE KEY ANALYSIS")
    print("=" * 80)
    
    results = test_page_number_key()
    all_results.extend(results)
    
    results = test_keyword_cipher()
    all_results.extend(results)
    
    results = test_keyword_plus_master()
    all_results.extend(results)
    
    results = test_fibonacci_key()
    all_results.extend(results)
    
    results = test_prime_sequence_key()
    all_results.extend(results)
    
    results = test_gematria_primus_key()
    all_results.extend(results)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    if all_results:
        all_results.sort(key=lambda x: -x['score'])
        print(f"\nTotal high-scoring results: {len(all_results)}")
        print("\nTop 10:")
        for i, r in enumerate(all_results[:10]):
            print(f"\n#{i+1}: Page {r['page']}, Score {r['score']}")
            print(f"    {r}")
    else:
        print("\nNo high-scoring results found with alternative keys.")
    
    print("\n🎯 ALTERNATIVE KEY ANALYSIS COMPLETE")

if __name__ == '__main__':
    main()

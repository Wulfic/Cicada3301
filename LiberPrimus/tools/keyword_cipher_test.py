#!/usr/bin/env python3
"""
Test known Cicada-related keywords as cipher keys.

Based on findings:
- Keys [10, 7] = I, W found for specific words
- The cipher may use meaningful words as keys
- Test keywords: DIVINITY, WISDOM, PRIMES, LIBER, PRIMUS, etc.
"""

import os
import re
from collections import Counter

# Gematria Primus - 29 runes with values 0-28
GEMATRIA_PRIMUS = [
    ('F', 0), ('U', 1), ('TH', 2), ('O', 3), ('R', 4),
    ('C', 5), ('G', 6), ('W', 7), ('H', 8), ('N', 9),
    ('I', 10), ('J', 11), ('EO', 12), ('P', 13), ('X', 14),
    ('S', 15), ('T', 16), ('B', 17), ('E', 18), ('M', 19),
    ('L', 20), ('NG', 21), ('OE', 22), ('D', 23), ('A', 24),
    ('AE', 25), ('Y', 26), ('IO', 27), ('EA', 28)
]

RUNE_TO_IDX = {rune: idx for rune, idx in GEMATRIA_PRIMUS}
IDX_TO_RUNE = {idx: rune for rune, idx in GEMATRIA_PRIMUS}

# Common English words for scoring
ENGLISH_WORDS = {
    'THE', 'OF', 'AND', 'TO', 'IN', 'IS', 'IT', 'FOR', 'THAT', 'WAS',
    'ON', 'ARE', 'BE', 'HAS', 'WITH', 'AS', 'AT', 'BY', 'FROM', 'OR',
    'AN', 'NOT', 'HAVE', 'THIS', 'BUT', 'HAD', 'HIS', 'THEY', 'HER',
    'WERE', 'BEEN', 'HE', 'SHE', 'WE', 'YOU', 'ALL', 'WILL', 'CAN',
    'ONE', 'THERE', 'THEIR', 'WHAT', 'SO', 'UP', 'OUT', 'IF', 'ABOUT',
    'WHO', 'GET', 'WHICH', 'GO', 'ME', 'WHEN', 'MAKE', 'LIKE', 'TIME',
    'KNOW', 'TAKE', 'COME', 'COULD', 'NOW', 'THAN', 'FIRST', 'BEEN',
    'PATH', 'TRUTH', 'SEEK', 'FIND', 'WISDOM', 'DIVINE', 'LIGHT',
    'DARK', 'PRIME', 'NUMBER', 'CIPHER', 'CODE', 'SECRET', 'MYSTERY',
    'SOME', 'FORM', 'INTO', 'WOULD', 'THEM', 'THESE', 'MAY', 'OTHER',
    'DO', 'NO', 'I', 'A', 'MY', 'THY', 'YE', 'THEE', 'THOU'
}

# Cicada-related keywords to test
CICADA_KEYWORDS = [
    'DIVINITY', 'WISDOM', 'PRIMES', 'LIBER', 'PRIMUS', 'CICADA',
    'TRUTH', 'ENLIGHTEN', 'ILLUMINATI', 'SEEK', 'FIND', 'KNOWLEDGE',
    'PATH', 'PILGRIM', 'JOURNEY', 'MYSTERY', 'DIVINE', 'SACRED',
    'INSTAR', 'EMERGENCE', 'GEMATRIA', 'RUNE', 'RUNES', 'CIPHER',
    'ENCRYPT', 'DECRYPT', 'SECRET', 'HIDDEN', 'AWAKEN', 'AWARE',
    'CONSUME', 'INTELLIGENCE', 'ABILITY', 'YOURSELF', 'COMMAND',
    'SOME', 'DO', 'DIFFER', 'CIRCUMFERENCE', 'CONSUMPTION',
    'IW', 'WI', 'AN', 'ANANSI', 'SPIDER', 'WEB', 'PARABLE',
    'ADMONITION', 'SELF', 'LOSS', 'INSTRUCTION'
]

def parse_runes(text):
    """Parse text into rune indices."""
    runes = []
    text = text.upper().strip()
    i = 0
    while i < len(text):
        # Skip non-rune characters
        if text[i] in ' .-&\n\r':
            i += 1
            continue
        
        # Try digraphs first
        found = False
        for rune, idx in GEMATRIA_PRIMUS:
            if len(rune) > 1 and text[i:].startswith(rune):
                runes.append(idx)
                i += len(rune)
                found = True
                break
        
        if not found:
            # Try single chars
            for rune, idx in GEMATRIA_PRIMUS:
                if len(rune) == 1 and text[i] == rune:
                    runes.append(idx)
                    i += 1
                    found = True
                    break
        
        if not found:
            i += 1  # Skip unknown char
    
    return runes

def word_to_key_indices(word):
    """Convert a word to key indices."""
    return parse_runes(word)

def decrypt_with_key(cipher_indices, key_indices):
    """Decrypt cipher using repeating key."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (c - k) % 29
        plaintext.append(p)
    return plaintext

def indices_to_text(indices):
    """Convert indices back to text."""
    return ''.join(IDX_TO_RUNE[i] for i in indices)

def score_text(text):
    """Score based on English word presence."""
    score = 0
    text_upper = text.upper()
    
    # Check for common words
    for word in ENGLISH_WORDS:
        count = text_upper.count(word)
        score += count * len(word)
    
    # Bonus for digraph diversity (natural language has varied patterns)
    digraph_count = sum(1 for r in ['TH', 'NG', 'EA', 'IO', 'OE', 'EO', 'AE'] if r in text_upper)
    score += digraph_count * 2
    
    return score

def load_page_runes(page_num):
    """Load runes from a page."""
    page_dir = f"../pages/page_{page_num:02d}"
    rune_file = os.path.join(page_dir, "runes.txt")
    
    if os.path.exists(rune_file):
        with open(rune_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def test_keyword_cipher(pages=[8, 13, 43, 46]):
    """Test Cicada keywords as cipher keys."""
    
    print("=" * 70)
    print("KEYWORD CIPHER TESTING")
    print("=" * 70)
    
    for page_num in pages:
        rune_text = load_page_runes(page_num)
        if not rune_text:
            print(f"Could not load page {page_num}")
            continue
        
        cipher_indices = parse_runes(rune_text)
        if len(cipher_indices) < 20:
            continue
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} - Testing Keywords")
        print(f"{'='*70}")
        
        results = []
        
        for keyword in CICADA_KEYWORDS:
            key_indices = word_to_key_indices(keyword)
            if not key_indices:
                continue
            
            plaintext_indices = decrypt_with_key(cipher_indices, key_indices)
            plaintext = indices_to_text(plaintext_indices)
            
            score = score_text(plaintext[:200])
            results.append((keyword, key_indices, score, plaintext[:80]))
        
        # Sort by score
        results.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\nTop 10 keyword results:")
        for keyword, key_idx, score, text in results[:10]:
            key_str = ','.join(str(k) for k in key_idx)
            print(f"  {keyword:15} key=[{key_str:20}] score={score:3}: {text[:50]}")

def test_iw_variation():
    """Test variations around IW key pattern."""
    
    print("\n" + "=" * 70)
    print("IW KEY PATTERN INVESTIGATION")
    print("=" * 70)
    
    # From earlier: keys [10, 7] = I, W found
    # Test variations and extensions
    
    base_patterns = [
        [10, 7],  # IW
        [7, 10],  # WI
        [10, 7, 10, 7],  # IWIW
        [10, 7, 23],  # IWD
        [10, 7, 27],  # IWIO
    ]
    
    # Also test starting at different positions
    for page_num in [8, 13, 43, 46]:
        rune_text = load_page_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = parse_runes(rune_text)
        
        print(f"\nPage {page_num}:")
        
        for key in base_patterns:
            # Try with different starting offsets
            for offset in range(min(5, len(key))):
                shifted_key = key[offset:] + key[:offset]
                plaintext_indices = decrypt_with_key(cipher_indices, shifted_key)
                plaintext = indices_to_text(plaintext_indices)
                score = score_text(plaintext[:200])
                
                key_runes = ''.join(IDX_TO_RUNE[k] for k in shifted_key)
                print(f"  Key {key_runes}: score={score:3}, text={plaintext[:60]}")

def test_autokey_with_keywords():
    """Test autokey cipher with keyword primers."""
    
    print("\n" + "=" * 70)
    print("AUTOKEY WITH KEYWORD PRIMERS")
    print("=" * 70)
    
    primers = ['DIVINITY', 'WISDOM', 'PRIMES', 'THE', 'LIBER', 'PRIMUS', 'I', 'W', 'IW']
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_page_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = parse_runes(rune_text)
        
        print(f"\nPage {page_num}:")
        
        for primer in primers:
            primer_indices = word_to_key_indices(primer)
            if not primer_indices:
                continue
            
            # Autokey: key = primer + previous plaintext
            plaintext = []
            for i, c in enumerate(cipher_indices):
                if i < len(primer_indices):
                    k = primer_indices[i]
                else:
                    k = plaintext[i - len(primer_indices)]
                p = (c - k) % 29
                plaintext.append(p)
            
            plaintext_text = indices_to_text(plaintext)
            score = score_text(plaintext_text[:200])
            
            print(f"  Primer '{primer:12}': score={score:3}, text={plaintext_text[:50]}")

def analyze_discovered_keys():
    """Analyze the keys we've discovered to find patterns."""
    
    print("\n" + "=" * 70)
    print("DISCOVERED KEY PATTERN ANALYSIS")
    print("=" * 70)
    
    # From word_boundary_solver.py:
    discovered_keys = {
        'Page 8': {'PATH': 14, 'THE': 1},
        'Page 13': {'TH': 2, 'IN': 23, 'DO': 9},
        'Page 43': {'BE': 12, 'THY': 25, 'NO': 3},
        'Page 46': {'I': 11, 'UP': 5, 'GO': 15, 'AN': 18, 'BE': 12}
    }
    
    print("\nDiscovered key values:")
    all_keys = []
    for page, words in discovered_keys.items():
        print(f"\n{page}:")
        for word, key in words.items():
            key_rune = IDX_TO_RUNE[key]
            print(f"  {word} -> key={key} ({key_rune})")
            all_keys.append(key)
    
    print(f"\nAll key values: {all_keys}")
    print(f"Unique keys: {sorted(set(all_keys))}")
    
    # Check if keys follow any sequence
    print("\nKey sequence analysis:")
    for page, words in discovered_keys.items():
        keys = list(words.values())
        print(f"{page} keys: {keys}")
        
        # Check differences
        if len(keys) > 1:
            diffs = [keys[i+1] - keys[i] for i in range(len(keys)-1)]
            print(f"  Differences: {diffs}")
        
        # Check if keys map to a word
        key_runes = ''.join(IDX_TO_RUNE[k] for k in keys)
        print(f"  As runes: {key_runes}")

def test_running_key():
    """Test if the key is the plaintext of another page (running key cipher)."""
    
    print("\n" + "=" * 70)
    print("RUNNING KEY CIPHER TEST")
    print("=" * 70)
    print("Testing if solved pages are used as keys for unsolved pages...")
    
    # Try using solved page 0 as key for unsolved pages
    # Page 0 plaintext (approximate): "THE PRIMES ARE SACRED..."
    solved_key = "THEPRIMESARESACRED"
    key_indices = word_to_key_indices(solved_key)
    
    print(f"Key from solved page: {solved_key}")
    print(f"Key indices: {key_indices}")
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_page_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = parse_runes(rune_text)
        plaintext_indices = decrypt_with_key(cipher_indices, key_indices)
        plaintext = indices_to_text(plaintext_indices)
        score = score_text(plaintext[:200])
        
        print(f"\nPage {page_num}: score={score}")
        print(f"  {plaintext[:80]}")

if __name__ == '__main__':
    test_keyword_cipher()
    test_iw_variation()
    test_autokey_with_keywords()
    analyze_discovered_keys()
    test_running_key()

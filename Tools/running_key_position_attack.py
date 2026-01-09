#!/usr/bin/env python3
"""
RUNNING KEY POSITION ATTACK

Key finding from analysis:
- Page 46, word "UP": rune_start=34, key=5
- (key - rune_start) mod 29 = (5 - 34) mod 29 = -29 mod 29 = 0

Hypothesis: key[position] = (rune_position + base_offset) mod 29

OR the key is determined by the running POSITION in the text,
possibly with a page-specific offset.
"""

import os
from pathlib import Path
from collections import Counter

# Gematria Primus mappings
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

COMMON_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN',
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US',
    'WE', 'ALL', 'AND', 'ARE', 'BUT', 'CAN', 'FOR', 'HAS', 'HIM', 'HIS',
    'HOW', 'ITS', 'MAY', 'NEW', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT',
    'OWN', 'SAY', 'SHE', 'THE', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'YOU',
    'FIND', 'FROM', 'HAVE', 'INTO', 'JUST', 'KNOW', 'LIKE', 'MAKE', 'MANY',
    'MORE', 'MUST', 'ONLY', 'OVER', 'PATH', 'SELF', 'SOME', 'SUCH', 'TAKE', 
    'THAN', 'THAT', 'THEM', 'THEN', 'THIS', 'THUS', 'UNTO', 'UPON', 'WHAT', 
    'WHEN', 'WILL', 'WITH', 'YOUR', 'BEING', 'THEIR', 'THERE', 'THESE', 
    'THING', 'THOSE', 'TRUTH', 'WHICH', 'WITHIN', 'THEE', 'THOU', 'THY',
    'YE', 'HATH', 'DOTH', 'SEEK', 'WISDOM', 'LIGHT', 'KNOWLEDGE', 'DIVINE'
}

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(LETTERS[i] for i in indices)

def decrypt_position_key(cipher_indices, base_offset):
    """Decrypt using key = (position + base_offset) mod 29."""
    plaintext = []
    for pos, c in enumerate(cipher_indices):
        key = (pos + base_offset) % 29
        p = (c - key) % 29
        plaintext.append(p)
    return plaintext

def score_text(text):
    """Score based on English words."""
    score = 0
    text_upper = text.upper()
    
    for word in COMMON_WORDS:
        if word in text_upper:
            # Bonus for word appearing as separate word (with boundaries)
            score += len(word) * 10
    
    return score

def test_position_key():
    """Test position-based key hypothesis."""
    
    print("=" * 70)
    print("POSITION-BASED KEY TESTING")
    print("=" * 70)
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        # Parse runes
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num}")
        print(f"{'='*70}")
        
        best_results = []
        
        for base_offset in range(29):
            plaintext_indices = decrypt_position_key(cipher_indices, base_offset)
            plaintext = indices_to_text(plaintext_indices)
            score = score_text(plaintext)
            best_results.append((base_offset, score, plaintext[:80]))
        
        # Sort by score
        best_results.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\nTop 10 base offsets:")
        for offset, score, text in best_results[:10]:
            print(f"  Offset {offset:2d}: score={score:4d}, text={text[:60]}")

def test_multiplied_position_key():
    """Test key = (position * multiplier + offset) mod 29."""
    
    print("\n" + "=" * 70)
    print("MULTIPLIED POSITION KEY TESTING")
    print("=" * 70)
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        print(f"\nPage {page_num}:")
        
        best_overall = []
        
        for mult in range(1, 29):
            for offset in range(29):
                plaintext_indices = []
                for pos, c in enumerate(cipher_indices):
                    key = (pos * mult + offset) % 29
                    p = (c - key) % 29
                    plaintext_indices.append(p)
                
                plaintext = indices_to_text(plaintext_indices)
                score = score_text(plaintext)
                
                if score > 100:
                    best_overall.append((mult, offset, score, plaintext[:60]))
        
        best_overall.sort(key=lambda x: x[2], reverse=True)
        
        for mult, offset, score, text in best_overall[:5]:
            print(f"  mult={mult:2d}, offset={offset:2d}: score={score:4d}, text={text}")

def test_prime_position_key():
    """Test key = prime(position) mod 29."""
    
    print("\n" + "=" * 70)
    print("PRIME POSITION KEY TESTING")
    print("=" * 70)
    
    # Generate many primes
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [p for p in range(2, 1500) if is_prime(p)]
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        print(f"\nPage {page_num}:")
        
        # Test: key = prime[position] mod 29
        plaintext_indices = []
        for pos, c in enumerate(cipher_indices):
            if pos < len(primes):
                key = primes[pos] % 29
            else:
                key = 0
            p = (c - key) % 29
            plaintext_indices.append(p)
        
        plaintext = indices_to_text(plaintext_indices)
        score = score_text(plaintext)
        print(f"  key=prime[pos] mod 29: score={score:4d}, text={plaintext[:60]}")
        
        # Test: key = prime[position+offset] mod 29
        for start_offset in range(20):
            plaintext_indices = []
            for pos, c in enumerate(cipher_indices):
                idx = pos + start_offset
                if idx < len(primes):
                    key = primes[idx] % 29
                else:
                    key = 0
                p = (c - key) % 29
                plaintext_indices.append(p)
            
            plaintext = indices_to_text(plaintext_indices)
            score = score_text(plaintext)
            
            if score > 100:
                print(f"  key=prime[pos+{start_offset}] mod 29: score={score:4d}, text={plaintext[:50]}")

def test_cumulative_position_key():
    """Test key = cumulative sum of positions mod 29."""
    
    print("\n" + "=" * 70)
    print("CUMULATIVE SUM KEY TESTING")
    print("=" * 70)
    
    for page_num in [8, 13, 43, 46]:
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        cipher_indices = []
        for char in rune_text:
            if char in RUNE_MAP:
                cipher_indices.append(RUNE_MAP[char])
        
        print(f"\nPage {page_num}:")
        
        # Triangular numbers: T(n) = n*(n+1)/2
        plaintext_indices = []
        for pos, c in enumerate(cipher_indices):
            key = (pos * (pos + 1) // 2) % 29
            p = (c - key) % 29
            plaintext_indices.append(p)
        
        plaintext = indices_to_text(plaintext_indices)
        score = score_text(plaintext)
        print(f"  key=T(pos) mod 29 (triangular): score={score:4d}, text={plaintext[:60]}")
        
        # Fibonacci-based key
        fib = [1, 1]
        while len(fib) < len(cipher_indices):
            fib.append(fib[-1] + fib[-2])
        
        plaintext_indices = []
        for pos, c in enumerate(cipher_indices):
            key = fib[pos] % 29
            p = (c - key) % 29
            plaintext_indices.append(p)
        
        plaintext = indices_to_text(plaintext_indices)
        score = score_text(plaintext)
        print(f"  key=Fib(pos) mod 29: score={score:4d}, text={plaintext[:60]}")

def analyze_word_specific():
    """Check if word-level key might use word properties."""
    
    print("\n" + "=" * 70)
    print("WORD-SPECIFIC KEY ANALYSIS")
    print("=" * 70)
    print("Checking if key for word relates to word length or word position...")
    
    # Known discoveries with word lengths
    discoveries = [
        {'page': 8, 'word_pos': 3, 'word': 'PATH', 'len': 4, 'key': 14},
        {'page': 8, 'word_pos': 10, 'word': 'THE', 'len': 3, 'key': 1},
        {'page': 13, 'word_pos': 5, 'word': 'A', 'len': 1, 'key': 2},
        {'page': 13, 'word_pos': 7, 'word': 'A', 'len': 1, 'key': 6},
        {'page': 13, 'word_pos': 11, 'word': 'IN', 'len': 2, 'key': 23},
        {'page': 13, 'word_pos': 13, 'word': 'I', 'len': 1, 'key': 8},
        {'page': 13, 'word_pos': 17, 'word': 'DO', 'len': 2, 'key': 9},
        {'page': 43, 'word_pos': 6, 'word': 'BE', 'len': 2, 'key': 12},
        {'page': 43, 'word_pos': 12, 'word': 'THY', 'len': 3, 'key': 25},
        {'page': 43, 'word_pos': 17, 'word': 'NO', 'len': 2, 'key': 3},
        {'page': 46, 'word_pos': 6, 'word': 'I', 'len': 1, 'key': 11},
        {'page': 46, 'word_pos': 10, 'word': 'UP', 'len': 2, 'key': 5},
        {'page': 46, 'word_pos': 17, 'word': 'GO', 'len': 2, 'key': 15},
        {'page': 46, 'word_pos': 19, 'word': 'AN', 'len': 2, 'key': 18},
        {'page': 46, 'word_pos': 20, 'word': 'I', 'len': 1, 'key': 12},
    ]
    
    print("\nKey = word_length + page + word_pos + offset?")
    for d in discoveries:
        val = (d['len'] + d['page'] + d['word_pos']) % 29
        diff = (d['key'] - val) % 29
        print(f"  {d['word']:4} page={d['page']:2} pos={d['word_pos']:2} len={d['len']}: "
              f"key={d['key']:2}, (len+page+pos) mod 29={val:2}, diff={diff}")
    
    print("\nKey = 2*word_pos mod 29?")
    for d in discoveries:
        val = (2 * d['word_pos']) % 29
        match = "✓" if val == d['key'] else ""
        print(f"  {d['word']:4}: key={d['key']:2}, 2*pos mod 29={val:2} {match}")

if __name__ == '__main__':
    test_position_key()
    test_multiplied_position_key()
    test_prime_position_key()
    test_cumulative_position_key()
    analyze_word_specific()

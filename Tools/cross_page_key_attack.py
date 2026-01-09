#!/usr/bin/env python3
"""
CROSS-PAGE KEY ATTACK

Hypothesis: Ciphertext from one page is used as the key for another page.
For example:
- Page 00 ciphertext → Key for Page 18
- Page 01 ciphertext → Key for Page 19
etc.

This would explain why we can't crack pages 18+ without first transcribing all pages.
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(SCRIPT_DIR, "..", "pages")

# Rune to index mapping
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4,
    'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19,
    'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R',
    5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X',
    15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M',
    20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A',
    25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

def load_rune_indices(page_num: int) -> list[int]:
    """Load runes and convert to indices."""
    runes_file = os.path.join(PAGES_DIR, f"page_{page_num:02d}", "runes.txt")
    if not os.path.exists(runes_file):
        return []
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    indices = []
    for char in content:
        if char in RUNE_TO_INDEX:
            indices.append(RUNE_TO_INDEX[char])
    return indices

def indices_to_text(indices: list[int]) -> str:
    return "".join(INDEX_TO_LATIN.get(i, "?") for i in indices)

def decrypt_sub(cipher: list[int], key: list[int]) -> list[int]:
    """SUB mode: P = (C - K) mod 29"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)] if key else 0
        p = (c - k) % 29
        result.append(p)
    return result

def decrypt_add(cipher: list[int], key: list[int]) -> list[int]:
    """ADD mode: P = (C + K) mod 29"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)] if key else 0
        p = (c + k) % 29
        result.append(p)
    return result

def score_text(text: str) -> float:
    """Score based on English patterns."""
    score = 0.0
    words = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'THAT', 'WAS',
             'FOR', 'ON', 'WITH', 'AS', 'AT', 'BY', 'NOT', 'ARE', 'ALL', 'FROM',
             'HAVE', 'HAS', 'BUT', 'OR', 'AN', 'THEY', 'WHICH', 'YOU', 'WERE',
             'TRUTH', 'WISDOM', 'DIVINE', 'SACRED', 'SOUL', 'SELF', 'TRUST',
             'SEEK', 'FIND', 'PATH', 'LIGHT', 'DARK', 'PILGRIM', 'PRIMES',
             'WELCOME', 'BELIEVE', 'NOTHING', 'EVERYTHING', 'WITHIN', 'POWER']
    
    for word in words:
        if word in text:
            score += len(word) * 10
    
    return score

def main():
    print("=" * 80)
    print("CROSS-PAGE KEY ATTACK")
    print("=" * 80)
    
    # Load all page ciphertexts
    all_ciphers = {}
    for page in range(0, 75):
        indices = load_rune_indices(page)
        if indices:
            all_ciphers[page] = indices
    
    print(f"Loaded {len(all_ciphers)} pages with rune data")
    
    # Test: Use page X as key for page Y
    # Strategy 1: Use page N as key for page N+18 (LP1 -> LP2)
    print(f"\n{'='*60}")
    print("STRATEGY 1: Page N → Key for Page N+18")
    print("=" * 60)
    
    for key_page in range(0, 18):
        target_page = key_page + 18
        if key_page in all_ciphers and target_page in all_ciphers:
            key = all_ciphers[key_page]
            cipher = all_ciphers[target_page]
            
            for mode, decrypt_fn in [('SUB', decrypt_sub), ('ADD', decrypt_add)]:
                plain = decrypt_fn(cipher, key)
                text = indices_to_text(plain)
                score = score_text(text)
                
                if score > 100:
                    print(f"\n  [{score:.1f}] Page {key_page} → Page {target_page} ({mode})")
                    print(f"    {text[:100]}...")
    
    # Strategy 2: Use page N as key for page N+1
    print(f"\n{'='*60}")
    print("STRATEGY 2: Page N → Key for Page N+1")
    print("=" * 60)
    
    for key_page in range(17, 54):
        target_page = key_page + 1
        if key_page in all_ciphers and target_page in all_ciphers:
            key = all_ciphers[key_page]
            cipher = all_ciphers[target_page]
            
            for mode, decrypt_fn in [('SUB', decrypt_sub), ('ADD', decrypt_add)]:
                plain = decrypt_fn(cipher, key)
                text = indices_to_text(plain)
                score = score_text(text)
                
                if score > 100:
                    print(f"\n  [{score:.1f}] Page {key_page} → Page {target_page} ({mode})")
                    print(f"    {text[:100]}...")
    
    # Strategy 3: Use solved pages (55-74) as keys for unsolved (18-37)
    print(f"\n{'='*60}")
    print("STRATEGY 3: Solved Page (55+N) → Key for Unsolved (18+N)")
    print("=" * 60)
    
    for offset in range(0, 20):
        key_page = 55 + offset
        target_page = 18 + offset
        if key_page in all_ciphers and target_page in all_ciphers:
            key = all_ciphers[key_page]
            cipher = all_ciphers[target_page]
            
            for mode, decrypt_fn in [('SUB', decrypt_sub), ('ADD', decrypt_add)]:
                plain = decrypt_fn(cipher, key)
                text = indices_to_text(plain)
                score = score_text(text)
                
                if score > 100:
                    print(f"\n  [{score:.1f}] Page {key_page} → Page {target_page} ({mode})")
                    print(f"    {text[:100]}...")
    
    # Strategy 4: Reverse - Use page 17 (EPILOGUE) as key for page 18
    print(f"\n{'='*60}")
    print("STRATEGY 4: EPILOGUE page (17) variations")
    print("=" * 60)
    
    if 17 in all_ciphers and 18 in all_ciphers:
        key = all_ciphers[17]
        cipher = all_ciphers[18]
        
        # Try different key offsets
        for offset in range(0, min(50, len(key))):
            shifted_key = key[offset:] + key[:offset]
            
            for mode, decrypt_fn in [('SUB', decrypt_sub), ('ADD', decrypt_add)]:
                plain = decrypt_fn(cipher, shifted_key)
                text = indices_to_text(plain)
                score = score_text(text)
                
                if score > 120:
                    print(f"\n  [{score:.1f}] Page 17 (offset {offset}) → Page 18 ({mode})")
                    print(f"    {text[:100]}...")

if __name__ == "__main__":
    main()

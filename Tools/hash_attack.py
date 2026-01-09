#!/usr/bin/env python3
"""
SHA-512 Hash-Based Cipher Attack
Using the hash from Page 56 as a key for decryption

The hash: 36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4
"""

import os
from collections import Counter

# The SHA-512 hash from page 56
HASH = "36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4"

# Gematria Primus mapping
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LETTER = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E',
    19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

COMMON_WORDS = {'THE', 'AND', 'IS', 'OF', 'TO', 'IN', 'IT', 'FOR', 'AS', 'WITH', 'WAS', 
                'HIS', 'BE', 'AT', 'BY', 'THIS', 'HAD', 'NOT', 'ARE', 'BUT', 'FROM',
                'DIVINITY', 'WITHIN', 'PRIMES', 'SACRED', 'PILGRIM', 'WISDOM', 'TRUTH'}

def load_runes(page_num):
    """Load runes from a page's runes.txt file"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_file = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if not os.path.exists(rune_file):
        return None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    runes = [c for c in content if c in RUNE_TO_INDEX]
    return runes

def hash_to_key_bytes(h):
    """Convert hex hash to bytes (0-255)"""
    return [int(h[i:i+2], 16) for i in range(0, len(h), 2)]

def hash_to_key_nibbles(h):
    """Convert hex hash to nibbles (0-15)"""
    return [int(c, 16) for c in h]

def hash_to_key_chars(h):
    """Map hash characters to indices: 0-9 -> 0-9, a-f -> 10-15"""
    result = []
    for c in h:
        if c.isdigit():
            result.append(int(c))
        else:
            result.append(ord(c.lower()) - ord('a') + 10)
    return result

def decrypt(cipher_runes, key, mode='SUB', key_mod=29):
    """Decrypt using the key"""
    plaintext = []
    
    for i, rune in enumerate(cipher_runes):
        key_val = key[i % len(key)]
        if key_mod:
            key_val = key_val % key_mod
        cipher_val = RUNE_TO_INDEX[rune]
        
        if mode == 'SUB':
            plain_val = (cipher_val - key_val) % 29
        elif mode == 'ADD':
            plain_val = (cipher_val + key_val) % 29
        else:  # XOR
            plain_val = cipher_val ^ key_val
            plain_val = plain_val % 29
        
        plaintext.append(INDEX_TO_LETTER[plain_val])
    
    return ''.join(plaintext)

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def calculate_ioc(text):
    counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    return sum(count * (count - 1) for count in counts.values()) / (n * (n - 1))

def main():
    print("=" * 70)
    print("SHA-512 HASH-BASED CIPHER ATTACK")
    print("=" * 70)
    print(f"Hash: {HASH}")
    print(f"Hash length: {len(HASH)} hex chars = {len(HASH)//2} bytes = 512 bits")
    
    # Convert hash to different key formats
    key_bytes = hash_to_key_bytes(HASH)  # 64 bytes (0-255)
    key_nibbles = hash_to_key_nibbles(HASH)  # 128 nibbles (0-15)
    key_chars = hash_to_key_chars(HASH)  # 128 values (0-15)
    
    print(f"\nKey formats:")
    print(f"  Bytes (64 values, 0-255): {key_bytes[:10]}...")
    print(f"  Nibbles (128 values, 0-15): {key_nibbles[:20]}...")
    
    # Load page 18 for testing
    runes = load_runes(18)
    if not runes:
        print("Could not load page 18")
        return
    
    print(f"\nPage 18: {len(runes)} runes")
    
    print("\n" + "=" * 70)
    print("STRATEGY 1: Hash bytes as key (mod 29)")
    print("=" * 70)
    
    for mode in ['SUB', 'ADD']:
        plaintext = decrypt(runes, key_bytes, mode, key_mod=29)
        score = score_text(plaintext)
        ioc = calculate_ioc(plaintext)
        print(f"  {mode}: Score={score}, IoC={ioc:.4f}")
        print(f"    Preview: {plaintext[:80]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 2: Hash nibbles as key (mod 29)")
    print("=" * 70)
    
    for mode in ['SUB', 'ADD']:
        plaintext = decrypt(runes, key_nibbles, mode, key_mod=29)
        score = score_text(plaintext)
        ioc = calculate_ioc(plaintext)
        print(f"  {mode}: Score={score}, IoC={ioc:.4f}")
        print(f"    Preview: {plaintext[:80]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 3: Hash bytes as XOR key")
    print("=" * 70)
    
    plaintext = decrypt(runes, key_bytes, 'XOR', key_mod=None)
    score = score_text(plaintext)
    ioc = calculate_ioc(plaintext)
    print(f"  XOR: Score={score}, IoC={ioc:.4f}")
    print(f"    Preview: {plaintext[:80]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 4: Cumulative sum of hash bytes (mod 29)")
    print("=" * 70)
    
    cumsum_key = []
    s = 0
    for b in key_bytes:
        s = (s + b) % 29
        cumsum_key.append(s)
    
    for mode in ['SUB', 'ADD']:
        plaintext = decrypt(runes, cumsum_key, mode, key_mod=None)
        score = score_text(plaintext)
        ioc = calculate_ioc(plaintext)
        print(f"  {mode}: Score={score}, IoC={ioc:.4f}")
        print(f"    Preview: {plaintext[:80]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 5: Hash as running key with various interpretations")
    print("=" * 70)
    
    # Interpret hex chars as letters (a=0, b=1, ..., f=5, digits ignored)
    letter_key = []
    for c in HASH:
        if c.isalpha():
            letter_key.append(ord(c.lower()) - ord('a'))
        elif c.isdigit():
            letter_key.append(int(c))
    
    for mode in ['SUB', 'ADD']:
        plaintext = decrypt(runes, letter_key, mode, key_mod=29)
        score = score_text(plaintext)
        ioc = calculate_ioc(plaintext)
        print(f"  {mode}: Score={score}, IoC={ioc:.4f}")
        print(f"    Preview: {plaintext[:80]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 6: Hash concatenated with itself (for longer pages)")
    print("=" * 70)
    
    extended_key = (key_bytes * 10)[:1000]
    
    for page_num in [18, 19, 20, 25, 50]:
        runes = load_runes(page_num)
        if not runes:
            continue
        
        for mode in ['SUB', 'ADD']:
            plaintext = decrypt(runes, extended_key, mode, key_mod=29)
            score = score_text(plaintext)
            ioc = calculate_ioc(plaintext)
            if score > 0 or ioc > 0.05:
                print(f"  Page {page_num} {mode}: Score={score}, IoC={ioc:.4f}")
                print(f"    Preview: {plaintext[:60]}")
    
    print("\n" + "=" * 70)
    print("STRATEGY 7: Repeated 2-byte or 4-byte patterns from hash")
    print("=" * 70)
    
    runes = load_runes(18)
    
    # Try each 2-byte segment as a repeating key
    best_2byte = None
    for i in range(0, len(key_bytes) - 1):
        short_key = [key_bytes[i], key_bytes[i+1]]
        for mode in ['SUB', 'ADD']:
            plaintext = decrypt(runes, short_key, mode, key_mod=29)
            score = score_text(plaintext)
            if best_2byte is None or score > best_2byte[2]:
                best_2byte = (i, mode, score, plaintext[:60])
    
    if best_2byte:
        print(f"  Best 2-byte key at position {best_2byte[0]}: {mode}={best_2byte[2]}")
        print(f"    Key bytes: {key_bytes[best_2byte[0]:best_2byte[0]+2]}")
        print(f"    Preview: {best_2byte[3]}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("The SHA-512 hash provides various key derivation possibilities.")
    print("If no clear solution emerges, the hash might point to:")
    print("  1. An external resource (onion page)")
    print("  2. A verification mechanism (not the key itself)")
    print("  3. A more complex key derivation function")

if __name__ == '__main__':
    main()

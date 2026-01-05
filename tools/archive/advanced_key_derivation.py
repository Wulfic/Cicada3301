#!/usr/bin/env python3
"""
Findings so far:
1. Offset -200 (≡ 3 mod 29) gives best results for most pages
2. IoC reaches ~1.4-1.57, not quite English (~1.73)
3. The gematria+ transformation also gives high IoC (~1.79)

Let's try combining these approaches and also:
1. Per-word keys based on word position
2. Interleaved/alternating ciphers
3. Look for patterns in word lengths
"""

import numpy as np
from collections import Counter
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
           'A', 'AE', 'Y', 'IA', 'EA']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
            59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def text_to_indices(text):
    return np.array([RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX], dtype=np.int32)

def indices_to_english(indices):
    return ''.join(LETTERS[int(i) % 29] for i in indices)

def compute_ioc_normalized(indices):
    n = len(indices)
    if n <= 1:
        return 0.0
    counts = np.bincount(indices, minlength=29)
    sum_ni = np.sum(counts * (counts - 1))
    return (sum_ni / (n * (n - 1))) * 29

def try_per_word_key(page_text):
    """Try different keys for each word."""
    
    # Parse into words (separated by • - / etc)
    words = []
    current_word = []
    
    for char in page_text:
        if char in RUNE_TO_IDX:
            current_word.append(RUNE_TO_IDX[char])
        else:
            if current_word:
                words.append(np.array(current_word, dtype=np.int32))
                current_word = []
    if current_word:
        words.append(np.array(current_word, dtype=np.int32))
    
    return words

def try_word_position_key(words):
    """Key is based on word position."""
    print("\n" + "="*60)
    print("WORD POSITION BASED KEY")
    print("="*60)
    
    all_decrypted = []
    
    for offset in range(29):
        decrypted = []
        for word_idx, word in enumerate(words):
            key = (word_idx + offset) % 29
            dec_word = (word - key) % 29
            decrypted.extend(dec_word.tolist())
        
        indices = np.array(decrypted)
        ioc = compute_ioc_normalized(indices)
        
        if ioc > 1.3:
            text = indices_to_english(indices[:50])
            print(f"Offset {offset}: IoC={ioc:.4f} -> {text}")

def try_word_length_key(words):
    """Key is based on word length."""
    print("\n" + "="*60)
    print("WORD LENGTH BASED KEY")
    print("="*60)
    
    for offset in range(29):
        decrypted = []
        for word in words:
            key = (len(word) + offset) % 29
            dec_word = (word - key) % 29
            decrypted.extend(dec_word.tolist())
        
        indices = np.array(decrypted)
        ioc = compute_ioc_normalized(indices)
        
        if ioc > 1.3:
            text = indices_to_english(indices[:50])
            print(f"Offset {offset}: IoC={ioc:.4f} -> {text}")

def try_gematria_word_sum_key(words):
    """Key for each word is based on sum of gematria of previous word."""
    print("\n" + "="*60)
    print("GEMATRIA SUM CHAINING")
    print("="*60)
    
    # Key for word n = sum of gematria of word n-1
    for initial in range(29):
        decrypted = []
        prev_sum = initial
        
        for word in words:
            key = prev_sum % 29
            dec_word = (word - key) % 29
            decrypted.extend(dec_word.tolist())
            
            # Calculate sum for next word
            prev_sum = sum(GEMATRIA[idx] for idx in word)
        
        indices = np.array(decrypted)
        ioc = compute_ioc_normalized(indices)
        
        if ioc > 1.3:
            text = indices_to_english(indices[:50])
            print(f"Initial {initial}: IoC={ioc:.4f} -> {text}")

def try_prime_shift_per_position(page_indices):
    """Each position uses -(gematria + position) mod 29."""
    print("\n" + "="*60)
    print("POSITION-INDEXED GEMATRIA SHIFT")
    print("="*60)
    
    n = len(page_indices)
    
    # Try: plaintext[i] = -(gematria(cipher[i]) + i*k + offset) mod 29
    for k in range(1, 30):
        for offset in range(29):
            decrypted = np.zeros(n, dtype=np.int32)
            for i in range(n):
                gem = GEMATRIA[page_indices[i]]
                decrypted[i] = (-(gem + i * k + offset)) % 29
            
            ioc = compute_ioc_normalized(decrypted)
            if ioc > 1.5:
                text = indices_to_english(decrypted[:50])
                print(f"k={k}, offset={offset}: IoC={ioc:.4f} -> {text}")

def try_rune_position_key(page_indices):
    """Key based on rune's position in alphabet: k[i] = cipher[i] mod 29"""
    print("\n" + "="*60)
    print("SELF-KEYED (RUNE VALUE AS KEY)")
    print("="*60)
    
    n = len(page_indices)
    
    # Vigenère with key = ciphertext itself
    # P = C - K = C - C[i] = 0 (trivial)
    # But what about: P = C - C[i-1]?
    
    # Autokey decrypt
    for primer in range(29):
        decrypted = np.zeros(n, dtype=np.int32)
        decrypted[0] = (page_indices[0] - primer) % 29
        
        for i in range(1, n):
            decrypted[i] = (page_indices[i] - decrypted[i-1]) % 29
        
        ioc = compute_ioc_normalized(decrypted)
        if ioc > 1.3:
            text = indices_to_english(decrypted[:50])
            print(f"Autokey primer {primer}: IoC={ioc:.4f} -> {text}")
    
    # Running key with gematria values
    print("\n  Running key with gematria progression:")
    for offset in range(29):
        decrypted = np.zeros(n, dtype=np.int32)
        gem_sum = offset
        
        for i in range(n):
            decrypted[i] = (page_indices[i] - gem_sum) % 29
            gem_sum = (gem_sum + GEMATRIA[page_indices[i]]) % 29
        
        ioc = compute_ioc_normalized(decrypted)
        if ioc > 1.3:
            text = indices_to_english(decrypted[:50])
            print(f"Gem running key offset {offset}: IoC={ioc:.4f} -> {text}")

def analyze_two_layer_cipher(page_indices):
    """
    What if it's: prime_shift(vigenere(plaintext))?
    We'd need to reverse both layers.
    """
    print("\n" + "="*60)
    print("TWO-LAYER CIPHER: PRIME + VIGENERE")
    print("="*60)
    
    n = len(page_indices)
    
    # First, try to reverse gematria shift
    # Then try short Vigenere keys
    
    for gem_offset in range(-100, 101, 10):
        # Reverse gematria layer
        intermediate = np.zeros(n, dtype=np.int32)
        for i in range(n):
            gem = GEMATRIA[page_indices[i]]
            intermediate[i] = (-(gem + gem_offset)) % 29
        
        # Now try Vigenere with short keys
        for key_len in range(2, 6):
            # Find best key for this key length
            best_key = [0] * key_len
            
            for pos in range(key_len):
                best_shift = 0
                best_ioc = 0
                
                for shift in range(29):
                    subset = intermediate[pos::key_len]
                    shifted = (subset - shift) % 29
                    ioc = compute_ioc_normalized(shifted)
                    if ioc > best_ioc:
                        best_ioc = ioc
                        best_shift = shift
                
                best_key[pos] = best_shift
            
            # Apply best key
            decrypted = np.zeros(n, dtype=np.int32)
            for i in range(n):
                decrypted[i] = (intermediate[i] - best_key[i % key_len]) % 29
            
            ioc = compute_ioc_normalized(decrypted)
            
            if ioc > 1.6:
                text = indices_to_english(decrypted[:50])
                print(f"Gem offset {gem_offset}, Vig key {best_key}: IoC={ioc:.4f}")
                print(f"  -> {text}")

def main():
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(lp_path, 'r', encoding='utf-8') as f:
        lp_text = f.read()
    
    # Work with first page as test case
    pages = lp_text.split('&')
    
    print("="*70)
    print("ADVANCED KEY DERIVATION TESTING - PAGE 0")
    print("="*70)
    
    page_text = pages[0]
    page_indices = text_to_indices(page_text)
    words = try_per_word_key(page_text)
    
    print(f"\nPage 0: {len(page_indices)} runes, {len(words)} words")
    print(f"Original IoC: {compute_ioc_normalized(page_indices):.4f}")
    
    try_word_position_key(words)
    try_word_length_key(words)
    try_gematria_word_sum_key(words)
    try_prime_shift_per_position(page_indices)
    try_rune_position_key(page_indices)
    analyze_two_layer_cipher(page_indices)

if __name__ == "__main__":
    main()

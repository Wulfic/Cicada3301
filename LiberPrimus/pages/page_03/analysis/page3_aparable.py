#!/usr/bin/env python3
"""
ADVANCED PAGE 3 ANALYSIS: Known-Plaintext Attack with "A PARABLE"

Key insight: The known-plaintext "A PARABLE" gives us 8 key values.
We need to find the correct key length and extend/refine the key.
"""

from pathlib import Path
from collections import Counter
import itertools

# Constants
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]

def indices_to_text(indices):
    return "".join(LETTERS[i] for i in indices)

def text_to_indices(text):
    result = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph in LETTERS:
                result.append(LETTERS.index(digraph))
                i += 2
                continue
        if text[i] in LETTERS:
            result.append(LETTERS.index(text[i]))
        i += 1
    return result

def decrypt_sub(cipher, key):
    return [(cipher[i] - key[i % len(key)]) % 29 for i in range(len(cipher))]

def encrypt_sub(plain, key):
    return [(plain[i] + key[i % len(key)]) % 29 for i in range(len(plain))]

def score_english(text):
    text = text.upper()
    score = 0.0
    
    # Strong trigrams
    trigrams = {
        'THE': 50, 'AND': 35, 'ING': 30, 'ION': 25, 'TIO': 25,
        'FOR': 20, 'ERE': 20, 'HER': 20, 'ATE': 20, 'ENT': 20,
        'VER': 15, 'TER': 15, 'THA': 15, 'ITH': 15, 'WIT': 15,
        'HAT': 15, 'OUR': 15, 'YOU': 15, 'HIS': 15, 'ALL': 15,
        'OUT': 15, 'NOT': 15, 'ARE': 15, 'BUT': 15, 'ONE': 15,
    }
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    # Bigrams
    bigrams = {
        'TH': 25, 'HE': 22, 'IN': 18, 'ER': 17, 'AN': 16,
        'RE': 15, 'ON': 14, 'AT': 14, 'EN': 13, 'ND': 13,
        'TI': 12, 'ES': 12, 'OR': 12, 'TE': 12, 'OF': 12,
        'ED': 11, 'IS': 11, 'IT': 11, 'AL': 11, 'AR': 11,
        'ST': 11, 'TO': 11, 'OU': 10, 'SE': 10, 'HA': 10,
    }
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    # Keywords
    keywords = {
        'PARABLE': 200, 'WISDOM': 150, 'TRUTH': 150, 'DIVINE': 150, 
        'INSTAR': 180, 'EMERGE': 150, 'CIRCUMFERENCE': 200,
        'PRIMES': 150, 'SACRED': 150, 'WITHIN': 120, 'PILGRIM': 150,
        'INSTRUCTION': 150, 'KOAN': 150, 'MASTER': 120,
    }
    for kw, bonus in keywords.items():
        score += text.count(kw) * bonus
    
    return score

def load_page3():
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pages = content.split('%')
    page3_raw = pages[2]
    return [RUNE_TO_INDEX[c] for c in page3_raw if c in RUNE_TO_INDEX]

def hill_climb(cipher, initial_key, max_iter=1000):
    """Hill-climbing optimization"""
    key = initial_key[:]
    best_score = score_english(indices_to_text(decrypt_sub(cipher, key)))
    
    for _ in range(max_iter):
        improved = False
        for i in range(len(key)):
            for delta in [-1, 1]:
                test_key = key[:]
                test_key[i] = (key[i] + delta) % 29
                test_text = indices_to_text(decrypt_sub(cipher, test_key))
                test_score = score_english(test_text)
                if test_score > best_score:
                    key = test_key
                    best_score = test_score
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
    
    return key, best_score

def main():
    cipher = load_page3()
    print(f"Page 3: {len(cipher)} runes")
    
    # Known plaintext from "A PARABLE"
    known = "APARABLE"
    known_idx = text_to_indices(known)
    
    # Derive key fragment
    key_frag = [(cipher[i] - known_idx[i]) % 29 for i in range(len(known_idx))]
    print(f"\nKnown plaintext: {known}")
    print(f"Known indices: {known_idx}")
    print(f"Derived key fragment: {key_frag}")
    
    print("\n" + "=" * 80)
    print("APPROACH 1: Extend Key Fragment to Prime Lengths + Hill Climb")
    print("=" * 80)
    
    results = []
    for key_len in [p for p in PRIMES if 60 <= p <= 120]:
        # Create initial key by:
        # 1. Using known values at positions 0-7
        # 2. Using frequency analysis for other positions
        
        initial_key = [0] * key_len
        
        # Fill in known values
        for i in range(len(key_frag)):
            initial_key[i] = key_frag[i]
        
        # Frequency-based initialization for remaining positions
        for pos in range(len(key_frag), key_len):
            coset = [cipher[j] for j in range(pos, len(cipher), key_len)]
            if coset:
                most_common = Counter(coset).most_common(1)[0][0]
                # Assume most common decrypts to E (index 18)
                initial_key[pos] = (most_common - 18) % 29
        
        # Hill climb
        optimized_key, best_score = hill_climb(cipher, initial_key, max_iter=500)
        plaintext = decrypt_sub(cipher, optimized_key)
        text = indices_to_text(plaintext)
        
        # Verify first 8 characters
        first8 = text[:len(known)]
        match = first8 == known
        
        results.append((key_len, best_score, text, match))
        
        if best_score > 600:
            marker = "✓" if match else ""
            print(f"\nKey length {key_len}: Score {best_score:.0f} {marker}")
            print(f"  First 8: {first8} {'== ' + known if match else '!= ' + known}")
            print(f"  Text: {text[:80]}...")
    
    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)
    print("\n" + "=" * 80)
    print("TOP 5 RESULTS")
    print("=" * 80)
    for kl, sc, txt, match in results[:5]:
        marker = "✓ MATCHES" if match else ""
        print(f"\nKey length {kl}: Score {sc:.0f} {marker}")
        print(f"  Text: {txt}")
    
    print("\n" + "=" * 80)
    print("APPROACH 2: What if Key Length is NOT Prime?")
    print("=" * 80)
    
    # The IoC showed 146 as best non-prime, let's also try nearby values
    for key_len in [145, 146, 147, 148]:
        initial_key = [0] * key_len
        for i in range(len(key_frag)):
            initial_key[i] = key_frag[i]
        for pos in range(len(key_frag), key_len):
            coset = [cipher[j] for j in range(pos, len(cipher), key_len)]
            if coset:
                most_common = Counter(coset).most_common(1)[0][0]
                initial_key[pos] = (most_common - 18) % 29
        
        optimized_key, best_score = hill_climb(cipher, initial_key, max_iter=500)
        text = indices_to_text(decrypt_sub(cipher, optimized_key))
        
        print(f"\nKey length {key_len}: Score {best_score:.0f}")
        print(f"  First 8: {text[:len(known)]}")
        print(f"  Text: {text[:80]}...")
    
    print("\n" + "=" * 80)
    print("APPROACH 3: Running Key (Autokey) with APARABLE Start")
    print("=" * 80)
    
    # Autokey cipher: key = seed + plaintext
    # For decryption: key[i] = seed[i] for i < len(seed), else key[i] = plaintext[i - len(seed)]
    
    seeds = ["APARABLE", "PARABLE", "WISDOM", "TRUTH", "PRIMES"]
    
    for seed_text in seeds:
        seed = text_to_indices(seed_text)
        if len(seed) < 3:
            continue
        
        plaintext = []
        for i, c in enumerate(cipher):
            if i < len(seed):
                k = seed[i]
            else:
                k = plaintext[i - len(seed)]
            p = (c - k) % 29
            plaintext.append(p)
        
        text = indices_to_text(plaintext)
        sc = score_english(text)
        
        if sc > 200:
            print(f"\nSeed '{seed_text}': Score {sc:.0f}")
            print(f"  Text: {text[:100]}...")
    
    print("\n" + "=" * 80)
    print("APPROACH 4: Deep Refinement of Key-79 (Highest Score with APARABLE Match)")
    print("=" * 80)
    
    # From earlier: key length 79 gave score 720 with APARABLE matching
    key_len = 79
    initial_key = [0] * key_len
    for i in range(len(key_frag)):
        initial_key[i] = key_frag[i]
    for pos in range(len(key_frag), key_len):
        coset = [cipher[j] for j in range(pos, len(cipher), key_len)]
        if coset:
            most_common = Counter(coset).most_common(1)[0][0]
            initial_key[pos] = (most_common - 18) % 29
    
    # Extended hill climb with multiple restarts
    best_overall_key = None
    best_overall_score = 0
    
    for target_letter_idx in [18, 16, 24, 9, 10]:  # E, T, A, N, I
        test_key = initial_key[:]
        for pos in range(len(key_frag), key_len):
            coset = [cipher[j] for j in range(pos, len(cipher), key_len)]
            if coset:
                most_common = Counter(coset).most_common(1)[0][0]
                test_key[pos] = (most_common - target_letter_idx) % 29
        
        opt_key, opt_score = hill_climb(cipher, test_key, max_iter=1000)
        if opt_score > best_overall_score:
            best_overall_score = opt_score
            best_overall_key = opt_key
            print(f"  Target letter {LETTERS[target_letter_idx]}: Score {opt_score:.0f}")
    
    if best_overall_key:
        final_text = indices_to_text(decrypt_sub(cipher, best_overall_key))
        print(f"\nBest result for key-79:")
        print(f"  Score: {best_overall_score:.0f}")
        print(f"  Key: {best_overall_key}")
        print(f"  Text: {final_text}")
        
        # Verify reversibility
        re_encrypted = encrypt_sub(decrypt_sub(cipher, best_overall_key), best_overall_key)
        matches = sum(1 for a, b in zip(cipher, re_encrypted) if a == b)
        print(f"  Reversibility: {matches}/{len(cipher)}")

if __name__ == "__main__":
    main()

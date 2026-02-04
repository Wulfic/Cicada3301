#!/usr/bin/env python3
"""
Attack Page 20: Use the decoded prime-position stream as a key for non-prime positions

The 166-char decoded stream from prime positions contains meaningful text like
"THE LONE", "EODE", "SEFA". This script tests using that stream as a running key
for the remaining 646 non-prime runes.

Based on the P19 hint: "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"
"""

import os
from collections import Counter

# Gematria Primus mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X',
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

CHAR_TO_IDX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
    'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

# Single letter fallback
SINGLE_CHAR_TO_IDX = {c: i for i, c in enumerate('FUTHORCGWHNIJEOPXSTBEMLODA') if i < 26}
SINGLE_CHAR_TO_IDX['Y'] = 26
# Handle digraphs properly
SINGLE_CHAR_TO_IDX['K'] = 5  # K = C in Gematria

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def load_runes(filepath):
    """Load runes from file, return list of indices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove formatting but track positions
    indices = []
    for c in content:
        if c in RUNE_MAP:
            indices.append(RUNE_MAP[c])
    return indices

def string_to_indices(s):
    """Convert a string to Gematria indices, handling digraphs."""
    indices = []
    i = 0
    while i < len(s):
        # Check for digraphs first
        if i + 1 < len(s):
            digraph = s[i:i+2].upper()
            if digraph in CHAR_TO_IDX:
                indices.append(CHAR_TO_IDX[digraph])
                i += 2
                continue
        # Single character
        c = s[i].upper()
        if c in SINGLE_CHAR_TO_IDX:
            indices.append(SINGLE_CHAR_TO_IDX[c])
        elif c in CHAR_TO_IDX:
            indices.append(CHAR_TO_IDX[c])
        i += 1
    return indices

def calc_ioc(indices):
    """Calculate Index of Coincidence for 29-letter alphabet."""
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    """Convert indices to Latin letters."""
    return ''.join(LATIN_TABLE[i] for i in indices)

def vigenere_decrypt(cipher, key, mode='sub'):
    """Decrypt with Vigenère cipher. mode: 'sub', 'add', or 'beaufort'."""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        elif mode == 'add':
            result.append((c + k) % 29)
        elif mode == 'beaufort':
            result.append((k - c) % 29)
    return result

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    # Load P20 runes
    cipher = load_runes(p20_path)
    print(f"Loaded {len(cipher)} runes from Page 20")
    
    # The decoded stream from prime positions (Beaufort with Deor, 2x83 transposed)
    decoded_stream = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"
    
    # Also try the pre-transposition stream
    pre_transposition_stream = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"
    
    # Convert streams to indices
    decoded_key = string_to_indices(decoded_stream)
    pre_trans_key = string_to_indices(pre_transposition_stream)
    
    print(f"Decoded stream as key: {len(decoded_key)} indices")
    print(f"Pre-transposition stream as key: {len(pre_trans_key)} indices")
    
    # Separate prime and non-prime positions
    prime_positions = [i for i in range(len(cipher)) if is_prime(i)]
    non_prime_positions = [i for i in range(len(cipher)) if not is_prime(i)]
    
    non_prime_runes = [cipher[i] for i in non_prime_positions]
    print(f"\nNon-prime positions: {len(non_prime_positions)} runes")
    
    # Test various approaches
    results = []
    
    # Approach 1: Use decoded stream as cycling key (various modes)
    for mode in ['sub', 'add', 'beaufort']:
        for key_name, key in [('decoded', decoded_key), ('pre_trans', pre_trans_key)]:
            decrypted = vigenere_decrypt(non_prime_runes, key, mode)
            ioc = calc_ioc(decrypted)
            latin = indices_to_latin(decrypted)
            results.append({
                'method': f'{key_name}_stream_{mode}',
                'ioc': ioc,
                'preview': latin[:100]
            })
    
    # Approach 2: Try THE LONE as a key
    the_lone_key = [2, 18, 20, 3, 9, 18]  # TH-E-L-O-N-E
    for mode in ['sub', 'add', 'beaufort']:
        decrypted = vigenere_decrypt(non_prime_runes, the_lone_key, mode)
        ioc = calc_ioc(decrypted)
        latin = indices_to_latin(decrypted)
        results.append({
            'method': f'THE_LONE_{mode}',
            'ioc': ioc,
            'preview': latin[:100]
        })
    
    # Approach 3: Try SEFA as a key
    sefa_key = [15, 18, 0, 24]  # S-E-F-A
    for mode in ['sub', 'add', 'beaufort']:
        decrypted = vigenere_decrypt(non_prime_runes, sefa_key, mode)
        ioc = calc_ioc(decrypted)
        latin = indices_to_latin(decrypted)
        results.append({
            'method': f'SEFA_{mode}',
            'ioc': ioc,
            'preview': latin[:100]
        })
    
    # Approach 4: Try EODE as a key
    eode_key = [18, 3, 23, 18]  # E-O-D-E
    for mode in ['sub', 'add', 'beaufort']:
        decrypted = vigenere_decrypt(non_prime_runes, eode_key, mode)
        ioc = calc_ioc(decrypted)
        latin = indices_to_latin(decrypted)
        results.append({
            'method': f'EODE_{mode}',
            'ioc': ioc,
            'preview': latin[:100]
        })
    
    # Approach 5: Try DEOR as a key
    deor_key = [23, 18, 3, 4]  # D-E-O-R
    for mode in ['sub', 'add', 'beaufort']:
        decrypted = vigenere_decrypt(non_prime_runes, deor_key, mode)
        ioc = calc_ioc(decrypted)
        latin = indices_to_latin(decrypted)
        results.append({
            'method': f'DEOR_{mode}',
            'ioc': ioc,
            'preview': latin[:100]
        })
    
    # Approach 6: Apply the decoded stream as key to FULL cipher (not just non-primes)
    for mode in ['sub', 'add', 'beaufort']:
        decrypted = vigenere_decrypt(cipher, decoded_key, mode)
        ioc = calc_ioc(decrypted)
        latin = indices_to_latin(decrypted)
        results.append({
            'method': f'full_cipher_{mode}',
            'ioc': ioc,
            'preview': latin[:100]
        })
    
    # Sort by IoC (higher = better for English)
    results.sort(key=lambda x: x['ioc'], reverse=True)
    
    print("\n" + "="*80)
    print("RESULTS (sorted by IoC, English ~1.73, Random ~1.0)")
    print("="*80)
    
    for r in results[:15]:
        print(f"\n[{r['method']}] IoC: {r['ioc']:.4f}")
        print(f"  Preview: {r['preview']}")
    
    # Best result analysis
    best = results[0]
    if best['ioc'] > 1.3:
        print("\n" + "="*80)
        print("POTENTIAL HIT DETECTED!")
        print("="*80)
        print(f"Method: {best['method']}")
        print(f"IoC: {best['ioc']:.4f}")
        print(f"Full output: {best['preview']}")

if __name__ == '__main__':
    main()

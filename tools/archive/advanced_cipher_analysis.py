#!/usr/bin/env python3
"""
Advanced cipher analysis for Liber Primus
Tests polyalphabetic, autokey, running key, and more exotic ciphers
"""
import re
import sys
from collections import Counter
from itertools import combinations
import math

# =============================================================================
# RUNE MAPPINGS (Unicode)
# =============================================================================
RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 
           'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
PRIME_TO_IDX = {p: i for i, p in enumerate(PRIMES)}

# =============================================================================
# DATA LOADING
# =============================================================================
def load_pages():
    """Load all pages from RuneSolver.py"""
    data_file = r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py"
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        # Extract only valid runes
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    return pages

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def runes_to_indices(runes):
    return [RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX]

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def indices_to_runes(indices):
    return ''.join(IDX_TO_RUNE[i % 29] for i in indices)

def calculate_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def get_gematria(idx):
    return PRIMES[idx]

# =============================================================================
# CIPHER METHODS
# =============================================================================

def simple_shift(indices, shift):
    """Simple Caesar shift"""
    return [(i - shift) % 29 for i in indices]

def gematria_self_shift(indices):
    """Each rune shifts the next by its gematria value"""
    result = [indices[0]]
    for i in range(1, len(indices)):
        prev_gem = get_gematria(indices[i-1])
        decrypted = (indices[i] - prev_gem) % 29
        result.append(decrypted)
    return result

def vigenere_decrypt(indices, key_indices):
    """Vigenere with repeating key"""
    key_len = len(key_indices)
    return [(indices[i] - key_indices[i % key_len]) % 29 for i in range(len(indices))]

def autokey_decrypt(indices, primer):
    """Autokey cipher - plaintext becomes key"""
    result = []
    key = list(primer)  # Initial key (primer)
    for i, c in enumerate(indices):
        decrypted = (c - key[i % len(key)]) % 29
        result.append(decrypted)
        # Extend key with plaintext
        if i >= len(primer) - 1:
            key.append(result[-len(primer)])
    return result

def running_key_decrypt(indices, key_indices):
    """Running key cipher - non-repeating key"""
    return [(indices[i] - key_indices[i]) % 29 for i in range(min(len(indices), len(key_indices)))]

def beaufort_decrypt(indices, key_indices):
    """Beaufort cipher: P = K - C mod 29"""
    key_len = len(key_indices)
    return [(key_indices[i % key_len] - indices[i]) % 29 for i in range(len(indices))]

def gematria_vigenere(indices, key_indices):
    """Use gematria values as key shifts"""
    key_len = len(key_indices)
    result = []
    for i, c in enumerate(indices):
        key_gem = get_gematria(key_indices[i % key_len])
        decrypted = (c - key_gem) % 29
        result.append(decrypted)
    return result

def fibonacci_shift(indices):
    """Shift by fibonacci sequence positions"""
    fib = [1, 1]
    while len(fib) < len(indices):
        fib.append(fib[-1] + fib[-2])
    return [(indices[i] - fib[i]) % 29 for i in range(len(indices))]

def totient_shift(indices):
    """Shift by totient of position"""
    def euler_phi(n):
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
        return max(1, result)
    
    return [(indices[i] - euler_phi(i + 1)) % 29 for i in range(len(indices))]

def prime_position_shift(indices):
    """Shift each position by the nth prime"""
    return [(indices[i] - PRIMES[i % 29]) % 29 for i in range(len(indices))]

def word_based_key(runes, key_word_indices):
    """Use word positions to determine key application"""
    words = runes.split('•') if '•' in runes else [runes]
    result = []
    for word_idx, word in enumerate(words):
        indices = runes_to_indices(word)
        key_val = key_word_indices[word_idx % len(key_word_indices)]
        for idx in indices:
            result.append((idx - key_val) % 29)
    return result

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_page(page_num, runes, verbose=True):
    """Comprehensive analysis of a single page"""
    indices = runes_to_indices(runes)
    
    results = []
    
    # Test various methods
    methods = [
        ("Raw", indices),
        ("Gematria self-shift", gematria_self_shift(indices)),
        ("Fibonacci shift", fibonacci_shift(indices)),
        ("Prime position shift", prime_position_shift(indices)),
    ]
    
    # Try various simple shifts
    for shift in range(29):
        methods.append((f"Shift {shift}", simple_shift(indices, shift)))
    
    # Try various Vigenere keys
    for key_len in range(2, 8):
        for key_start in range(min(5, 29 - key_len + 1)):
            key = list(range(key_start, key_start + key_len))
            result = vigenere_decrypt(indices, key)
            methods.append((f"Vig k={key[:3]}...", result))
    
    # Analyze
    for name, decrypted in methods:
        ioc = calculate_ioc(decrypted)
        text = indices_to_text(decrypted[:50])
        results.append((ioc, name, text))
    
    # Sort by IoC
    results.sort(reverse=True)
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} ANALYSIS")
        print(f"{'='*70}")
        print(f"Length: {len(indices)} runes")
        print(f"\nTop 20 methods by IoC:")
        for i, (ioc, name, text) in enumerate(results[:20]):
            print(f"{i+1:2}. {name:25s} IoC={ioc:.4f}: {text}")
    
    return results

def analyze_kasiski(runes):
    """Kasiski examination for polyalphabetic key length"""
    indices = runes_to_indices(runes)
    
    # Find repeated sequences
    sequences = {}
    for length in range(3, 8):
        for i in range(len(indices) - length):
            seq = tuple(indices[i:i+length])
            if seq not in sequences:
                sequences[seq] = []
            sequences[seq].append(i)
    
    # Find distances between repetitions
    distances = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for i in range(len(positions) - 1):
                for j in range(i + 1, len(positions)):
                    dist = positions[j] - positions[i]
                    if dist > 0:
                        distances.append(dist)
    
    # Find GCD of distances
    if not distances:
        return None
    
    # Count factors
    factors = Counter()
    for d in distances:
        for f in range(2, min(d + 1, 30)):
            if d % f == 0:
                factors[f] += 1
    
    return factors.most_common(10)

def test_running_key_with_parable(encrypted_runes, parable_runes):
    """Use PARABLE text as running key"""
    enc_indices = runes_to_indices(encrypted_runes)
    key_indices = runes_to_indices(parable_runes)
    
    # Extend key if needed (repeat)
    while len(key_indices) < len(enc_indices):
        key_indices = key_indices + key_indices
    
    results = []
    
    # Standard running key
    decrypted = running_key_decrypt(enc_indices, key_indices)
    ioc = calculate_ioc(decrypted)
    results.append(("Running key (C-K)", ioc, indices_to_text(decrypted[:60])))
    
    # Beaufort running key
    decrypted = [(key_indices[i] - enc_indices[i]) % 29 for i in range(len(enc_indices))]
    ioc = calculate_ioc(decrypted)
    results.append(("Beaufort (K-C)", ioc, indices_to_text(decrypted[:60])))
    
    # Gematria-based running key
    decrypted = []
    for i in range(len(enc_indices)):
        key_gem = get_gematria(key_indices[i])
        dec = (enc_indices[i] - key_gem) % 29
        decrypted.append(dec)
    ioc = calculate_ioc(decrypted)
    results.append(("Gematria running key", ioc, indices_to_text(decrypted[:60])))
    
    # Sum of indices
    decrypted = [(enc_indices[i] + key_indices[i]) % 29 for i in range(len(enc_indices))]
    ioc = calculate_ioc(decrypted)
    results.append(("Sum (C+K)", ioc, indices_to_text(decrypted[:60])))
    
    return results

def test_page_56_formula_variants(indices):
    """Test variants of the Page 56 formula"""
    results = []
    
    for constant in range(-30, 150):
        # -(gematria + constant) mod 29
        decrypted = []
        for i, idx in enumerate(indices):
            gem = get_gematria(idx)
            dec = (-gem - constant) % 29
            decrypted.append(dec)
        ioc = calculate_ioc(decrypted)
        if ioc > 1.6:
            text = indices_to_text(decrypted[:60])
            results.append((ioc, f"-(gem+{constant})", text))
        
        # Position-based variant: -(gematria + position) mod 29
        decrypted = []
        for i, idx in enumerate(indices):
            gem = get_gematria(idx)
            dec = (-(gem + i)) % 29
            decrypted.append(dec)
        ioc = calculate_ioc(decrypted)
        if ioc > 1.6:
            text = indices_to_text(decrypted[:60])
            results.append((ioc, f"-(gem+pos)", text))
    
    return sorted(results, reverse=True)[:10]

def search_best_vigenere_key(indices, max_key_len=8):
    """Exhaustively search for best Vigenere key"""
    best_results = []
    
    for key_len in range(2, max_key_len + 1):
        # Split into columns
        columns = [[] for _ in range(key_len)]
        for i, idx in enumerate(indices):
            columns[i % key_len].append(idx)
        
        # Find best shift for each column
        best_key = []
        for col in columns:
            best_ioc = 0
            best_shift = 0
            for shift in range(29):
                shifted = [(c - shift) % 29 for c in col]
                ioc = calculate_ioc(shifted)
                if ioc > best_ioc:
                    best_ioc = ioc
                    best_shift = shift
            best_key.append(best_shift)
        
        # Decrypt with this key
        decrypted = vigenere_decrypt(indices, best_key)
        overall_ioc = calculate_ioc(decrypted)
        text = indices_to_text(decrypted[:60])
        key_text = indices_to_text(best_key)
        
        best_results.append((overall_ioc, key_len, best_key, key_text, text))
    
    return sorted(best_results, reverse=True)

# =============================================================================
# MAIN
# =============================================================================
def main():
    print("="*70)
    print("ADVANCED CIPHER ANALYSIS - LIBER PRIMUS")
    print("="*70)
    
    pages = load_pages()
    print(f"Loaded {len(pages)} pages\n")
    
    # Get Page 57 (PARABLE - known plaintext)
    parable_runes = pages.get(57, '')
    if parable_runes:
        print(f"PARABLE text (Page 57): {len(parable_runes)} runes")
        print(f"Text: {indices_to_text(runes_to_indices(parable_runes))}\n")
    
    # Focus analysis on Page 43 (highest IoC after gematria+)
    print("="*70)
    print("DEEP ANALYSIS: PAGE 43 (Highest IoC potential)")
    print("="*70)
    
    if 43 in pages:
        runes = pages[43]
        indices = runes_to_indices(runes)
        print(f"Page 43: {len(indices)} runes")
        
        # Kasiski test
        print("\nKasiski Analysis (key length detection):")
        kasiski = analyze_kasiski(runes)
        if kasiski:
            for factor, count in kasiski[:5]:
                print(f"  Factor {factor}: {count} occurrences")
        
        # Search best Vigenere key
        print("\nBest Vigenere keys:")
        vig_results = search_best_vigenere_key(indices)
        for ioc, key_len, key, key_text, text in vig_results[:5]:
            print(f"  len={key_len}, key={key_text}, IoC={ioc:.4f}: {text[:50]}")
        
        # Test with PARABLE running key
        if parable_runes:
            print("\nRunning key with PARABLE:")
            rk_results = test_running_key_with_parable(runes, parable_runes)
            for name, ioc, text in rk_results:
                print(f"  {name}: IoC={ioc:.4f}: {text}")
    
    # Test several encrypted pages
    print("\n" + "="*70)
    print("COMPARATIVE ANALYSIS ACROSS PAGES")
    print("="*70)
    
    # Calculate best methods for each page
    page_analysis = {}
    for page_num in sorted(pages.keys()):
        if page_num == 57:  # Skip known plaintext
            continue
        
        runes = pages[page_num]
        indices = runes_to_indices(runes)
        
        if len(indices) < 20:
            continue
        
        # Test key methods
        raw_ioc = calculate_ioc(indices)
        gem_ioc = calculate_ioc(gematria_self_shift(indices))
        
        # Best Vigenere
        vig_results = search_best_vigenere_key(indices, max_key_len=6)
        best_vig_ioc = vig_results[0][0] if vig_results else 0
        
        page_analysis[page_num] = {
            'raw': raw_ioc,
            'gematria': gem_ioc,
            'best_vig': best_vig_ioc,
            'length': len(indices)
        }
        
        print(f"Page {page_num:2}: raw={raw_ioc:.4f}, gem={gem_ioc:.4f}, vig={best_vig_ioc:.4f} ({len(indices)} runes)")
    
    # Find pages with highest potential
    print("\n" + "="*70)
    print("PAGES RANKED BY DECRYPTION POTENTIAL")
    print("="*70)
    
    # Sort by best IoC achieved
    ranked = sorted(page_analysis.items(), 
                   key=lambda x: max(x[1]['raw'], x[1]['gematria'], x[1]['best_vig']),
                   reverse=True)
    
    for i, (page_num, analysis) in enumerate(ranked[:10]):
        best = max(analysis['raw'], analysis['gematria'], analysis['best_vig'])
        print(f"{i+1}. Page {page_num}: best IoC={best:.4f}")
    
    # Deep dive into top 3
    print("\n" + "="*70)
    print("DETAILED ANALYSIS OF TOP 3 PAGES")
    print("="*70)
    
    for page_num, analysis in ranked[:3]:
        analyze_page(page_num, pages[page_num], verbose=True)

if __name__ == "__main__":
    main()

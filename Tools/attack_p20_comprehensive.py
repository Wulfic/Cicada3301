"""
Page 20 Comprehensive Attack Script
====================================
Based on hint: "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR"

Approaches:
1. Prime-based path through grid
2. Deor poem as running key after transposition
3. Prime column permutations
4. Strophe-based key extraction
"""

import collections
import os
import itertools

# === CONSTANTS ===

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# Gematria Primus prime values
IDX_TO_PRIME = {
    0: 2, 1: 3, 2: 5, 3: 7, 4: 11, 5: 13, 6: 17, 7: 19,
    8: 23, 9: 29, 10: 31, 11: 37, 12: 41, 13: 43, 14: 47, 15: 53,
    16: 59, 17: 61, 18: 67, 19: 71, 20: 73, 21: 79, 22: 83, 23: 89,
    24: 97, 25: 101, 26: 103, 27: 107, 28: 109
}

PRIME_TO_IDX = {v: k for k, v in IDX_TO_PRIME.items()}

# English letter to rune index (approximate)
ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def get_primes_up_to(n):
    return [i for i in range(2, n+1) if is_prime(i)]

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def load_deor_as_indices():
    """Load Deor poem and convert to rune indices"""
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    try:
        with open(deor_path, 'r', encoding='utf-8') as f:
            text = f.read().upper()
    except:
        return []
    
    indices = []
    for c in text:
        if c in ENGLISH_TO_IDX:
            indices.append(ENGLISH_TO_IDX[c])
    return indices

def vigenere_decrypt(cipher, key, mode='sub'):
    """Decrypt using Vigenère cipher"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            p = (c - k) % 29
        else:  # add
            p = (c + k) % 29
        result.append(p)
    return result

def beaufort_decrypt(cipher, key):
    """Decrypt using Beaufort cipher: P = K - C"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        p = (k - c) % 29
        result.append(p)
    return result

# === ATTACK FUNCTIONS ===

def attack_prime_path(runes, rows=28, cols=29):
    """Read grid following a path determined by primes"""
    print("\n" + "="*60)
    print("ATTACK: Prime-Based Path Through Grid")
    print("="*60)
    
    grid = []
    for r in range(rows):
        row = runes[r*cols:(r+1)*cols]
        grid.append(row)
    
    results = []
    
    # Path 1: Visit cells where (row * cols + col) is prime
    prime_linear = []
    for i in range(len(runes)):
        if is_prime(i):
            prime_linear.append(runes[i])
    
    ioc = calculate_ioc(prime_linear)
    results.append(("Prime linear positions", ioc, prime_linear))
    print(f"\n1. Prime linear positions (n={len(prime_linear)}): IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(prime_linear[:60])}")
    
    # Path 2: Prime row + prime col intersections
    prime_rows = [r for r in range(rows) if is_prime(r)]
    prime_cols = [c for c in range(cols) if is_prime(c)]
    
    intersections = []
    for r in prime_rows:
        for c in prime_cols:
            if r < len(grid) and c < len(grid[r]):
                intersections.append(grid[r][c])
    
    ioc = calculate_ioc(intersections)
    results.append(("Prime row/col intersections", ioc, intersections))
    print(f"\n2. Prime row/col intersections (n={len(intersections)}): IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(intersections[:60])}")
    
    # Path 3: Read by prime-numbered columns first
    prime_col_read = []
    for c in prime_cols:
        for r in range(rows):
            if c < len(grid[r]):
                prime_col_read.append(grid[r][c])
    
    ioc = calculate_ioc(prime_col_read)
    results.append(("Prime columns read vertically", ioc, prime_col_read))
    print(f"\n3. Prime columns read vertically (n={len(prime_col_read)}): IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(prime_col_read[:60])}")
    
    # Path 4: Fermat spiral (visit cells in order of distance from center, prioritizing primes)
    center_r, center_c = rows // 2, cols // 2
    cells_by_dist = []
    for r in range(rows):
        for c in range(cols):
            dist = abs(r - center_r) + abs(c - center_c)
            cells_by_dist.append((dist, r, c))
    
    cells_by_dist.sort()
    spiral_prime = []
    for i, (d, r, c) in enumerate(cells_by_dist):
        if is_prime(i) and r < len(grid) and c < len(grid[r]):
            spiral_prime.append(grid[r][c])
    
    ioc = calculate_ioc(spiral_prime)
    results.append(("Fermat spiral prime positions", ioc, spiral_prime))
    print(f"\n4. Fermat spiral prime positions (n={len(spiral_prime)}): IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(spiral_prime[:60])}")
    
    return results

def attack_deor_running_key(runes):
    """Use Deor poem as running key with various offsets"""
    print("\n" + "="*60)
    print("ATTACK: Deor Running Key (Multiple Offsets)")
    print("="*60)
    
    deor = load_deor_as_indices()
    if not deor:
        print("Could not load Deor poem")
        return []
    
    print(f"Deor length: {len(deor)}")
    
    best_results = []
    
    # Try different offsets into Deor
    for offset in range(0, min(500, len(deor) - len(runes)), 47):  # Step by 47 (P19 key length)
        key = deor[offset:offset + len(runes)]
        if len(key) < len(runes):
            key = key * (len(runes) // len(key) + 1)
            key = key[:len(runes)]
        
        # Try subtract
        result = vigenere_decrypt(runes, key, 'sub')
        ioc = calculate_ioc(result)
        if ioc > 1.2:
            best_results.append((f"Deor offset {offset} SUB", ioc, result))
        
        # Try add
        result = vigenere_decrypt(runes, key, 'add')
        ioc = calculate_ioc(result)
        if ioc > 1.2:
            best_results.append((f"Deor offset {offset} ADD", ioc, result))
        
        # Try Beaufort
        result = beaufort_decrypt(runes, key)
        ioc = calculate_ioc(result)
        if ioc > 1.2:
            best_results.append((f"Deor offset {offset} BEAUFORT", ioc, result))
    
    # Sort by IoC
    best_results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop results (IoC > 1.2):")
    for name, ioc, result in best_results[:10]:
        print(f"  {name}: IoC={ioc:.4f}")
        print(f"    Preview: {runes_to_latin(result[:80])}")
    
    return best_results

def attack_transposed_then_deor(runes, rows=28, cols=29):
    """First transpose, then apply Deor key"""
    print("\n" + "="*60)
    print("ATTACK: Transpose Grid, Then Apply Deor Key")
    print("="*60)
    
    grid = []
    for r in range(rows):
        row = runes[r*cols:(r+1)*cols]
        grid.append(row)
    
    deor = load_deor_as_indices()
    if not deor:
        print("Could not load Deor poem")
        return []
    
    results = []
    
    # Transposition 1: Column-major read
    col_major = []
    for c in range(cols):
        for r in range(rows):
            if c < len(grid[r]):
                col_major.append(grid[r][c])
    
    # Apply Deor
    key = deor[:len(col_major)]
    if len(key) < len(col_major):
        key = key * (len(col_major) // len(key) + 1)
        key = key[:len(col_major)]
    
    result = vigenere_decrypt(col_major, key, 'sub')
    ioc = calculate_ioc(result)
    results.append(("Column-major + Deor SUB", ioc, result))
    print(f"\n1. Column-major + Deor SUB: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    result = vigenere_decrypt(col_major, key, 'add')
    ioc = calculate_ioc(result)
    results.append(("Column-major + Deor ADD", ioc, result))
    print(f"\n2. Column-major + Deor ADD: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    # Transposition 2: Reverse columns
    rev_cols = []
    for r in range(rows):
        for c in range(cols-1, -1, -1):
            if c < len(grid[r]):
                rev_cols.append(grid[r][c])
    
    result = vigenere_decrypt(rev_cols, key, 'sub')
    ioc = calculate_ioc(result)
    results.append(("Reverse columns + Deor SUB", ioc, result))
    print(f"\n3. Reverse columns + Deor SUB: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    # Transposition 3: Prime column permutation
    prime_cols = [c for c in range(cols) if is_prime(c)]
    non_prime_cols = [c for c in range(cols) if not is_prime(c)]
    col_order = prime_cols + non_prime_cols
    
    permuted = []
    for r in range(rows):
        for c in col_order:
            if c < len(grid[r]):
                permuted.append(grid[r][c])
    
    result = vigenere_decrypt(permuted, key, 'sub')
    ioc = calculate_ioc(result)
    results.append(("Prime cols first + Deor SUB", ioc, result))
    print(f"\n4. Prime cols first + Deor SUB: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    return results

def attack_deor_strophe_key(runes):
    """Use Deor strophes to derive key"""
    print("\n" + "="*60)
    print("ATTACK: Deor Strophe-Based Keys")
    print("="*60)
    
    # Deor strophe structure (approximate character counts per strophe)
    # Strophe 1: lines 1-7 (Wayland)
    # Strophe 2: lines 8-14 (Beadohild)
    # Strophe 3: lines 15-18 (Maethhild)
    # Strophe 4: lines 19-22 (Theodric)
    # Strophe 5: lines 23-30 (Eormanric)
    # Strophe 6: lines 31-38 (general suffering)
    # Strophe 7: lines 39-46 (Deor himself)
    
    # The refrain: "Þæs ofereode, þisses swa mæg" appears 7 times
    refrain = "THAESOFEREODETHISTHESOEWAMAEAE"  # Approximation
    refrain_indices = [ENGLISH_TO_IDX.get(c, 0) for c in refrain]
    
    print(f"Refrain length: {len(refrain_indices)}")
    
    results = []
    
    # Try refrain as key
    key = refrain_indices * (len(runes) // len(refrain_indices) + 1)
    key = key[:len(runes)]
    
    result = vigenere_decrypt(runes, key, 'sub')
    ioc = calculate_ioc(result)
    results.append(("Refrain SUB", ioc, result))
    print(f"\n1. Refrain as key SUB: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    result = vigenere_decrypt(runes, key, 'add')
    ioc = calculate_ioc(result)
    results.append(("Refrain ADD", ioc, result))
    print(f"\n2. Refrain as key ADD: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    # Try "DEOR" repeated
    deor_word = [23, 18, 3, 4]  # D E O R
    key = deor_word * (len(runes) // 4 + 1)
    key = key[:len(runes)]
    
    result = vigenere_decrypt(runes, key, 'sub')
    ioc = calculate_ioc(result)
    results.append(("DEOR word SUB", ioc, result))
    print(f"\n3. 'DEOR' as key SUB: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    # Try prime strophes (2, 3, 5, 7 = strophes 2,3,5,7)
    deor = load_deor_as_indices()
    if deor:
        # Approximate strophe boundaries (chars, not lines)
        strophe_bounds = [0, 150, 300, 380, 440, 600, 750, 900]
        prime_strophes = [2, 3, 5, 7]
        
        prime_key = []
        for s in prime_strophes:
            if s < len(strophe_bounds):
                start = strophe_bounds[s-1]
                end = strophe_bounds[s] if s < len(strophe_bounds) else len(deor)
                prime_key.extend(deor[start:end])
        
        if prime_key:
            key = prime_key * (len(runes) // len(prime_key) + 1)
            key = key[:len(runes)]
            
            result = vigenere_decrypt(runes, key, 'sub')
            ioc = calculate_ioc(result)
            results.append(("Prime strophes (2,3,5,7) SUB", ioc, result))
            print(f"\n4. Prime strophes (2,3,5,7) SUB: IoC={ioc:.4f}")
            print(f"   Preview: {runes_to_latin(result[:80])}")
    
    return results

def attack_prime_value_transform(runes):
    """Transform using the prime VALUES of runes"""
    print("\n" + "="*60)
    print("ATTACK: Prime Value Transformations")
    print("="*60)
    
    results = []
    
    # Get prime values for each rune
    prime_values = [IDX_TO_PRIME[r] for r in runes]
    
    # Transform 1: Map prime values modulo 29
    mod29 = [p % 29 for p in prime_values]
    ioc = calculate_ioc(mod29)
    results.append(("Prime values mod 29", ioc, mod29))
    print(f"\n1. Prime values mod 29: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(mod29[:60])}")
    
    # Transform 2: Differences of consecutive primes mod 29
    diffs = [(prime_values[i+1] - prime_values[i]) % 29 for i in range(len(prime_values)-1)]
    ioc = calculate_ioc(diffs)
    results.append(("Consecutive prime diffs mod 29", ioc, diffs))
    print(f"\n2. Consecutive prime diffs mod 29: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(diffs[:60])}")
    
    # Transform 3: XOR-like operation with prime sequence
    prime_seq = get_primes_up_to(1000)[:len(runes)]
    xor_result = [(runes[i] ^ (prime_seq[i] % 29)) % 29 for i in range(len(prime_seq))]
    ioc = calculate_ioc(xor_result)
    results.append(("XOR with prime sequence", ioc, xor_result))
    print(f"\n3. XOR with prime sequence: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(xor_result[:60])}")
    
    # Transform 4: Use totient function phi(prime) = prime - 1
    totients = [(IDX_TO_PRIME[r] - 1) % 29 for r in runes]
    ioc = calculate_ioc(totients)
    results.append(("Totient values mod 29", ioc, totients))
    print(f"\n4. Totient values mod 29: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(totients[:60])}")
    
    return results

def attack_columnar_permutation(runes, rows=28, cols=29):
    """Try columnar transposition with prime-based permutations"""
    print("\n" + "="*60)
    print("ATTACK: Columnar Permutation Based on Primes")
    print("="*60)
    
    grid = []
    for r in range(rows):
        row = runes[r*cols:(r+1)*cols]
        grid.append(row)
    
    # Get first 29 primes for column ordering
    primes_29 = get_primes_up_to(120)[:29]  # First 29 primes
    
    results = []
    
    # Permutation 1: Order columns by their corresponding prime
    col_prime_pairs = [(primes_29[c], c) for c in range(cols)]
    col_prime_pairs.sort()  # Sort by prime value
    col_order = [c for _, c in col_prime_pairs]
    
    permuted = []
    for r in range(rows):
        for c in col_order:
            if c < len(grid[r]):
                permuted.append(grid[r][c])
    
    ioc = calculate_ioc(permuted)
    results.append(("Columns sorted by prime value", ioc, permuted))
    print(f"\n1. Columns sorted by prime value: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(permuted[:80])}")
    
    # Permutation 2: Order columns by (prime mod 29)
    col_mod_pairs = [(primes_29[c] % 29, c) for c in range(cols)]
    col_mod_pairs.sort()
    col_order = [c for _, c in col_mod_pairs]
    
    permuted = []
    for r in range(rows):
        for c in col_order:
            if c < len(grid[r]):
                permuted.append(grid[r][c])
    
    ioc = calculate_ioc(permuted)
    results.append(("Columns sorted by prime mod 29", ioc, permuted))
    print(f"\n2. Columns sorted by prime mod 29: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(permuted[:80])}")
    
    # Permutation 3: Interleave prime and non-prime columns
    prime_cols = [c for c in range(cols) if is_prime(c)]
    non_prime_cols = [c for c in range(cols) if not is_prime(c)]
    
    interleaved = []
    for i in range(max(len(prime_cols), len(non_prime_cols))):
        if i < len(prime_cols):
            interleaved.append(prime_cols[i])
        if i < len(non_prime_cols):
            interleaved.append(non_prime_cols[i])
    
    permuted = []
    for r in range(rows):
        for c in interleaved:
            if c < len(grid[r]):
                permuted.append(grid[r][c])
    
    ioc = calculate_ioc(permuted)
    results.append(("Interleaved prime/non-prime cols", ioc, permuted))
    print(f"\n3. Interleaved prime/non-prime cols: IoC={ioc:.4f}")
    print(f"   Preview: {runes_to_latin(permuted[:80])}")
    
    # Now try applying Deor key to best permutation
    deor = load_deor_as_indices()
    if deor and results:
        best_perm = max(results, key=lambda x: x[1])[2]
        key = deor[:len(best_perm)]
        if len(key) < len(best_perm):
            key = key * (len(best_perm) // len(key) + 1)
            key = key[:len(best_perm)]
        
        decrypted = vigenere_decrypt(best_perm, key, 'sub')
        ioc = calculate_ioc(decrypted)
        print(f"\n4. Best permutation + Deor key: IoC={ioc:.4f}")
        print(f"   Preview: {runes_to_latin(decrypted[:80])}")
        results.append(("Best perm + Deor", ioc, decrypted))
    
    return results

def attack_autokey_variants(runes):
    """Try autokey cipher variants"""
    print("\n" + "="*60)
    print("ATTACK: Autokey Cipher Variants")
    print("="*60)
    
    results = []
    
    # Primer from P19 hint
    primers = [
        "REARRANGINGTHEPRIMESNUMBERS",
        "PRIMENUMBERS",
        "DEOR",
        "THAESOFEREODETHISTHESOEWAMAEAE",  # Refrain
    ]
    
    for primer_text in primers:
        primer = [ENGLISH_TO_IDX.get(c, 0) for c in primer_text.upper()]
        
        # Autokey decrypt (standard)
        result = []
        key = list(primer)
        for i, c in enumerate(runes):
            if i < len(primer):
                k = primer[i]
            else:
                k = result[i - len(primer)]
            p = (c - k) % 29
            result.append(p)
        
        ioc = calculate_ioc(result)
        if ioc > 1.0:
            results.append((f"Autokey '{primer_text[:20]}...' SUB", ioc, result))
            print(f"\nAutokey '{primer_text[:20]}...' SUB: IoC={ioc:.4f}")
            print(f"  Preview: {runes_to_latin(result[:60])}")
        
        # Autokey using ciphertext
        result = []
        for i, c in enumerate(runes):
            if i < len(primer):
                k = primer[i]
            else:
                k = runes[i - len(primer)]
            p = (c - k) % 29
            result.append(p)
        
        ioc = calculate_ioc(result)
        if ioc > 1.0:
            results.append((f"Autokey-CT '{primer_text[:20]}...'", ioc, result))
            print(f"\nAutokey-CT '{primer_text[:20]}...': IoC={ioc:.4f}")
            print(f"  Preview: {runes_to_latin(result[:60])}")
    
    return results

def main():
    print("="*60)
    print("PAGE 20 COMPREHENSIVE ATTACK")
    print("="*60)
    
    rune_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    runes = load_runes(rune_path)
    
    print(f"\nLoaded {len(runes)} runes")
    print(f"Grid: 28 rows × 29 cols = {28*29}")
    print(f"Base IoC: {calculate_ioc(runes):.4f}")
    
    all_results = []
    
    # Run all attacks
    all_results.extend(attack_prime_path(runes))
    all_results.extend(attack_deor_running_key(runes))
    all_results.extend(attack_transposed_then_deor(runes))
    all_results.extend(attack_deor_strophe_key(runes))
    all_results.extend(attack_prime_value_transform(runes))
    all_results.extend(attack_columnar_permutation(runes))
    all_results.extend(attack_autokey_variants(runes))
    
    # Sort all results by IoC
    all_results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*60)
    print("TOP 15 RESULTS BY IoC")
    print("="*60)
    
    for i, (name, ioc, result) in enumerate(all_results[:15]):
        print(f"\n{i+1}. {name}")
        print(f"   IoC: {ioc:.4f}")
        print(f"   Text: {runes_to_latin(result[:100])}")
    
    # Check if any result looks like English
    print("\n" + "="*60)
    print("ENGLISH WORD CHECK (Top 5)")
    print("="*60)
    
    common_words = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'FOR', 'BE', 'AS', 'AT', 'THIS', 'WITH', 'ARE', 'FROM', 'THAT', 'WAS', 'HE', 'SHE', 'WE', 'THEY', 'ALL', 'HAVE', 'NOT', 'BUT', 'WHAT', 'CAN', 'OUT', 'ONE']
    
    for name, ioc, result in all_results[:5]:
        text = runes_to_latin(result)
        found = [w for w in common_words if w in text]
        print(f"\n{name} (IoC={ioc:.4f}):")
        print(f"  Words found: {found[:10]}")

if __name__ == "__main__":
    main()

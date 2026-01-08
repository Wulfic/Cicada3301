#!/usr/bin/env python3
"""
Test the Page 56 method (prime-1 subtraction / totient) on Pages 0-4.
Based on community-confirmed solving method for Page 56.

Page 56 formula: decimal[i] = (decimal[i] - (primes[i] - 1)) % 29
This is equivalent to: decimal[i] = (decimal[i] - φ(primes[i])) % 29
where φ(p) = p - 1 for prime p.
"""

# Gematria Primus
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
IDX_TO_LETTER = ['F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
                 'A', 'AE', 'Y', 'IA', 'EA']

# First 300 primes
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
          157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 
          239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 
          331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 
          421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
          509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
          613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
          709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
          821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
          919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019,
          1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097,
          1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
          1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291,
          1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409,
          1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487,
          1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579,
          1583, 1597, 1601, 1607, 1609, 1613, 1619]

# English frequency scoring
ENGLISH_FREQ = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 
                'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
                'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0,
                'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.1, 'Z': 0.07}
ENGLISH_BIGRAMS = {'TH': 15.2, 'HE': 12.8, 'IN': 9.8, 'ER': 9.4, 'AN': 8.2, 'RE': 6.8, 
                   'ON': 6.5, 'AT': 6.2, 'EN': 5.6, 'ND': 5.6, 'TI': 5.4, 'ES': 5.2,
                   'OR': 5.0, 'TE': 4.6, 'OF': 4.0, 'ED': 4.0, 'IS': 4.0, 'IT': 4.0,
                   'AL': 3.8, 'AR': 3.6, 'ST': 3.6, 'TO': 3.2, 'NT': 3.2, 'NG': 3.0}

def score_text(text):
    """Score text based on English letter and bigram frequency."""
    text = text.upper()
    score = 0
    
    for char in text:
        if char in ENGLISH_FREQ:
            score += ENGLISH_FREQ[char]
    
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in ENGLISH_BIGRAMS:
            score += ENGLISH_BIGRAMS[bigram] * 2
    
    return score

def parse_runes_from_file(filepath):
    """Extract just the runes from a rune file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    indices = []
    for char in content:
        if char in RUNE_TO_IDX:
            indices.append(RUNE_TO_IDX[char])
    return indices

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(IDX_TO_LETTER[i] for i in indices)

def method_prime_minus_1(cipher_indices):
    """Page 56 method: subtract (prime[i] - 1) from each position."""
    result = []
    for i, c in enumerate(cipher_indices):
        if i < len(PRIMES):
            shift = (PRIMES[i] - 1) % 29
            result.append((c - shift) % 29)
        else:
            result.append(c)  # No more primes, keep as-is
    return result

def method_prime_only(cipher_indices):
    """Alternative: subtract prime[i] directly."""
    result = []
    for i, c in enumerate(cipher_indices):
        if i < len(PRIMES):
            shift = PRIMES[i] % 29
            result.append((c - shift) % 29)
        else:
            result.append(c)
    return result

def method_totient_sequence(cipher_indices):
    """Use φ(i+1) as shift sequence."""
    def phi(n):
        result = 0
        for k in range(1, n + 1):
            from math import gcd
            if gcd(n, k) == 1:
                result += 1
        return result
    
    result = []
    for i, c in enumerate(cipher_indices):
        shift = phi(i + 1) % 29
        result.append((c - shift) % 29)
    return result

def method_prime_plus_offset(cipher_indices, offset):
    """Subtract (prime[i] + offset) from each position."""
    result = []
    for i, c in enumerate(cipher_indices):
        if i < len(PRIMES):
            shift = (PRIMES[i] + offset) % 29
            result.append((c - shift) % 29)
        else:
            result.append(c)
    return result

def test_page(page_num, filepath):
    """Test all methods on a page."""
    print(f"\n{'='*60}")
    print(f"PAGE {page_num}")
    print(f"{'='*60}")
    
    try:
        cipher_indices = parse_runes_from_file(filepath)
        print(f"Loaded {len(cipher_indices)} runes from {filepath}")
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return
    
    # Test various methods
    methods = [
        ("Prime - 1 (Page 56 method)", method_prime_minus_1(cipher_indices)),
        ("Prime only", method_prime_only(cipher_indices)),
        ("Prime + 57", method_prime_plus_offset(cipher_indices, 57)),
    ]
    
    results = []
    for name, result_indices in methods:
        text = indices_to_text(result_indices)
        score = score_text(text)
        results.append((name, score, text[:80]))
    
    # Sort by score
    results.sort(key=lambda x: -x[1])
    
    print("\nResults (sorted by score):")
    print("-" * 60)
    for name, score, text in results:
        print(f"\n{name}: Score = {score:.1f}")
        print(f"Output: {text}...")
    
    # Show best full output
    print(f"\n\nBest result: {results[0][0]}")
    best_indices = methods[0][1] if results[0][0] == methods[0][0] else methods[1][1]
    for name, result_indices in methods:
        if name == results[0][0]:
            text = indices_to_text(result_indices)
            print(f"Full output ({len(text)} chars):")
            print(text)
            break

def main():
    print("Testing Page 56 Method (Prime - 1 subtraction) on Pages 0-4")
    print("=" * 70)
    print("\nThis method solved Page 56:")
    print("  decimal[i] = (decimal[i] - (primes[i] - 1)) % 29")
    print("  Equivalent to: decimal[i] = (decimal[i] - φ(primes[i])) % 29")
    print("\nTesting on original ciphertext (not first-layer output)...")
    
    base_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    
    for page_num in range(5):
        page_dir = f"page_{page_num:02d}"
        runes_file = f"{base_path}\\{page_dir}\\runes.txt"
        test_page(page_num, runes_file)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nIf scores are low, the prime-1 method doesn't work directly on these pages.")
    print("Our SUB mod 29 with key-length attack may be the correct first layer.")
    print("The second layer might use the prime-1 method on our first-layer output.")

if __name__ == "__main__":
    main()

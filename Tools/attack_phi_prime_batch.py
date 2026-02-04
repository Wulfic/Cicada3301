#!/usr/bin/env python3
"""
Apply φ(prime) cipher method to unsolved pages

This method is CONFIRMED to work on Pages 55 and 73:
- Formula: plaintext[i] = (cipher[i] - φ(prime[key_idx])) mod 29
- φ(p) = p-1 for primes (Euler's totient function)
- Literal F rule: When cipher=ᚠ and expected plaintext=F, output F without incrementing key

Testing on: Pages 20-54
"""

import os
from collections import Counter

# Gematria Primus
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

def get_primes(n):
    """Generate first n primes."""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

def euler_totient(n):
    """Euler's totient function φ(n). For prime p, φ(p) = p-1."""
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
    return result

def load_runes(filepath):
    """Load runes from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def calc_ioc(indices):
    """Calculate Index of Coincidence."""
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    """Convert indices to Latin text."""
    return ''.join(LATIN_TABLE[i] for i in indices)

def phi_prime_decrypt(cipher, start_prime_idx=0, use_literal_f=True):
    """
    Decrypt using φ(prime) method.
    
    Args:
        cipher: List of rune indices
        start_prime_idx: Which prime to start with (0 = prime[0] = 2)
        use_literal_f: Whether to apply the literal F rule
    """
    primes = get_primes(len(cipher) + start_prime_idx + 100)
    result = []
    key_idx = start_prime_idx
    
    for i, c in enumerate(cipher):
        # Literal F rule: if cipher is ᚠ (0), check if it should be literal F
        if use_literal_f and c == 0:
            # We assume literal F and don't increment the key
            result.append(0)  # F
            continue
        
        # Apply φ(prime) decryption
        phi_val = primes[key_idx] - 1  # φ(p) = p-1 for prime p
        key = phi_val % 29
        plain = (c - key) % 29
        result.append(plain)
        key_idx += 1
    
    return result

def phi_prime_decrypt_add(cipher, start_prime_idx=0, use_literal_f=True):
    """φ(prime) with ADD instead of SUB."""
    primes = get_primes(len(cipher) + start_prime_idx + 100)
    result = []
    key_idx = start_prime_idx
    
    for i, c in enumerate(cipher):
        if use_literal_f and c == 0:
            result.append(0)
            continue
        
        phi_val = primes[key_idx] - 1
        key = phi_val % 29
        plain = (c + key) % 29
        result.append(plain)
        key_idx += 1
    
    return result

def score_english(text):
    """Score text based on English patterns."""
    score = 0
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
                    'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HIS', 'HAS',
                    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM',
                    'THEY', 'BEEN', 'SOME', 'WHO', 'ITS', 'WHAT', 'WHEN',
                    'CIRCUMFERENCE', 'DIVINITY', 'SACRED', 'PRIMES', 'WISDOM',
                    'WITHIN', 'BEING', 'PILGRIMAGE', 'PILGRIM', 'SEEK', 'PATH',
                    'KOAN', 'INSTRUCTION', 'WARNING', 'EPILOGUE', 'DEEP', 'WEB',
                    'BELIEVE', 'NOTHING', 'BOOK', 'TRUE', 'QUESTION', 'THINGS',
                    'INSTAR', 'TUNNEL', 'SURFACE', 'EMERGE', 'PARABLE']
    for word in common_words:
        count = text.count(word)
        if count:
            score += len(word) * 10 * count
    return score

def analyze_page(page_num, repo_path):
    """Analyze a single page with φ(prime) methods."""
    page_dir = os.path.join(repo_path, 'LiberPrimus', 'pages', f'page_{page_num:02d}')
    runes_path = os.path.join(page_dir, 'runes.txt')
    
    if not os.path.exists(runes_path):
        return None
    
    cipher = load_runes(runes_path)
    if len(cipher) < 10:
        return None
    
    results = []
    
    # Test various starting prime indices and both modes
    for start_idx in range(10):  # Try starting at different primes
        for use_literal_f in [True, False]:
            for mode in ['sub', 'add']:
                if mode == 'sub':
                    decrypted = phi_prime_decrypt(cipher, start_idx, use_literal_f)
                else:
                    decrypted = phi_prime_decrypt_add(cipher, start_idx, use_literal_f)
                
                ioc = calc_ioc(decrypted)
                latin = indices_to_latin(decrypted)
                eng_score = score_english(latin)
                
                results.append({
                    'page': page_num,
                    'start_idx': start_idx,
                    'literal_f': use_literal_f,
                    'mode': mode,
                    'ioc': ioc,
                    'eng_score': eng_score,
                    'preview': latin[:100],
                    'rune_count': len(cipher)
                })
    
    return results

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    
    # Pages to test (unsolved pages)
    unsolved_pages = list(range(20, 55)) + [2, 65, 66, 69, 70, 71]
    
    all_results = []
    
    print("Testing φ(prime) cipher on unsolved pages...")
    print("="*80)
    
    for page_num in unsolved_pages:
        results = analyze_page(page_num, repo)
        if results:
            all_results.extend(results)
            # Get best result for this page
            best = max(results, key=lambda x: x['ioc'])
            if best['ioc'] > 1.2 or best['eng_score'] > 50:
                print(f"\nPage {page_num:02d} ({best['rune_count']} runes):")
                print(f"  Best IoC: {best['ioc']:.4f} (start={best['start_idx']}, F={best['literal_f']}, {best['mode']})")
                print(f"  Eng Score: {best['eng_score']}")
                print(f"  Preview: {best['preview'][:80]}")
    
    # Find overall best hits
    print("\n" + "="*80)
    print("TOP 20 RESULTS OVERALL")
    print("="*80)
    
    all_results.sort(key=lambda x: (x['ioc'], x['eng_score']), reverse=True)
    
    seen_pages = set()
    count = 0
    for r in all_results:
        if r['page'] not in seen_pages and count < 20:
            seen_pages.add(r['page'])
            count += 1
            print(f"\nPage {r['page']:02d} | IoC: {r['ioc']:.4f} | EngScore: {r['eng_score']}")
            print(f"  Start Prime Idx: {r['start_idx']}, Literal F: {r['literal_f']}, Mode: {r['mode']}")
            print(f"  Preview: {r['preview'][:80]}")
    
    # Filter for promising results
    print("\n" + "="*80)
    print("PROMISING HITS (IoC > 1.4 or EngScore > 100)")
    print("="*80)
    
    promising = [r for r in all_results if r['ioc'] > 1.4 or r['eng_score'] > 100]
    for r in promising:
        print(f"\n*** Page {r['page']:02d} ***")
        print(f"IoC: {r['ioc']:.4f}, Eng Score: {r['eng_score']}")
        print(f"Mode: {r['mode']}, Start Idx: {r['start_idx']}, Literal F: {r['literal_f']}")
        print(f"Preview: {r['preview']}")

if __name__ == '__main__':
    main()

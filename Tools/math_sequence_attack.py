#!/usr/bin/env python3
"""
MATHEMATICAL SEQUENCE KEY ATTACK

The unsolved pages have IoC ≈ 0.034 (random), but page 55 with same IoC 
was solved using φ(prime) sequence. This suggests unsolved pages may use
a different mathematical sequence.

Testing various mathematical sequences as key streams.
"""

from pathlib import Path
from collections import Counter

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

# Extended prime list
def sieve_primes(n):
    """Generate primes up to n using sieve."""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]

PRIMES = sieve_primes(10000)

# Fibonacci sequence
def fibonacci_sequence(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

FIBONACCI = fibonacci_sequence(1000)

# Lucas numbers
def lucas_sequence(n):
    luc = [2, 1]
    for i in range(2, n):
        luc.append(luc[-1] + luc[-2])
    return luc

LUCAS = lucas_sequence(1000)

# Triangular numbers
TRIANGULAR = [n * (n + 1) // 2 for n in range(1, 1001)]

# Prime gaps
PRIME_GAPS = [PRIMES[i+1] - PRIMES[i] for i in range(len(PRIMES) - 1)]

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    rune_file = page_dir / "runes.txt"
    if not rune_file.exists():
        return None
    with open(rune_file, 'r', encoding='utf-8') as f:
        return f.read()

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def score_result(text):
    """Score based on English patterns."""
    COMMON_WORDS = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'WITH', 'THIS', 'THAT', 'FROM', 'HAVE', 'WILL', 'WHAT', 'WHEN', 
        'THERE', 'THEIR', 'WHICH', 'BEING', 'AN', 'A', 'TO', 'IN', 'IT', 
        'IS', 'BE', 'AS', 'AT', 'SO', 'WE', 'HE', 'BY', 'OR', 'ON', 'DO',
        'SOME', 'WISDOM', 'PILGRIM', 'TRUTH', 'KNOW', 'SACRED', 'PRIMES',
        'INSTRUCTION', 'PARABLE', 'WITHIN', 'DEEP', 'WEB', 'PAGE', 'DUTY',
        'QUESTION', 'DISCOVER', 'FOLLOW', 'NOTHING', 'OTHERS', 'YOURSELF',
        'EPILOGUE', 'WARNING', 'WELCOME', 'JOURNEY', 'DIVINITY', 'END'
    ]
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def decrypt_with_sequence(cipher, sequence, operation='sub'):
    """Decrypt using a mathematical sequence as key."""
    result = []
    for i, c in enumerate(cipher):
        k = sequence[i % len(sequence)] % 29
        if operation == 'sub':
            p = (c - k) % 29
        else:  # add
            p = (c + k) % 29
        result.append(p)
    return result

def test_sequences(cipher, page_num):
    """Test various mathematical sequences."""
    results = []
    
    sequences = {
        # φ(prime) sequences
        'phi_primes': [p - 1 for p in PRIMES],
        'phi_primes_offset_10': [PRIMES[i+10] - 1 for i in range(len(PRIMES)-10)],
        'phi_primes_offset_17': [PRIMES[i+17] - 1 for i in range(len(PRIMES)-17)],
        
        # Direct prime sequences
        'primes': PRIMES,
        'primes_offset_10': PRIMES[10:],
        'primes_offset_17': PRIMES[17:],
        
        # Prime indices (position of prime)
        'prime_indices': list(range(len(PRIMES))),
        
        # Fibonacci and Lucas
        'fibonacci': FIBONACCI,
        'lucas': LUCAS,
        
        # Triangular numbers
        'triangular': TRIANGULAR,
        
        # Prime gaps
        'prime_gaps': PRIME_GAPS,
        
        # Products
        'primes_squared': [p * p for p in PRIMES],
        'prime_times_index': [(i+1) * p for i, p in enumerate(PRIMES)],
        
        # Page-based offsets
        f'phi_primes_page{page_num}': [PRIMES[i+page_num] - 1 for i in range(len(PRIMES)-page_num)] if page_num < len(PRIMES) else [p - 1 for p in PRIMES],
        
        # Cumulative sums
        'phi_prime_cumsum': [sum(PRIMES[j] - 1 for j in range(i+1)) for i in range(len(PRIMES))],
        
        # Alternating
        'alternating_phi': [(PRIMES[i] - 1) * ((-1) ** i) for i in range(len(PRIMES))],
    }
    
    for name, seq in sequences.items():
        if len(seq) < len(cipher):
            continue
            
        for op in ['sub', 'add']:
            decrypted = decrypt_with_sequence(cipher, seq, op)
            text = indices_to_text(decrypted)
            score = score_result(text)
            
            if score >= 100:  # Only track promising results
                results.append({
                    'name': name,
                    'operation': op,
                    'score': score,
                    'preview': text[:100]
                })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:10]

def main():
    print("MATHEMATICAL SEQUENCE KEY ATTACK")
    print("=" * 80)
    
    # Test on a few unsolved pages
    test_pages = [17, 18, 19, 20, 21, 54]
    
    for page_num in test_pages:
        rune_text = load_page(page_num)
        if not rune_text:
            continue
            
        cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
        
        print(f"\n{'='*80}")
        print(f"PAGE {page_num} ({len(cipher)} runes)")
        print("=" * 80)
        
        results = test_sequences(cipher, page_num)
        
        if results:
            print("Top results:")
            for r in results[:5]:
                print(f"  {r['name']} ({r['operation']}): score {r['score']}")
                print(f"    {r['preview']}...")
        else:
            print("  No results with score >= 100")
        
        # Also test with different starting points for key sequences
        print("\n--- Testing different key offsets for φ(prime) ---")
        phi_seq = [p - 1 for p in PRIMES]
        
        best_offset = 0
        best_score = 0
        best_text = ""
        
        for offset in range(0, 100):
            seq = phi_seq[offset:]
            if len(seq) < len(cipher):
                break
            decrypted = decrypt_with_sequence(cipher, seq, 'sub')
            text = indices_to_text(decrypted)
            score = score_result(text)
            
            if score > best_score:
                best_score = score
                best_offset = offset
                best_text = text
        
        print(f"  Best offset: {best_offset}, score: {best_score}")
        print(f"  Preview: {best_text[:100]}...")

if __name__ == '__main__':
    main()

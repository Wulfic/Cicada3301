#!/usr/bin/env python3
"""
Test if Page 1's readable text comes from a more complex interleaving pattern
Maybe it's not every-2nd, but a different split pattern
"""

from pathlib import Path
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page1():
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_runes = segments[0]
    page1_indices = [RUNE_TO_INDEX[c] for c in page1_runes if c in RUNE_TO_INDEX]
    
    return page1_indices

def decrypt_sub(cipher_indices, key_indices):
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def indices_to_text(indices):
    return "".join(LETTERS[idx] for idx in indices)

def score_english(text):
    text = text.upper()
    common_words = ['THE', 'AND', 'OF', 'TO', 'IN', 'A', 'IS', 'THAT', 'FOR', 'IT', 'WITH', 'AS', 'WAS', 'ON', 'ARE', 'FROM', 'OR', 'BY', 'THIS', 'WHICH', 'WISDOM', 'DIVINE', 'TRUTH', 'KNOWLEDGE', 'SECRET', 'KNOW', 'UNDERSTAND']
    score = sum(text.count(word) * len(word) * 10 for word in common_words)
    
    # Bigrams
    common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
    score += sum(text.count(bg) * 5 for bg in common_bigrams)
    
    # Trigrams
    common_trigrams = ['THE', 'AND', 'ING', 'HER', 'ENT', 'ION', 'THA', 'FOR']
    score += sum(text.count(tg) * 8 for tg in common_trigrams)
    
    return score

# Best key from previous work
BEST_KEY_71 = [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7]

def test_block_interleaving(plaintext_indices):
    """Test if text is split into fixed-size blocks that are interleaved"""
    results = []
    
    # Try different block sizes
    for block_size in range(2, 20):
        # Split into blocks
        blocks = []
        for i in range(block_size):
            block = plaintext_indices[i::block_size]
            blocks.append(block)
        
        # For each block, treat as separate text
        for block_idx, block in enumerate(blocks):
            if len(block) < 10:  # Too short
                continue
            
            text = indices_to_text(block)
            score = score_english(text)
            
            if score > 500:  # Interesting threshold
                results.append({
                    'block_size': block_size,
                    'block_num': block_idx,
                    'score': score,
                    'length': len(block),
                    'text': text
                })
    
    return results

def test_alternating_pattern(plaintext_indices):
    """Test patterns like: take 1, skip 2, take 1, skip 3, etc."""
    results = []
    
    # Pattern: take N, skip M, repeat
    for take in range(1, 5):
        for skip in range(1, 10):
            extracted = []
            i = 0
            while i < len(plaintext_indices):
                # Take 'take' elements
                for _ in range(take):
                    if i < len(plaintext_indices):
                        extracted.append(plaintext_indices[i])
                        i += 1
                # Skip 'skip' elements
                i += skip
            
            if len(extracted) < 20:
                continue
            
            text = indices_to_text(extracted)
            score = score_english(text)
            
            if score > 500:
                results.append({
                    'pattern': f'take {take}, skip {skip}',
                    'score': score,
                    'length': len(extracted),
                    'text': text
                })
    
    return results

def test_prime_positions(plaintext_indices):
    """Test if readable text is at prime positions"""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [i for i in range(len(plaintext_indices)) if is_prime(i)]
    extracted = [plaintext_indices[i] for i in primes]
    
    text = indices_to_text(extracted)
    score = score_english(text)
    
    return {
        'pattern': 'prime positions',
        'score': score,
        'length': len(extracted),
        'text': text
    }

def test_fibonacci_positions(plaintext_indices):
    """Test if readable text is at Fibonacci positions"""
    fib = [0, 1]
    while fib[-1] < len(plaintext_indices):
        fib.append(fib[-1] + fib[-2])
    
    fib = [f for f in fib if f < len(plaintext_indices)]
    extracted = [plaintext_indices[i] for i in fib]
    
    text = indices_to_text(extracted)
    score = score_english(text)
    
    return {
        'pattern': 'fibonacci positions',
        'score': score,
        'length': len(extracted),
        'text': text
    }

def main():
    print("=" * 80)
    print("PAGE 1 - TESTING ADVANCED INTERLEAVING PATTERNS")
    print("=" * 80)
    
    cipher_indices = load_page1()
    plaintext_indices = decrypt_sub(cipher_indices, BEST_KEY_71)
    plaintext_text = indices_to_text(plaintext_indices)
    
    base_score = score_english(plaintext_text)
    print(f"\nBase SUB-71 output:")
    print(f"  Length: {len(plaintext_text)}")
    print(f"  Score: {base_score}")
    print(f"  Preview: {plaintext_text[:80]}")
    
    # Test 1: Block interleaving
    print("\n" + "=" * 80)
    print("BLOCK INTERLEAVING TEST")
    print("=" * 80)
    
    block_results = test_block_interleaving(plaintext_indices)
    block_results_sorted = sorted(block_results, key=lambda x: x['score'], reverse=True)
    
    print(f"\nFound {len(block_results_sorted)} interesting block patterns")
    if block_results_sorted:
        print(f"\nTop 10 block patterns:")
        print(f"{'Rank':<6} {'Block Size':<12} {'Block #':<8} {'Length':<8} {'Score':<10} {'Preview'}")
        print("-" * 100)
        
        for i, r in enumerate(block_results_sorted[:10], 1):
            preview = r['text'][:50]
            print(f"{i:<6} {r['block_size']:<12} {r['block_num']:<8} {r['length']:<8} {r['score']:<10} {preview}")
        
        # Show best in detail
        best = block_results_sorted[0]
        if best['score'] > base_score * 1.2:
            print(f"\n{'='*80}")
            print("SIGNIFICANT IMPROVEMENT FOUND!")
            print(f"{'='*80}")
            print(f"\nBlock size: {best['block_size']}")
            print(f"Block number: {best['block_num']}")
            print(f"Score: {best['score']} (vs base {base_score})")
            print(f"\nFull text:\n{best['text']}")
    
    # Test 2: Alternating patterns
    print("\n" + "=" * 80)
    print("ALTERNATING PATTERN TEST")
    print("=" * 80)
    
    alt_results = test_alternating_pattern(plaintext_indices)
    alt_results_sorted = sorted(alt_results, key=lambda x: x['score'], reverse=True)
    
    print(f"\nFound {len(alt_results_sorted)} interesting alternating patterns")
    if alt_results_sorted:
        print(f"\nTop 10 alternating patterns:")
        print(f"{'Rank':<6} {'Pattern':<20} {'Length':<8} {'Score':<10} {'Preview'}")
        print("-" * 100)
        
        for i, r in enumerate(alt_results_sorted[:10], 1):
            preview = r['text'][:50]
            print(f"{i:<6} {r['pattern']:<20} {r['length']:<8} {r['score']:<10} {preview}")
    
    # Test 3: Prime positions
    print("\n" + "=" * 80)
    print("PRIME POSITIONS TEST")
    print("=" * 80)
    
    prime_result = test_prime_positions(plaintext_indices)
    print(f"\nPattern: {prime_result['pattern']}")
    print(f"Length: {prime_result['length']}")
    print(f"Score: {prime_result['score']}")
    print(f"Preview: {prime_result['text'][:80]}")
    
    if prime_result['score'] > base_score * 1.2:
        print(f"\n✓ Prime positions show improvement!")
        print(f"\nFull text:\n{prime_result['text']}")
    
    # Test 4: Fibonacci positions
    print("\n" + "=" * 80)
    print("FIBONACCI POSITIONS TEST")
    print("=" * 80)
    
    fib_result = test_fibonacci_positions(plaintext_indices)
    print(f"\nPattern: {fib_result['pattern']}")
    print(f"Length: {fib_result['length']}")
    print(f"Score: {fib_result['score']}")
    print(f"Preview: {fib_result['text'][:80]}")
    
    if fib_result['score'] > base_score * 1.2:
        print(f"\n✓ Fibonacci positions show improvement!")
        print(f"\nFull text:\n{fib_result['text']}")
    
    # Overall conclusion
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    all_results = block_results_sorted + alt_results_sorted + [prime_result, fib_result]
    best_overall = max(all_results, key=lambda x: x['score'])
    
    if best_overall['score'] > base_score * 1.3:
        print(f"\n✓ SIGNIFICANT PATTERN FOUND!")
        pattern_name = best_overall.get('pattern', f'block {best_overall.get("block_size", "?")}')
        print(f"Pattern type: {pattern_name}")
        print(f"Score improvement: {best_overall['score']} vs {base_score} ({best_overall['score']/base_score:.2f}x)")
        print("\nThis suggests the SUB-71 output requires this specific extraction pattern.")
    else:
        print(f"\n⚠ No pattern significantly outperformed base output (base={base_score})")
        print("Possible explanations:")
        print("  1. The SUB-71 output is already in the correct order (just unusual text)")
        print("  2. More complex pattern needed (not tested here)")
        print("  3. Key or cipher operation still needs refinement")
        print("  4. Plaintext is intentionally non-standard (word list, etc.)")

if __name__ == '__main__':
    main()

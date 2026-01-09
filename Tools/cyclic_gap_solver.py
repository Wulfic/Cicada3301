#!/usr/bin/env python3
"""
Cyclic Gap Pattern Solver for Liber Primus
==========================================

Based on community research by Profetul/Mortlach suggesting that keys
may have CYCLIC GAP PATTERNS where:
- Gap = K(i+1) - K(i) follows a repeating pattern
- Pattern like [11, -18, 11, 11, -18, 11] generates "low doubles"
- 29 - 18 = 11, so +11 and -18 are equivalent mod 29

Key insight: Rather than random or sequence-based keys, the key may be
generated from a simple repeating gap pattern.
"""

import os
import sys
from pathlib import Path

# Gematria Primus mapping
GEMATRIA_PRIMUS = {
    'ᚠ': (0, 'F'), 'ᚢ': (1, 'U'), 'ᚦ': (2, 'TH'), 'ᚩ': (3, 'O'),
    'ᚱ': (4, 'R'), 'ᚳ': (5, 'CK'), 'ᚷ': (6, 'G'), 'ᚹ': (7, 'W'),
    'ᚻ': (8, 'H'), 'ᚾ': (9, 'N'), 'ᛁ': (10, 'I'), 'ᛂ': (11, 'J'),
    'ᛇ': (12, 'EO'), 'ᛈ': (13, 'P'), 'ᛉ': (14, 'X'), 'ᛋ': (15, 'S'),
    'ᛏ': (16, 'T'), 'ᛒ': (17, 'B'), 'ᛖ': (18, 'E'), 'ᛗ': (19, 'M'),
    'ᛚ': (20, 'L'), 'ᛝ': (21, 'NG'), 'ᛟ': (22, 'OE'), 'ᛞ': (23, 'D'),
    'ᚪ': (24, 'A'), 'ᚫ': (25, 'AE'), 'ᚣ': (26, 'Y'), 'ᛡ': (27, 'IA'),
    'ᛠ': (28, 'EA')
}

INDEX_TO_RUNE = {v[0]: (k, v[1]) for k, v in GEMATRIA_PRIMUS.items()}

# English letter frequency (approximate, for scoring)
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'U': 2.8,
    'C': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8
}

# Common trigrams for scoring
TRIGRAMS = set([
    'THE', 'AND', 'ING', 'ENT', 'ION', 'HER', 'FOR', 'THA', 'NTH',
    'INT', 'ERA', 'TIO', 'ERE', 'EST', 'ATE', 'ALL', 'EAR', 'ART',
    'YOU', 'OUT', 'ONE', 'ARE', 'HIS', 'WAS', 'HAS', 'HAD', 'NOT',
    'BUT', 'CAN', 'WHO', 'OUR', 'SAY', 'SHE', 'WIT', 'THI', 'PRO',
    'IVE', 'WOU', 'MAN', 'COM', 'HAS', 'BEC', 'OWN', 'WHA', 'SEL',
    'DIS', 'TRU', 'DIV', 'WIS', 'NOW', 'THO', 'FAL', 'FIN', 'UND'
])

def load_runes(page_num: int) -> str:
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return ""
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract only rune characters
    runes = ''.join(c for c in content if c in GEMATRIA_PRIMUS)
    return runes

def runes_to_indices(runes: str) -> list:
    """Convert rune string to list of indices."""
    return [GEMATRIA_PRIMUS[r][0] for r in runes if r in GEMATRIA_PRIMUS]

def indices_to_text(indices: list) -> str:
    """Convert indices to runeglish text."""
    result = []
    for idx in indices:
        if idx in INDEX_TO_RUNE:
            result.append(INDEX_TO_RUNE[idx][1])
    return ''.join(result)

def generate_cyclic_gap_key(length: int, gap_pattern: list, start: int = 0) -> list:
    """
    Generate a key using a cyclic gap pattern.
    
    Args:
        length: Length of key to generate
        gap_pattern: List of gaps that repeat cyclically
        start: Starting value for the key
    
    Returns:
        List of key indices (mod 29)
    """
    key = [start % 29]
    pattern_len = len(gap_pattern)
    
    for i in range(1, length):
        gap = gap_pattern[(i - 1) % pattern_len]
        key.append((key[-1] + gap) % 29)
    
    return key

def generate_arithmetic_key(length: int, step: int, start: int = 0) -> list:
    """
    Generate an arithmetic progression key.
    K(i) = (start + step * i) mod 29
    """
    return [(start + step * i) % 29 for i in range(length)]

def decrypt_sub(cipher_indices: list, key: list) -> list:
    """Decrypt using SUB mode: plaintext = (cipher - key) mod 29"""
    result = []
    key_len = len(key)
    for i, c in enumerate(cipher_indices):
        k = key[i % key_len]
        result.append((c - k) % 29)
    return result

def calculate_ioc(indices: list) -> float:
    """Calculate Index of Coincidence."""
    n = len(indices)
    if n <= 1:
        return 0.0
    
    freq = [0] * 29
    for idx in indices:
        freq[idx] += 1
    
    numerator = sum(f * (f - 1) for f in freq)
    denominator = n * (n - 1)
    
    return numerator / denominator if denominator > 0 else 0.0

def score_text(indices: list) -> tuple:
    """
    Score decrypted text based on:
    1. Trigram matches
    2. Letter frequency similarity
    3. IoC
    
    Returns: (score, ioc)
    """
    text = indices_to_text(indices).upper()
    
    # Trigram scoring
    trigram_score = 0
    for i in range(len(text) - 2):
        tri = text[i:i+3]
        if tri in TRIGRAMS:
            trigram_score += 100
    
    # Frequency scoring (bonus for common letters)
    freq_score = 0
    for char in text:
        if char in ENGLISH_FREQ:
            freq_score += ENGLISH_FREQ[char]
    
    # IoC
    ioc = calculate_ioc(indices)
    
    # Combined score
    total_score = trigram_score + freq_score + (ioc * 1000)
    
    return total_score, ioc

def test_cyclic_patterns_on_page(page_num: int, verbose: bool = False):
    """Test various cyclic gap patterns on a page."""
    runes = load_runes(page_num)
    if not runes:
        print(f"Page {page_num:02d}: No runes found")
        return []
    
    cipher_indices = runes_to_indices(runes)
    cipher_len = len(cipher_indices)
    
    print(f"\n{'='*60}")
    print(f"Page {page_num:02d}: {cipher_len} runes")
    print(f"{'='*60}")
    
    results = []
    
    # Gap patterns to test (based on community research)
    gap_patterns = [
        # Simple arithmetic progressions (step 11 is significant)
        ([11], "Step +11"),
        ([18], "Step +18"),
        ([-11], "Step -11"),
        ([-18], "Step -18"),
        
        # Alternating patterns from research
        ([11, -18], "Alt +11/-18"),
        ([-18, 11], "Alt -18/+11"),
        ([11, 11, -18], "11,11,-18"),
        ([11, -18, 11, 11, -18, 11], "Prof: 11,-18,11,11,-18,11"),
        
        # Other potentially significant gaps (coprime to 29)
        ([1], "Step +1"),
        ([2], "Step +2"),
        ([3], "Step +3"),
        ([5], "Step +5"),
        ([7], "Step +7"),
        ([13], "Step +13"),
        
        # Fibonacci-related gaps
        ([1, 1, 2, 3, 5, 8, 13], "Fib gaps"),
        ([3, 3, 1], "331 pattern"),
        ([29, 1], "29,1 pattern"),
    ]
    
    # Test each gap pattern with different starting values
    for gap_pattern, pattern_name in gap_patterns:
        best_score = 0
        best_start = 0
        best_ioc = 0
        best_text = ""
        
        for start in range(29):
            key = generate_cyclic_gap_key(cipher_len, gap_pattern, start)
            plain_indices = decrypt_sub(cipher_indices, key)
            score, ioc = score_text(plain_indices)
            
            if score > best_score:
                best_score = score
                best_start = start
                best_ioc = ioc
                best_text = indices_to_text(plain_indices)[:80]
        
        results.append({
            'pattern': pattern_name,
            'gaps': gap_pattern,
            'start': best_start,
            'score': best_score,
            'ioc': best_ioc,
            'preview': best_text
        })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Print top 5 results
    print(f"\nTop 5 results for Page {page_num:02d}:")
    print("-" * 80)
    for i, r in enumerate(results[:5]):
        print(f"{i+1}. Pattern: {r['pattern']:25} Start: {r['start']:2} "
              f"Score: {r['score']:8.1f} IoC: {r['ioc']:.4f}")
        print(f"   Gaps: {r['gaps']}")
        print(f"   Text: {r['preview'][:60]}...")
        print()
    
    return results

def analyze_solved_key_gaps():
    """Analyze gap patterns in known solved keys."""
    known_keys = {
        'DIVINITY': 'DIVINITY',
        'FIRFUMFERENFE': 'FIRFUMFERENFE',
        'CONSUMPTION': 'CONSUMPTION',
        'KAON': 'KAON',
        'CICADA': 'CICADA'
    }
    
    print("\n" + "="*60)
    print("ANALYZING GAP PATTERNS IN KNOWN KEYS")
    print("="*60)
    
    for name, key in known_keys.items():
        # Convert key to indices
        indices = []
        for char in key.upper():
            for rune, (idx, letter) in GEMATRIA_PRIMUS.items():
                if letter.upper() == char or (len(letter) > 1 and letter[0].upper() == char):
                    indices.append(idx)
                    break
        
        if len(indices) < 2:
            continue
        
        # Calculate gaps
        gaps = [(indices[i+1] - indices[i]) % 29 for i in range(len(indices)-1)]
        
        print(f"\n{name}:")
        print(f"  Indices: {indices}")
        print(f"  Gaps:    {gaps}")
        print(f"  Gaps (signed): {[(g if g <= 14 else g-29) for g in gaps]}")

def main():
    print("="*60)
    print("CYCLIC GAP PATTERN SOLVER FOR LIBER PRIMUS")
    print("Based on Profetul/Mortlach research")
    print("="*60)
    
    # First, analyze known key gaps
    analyze_solved_key_gaps()
    
    # Test unsolved pages
    unsolved_pages = list(range(18, 55))  # Pages 18-54
    
    all_results = []
    
    for page in unsolved_pages:
        results = test_cyclic_patterns_on_page(page)
        if results:
            all_results.append({
                'page': page,
                'best': results[0] if results else None
            })
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY - BEST RESULTS PER PAGE")
    print("="*60)
    
    # Sort by IoC (looking for IoC > 0.04 which would indicate non-random)
    all_results.sort(key=lambda x: x['best']['ioc'] if x['best'] else 0, reverse=True)
    
    print(f"\n{'Page':<6} {'Pattern':<30} {'IoC':<8} {'Score':<10}")
    print("-"*60)
    for r in all_results[:15]:
        if r['best']:
            print(f"{r['page']:<6} {r['best']['pattern']:<30} "
                  f"{r['best']['ioc']:<8.4f} {r['best']['score']:<10.1f}")

if __name__ == "__main__":
    main()

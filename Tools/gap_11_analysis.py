#!/usr/bin/env python3
"""
GAP-11 DETAILED ANALYSIS

The community found that the unsolved pages have special structure at 11-character gaps.
This tool explores the gap-11 hypothesis in depth.

Specifically testing:
1. Every 11th character forms a pattern
2. Key = position mod 11 based
3. Interleaved streams separated by 11
"""

import os
from pathlib import Path
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

ENGLISH = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
    'WE', 'THE', 'AND', 'FOR', 'THY', 'WITH', 'THIS', 'THAT', 'PATH',
    'YEA', 'NAY', 'NOT', 'BUT', 'HATH', 'DOTH', 'THOU', 'THEE'
}

def load_runes(page_num):
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_rune_stream(rune_text):
    return [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def extract_gap_streams(runes, gap):
    """Extract 'gap' interleaved streams from runes."""
    streams = [[] for _ in range(gap)]
    for i, r in enumerate(runes):
        streams[i % gap].append(r)
    return streams

def analyze_gap_IoC(runes, max_gap=30):
    """Calculate Index of Coincidence for each gap."""
    print("Index of Coincidence by gap size:")
    print("-" * 40)
    
    results = []
    
    for gap in range(2, max_gap + 1):
        streams = extract_gap_streams(runes, gap)
        
        # Calculate IoC for each stream
        iocs = []
        for stream in streams:
            if len(stream) < 2:
                continue
            freq = Counter(stream)
            n = len(stream)
            ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) if n > 1 else 0
            iocs.append(ioc)
        
        avg_ioc = sum(iocs) / len(iocs) if iocs else 0
        results.append((gap, avg_ioc))
        
        if gap <= 15 or avg_ioc > 0.05:
            print(f"Gap {gap:2d}: IoC = {avg_ioc:.4f}")
    
    # Find peak
    best_gap = max(results, key=lambda x: x[1])
    print(f"\nBest gap: {best_gap[0]} with IoC = {best_gap[1]:.4f}")
    
    return best_gap[0]

def test_gap_decryption(runes, gap):
    """Test decryption using gap-based key."""
    
    print(f"\nTesting gap={gap} decryption:")
    print("-" * 40)
    
    # Key = [k0, k1, k2, ... k_{gap-1}]
    # key[i] = K[i mod gap]
    
    # Try all possible key combinations (brute force first key positions)
    best_score = 0
    best_key = None
    best_plain = None
    
    # Try simple linear keys: K[j] = (j * mult + offset) mod 29
    for mult in range(29):
        for offset in range(29):
            key = [(j * mult + offset) % 29 for j in range(gap)]
            plain = [(runes[i] - key[i % gap]) % 29 for i in range(len(runes))]
            plain_text = indices_to_text(plain)
            
            # Score by common patterns
            score = 0
            for word in ENGLISH:
                score += plain_text.count(word) * len(word) * 10
            
            if score > best_score:
                best_score = score
                best_key = key
                best_plain = plain_text
    
    print(f"Best linear key (mult={mult}, offset={offset}):")
    print(f"  Key: {best_key[:15]}...")
    print(f"  Score: {best_score}")
    print(f"  Preview: {best_plain[:80]}")
    
    return best_score

def analyze_position_mod_11(runes):
    """Analyze patterns at position mod 11."""
    
    print("\nRune frequency by position mod 11:")
    print("-" * 50)
    
    for pos_mod in range(11):
        subset = [runes[i] for i in range(pos_mod, len(runes), 11)]
        freq = Counter(subset)
        top_3 = freq.most_common(3)
        top_str = ", ".join(f"{LETTERS[r]}({c})" for r, c in top_3)
        print(f"pos mod 11 = {pos_mod:2d}: n={len(subset):3d}, top: {top_str}")

def gap_11_stream_analysis(page_num):
    """Deep analysis of gap-11 pattern on a page."""
    
    print(f"\n{'='*70}")
    print(f"GAP-11 ANALYSIS: PAGE {page_num}")
    print("=" * 70)
    
    rune_text = load_runes(page_num)
    if not rune_text:
        print("Could not load page")
        return
    
    runes = parse_rune_stream(rune_text)
    print(f"Total runes: {len(runes)}")
    
    # Find best gap using IoC
    best_gap = analyze_gap_IoC(runes)
    
    # Detailed analysis at gap 11
    analyze_position_mod_11(runes)
    
    # Test decryption
    for gap in [11, best_gap]:
        test_gap_decryption(runes, gap)

def main():
    for page_num in [8, 43, 51]:
        gap_11_stream_analysis(page_num)

if __name__ == '__main__':
    main()

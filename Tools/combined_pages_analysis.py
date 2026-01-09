#!/usr/bin/env python3
"""
Combined Pages Analysis

Hypothesis: Pages 18-54 might be ONE continuous message that was split
across pages, and needs to be analyzed as a whole.

This script:
1. Combines all page 18-54 runes into one text
2. Performs columnar reading at various widths
3. Tries interleaved reading patterns
4. Tests for transposition patterns
"""

import os
from collections import Counter

# Gematria Primus mapping
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_CHARS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
            'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
            'A', 'AE', 'Y', 'IA', 'EA']

def runes_to_indices(rune_text):
    """Convert rune text to list of indices"""
    return [RUNE_TO_IDX[r] for r in rune_text if r in RUNE_TO_IDX]

def indices_to_runeglish(indices):
    """Convert indices to runeglish"""
    return ''.join(GP_CHARS[i] for i in indices)

def calculate_ioc(indices):
    """Calculate Index of Coincidence"""
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator > 0 else 0

# Collect all runes from pages 18-54
print("=" * 70)
print("COMBINED PAGES 18-54 ANALYSIS")
print("=" * 70)

all_runes = []
page_lengths = []
base_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"

for page_num in range(18, 55):
    page_path = os.path.join(base_path, f"page_{page_num:02d}", "runes.txt")
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        runes = [c for c in content if c in RUNE_TO_IDX]
        page_lengths.append((page_num, len(runes)))
        all_runes.extend(runes)

print(f"Total runes collected: {len(all_runes)}")
print(f"\nPage lengths:")
for page, length in page_lengths[:10]:
    print(f"  Page {page}: {length} runes")
print(f"  ...")

# Convert to indices
all_indices = runes_to_indices(''.join(all_runes))
print(f"\nTotal indices: {len(all_indices)}")

# Calculate IoC of combined text
ioc = calculate_ioc(all_indices)
print(f"Combined IoC: {ioc:.4f}")

# Frequency analysis
freq = Counter(all_indices)
print(f"\nTop 10 most frequent runes:")
for idx, count in freq.most_common(10):
    print(f"  {GP_CHARS[idx]:4s}: {count} ({100*count/len(all_indices):.1f}%)")

# Try columnar reading
print("\n" + "=" * 70)
print("COLUMNAR TRANSPOSITION ANALYSIS")
print("=" * 70)

def columnar_read(indices, num_cols):
    """Read indices column by column instead of row by row"""
    num_rows = (len(indices) + num_cols - 1) // num_cols
    grid = [[None] * num_cols for _ in range(num_rows)]
    
    # Fill grid row by row
    idx = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if idx < len(indices):
                grid[r][c] = indices[idx]
                idx += 1
    
    # Read column by column
    result = []
    for c in range(num_cols):
        for r in range(num_rows):
            if grid[r][c] is not None:
                result.append(grid[r][c])
    
    return result

# Test various column widths (prime numbers)
prime_widths = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

for width in prime_widths:
    reordered = columnar_read(all_indices, width)
    ioc_reordered = calculate_ioc(reordered)
    sample = indices_to_runeglish(reordered[:50])
    print(f"Width {width:2d}: IoC={ioc_reordered:.4f} - {sample}...")

# Try every Nth letter
print("\n" + "=" * 70)
print("EVERY NTH LETTER ANALYSIS")
print("=" * 70)

for n in [2, 3, 5, 7, 11, 13]:
    samples = []
    for start in range(n):
        nth_indices = all_indices[start::n]
        ioc_nth = calculate_ioc(nth_indices)
        sample = indices_to_runeglish(nth_indices[:30])
        samples.append((start, ioc_nth, sample))
    
    print(f"\nEvery {n}th letter:")
    for start, ioc_nth, sample in samples:
        print(f"  Start {start}: IoC={ioc_nth:.4f} - {sample}...")

# Try reading pages in different orders
print("\n" + "=" * 70)
print("INTERLEAVED PAGE READING")
print("=" * 70)

# Collect pages as separate lists
pages = {}
for page_num in range(18, 55):
    page_path = os.path.join(base_path, f"page_{page_num:02d}", "runes.txt")
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pages[page_num] = runes_to_indices(content)

# Try reading first letter from each page, then second, etc.
print("\nInterleaved reading (round-robin across pages):")
interleaved = []
max_len = max(len(pages[p]) for p in pages)
for pos in range(min(50, max_len)):
    for page_num in sorted(pages.keys()):
        if pos < len(pages[page_num]):
            interleaved.append(pages[page_num][pos])

ioc_interleaved = calculate_ioc(interleaved)
sample = indices_to_runeglish(interleaved[:100])
print(f"IoC: {ioc_interleaved:.4f}")
print(f"Sample: {sample}")

# Try reverse page order
print("\nReverse page order:")
reverse_all = []
for page_num in range(54, 17, -1):
    if page_num in pages:
        reverse_all.extend(pages[page_num])
sample = indices_to_runeglish(reverse_all[:100])
print(f"Sample: {sample}")

# Try reverse within each page
print("\nReversed within each page:")
reversed_within = []
for page_num in range(18, 55):
    if page_num in pages:
        reversed_within.extend(reversed(pages[page_num]))
sample = indices_to_runeglish(reversed_within[:100])
print(f"Sample: {sample}")

# Odd/even interleave
print("\nOdd pages then even pages:")
odd_even = []
for page_num in range(19, 55, 2):  # Odd
    if page_num in pages:
        odd_even.extend(pages[page_num])
for page_num in range(18, 55, 2):  # Even
    if page_num in pages:
        odd_even.extend(pages[page_num])
sample = indices_to_runeglish(odd_even[:100])
print(f"Sample: {sample}")

# Check if pages 18-54 length equals pages 55-74 total (for XOR operation)
total_18_54 = sum(len(pages[p]) for p in range(18, 55) if p in pages)
print(f"\nTotal length pages 18-54: {total_18_54}")

# Cross-check with other page ranges
pages_55_74 = {}
for page_num in range(55, 75):
    page_path = os.path.join(base_path, f"page_{page_num:02d}", "runes.txt")
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pages_55_74[page_num] = runes_to_indices(content)

total_55_74 = sum(len(pages_55_74.get(p, [])) for p in range(55, 75))
print(f"Total length pages 55-74: {total_55_74}")

# Maybe they're related?
if total_18_54 > 0 and total_55_74 > 0:
    ratio = total_18_54 / total_55_74
    print(f"Ratio 18-54/55-74: {ratio:.2f}")

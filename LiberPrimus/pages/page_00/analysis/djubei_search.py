#!/usr/bin/env python3
"""
Search for the DJUBEI pattern in the Liber Primus pages.
DJUBEI is reported to occur exactly twice in the unsolved corpus.
This is the longest repeated 6-gram and may be a crib point.

In Gematria Primus:
D = 23, J = 11, U (V) = 1, B = 17, E = 18, I = 10
Runic: ᛞᛄᚢᛒᛖᛁ
"""

import os

# Gematria Primus
RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'V', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 'ᚹ': 'W',
    'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 'ᛉ': 'X', 'ᛋ': 'S',
    'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D',
    'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LETTER = ['F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
                 'A', 'AE', 'Y', 'IA', 'EA']

# DJUBEI as indices
DJUBEI_PATTERN = [23, 11, 1, 17, 18, 10]  # D=23, J=11, V(U)=1, B=17, E=18, I=10
DJUBEI_RUNES = 'ᛞᛄᚢᛒᛖᛁ'

def parse_runes(filepath):
    """Extract rune indices from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    indices = []
    for char in content:
        if char in RUNE_TO_IDX:
            indices.append(RUNE_TO_IDX[char])
    return indices

def runes_to_text(filepath):
    """Convert runes to text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    text = []
    for char in content:
        if char in RUNE_TO_LETTER:
            text.append(RUNE_TO_LETTER[char])
    return ''.join(text)

def find_pattern(indices, pattern):
    """Find all occurrences of a pattern in indices."""
    matches = []
    for i in range(len(indices) - len(pattern) + 1):
        if indices[i:i+len(pattern)] == pattern:
            matches.append(i)
    return matches

def find_all_ngrams(indices, n=6):
    """Find all repeated n-grams."""
    ngram_positions = {}
    for i in range(len(indices) - n + 1):
        ngram = tuple(indices[i:i+n])
        if ngram not in ngram_positions:
            ngram_positions[ngram] = []
        ngram_positions[ngram].append(i)
    
    # Filter to only repeated ones
    repeated = {k: v for k, v in ngram_positions.items() if len(v) > 1}
    return repeated

def main():
    base_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    
    print("Searching for DJUBEI pattern in Liber Primus pages")
    print("=" * 60)
    print(f"DJUBEI indices: {DJUBEI_PATTERN}")
    print(f"DJUBEI runes: {DJUBEI_RUNES}")
    print()
    
    all_indices = []
    page_ranges = {}
    
    # Collect all pages
    for page_num in range(75):
        page_dir = f"page_{page_num:02d}"
        runes_file = os.path.join(base_path, page_dir, "runes.txt")
        
        if os.path.exists(runes_file):
            start_idx = len(all_indices)
            page_indices = parse_runes(runes_file)
            all_indices.extend(page_indices)
            page_ranges[page_num] = (start_idx, start_idx + len(page_indices))
    
    print(f"Total runes collected: {len(all_indices)}")
    print(f"Pages found: {len(page_ranges)}")
    print()
    
    # Search for DJUBEI
    print("Searching for DJUBEI pattern...")
    matches = find_pattern(all_indices, DJUBEI_PATTERN)
    
    if matches:
        print(f"Found {len(matches)} occurrences:")
        for pos in matches:
            # Find which page
            for page_num, (start, end) in page_ranges.items():
                if start <= pos < end:
                    local_pos = pos - start
                    print(f"  Position {pos} (Page {page_num}, local pos {local_pos})")
                    # Show context
                    context_start = max(0, pos - 3)
                    context_end = min(len(all_indices), pos + 9)
                    context = all_indices[context_start:context_end]
                    context_text = ''.join(IDX_TO_LETTER[i] for i in context)
                    print(f"    Context: ...{context_text}...")
                    break
    else:
        print("DJUBEI pattern not found in collected pages")
    
    # Find all repeated 6-grams in our pages 0-4
    print("\n" + "=" * 60)
    print("Repeated 6-grams in Pages 0-4:")
    print("=" * 60)
    
    pages_0_4_indices = []
    for page_num in range(5):
        if page_num in page_ranges:
            start, end = page_ranges[page_num]
            pages_0_4_indices.extend(all_indices[start:end])
    
    repeated_6grams = find_all_ngrams(pages_0_4_indices, 6)
    
    if repeated_6grams:
        print(f"Found {len(repeated_6grams)} repeated 6-grams:")
        for ngram, positions in sorted(repeated_6grams.items(), key=lambda x: -len(x[1])):
            text = ''.join(IDX_TO_LETTER[i] for i in ngram)
            print(f"  {text}: positions {positions}")
    else:
        print("No repeated 6-grams in pages 0-4")
    
    # Find all repeated 5-grams
    print("\nRepeated 5-grams in Pages 0-4:")
    repeated_5grams = find_all_ngrams(pages_0_4_indices, 5)
    if repeated_5grams:
        print(f"Found {len(repeated_5grams)} repeated 5-grams:")
        for ngram, positions in sorted(repeated_5grams.items(), key=lambda x: -len(x[1]))[:20]:
            text = ''.join(IDX_TO_LETTER[i] for i in ngram)
            print(f"  {text}: {len(positions)}x at {positions}")
    
    # Find all repeated 4-grams
    print("\nTop 20 repeated 4-grams in Pages 0-4:")
    repeated_4grams = find_all_ngrams(pages_0_4_indices, 4)
    if repeated_4grams:
        for ngram, positions in sorted(repeated_4grams.items(), key=lambda x: -len(x[1]))[:20]:
            text = ''.join(IDX_TO_LETTER[i] for i in ngram)
            print(f"  {text}: {len(positions)}x")

if __name__ == "__main__":
    main()

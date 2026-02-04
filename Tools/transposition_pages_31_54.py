"""
Apply Transposition to Caesar-Decrypted Pages 31-54
Focus on top candidates (Pages 32, 44, 50)
"""

import os
import sys
import math

# Gematria Primus mappings
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21,
    'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_INDEX_TO_LATIN = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N',
    'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
    'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

def load_and_decrypt_page(page_num, shift):
    """Load page and apply Caesar shift"""
    page_dir = f"LiberPrimus/pages/page_{page_num:02d}"
    rune_file = os.path.join(page_dir, "runes.txt")
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    # Extract runes and decrypt
    indices = []
    for char in text:
        if char in GP_RUNE_TO_INDEX:
            idx = GP_RUNE_TO_INDEX[char]
            decrypted = (idx - shift) % 29
            indices.append(decrypted)
    
    # Convert to text
    return ''.join(GP_INDEX_TO_LATIN[i] for i in indices)

def read_columnar(text, cols):
    """Read text in columnar transposition"""
    if len(text) < cols:
        return text
    
    rows = math.ceil(len(text) / cols)
    grid = []
    
    # Fill grid row by row
    idx = 0
    for r in range(rows):
        row = []
        for c in range(cols):
            if idx < len(text):
                row.append(text[idx])
                idx += 1
            else:
                row.append('')
        grid.append(row)
    
    # Read column by column
    result = []
    for c in range(cols):
        for r in range(rows):
            if grid[r][c]:
                result.append(grid[r][c])
    
    return ''.join(result)

def read_reverse_columnar(text, cols):
    """Read columnar transposition in reverse (decrypt)"""
    if len(text) < cols:
        return text
    
    n = len(text)
    rows = math.ceil(n / cols)
    
    # Calculate how many columns are "full"
    full_cols = n % cols if n % cols != 0 else cols
    
    # Read back from column-major order
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if c < full_cols or r < rows - 1:
                if idx < n:
                    grid[r][c] = text[idx]
                    idx += 1
    
    # Output row by row
    result = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c]:
                result.append(grid[r][c])
    
    return ''.join(result)

def read_diagonal(text, width):
    """Read diagonally"""
    rows = math.ceil(len(text) / width)
    grid = []
    
    # Fill grid
    idx = 0
    for r in range(rows):
        row = []
        for c in range(width):
            if idx < len(text):
                row.append(text[idx])
                idx += 1
            else:
                row.append('')
        grid.append(row)
    
    # Read diagonals
    result = []
    for start_col in range(width):
        r, c = 0, start_col
        while r < rows and c < width:
            if grid[r][c]:
                result.append(grid[r][c])
            r += 1
            c += 1
    
    for start_row in range(1, rows):
        r, c = start_row, 0
        while r < rows and c < width:
            if grid[r][c]:
                result.append(grid[r][c])
            r += 1
            c += 1
    
    return ''.join(result)

def read_every_nth(text, n):
    """Read every nth character"""
    results = []
    for start in range(n):
        result = text[start::n]
        results.append(result)
    return ''.join(results)

def score_english(text):
    """Score text for English readability"""
    text_upper = text.upper()
    
    # Common words
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE',
        'FROM', 'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN',
        'KNOW', 'TRUTH', 'WISDOM', 'PATH', 'PRIMES', 'SACRED', 'WARNING',
        'KOAN', 'SEEK', 'FIND', 'WAY', 'LIGHT', 'DARK', 'DEATH', 'LIFE'
    ]
    
    score = sum(text_upper.count(word) * 3 for word in common_words)
    
    # Common bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'EA', 'NG']
    score += sum(text_upper.count(bg) for bg in bigrams)
    
    # Common trigrams
    trigrams = ['THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE', 'FOR']
    score += sum(text_upper.count(tg) * 2 for tg in trigrams)
    
    return score

def analyze_page(page_num, caesar_shift):
    """Analyze one page with transpositions"""
    print(f"\n{'='*80}")
    print(f"PAGE {page_num} - Caesar Shift {caesar_shift}")
    print(f"{'='*80}\n")
    
    # Get Caesar-decrypted text
    text = load_and_decrypt_page(page_num, caesar_shift)
    print(f"Length: {len(text)} characters")
    print(f"Original: {text[:100]}...")
    print()
    
    results = []
    
    # Test various transposition widths (focus on primes)
    test_widths = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    for width in test_widths:
        if width > len(text):
            continue
        
        # Reverse columnar (decrypt columnar transposition)
        decoded = read_reverse_columnar(text, width)
        score = score_english(decoded)
        if score > 50:
            results.append(('REV_COLUMNAR', width, score, decoded))
        
        # Regular columnar (just in case)
        decoded = read_columnar(text, width)
        score = score_english(decoded)
        if score > 50:
            results.append(('COLUMNAR', width, score, decoded))
        
        # Diagonal
        decoded = read_diagonal(text, width)
        score = score_english(decoded)
        if score > 50:
            results.append(('DIAGONAL', width, score, decoded))
    
    # Every nth character
    for n in [2, 3, 5, 7, 11]:
        if n < len(text):
            decoded = read_every_nth(text, n)
            score = score_english(decoded)
            if score > 50:
                results.append(('EVERY_NTH', n, score, decoded))
    
    # Sort by score
    results.sort(key=lambda x: x[2], reverse=True)
    
    if results:
        print("TOP 10 TRANSPOSITION RESULTS:\n")
        for i, (method, param, score, text) in enumerate(results[:10], 1):
            print(f"{i}. {method}_{param:<3} Score: {score:>5.1f}")
            print(f"   {text[:100]}")
            print()
        
        # Save best result
        best = results[0]
        filename = f"page_{page_num:02d}_transposition_best.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"PAGE {page_num} - BEST TRANSPOSITION RESULT\n")
            f.write(f"Method: {best[0]}_{best[1]}\n")
            f.write(f"Caesar Shift: {caesar_shift}\n")
            f.write(f"Score: {best[2]:.1f}\n")
            f.write("=" * 80 + "\n\n")
            f.write(best[3])
        
        print(f"✅ Saved: {filename}\n")
        return best
    else:
        print("❌ No high-scoring transposition found\n")
        return None

def main():
    # Top candidates from simple cipher test
    candidates = [
        (32, 11),   # Score 285
        (44, 5),    # Score 227
        (50, 6),    # Score 224
        (40, 0),    # Score 163
        (43, 23),   # Score 64
    ]
    
    print("=" * 80)
    print("TRANSPOSITION ANALYSIS - TOP PAGES")
    print("=" * 80)
    
    all_results = []
    
    for page_num, shift in candidates:
        result = analyze_page(page_num, shift)
        if result:
            all_results.append((page_num, shift, result))
    
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80 + "\n")
    
    if all_results:
        for page_num, shift, (method, param, score, text) in all_results:
            print(f"Page {page_num} (Caesar {shift}): {method}_{param} → Score {score:.1f}")
            print(f"  {text[:80]}")
            print()
    else:
        print("No successful transpositions found.")
        print("Pages 31-54 may require:")
        print("  - More complex transposition methods")
        print("  - Running key cipher after Caesar")
        print("  - Page-dependent transformation")

if __name__ == "__main__":
    main()

"""
Transposition Analysis for High-IoC Decrypted Text
Applies multiple reading methods to extract plaintext
"""

import math

def read_zigzag(text, rows):
    """Read text in zigzag pattern (rail fence)"""
    if rows <= 1:
        return text
    
    # Calculate rail fence decoding
    n = len(text)
    cycle = 2 * rows - 2
    result = []
    
    for row in range(rows):
        pos = row
        if row == 0 or row == rows - 1:
            # Top and bottom rails
            while pos < n:
                result.append((pos, text[pos]))
                pos += cycle
        else:
            # Middle rails
            while pos < n:
                result.append((pos, text[pos]))
                pos += cycle
                if pos < n:
                    result.append((pos, text[pos]))
                pos += cycle - 2 * row
    
    # Sort by original position and extract text
    result.sort(key=lambda x: x[0])
    return ''.join([char for _, char in result])

def read_columnar(text, cols):
    """Read text column by column"""
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

def read_diagonal(text, width):
    """Read text diagonally"""
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
    
    # Read diagonals (top-left to bottom-right)
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

def read_reverse_every_other(text, width):
    """Read rows alternating direction (boustrophedon)"""
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
    
    # Read with alternating direction
    result = []
    for r in range(rows):
        if r % 2 == 0:
            # Left to right
            result.extend([c for c in grid[r] if c])
        else:
            # Right to left
            result.extend([c for c in reversed(grid[r]) if c])
    
    return ''.join(result)

def calculate_ioc(text):
    """Calculate Index of Coincidence"""
    text = text.upper()
    freq = {}
    n = 0
    
    for char in text:
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
            n += 1
    
    if n <= 1:
        return 0
    
    ioc = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ioc * 26  # Normalized

def score_english(text):
    """Score text for English-like properties"""
    text = text.upper()
    
    # Common English bigrams
    common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
    bigram_score = sum(text.count(bg) for bg in common_bigrams)
    
    # Common trigrams
    common_trigrams = ['THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE', 'FOR', 'ENT']
    trigram_score = sum(text.count(tg) for tg in common_trigrams) * 2
    
    # Common words
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT']
    word_score = sum((' ' + text + ' ').count(' ' + word + ' ') for word in common_words) * 5
    
    return bigram_score + trigram_score + word_score

def analyze_text(text, label):
    """Analyze transposition result"""
    ioc = calculate_ioc(text)
    score = score_english(text)
    
    # Extract first 100 chars for preview
    preview = text[:100] if len(text) <= 100 else text[:100] + '...'
    
    return {
        'label': label,
        'ioc': ioc,
        'score': score,
        'preview': preview,
        'text': text
    }

def main():
    # Read the decrypted text
    input_file = "p20_non_prime_shift16_result.txt"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    print(f"Analyzing: {input_file}")
    print(f"Length: {len(text)} characters")
    print("=" * 80)
    
    results = []
    
    # Original
    results.append(analyze_text(text, "ORIGINAL"))
    
    # Zigzag (rail fence) with different heights
    for height in [2, 3, 4, 5, 7, 11]:
        decoded = read_zigzag(text, height)
        results.append(analyze_text(decoded, f"ZIGZAG_{height}_rails"))
    
    # Columnar with different widths
    factors = []
    n = len(text)
    for i in range(2, min(50, n)):
        if n % i == 0 or abs(n - i * (n // i)) <= 5:
            factors.append(i)
    
    # Test common grid dimensions
    test_widths = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]  # Primes
    for width in test_widths:
        if width < len(text):
            decoded = read_columnar(text, width)
            results.append(analyze_text(decoded, f"COLUMNAR_{width}_cols"))
    
    # Diagonal reading
    for width in [11, 13, 17, 19, 23]:
        if width < len(text):
            decoded = read_diagonal(text, width)
            results.append(analyze_text(decoded, f"DIAGONAL_{width}_width"))
    
    # Reverse every other row
    for width in [11, 13, 17, 19, 23]:
        if width < len(text):
            decoded = read_reverse_every_other(text, width)
            results.append(analyze_text(decoded, f"BOUSTROPHEDON_{width}_width"))
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\nTOP 20 RESULTS (by English score):\n")
    for i, result in enumerate(results[:20], 1):
        print(f"{i}. {result['label']:<30} IoC: {result['ioc']:.4f}  Score: {result['score']:>4}")
        print(f"   {result['preview']}")
        print()
    
    # Save best results
    print("\nSaving top 5 results...")
    for i, result in enumerate(results[:5], 1):
        filename = f"p20_transposition_{result['label'].lower()}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{result['label']}\n")
            f.write(f"IoC: {result['ioc']:.4f}, Score: {result['score']}\n")
            f.write("=" * 80 + "\n\n")
            f.write(result['text'])
        print(f"   Saved: {filename}")

if __name__ == "__main__":
    main()

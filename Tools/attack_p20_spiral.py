"""
Page 20 - Spiral and Snake Path Attack
======================================
Try different reading paths through the grid.
"""

import collections

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def load_deor():
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    with open(deor_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return ''.join(c for c in text.upper() if c.isalpha())

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def decrypt_vigenere(cipher, key, mode='sub'):
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        else:
            result.append((c + k) % 29)
    return result

def spiral_path(rows, cols):
    """Generate spiral reading order (clockwise from top-left)."""
    path = []
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    
    while top <= bottom and left <= right:
        # Right
        for c in range(left, right + 1):
            path.append((top, c))
        top += 1
        
        # Down
        for r in range(top, bottom + 1):
            path.append((r, right))
        right -= 1
        
        # Left
        if top <= bottom:
            for c in range(right, left - 1, -1):
                path.append((bottom, c))
            bottom -= 1
        
        # Up
        if left <= right:
            for r in range(bottom, top - 1, -1):
                path.append((r, left))
            left += 1
    
    return path

def snake_path(rows, cols):
    """Generate snake/boustrophedon reading order."""
    path = []
    for r in range(rows):
        if r % 2 == 0:
            for c in range(cols):
                path.append((r, c))
        else:
            for c in range(cols - 1, -1, -1):
                path.append((r, c))
    return path

def diagonal_path(rows, cols):
    """Generate diagonal reading order."""
    path = []
    for diag in range(rows + cols - 1):
        if diag % 2 == 0:
            # Up-right
            r = min(diag, rows - 1)
            c = diag - r
            while r >= 0 and c < cols:
                path.append((r, c))
                r -= 1
                c += 1
        else:
            # Down-left
            c = min(diag, cols - 1)
            r = diag - c
            while c >= 0 and r < rows:
                path.append((r, c))
                r += 1
                c -= 1
    return path

def column_major_path(rows, cols):
    """Read column by column."""
    path = []
    for c in range(cols):
        for r in range(rows):
            path.append((r, c))
    return path

def main():
    print("="*60)
    print("PAGE 20 - SPIRAL AND SNAKE PATH ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    deor = load_deor()
    rows, cols = 28, 29
    grid = [[runes[r*cols + c] for c in range(cols)] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    # Extended Deor key
    deor_key = [ENGLISH_TO_IDX.get(c, 0) for c in deor]
    extended_deor = deor_key * (len(runes) // len(deor_key) + 1)
    extended_deor = extended_deor[:len(runes)]
    
    paths = {
        "Row-major (normal)": [(r, c) for r in range(rows) for c in range(cols)],
        "Column-major": column_major_path(rows, cols),
        "Snake": snake_path(rows, cols),
        "Spiral": spiral_path(rows, cols),
        "Diagonal": diagonal_path(rows, cols),
    }
    
    print("\n--- Testing Different Reading Paths ---")
    
    best_ioc = 0
    best_config = None
    
    for path_name, path in paths.items():
        # Read grid in this order
        path_runes = [grid[r][c] for r, c in path]
        
        # Raw IoC
        ioc = calculate_ioc(path_runes)
        print(f"\n{path_name}: Raw IoC={ioc:.4f}")
        
        # With Deor SUB
        result = decrypt_vigenere(path_runes, extended_deor, 'sub')
        ioc = calculate_ioc(result)
        print(f"  + Deor SUB: IoC={ioc:.4f}")
        if ioc > best_ioc:
            best_ioc = ioc
            best_config = (path_name, "Deor SUB", result)
        
        # With Deor ADD
        result = decrypt_vigenere(path_runes, extended_deor, 'add')
        ioc = calculate_ioc(result)
        print(f"  + Deor ADD: IoC={ioc:.4f}")
        if ioc > best_ioc:
            best_ioc = ioc
            best_config = (path_name, "Deor ADD", result)
    
    print("\n" + "="*60)
    print(f"BEST RESULT: {best_config[0]} + {best_config[1]}")
    print(f"IoC: {best_ioc:.4f}")
    print(f"Text: {runes_to_latin(best_config[2][:150])}")
    
    # Now try: Read path, then apply Deor in reverse order
    print("\n" + "="*60)
    print("REVERSE DEOR")
    print("="*60)
    
    reversed_deor = deor_key[::-1]
    extended_rev = reversed_deor * (len(runes) // len(reversed_deor) + 1)
    extended_rev = extended_rev[:len(runes)]
    
    for path_name, path in paths.items():
        path_runes = [grid[r][c] for r, c in path]
        
        result = decrypt_vigenere(path_runes, extended_rev, 'sub')
        ioc = calculate_ioc(result)
        if ioc > 1.1:
            print(f"{path_name} + Reversed Deor: IoC={ioc:.4f}")
            print(f"  Text: {runes_to_latin(result[:80])}")

if __name__ == "__main__":
    main()

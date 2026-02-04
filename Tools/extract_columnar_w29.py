"""
Extract full columnar width-29 result
"""

import os
import math

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

def load_caesar_11_text():
    """Load Page 32 after Caesar 11"""
    page_dir = "LiberPrimus/pages/page_32"
    rune_file = os.path.join(page_dir, "runes.txt")
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    indices = []
    for char in text:
        if char in GP_RUNE_TO_INDEX:
            indices.append(GP_RUNE_TO_INDEX[char])
    
    # Caesar 11
    caesar = [(i - 11) % 29 for i in indices]
    
    # Convert to text
    result = []
    for idx in caesar:
        result.append(GP_INDEX_TO_LATIN[idx])
    
    return ''.join(result)

def organize_columnar(text, cols):
    """Organize text in columnar format (row-major)"""
    rows = math.ceil(len(text) / cols)
    grid = []
    
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
    
    return grid

def read_columns(grid):
    """Read column by column"""
    text = []
    cols = len(grid[0]) if grid else 0
    rows = len(grid)
    
    for c in range(cols):
        for r in range(rows):
            if grid[r][c]:
                text.append(grid[r][c])
    
    return ''.join(text)

def main():
    text = load_caesar_11_text()
    print(f"Loaded Caesar-11 text: {len(text)} elements")
    print()
    
    # Extract with width 29
    grid = organize_columnar(text, 29)
    extracted = read_columns(grid)
    
    print("Width 29 Columnar Extraction:")
    print("=" * 80)
    print(extracted)
    print()
    print(f"Length: {len(extracted)}")
    
    # Save to file
    with open('page_32_columnar_w29.txt', 'w') as f:
        f.write(extracted)
    
    print("\nSaved to page_32_columnar_w29.txt")

if __name__ == "__main__":
    main()

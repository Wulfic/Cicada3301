"""
Columnar Analysis - Page 32
Try organizing text in columns and reading different ways
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

WORD_DICT = set([
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
    'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM',
    'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN', 'HIM', 'HIS',
    'HOW', 'WHO', 'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'TWO', 'WAY', 'WHY',
    'TRY', 'ASK', 'END', 'EVEN', 'FIND', 'FIRST', 'GET', 'GIVE', 'GOOD',
    'HAND', 'HELP', 'HERE', 'HIGH', 'JUST', 'KEEP', 'KNOW', 'LAST', 'LIFE',
    'LIKE', 'LONG', 'LOOK', 'MAKE', 'MAN', 'MAY', 'MORE', 'MOST', 'MUST',
    'NAME', 'NEED', 'NEVER', 'NEW', 'NEXT', 'NO', 'NOW', 'OF', 'OLD', 'ON',
    'ONLY', 'OR', 'OTHER', 'OVER', 'OWN', 'PART', 'PATH', 'PEOPLE', 'PLACE',
    'RIGHT', 'SAME', 'SEE', 'SEEM', 'SHOULD', 'SHOW', 'SIDE', 'SOME', 'SUCH',
    'TAKE', 'TELL', 'THAN', 'THEM', 'THEN', 'THESE', 'THING', 'THINK', 'THIS',
    'THOSE', 'TIME', 'TO', 'TOO', 'TOOK', 'TOP', 'TOWN', 'TURN', 'TWO',
    'UNDER', 'UP', 'US', 'VERY', 'WAY', 'WEEK', 'WERE', 'WHICH', 'WHILE',
    'WILL', 'WITH', 'WORD', 'WORK', 'WORLD', 'YEAR', 'YES', 'YOU', 'YOUR',
])

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
    """Organize text in columnar format"""
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

def read_diagonals(grid):
    """Read diagonally"""
    text = []
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    
    # Main diagonals
    for start_col in range(cols):
        r, c = 0, start_col
        while r < rows and c < cols:
            if grid[r][c]:
                text.append(grid[r][c])
            r += 1
            c += 1
    
    for start_row in range(1, rows):
        r, c = start_row, 0
        while r < rows and c < cols:
            if grid[r][c]:
                text.append(grid[r][c])
            r += 1
            c += 1
    
    return ''.join(text)

def score_english(text):
    """Count English words in text"""
    count = 0
    i = 0
    while i < len(text) - 2:
        for length in range(4, 1, -1):
            if i + length <= len(text):
                word = text[i:i+length].upper()
                if word in WORD_DICT:
                    count += 1
                    i += length
                    break
        else:
            i += 1
    
    return count

def main():
    print("=" * 80)
    print("COLUMNAR ANALYSIS - PAGE 32")
    print("=" * 80)
    print()
    
    text = load_caesar_11_text()
    print(f"Text length: {len(text)}")
    print()
    
    # Test with prime number widths and other strategic widths
    test_widths = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                   2, 3, 5, 7, 42, 50, 48, 56, 64, 84]
    
    results = []
    
    print("Testing columnar layouts...\n")
    
    for width in test_widths:
        if width > len(text) / 2:
            continue
        
        grid = organize_columnar(text, width)
        
        # Try different reading methods
        for method_name, method_func in [('columns', read_columns), ('diagonals', read_diagonals)]:
            try:
                extracted = method_func(grid)
                score = score_english(extracted)
                
                if score >= 10:  # Only report good results
                    results.append({
                        'width': width,
                        'method': method_name,
                        'score': score,
                        'text': extracted[:150]
                    })
            except:
                pass
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("Top 10 Columnar Results:\n")
    print(f"{'Width':<8} {'Method':<12} {'Score':<8} {'Preview'}")
    print("-" * 80)
    
    for r in results[:10]:
        print(f"{r['width']:<8} {r['method']:<12} {r['score']:<8} {r['text'][:50]}")
    
    if results:
        print()
        print("=" * 80)
        print("BEST RESULT")
        print("=" * 80)
        print()
        
        best = results[0]
        print(f"Width: {best['width']}, Method: {best['method']}, Score: {best['score']}")
        print()
        print(best['text'][:500])

if __name__ == "__main__":
    main()

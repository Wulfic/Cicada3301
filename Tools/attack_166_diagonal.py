"""
Test diagonal reading on 166-stream based on "DIAG" hint from PAIR-SUM result
"""

from collections import Counter
import math

STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

GP_MAP = {'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9, 
          'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
          'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28}

single_gp = {k: v for k, v in GP_MAP.items() if len(k) == 1}
INV_MAP = {v: k for k, v in GP_MAP.items()}

def to_indices(text):
    return [single_gp[c] for c in text if c in single_gp]

def to_text(indices):
    return "".join(INV_MAP[i % 29] for i in indices)

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def diagonal_read(text, width, step=1, top_to_bottom=True):
    """Read text arranged in grid diagonally"""
    n = len(text)
    if width <= 0 or n % width != 0:
        return None
    height = n // width
    
    result = []
    
    if top_to_bottom:
        # Start from each column, move down-right (with wrap)
        for start_col in range(width):
            col = start_col
            for row in range(height):
                idx = row * width + (col % width)
                if idx < n:
                    result.append(text[idx])
                col += step
    else:
        # Start from each column, move up-right
        for start_col in range(width):
            col = start_col
            for row in range(height - 1, -1, -1):
                idx = row * width + (col % width)
                if idx < n:
                    result.append(text[idx])
                col += step
    
    return "".join(result)

def diagonal_read_offset(text, width, offset):
    """Diagonal with offset between rows"""
    n = len(text)
    if width <= 0 or n % width != 0:
        return None
    height = n // width
    
    result = []
    
    # For each diagonal
    for d in range(width + height - 1):
        if d < width:
            start_row = 0
            start_col = d
        else:
            start_row = d - width + 1
            start_col = width - 1
        
        row, col = start_row, start_col
        while row < height and col >= 0:
            idx = row * width + col
            result.append(text[idx])
            row += 1
            col -= 1
    
    return "".join(result)

def anti_diagonal_read(text, width):
    """Read anti-diagonals (top-right to bottom-left)"""
    n = len(text)
    if width <= 0 or n % width != 0:
        return None
    height = n // width
    
    result = []
    
    for d in range(width + height - 1):
        if d < width:
            start_row = 0
            start_col = d
        else:
            start_row = d - width + 1
            start_col = width - 1
        
        row, col = start_row, start_col
        while row < height and col >= 0:
            idx = row * width + col
            result.append(text[idx])
            row += 1
            col -= 1
    
    return "".join(result)

def main_diagonal_read(text, width):
    """Read main diagonals (top-left to bottom-right)"""
    n = len(text)
    if width <= 0 or n % width != 0:
        return None
    height = n // width
    
    result = []
    
    # Diagonals starting from first column
    for start_row in range(height - 1, -1, -1):
        row, col = start_row, 0
        while row < height and col < width:
            idx = row * width + col
            result.append(text[idx])
            row += 1
            col += 1
    
    # Diagonals starting from first row (except col 0)
    for start_col in range(1, width):
        row, col = 0, start_col
        while row < height and col < width:
            idx = row * width + col
            result.append(text[idx])
            row += 1
            col += 1
    
    return "".join(result)

print("="*70)
print("DIAGONAL READING OF 166-STREAM")
print("="*70)

n = len(STREAM_166)
print(f"Stream: {STREAM_166[:50]}...")
print(f"Length: {n}")

# Find valid grid dimensions
print("\n--- Valid grid dimensions for 166 ---")
for i in range(2, n+1):
    if n % i == 0:
        print(f"  {i} x {n//i}")

print("\n" + "="*70)
print("TESTING GRIDS WITH DIAGONAL READS")
print("="*70)

results = []

# Test all valid dimensions
for width in [2, 83, 166]:
    if n % width != 0:
        continue
    height = n // width
    
    print(f"\n--- Grid {height}x{width} ---")
    
    # Main diagonal
    text_diag = main_diagonal_read(STREAM_166, width)
    if text_diag:
        indices = to_indices(text_diag)
        ioc = calc_ioc(indices)
        print(f"Main diagonal: IoC={ioc:.4f}")
        print(f"  '{text_diag[:60]}...'")
        results.append(('main_diag', width, ioc, text_diag))
    
    # Anti-diagonal
    text_anti = anti_diagonal_read(STREAM_166, width)
    if text_anti:
        indices = to_indices(text_anti)
        ioc = calc_ioc(indices)
        print(f"Anti-diagonal: IoC={ioc:.4f}")
        print(f"  '{text_anti[:60]}...'")
        results.append(('anti_diag', width, ioc, text_anti))
    
    # Step diagonals
    for step in [1, 2, 3, 5, 7, 11]:
        for direction in [True, False]:
            text_step = diagonal_read(STREAM_166, width, step, direction)
            if text_step:
                indices = to_indices(text_step)
                ioc = calc_ioc(indices)
                dir_name = "down" if direction else "up"
                if ioc > 1.0:  # Only show promising
                    print(f"Step {step} ({dir_name}): IoC={ioc:.4f}")
                    print(f"  '{text_step[:60]}...'")
                results.append((f'step_{step}_{dir_name}', width, ioc, text_step))

# Also try the interleaved version
print("\n" + "="*70)
print("DIAGONAL ON INTERLEAVED VERSION")
print("="*70)

first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))
print(f"Interleaved: {INTERLEAVED[:50]}...")

# 83 is prime, can't make a clean grid
# But try 166 as 2x83 arrangement
for width in [2, 83]:
    height = 166 // width
    print(f"\n--- Interleaved Grid {height}x{width} ---")
    
    text_diag = main_diagonal_read(INTERLEAVED, width)
    if text_diag:
        indices = to_indices(text_diag)
        ioc = calc_ioc(indices)
        print(f"Main diagonal: IoC={ioc:.4f}")
        print(f"  '{text_diag[:60]}...'")

# What about non-rectangular arrangements?
print("\n" + "="*70)
print("SNAKE/BOUSTROPHEDON DIAGONAL")
print("="*70)

# Reverse every other row before diagonal read
for width in [2, 83]:
    height = 166 // width
    snake = []
    for row in range(height):
        row_chars = STREAM_166[row*width:(row+1)*width]
        if row % 2 == 1:
            row_chars = row_chars[::-1]
        snake.extend(list(row_chars))
    snake_text = "".join(snake)
    
    text_diag = main_diagonal_read(snake_text, width)
    if text_diag:
        indices = to_indices(text_diag)
        ioc = calc_ioc(indices)
        print(f"Snake {height}x{width} main diag: IoC={ioc:.4f}")
        print(f"  '{text_diag[:60]}...'")

# Sort and show best results
print("\n" + "="*70)
print("BEST RESULTS (IoC > 1.0)")
print("="*70)

results.sort(key=lambda x: x[2], reverse=True)
for method, width, ioc, text in results[:10]:
    if ioc > 1.0:
        print(f"{method} (w={width}): IoC={ioc:.4f}")
        print(f"  Words found: ", end="")
        for word in ['THE', 'LONE', 'HER', 'SELF', 'ALT', 'DEAD', 'REAPER', 'AEON', 'MEAN', 'DIAG']:
            if word in text:
                print(word, end=" ")
        print()


import os
from collections import Counter

GRID_DATA = """
2M 0w 3L 3D 2r 0S 1p 15
3V 3e 3I 0n 3u 1O 0u 0Z
3g 2U 1C 0Y 1N 3n 0W 3Q
22 13 0V 3c 0E 34 0W 1t
1D 2N 3H 47 0s 2p 0Z 34
0g 3v 1Q 0s 0D 0K 2h 3D
3L 2x 1Q 20 2n 2L 1C 2p
0A 29 3r 0D 45 0k 2e 2W
25 3U 1W 2r 46 2s 2X 39
3p 0X 0E 1q 0q 4B 49 48
3r 3b 3C 1M 1j 0I 4A 48
40 3m 4E 0s 2S 1v 3T 0I
3t 2B 2k 2t 2O 0e 2I 1L
"""
# Note: Copied from file content manually for simplicity.

def analyze_grid():
    rows = GRID_DATA.strip().split('\n')
    cells = []
    
    for r in rows:
        parts = r.strip().split()
        if not parts: continue
        cells.extend(parts)
        
    print(f"Total Cells: {len(cells)}")
    print(f"Dimensions: {len(rows)} rows x {len(rows[0].split())} cols")
    
    # Analyze constituents
    first_chars = [c[0] for c in cells]
    second_chars = [c[1] for c in cells]
    
    print("\nFreq Char 1 (High Order?):")
    print(Counter(first_chars))
    
    print("\nFreq Char 2 (Low Order?):")
    print(Counter(second_chars).most_common(20))
    
    # Check bounds
    print(f"Range Char 1: {min(first_chars)} - {max(first_chars)}")
    print(f"Range Char 2: {min(second_chars)} - {max(second_chars)}")

    # Gematria Primus has 29 Runes.
    # Maybe these are base-N values representing Runes?
    # Max rune index is 28.
    # If these are Base 29?
    # 2M? 
    
    # What if they correspond to the Matrix/Grid on Page 0?
    
if __name__ == "__main__":
    analyze_grid()

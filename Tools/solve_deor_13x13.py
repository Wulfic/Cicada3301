
import sys
import os

RUNE_MAP_INV = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X',
    15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG',
    22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# The stream found
STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

def print_grid(grid, label):
    print(f"\n--- {label} ---")
    for row in grid:
        print(" ".join([f"{c:3}" for c in row]))
        
def solve():
    print(f"Stream Length: {len(STREAM)}")
    
    # 1. 13x13 Grid (169 cells). Need 3 nulls.
    # Try padding at END
    padded_end = STREAM + "XXX"
    
    # Grid 13x13 Row Major
    grid_rows = []
    for i in range(0, 169, 13):
        grid_rows.append(list(padded_end[i:i+13]))
        
    print_grid(grid_rows, "13x13 Row Major (Pad End)")
    
    # Check Columns for words
    cols = []
    for c in range(13):
        col_str = "".join([grid_rows[r][c] for r in range(13)])
        cols.append(col_str)
    
    print("\nColumns (Top-Down):")
    for i, c in enumerate(cols):
        print(f"Col {i}: {c}")

    # Spiral In
    # ... Implementation of Spiral Matrix ...
    
    # Reverse Stream
    rev_stream = STREAM[::-1]
    
    # Try 13x13 with Reverse
    
    # 2. 11x15 = 165 (+1 extra?). No.
    # 3. 2x83 (Two lines).
    
    # Analyze Words in Text Directly
    print("\n--- Direct Text Word Analysis ---")
    # Simple dictionary check
    common = ["THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "ANY", "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "MAN", "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO", "BOY", "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE", "DEATH", "LIFE", "KEEP", "FIND", "PATH", "SHOW", "KNOW", "WILL", "PRIMES", "NUMBERS", "ORDER", "INSTAR", "CICADA", "EMERGE"]
    
    # Check regular
    found = [w for w in common if w in STREAM]
    print(f"Forward words: {found}")
    
    # Check reverse
    found_rev = [w for w in common if w in rev_stream]
    print(f"Reverse words: {found_rev}")
    

if __name__ == "__main__":
    solve()

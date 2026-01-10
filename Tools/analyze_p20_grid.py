import sys

# Extracted Stream (Shift+5 verified)
STREAM = "YEOTJEOBJSGOXAEOUIWEEOHSHCHELTFFXENGMHETHEAAEWTHFJIAHEAJYFCN"
# Atbash version
ATBASH = "THTEOBTJBPOEAEXOAEIAENGITLPLDLIHEOEAEAXIWNLIYFONGYEABULFBTHEADM"

def get_gp_map():
    return {
        'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
        'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
        'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }

def get_inv_map():
    return {v: k for k, v in get_gp_map().items()}

def to_int(text):
    gem = get_gp_map()
    res = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text) and text[i:i+2] in gem:
            res.append(gem[text[i:i+2]])
            i += 2
        elif text[i] in gem:
            res.append(gem[text[i]])
            i += 1
        else:
            i += 1
    return res

def to_str(nums):
    inv = get_inv_map()
    return "".join([inv.get(n, "?") for n in nums])

def print_grid(nums, size=7):
    # Ensure length matches size^2
    total = size * size
    if len(nums) != total:
        print(f"Warning: Num runes {len(nums)} != {size}x{size} ({total})")
    
    # Create grid
    grid = []
    for r in range(size):
        row = nums[r*size : (r+1)*size]
        grid.append(row)
    
    # Print Rows
    print(f"\n--- {size}x{size} Grid (Rows) ---")
    for row in grid:
        print(" ".join([f"{to_str([x]):<3}" for x in row]))
        
    # Print Columns (Transposed)
    print(f"\n--- {size}x{size} Grid (Columns Readout) ---")
    cols = []
    for c in range(size):
        col_str = []
        for r in range(size):
            col_str.append(grid[r][c])
        cols.extend(col_str)
    print(to_str(cols))
    
    # Print Diagonal 1
    print(f"\n--- Diagonals ---")
    diag1 = [grid[i][i] for i in range(size)]
    print(f"Diag 1: {to_str(diag1)}")
    
    diag2 = [grid[i][size-1-i] for i in range(size)]
    print(f"Diag 2: {to_str(diag2)}")

def main():
    print("Analyzing 7x7 Grid of P20 Stream")
    
    s_nums = to_int(STREAM)
    print(f"\nORIGINAL Stream (Len {len(s_nums)}):")
    print_grid(s_nums, 7)
    
    a_nums = to_int(ATBASH)
    print(f"\nATBASH Stream (Len {len(a_nums)}):")
    print_grid(a_nums, 7)

if __name__ == "__main__":
    main()

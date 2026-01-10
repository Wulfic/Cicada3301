"""
Page 20 - Verify Grid Reading
==============================
Let's correctly understand what transposition produces "THE LONE"
"""

# The 166-stream 
STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

print(f"Original ({len(STREAM)} chars):")
print(STREAM)
print()

# Try all grid sizes that work
print("=== ALL VALID GRID TRANSPOSITIONS ===\n")

def col_read_grid(text, rows, cols):
    """Read text as if written in rows but read by columns"""
    # Fill row by row
    grid = []
    for r in range(rows):
        start = r * cols
        end = start + cols
        grid.append(text[start:end] if start < len(text) else "")
    
    # Read column by column
    result = ""
    for c in range(cols):
        for r in range(rows):
            if c < len(grid[r]):
                result += grid[r][c]
    return result

# Find the grid that produces "THE LONE"
for rows in [2, 83, 166]:
    for cols in [166, 83, 2]:
        if rows * cols == 166:
            result = col_read_grid(STREAM, rows, cols)
            if 'THELONE' in result or 'THE LONE' in result.replace('', ' '):
                print(f"Grid {rows}x{cols}:")
                print(f"  {result[:80]}...")
                if 'THELONE' in result:
                    idx = result.find('THELONE')
                    print(f"  THE LONE at position {idx}")

print()

# The known working result from previous script:
KNOWN_GOOD = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"

print(f"Known good result ({len(KNOWN_GOOD)} chars):")
print(KNOWN_GOOD)
print()

# Figure out the mapping
print("=== REVERSE ENGINEERING THE TRANSPOSITION ===")
print()

# For each position in known_good, find where it came from in original
mapping = []
for i, char in enumerate(KNOWN_GOOD[:20]):
    # Find all occurrences of this char in original
    positions = [j for j, c in enumerate(STREAM) if c == char]
    print(f"Pos {i:2d}: '{char}' <- original positions: {positions[:5]}...")
    if positions:
        mapping.append(positions[0])  # Take first occurrence

print()
print(f"First 20 positions map: {mapping}")

# Check if it's a simple pattern
print()
print("=== CHECKING PATTERN ===")

# Let's verify manually:
# Grid 2x83: text written in 2 rows of 83 chars, read by columns
# Row 0 = positions 0-82
# Row 1 = positions 83-165

# Column read: pos 0, 83, 1, 84, 2, 85, ...
row_0 = STREAM[0:83]
row_1 = STREAM[83:166]

print(f"Row 0: {row_0[:40]}...")
print(f"Row 1: {row_1[:40]}...")

# Interleave
interleaved = ""
for i in range(83):
    interleaved += row_0[i]
    if i < len(row_1):
        interleaved += row_1[i]

print(f"\nInterleaved: {interleaved[:80]}...")
print(f"Known good:  {KNOWN_GOOD[:80]}...")
print(f"Match: {interleaved == KNOWN_GOOD}")

# Maybe it's column-interleaved the other way?
col_interleaved = ""
for i in range(83):
    col_interleaved += row_0[i]
col_interleaved += row_1

print(f"\nConcat (0 then 1): {col_interleaved[:80]}...")

# Or maybe it's reading down column 0, then column 1
# Where the grid is 83 rows x 2 cols
grid83x2 = []
for r in range(83):
    start = r * 2
    grid83x2.append(STREAM[start:start+2])

col0 = "".join(row[0] for row in grid83x2 if len(row) > 0)
col1 = "".join(row[1] for row in grid83x2 if len(row) > 1)

print(f"\n83x2 grid, col 0: {col0[:40]}...")
print(f"83x2 grid, col 1: {col1[:40]}...")
print(f"Col0 + Col1: {(col0+col1)[:80]}...")

# Check if this is the answer
result_83x2 = col0 + col1
print(f"\nMatch with known: {result_83x2 == KNOWN_GOOD}")

# AHA! Let me check if we need to use a different grid reading
# Maybe it's interleaved differently

# Try: read odd positions, then even positions
evens = STREAM[0::2]  # positions 0, 2, 4, ...
odds = STREAM[1::2]   # positions 1, 3, 5, ...

print(f"\nEvens (0,2,4...): {evens[:40]}...")
print(f"Odds (1,3,5...):  {odds[:40]}...")
print(f"Evens+Odds: {(evens+odds)[:80]}...")

# Nope. Let me try the actual column reading formula
print("\n=== DIRECT FORMULA TEST ===")

# For grid with R rows and C cols, column-major reading:
# output[i] = input[ (i % R) * C + (i // R) ]

for R, C in [(2, 83), (83, 2)]:
    result = ""
    for i in range(len(STREAM)):
        src_idx = (i % R) * C + (i // R)
        if src_idx < len(STREAM):
            result += STREAM[src_idx]
    print(f"Grid {R}x{C} column read: {result[:80]}...")
    if result == KNOWN_GOOD:
        print(f"  *** MATCH! ***")

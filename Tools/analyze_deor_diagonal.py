
deor_msg = "DEAR SIX CUBITS DEAD LEARNING YEAR IMPERIAL AGUE THE SONG WHO EYE OPEN THE ISLE AIR SOLE A VIEW A HANGING GUESSING MEANING DIAGONAL"
pieces = deor_msg.replace(" ", "")
print(f"Message: {pieces}")
print(f"Length: {len(pieces)}")

import math
side = math.sqrt(len(pieces))
print(f"Sqrt: {side}")

if side.is_integer():
    width = int(side)
    print(f"Grid {width}x{width}")
    grid = [pieces[i:i+width] for i in range(0, len(pieces), width)]
    diag = ""
    for i in range(width):
        diag += grid[i][i]
    print(f"Diagonal: {diag}")
else:
    print("Not a perfect square. Trying implicit widths.")
    for w in range(2, 20):
        # Print diagonal for width w
        grid = [pieces[i:i+w] for i in range(0, len(pieces), w)]
        diag = ""
        for i in range(min(len(grid), w)):
            if i < len(grid[i]):
                diag += grid[i][i]
        print(f"Width {w} Diagonal: {diag}")


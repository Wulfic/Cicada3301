
import os

# Solution text from README.md
solution_text = """A KOAN
A MAN DECIDED TO GO AND STUDY WITH A MASTER.
HE WENT TO THE DOOR OF THE MASTER
"WHO ARE YOU WHO WISHES TO STUDY HERE?"
ASKED THE MASTER.
THE STUDENT TOLD THE MASTER HIS NAME.
"THAT IS NOT WHAT YOU ARE THAT IS ONLY WHAT YOU ARE CALLED.
WHO ARE YOU WHO WISHES TO STUDY HERE?" HE ASKED AGAIN."""

def clean_text(text):
    return "".join([c for c in text.upper() if c.isalpha()])

def print_grid(text, width):
    print(f"\n--- GRID WIDTH {width} ---")
    rows = [text[i:i+width] for i in range(0, len(text), width)]
    for r in rows:
        print(" ".join(list(r)))
    
    # Diagonal TL-BR
    diag = ""
    for i in range(min(len(rows), width)):
        if i < len(rows[i]):
            diag += rows[i][i]
    print(f"Diagonal TL-BR: {diag}")

    # Diagonal TR-BL
    diag_rev = ""
    for i in range(min(len(rows), width)):
        col = width - 1 - i
        if col >= 0 and i < len(rows[i]):
            diag_rev += rows[i][col]
    print(f"Diagonal TR-BL: {diag_rev}")

def main():
    cleaned = clean_text(solution_text)
    print(f"Cleaned Length: {len(cleaned)}")
    
    # "SIX CUBITS"
    print_grid(cleaned, 6)
    
    # "IMPERIAL" (8)
    print_grid(cleaned, 8)
    
    # Check if length is perfect square
    import math
    side = math.sqrt(len(cleaned))
    print(f"\nSqrt Length: {side}")
    if side.is_integer():
        print_grid(cleaned, int(side))

if __name__ == "__main__":
    main()

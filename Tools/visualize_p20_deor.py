
import os

# Rune Map
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

DEOR_VALUES = {
    7: 'W',  # Welund
    17: 'B', # Beadohild
    19: 'M', # Maethhild
    2: 'T',  # Theodric (TH)
    23: 'D'  # Deor
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace('-', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    COLS = 29
    ROWS = 28
    
    print("Page 20 Deor Rune Visualization")
    print("Legend: W=Welund(7), B=Beadohild(17), M=Maethhild(19), T=Theodric(2), D=Deor(23)")
    print("-" * COLS)
    
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            idx = r * COLS + c
            if idx < len(cipher):
                val = cipher[idx]
                if val in DEOR_VALUES:
                    row_str += DEOR_VALUES[val]
                else:
                    row_str += "."
            else:
                row_str += " "
        print(row_str)

if __name__ == "__main__":
    main()

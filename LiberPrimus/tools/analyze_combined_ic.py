
import os
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

def calculate_ic(text):
    indices = [RUNE_MAP[c] for c in text if c in RUNE_MAP]
    n = len(indices)
    if n < 2: return 0.0
    
    counts = Counter(indices)
    numerator = sum(v * (v - 1) for v in counts.values())
    denominator = n * (n - 1)
    
    return numerator / denominator

def main():
    base_dir = "c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages"
    
    combined_runes = ""
    for p in range(18, 55):
        path = os.path.join(base_dir, f"page_{p:02d}", "runes.txt")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                combined_runes += f.read()

    combined_ic = calculate_ic(combined_runes)
    print(f"Combined Pages 18-54 IC: {combined_ic:.5f}")
    print(f"Total Runes: {len([c for c in combined_runes if c in RUNE_MAP])}")

if __name__ == "__main__":
    main()

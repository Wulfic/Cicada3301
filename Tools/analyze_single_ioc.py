
import sys
import os
from collections import Counter

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

def load_runes(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return [RUNE_TO_IDX[r] for r in content if r in RUNE_TO_IDX]
    return []

def calculate_ioc(nums):
    if len(nums) < 2: return 0
    counts = Counter(nums)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(nums) * (len(nums) - 1)
    # The value 1.75 is approx expected for English (0.066 * 26 or something similar normalized)
    # For random text on alphabet size 29: 1.0
    return numerator / denominator * 29 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_single_ioc.py <file_path>")
        sys.exit(1)
        
    for path in sys.argv[1:]:
        nums = load_runes(path)
        ioc = calculate_ioc(nums)
        print(f"File: {os.path.basename(path)}")
        print(f"  Length: {len(nums)}")
        print(f"  IoC: {ioc:.4f}")
        
        if ioc > 1.5:
            print("  Likely Monoalphabetic or Transposition (or very short key)")
        elif ioc < 1.1:
            print("  Likely Polyalphabetic (Vigenere, etc)")
        else:
            print("  Ambiguous / Short Text")

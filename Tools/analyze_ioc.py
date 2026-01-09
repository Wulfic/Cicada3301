
import os
from collections import Counter

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

def load_page(page_num):
    paths = [
        f"LiberPrimus/pages/page_{page_num:02d}/runes.txt",
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [RUNE_TO_IDX[r] for r in content if r in RUNE_TO_IDX]
    return []

def calculate_ioc(nums):
    if len(nums) < 2: return 0
    counts = Counter(nums)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(nums) * (len(nums) - 1)
    return numerator / denominator * 29 # Normalized for 29 chars

for i in range(1, 15):
    runes = load_page(i)
    if not runes: continue
    ioc = calculate_ioc(runes)
    print(f"Page {i}: Length {len(runes)}, IoC: {ioc:.4f}")

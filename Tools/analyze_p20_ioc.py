
import sys
import collections

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0 # Normalized for 29 chars

def analyze_periods(runes, max_len=100):
    print(f"Total Runes: {len(runes)}")
    print("Top IoC values:")
    best_ioc = 0
    best_p = 0
    
    for p in range(1, max_len + 1):
        avg_ioc = 0
        for i in range(p):
            slice_text = runes[i::p]
            avg_ioc += calculate_ioc(slice_text)
        avg_ioc /= p
        
        if True: # Print top values
            # print(f"Period {p}: IoC = {avg_ioc:.4f}")
            pass
            
    # Sort and print
    results = []
    for p in range(1, max_len + 1):
        avg_ioc = 0
        for i in range(p):
            slice_text = runes[i::p]
            avg_ioc += calculate_ioc(slice_text)
        avg_ioc /= p
        results.append((p, avg_ioc))
    
    results.sort(key=lambda x: x[1], reverse=True)
    for p, ioc in results[:10]:
        print(f"Period {p}: IoC = {ioc:.4f}")

if __name__ == "__main__":
    file_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    runes = load_runes(file_path)
    analyze_periods(runes)

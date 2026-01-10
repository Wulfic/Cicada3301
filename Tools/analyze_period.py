
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
    return numerator / denominator * 29 

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_period.py <file_path>")
        sys.exit(1)
        
    path = sys.argv[1]
    cipher = load_runes(path)
    print(f"File: {os.path.basename(path)} (Len: {len(cipher)})")
    
    print("\n--- Period Analysis ---")
    
    potential_periods = []
    
    for period in range(1, 100):
        # Extract columns (slices)
        avg_ioc = 0
        valid_cols = 0
        
        for p in range(period):
            col = cipher[p::period]
            if len(col) > 1:
                avg_ioc += calculate_ioc(col)
                valid_cols += 1
                
        if valid_cols > 0:
            avg_ioc /= valid_cols
            
        print(f"Period {period:02d}: IOC {avg_ioc:.4f}")
        
        if avg_ioc > 1.4: # Threshold for 'English-like'
            potential_periods.append((period, avg_ioc))
            
    print("\n--- Top Periods ---")
    potential_periods.sort(key=lambda x: x[1], reverse=True)
    for p, ioc in potential_periods[:10]:
        print(f"Period {p}: {ioc:.4f}")

if __name__ == "__main__":
    main()

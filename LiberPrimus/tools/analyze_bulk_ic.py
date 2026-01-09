
import os
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

def calculate_ic(text):
    # Filter only valid runes
    indices = [RUNE_MAP[c] for c in text if c in RUNE_MAP]
    n = len(indices)
    if n < 2: return 0.0
    
    counts = Counter(indices)
    numerator = sum(v * (v - 1) for v in counts.values())
    denominator = n * (n - 1)
    
    return numerator / denominator

def main():
    base_dir = "c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages"
    
    # Ranges: 02, 18-54, 65-66, 69-71
    # Note: 69-70 might be empty/no runes, we check.
    
    targets = [2] + list(range(18, 55)) + [65, 66] + list(range(69, 72))
    
    results = []
    
    print(f"{'PAGE':<6} | {'IC':<8} | {'TYPE':<15} | {'RUNES':<6}")
    print("-" * 45)
    
    for p in targets:
        pg_str = f"page_{p:02d}"
        path = os.path.join(base_dir, pg_str, "runes.txt")
        
        if not os.path.exists(path):
            results.append((p, 0.0, "MISSING", 0))
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        ic = calculate_ic(content)
        cnt = len([c for c in content if c in RUNE_MAP])
        
        # Heuristic
        # English ~0.066, Random ~0.034 (for 29 runes) 
        # Actually random for 29 chars is 1/29 = ~0.0345
        
        if cnt < 10:
            type_guess = "EMPTY/LOW"
        elif ic > 0.055:
            type_guess = "MONO/TEXT"
        elif ic > 0.045:
            type_guess = "POSS. MONO"
        else:
            type_guess = "POLY/RAND"
            
        print(f"{p:<6} | {ic:.4f}   | {type_guess:<15} | {cnt:<6}")

if __name__ == "__main__":
    main()

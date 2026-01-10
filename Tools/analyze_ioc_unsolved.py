
import os
import collections

# Rune to index mapping (Gematria Primus)
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4,
    'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19,
    'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def calculate_ioc(indices):
    counts = collections.Counter(indices)
    numerator = sum(n * (n - 1) for n in counts.values())
    N = len(indices)
    return numerator / (N * (N - 1)) if N > 1 else 0

def analyze_page(page_num, repo_root):
    path = os.path.join(repo_root, "LiberPrimus", "pages", f"page_{page_num:02d}", "runes.txt")
    if not os.path.exists(path):
        print(f"Page {page_num} runes not found.")
        return

    indices = load_runes(path)
    print(f"\nPage {page_num} Analysis:")
    print(f"Length: {len(indices)}")
    
    # Overall IoC
    ioc = calculate_ioc(indices)
    print(f"Overall IoC: {ioc:.4f} (English ~0.066, Random ~0.034)")
    
    # Check for period lengths
    print("Period Analysis (Top 5):")
    best_period = 0
    best_avg_ioc = 0
    
    for period in range(1, 100):
        avg_ioc = 0
        columns = [[] for _ in range(period)]
        for i, val in enumerate(indices):
            columns[i % period].append(val)
        
        valid_cols = 0
        for col in columns:
            if len(col) > 1:
                avg_ioc += calculate_ioc(col)
                valid_cols += 1
        
        if valid_cols > 0:
            avg_ioc /= valid_cols
            if avg_ioc > best_avg_ioc:
                 best_avg_ioc = avg_ioc
                 best_period = period
            
            if avg_ioc > 0.06:
                print(f"  Period {period}: IoC {avg_ioc:.4f}")

    print(f"Best Period seems to be {best_period} with IoC {best_avg_ioc:.4f}")

def main():
    repo_root = r"c:\Users\tyler\Repos\Cicada3301"
    # Analyze Unsolved Pages
    analyze_page(18, repo_root)
    analyze_page(71, repo_root)

if __name__ == "__main__":
    main()

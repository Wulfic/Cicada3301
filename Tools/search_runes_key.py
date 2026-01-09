
import os

# RUNE CHARS
RUNE_CHARS = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28 #, 'ᛂ': 11
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg:02d}\\runes.txt"
    if not os.path.exists(path):
        # Try no zero pad
        path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            runes = f.read()
            return [RUNE_CHARS[c] for c in runes if c in RUNE_CHARS]
    return []

def main():
    all_runes = []
    page_starts = {}
    
    # Load all pages 0 to 70
    for pg in range(71):
        r = load_runes(pg)
        if r:
            page_starts[pg] = len(all_runes)
            all_runes.extend(r)
            # print(f"Loaded Page {pg}, length {len(r)}")
            
    print(f"Total Runes in Workspace (0-70): {len(all_runes)}")
    
    # Target sequences
    # FEOPATH: 0, 18, 3, 13, 24, 16, 8
    target1 = [0, 18, 3, 13, 24, 16, 8]
    
    # Just FEO: 0, 18, 3
    target2 = [0, 18, 3]
    
    # Just PATH: 13, 24, 16, 8
    target3 = [13, 24, 16, 8]
    
    # Search
    def search(tgt, name):
        print(f"Searching for {name} ({tgt})...")
        found = False
        for i in range(len(all_runes) - len(tgt)):
            if all_runes[i:i+len(tgt)] == tgt:
                print(f"  FOUND at index {i}!")
                # Identify which page
                for p in sorted(page_starts.keys()):
                    if page_starts[p] <= i:
                        pg_num = p
                    else:
                        break
                print(f"  (Page {pg_num}, offset {i - page_starts[pg_num]})")
                found = True
        if not found:
            print("  Not found.")

    search(target1, "FEOPATH")
    search(target3, "PATH")
    search(target2, "FEO")

if __name__ == "__main__":
    main()

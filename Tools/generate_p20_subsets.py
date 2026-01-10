import os
import collections

# GP Mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [c for c in content if c in RUNE_MAP]

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    # Subset 1: Prime Indices (0-based)
    sub1 = [cipher[i] for i in range(len(cipher)) if is_prime(i)]
    with open(os.path.join(repo, "LiberPrimus", "pages", "page_20", "subset_prime_indices.txt"), 'w', encoding='utf-8') as f:
        f.write("".join(sub1))
        
    # Subset 2: Prime Values
    sub2 = [c for c in cipher if is_prime(RUNE_MAP[c])]
    with open(os.path.join(repo, "LiberPrimus", "pages", "page_20", "subset_prime_values.txt"), 'w', encoding='utf-8') as f:
        f.write("".join(sub2))

    print(f"Generated Subset 1 (Prime Indices): {len(sub1)} runes")
    print(f"Generated Subset 2 (Prime Values): {len(sub2)} runes")

if __name__ == "__main__":
    main()

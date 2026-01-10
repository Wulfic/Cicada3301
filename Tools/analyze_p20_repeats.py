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

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher_runes = load_runes(p20_path)
    cipher_indices = [RUNE_MAP[c] for c in cipher_runes]
    
    # Search for repeats of length 3+
    MAX_LEN = 10
    MIN_LEN = 3
    
    repeats = collections.defaultdict(list)
    
    for length in range(MIN_LEN, MAX_LEN + 1):
        seen = {}
        for i in range(len(cipher_indices) - length + 1):
            gram = tuple(cipher_indices[i:i+length])
            if gram in seen:
                dist = i - seen[gram]
                repeats[length].append((gram, dist, seen[gram], i))
            else:
                seen[gram] = i
                
    print(f"Total Repeated N-grams Found: {sum(len(v) for v in repeats.values())}")
    for length in sorted(repeats.keys(), reverse=True):
        if repeats[length]:
            print(f"\n--- Length {length} ---")
            for gram, dist, i1, i2 in repeats[length]:
                # Factorize distance
                factors = []
                d = dist
                for x in range(2, d+1):
                    if d % x == 0: factors.append(x)
                
                print(f"Gram: {gram} | Locs: {i1}, {i2} | Dist: {dist} | Factors: {factors}")

if __name__ == "__main__":
    main()


import os
import sys

# Rune to index mapping (Gematria Primus)
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4,
    'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19,
    'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M',
    20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            primes.append(num)
        num += 1
    return primes

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def score_text(text):
    common = ['THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'THIS', 'NOT', 'FOR', 'BUT', 'ARE', 'ALL', 'FROM']
    score = 0
    for w in common:
        score += text.count(w) * len(w)
    return score

def decrypt(cipher, primes, start_idx):
    dec = []
    pidx = start_idx
    
    for c in cipher:
        p_val = primes[pidx % len(primes)]
        phi = p_val - 1
        # P = (C - phi) % 29
        p = (c - phi) % 29
        dec.append(LATIN_TABLE[p])
        pidx += 1
    return "".join(dec)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p71_runes_file = os.path.join(repo, "LiberPrimus", "pages", "page_71", "runes.txt")
    
    if not os.path.exists(p71_runes_file):
        print("Page 71 runes not found")
        return

    cipher = load_runes(p71_runes_file)
    print(f"Loaded Page 71: {len(cipher)} runes")
    
    # Generate primes
    primes = generate_primes(5000)
    
    best_score = 0
    best_info = ""
    
    # Scan offsets
    # Also check reversed prime order or other variations if simple scan fails
    
    for start in range(0, 4000):
        res = decrypt(cipher, primes, start)
        s = score_text(res)
        if s > best_score:
            best_score = s
            best_info = f"Prime Offset {start} (P={primes[start]}) | Score: {s}\n{res[:100]}"
            if s > 30: # Only print if somewhat promising
                 print(f"Hit: {best_info}")

    print("\nBest Result:")
    print(best_info)

if __name__ == "__main__":
    main()

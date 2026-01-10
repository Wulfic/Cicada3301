
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
    """Generate first n primes."""
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
    common = ['THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'THIS', 'NOT', 'FOR', 'BUT', 'ARE', 'ALL', 'FROM', 'OF', 'TO']
    score = 0
    for w in common:
        score += text.count(w) * len(w)
    return score

def decrypt_totient(cipher, primes, start_index, literal_f=False):
    decrypted = []
    key_idx = start_index % len(primes)
    
    for c in cipher:
        # Literal F logic (simplified assumption: if Cipher is F, it stays F, and we skip key)
        if literal_f and c == 0:
            decrypted.append(LATIN_TABLE[0])
            continue
            
        p = primes[key_idx]
        phi = p - 1
        # Decrypt: P = (C - phi) % 29
        # Assuming SUB mode as per Page 55
        decoded = (c - phi) % 29
        decrypted.append(LATIN_TABLE[decoded])
        
        key_idx = (key_idx + 1) % len(primes)
        
    return "".join(decrypted)

def main():
    repo_root = r"c:\Users\tyler\Repos\Cicada3301"
    p18_path = os.path.join(repo_root, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    if not os.path.exists(p18_path):
        print("Page 18 runes not found")
        return

    cipher_indices = load_runes(p18_path)
    print(f"Loaded Page 18: {len(cipher_indices)} runes")
    
    # Generate enough primes
    # Page length is ~300? 
    # generate 2000 primes to be safe for offsets
    primes = generate_primes(3000) 
    
    best_score = 0
    best_info = ""

    # Test shifting start index
    # Also test literal F on/off
    
    for literal_f in [True, False]:
        for start in range(0, 2000):
            dec = decrypt_totient(cipher_indices, primes, start, literal_f)
            s = score_text(dec)
            if s > best_score:
                best_score = s
                best_info = f"Start Prime: {primes[start]} (Idx {start}) | Literal F: {literal_f}\nResult: {dec[:100]}"
                # print(f"New Best: {best_info}") # too noisy

    print("\nBest Result:")
    print(best_info)

if __name__ == "__main__":
    main()

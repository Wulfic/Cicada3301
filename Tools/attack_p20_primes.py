
import sys

# Constants
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

COMMON_WORDS = {
    'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'THIS', 'NOT', 'FOR', 'BUT', 'ARE', 'ALL', 'FROM',
    'CICADA', 'PRIMES', 'TOTIENT', 'ENLIGHTENMENT', 'CONSUMPTION', 'WELCOME', 'PILGRIM', 'INSTRUCTION',
    'WITHIN', 'DEEP', 'WEB', 'EXISTS', 'PAGE', 'HASHES', 'DUTY', 'EVERY', 'SEEK', 'OUT', 'FIND',
    'WARNING', 'BELIEVE', 'NOTHING', 'BOOK', 'INTUS', 'CHAPTER', 'KOAN', 'MASTER', 'LIKE', 'INSTAR',
    'BEING', 'VISIBLE', 'INVISIBLE', 'OATH', 'ABOVE', 'BELOW', 'FORM', 'VOID', 'LIFE', 'DEATH',
    'WILL', 'ONE', 'WAY'
}

TRIGRAMS = {
    'THE': 50, 'AND': 40, 'THA': 30, 'ENT': 30, 'ION': 30, 'ING': 40,
    'HER': 20, 'FOR': 25, 'HIS': 20, 'OFT': 25, 'ITH': 25, 'FTH': 20, 'STH': 20
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    for t, v in TRIGRAMS.items():
        score += text.count(t) * v
    return score

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate: break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    primes = generate_primes(len(cipher))
    
    # Try SUB
    plain_sub = []
    for i, c in enumerate(cipher):
        k = primes[i]
        plain_sub.append((c - k) % 29)
    txt_sub = text_from_indices(plain_sub)
    print(f"SUB Primes Score: {score_text(txt_sub)}")
    print(f"Preview: {txt_sub[:100]}...")

    # Try ADD
    plain_add = []
    for i, c in enumerate(cipher):
        k = primes[i]
        plain_add.append((c + k) % 29)
    txt_add = text_from_indices(plain_add)
    print(f"ADD Primes Score: {score_text(txt_add)}")
    print(f"Preview: {txt_add[:100]}...")

if __name__ == "__main__":
    main()

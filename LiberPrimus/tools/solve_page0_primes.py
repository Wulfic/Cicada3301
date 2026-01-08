
import collections
import sympy

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

RUNES = """
ᛋᚻᛖᚩᚷᛗᛡᚠ-ᛋᚣᛖᛝᚳ.ᚦᛄᚷᚫ-ᚠᛄᛟ-

ᚩᚾᚦ-ᚾᛖᚹᛒᚪᛋᛟᛇᛁᛝᚢ-ᚾᚫᚷᛁᚦ-ᚻᛒᚾᛡ-
"""
# Need full runes. I'll read from file in main.

def parse_runes(text):
    return [RUNE_MAP[c] for c in text if c in RUNE_MAP]

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def generate_prime_key(length, start_prime_idx=0, shift=0):
    primes = []
    p = 2
    count = 0
    # Skip to start_prime_idx
    while count < start_prime_idx:
        p = sympy.nextprime(p)
        count += 1
    
    key = []
    for _ in range(length):
        key.append((p + shift) % 29)
        p = sympy.nextprime(p)
    return key

def score_text(text):
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL']
    score = 0
    upper_text = text.upper()
    for word in common_words:
        score += upper_text.count(word) * len(word)
    return score

def main():
    with open(r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    cipher = parse_runes(content)
    length = len(cipher)
    print(f"Rune count: {length}")
    
    # Try shifts 0 to 28, and start_prime_idx 0 (2) to 100
    best_score = 0
    best_res = ""
    
    print("Testing Prime Keys...")
    for start_idx in range(100):
        for shift in range(29):
            key = generate_prime_key(length, start_idx, shift)
            plain = [(c - k) % 29 for c, k in zip(cipher, key)]
            text = indices_to_text(plain)
            score = score_text(text)
            
            if score > 20: # Threshold
                print(f"Start Prime #{start_idx} ({sympy.prime(start_idx+1)}), Shift {shift}: Score {score}")
                print(f"Preview: {text[:50]}")
                if score > best_score:
                    best_score = score
                    best_res = text

if __name__ == "__main__":
    main()


import os
from collections import Counter

# Rune Map
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace('-', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def to_letters(values):
    return "".join([LATIN_TABLE[v] for v in values])

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def get_totient(n):
    # Euler's Totient Function
    count = 0
    for i in range(1, n):
        if os.sys.modules['math'].gcd(i, n) == 1:
            count += 1
    return count

# Need gcd
import math

def generate_totient_stream(length):
    stream = []
    n = 2
    while len(stream) < length:
        if is_prime(n):
            # Key is phi(prime)
            # phi(p) = p - 1
            stream.append((n - 1) % 29)
        n += 1
    return stream

def generate_totient_stream_all(length):
    stream = []
    n = 1
    while len(stream) < length:
        # Key is phi(n)
        phi = 0
        for k in range(1, n+1):
            if math.gcd(n, k) == 1:
                phi += 1
        stream.append(phi % 29)
        n += 1
    return stream

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    # 1. Totient of Primes Stream
    # stream = [phi(2), phi(3), phi(5)...]
    # phi(p) = p-1. So [1, 2, 4, 6...]
    key1 = generate_totient_stream(len(cipher))
    
    dec1 = [(c - k) % 29 for c, k in zip(cipher, key1)]
    print(f"Totient(Primes) Stream IoC: {calculate_ioc(dec1):.4f}")
    print(f"Preview: {to_letters(dec1)[:50]}")
    
    # 2. Totient of Integers Stream
    # stream = [phi(1), phi(2), phi(3)...]
    key2 = generate_totient_stream_all(len(cipher))
    dec2 = [(c - k) % 29 for c, k in zip(cipher, key2)]
    print(f"Totient(Ints) Stream IoC: {calculate_ioc(dec2):.4f}")
    
    # 3. Totient of Primes reversed?
    key3 = key1[::-1]
    dec3 = [(c - k) % 29 for c, k in zip(cipher, key3)]
    print(f"Totient(Primes) Reversed IoC: {calculate_ioc(dec3):.4f}")

if __name__ == "__main__":
    main()

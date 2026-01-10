import collections

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
INV_RUNE_MAP = {v: k for k, v in RUNE_MAP.items()}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [c for c in content if c in RUNE_MAP]

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

p20_runes = load_runes('LiberPrimus/pages/page_20/runes.txt')

primes_0 = [i for i in range(len(p20_runes)) if is_prime(i)]

def calc_ioc(runes):
    if len(runes) < 2: return 0
    c = collections.Counter(runes)
    num = sum(n * (n - 1) for n in c.values())
    den = len(runes) * (len(runes) - 1)
    return num / den * 29.0

# Filter by Rune Value being Prime
prime_value_runes = [r for r in p20_runes if is_prime(RUNE_MAP[r])]
non_prime_value_runes = [r for r in p20_runes if not is_prime(RUNE_MAP[r])]

print(f"Total Runes: {len(p20_runes)}")
print(f"Runes with Prime GP Values: {len(prime_value_runes)}")
print(f"IoC: {calc_ioc(prime_value_runes):.4f}")
print("".join(prime_value_runes)[:100])

print(f"\nRunes with Non-Prime GP Values: {len(non_prime_value_runes)}")
print(f"IoC: {calc_ioc(non_prime_value_runes):.4f}")
print("".join(non_prime_value_runes)[:100])


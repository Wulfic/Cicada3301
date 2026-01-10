import os

def get_rune_map():
    return {
        'ᚠ':0, 'ᚢ':1, 'ᚦ':2, 'ᚩ':3, 'ᚱ':4, 'ᚳ':5, 'ᚷ':6, 'ᚹ':7, 'ᚻ':8, 'ᚾ':9, 'ᛁ':10, 'ᛄ':11, 'ᛇ':12,
        'ᛈ':13, 'ᛉ':14, 'ᛋ':15, 'ᛏ':16, 'ᛒ':17, 'ᛖ':18, 'ᛗ':19, 'ᛚ':20, 'ᛝ':21, 'ᛟ':22, 'ᛞ':23, 'ᚪ':24,
        'ᚫ':25, 'ᚣ':26, 'ᛡ':27, 'ᛠ':28
    }

def main():
    path = "LiberPrimus/pages/page_20/runes.txt"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    runes = [c for c in content if c in get_rune_map()]
    print(f"Content Length: {len(content)}")
    print(f"Rune Count: {len(runes)}")

    # Check prime limit
    limit = len(runes)
    primes = 0
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n%i==0: return False
        return True
    
    for i in range(limit):
        if is_prime(i): primes += 1
    
    print(f"Primes in range(0, {limit}): {primes}")

if __name__ == "__main__":
    main()

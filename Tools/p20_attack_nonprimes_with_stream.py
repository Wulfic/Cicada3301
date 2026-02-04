"""
Page 20 - Attack Non-Prime Runes with 166-Stream as Key
========================================================
The 166-stream from prime positions (IoC=1.8952) decoded to:
HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW

We'll use this as a potential key for the 646 non-prime indexed runes.
Cicada likes self-referential puzzles - this is perfect!
"""

import os
from collections import Counter
from itertools import cycle

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def to_str(nums):
    return "".join(RUNEGLISH[n % 29] for n in nums)

def calc_ioc(text):
    """Calculate Index of Coincidence"""
    if len(text) < 2:
        return 0
    counts = Counter(text)
    n = len(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Load P20
p20 = load_runes("LiberPrimus/pages/page_20/runes.txt")
print(f"[*] Page 20: {len(p20)} runes loaded")

# Extract prime and non-prime indices
prime_indices = [i for i in range(len(p20)) if is_prime(i)]
non_prime_indices = [i for i in range(len(p20)) if not is_prime(i)]

print(f"[*] Prime indices: {len(prime_indices)}")
print(f"[*] Non-prime indices: {len(non_prime_indices)}")

# Get prime and non-prime runes
prime_runes = [p20[i] for i in prime_indices]
non_prime_runes = [p20[i] for i in non_prime_indices]

print(f"[*] Prime runes: {len(prime_runes)}")
print(f"[*] Non-prime runes: {len(non_prime_runes)}")

# The 166-stream (should match prime runes length)
STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Convert to indices
stream_indices = [RUNEGLISH.index(c) if c in RUNEGLISH else 
                  RUNEGLISH.index(RUNEGLISH[-1]) for c in STREAM_166]

print(f"[*] Stream 166: {len(stream_indices)} elements")

# ============================================
# STRATEGY 1: Use 166-stream as key for Vigenère SUB on non-primes
# ============================================

print("\n" + "="*60)
print("STRATEGY 1: Vigenère SUB with 166-stream as key")
print("="*60)

stream_key = cycle(stream_indices)
decrypted = []
for cipher_val in non_prime_runes:
    key_val = next(stream_key)
    plain_val = (cipher_val - key_val) % 29
    decrypted.append(plain_val)

decrypted_text = to_str(decrypted)
ioc = calc_ioc(decrypted_text)
print(f"IoC: {ioc:.4f}")
print(f"Result: {decrypted_text[:100]}...")

# Look for common words
words_check = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'ONE', 'HER',
               'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'DEATH', 'PATH']
found_words = [w for w in words_check if w in decrypted_text]
print(f"Words found: {found_words}")

if ioc > 1.5 or found_words:
    print(f"\n[+] PROMISING! Full result:")
    print(decrypted_text)
    with open("p20_non_prime_sub_result.txt", "w") as f:
        f.write(decrypted_text)

# ============================================
# STRATEGY 2: Use 166-stream as key for Vigenère ADD on non-primes
# ============================================

print("\n" + "="*60)
print("STRATEGY 2: Vigenère ADD with 166-stream as key")
print("="*60)

stream_key = cycle(stream_indices)
decrypted = []
for cipher_val in non_prime_runes:
    key_val = next(stream_key)
    plain_val = (cipher_val + key_val) % 29
    decrypted.append(plain_val)

decrypted_text = to_str(decrypted)
ioc = calc_ioc(decrypted_text)
print(f"IoC: {ioc:.4f}")
print(f"Result: {decrypted_text[:100]}...")

found_words = [w for w in words_check if w in decrypted_text]
print(f"Words found: {found_words}")

if ioc > 1.5 or found_words:
    print(f"\n[+] PROMISING! Full result:")
    print(decrypted_text)
    with open("p20_non_prime_add_result.txt", "w") as f:
        f.write(decrypted_text)

# ============================================
# STRATEGY 3: Beaufort cipher with 166-stream
# ============================================

print("\n" + "="*60)
print("STRATEGY 3: Beaufort cipher with 166-stream as key")
print("="*60)

stream_key = cycle(stream_indices)
decrypted = []
for cipher_val in non_prime_runes:
    key_val = next(stream_key)
    plain_val = (key_val - cipher_val) % 29
    decrypted.append(plain_val)

decrypted_text = to_str(decrypted)
ioc = calc_ioc(decrypted_text)
print(f"IoC: {ioc:.4f}")
print(f"Result: {decrypted_text[:100]}...")

found_words = [w for w in words_check if w in decrypted_text]
print(f"Words found: {found_words}")

if ioc > 1.5 or found_words:
    print(f"\n[+] PROMISING! Full result:")
    print(decrypted_text)
    with open("p20_non_prime_beaufort_result.txt", "w") as f:
        f.write(decrypted_text)

# ============================================
# STRATEGY 4: Try Caesar-like fixed shifts on non-primes
# ============================================

print("\n" + "="*60)
print("STRATEGY 4: Fixed Caesar shifts (0-28) on non-primes")
print("="*60)

best_ioc = 0
best_shift = 0
best_text = ""

for shift in range(29):
    decrypted = [(r - shift) % 29 for r in non_prime_runes]
    decrypted_text = to_str(decrypted)
    ioc = calc_ioc(decrypted_text)
    
    if ioc > best_ioc:
        best_ioc = ioc
        best_shift = shift
        best_text = decrypted_text
    
    found_words = [w for w in words_check if w in decrypted_text]
    if found_words:
        print(f"Shift {shift}: IoC={ioc:.4f}, Words: {found_words}")

print(f"\nBest shift: {best_shift}, IoC: {best_ioc:.4f}")
print(f"Result: {best_text[:100]}...")

found_words = [w for w in words_check if w in best_text]
print(f"Words: {found_words}")

if best_ioc > 1.5 or len(found_words) >= 3:
    print(f"\n[+] PROMISING! Full result (shift {best_shift}):")
    print(best_text)
    with open(f"p20_non_prime_shift{best_shift}_result.txt", "w") as f:
        f.write(best_text)

# ============================================
# Additional analysis
# ============================================

print("\n" + "="*60)
print("ANALYSIS: Non-Prime Rune Frequencies")
print("="*60)

freq = Counter(non_prime_runes)
print(f"Most common rune indices: {freq.most_common(5)}")
print(f"Total unique runes: {len(freq)}")

print(f"\n[*] Non-prime runes as text: {to_str(non_prime_runes)[:100]}...")
print(f"IoC of raw non-prime stream: {calc_ioc(to_str(non_prime_runes)):.4f}")

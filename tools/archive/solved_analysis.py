#!/usr/bin/env python3
"""
Analyze SOLVED pages to understand the cipher patterns.
Then apply learnings to unsolved pages.
"""

import re

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

def rune_to_letters(runes):
    return ''.join(RUNE_TO_LETTER.get(r, '?') for r in runes)

def get_runes_only(page):
    return ''.join(c for c in page if c in RUNE_TO_IDX)

# Read pages
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def decrypt_caesar(cipher_runes, shift):
    result = []
    for rune in cipher_runes:
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            plain_idx = (idx - shift) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

print("="*70)
print("ANALYZING SOLVED PAGE 56")
print("="*70)

# Page 56 is known to decrypt with shift 57 using GP-SUM-PRIMES cipher
# But let's verify: shift 57 mod 29 = 28
cipher_56 = get_runes_only(PAGES[56])
print(f"Page 56 cipher length: {len(cipher_56)}")
print(f"Cipher: {rune_to_letters(cipher_56[:30])}...")

# The "shift 57" is actually using Totient primes
# Let me check what the actual method was

# Try shift 57 applied to each position
decrypted_57 = decrypt_caesar(cipher_56, 57 % 29)  # Just shift 28
print(f"\nCaesar shift 28: {rune_to_letters(decrypted_57[:50])}")

# Try with shift 57 as a Gematria-based constant
# The key might be: use prime 57 (but 57 isn't prime... 3*19)

# Actually, page 56 uses a TOTIENT STREAM cipher
# Each position uses prime(i+1) mod 29

def totient_stream_decrypt(cipher_runes, prime_constant):
    """Decrypt using totient stream - each position uses prime(i) mod 29."""
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            # Use the (i+1)th prime + constant, mod 29
            if i < len(GP_PRIMES):
                shift = (GP_PRIMES[i] + prime_constant) % 29
            else:
                shift = (GP_PRIMES[i % 29] + prime_constant) % 29
            plain_idx = (idx - shift) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

for const in range(30):
    decrypted = totient_stream_decrypt(cipher_56, const)
    text = rune_to_letters(decrypted)
    if "THE" in text or "AND" in text:
        print(f"Constant {const}: {text[:60]}")

print("\n" + "="*70)
print("ANALYZING SOLVED PAGES 0-24 (use Vigenere with master key)")
print("="*70)

# Let's verify some solved pages
for pg in [0, 54, 56]:
    if pg in PAGES:
        cipher = get_runes_only(PAGES[pg])
        decrypted = decrypt_vigenere(cipher, MASTER_KEY)
        text = rune_to_letters(decrypted)[:80]
        print(f"\nPage {pg}: {text}...")

print("\n" + "="*70)
print("THE KEY INSIGHT: Check if Page 0 and 54 are SAME")
print("="*70)

p0 = get_runes_only(PAGES[0])
p54 = get_runes_only(PAGES[54])
print(f"Page 0 length:  {len(p0)}")
print(f"Page 54 length: {len(p54)}")
print(f"Are they equal: {p0 == p54}")

if p0 == p54:
    print("\nPages 0 and 54 are IDENTICAL!")
    print("This confirms the circular nature of Liber Primus")

print("\n" + "="*70)
print("ANALYZE: What makes unsolved pages different?")
print("="*70)

# Compare frequency distributions of solved vs unsolved pages
def get_freq_distribution(rune_text):
    from collections import Counter
    freq = Counter(rune_text)
    total = len(rune_text)
    return {RUNE_TO_LETTER[r]: count/total for r, count in freq.items() if r in RUNE_TO_LETTER}

print("\nSolved page frequency (Page 0 decrypted):")
p0_decrypted = decrypt_vigenere(p0, MASTER_KEY)
solved_freq = get_freq_distribution(p0_decrypted)
for letter, freq in sorted(solved_freq.items(), key=lambda x: -x[1])[:5]:
    print(f"  {letter}: {freq*100:.1f}%")

print("\nUnsolved page frequency (Page 27 raw):")
p27_raw = get_runes_only(PAGES[27])
unsolved_freq = get_freq_distribution(p27_raw)
for letter, freq in sorted(unsolved_freq.items(), key=lambda x: -x[1])[:5]:
    print(f"  {letter}: {freq*100:.1f}%")

print("\n" + "="*70)
print("KEY RECOVERY ATTEMPT: If we know some plaintext...")
print("="*70)

# If the unsolved pages start with common words, we can try to recover the key
# Common starting phrases in Liber Primus: "SOME WISDOM...", "AN INSTRUCTION...", etc.

# Let's test if any unsolved page starts with "THE" (ᚦᛖ)
THE_runes = "ᚦᛖ"
THE_idx = [RUNE_TO_IDX[r] for r in THE_runes]  # [2, 18]

for pg in [27, 28, 29, 30, 31]:
    cipher = get_runes_only(PAGES[pg])
    cipher_start = [RUNE_TO_IDX[r] for r in cipher[:2]]
    
    # If plaintext starts with THE, the key would be:
    # key[0] = (cipher[0] - TH_idx) % 29
    # key[1] = (cipher[1] - E_idx) % 29
    
    key_if_THE = [(cipher_start[i] - THE_idx[i]) % 29 for i in range(2)]
    print(f"\nPage {pg}: If starts with 'THE', key begins with {key_if_THE}")
    
    # Check if this matches master key at some offset
    for offset in range(95):
        if MASTER_KEY[offset] == key_if_THE[0] and MASTER_KEY[(offset+1) % 95] == key_if_THE[1]:
            print(f"  MATCH at offset {offset}!")

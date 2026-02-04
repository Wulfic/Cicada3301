"""
Page 21 Full Decryption Verification
=====================================
Decrypt with CABAL/Beaufort and extract plaintext.
"""

from collections import Counter

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
    result = ""
    for n in nums:
        idx = n % 29
        result += RUNEGLISH[idx]
    return result

def calc_ioc(text):
    if len(text) < 2:
        return 0
    counts = Counter(text)
    n = len(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def string_to_key(s):
    gematria_map = {runeglish: i for i, runeglish in enumerate(RUNEGLISH)}
    key = []
    i = 0
    s = s.upper()
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in gematria_map:
            key.append(gematria_map[s[i:i+2]])
            i += 2
        elif s[i] in gematria_map:
            key.append(gematria_map[s[i]])
            i += 1
        else:
            i += 1
    return key

import os
os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Load Page 21
p21_runes = load_runes("LiberPrimus/pages/page_21/runes.txt")
print(f"[*] Page 21: {len(p21_runes)} runes")

# Decrypt with CABAL / Beaufort
key = string_to_key("CABAL")
print(f"[*] Key CABAL: {key}")

decrypted = []
key_cycle = 0
for cipher_val in p21_runes:
    key_val = key[key_cycle % len(key)]
    plain_val = (key_val - cipher_val) % 29  # Beaufort
    decrypted.append(plain_val)
    key_cycle += 1

decrypted_text = to_str(decrypted)
ioc = calc_ioc(decrypted_text)

print(f"\n[*] IoC: {ioc:.4f}")
print(f"\n[*] Full Plaintext:\n")
print(decrypted_text)

# Try to find word boundaries
print("\n" + "="*80)
print("WORD ANALYSIS")
print("="*80)

common_words = ['THE', 'AND', 'BUT', 'FOR', 'ARE', 'NOT', 'YOU', 'ALL', 'ONE', 'HER',
               'THAT', 'THIS', 'WITH', 'HAVE', 'THEY', 'BEEN', 'KNOW', 'FROM', 'WHEN',
               'WHAT', 'WHERE', 'WILL', 'WHICH', 'WOULD', 'COULD', 'SHOULD', 'THERE']

found_words = {}
for word in common_words:
    if word in decrypted_text:
        found_words[word] = decrypted_text.find(word)

if found_words:
    print(f"\n[+] Found {len(found_words)} common English words:")
    for word in sorted(found_words, key=found_words.get):
        print(f"    {word} at position {found_words[word]}")

# Look for letter frequencies
print("\n" + "="*80)
print("LETTER FREQUENCIES")
print("="*80)

freq = Counter(decrypted_text)
total = len(decrypted_text)
print(f"\nMost common (comparing to English expectations):")
print(f"{'Char':<5} {'Count':<6} {'%':<8} {'Eng %'}")
print("-" * 35)

eng_freq = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 
            'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8}

for char, count in freq.most_common(15):
    pct = count / total * 100
    eng_pct = eng_freq.get(char, 0)
    print(f"{char:<5} {count:<6} {pct:<8.1f} {eng_pct:>6.1f}")

# Try to segment
print("\n" + "="*80)
print("TRYING TRIGRAPH PATTERNS")
print("="*80)

for i in range(0, min(len(decrypted_text)-30, 200), 10):
    substring = decrypted_text[i:i+30]
    print(f"Pos {i:3d}: {substring}")

# Save the plaintext
with open("p21_decrypted_cabal_beaufort.txt", "w") as f:
    f.write(f"PAGE 21 - CABAL/BEAUFORT\n")
    f.write(f"IoC: {ioc:.4f}\n")
    f.write(f"Runes: {len(p21_runes)}\n")
    f.write("="*80 + "\n\n")
    f.write(decrypted_text)

print(f"\n[*] Saved to: p21_decrypted_cabal_beaufort.txt")

# Try other promising methods for Page 21
print("\n" + "="*80)
print("TRYING OTHER METHODS FOR PAGE 21")
print("="*80)

methods = [
    ("CABAL", "ADD", lambda c, k: (c + k) % 29),
    ("CABAL", "SUB", lambda c, k: (c - k) % 29),
    ("MOURNFUL", "ADD", lambda c, k: (c + k) % 29),
    ("MOURNFUL", "BEAUFORT", lambda c, k: (k - c) % 29),
]

for keyword, mode, cipher_func in methods:
    key = string_to_key(keyword)
    decrypted = []
    key_cycle = 0
    for cipher_val in p21_runes:
        key_val = key[key_cycle % len(key)]
        plain_val = cipher_func(cipher_val, key_val)
        decrypted.append(plain_val)
        key_cycle += 1
    
    decrypted_text = to_str(decrypted)
    ioc = calc_ioc(decrypted_text)
    found = [w for w in common_words if w in decrypted_text]
    
    print(f"\n{keyword:12} / {mode:8}: IoC={ioc:.4f}, Words={found}")
    if ioc > 1.85:
        print(f"Preview: {decrypted_text[:80]}")

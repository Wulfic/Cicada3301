#!/usr/bin/env python3
"""
Page 17 Deep Analysis - Handle word separators correctly
"""

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

# Load Page 17
with open(r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_17\runes.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print("Page 17 Raw Content (first 500 chars):")
print(content[:500])
print("\n" + "="*80)

# Extract words (separated by •)
words = []
current_word = []
for char in content:
    if char in RUNE_MAP:
        current_word.append(RUNE_MAP[char])
    elif char == '•':
        if current_word:
            words.append(current_word)
            current_word = []
    elif char == '\n':
        if current_word:
            words.append(current_word)
            current_word = []
if current_word:
    words.append(current_word)

print(f"Found {len(words)} words")
print(f"Word lengths: {[len(w) for w in words[:30]]}")

# Key YAHEOOPYJ = [26, 24, 8, 12, 3, 13, 26, 11]
KEY = [26, 24, 8, 12, 3, 13, 26, 11]

# Method 1: Key resets at each word
print("\n" + "="*80)
print("Method 1: Key resets at each word boundary")
print("="*80)
result = []
for word in words:
    decrypted_word = []
    for i, c in enumerate(word):
        k = KEY[i % len(KEY)]
        p = (c - k) % 29
        decrypted_word.append(LETTERS[p])
    result.append(''.join(decrypted_word))

print(' '.join(result[:50]))

# Method 2: Key continues across word boundaries (skip the bullet)
print("\n" + "="*80)
print("Method 2: Key continues across words")
print("="*80)
all_runes = [RUNE_MAP[c] for c in content if c in RUNE_MAP]
result2 = []
key_idx = 0
for i, c in enumerate(all_runes):
    k = KEY[key_idx % len(KEY)]
    p = (c - k) % 29
    result2.append(LETTERS[p])
    key_idx += 1

# Reconstruct with spaces at word boundaries
output = []
idx = 0
for char in content:
    if char in RUNE_MAP:
        output.append(result2[idx])
        idx += 1
    elif char == '•':
        output.append(' ')
    elif char == '\n':
        output.append('\n')

print(''.join(output[:500]))

# Method 3: Try different key - maybe EO should be E + O
print("\n" + "="*80)
print("Method 3: Key as Y=26, A=24, H=8, E=18, O=3, O=3, P=13, Y=26, J=11")
print("="*80)
KEY2 = [26, 24, 8, 18, 3, 3, 13, 26, 11]
result3 = []
for i, c in enumerate(all_runes):
    k = KEY2[i % len(KEY2)]
    p = (c - k) % 29
    result3.append(LETTERS[p])

output3 = []
idx = 0
for char in content:
    if char in RUNE_MAP:
        output3.append(result3[idx])
        idx += 1
    elif char == '•':
        output3.append(' ')
    elif char == '\n':
        output3.append('\n')

print(''.join(output3[:500]))

# Analyze what "EPILOGUE" tells us
print("\n" + "="*80)
print("Analyzing EPILOGUE match:")
print("="*80)
expected = "EPILOGUE"
expected_indices = [18, 13, 10, 20, 3, 6, 1, 18]  # E, P, I, L, O, G, U, E
cipher_start = all_runes[:8]
print(f"Expected plaintext: {expected}")
print(f"Expected indices: {expected_indices}")
print(f"Cipher indices: {cipher_start}")
print(f"Key needed (cipher - plain):")
for i in range(8):
    needed = (cipher_start[i] - expected_indices[i]) % 29
    print(f"  Position {i}: cipher={cipher_start[i]} - plain={expected_indices[i]} = key {needed} ({LETTERS[needed]})")

# Derive complete key from expected plaintext
print("\n" + "="*80)
print("If the plaintext is 'EPILOGUE WITHIN THE DEEP WEB...'")
print("="*80)
expected_full = "EPILOGUEWITHINTHEDEEPWEBTHERE"
exp_idx = []
i = 0
while i < len(expected_full):
    ch = expected_full[i]
    # Handle digraphs
    if i+1 < len(expected_full):
        dg = expected_full[i:i+2]
        if dg == 'TH':
            exp_idx.append(2); i += 2; continue
        elif dg == 'NG':
            exp_idx.append(21); i += 2; continue
        elif dg == 'EO':
            exp_idx.append(12); i += 2; continue
        elif dg == 'OE':
            exp_idx.append(22); i += 2; continue
        elif dg == 'EA':
            exp_idx.append(28); i += 2; continue
    # Single chars
    single_map = {'E':18,'P':13,'I':10,'L':20,'O':3,'G':6,'U':1,'W':7,'T':16,'H':8,'N':9,'D':23,'B':17,'R':4,'A':24,'X':14,'S':15}
    if ch in single_map:
        exp_idx.append(single_map[ch])
    i += 1

print(f"Expected: {expected_full}")
print(f"Indices: {exp_idx[:30]}")
print(f"Cipher:  {all_runes[:30]}")

# Derive key
derived_key = []
for i in range(min(30, len(exp_idx), len(all_runes))):
    k = (all_runes[i] - exp_idx[i]) % 29
    derived_key.append(k)
print(f"Derived key: {derived_key}")
print(f"As letters: {[LETTERS[k] for k in derived_key]}")

# Look for key pattern
print("\nLooking for repeating key pattern...")
for key_len in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
    matches = True
    for i in range(key_len, min(30, len(derived_key))):
        if derived_key[i] != derived_key[i % key_len]:
            matches = False
            break
    if matches:
        print(f"  Key length {key_len} might work: {derived_key[:key_len]}")

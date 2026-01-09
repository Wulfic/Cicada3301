#!/usr/bin/env python3
"""
Page 17 Autokey Analysis - Test if it's an autokey cipher
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

# Get cipher indices
cipher = [RUNE_MAP[c] for c in content if c in RUNE_MAP]
print(f"Cipher length: {len(cipher)}")

# Initial key YAHEOOPYJ = [26, 24, 8, 12, 3, 13, 26, 11]
SEED = [26, 24, 8, 12, 3, 13, 26, 11]

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

print("="*80)
print("Testing AUTOKEY cipher (plaintext extends key)")
print("="*80)

# Autokey: key = SEED + plaintext
# plaintext[i] = (cipher[i] - key[i]) mod 29
# where key[i] = SEED[i] for i < len(SEED), else plaintext[i - len(SEED)]

result = []
for i, c in enumerate(cipher):
    if i < len(SEED):
        k = SEED[i]
    else:
        k = result[i - len(SEED)]
    
    p = (c - k) % 29
    result.append(p)

text = indices_to_text(result)
print("Autokey (plaintext extends key, SUB):")
print(text[:200])

# Also try with key extending instead of plaintext
result2 = []
key = list(SEED)
for i, c in enumerate(cipher):
    k = key[i % len(key)]
    p = (c - k) % 29
    result2.append(p)
    if len(key) < len(cipher):
        key.append(p)  # Add plaintext to key

text2 = indices_to_text(result2)
print("\nAutokey variant (growing key, SUB):")
print(text2[:200])

# Try autokey with ciphertext extending key
result3 = []
for i, c in enumerate(cipher):
    if i < len(SEED):
        k = SEED[i]
    else:
        k = cipher[i - len(SEED)]  # Use CIPHERTEXT instead
    
    p = (c - k) % 29
    result3.append(p)

text3 = indices_to_text(result3)
print("\nAutokey (ciphertext extends key, SUB):")
print(text3[:200])

# Count 'THE' occurrences as quality metric
print(f"\nTHE count (autokey plain): {text.count('THE')}")
print(f"THE count (autokey cipher): {text3.count('THE')}")

# Try with word boundary handling
print("\n" + "="*80)
print("Testing with word boundary key reset")
print("="*80)

words_cipher = []
current = []
for char in content:
    if char in RUNE_MAP:
        current.append(RUNE_MAP[char])
    elif char == '•' or char == '\n':
        if current:
            words_cipher.append(current)
            current = []
if current:
    words_cipher.append(current)

# For autokey with word reset, the key resets at each word
# but still extends with plaintext within the word
result_words = []
for word in words_cipher:
    word_plain = []
    for i, c in enumerate(word):
        if i < len(SEED):
            k = SEED[i]
        else:
            k = word_plain[i - len(SEED)]
        p = (c - k) % 29
        word_plain.append(p)
    result_words.append(indices_to_text(word_plain))

print("Words (first 30):")
for i, w in enumerate(result_words[:30]):
    print(f"  {i}: {w}")

# Check if any known expected text appears
expected_words = ['EPILOGUE', 'WITHIN', 'THE', 'DEEP', 'WEB', 'THERE', 'EXISTS', 'PAGE', 'THAT', 'HASHES']
print("\nMatching expected words:")
for i, w in enumerate(result_words):
    if w in expected_words:
        print(f"  Word {i}: {w}")

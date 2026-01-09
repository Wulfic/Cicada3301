#!/usr/bin/env python3
"""Test the community-documented key for segment 0.5 (our page_00)"""

GEMATRIA = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᚣᛡᛠ'
LATIN_SIMPLE = 'FUTHORXGWHNIJEOPZSTBEMLNGDOAEYIO'

# Community-documented key: firfumferenfe (0,10,4,0,1,19,0,18,4,18,9,0,18)
key = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]

with open(r'C:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt', 'r', encoding='utf-8') as f:
    raw = f.read().replace('\n', '')
runes = [r for r in raw if r in GEMATRIA]
cipher_indices = [GEMATRIA.index(r) for r in runes]

print('=== Testing Community Key Variations ===')
print(f'Key: firfumferenfe = {key}')
print(f'Key length: {len(key)}')
print(f'Cipher length: {len(cipher_indices)}')
print()

def vig_decrypt_all(cipher, key):
    return [(c - key[i % len(key)]) % 29 for i, c in enumerate(cipher)]

def invert_gematria(indices):
    return [(28 - i) % 29 for i in indices]

# Test 1: Standard vigenere c-k
result1 = vig_decrypt_all(cipher_indices, key)
text1 = ''.join(LATIN_SIMPLE[i] for i in result1)
print('Test 1 - Vigenere (c-k):')
print(f'  {text1[:100]}')
print(f'  TH: {text1.count("TH")}, THE: {text1.count("THE")}')
print()

# Test 2: With inverted key
inv_key = [(29 - k) % 29 for k in key]
result2 = vig_decrypt_all(cipher_indices, inv_key)
text2 = ''.join(LATIN_SIMPLE[i] for i in result2)
print('Test 2 - Inverted key (c-invk):')
print(f'  {text2[:100]}')
print(f'  TH: {text2.count("TH")}, THE: {text2.count("THE")}')
print()

# Test 3: Decrypt then invert gematria (Atbash)
result3 = invert_gematria(result1)
text3 = ''.join(LATIN_SIMPLE[i] for i in result3)
print('Test 3 - Vig then Atbash:')
print(f'  {text3[:100]}')
print(f'  TH: {text3.count("TH")}, THE: {text3.count("THE")}')
print()

# Test 4: c+k (encryption direction)
result4 = [(c + key[i % len(key)]) % 29 for i, c in enumerate(cipher_indices)]
text4 = ''.join(LATIN_SIMPLE[i] for i in result4)
print('Test 4 - Reverse (c+k):')
print(f'  {text4[:100]}')
print(f'  TH: {text4.count("TH")}, THE: {text4.count("THE")}')
print()

# Test 5: F not encrypted rule - skip F in key position
def vig_f_skip(cipher, key):
    result = []
    key_pos = 0
    for c in cipher:
        if c == 0:  # F - not encrypted, output as-is
            result.append(c)
            # Don't advance key
        else:
            result.append((c - key[key_pos % len(key)]) % 29)
            key_pos += 1
    return result

result5 = vig_f_skip(cipher_indices, key)
text5 = ''.join(LATIN_SIMPLE[i] for i in result5)
print('Test 5 - F skip (documented rule):')
print(f'  {text5[:100]}')
print(f'  TH: {text5.count("TH")}, THE: {text5.count("THE")}')
print()

# Test 6: Maybe the key needs to be inverted AND the cipher operation reversed?
result6 = [(c + inv_key[i % len(key)]) % 29 for i, c in enumerate(cipher_indices)]
text6 = ''.join(LATIN_SIMPLE[i] for i in result6)
print('Test 6 - c+invk:')
print(f'  {text6[:100]}')
print(f'  TH: {text6.count("TH")}, THE: {text6.count("THE")}')
print()

# Summary
print('=== Best Results ===')
results = [
    ('c-k', text1),
    ('c-invk', text2),
    ('c-k+atbash', text3),
    ('c+k', text4),
    ('F-skip', text5),
    ('c+invk', text6),
]
for name, text in sorted(results, key=lambda x: x[1].count('THE'), reverse=True):
    print(f'{name}: TH={text.count("TH")}, THE={text.count("THE")}')

#!/usr/bin/env python3
"""
Verify Page 17 - Test all possible decryption methods to find if YAHEOOPYJ actually works
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

def runes_to_indices(text):
    return [RUNE_MAP[c] for c in text if c in RUNE_MAP]

def indices_to_eng(indices):
    return "".join([LETTERS[i] for i in indices])

def text_to_key(text):
    """Convert text to key indices"""
    LATIN_TO_IDX = {'F':0,'U':1,'V':1,'TH':2,'O':3,'R':4,'C':5,'K':5,'G':6,
                    'W':7,'H':8,'N':9,'I':10,'J':11,'EO':12,'P':13,'X':14,
                    'S':15,'T':16,'B':17,'E':18,'M':19,'L':20,'NG':21,'OE':22,
                    'D':23,'A':24,'AE':25,'Y':26,'IA':27,'IO':27,'EA':28,'Q':5,'Z':15}
    key = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_IDX:
                key.append(LATIN_TO_IDX[digraph])
                i += 2
                continue
        if text[i] in LATIN_TO_IDX:
            key.append(LATIN_TO_IDX[text[i]])
        i += 1
    return key

# Load Page 17
with open(r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_17\runes.txt', 'r', encoding='utf-8') as f:
    content = f.read()

cipher = runes_to_indices(content)
print(f"Page 17 has {len(cipher)} runes")

# Key YAHEOOPYJ 
# Y=26, A=24, H=8, E=18, O=3, O=3, P=13, Y=26, J=11
KEY = text_to_key('YAHEOOPYJ')
print(f"Key YAHEOOPYJ = {KEY}")

# Try all operations
print("\n" + "="*80)
print("Testing YAHEOOPYJ with different operations:")
print("="*80)

def decrypt(cipher, key, mode):
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'SUB':
            p = (c - k) % 29
        elif mode == 'ADD':
            p = (c + k) % 29
        elif mode == 'SUB_REV':
            p = (k - c) % 29
        elif mode == 'ADD_REV':
            p = (-c - k) % 29
        else:
            p = c
        result.append(p)
    return result

for mode in ['SUB', 'ADD', 'SUB_REV', 'ADD_REV']:
    result = decrypt(cipher, KEY, mode)
    text = indices_to_eng(result)
    
    # Check for "EPILOGUE" pattern
    has_epilogue = 'EPILOGUE' in text or 'EPIL' in text[:50]
    has_within = 'WITHIN' in text
    has_the = text.count('THE') > 5
    
    print(f"\n{mode}:")
    print(f"  First 100: {text[:100]}")
    print(f"  Has EPIL: {has_epilogue}, Has WITHIN: {has_within}, THE count: {text.count('THE')}")

# Try with reversed key
print("\n" + "="*80)
print("Testing with REVERSED key:")
print("="*80)

KEY_REV = KEY[::-1]
print(f"Key reversed = {KEY_REV}")

for mode in ['SUB', 'ADD', 'SUB_REV']:
    result = decrypt(cipher, KEY_REV, mode)
    text = indices_to_eng(result)
    print(f"\n{mode} (reversed key):")
    print(f"  First 100: {text[:100]}")

# Try other potential keys
print("\n" + "="*80)
print("Testing other thematic keys:")
print("="*80)

test_keys = {
    'EPILOGUE': text_to_key('EPILOGUE'),
    'DEEPWEB': text_to_key('DEEPWEB'),
    'ANEND': text_to_key('ANEND'),
    'DIVINITY': text_to_key('DIVINITY'),
    'CICADA': text_to_key('CICADA'),
    'FIRFUMFERENFE': text_to_key('FIRFUMFERENFE'),
}

for key_name, key in test_keys.items():
    for mode in ['SUB', 'ADD']:
        result = decrypt(cipher, key, mode)
        text = indices_to_eng(result)
        if text.count('THE') > 10 or 'WITHIN' in text or 'EPILOGUE' in text:
            print(f"\n{key_name} + {mode}:")
            print(f"  First 100: {text[:100]}")
            print(f"  THE count: {text.count('THE')}")

# Check for patterns without a key (maybe it's not Vigenère?)
print("\n" + "="*80)
print("Checking raw patterns:")
print("="*80)

# Raw runeglish
raw = indices_to_eng(cipher)
print(f"Raw (first 100): {raw[:100]}")
print(f"THE count (raw): {raw.count('THE')}")

# Try simple Caesar shifts
print("\nCaesar shifts with high THE count:")
for shift in range(29):
    result = [(c + shift) % 29 for c in cipher]
    text = indices_to_eng(result)
    if text.count('THE') > 15:
        print(f"  Shift +{shift}: THE={text.count('THE')}, preview: {text[:60]}")

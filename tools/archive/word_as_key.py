#!/usr/bin/env python3
"""
Test using the corresponding PARABLE word as secondary key for each page.
Pattern: Page N -> Word (N-20)
"""

import numpy as np

RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107, 109, 113]

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

PARABLE_WORDS = ['PARABLE', 'LICE', 'THE', 'INSTAR', 'TUNNELNG', 'TO', 'THE', 'SURFACE', 'WE', 'MUST', 
                 'SHED', 'OUR', 'OWN', 'CIRCUMFERENCES', 'FIND', 'THE', 'DIUINITY', 'WITHIN', 'AND', 'EMERGE']

def text_to_indices(text):
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        matched = False
        for length in [2, 1]:
            if i + length <= len(text):
                substr = text[i:i+length]
                if substr in RUNE_TO_IDX:
                    indices.append(RUNE_TO_IDX[substr])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return indices

def unicode_to_indices(text):
    return [RUNE_TO_IDX[RUNE_UNICODE[c]] for c in text if c in RUNE_UNICODE]

def indices_to_text(indices):
    return ''.join(RUNES[i % 29] for i in indices)

def score_english(text):
    vowels = set('AEIOU')
    score = sum(1 for c in text if c in vowels)
    for word in ['THE', 'AND', 'IS', 'TO', 'OF', 'IN', 'IT', 'FOR', 'AS', 'WITH', 'THIS', 'THAT', 
             'BE', 'ARE', 'WE', 'YOU', 'THEY', 'HAVE', 'FROM', 'OR', 'AN']:
        score += text.count(word) * len(word)
    return score

pages_raw = {
    27: 'ᚠᛇᚹᛄᚠᛋᚳᛁᛖᛡᛖᛚᛁᛈᛝᛗᚹᛝᛟᛞᛈᛡᛗᛡᛁᛄᛈᛁᛄᛠᚹᛚᛝᚳᛒᛡᛈᛏᚦᚦᛄᛒᛁᛈᚱᛠᛁᛟᚪᚫᛈᛄᛈᚩᛖᛁᛏᛁᚢᛗᚷᛁᚪᚾᚫᛁᛈᚳᛈᚩᛄᛗᛟᛝᛚᚷᚠᚳᛠᛈᚠᚷᛟᛠᛞᚩᛈᛄᚾᛁᚠᛋᚪᚱᚱ',
    28: 'ᛁᛋᛡᛖᛖᛝᛁᛄᚦᛝᚦᛟᛄᚳᚳᛁᚢᛏᛁᚦᛁᛗᛒᛁᛝᚣᛋᚳᛡᚱᛈᛄᛖᛈᛖᛁᚪᛝᛖᛈᚳᛁᛄᚦᛝᛞᛒᛏᚾᛄᚱᚢᛈᚢᛞᛏᚾᛄᛝᛟᛡᛡᛠᛞᚢᛖᚳᛁᛠᚦᛁᚳᛋᛞ',
    29: 'ᛠᛈᛈᛡᛁᚦᛟᚱᚻᚫᛏᛁᛠᚢᛖᚻᚠᛋᛈᛄᚾᚷᛚᛈᚠᛈᛟᛋᚾᛁᚪᛗᚠᚪᚢᚦᚪᚳᛁᚳᛈᛡᛁᛄᚱᚱᛈᛏᚱᚦᛈᛠᛄᚱᛁᛁᛝᚢᚻᛄᛗᛖᚳᛇ',
    30: 'ᚦᛝᛚᛟᛚᛏᛁᛚᛟᚣᚫᛡᛏᛡᚳᛟᛈᛈᛇᛠᛒᛋᛒᛈᚻᛄᛈᚳᚾᛠᛞᛏᛗᚳᛁᚾᛠᛝᛖᚠᚱᚫᚠᚣᛟᚢᛄᛚᚷᛖᛇᛋᚾᛏᛁᚫᚦᚾᛈᛈᛁᛁᛖᛋᛏ',
    31: 'ᛖᛝᚷᚦᛁᛖᛄᛠᚫᛋᛁᛗᛡᚪᛄᛖᛚᛋᚪᚦᚢᛋᛁᚷᚾᛝᛚᛟᛖᛖᛁᛇᛝᛄᛚᛟᚹᛁᛞᚾᛏᚫᚾᛠᛡᛁᚾᛋᛗᛡᛇᛈᛖᚦᛏᚢᛇᛟᛝᚳᚫᛒᚻᛋᛁᚩᛚᛚᛁᛝᚪᛗᛚᛋᛠᛠᚦ',
}

print('='*70)
print('THEORY: Use the corresponding WORD as a repeating secondary key')
print('Page N -> Word (N-20) as secondary key')
print('='*70)

for page_num, rune_text in pages_raw.items():
    word_num = page_num - 20
    if word_num >= len(PARABLE_WORDS):
        continue
    
    word = PARABLE_WORDS[word_num]
    word_key = text_to_indices(word)
    cipher = unicode_to_indices(rune_text)
    
    print(f'\nPage {page_num}: Using word "{word}" as secondary key')
    print(f'Word key indices: {word_key}')
    
    # Try: cipher - master_key - word_key (repeating)
    best_score = 0
    best_result = ''
    best_method = ''
    
    for key_offset in range(len(MASTER_KEY)):
        decrypted = []
        for i, c in enumerate(cipher):
            k = MASTER_KEY[(i + key_offset) % len(MASTER_KEY)]
            w = word_key[i % len(word_key)]
            d = (c - k - w) % 29
            decrypted.append(d)
        text = indices_to_text(decrypted)
        score = score_english(text)
        if score > best_score:
            best_score = score
            best_result = text
            best_method = f'key_off={key_offset}'
    
    print(f'Best with (cipher - key - word): score {best_score}, {best_method}')
    print(f'Text: {best_result[:70]}...')
    
    # Also try: cipher - master_key + word_key
    best_score2 = 0
    best_result2 = ''
    best_method2 = ''
    
    for key_offset in range(len(MASTER_KEY)):
        decrypted = []
        for i, c in enumerate(cipher):
            k = MASTER_KEY[(i + key_offset) % len(MASTER_KEY)]
            w = word_key[i % len(word_key)]
            d = (c - k + w) % 29
            decrypted.append(d)
        text = indices_to_text(decrypted)
        score = score_english(text)
        if score > best_score2:
            best_score2 = score
            best_result2 = text
            best_method2 = f'key_off={key_offset}'
    
    print(f'Best with (cipher - key + word): score {best_score2}, {best_method2}')
    print(f'Text: {best_result2[:70]}...')

# Now let's also check what happens if we use the page number relationship differently
print('\n' + '='*70)
print('EXPLORING: What if the offset IS the word number?')
print('='*70)

for page_num, rune_text in pages_raw.items():
    word_num = page_num - 20
    if word_num >= len(PARABLE_WORDS):
        continue
    
    word = PARABLE_WORDS[word_num]
    cipher = unicode_to_indices(rune_text)
    
    # Use word_num as key offset
    decrypted = []
    for i, c in enumerate(cipher):
        k = MASTER_KEY[(i + word_num) % len(MASTER_KEY)]
        d = (c - k) % 29
        decrypted.append(d)
    text = indices_to_text(decrypted)
    score = score_english(text)
    
    print(f'Page {page_num}: key_offset={word_num} (word "{word}")')
    print(f'  Score: {score}')
    print(f'  Text: {text[:70]}...')

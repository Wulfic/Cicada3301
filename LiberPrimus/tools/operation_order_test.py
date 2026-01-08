#!/usr/bin/env python3
"""
Test different operation orders on encryption
"""

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}
INDEX_TO_LETTER = {i: L for i, L in enumerate(LETTERS)}

RUNE_DATA = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛂ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER.get(i, '?') for i in indices)

def text_to_indices(text):
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        matched = False
        for length in [2, 1]:
            if i + length <= len(text):
                segment = text[i:i+length]
                if segment in LETTER_TO_INDEX:
                    indices.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return indices

# Read Page 2
with open(r'C:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_02\runes.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract words
words = []
current = []
pos = 0
for c in content:
    if c in RUNE_DATA:
        current.append((RUNE_DATA[c], pos))
        pos += 1
    elif c == '-' or c == '\n':
        if current:
            words.append(current)
            current = []
if current:
    words.append(current)

key_length = 83

print('Testing different operation orders on Page 2:')
print(f'Found {len(words)} words')
print()

test_keys = [
    ([10, 13], 'IP'),
    ([13, 10], 'PI'),
    (text_to_indices('WISDOM'), 'WISDOM'),
    (text_to_indices('PILGRIM'), 'PILGRIM'),
    (text_to_indices('SACRED'), 'SACRED'),
]

for word_key, name in test_keys:
    if not word_key:
        continue
        
    # Order 1: pos first, then word (standard)
    order1_words = []
    for word_data in words[:15]:
        result = []
        for rune_idx, rune_pos in word_data:
            after_pos = (rune_idx - (rune_pos % key_length)) % 29
            final = (after_pos + word_key[rune_pos % len(word_key)]) % 29
            result.append(final)
        order1_words.append(indices_to_text(result))
    
    # Order 2: word first, then pos
    order2_words = []
    for word_data in words[:15]:
        result = []
        for rune_idx, rune_pos in word_data:
            after_word = (rune_idx + word_key[rune_pos % len(word_key)]) % 29
            final = (after_word - (rune_pos % key_length)) % 29
            result.append(final)
        order2_words.append(indices_to_text(result))
    
    # Order 3: Just word key, no pos
    order3_words = []
    for word_data in words[:15]:
        result = []
        for i, (rune_idx, rune_pos) in enumerate(word_data):
            final = (rune_idx - word_key[i % len(word_key)]) % 29
            result.append(final)
        order3_words.append(indices_to_text(result))
    
    # Order 4: word key with word-local position (not global)
    order4_words = []
    for word_data in words[:15]:
        result = []
        for i, (rune_idx, rune_pos) in enumerate(word_data):
            # Subtract word key cycling within the word
            after_word = (rune_idx - word_key[i % len(word_key)]) % 29
            # Then subtract word-local position
            final = (after_word - i) % 29
            result.append(final)
        order4_words.append(indices_to_text(result))
    
    print(f'{name} key ({word_key}):')
    print(f'  Order 1 (pos-sub then word-add): ' + ' '.join(order1_words[:8]))
    print(f'  Order 2 (word-add then pos-sub): ' + ' '.join(order2_words[:8]))
    print(f'  Order 3 (word-sub only):         ' + ' '.join(order3_words[:8]))
    print(f'  Order 4 (word-sub then local-sub): ' + ' '.join(order4_words[:8]))
    print()

"""Test segment 0.5 headline with different cipher operations."""

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

# Single char mappings
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

key = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]
headline = 'ᛋᚻᛖᚩᚷᛗᛡᚠ'

print('Testing ᛋᚻᛖᚩᚷᛗᛡᚠ (0.5 headline):')
print('=' * 50)

# Method 1: (c + k) mod 29
print('\n(c + k) mod 29:')
result = []
for i, rune in enumerate(headline):
    idx = RUNE_TO_IDX[rune]
    k = key[i % len(key)]
    plain = (idx + k) % 29
    letter = IDX_TO_LETTER[plain]
    result.append(letter)
    print(f'  {rune}({idx}) + {k} = {plain} -> {letter}')
print(f'  Result: {".".join(result)}')

# Method 2: (c - k) mod 29
print('\n(c - k) mod 29:')
result = []
for i, rune in enumerate(headline):
    idx = RUNE_TO_IDX[rune]
    k = key[i % len(key)]
    plain = (idx - k) % 29
    letter = IDX_TO_LETTER[plain]
    result.append(letter)
    print(f'  {rune}({idx}) - {k} = {plain} -> {letter}')
print(f'  Result: {".".join(result)}')

# Method 3: With F-skip (skip F in key cycle) + add
print('\n(c + k) with F-skip:')
result = []
key_pos = 0
for rune in headline:
    idx = RUNE_TO_IDX[rune]
    if idx == 0:  # F - passthrough, don't advance key
        result.append('F')
        print(f'  {rune}({idx}) = F (passthrough)')
    else:
        k = key[key_pos % len(key)]
        plain = (idx + k) % 29
        letter = IDX_TO_LETTER[plain]
        result.append(letter)
        print(f'  {rune}({idx}) + {k} = {plain} -> {letter}')
        key_pos += 1
print(f'  Result: {".".join(result)}')

# Method 4: (c - k) with F-skip
print('\n(c - k) with F-skip:')
result = []
key_pos = 0
for rune in headline:
    idx = RUNE_TO_IDX[rune]
    if idx == 0:  # F - passthrough, don't advance key
        result.append('F')
        print(f'  {rune}({idx}) = F (passthrough)')
    else:
        k = key[key_pos % len(key)]
        plain = (idx - k) % 29
        letter = IDX_TO_LETTER[plain]
        result.append(letter)
        print(f'  {rune}({idx}) - {k} = {plain} -> {letter}')
        key_pos += 1
print(f'  Result: {".".join(result)}')

# Method 5: Invert first, then (c - k) with F-skip
print('\nInvert Gematria + (c - k) with F-skip:')
result = []
key_pos = 0
for rune in headline:
    idx = RUNE_TO_IDX[rune]
    inverted = (28 - idx) % 29  # Invert first
    if inverted == 0:  # F - passthrough
        result.append('F')
        print(f'  {rune}({idx}) -> inv({inverted}) = F (passthrough)')
    else:
        k = key[key_pos % len(key)]
        plain = (inverted - k) % 29
        letter = IDX_TO_LETTER[plain]
        result.append(letter)
        print(f'  {rune}({idx}) -> inv({inverted}) - {k} = {plain} -> {letter}')
        key_pos += 1
print(f'  Result: {".".join(result)}')

# Method 6: (c - k) then invert
print('\n(c - k) with F-skip then Invert:')
result = []
key_pos = 0
for rune in headline:
    idx = RUNE_TO_IDX[rune]
    if idx == 0:  # F - passthrough
        result.append('F')
        print(f'  {rune}({idx}) = F (passthrough)')
    else:
        k = key[key_pos % len(key)]
        intermediate = (idx - k) % 29
        plain = (28 - intermediate) % 29
        letter = IDX_TO_LETTER[plain]
        result.append(letter)
        print(f'  {rune}({idx}) - {k} = {intermediate} -> inv({plain}) -> {letter}')
        key_pos += 1
print(f'  Result: {".".join(result)}')

# What about trying "CIRCUMFERENCE" as expected answer?
print('\n' + '=' * 50)
print('Expected answer might be "CIRCUMFERENCE"')
print('C.I.R.C.U.M.F.E.R.E.N.C.E')
print()
print('Checking if headline can decrypt to CIRCUMFERENCE...')
headline_runes = list(headline)  # ['ᛋ','ᚻ','ᛖ','ᚩ','ᚷ','ᛗ','ᛡ','ᚠ']
expected = ['C','I','R','C','U','M','F','E','R','E','N','C','E']

# The headline is 8 runes, but CIRCUMFERENCE is 13 letters
# BUT with digraphs: C-I-R-C-U-M-F-E-R-E-N-C-E could be 13 letters = 13 indices
# Wait, headline is only 8 runes - so expected plaintext is 8 elements max

# What's the expected for each rune position to spell something?
# Let's see what key would make each position spell common letters
print('\nReverse engineering - what key makes each position spell useful letters:')
for i, rune in enumerate(headline_runes):
    idx = RUNE_TO_IDX[rune]
    print(f'{rune} (idx={idx}):')
    # Try to make it spell C, I, R, etc
    for target_letter in ['C', 'I', 'R', 'U', 'M', 'F', 'E', 'N', 'S', 'H', 'A', 'O', 'T']:
        for ti, letter in enumerate(IDX_TO_LETTER):
            if letter == target_letter:
                needed_key = (idx - ti) % 29
                print(f'  To get {target_letter} (idx={ti}): key = {needed_key}')
                break

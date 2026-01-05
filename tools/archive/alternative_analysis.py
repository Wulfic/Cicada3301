#!/usr/bin/env python3
"""
Alternative interpretation: The numbers 7, 5, 4 in positions indicate something special.
Also trying the cipher as groups rearranged rather than character transposition.
"""

from itertools import permutations
from collections import Counter

# Original groups
GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
          'UIMNI', 'TELNJ', '7TFYV', 'OIUAU', 'SNOCO', '5JI4M', 'EODZZ']

# Groups without numbers
CLEAN_GROUPS = ['IDGTK', 'UMLOO', 'ARWOE', 'RTHIS', 'UTETL', 'HUTIA', 'TSLLO', 
                'UIMNI', 'TELNJ', 'TFYV', 'OIUAU', 'SNOCO', 'JIM', 'EODZZ']

# Just the letters
CIPHER_LETTERS = "IDGTKUMLOOARWOERTHISUTETLHUTIATSLLOUIMNITELNJTFYVOIUAUSNOCOJIMEODZZ"

# Known Cicada text for comparison
PARABLE = "LIKETHEINSTARTUNNELINGTOTHESURFACEWEMUSTSHEDO UROWNCIRCUMFERENCESFINDTHEDIVINITYWITHINANDEMERGE"

CICADA_WORDS = ['THE', 'UNTO', 'INITIATED', 'LIKE', 'INSTAR', 'TUNNELING', 'SURFACE',
                'MUST', 'SHED', 'OUR', 'OWN', 'CIRCUMFERENCE', 'FIND', 'DIVINITY',
                'WITHIN', 'EMERGE', 'TRUTH', 'SEEK', 'AND', 'THIS', 'KEY', 'YOU']

def score_text(text):
    score = 0
    for word in CICADA_WORDS:
        if word in text:
            score += len(word) * 50
    return score

print("="*70)
print("ALTERNATIVE CIPHER ANALYSIS")
print("="*70)

# ============================================================
# Hypothesis 1: The groups themselves are scrambled
# ============================================================
print("\n" + "="*50)
print("TESTING GROUP PERMUTATIONS")
print("="*50)

# The numbers appear in groups 10 (7TFYV) and 13 (5JI4M)
# 7, 5, 4 could indicate: 
#   - Group positions to read first: groups 7, 5, 4
#   - Or group 10 should be at position 7, group 13 should be at positions 5 and 4

# Reading specific columns from the 14x5 grid
print("\nReading columns from 14x5 grid:")
for col_order in [
    [0,1,2,3,4],  # Normal
    [4,3,2,1,0],  # Reverse
    [6,4,3,0,1,2,5,7,8,9,10,11,12,13],  # 7,5,4 positions first (0-indexed: 6,4,3)
]:
    # Interpret column-first reading
    result = ''
    for col in col_order[:5]:  # Read just first 5 as columns
        for row in range(14):
            if col < 5:
                result += GROUPS[row][col] if row < len(GROUPS) and col < len(GROUPS[row]) else ''
    print(f"  Order {col_order[:5]}: {result[:40]}... (score={score_text(result)})")

# ============================================================
# Hypothesis 2: The 7, 5, 4 tell us HOW to read
# ============================================================
print("\n" + "="*50)
print("TESTING 7-5-4 AS READING INSTRUCTIONS")
print("="*50)

# Perhaps: read 7 chars, skip to position 5, read 4 chars, etc.?
# Or: read every 7th, then every 5th, then every 4th?

print("\nReading every Nth character:")
for n in [7, 5, 4, 3]:
    chars = [CIPHER_LETTERS[i] for i in range(0, len(CIPHER_LETTERS), n)]
    result = ''.join(chars)
    print(f"  Every {n}th: {result}")

print("\nCombined: 7th + 5th + 4th positions:")
result = ''
for i in range(0, len(CIPHER_LETTERS), 7):
    if i < len(CIPHER_LETTERS):
        result += CIPHER_LETTERS[i]
for i in range(0, len(CIPHER_LETTERS), 5):
    if i < len(CIPHER_LETTERS):
        result += CIPHER_LETTERS[i]
for i in range(0, len(CIPHER_LETTERS), 4):
    if i < len(CIPHER_LETTERS):
        result += CIPHER_LETTERS[i]
print(f"  Combined: {result}")

# ============================================================
# Hypothesis 3: Read with key [7,5,4,1,2,3,6]
# ============================================================
print("\n" + "="*50)
print("TESTING COLUMNAR WITH [7,5,4] BASED KEYS")
print("="*50)

def columnar_decrypt(text, key):
    """Decrypt columnar transposition."""
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    full_cols = len(text) % num_cols
    if full_cols == 0:
        full_cols = num_cols
    
    # Column lengths based on key order
    col_order = sorted(range(num_cols), key=lambda x: key[x])
    col_lengths = {}
    for i, col in enumerate(col_order):
        col_lengths[col] = num_rows if i < full_cols else num_rows - 1
    
    # Fill columns
    columns = {}
    idx = 0
    for col in col_order:
        length = col_lengths[col]
        columns[col] = text[idx:idx+length]
        idx += length
    
    # Read row by row
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(columns.get(col, '')):
                result.append(columns[col][row])
    
    return ''.join(result)

# Try various 7-column keys with 7,5,4 as significant values
keys_to_try = [
    [1, 2, 3, 4, 5, 6, 7],  # Base
    [7, 5, 4, 1, 2, 3, 6],  # 7,5,4 first
    [4, 5, 7, 1, 2, 3, 6],  # 4,5,7 first
    [1, 2, 3, 4, 7, 5, 6],  # 7,5 at end positions
    [3, 5, 7, 1, 2, 4, 6],  # Interleaved
    [7, 6, 5, 4, 3, 2, 1],  # Reverse
    [5, 7, 4, 1, 2, 3, 6],  # 5,7,4 first
]

for key in keys_to_try:
    result = columnar_decrypt(CIPHER_LETTERS, key)
    s = score_text(result)
    if s > 0 or True:
        print(f"  Key {key}: {result[:40]}... (score={s})")

# ============================================================
# Hypothesis 4: The numbers mark WHERE to start reading
# ============================================================
print("\n" + "="*50)
print("READING FROM MARKED POSITIONS")
print("="*50)

# Numbers are at positions: 7 at pos 45, 5 at pos 60, 4 at pos 63
# Try reading from those positions
full_cipher = ''.join(GROUPS)
pos_7 = full_cipher.find('7')  # 45
pos_5 = full_cipher.find('5')  # 60
pos_4 = full_cipher.find('4')  # 63

print(f"Positions: 7={pos_7}, 5={pos_5}, 4={pos_4}")

# Reading starting from these positions
for start_pos in [45, 60, 63]:
    # Wrap around
    result = full_cipher[start_pos:] + full_cipher[:start_pos]
    result = result.replace('7', '').replace('5', '').replace('4', '')
    print(f"  From pos {start_pos}: {result[:40]}...")

# ============================================================
# Hypothesis 5: Groups 10 and 13 are special
# ============================================================
print("\n" + "="*50)
print("GROUPS 10 AND 13 AS KEYS")
print("="*50)

# 7TFYV and 5JI4M contain the numbers
# Maybe TFYV and JIM are meaningful?

print("Group 10 letters: TFYV")
print("Group 13 letters: JIM")
print("Combined: TFYVJIM")

# Use these as key for columnar?
def keyword_to_order(keyword):
    """Convert keyword to numeric order."""
    chars = [(c, i) for i, c in enumerate(keyword)]
    sorted_chars = sorted(chars)
    return [i for c, i in sorted(sorted_chars, key=lambda x: (x[0], x[1]))]

for kw in ['TFYVJIM', 'JIMTFYV', 'DIVINITY', 'PRIMUS', 'CICADA', 'TRUTH']:
    order = keyword_to_order(kw)
    result = columnar_decrypt(CIPHER_LETTERS, [x+1 for x in order])
    print(f"  {kw}: {result[:40]}... (score={score_text(result)})")

# ============================================================
# Hypothesis 6: Read groups in prime order
# ============================================================
print("\n" + "="*50)
print("READING GROUPS IN PRIME ORDER")  
print("="*50)

primes = [2, 3, 5, 7, 11, 13]  # 1-indexed group positions

# Read groups at prime positions (groups 2,3,5,7,11,13 = indices 1,2,4,6,10,12)
prime_indices = [1, 2, 4, 6, 10, 12]
non_prime_indices = [i for i in range(14) if i not in prime_indices]

result_prime = ''.join(CLEAN_GROUPS[i] for i in prime_indices)
result_non = ''.join(CLEAN_GROUPS[i] for i in non_prime_indices)
print(f"Prime groups: {result_prime}")
print(f"Non-prime groups: {result_non}")
print(f"Prime then non: {result_prime + result_non}")

# ============================================================
# Hypothesis 7: Each group is internally scrambled
# ============================================================
print("\n" + "="*50)
print("UNSCRAMBLING INDIVIDUAL GROUPS")
print("="*50)

# What if each 5-letter group is an anagram?
# IDGTK -> ? UMLOO -> ? ARWOE -> ? RTHIS -> THIS R

print("Possible anagrams for each group:")
import itertools

for i, group in enumerate(CLEAN_GROUPS[:6]):  # Check first 6
    perms = [''.join(p) for p in itertools.permutations(group)]
    # Look for English words
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                    'THIS', 'THAT', 'WITH', 'INTO', 'UNTO', 'LIKE', 'MUST',
                    'GOOD', 'LOOK', 'WOOL', 'ROOM', 'TOOL', 'LOOP', 'POOL']
    for perm in perms:
        for word in common_words:
            if word in perm:
                print(f"  Group {i+1} ({group}) -> {perm} contains '{word}'")
                break

# UMLOO could be LLOOM, MOOLU, etc - or contain "LOO"
# Check what real words can be formed
print("\nLooking for word matches in scrambled groups...")
all_words = set(['THIS', 'UNTO', 'THE', 'LIKE', 'AND', 'INTO', 'LOOK', 'TOOL',
                'WOOL', 'LOOP', 'POOL', 'ROOM', 'MOOT', 'ROOT', 'HOOT', 'LOOT',
                'MUTE', 'TALL', 'TALL', 'HULL', 'ALSO', 'ELSE', 'SLIM', 'JAIL'])

for i, group in enumerate(CLEAN_GROUPS):
    letters = sorted(group)
    letters_str = ''.join(letters)
    matches = []
    for word in all_words:
        if sorted(word) == sorted(group)[:len(word)]:
            matches.append(word)
    if matches:
        print(f"  {group}: possible words {matches}")

# ============================================================
# The actual discovered text breakdown
# ============================================================
print("\n" + "="*50)
print("LETTER INVENTORY ANALYSIS")
print("="*50)

our_letters = Counter(CIPHER_LETTERS)
print(f"Our 67 letters: {dict(sorted(our_letters.items()))}")

# What 67-character message could this be?
# Known parable is longer (105 chars)
# But we could have part of it

# "UNTO THE INITIATED" = 16 letters
# Remaining after that = 51 letters

test = "UNTOTHEINITIATEDLIKETHEINSTARYOUMUSTSEEK"  # 41 chars
test_count = Counter(test)
print(f"\nTest phrase '{test}':")
print(f"  Length: {len(test)}")
print(f"  Matches: {all(our_letters.get(c, 0) >= test_count[c] for c in test_count)}")

# What's the difference?
missing = []
for c in test_count:
    if our_letters.get(c, 0) < test_count[c]:
        missing.append(f"{c}({test_count[c] - our_letters.get(c, 0)})")
if missing:
    print(f"  Missing: {', '.join(missing)}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
Key findings:
- The cipher has 67 letters (plus 3 numbers: 7, 5, 4)
- "THIS" is clearly visible in RTHIS
- Can form "UNTO THE INITIATED" and "LIKE THE INSTAR" from letters
- Numbers 7, 5, 4 appear to be positional markers

Most promising theories:
1. Columnar transposition with prime-based key
2. Groups need to be reordered before reading
3. Numbers indicate start position or column order

Next: Try more systematic keyword-based decryption
""")

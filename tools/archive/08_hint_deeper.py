"""
08.JPG HINT - DEEPER ANALYSIS
==============================

Line 1: TL BE IE OV UT HT RE ID TS EO ST PO SO YR
Line 2: SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M

Key observations:
1. II = 666 in base-36 (Number of the Beast)
2. Line 1 uses only letters
3. Line 2 has numbers mixed in
4. There are exactly 14 pairs (7 + 7?)

Let's see if Line 1 spells something when read differently...
"""

line1 = ['TL', 'BE', 'IE', 'OV', 'UT', 'HT', 'RE', 'ID', 'TS', 'EO', 'ST', 'PO', 'SO', 'YR']
line2 = ['SL', 'BT', 'II', 'IY', 'T4', 'DG', 'UQ', 'IM', 'NU', '44', '2I', '15', '33', '9M']

print("Reading first letters of Line 1:", ''.join(p[0] for p in line1))
print("Reading second letters of Line 1:", ''.join(p[1] for p in line1))
print()

# Full concatenation
full_line1 = ''.join(line1)
print(f"Full Line 1: {full_line1}")
print(f"Length: {len(full_line1)}")
print()

# Looking for words
# TLBEIEOVUTHTREIDTSEOSTPOSOYR
# Let's try to find English words in it
words = ['THE', 'BE', 'OBEY', 'OR', 'OUT', 'HER', 'ID', 'IT', 'TO', 'SO', 'PO', 'YR', 'REST', 'POST', 
         'POSE', 'STORY', 'STORE', 'SORT', 'RESORT', 'BEST', 'TEST', 'OVER', 'OVER', 'UTTER']

print("Searching for words in Line 1 concatenation:")
for word in words:
    if word in full_line1:
        idx = full_line1.find(word)
        print(f"  '{word}' at position {idx}")

# Reading pairs as letter+letter combinations
print()
print("Reading Line 1 as bigrams (Anglo-Saxon):")
# TL = T + L
# BE = B + E 
# etc.

# But wait - in Gematria Primus:
# TL could indicate T at position L (16 at position 20)?
# Or T shifted by L?

print()
print("What if pairs indicate shifts?")
print("Each pair XY means: apply shift Y to rune X")
print("Or: swap runes at positions X and Y")
print()

# Anglo-Saxon to index
RUNE_POSITIONS = {'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 
                  'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 
                  'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 
                  'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28}

# Single letter to index
LETTER_TO_IDX = {
    'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
    'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26
}

print("Line 1 as position pairs:")
for p in line1:
    if len(p) == 2 and p[0] in LETTER_TO_IDX and p[1] in LETTER_TO_IDX:
        idx1 = LETTER_TO_IDX[p[0]]
        idx2 = LETTER_TO_IDX[p[1]]
        print(f"  {p}: ({idx1}, {idx2}) -> diff = {(idx2 - idx1) % 29}, sum = {(idx1 + idx2) % 29}")

print()
print("=" * 70)
print("INTERPRETING AS A SUBSTITUTION CIPHER KEY")
print("=" * 70)
print()
print("Line 1 (original) -> Line 2 (encrypted)")
print("This could be showing us how the cipher transforms letters:")

substitutions = {}
for p1, p2 in zip(line1, line2):
    # Get only alphabetic parts
    p2_alpha = ''.join(c for c in p2 if c.isalpha())
    if p2_alpha:
        substitutions[p1] = p2_alpha
        print(f"  {p1} becomes {p2_alpha}")

print()
print("=" * 70)
print("TESTING: ANAGRAM ANALYSIS")
print("=" * 70)
print()

# What if Line 1 is an anagram?
# TLBEIEOVUTHTREIDTSEOSTPOSOYR
first_letters = ''.join(p[0] for p in line1)
second_letters = ''.join(p[1] for p in line1)
print(f"First letters: {first_letters} (sorted: {''.join(sorted(first_letters))})")
print(f"Second letters: {second_letters} (sorted: {''.join(sorted(second_letters))})")
print(f"All together: {''.join(sorted(full_line1))}")

# Count letters
from collections import Counter
letter_counts = Counter(full_line1)
print(f"Letter frequency: {dict(letter_counts)}")

# Common anagrams?
# Could this be "THE DESTROYER" + something?
# Or "OUTSIDE" + "POETRY"?

print()
print("=" * 70)
print("THE SOLUTION HINT")
print("=" * 70)
print("""
The hint says "For those who have fallen behind" - this is explicitly
for people stuck on the unsolved pages.

Key insight: Line 1 contains only letter pairs that could represent
RUNE PAIRS (digraphs) in Anglo-Saxon:
- TH is a rune
- EO is a rune  
- ST could be S+T

Line 2 has anomalies:
- II = 666 (significant!)
- Numbers mixed in: T4, 44, 2I, 15, 33, 9M

The numbers might indicate:
1. Position offsets
2. Reading sequence  
3. Key modifications

Let me extract just the numeric parts from Line 2:
""")

# Extract numbers from line 2
numeric_parts = []
for p in line2:
    nums = ''.join(c for c in p if c.isdigit())
    if nums:
        numeric_parts.append((p, int(nums) if nums else 0))
        print(f"  {p} contains number: {nums}")

print()
print("Purely numeric values in Line 2:", [p for p in line2 if any(c.isdigit() for c in p)])

# These numbers: 4, 44, 2, 15, 33, 9
# 4 + 44 + 2 + 15 + 33 + 9 = 107 (prime!)
print()
print("Sum of numbers: 4 + 44 + 2 + 15 + 33 + 9 =", 4 + 44 + 2 + 15 + 33 + 9)
print("107 is prime! And 107 is the Gematria value of IA (rune 27)")

# Maybe these are specific rune positions to pay attention to?
print()
print("Positions 4, 44, 2, 15, 33, 9 in the text could be key positions")
print("Or these could be modular shifts")

# Test reading Line 1 at specific intervals
print()
print("Reading Line 1 at intervals:")
for interval in [2, 3, 4, 5, 6, 7]:
    result = full_line1[::interval]
    print(f"  Every {interval}th letter: {result}")

# Reverse?
print()
print(f"Line 1 reversed: {full_line1[::-1]}")

# What about reading alternate letters?
print()
print("Odd positions:", full_line1[0::2])
print("Even positions:", full_line1[1::2])

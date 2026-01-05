"""
EXPLORING THE BEST COMBINATIONS
================================

Best results so far:
- Page 27 Standard + Parable: 34
- Page 30 Parable as key: 32
- Page 29 Parable as key: 28

Let's explore these more deeply!
"""

import numpy as np
from collections import Counter

# Parable text (from Page 57)
PARABLE_TEXT = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

# Anglo-Saxon Futhorc
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
         'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
         'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
LETTER_TO_IDX = {l: i for i, l in enumerate(LATIN)}

# Also single letter mappings
SINGLE_LETTER_MAP = {
    'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
    'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26
}

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

MASTER_KEY = np.array([
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
], dtype=np.int32)

UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
}

def indices_to_text(indices):
    return ''.join(LATIN[i % 29] for i in indices)

def word_score(text):
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE', 'MUST',
             'SURFACE', 'TUNNEL', 'EMERGE', 'CIRCUMFERENCE', 'SHED', 'OWN', 'BECOME', 'FIND',
             'EACH', 'HAVE', 'HAS', 'MORE', 'THAN', 'WHEN', 'WHERE', 'WHAT', 'HOW', 'WHO',
             'WAR', 'CONSUME', 'LOSS', 'ILLUSION', 'REALITY', 'BELIEF', 'FAITH', 'KNOW',
             'SOME', 'ANY', 'MANY', 'FEW', 'LITTLE', 'MUCH', 'OTHER', 'ANOTHER', 'EACH',
             'SUCH', 'SAME', 'SELF', 'ONLY', 'THING', 'THINGS', 'WAY', 'WAYS', 'TIME',
             'PLACE', 'WORLD', 'LIFE', 'DEATH', 'MAN', 'MEN', 'MIND', 'BODY', 'SOUL',
             'SPIRIT', 'HEART', 'LOVE', 'HATE', 'FEAR', 'HOPE', 'GOOD', 'EVIL', 'LIGHT',
             'DARK', 'TRUE', 'FALSE', 'SEEK', 'SEE', 'HEAR', 'SPEAK', 'THINK', 'FEEL']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        score += text_upper.count(word) * len(word)
    return score

# Convert Parable text to indices
def text_to_key(text):
    key = []
    i = 0
    while i < len(text):
        # Check for digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_IDX:
                key.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        # Single letter
        if text[i] in SINGLE_LETTER_MAP:
            key.append(SINGLE_LETTER_MAP[text[i]])
        i += 1
    return np.array(key, dtype=np.int32)

parable_key = text_to_key(PARABLE_TEXT)

print("=" * 70)
print("EXPLORING PAGE 27 (Standard + Parable score 34)")
print("=" * 70)

page_data = UNSOLVED_PAGES[27]
pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
n = len(pg_idx)

# Extend keys
key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
parable_ext = np.tile(parable_key, (n // len(parable_key)) + 1)[:n]

# Standard + Parable
decrypted = (pg_idx - key_ext - parable_ext) % 29
text = indices_to_text(decrypted)
print(f"Standard + Parable key:")
print(f"  Score: {word_score(text)}")
print(f"  Full text: {text}")
print()

# Try variations
print("Testing variations:")
for shift1 in range(0, 30, 5):
    for shift2 in range(0, 30, 5):
        mod_key = np.roll(MASTER_KEY, shift1)
        mod_parable = np.roll(parable_key, shift2)
        key_ext = np.tile(mod_key, (n // len(mod_key)) + 1)[:n]
        parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
        decrypted = (pg_idx - key_ext - parable_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 35:
            print(f"  Key shift {shift1}, Parable shift {shift2}: score {score}")
            print(f"    {text[:70]}...")

print()
print("=" * 70)
print("EXPLORING PAGE 30 (Parable as key score 32)")
print("=" * 70)

page_data = UNSOLVED_PAGES[30]
pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
n = len(pg_idx)

parable_ext = np.tile(parable_key, (n // len(parable_key)) + 1)[:n]

# Parable as key
decrypted = (pg_idx - parable_ext) % 29
text = indices_to_text(decrypted)
print(f"Parable as key:")
print(f"  Score: {word_score(text)}")
print(f"  Full text: {text}")
print()

# Look for word patterns
print("Potential word boundaries:")
# Common 3+ letter patterns
for i in range(len(text) - 2):
    if text[i:i+3] in ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'ALL', 'CAN', 'HER', 'WAS', 'ONE']:
        print(f"  Found '{text[i:i+3]}' at position {i}")
    if i < len(text) - 3:
        if text[i:i+4] in ['THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'THEY', 'FROM', 'BEEN']:
            print(f"  Found '{text[i:i+4]}' at position {i}")

# Try parable shifted by page number
print("\nTrying Parable shifted by various amounts:")
best_shift = (0, 0, "")
for shift in range(95):
    mod_parable = np.roll(parable_key, -shift)
    parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
    decrypted = (pg_idx - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    if score > best_shift[0]:
        best_shift = (score, shift, text)

print(f"Best: shift {best_shift[1]} with score {best_shift[0]}")
print(f"  {best_shift[2][:70]}...")

print()
print("=" * 70)
print("THE KEY INSIGHT: DOUBLE KEYING")
print("=" * 70)
print("""
The hint mentions "words are the map" and "numbers are the direction".

What if:
1. First layer: Standard Vigenère with Master Key (the "map")
2. Second layer: Use Parable's Gematria values as "direction"

The Parable provides MEANING (the road) through its Gematria NUMBERS (direction).
""")

# Get Gematria values for parable
parable_gematria = np.array([GEMATRIA[i] for i in parable_key])

for pg_num in [27, 28, 29, 30, 31]:
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    gematria_ext = np.tile(parable_gematria, (n // len(parable_gematria)) + 1)[:n]
    
    # First apply master key, then add gematria
    decrypted1 = (pg_idx - key_ext) % 29
    decrypted2 = (decrypted1 - (gematria_ext % 29)) % 29
    text = indices_to_text(decrypted2)
    score = word_score(text)
    
    print(f"Page {pg_num}: Master Key then Parable Gematria mod 29: score {score}")
    if score > 30:
        print(f"  {text[:70]}...")
    
    # Try Gematria first, then master key
    decrypted1 = (pg_idx - (gematria_ext % 29)) % 29
    decrypted2 = (decrypted1 - key_ext) % 29
    text = indices_to_text(decrypted2)
    score = word_score(text)
    
    print(f"Page {pg_num}: Parable Gematria then Master Key: score {score}")
    if score > 30:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("TESTING: Maybe each unsolved page uses the NEXT page's content as key?")
print("=" * 70)

# What if page 27 uses page 28 as key? Page 28 uses page 29 as key? etc.
# This would be "forward looking"

for pg_num in [27, 28, 29, 30]:
    next_pg = pg_num + 1
    if next_pg in UNSOLVED_PAGES:
        page_data = UNSOLVED_PAGES[pg_num]
        next_page_data = UNSOLVED_PAGES[next_pg]
        
        pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
        next_idx = np.array([RUNE_TO_INDEX[r] for r in next_page_data])
        
        n = len(pg_idx)
        next_ext = np.tile(next_idx, (n // len(next_idx)) + 1)[:n]
        
        # XOR with next page
        decrypted = (pg_idx - next_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        print(f"Page {pg_num} XOR with Page {next_pg}: score {score}")
        if score > 25:
            print(f"  {text[:70]}...")

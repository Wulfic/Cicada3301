"""
RUNNING KEY CIPHER WITH PARABLE
================================

The Parable is clearly significant - it's on Page 57 (plaintext) and encrypted on Pages 0 & 54.
What if the unsolved pages use the Parable TEXT itself as a running key?

"Its words are the map, their meaning is the road, and their NUMBERS are the direction."

The Parable text could provide:
1. A running key (Vigenère style)
2. A reading order (based on Gematria values)
3. Position markers
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
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
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
             'WAR', 'CONSUME', 'LOSS', 'ILLUSION', 'REALITY', 'BELIEF', 'FAITH', 'KNOW']
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
print(f"Parable as key: {len(parable_key)} indices")
print(f"First 20 values: {parable_key[:20]}")
print(f"Sum: {sum(parable_key)}, Sum mod 29: {sum(parable_key) % 29}")
print()

print("=" * 70)
print("TESTING PARABLE AS RUNNING KEY")
print("=" * 70)

for pg_num in sorted(UNSOLVED_PAGES.keys()):
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    # Extend parable key to match page length
    parable_ext = np.tile(parable_key, (n // len(parable_key)) + 1)[:n]
    
    print(f"\nPage {pg_num} ({n} runes):")
    
    # 1. Standard key
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    decrypted = (pg_idx - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"  Standard key: score {score}")
    
    # 2. Parable as key
    decrypted = (pg_idx - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"  Parable as key: score {score}")
    if score > 20:
        print(f"    {text[:60]}...")
    
    # 3. Standard key + Parable (double key)
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"  Standard + Parable: score {score}")
    if score > 20:
        print(f"    {text[:60]}...")
    
    # 4. Standard key XOR Parable positions
    combined_key = (key_ext ^ parable_ext) % 29
    decrypted = (pg_idx - combined_key) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"  Standard XOR Parable: score {score}")
    if score > 20:
        print(f"    {text[:60]}...")
    
    # 5. Parable shifted by page number
    parable_shifted = np.roll(parable_key, pg_num)
    parable_shifted_ext = np.tile(parable_shifted, (n // len(parable_shifted)) + 1)[:n]
    decrypted = (pg_idx - parable_shifted_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"  Parable shifted by {pg_num}: score {score}")
    if score > 20:
        print(f"    {text[:60]}...")

print()
print("=" * 70)
print("TESTING PARABLE GEMATRIA AS READING ORDER")
print("=" * 70)

# Get Gematria values for parable
parable_gematria = [GEMATRIA[i] for i in parable_key]
print(f"Parable Gematria sum: {sum(parable_gematria)}")
print(f"First 20 Gematria values: {parable_gematria[:20]}")

# The hint says "NUMBERS are the direction"
# Maybe the Parable's Gematria values tell us the reading order?

for pg_num in [27, 28, 29, 30, 31]:
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    print(f"\nPage {pg_num}:")
    
    # Use Parable Gematria mod n as reading order
    reading_order = [g % n for g in parable_gematria[:n]]
    
    # Make sure we have unique positions
    # Actually, use cumulative sum mod n
    cumsum = np.cumsum(parable_gematria[:n]) % n
    
    result = pg_idx[cumsum]
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    decrypted = (result - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"  Parable Gematria cumsum as index + key: score {score}")
    if score > 30:
        print(f"    {text[:60]}...")

print()
print("=" * 70)
print("TESTING THE FORMULA: Page Number as Parable Index Offset")  
print("=" * 70)

# Maybe each page starts from a different position in the Parable key?
# Specifically, starting at position (page_number % 95) in the master key?

for pg_num in sorted(UNSOLVED_PAGES.keys()):
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    # Start key at position page_num mod 95
    start_pos = pg_num % 95
    shifted_key = np.roll(MASTER_KEY, -start_pos)
    key_ext = np.tile(shifted_key, (n // len(shifted_key)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    if score > 30:
        print(f"Page {pg_num} with key offset {start_pos}: score {score}")
        print(f"  {text[:60]}...")

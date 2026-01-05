"""
NUMBERS ARE THE DIRECTION
=========================

The 2016 clue says: "Its words are the map, their meaning is the road, 
and their NUMBERS are the direction."

What if the GEMATRIA VALUES of the Parable tell us HOW to apply the key?
"""

import numpy as np

# Parable text (from Page 57)
PARABLE_TEXT = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

# Anglo-Saxon Futhorc
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
         'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
         'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107, 109, 113]
LETTER_TO_IDX = {l: i for i, l in enumerate(LATIN)}

SINGLE_LETTER_MAP = {
    'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
    'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26
}

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
             'EACH', 'HAVE', 'HAS', 'MORE', 'THAN', 'WHEN', 'WHERE', 'WHAT', 'HOW', 'WHO']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        score += text_upper.count(word) * len(word)
    return score

def text_to_key(text):
    key = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_IDX:
                key.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        if text[i] in SINGLE_LETTER_MAP:
            key.append(SINGLE_LETTER_MAP[text[i]])
        i += 1
    return np.array(key, dtype=np.int32)

def text_to_gematria(text):
    """Convert text to Gematria values"""
    indices = text_to_key(text)
    return np.array([GEMATRIA[i] for i in indices])

parable_key = text_to_key(PARABLE_TEXT)
parable_gematria = text_to_gematria(PARABLE_TEXT)

print("Parable as indices:", parable_key[:20])
print("Parable as Gematria:", parable_gematria[:20])
print(f"Sum of Parable Gematria: {sum(parable_gematria)}")
print()

# Convert master key to Gematria
master_gematria = np.array([GEMATRIA[i] for i in MASTER_KEY])
print(f"Sum of Master Key Gematria: {sum(master_gematria)}")
print()

print("=" * 70)
print("THEORY 1: USE GEMATRIA VALUES AS DIRECTION")
print("=" * 70)
print("What if we use Parable Gematria values (mod 29) as a secondary key?")

parable_gematria_mod29 = parable_gematria % 29
print("Parable Gematria mod 29:", parable_gematria_mod29[:20])

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    gematria_ext = np.tile(parable_gematria_mod29, (n // len(parable_gematria_mod29)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - gematria_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")
    if score > 30:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("THEORY 2: CUMULATIVE GEMATRIA DIRECTION")
print("=" * 70)
print("What if the Gematria accumulates (running sum) to show direction?")

# Running sum of Gematria mod 29
cumulative_gematria = np.cumsum(parable_gematria) % 29
print("Cumulative Gematria mod 29:", cumulative_gematria[:20])

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    gematria_ext = np.tile(cumulative_gematria, (n // len(cumulative_gematria)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - gematria_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")
    if score > 30:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("THEORY 3: PAGE NUMBER DETERMINES STARTING POSITION IN GEMATRIA")
print("=" * 70)
print("What if page number tells us where to start in the Gematria sequence?")

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    
    # Roll Gematria by page number
    rolled_gematria = np.roll(parable_gematria_mod29, pg_num)
    gematria_ext = np.tile(rolled_gematria, (n // len(rolled_gematria)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - gematria_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} (roll by page#): score {score}")

print()
print("=" * 70)
print("THEORY 4: GEMATRIA VALUE OF PAGE NUMBER DETERMINES SHIFT")
print("=" * 70)
print("Page 27 = IA = Gematria 109")
print("Page 28 = EA = Gematria 113")

page_to_gematria = {
    27: 109,  # IA
    28: 113,  # EA
    29: 2,    # F (29 mod 29 = 0, so F at index 0, Gematria = 2)
    30: 3,    # U (30 mod 29 = 1, so U at index 1, Gematria = 3)
    31: 5,    # TH (31 mod 29 = 2, so TH at index 2, Gematria = 5)
}

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    
    # Roll by Gematria of page number
    pg_gematria = page_to_gematria.get(pg_num, pg_num % 29)
    rolled_parable = np.roll(parable_key, pg_gematria % 95)
    parable_ext = np.tile(rolled_parable, (n // len(rolled_parable)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} (Gematria {pg_gematria}, roll {pg_gematria % 95}): score {score}")

print()
print("=" * 70)
print("THEORY 5: INTERLEAVE KEY AND PARABLE")
print("=" * 70)
print("What if key and parable alternate?")

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    parable_ext = np.tile(parable_key, (n // len(parable_key)) + 1)[:n]
    
    # Interleave: evens use key, odds use parable
    combined = np.where(np.arange(n) % 2 == 0, key_ext, parable_ext)
    
    decrypted = (pg_idx - combined) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} (interleaved): score {score}")

print()
print("=" * 70)
print("THEORY 6: TRANSPOSE THEN DECRYPT")
print("=" * 70)
print("From 08.jpg hint: maybe there's a transposition involved")

# Transposition order from 08.jpg values
reading_order = [11, 10, 12, 9, 13, 1, 5, 2, 7, 3, 8, 0, 4, 6]

for pg_num, page_data in list(UNSOLVED_PAGES.items())[:2]:  # Just test 2 pages
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    # Apply transposition to 14-char chunks
    chunk_size = 14
    transposed = []
    for i in range(0, n, chunk_size):
        chunk = pg_idx[i:i+chunk_size]
        if len(chunk) == chunk_size:
            reordered = [chunk[reading_order[j]] for j in range(chunk_size)]
            transposed.extend(reordered)
        else:
            transposed.extend(chunk)
    
    transposed = np.array(transposed)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    
    decrypted = (transposed - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} (transposed then decrypted): score {score}")
    
    # Also try without transposition
    decrypted2 = (pg_idx - key_ext) % 29
    text2 = indices_to_text(decrypted2)
    score2 = word_score(text2)
    print(f"Page {pg_num} (just key, no transposition): score {score2}")

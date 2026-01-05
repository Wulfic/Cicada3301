"""
PARABLE GEMATRIA AS DIRECTION
=============================

The 2016 clue says: "their NUMBERS are the direction"

What if the Parable's Gematria values tell us HOW to read/apply the key?
For instance:
- Use Parable Gematria to select which key element to use
- Use Parable Gematria to determine skip patterns
- Use Parable Gematria to determine reading order
"""

import numpy as np
from collections import Counter

PARABLE_TEXT = "PARABLELICETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

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
             'EACH', 'HAVE', 'HAS', 'MORE', 'THAN', 'WHEN', 'WHERE', 'WHAT', 'HOW', 'WHO',
             'WAR', 'CONSUME', 'LOSS', 'ILLUSION', 'REALITY']
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
    indices = text_to_key(text)
    return np.array([GEMATRIA[i] for i in indices])

parable_key = text_to_key(PARABLE_TEXT)
parable_gematria = text_to_gematria(PARABLE_TEXT)

print("Parable indices:", parable_key[:20])
print("Parable Gematria:", parable_gematria[:20])
print()

# Key Gematria
master_gematria = np.array([GEMATRIA[i] for i in MASTER_KEY])
print("Master Key as Gematria:", master_gematria[:20])
print()

print("=" * 70)
print("THEORY 1: USE PARABLE GEMATRIA TO INDEX INTO KEY")
print("=" * 70)
print("Each ciphertext position uses key[parable_gematria[i] % key_len]")

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    parable_ext = np.tile(parable_gematria, (n // len(parable_gematria)) + 1)[:n]
    
    # Use parable gematria to index into key
    key_indices = parable_ext % len(MASTER_KEY)
    key_vals = np.array([MASTER_KEY[i] for i in key_indices])
    
    decrypted = (pg_idx - key_vals) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")
    if score > 25:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("THEORY 2: PARABLE GEMATRIA CUMULATIVE AS KEY INDEX")
print("=" * 70)
print("Running sum of Parable Gematria indexes into key")

cumsum_gematria = np.cumsum(parable_gematria)

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    cumsum_ext = np.tile(cumsum_gematria, (n // len(cumsum_gematria)) + 1)[:n]
    
    key_indices = cumsum_ext % len(MASTER_KEY)
    key_vals = np.array([MASTER_KEY[i] for i in key_indices])
    
    decrypted = (pg_idx - key_vals) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")
    if score > 25:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("THEORY 3: PARABLE GEMATRIA AS SKIP IN KEY")
print("=" * 70)
print("For each position i, use key[(sum of first i gematria) % key_len]")

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    parable_ext = np.tile(parable_gematria, (n // len(parable_gematria)) + 1)[:n]
    
    # Cumulative position in key
    key_pos = 0
    key_vals = []
    for i in range(n):
        key_vals.append(MASTER_KEY[key_pos % len(MASTER_KEY)])
        key_pos += parable_ext[i]
    
    key_vals = np.array(key_vals)
    
    decrypted = (pg_idx - key_vals) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")
    if score > 25:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("THEORY 4: MULTIPLY KEY BY PARABLE GEMATRIA RATIO")
print("=" * 70)

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    parable_ext = np.tile(parable_gematria, (n // len(parable_gematria)) + 1)[:n]
    
    # Multiply key by parable gematria, then mod 29
    modified_key = (key_ext * parable_ext) % 29
    
    decrypted = (pg_idx - modified_key) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")
    if score > 25:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("THEORY 5: PARABLE AS MODULAR INVERSE KEY")
print("=" * 70)
print("What if Parable is the modular inverse of the key?")

# For modular arithmetic, if encrypted = plain + key, and
# we know the parable, maybe: key = parable^-1 * something

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    parable_ext = np.tile(parable_key, (n // len(parable_key)) + 1)[:n]
    
    # Try XOR of key and parable
    xor_key = np.bitwise_xor(key_ext, parable_ext) % 29
    
    decrypted = (pg_idx - xor_key) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} (XOR key): score {score}")
    
    # Try difference of key and parable
    diff_key = (key_ext - parable_ext) % 29
    
    decrypted2 = (pg_idx - diff_key) % 29
    text2 = indices_to_text(decrypted2)
    score2 = word_score(text2)
    
    print(f"Page {pg_num} (diff key): score {score2}")

print()
print("=" * 70)
print("THEORY 6: KEY POSITION BASED ON PRIME FACTORIZATION")
print("=" * 70)
print("Use the number of prime factors of gematria to modify key")

def prime_factors_count(n):
    count = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            count += 1
            n //= d
        d += 1
    if n > 1:
        count += 1
    return count

parable_factors = np.array([prime_factors_count(g) for g in parable_gematria])
print("Parable prime factor counts:", parable_factors[:20])

for pg_num, page_data in list(UNSOLVED_PAGES.items())[:2]:
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    factors_ext = np.tile(parable_factors, (n // len(parable_factors)) + 1)[:n]
    
    # Multiply key by factor count
    modified_key = (key_ext * factors_ext) % 29
    
    decrypted = (pg_idx - modified_key) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num}: score {score}")

print()
print("=" * 70)
print("THEORY 7: PAGE-SPECIFIC KEY DERIVED FROM PARABLE")
print("=" * 70)
print("Each page might use a different starting word in the Parable")

# Words in parable: PARABLE LIKE THE INSTAR TUNNELING TO THE SURFACE...
# Maybe page 27 starts at word position 27 mod (word count)?

parable_words = ["PARABLE", "LIKE", "THE", "INSTAR", "TUNNELING", "TO", "THE", "SURFACE", 
                 "WE", "MUST", "SHED", "OUR", "OWN", "CIRCUMFERENCES", "FIND", "THE", 
                 "DIVINITY", "WITHIN", "AND", "EMERGE"]

print(f"Number of words in Parable: {len(parable_words)}")

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    # Get starting word based on page number
    word_idx = pg_num % len(parable_words)
    start_word = parable_words[word_idx]
    
    # Find position of this word in parable
    start_pos = PARABLE_TEXT.find(start_word)
    
    # Roll parable key to start at this position
    rolled_parable = np.roll(parable_key, -start_pos)
    
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    parable_ext = np.tile(rolled_parable, (n // len(rolled_parable)) + 1)[:n]
    
    # Double keying
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} (word {word_idx}: '{start_word}', pos {start_pos}): score {score}")
    if score > 35:
        print(f"  {text[:70]}...")

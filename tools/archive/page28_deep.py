"""
Deep focus on Page 28 - scored 195 with standard key, almost solved!
"""
import numpy as np

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

def indices_to_text(indices):
    LATIN = "FUÞORC.WHNIJEOPXSTBEMLNGDAÆAYEA"[:29]
    return ''.join(LATIN[i % 29] for i in indices)

def word_score(text):
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE',
             'EACH', 'HAVE', 'HAS', 'HAD', 'SAID', 'WHEN', 'WHO', 'SOME', 'TIME', 'VERY',
             'UPON', 'OTHER', 'INTO', 'ONLY', 'LITTLE', 'LOOK', 'JUST', 'OVER', 'ALSO',
             'MADE', 'MAKE', 'MORE', 'AFTER', 'THINK', 'HOW', 'SUCH', 'OUR', 'THESE',
             'LONG', 'WAY', 'COULD', 'WORLD', 'BEEN', 'WILL', 'WOULD', 'SHOULD', 'MUST',
             'THING', 'THINGS', 'MAN', 'MEN', 'KNOW', 'THEN', 'THAN', 'NOW', 'COME', 'CAME',
             'THOSE', 'DO', 'DOES', 'DID', 'DAY', 'DAYS', 'WORD', 'WORDS', 'ABOUT', 'BECAUSE',
             'THROUGH', 'BETWEEN', 'UNDER', 'AFTER', 'BEFORE', 'GREAT', 'GOOD', 'LIFE', 'DEAD',
             'DEATH', 'WHERE', 'WHILE', 'FIND', 'GIVE', 'TAKE', 'SEE', 'SEEN', 'SEEK', 'FOUND',
             'BODY', 'SOUL', 'SPIRIT', 'MIND', 'HEART', 'LIGHT', 'DARK', 'EYES', 'HAND', 'HANDS',
             'HEAD', 'FACE', 'EARTH', 'HEAVEN', 'FIRE', 'WATER', 'AIR', 'NAME', 'NAMES', 'SACRED']
    score = 0
    text_upper = text.upper()
    for word in WORDS:
        score += text_upper.count(word) * len(word)
    return score

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

PAGE_28 = "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ"

pg_idx = np.array([RUNE_TO_INDEX[r] for r in PAGE_28])
key = np.array(MASTER_KEY)
key_ext = np.tile(key, (len(pg_idx) // len(key)) + 1)[:len(pg_idx)]

print("=" * 70)
print("PAGE 28 DEEP ANALYSIS")
print("=" * 70)
print(f"Page length: {len(pg_idx)} runes")
print()

# Standard decryption
decrypted = (pg_idx - key_ext) % 29
text = indices_to_text(decrypted)
print("Standard decryption:")
print(text)
print(f"Score: {word_score(text)}")
print()

# Look for patterns in the text
print("Character frequency:")
from collections import Counter
freq = Counter(text)
for char, count in freq.most_common(10):
    print(f"  '{char}': {count}")

# Try small shifts around the key
print("\n" + "=" * 70)
print("TESTING SMALL KEY MODIFICATIONS")
print("=" * 70)

best_results = []

# Test shifting each key position slightly
for shift_amount in range(-5, 6):
    modified_key = (key + shift_amount) % 29
    key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    best_results.append((score, f"Key + {shift_amount}", text[:70]))

# Test key rolled by small amounts
for roll_amount in range(1, 20):
    modified_key = np.roll(key, roll_amount)
    key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    best_results.append((score, f"Key rolled {roll_amount}", text[:70]))

# Test with page number offset
for offset in range(0, 60):
    # Start from position 'offset' in the key
    rolled_key = np.roll(key, -offset)
    key_ext_mod = np.tile(rolled_key, (len(pg_idx) // len(rolled_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    if score >= 150:
        best_results.append((score, f"Key start at {offset}", text[:70]))

# Sort and show best
best_results.sort(reverse=True)
print("\nTop results:")
for score, desc, text in best_results[:15]:
    print(f"  {score}: {desc}")
    print(f"      {text}")

# Now let's try alternative starting points based on page structure
print("\n" + "=" * 70)
print("TESTING ALTERNATIVE DECRYPTION STARTING POINTS")
print("=" * 70)

# Maybe page 28 uses a key starting at position 28 % 95 = 28
for key_start in [28, 27, 29, 30, 33, 56, 57, 66, 67, 76, 77, 85]:
    modified_key = np.roll(key, -key_start)
    key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    print(f"Key starting at position {key_start}: score {score}")
    if score >= 100:
        print(f"  {text[:80]}")

# Try adding page number to key
print("\nWith key + page_number:")
modified_key = (key + 28) % 29
key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
decrypted = (pg_idx - key_ext_mod) % 29
text = indices_to_text(decrypted)
print(f"Score: {word_score(text)}")
print(text[:80])

# Try double decryption (maybe already partially decrypted?)
print("\nDouble decryption (apply key twice):")
decrypted1 = (pg_idx - key_ext) % 29
decrypted2 = (decrypted1 - key_ext) % 29
text = indices_to_text(decrypted2)
print(f"Score: {word_score(text)}")
print(text[:80])

# Try Atbash after key
print("\nKey then Atbash:")
decrypted = (pg_idx - key_ext) % 29
atbash = (28 - decrypted) % 29
text = indices_to_text(atbash)
print(f"Score: {word_score(text)}")
print(text[:80])

# Try reverse order
print("\nReverse reading order:")
decrypted = (pg_idx[::-1] - key_ext) % 29
text = indices_to_text(decrypted)
print(f"Score: {word_score(text)}")
print(text[:80])

# The text from standard decryption - let's analyze it more
print("\n" + "=" * 70)
print("ANALYZING STANDARD DECRYPTION TEXT")
print("=" * 70)
decrypted = (pg_idx - key_ext) % 29
text = indices_to_text(decrypted)
print("Full text:")
print(text)
print()

# Look for English word fragments
print("Potential word boundaries (looking for common patterns):")
# Common 3-letter combinations
trigrams = ['THE', 'AND', 'ING', 'ION', 'TIO', 'ENT', 'ERE', 'HER', 'ATE', 'VER', 'TER', 'EST', 'IES']
for tri in trigrams:
    if tri in text:
        indices_found = [i for i in range(len(text) - 2) if text[i:i+3] == tri]
        print(f"  '{tri}' found at positions: {indices_found}")

# Try splitting into words by common English patterns
print("\nSearching for word-like patterns:")
import re
# Find runs of characters that could form English words
potential_words = re.findall(r'[AEIOUÞ]?[BCDFGHJKLMNPQRSTVWXYZ]+[AEIOUÞ]+[BCDFGHJKLMNPQRSTVWXYZ]*[AEIOUÞ]*', text)
print("Potential words:", potential_words[:20])

# Finally, try a columnar transposition interpretation
print("\n" + "=" * 70)
print("COLUMNAR READING PATTERNS")
print("=" * 70)
for cols in [7, 8, 9, 10, 11, 12, 13, 14]:
    n = len(pg_idx)
    rows = (n + cols - 1) // cols
    # Pad if needed
    padded = list(pg_idx) + [0] * (rows * cols - n)
    grid = np.array(padded).reshape(rows, cols)
    
    # Read column by column
    col_read = grid.T.flatten()[:n]
    decrypted = (col_read - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    if score >= 100:
        print(f"  Cols={cols}: score {score}")
        print(f"    {text[:70]}")
    
    # Read and then decrypt
    decrypted_first = (pg_idx - key_ext) % 29
    padded_dec = list(decrypted_first) + [0] * (rows * cols - n)
    grid = np.array(padded_dec).reshape(rows, cols)
    col_read = grid.T.flatten()[:n]
    text = indices_to_text(col_read)
    score = word_score(text)
    if score >= 100:
        print(f"  Cols={cols} after decrypt: score {score}")
        print(f"    {text[:70]}")

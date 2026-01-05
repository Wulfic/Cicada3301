"""
Deep analysis of Page 47 with XOR key modification
"""
import numpy as np
import os
import sys

# Define all the data locally
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

def indices_to_text(indices):
    LATIN = "FUÞORC.WHNIJEOPXSTBEMLNGDAÆAYEA"[:29]
    return ''.join(LATIN[i % 29] for i in indices)

def word_score(text):
    WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
             'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
             'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'PARABLE', 'INSTAR', 'LIKE', 'UNTO',
             'WISDOM', 'TRUTH', 'KNOWLEDGE', 'DIVINITY', 'WITHIN', 'PRIMES', 'CIRCLE']
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

# Embedded page data
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

# Extended word list with Cicada vocabulary
WORDS = {
    'THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'YOU', 'THAT',
    'WE', 'BE', 'ARE', 'FOR', 'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN',
    'THEY', 'WHICH', 'BY', 'THEIR', 'ALL', 'THERE', 'BUT', 'ONE', 'WHAT',
    'SO', 'OUT', 'UP', 'SOME', 'WOULD', 'IF', 'CAN', 'WHEN', 'WHO',
    'LIKE', 'INSTAR', 'PARABLE', 'CICADA', 'SURFACE', 'TUNNEL', 'WISDOM',
    'KNOWLEDGE', 'TRUTH', 'LIGHT', 'DARK', 'PATH', 'WAY', 'SELF', 'BEING',
    'MIND', 'SOUL', 'SPIRIT', 'BODY', 'WORLD', 'UNIVERSE', 'TIME', 'SPACE',
    'THOUGHT', 'THINK', 'KNOW', 'LEARN', 'UNDERSTAND', 'SEE', 'HEAR',
    'WITHIN', 'WITHOUT', 'ABOVE', 'BELOW', 'BETWEEN', 'AMONG', 'THROUGH',
    'MUST', 'SHALL', 'WILL', 'SHOULD', 'COULD', 'WOULD', 'MAY', 'MIGHT',
    'HAVE', 'HAS', 'HAD', 'DO', 'DOES', 'DID', 'MAKE', 'MADE', 'EACH',
    'OTHER', 'EVERY', 'MANY', 'SUCH', 'ONLY', 'FIRST', 'LAST', 'OWN',
    'THOSE', 'THESE', 'COME', 'CAME', 'GIVE', 'GAVE', 'TAKE', 'TOOK',
    'GOOD', 'GREAT', 'LITTLE', 'MUCH', 'VERY', 'MOST', 'ALSO', 'MORE',
    'WAR', 'CONSUME', 'LOSS', 'ILLUSION', 'REALITY', 'TRUTH', 'LIE',
    'PRIMES', 'NUMBERS', 'CIPHER', 'CODE', 'KEY', 'RUNE', 'WORD', 'WORDS',
    'COMMAND', 'INSTRUCTION', 'CIRCUMFERENCE', 'CIRCLE', 'SHED', 'OUR',
    'WHERE', 'WHEN', 'WHY', 'HOW', 'WHAT', 'HERE', 'NOW', 'THEN', 'EVER',
    'AGE', 'AGES', 'OLD', 'NEW', 'ANCIENT', 'MODERN', 'PAST', 'FUTURE',
    'BEGIN', 'END', 'START', 'STOP', 'CONTINUE', 'EMERGE', 'EMERGENCE',
    'UNTO', 'INTO', 'UPON', 'BEYOND', 'BEFORE', 'AFTER', 'DURING',
    'SEEK', 'FIND', 'SEARCH', 'DISCOVER', 'REVEAL', 'HIDE', 'HIDDEN',
    'SECRET', 'MYSTERY', 'ENIGMA', 'PUZZLE', 'ANSWER', 'QUESTION',
    'LETTER', 'BOOK', 'PAGE', 'CHAPTER', 'VERSE', 'TEXT', 'MESSAGE',
    'SIGN', 'SYMBOL', 'MARK', 'POINT', 'LINE', 'SHAPE', 'FORM',
    'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',
    'ELEVEN', 'TWELVE', 'THIRTEEN', 'HUNDRED', 'THOUSAND', 'MILLION',
    'NOT', 'NO', 'YES', 'MAYBE', 'PERHAPS', 'ALWAYS', 'NEVER', 'SOMETIMES',
    'HE', 'SHE', 'HIM', 'HER', 'HIS', 'HERS', 'THEM', 'US', 'ME', 'MY',
    'YOUR', 'YOURS', 'OURS', 'THEIRS', 'ITS', 'ITSELF', 'YOURSELF',
    'HIMSELF', 'HERSELF', 'OURSELVES', 'THEMSELVES', 'DEAD', 'LIFE',
    'LIVE', 'ALIVE', 'DIE', 'DEATH', 'BORN', 'BIRTH', 'CREATE', 'DESTROY',
    'BUILD', 'BREAK', 'GROW', 'SHRINK', 'RISE', 'FALL', 'OPEN', 'CLOSE',
    'ON', 'OFF', 'OVER', 'UNDER', 'INSIDE', 'OUTSIDE', 'LEFT', 'RIGHT',
    'NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTER', 'EDGE', 'CORNER',
    'FIRE', 'WATER', 'EARTH', 'AIR', 'WIND', 'RAIN', 'SNOW', 'ICE',
    'SUN', 'MOON', 'STAR', 'STARS', 'PLANET', 'COSMOS', 'VOID', 'ABYSS',
    'HEAVEN', 'HELL', 'GOD', 'GODS', 'DIVINE', 'HOLY', 'SACRED', 'PROFANE',
    'LOVE', 'HATE', 'FEAR', 'HOPE', 'JOY', 'SORROW', 'ANGER', 'PEACE',
    'WAR', 'CHAOS', 'ORDER', 'LAW', 'RULE', 'POWER', 'FORCE', 'ENERGY',
    'MATTER', 'NATURE', 'ART', 'SCIENCE', 'MAGIC', 'ALCHEMY', 'PHILOSOPHY',
    'REASON', 'LOGIC', 'INTUITION', 'FEELING', 'SENSE', 'PERCEPTION',
    'AWARENESS', 'CONSCIOUSNESS', 'UNCONSCIOUS', 'DREAM', 'WAKE', 'SLEEP'
}

def better_score(text):
    """Score with larger word preference"""
    score = 0
    text_upper = text.upper()
    for word in sorted(WORDS, key=len, reverse=True):  # Try longer words first
        count = text_upper.count(word)
        if count > 0:
            score += len(word) * count * len(word)  # Weight by word length squared
    return score

# Page 47 data
page_47 = UNSOLVED_PAGES.get(47, UNSOLVED_PAGES.get("47"))
if page_47 is None:
    print("Page 47 not found, listing keys:", list(UNSOLVED_PAGES.keys())[:5])
    exit()

pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_47])
key = np.array(MASTER_KEY)
key_ext = np.tile(key, (len(pg_idx) // len(key)) + 1)[:len(pg_idx)]

print("=" * 70)
print("PAGE 47 DEEP ANALYSIS")
print("=" * 70)
print(f"Page length: {len(pg_idx)} runes")
print()

# Test XOR with different values
print("Testing key XOR modifications:")
best_xor = []
for xor_val in range(1, 100):
    modified_key = np.array([(k ^ xor_val) % 29 for k in MASTER_KEY])
    key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    if score >= 150:
        best_xor.append((score, xor_val, text[:80]))

best_xor.sort(reverse=True)
print("Top XOR results:")
for score, xor_val, text in best_xor[:10]:
    print(f"  XOR {xor_val}: score {score}")
    print(f"    {text}")

# Also test adding values
print("\nTesting key ADD modifications:")
best_add = []
for add_val in range(1, 100):
    modified_key = np.array([(k + add_val) % 29 for k in MASTER_KEY])
    key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    if score >= 150:
        best_add.append((score, add_val, text[:80]))

best_add.sort(reverse=True)
print("Top ADD results:")
for score, add_val, text in best_add[:10]:
    print(f"  ADD {add_val}: score {score}")
    print(f"    {text}")

# Test combinations of XOR and shift
print("\nTesting shift + XOR combinations:")
best_combo = []
for shift in range(1, 50):
    for xor_val in [47, 48, 49, 50, 46, 45]:
        shifted_key = np.roll(key, shift)
        modified_key = np.array([(k ^ xor_val) % 29 for k in shifted_key])
        key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
        decrypted = (pg_idx - key_ext_mod) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        if score >= 200:
            best_combo.append((score, shift, xor_val, text[:80]))

best_combo.sort(reverse=True)
print("Top SHIFT + XOR results:")
for score, shift, xor_val, text in best_combo[:10]:
    print(f"  Shift {shift} XOR {xor_val}: score {score}")
    print(f"    {text}")

# The best result was XOR 47 - let's examine it more closely
print("\n" + "=" * 70)
print("DETAILED LOOK AT XOR 47")
print("=" * 70)
modified_key = np.array([(k ^ 47) % 29 for k in MASTER_KEY])
key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
decrypted = (pg_idx - key_ext_mod) % 29
text = indices_to_text(decrypted)
print(f"Full text ({len(text)} chars):")
print(text)
print()
print(f"Word score: {word_score(text)}")
print(f"Better score: {better_score(text)}")

# Check for word boundaries
print("\nPossible word segmentation:")
words_found = []
text_upper = text.upper()
for word in sorted(WORDS, key=len, reverse=True):
    start = 0
    while word in text_upper[start:]:
        idx = text_upper.index(word, start)
        words_found.append((idx, word))
        start = idx + 1
words_found.sort()
print("Words found in order:", [w for _, w in words_found[:30]])

# Test if page number XOR pattern works on other pages
print("\n" + "=" * 70)
print("TESTING PAGE NUMBER XOR ON ALL UNSOLVED PAGES")
print("=" * 70)

for pg_num in sorted(UNSOLVED_PAGES.keys(), key=int):
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    
    xor_val = int(pg_num)
    modified_key = np.array([(k ^ xor_val) % 29 for k in MASTER_KEY])
    key_ext_mod = np.tile(modified_key, (len(pg_idx) // len(modified_key)) + 1)[:len(pg_idx)]
    decrypted = (pg_idx - key_ext_mod) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} XOR {xor_val}: score {score}")
    if score >= 150:
        print(f"  {text[:70]}")

"""
DEEP DIVE: PAGE 27 WITH PARABLE SHIFT 25
=========================================

Score 51 found with Standard Key + Parable shifted by 25!
This is the highest score we've found so far for an unsolved page.

Let's analyze this more carefully.
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

PAGE_27 = "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ"

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

parable_key = text_to_key(PARABLE_TEXT)
pg_idx = np.array([RUNE_TO_INDEX[r] for r in PAGE_27])
n = len(pg_idx)

print(f"Page 27 length: {n} runes")
print(f"Parable key length: {len(parable_key)}")
print()

# Best result: Key shift 0, Parable shift 25
print("=" * 70)
print("THE BEST RESULT: Score 51")
print("=" * 70)

mod_parable = np.roll(parable_key, 25)
key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]

decrypted = (pg_idx - key_ext - parable_ext) % 29
text = indices_to_text(decrypted)
print(f"Full decrypted text ({len(text)} chars):")
print(text)
print()
print(f"Score: {word_score(text)}")
print()

# Find all words
print("Words found:")
words_found = []
WORDS = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'IT', 'THAT', 'WE', 'BE', 'ARE', 'FOR',
         'THIS', 'WITH', 'AS', 'FROM', 'OR', 'AN', 'THEY', 'WHICH', 'BY', 'THEIR', 'ALL',
         'THERE', 'BUT', 'ONE', 'WHAT', 'SO', 'OUT', 'NG', 'TH', 'EO']
for word in sorted(WORDS, key=len, reverse=True):
    count = text.count(word)
    if count > 0:
        positions = [i for i in range(len(text) - len(word) + 1) if text[i:i+len(word)] == word]
        words_found.append((word, count, positions))
        print(f"  '{word}' appears {count} times at positions {positions}")

print()

# Try to find more optimal shifts
print("=" * 70)
print("SCANNING ALL SHIFT COMBINATIONS FOR PAGE 27")
print("=" * 70)

best_results = []
for key_shift in range(95):
    for parable_shift in range(95):
        mod_key = np.roll(MASTER_KEY, key_shift)
        mod_parable = np.roll(parable_key, parable_shift)
        key_ext = np.tile(mod_key, (n // len(mod_key)) + 1)[:n]
        parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
        
        decrypted = (pg_idx - key_ext - parable_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score >= 45:
            best_results.append((score, key_shift, parable_shift, text[:80]))

best_results.sort(reverse=True)
print("Top 20 results:")
for i, (score, ks, ps, text) in enumerate(best_results[:20]):
    print(f"{i+1}. Score {score}: Key shift {ks}, Parable shift {ps}")
    print(f"   {text}")

print()
print("=" * 70)
print("TESTING THE SAME FORMULA ON OTHER PAGES")
print("=" * 70)

# Test if Parable shift 25 works on other pages too
for pg_num in [28, 29, 30, 31]:
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    mod_parable = np.roll(parable_key, 25)  # Same shift that worked for page 27
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} with same shifts: score {score}")
    if score > 30:
        print(f"  {text[:70]}...")
    
    # Also try shifting by page number difference
    pg_diff = pg_num - 27
    mod_parable = np.roll(parable_key, 25 + pg_diff)
    parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} with adjusted shift {25 + pg_diff}: score {score}")
    if score > 30:
        print(f"  {text[:70]}...")

print()
print("=" * 70)
print("WHY 25? ANALYZING THE SHIFT VALUE")
print("=" * 70)
print(f"25 is the index of 'AE' (ᚫ) in Gematria Primus")
print(f"25 = 5² (perfect square)")
print(f"Page 27 starts at position 25 in parable when shift is applied")
print(f"Page 27 mod 29 = 27")
print(f"Page 27 - 2 = 25 (maybe page - 2 is the formula?)")

# Test if page - 2 is the formula
print()
print("Testing if (page_num - 2) is the parable shift formula:")
for pg_num in [27, 28, 29, 30, 31]:
    page_data = UNSOLVED_PAGES[pg_num]
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    parable_shift = pg_num - 2
    mod_parable = np.roll(parable_key, parable_shift)
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    parable_ext = np.tile(mod_parable, (n // len(mod_parable)) + 1)[:n]
    
    decrypted = (pg_idx - key_ext - parable_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} with shift {parable_shift}: score {score}")

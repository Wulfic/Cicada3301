#!/usr/bin/env python3
"""
Analyze the NUMBERS from Liber Primus more carefully.

The 2016 clue says:
"Liber Primus is the way. Its words are the map, their meaning is the road,
and their NUMBERS are the direction."

What numbers exist in Liber Primus?
1. Page numbers
2. Gematria values of each rune
3. Gematria sums of words
4. Positions of words
5. Prime indices in Gematria Primus
6. RSA hex numbers on Page 56
"""

import re

# Define the rune system
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

def rune_to_letters(runes):
    return ''.join(RUNE_TO_LETTER.get(r, '?') for r in runes)

def gematria(runes):
    """Calculate Gematria sum of runes."""
    return sum(GP_PRIMES[RUNE_TO_IDX[r]] for r in runes if r in RUNE_TO_IDX)

# Read the pages from RuneSolver.py
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)

def get_runes_only(page):
    return ''.join(c for c in page if c in RUNE_TO_IDX)

# The PARABLE text (Page 57 - known plaintext)
PARABLE_RUNES = PAGES[57]
PARABLE_TEXT = "PARABLELIKETHEINSTARTUNELINGTOTHESURFACEWEMUSTSHTEDOUROWNSCIRCUMFERENCESFINDTHEDIVINITYWITHINANDEMERGE"

# Split Parable into words
parable_words_text = [
    "PARABLE", "LIKE", "THE", "INSTAR", "TUNNELING", "TO", "THE", "SURFACE",
    "WE", "MUST", "SHED", "OUR", "OWN", "CIRCUMFERENCES", "FIND", "THE",
    "DIVINITY", "WITHIN", "AND", "EMERGE"
]

# Calculate Gematria for each word
print("="*60)
print("WORD GEMATRIA VALUES FROM PARABLE")
print("="*60)

# First get the rune representation of each word
parable_runes_only = get_runes_only(PARABLE_RUNES)
print(f"Parable runes: {len(parable_runes_only)} runes")
print(f"Parable text: {rune_to_letters(parable_runes_only)}")

# Split on dots (word separators) - actually • is the separator
# Looking at Page57: words are separated by • (middle dot)
raw_parable = PARABLE_RUNES.replace('::', '').replace(':', '•')  # Normalize
words_runes = [w for w in raw_parable.replace('.', '•').split('•') if w]
print(f"\nWords found: {len(words_runes)}")

word_gematria = []
for i, word in enumerate(words_runes):
    if not word:
        continue
    runes = get_runes_only(word)
    gem = gematria(runes)
    text = rune_to_letters(runes)
    word_gematria.append((i, text, gem, gem % 29))
    print(f"  {i}: {text:20s} = {gem:4d} (mod 29 = {gem % 29:2d})")

print("\n" + "="*60)
print("CUMULATIVE GEMATRIA POSITIONS")
print("="*60)

# Maybe the cumulative Gematria tells us something
cumsum = 0
positions = []
for i, text, gem, mod29 in word_gematria:
    cumsum += gem
    positions.append((i, text, cumsum, cumsum % 29, cumsum % 95))
    print(f"  After '{text}': cumsum={cumsum:4d} (mod 29={cumsum%29:2d}, mod 95={cumsum%95:2d})")

print("\n" + "="*60)
print("PAGE NUMBERS AND THEIR SPECIAL VALUES")
print("="*60)

unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
for pg in unsolved:
    # Various number interpretations
    print(f"\nPage {pg}:")
    print(f"  Prime at index {pg}: {GP_PRIMES[pg] if pg < 29 else 'N/A'}")
    print(f"  {pg} mod 29 = {pg % 29}")
    print(f"  {pg} mod 11 = {pg % 11}")  # 11 is significant (1331 = 11^3)
    print(f"  {pg} - 20 = word {pg - 20}")  # Pattern we noticed
    
    # What word does this map to?
    word_idx = pg - 20
    if 0 <= word_idx < len(word_gematria):
        print(f"  Parable word {word_idx}: {word_gematria[word_idx][1]} (gem={word_gematria[word_idx][2]})")

print("\n" + "="*60)
print("TESTING: WORD GEMATRIA AS KEY OFFSET")
print("="*60)

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def decrypt_vigenere(cipher_runes, key, offset=0):
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[(i + offset) % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

def count_english_words(text):
    rune_text = rune_to_letters(text)
    words = ["THE", "AND", "OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT",
             "THIS", "THAT", "HAVE", "FROM", "OR", "AN", "BY", "NOT", "BUT",
             "WHAT", "ALL", "WERE", "WE", "WHEN", "YOUR", "CAN", "SAID",
             "THERE", "USE", "EACH", "WHICH", "DO", "HOW", "THEIR",
             "WILL", "OTHER", "ABOUT", "OUT", "MANY", "THEN", "THEM", "THESE",
             "SOME", "WOULD", "LIKE", "INTO", "TIME", "HAS", "LOOK", "TWO",
             "MORE", "GO", "SEE", "NO", "WAY", "COULD", "PEOPLE", "MY", "THAN",
             "FIRST", "BEEN", "CALL", "WHO", "ITS", "NOW", "FIND", "LONG",
             "DOWN", "DAY", "DID", "GET", "COME", "MADE", "MAY", "PART",
             "INSTAR", "DIVINITY", "EMERGE", "SURFACE", "CIRCUMFERENCE",
             "PRIMUS", "LIBER", "WITHIN", "DEEP", "WEB", "PAGE", "TRUTH"]
    score = 0
    for word in words:
        if len(word) >= 3:
            count = rune_text.count(word)
            score += count * len(word)
    return score

# Test: Use word Gematria mod 95 as the offset
print("Using word's Gematria (mod 95) as key start offset:")
for pg in unsolved[:7]:
    word_idx = pg - 20
    if 0 <= word_idx < len(word_gematria):
        _, word_text, gem, mod29 = word_gematria[word_idx]
        offset = gem % 95
        
        cipher = get_runes_only(PAGES[pg])
        decrypted = decrypt_vigenere(cipher, MASTER_KEY, offset)
        score = count_english_words(decrypted)
        text = rune_to_letters(decrypted)[:60]
        
        print(f"\nPage {pg} (word '{word_text}', gem={gem}, offset={offset}):")
        print(f"  Score: {score}")
        print(f"  Text: {text}...")

# Test: Add word's Gematria to each key element
print("\n\n" + "="*60)
print("TESTING: ADD WORD GEMATRIA TO KEY")
print("="*60)

for pg in unsolved[:7]:
    word_idx = pg - 20
    if 0 <= word_idx < len(word_gematria):
        _, word_text, gem, mod29 = word_gematria[word_idx]
        
        # Create modified key by adding Gematria mod 29
        modified_key = [(k + gem) % 29 for k in MASTER_KEY]
        
        cipher = get_runes_only(PAGES[pg])
        decrypted = decrypt_vigenere(cipher, modified_key, 0)
        score = count_english_words(decrypted)
        text = rune_to_letters(decrypted)[:60]
        
        print(f"\nPage {pg} (word '{word_text}', add gem mod 29 = {gem % 29}):")
        print(f"  Score: {score}")
        print(f"  Text: {text}...")

# Test: Multiply key by word's Gematria
print("\n\n" + "="*60)
print("TESTING: MULTIPLY KEY BY WORD GEMATRIA")
print("="*60)

for pg in unsolved[:5]:
    word_idx = pg - 20
    if 0 <= word_idx < len(word_gematria):
        _, word_text, gem, mod29 = word_gematria[word_idx]
        
        # Try different multipliers related to the word
        for mult in [mod29, gem % 95, (gem * 11) % 29]:
            if mult == 0:
                continue
            modified_key = [(k * mult) % 29 for k in MASTER_KEY]
            
            cipher = get_runes_only(PAGES[pg])
            decrypted = decrypt_vigenere(cipher, modified_key, 0)
            score = count_english_words(decrypted)
            
            if score > 20:
                text = rune_to_letters(decrypted)[:60]
                print(f"\nPage {pg} (word '{word_text}', mult={mult}):")
                print(f"  Score: {score}")
                print(f"  Text: {text}...")

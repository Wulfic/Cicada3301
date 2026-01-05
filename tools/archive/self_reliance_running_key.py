#!/usr/bin/env python3
"""
Test Self-Reliance (Emerson) as a running key for Liber Primus.
"""

import re

# Define the rune system
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

def rune_to_letters(runes):
    return ''.join(RUNE_TO_LETTER.get(r, '?') for r in runes)

# Read the pages from RuneSolver.py
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Extract individual page definitions
PAGES = {}
for i in range(58):
    pattern = rf'Page{i}\s*=\s*"([^"]+)"'
    match = re.search(pattern, content)
    if match:
        PAGES[i] = match.group(1)
        
print(f"Loaded {len(PAGES)} pages")

# Read Self-Reliance
with open(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\Self-Reliance.txt", 'r', encoding='utf-8') as f:
    self_reliance = f.read()

# Clean to uppercase letters only
sr_clean = ''.join(c.upper() for c in self_reliance if c.isalpha())
print(f"Self-Reliance length (letters only): {len(sr_clean)}")

# Convert to rune indices (A-Z -> 0-25, but we use 0-28 for Futhorc)
# For running key, we'll map letters to rune indices
LETTER_TO_RUNE = {}
for i, rune in enumerate(RUNES):
    if rune in "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ":
        pass  # We need letter mapping

# Actually, let's use the established letter->rune mapping
# From GP: F U Th O R C G W H N I J Eo P X S T B E M L Ng Oe D A Ae Y Ia Ea
LETTERS_TO_IDX = {
    'F': 0, 'U': 1, 'T': 16,  # Th would be special
    'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'B': 17, 'E': 18,
    'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26,
    # Handle missing letters
    'K': 5,  # K -> C
    'Q': 5,  # Q -> C  
    'V': 1,  # V -> U
    'Z': 15, # Z -> S
}

# Better: use gematria value mod 29
def letter_to_shift(letter):
    """Convert letter to shift value using various methods."""
    if letter in LETTERS_TO_IDX:
        return LETTERS_TO_IDX[letter]
    return ord(letter) - ord('A')  # fallback

def sr_to_key(text, length, start=0):
    """Convert Self-Reliance text to key values."""
    key = []
    idx = start
    while len(key) < length and idx < len(text):
        letter = text[idx]
        if letter.isalpha():
            key.append(letter_to_shift(letter.upper()))
        idx += 1
    return key

# Test pages - get from PAGES dict
UNSOLVED_PAGES = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

def get_page_runes(page_num):
    """Get runes for a page from PAGES dict."""
    if page_num in PAGES:
        # Filter to just runes
        return ''.join(c for c in PAGES[page_num] if c in RUNE_TO_IDX)
    return ""

def decrypt_with_key(cipher_runes, key):
    """Decrypt using running key."""
    result = []
    for i, rune in enumerate(cipher_runes):
        if rune in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[rune]
            key_val = key[i % len(key)]
            plain_idx = (idx - key_val) % 29
            result.append(RUNES[plain_idx])
    return ''.join(result)

def count_english_words(text):
    """Score based on English words found."""
    rune_text = rune_to_letters(text)
    if not rune_text:
        return 0
    
    words = ["THE", "AND", "OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT",
             "THIS", "THAT", "HAVE", "FROM", "OR", "AN", "BY", "NOT", "BUT",
             "WHAT", "ALL", "WERE", "WE", "WHEN", "YOUR", "CAN", "SAID",
             "THERE", "USE", "EACH", "WHICH", "SHE", "DO", "HOW", "THEIR",
             "WILL", "OTHER", "ABOUT", "OUT", "MANY", "THEN", "THEM", "THESE",
             "SO", "SOME", "HER", "WOULD", "MAKE", "LIKE", "HIM", "INTO",
             "TIME", "HAS", "LOOK", "TWO", "MORE", "WRITE", "GO", "SEE",
             "NUMBER", "NO", "WAY", "COULD", "PEOPLE", "MY", "THAN", "FIRST",
             "WATER", "BEEN", "CALL", "WHO", "OIL", "ITS", "NOW", "FIND",
             "LONG", "DOWN", "DAY", "DID", "GET", "COME", "MADE", "MAY", "PART",
             # Cicada-specific
             "INSTAR", "DIVINITY", "EMERGE", "SURFACE", "CIRCUMFERENCE",
             "PRIMUS", "LIBER", "WITHIN", "DEEP", "WEB", "PAGE", "TRUTH",
             # Self-Reliance specific
             "SELF", "RELIANCE", "TRUST", "THYSELF", "SOUL", "GENIUS",
             "NATURE", "MAN", "SOCIETY", "CONFORMITY", "INDIVIDUAL"]
    
    score = 0
    for word in words:
        if len(word) >= 3:
            count = rune_text.count(word)
            score += count * len(word)
    return score

print("\n" + "="*60)
print("TESTING SELF-RELIANCE AS RUNNING KEY")
print("="*60)

# Test different starting positions in Self-Reliance
for page_num in UNSOLVED_PAGES[:5]:  # First 5 unsolved pages
    print(f"\n--- Page {page_num} ---")
    cipher_runes = get_page_runes(page_num)
    
    best_score = 0
    best_start = 0
    best_text = ""
    
    # Try different starting positions
    for start in range(0, min(5000, len(sr_clean) - 300), 50):
        key = sr_to_key(sr_clean, len(cipher_runes), start)
        if len(key) < len(cipher_runes):
            continue
            
        decrypted = decrypt_with_key(cipher_runes, key)
        score = count_english_words(decrypted)
        
        if score > best_score:
            best_score = score
            best_start = start
            best_text = rune_to_letters(decrypted)[:100]
    
    print(f"  Best start position: {best_start}")
    print(f"  Best score: {best_score}")
    print(f"  Text sample: {best_text[:80]}...")
    
    # Show what Self-Reliance text is at that position
    sr_sample = sr_clean[best_start:best_start+50]
    print(f"  SR at position: {sr_sample}...")

# Also try: maybe the key is derived from Self-Reliance by taking first letter of each word
print("\n" + "="*60)
print("TESTING FIRST-LETTER-OF-EACH-WORD KEY")
print("="*60)

# Extract first letters of each word
words_sr = self_reliance.split()
first_letters = ''.join(w[0].upper() for w in words_sr if w and w[0].isalpha())
print(f"First letters key length: {len(first_letters)}")
print(f"First 95 letters: {first_letters[:95]}")

for page_num in UNSOLVED_PAGES[:5]:
    print(f"\n--- Page {page_num} (first-letter) ---")
    cipher_runes = get_page_runes(page_num)
    
    best_score = 0
    best_start = 0
    best_text = ""
    
    for start in range(0, min(1000, len(first_letters) - 100), 10):
        key = [letter_to_shift(c) for c in first_letters[start:start+len(cipher_runes)]]
        if len(key) < len(cipher_runes):
            continue
            
        decrypted = decrypt_with_key(cipher_runes, key)
        score = count_english_words(decrypted)
        
        if score > best_score:
            best_score = score
            best_start = start
            best_text = rune_to_letters(decrypted)[:100]
    
    print(f"  Best start: {best_start}, Score: {best_score}")
    print(f"  Text: {best_text[:80]}...")

# Try: Use paragraph numbers or sentence numbers from Self-Reliance
print("\n" + "="*60)
print("TESTING PAGE NUMBER * OFFSET RELATIONSHIP")
print("="*60)

# Maybe page 27 uses SR starting at position 27*something
for page_num in UNSOLVED_PAGES[:5]:
    print(f"\n--- Page {page_num} (mult test) ---")
    cipher_runes = get_page_runes(page_num)
    
    best_score = 0
    best_mult = 0
    best_text = ""
    
    for mult in range(1, 200):
        start = (page_num * mult) % len(sr_clean)
        key = sr_to_key(sr_clean, len(cipher_runes), start)
        if len(key) < len(cipher_runes):
            continue
            
        decrypted = decrypt_with_key(cipher_runes, key)
        score = count_english_words(decrypted)
        
        if score > best_score:
            best_score = score
            best_mult = mult
            best_text = rune_to_letters(decrypted)[:100]
    
    start_pos = (page_num * best_mult) % len(sr_clean)
    print(f"  Best: page * {best_mult} = start at {start_pos}")
    print(f"  Score: {best_score}")
    print(f"  Text: {best_text[:80]}...")

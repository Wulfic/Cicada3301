#!/usr/bin/env python3
"""
Test the user's pattern: Page N → Word (N-20) from Parable

But instead of just using the word POSITION as offset,
what if the WORD ITSELF is the key for that page?
"""

import re
from pathlib import Path

RUNE_ORDER = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Master key
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

PARABLE = "PARABLELIKETHEINSTARTUNNELNGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIUINITYWITHINANDEMERGE"

# Full Parable broken into words with character positions
PARABLE_WORDS = ["PARABLE", "LIKE", "THE", "INSTAR", "TUNNELNG", "TO", "THE", 
                 "SURFACE", "WE", "MUST", "SHED", "OUR", "OWN", "CIRCUMFERENCES",
                 "FIND", "THE", "DIUINITY", "WITHIN", "AND", "EMERGE"]

def rune_to_idx(r):
    return RUNE_ORDER.index(r) if r in RUNE_ORDER else -1

def idx_to_letter(idx):
    return LETTERS[idx % 29]

def letter_to_idx(letter):
    """Convert letter to rune index"""
    letter = letter.upper()
    if letter in LETTERS:
        return LETTERS.index(letter)
    return -1

def word_to_indices(word):
    """Convert a word to rune indices"""
    result = []
    i = 0
    while i < len(word):
        # Try 2-letter combinations first
        if i + 1 < len(word):
            two_char = word[i:i+2]
            if two_char in LETTERS:
                result.append(LETTERS.index(two_char))
                i += 2
                continue
        # Single letter
        one_char = word[i:i+1]
        if one_char in LETTERS:
            result.append(LETTERS.index(one_char))
        i += 1
    return result

def load_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_ORDER)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def score_english(text):
    """Score how English-like the text is."""
    # Common English bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'AT', 'ON', 'EN', 'ES', 'ED', 'OR', 'TE', 'ST']
    score = 0
    for bg in bigrams:
        score += text.count(bg) * 2
    # Common letters
    common = 'ETAOINSHRDLU'
    score += sum(1 for c in text if c in common)
    return score

def decrypt_with_word(cipher_runes, word):
    """Decrypt cipher using a word as the key (repeated)"""
    key_indices = word_to_indices(word)
    if not key_indices:
        return ""
    
    result = []
    for i, r in enumerate(cipher_runes):
        c_idx = rune_to_idx(r)
        if c_idx < 0:
            continue
        k = key_indices[i % len(key_indices)]
        plain_idx = (c_idx - k) % 29
        result.append(idx_to_letter(plain_idx))
    return ''.join(result)

def main():
    pages = load_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    print("=" * 70)
    print("THEORY: Page N → Use Word (N-20) as the KEY")
    print("Based on pattern: 27→SURFACE, 28→WE, 29→MUST, 30→SHED, 31→OUR")
    print("=" * 70)
    
    for page_num in unsolved:
        if page_num not in pages:
            continue
        
        cipher = pages[page_num]
        word_idx = (page_num - 20) % len(PARABLE_WORDS)
        word = PARABLE_WORDS[word_idx]
        
        decrypted = decrypt_with_word(cipher, word)
        score = score_english(decrypted)
        
        print(f"\nPage {page_num} → Word [{word_idx}] = '{word}'")
        print(f"  Key indices: {word_to_indices(word)}")
        print(f"  Decrypted: {decrypted[:60]}...")
        print(f"  Score: {score}")

    print("\n" + "=" * 70)
    print("THEORY 2: Try ALL words as key for each page")
    print("=" * 70)
    
    for page_num in [27, 28, 29]:
        if page_num not in pages:
            continue
        
        cipher = pages[page_num]
        print(f"\nPage {page_num}:")
        
        results = []
        for word in PARABLE_WORDS:
            decrypted = decrypt_with_word(cipher, word)
            score = score_english(decrypted)
            results.append((score, word, decrypted))
        
        # Sort by score
        results.sort(reverse=True)
        for score, word, text in results[:5]:
            print(f"  '{word}': score={score}, text={text[:40]}...")

    print("\n" + "=" * 70)
    print("THEORY 3: Page number as Gematria determines key segment")
    print("Using page number's Gematria sum to select key start")
    print("=" * 70)
    
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    for page_num in [27, 28, 29, 30, 31]:
        if page_num not in pages:
            continue
        
        cipher = pages[page_num]
        
        # Theory: page_num itself is a "number" - what's its gematria?
        # Or interpret page digits as rune indices
        
        # Try: sum of digits as offset
        digit_sum = sum(int(d) for d in str(page_num))
        
        # Try: page number mod 95 as offset
        offset = page_num % 95
        
        # Try: page number's prime as offset (page 27 → 27th item in something)
        
        result = []
        for i, r in enumerate(cipher):
            c_idx = rune_to_idx(r)
            if c_idx < 0:
                continue
            k = MASTER_KEY[(i + offset) % 95]
            plain_idx = (c_idx - k) % 29
            result.append(idx_to_letter(plain_idx))
        
        decrypted = ''.join(result)
        score = score_english(decrypted)
        
        print(f"Page {page_num}: offset={offset}, digit_sum={digit_sum}")
        print(f"  Text: {decrypted[:60]}...")

if __name__ == "__main__":
    main()

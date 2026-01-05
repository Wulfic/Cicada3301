"""
AUTOKEY CIPHER DEEP EXPLORATION
================================

Autokey cipher uses plaintext to extend the key.
Key len 13, start 2 gave 66.98% vowels on Page 27.
"""

import numpy as np
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᛡᛠᚪᚫᚣ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
         'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
         'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

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

def autokey_decrypt(ciphertext, initial_key):
    """Decrypt using autokey cipher - key extended with plaintext"""
    n = len(ciphertext)
    key = list(initial_key)
    plaintext = []
    
    for i in range(n):
        if i < len(initial_key):
            key_val = key[i]
        else:
            key_val = plaintext[i - len(initial_key)]
        plain_val = (ciphertext[i] - key_val) % 29
        plaintext.append(plain_val)
    
    return np.array(plaintext)

def autokey_ciphertext(ciphertext, initial_key):
    """Decrypt using autokey cipher - key extended with CIPHERTEXT (different variant)"""
    n = len(ciphertext)
    plaintext = []
    
    for i in range(n):
        if i < len(initial_key):
            key_val = initial_key[i]
        else:
            key_val = ciphertext[i - len(initial_key)]
        plain_val = (ciphertext[i] - key_val) % 29
        plaintext.append(plain_val)
    
    return np.array(plaintext)

print("=" * 80)
print("AUTOKEY CIPHER SCAN - FULL MASTER KEY")
print("=" * 80)

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    # Autokey with full master key
    decrypted = autokey_decrypt(pg_idx, MASTER_KEY)
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    print(f"Page {pg_num} autokey (master key): score {score}")
    if score > 25:
        print(f"  {text[:70]}...")
    
    # Autokey with ciphertext feedback
    decrypted2 = autokey_ciphertext(pg_idx, MASTER_KEY)
    text2 = indices_to_text(decrypted2)
    score2 = word_score(text2)
    
    print(f"Page {pg_num} autokey-ciphertext: score {score2}")
    if score2 > 25:
        print(f"  {text2[:70]}...")

print()
print("=" * 80)
print("PROGRESSIVE KEY - KEY SHIFTS EACH POSITION")
print("=" * 80)
print("What if the key advances differently than 1-to-1?")

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    best_score = 0
    best_text = ""
    best_step = 0
    
    for step in range(1, 30):  # Try different step sizes
        # Key advances by 'step' for each ciphertext character
        key_positions = [(i * step) % len(MASTER_KEY) for i in range(n)]
        key_vals = np.array([MASTER_KEY[pos] for pos in key_positions])
        
        decrypted = (pg_idx - key_vals) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score > best_score:
            best_score = score
            best_text = text
            best_step = step
    
    print(f"Page {pg_num}: best step {best_step}, score {best_score}")
    if best_score > 25:
        print(f"  {best_text[:70]}...")

print()
print("=" * 80)
print("SKIP CIPHER - READ EVERY Nth RUNE")
print("=" * 80)
print("What if we need to read every Nth rune, then decrypt?")

for pg_num, page_data in list(UNSOLVED_PAGES.items())[:2]:
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    for skip in [2, 3, 5, 7, 11, 13]:
        # Read every Nth rune, wrapping
        reordered = []
        visited = set()
        pos = 0
        while len(visited) < n:
            if pos not in visited:
                reordered.append(pg_idx[pos])
                visited.add(pos)
            pos = (pos + skip) % n
            if len(visited) == n:
                break
            # Safety check for coprime issues
            if pos in visited:
                # Find next unvisited
                for p in range(n):
                    if p not in visited:
                        pos = p
                        break
        
        reordered = np.array(reordered)
        key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
        
        decrypted = (reordered - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score > 25:
            print(f"Page {pg_num} skip {skip}: score {score}")
            print(f"  {text[:70]}...")

print()
print("=" * 80)
print("REVERSE READING DIRECTION")
print("=" * 80)

for pg_num, page_data in UNSOLVED_PAGES.items():
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    key_ext = np.tile(MASTER_KEY, (n // len(MASTER_KEY)) + 1)[:n]
    
    # Reverse the ciphertext
    pg_rev = pg_idx[::-1]
    decrypted = (pg_rev - key_ext) % 29
    text = indices_to_text(decrypted)
    score = word_score(text)
    
    if score > 20:
        print(f"Page {pg_num} reversed: score {score}")
        print(f"  {text[:70]}...")
    
    # Reverse the key
    key_rev = key_ext[::-1]
    decrypted2 = (pg_idx - key_rev) % 29
    text2 = indices_to_text(decrypted2)
    score2 = word_score(text2)
    
    if score2 > 20:
        print(f"Page {pg_num} reverse key: score {score2}")
        print(f"  {text2[:70]}...")

print()
print("=" * 80)
print("BOUSTROPHEDON READING (ALTERNATING DIRECTIONS)")
print("=" * 80)

for pg_num, page_data in list(UNSOLVED_PAGES.items())[:2]:
    pg_idx = np.array([RUNE_TO_INDEX[r] for r in page_data])
    n = len(pg_idx)
    
    for line_len in [7, 10, 11, 13, 14, 15]:
        # Split into lines, reverse alternate lines
        lines = [pg_idx[i:i+line_len] for i in range(0, n, line_len)]
        boustro = []
        for i, line in enumerate(lines):
            if i % 2 == 1:
                boustro.extend(line[::-1])
            else:
                boustro.extend(line)
        
        boustro = np.array(boustro)
        key_ext = np.tile(MASTER_KEY, (len(boustro) // len(MASTER_KEY)) + 1)[:len(boustro)]
        
        decrypted = (boustro - key_ext) % 29
        text = indices_to_text(decrypted)
        score = word_score(text)
        
        if score > 30:
            print(f"Page {pg_num} boustrophedon (line={line_len}): score {score}")
            print(f"  {text[:70]}...")

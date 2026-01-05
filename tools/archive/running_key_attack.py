#!/usr/bin/env python3
"""
RUNNING KEY / KNOWN TEXT ATTACK
===============================

Cicada 3301 uses philosophical texts. Let's try using known texts as running keys:
- The Parable itself (Page 57)
- Self-Reliance by Emerson (known Cicada reference)
- The Book of the Law (Liber AL vel Legis)
- Gematria Primus prime values

For each text, we try using it as a running key to decrypt each page.
"""

import re
import numpy as np
from pathlib import Path

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}
LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def text_to_indices(text):
    """Convert text like 'PARABLELIKETHE...' to indices"""
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Try 2-char tokens first
        if i+1 < len(text):
            two_char = text[i:i+2]
            if two_char in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[two_char])
                i += 2
                continue
        # Single char
        if text[i] in 'FUORCGWHNIJPXSTBEMLDAY':
            for j, letter in enumerate(LETTERS):
                if len(letter) == 1 and letter == text[i]:
                    indices.append(j)
                    break
        i += 1
    return np.array(indices, dtype=np.int32)

def load_all_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_only
    return pages

def score_text(text):
    """Score how English-like the text is"""
    score = 0
    
    common_words = {'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'THIS',
                    'AN', 'BE', 'IT', 'IS', 'TO', 'OF', 'IN', 'HE', 'WE', 'OR',
                    'AS', 'AT', 'BY', 'IF', 'NO', 'SO', 'ON', 'UP', 'MY', 'DO'}
    cicada_words = {'INSTAR', 'PARABLE', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
                    'WITHIN', 'SURFACE', 'SHED', 'PRIME', 'TRUTH', 'WISDOM',
                    'SELF', 'MIND', 'CONSCIOUSNESS', 'ENLIGHTENMENT', 'PILGRIM'}
    
    for word in common_words:
        count = text.count(word)
        score += count * len(word) * 3
    for word in cicada_words:
        count = text.count(word)
        score += count * len(word) * 10
    
    return score

# ==================== KNOWN TEXTS ====================

# The Parable (Page 57 plaintext)
PARABLE = """
PARABLE LIKE THE INSTAR TUNNELING TO THE SURFACE WE MUST SHED OUR OWN 
CIRCUMFERENCES FIND THE DIVINITY WITHIN AND EMERGE
"""

# Self-Reliance by Emerson (opening)
SELF_RELIANCE = """
THERE IS A TIME IN EVERY MANS EDUCATION WHEN HE ARRIVES AT THE CONVICTION 
THAT ENVY IS IGNORANCE THAT IMITATION IS SUICIDE THAT HE MUST TAKE HIMSELF 
FOR BETTER FOR WORSE AS HIS PORTION
"""

# The Book of the Law opening
LIBER_AL = """
HAD NUIT THE MANIFESTATION OF NUIT NONE BREATHED THE LIGHT FAINT AND FAERY 
OF THE STARS AND TWO THE UNVEILING OF THE COMPANY OF HEAVEN EVERY MAN AND 
EVERY WOMAN IS A STAR
"""

# Warning page text (from Liber Primus)
WARNING = """
WELCOME PILGRIM TO THE GREAT JOURNEY TOWARD THE END OF ALL THINGS IT IS NOT 
AN EASY TRIP BUT FOR THOSE WHO FIND THEIR WAY HERE IT IS A NECESSARY ONE
"""

# Known solved sections
SOLVEDP56 = """
THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED ALL THINGS ARE SACRED
"""

def clean_text(text):
    """Remove non-alpha characters and convert to uppercase"""
    return ''.join(c for c in text.upper() if c.isalpha())

def main():
    print("="*70)
    print("RUNNING KEY / KNOWN TEXT ATTACK")
    print("="*70)
    
    pages = load_all_pages()
    unsolved = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]
    
    # Prepare running keys
    known_texts = {
        'PARABLE': PARABLE,
        'SELF_RELIANCE': SELF_RELIANCE,
        'LIBER_AL': LIBER_AL,
        'WARNING': WARNING,
        'SOLVED_P56': SOLVEDP56,
    }
    
    running_keys = {}
    for name, text in known_texts.items():
        cleaned = clean_text(text)
        # Replace K->C (Futhorc has no K)
        cleaned = cleaned.replace('K', 'C')
        indices = text_to_indices(cleaned)
        running_keys[name] = indices
        print(f"Running key '{name}': {len(indices)} indices")
    
    # Also create the derived master key
    page0_idx = runes_to_indices(pages[0])
    page57_idx = runes_to_indices(pages[57])
    master_key = (page0_idx[:len(page57_idx)] - page57_idx) % 29
    running_keys['MASTER_KEY'] = master_key
    print(f"Running key 'MASTER_KEY': {len(master_key)} indices")
    
    # For each page, try each running key at different offsets
    results = []
    
    for pg_num in unsolved:
        pg_idx = runes_to_indices(pages[pg_num])
        pg_len = len(pg_idx)
        
        for key_name, key_indices in running_keys.items():
            key_len = len(key_indices)
            
            # Try different offsets into the running key
            for offset in range(0, min(key_len, 100), 5):  # Every 5 positions
                # Extract key starting at offset
                key = np.tile(key_indices, (pg_len // key_len + 2))
                key = key[offset:offset + pg_len]
                
                # Try subtraction
                decrypted = (pg_idx - key) % 29
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score > 30:
                    results.append((pg_num, key_name, 'sub', offset, score, text[:80]))
                
                # Try addition
                decrypted = (pg_idx + key) % 29
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score > 30:
                    results.append((pg_num, key_name, 'add', offset, score, text[:80]))
                
                # Try XOR
                decrypted = pg_idx ^ key
                decrypted = decrypted % 29  # Keep in range
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score > 30:
                    results.append((pg_num, key_name, 'xor', offset, score, text[:80]))
    
    # Sort by score
    results.sort(key=lambda x: -x[4])
    
    print("\n" + "="*70)
    print("TOP RESULTS")
    print("="*70)
    
    for pg, key, op, off, score, text in results[:30]:
        print(f"\nPage {pg} | key={key} | op={op} | offset={off} | score={score}")
        print(f"  {text}")
    
    # Now let's try autokey cipher
    print("\n" + "="*70)
    print("AUTOKEY CIPHER TEST")
    print("="*70)
    
    # In autokey, each plaintext character becomes part of the key
    # Key = initial_key + plaintext
    
    for pg_num in unsolved[:5]:  # Just first 5 pages
        pg_idx = runes_to_indices(pages[pg_num])
        
        # Try different initial key lengths and values
        for init_len in range(1, 10):
            for init_val in range(0, 29, 7):  # Sample values
                init_key = np.full(init_len, init_val, dtype=np.int32)
                
                # Autokey decryption
                decrypted = np.zeros(len(pg_idx), dtype=np.int32)
                key = init_key.tolist()
                
                for i in range(len(pg_idx)):
                    k = key[i] if i < len(key) else decrypted[i - len(init_key)]
                    decrypted[i] = (pg_idx[i] - k) % 29
                    if i >= len(init_key):
                        key.append(decrypted[i])
                
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score > 30:
                    print(f"Page {pg_num} | init_len={init_len} | init_val={init_val} | score={score}")
                    print(f"  {text[:80]}")
    
    # Try using other solved pages as running keys
    print("\n" + "="*70)
    print("CROSS-PAGE RUNNING KEYS")
    print("="*70)
    
    # Use each page as a potential running key for other pages
    source_pages = list(pages.keys())
    
    for target in unsolved[:5]:
        target_idx = runes_to_indices(pages[target])
        best = (0, None, None)
        
        for source in source_pages:
            if source == target:
                continue
            
            source_idx = runes_to_indices(pages[source])
            
            # Extend source to cover target
            extended = np.tile(source_idx, (len(target_idx) // len(source_idx) + 1))[:len(target_idx)]
            
            decrypted = (target_idx - extended) % 29
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > best[0]:
                best = (score, source, text[:80])
        
        if best[0] > 20:
            print(f"\nPage {target} best with Page {best[1]} as key (score={best[0]})")
            print(f"  {best[2]}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SOLVED PAGES RUNNING KEY ATTACK
================================
Use the plaintext from solved pages (59, 63, 64, 68) as running keys
to decrypt the unsolved pages (18-54).

The theory: Cicada might have used earlier solved content to encrypt later pages,
creating a "chain" where solving one page unlocks the next.

Author: Wulfic
Date: January 2026
"""

import os
from pathlib import Path

# Gematria Primus
GEMATRIA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101),'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107),'ᛠ': (28, 'EA', 109)
}

ALPHABET_SIZE = 29
RUNE_TO_INDEX = {k: v[0] for k, v in GEMATRIA.items()}
INDEX_TO_LATIN = {v[0]: v[1] for k, v in GEMATRIA.items()}

# Latin to Index
LATIN_TO_INDEX = {}
for k, v in GEMATRIA.items():
    latin = v[1]
    idx = v[0]
    if latin not in LATIN_TO_INDEX:
        LATIN_TO_INDEX[latin] = idx
    if len(latin) == 1:
        LATIN_TO_INDEX[latin] = idx
LATIN_TO_INDEX['K'] = LATIN_TO_INDEX['C']

# Solved page plaintexts
SOLVED_PAGES = {
    59: """A WARNING BELIEVE NOTHING FROM THIS BOOK EXCEPT WHAT YOU KNOW TO BE TRUE 
TEST THE KNOWLEDGE FIND YOUR TRUTH EXPERIENCE YOUR DEATH 
DO NOT EDIT OR CHANGE THIS BOOK OR THE MESSAGE CONTAINED WITHIN 
EITHER THE WORDS OR THEIR NUMBERS FOR ALL IS SACRED""",
    
    63: """SOME WISDOM THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED 
ALL THINGS SHOULD BE ENCRYPTED KNOW THIS 
SHADOWS AETHEREAL BUFFER SUOID CARNAL 
OBSCURA FORM MOBIUS ANALOGUOID MOURNFUL AETHEREAL CABAL""",
    
    64: """A KOAN A MAN DECIDED TO GO AND STUDY WITH A MASTER 
HE WENT TO THE DOOR OF THE MASTER 
WHO ARE YOU WHO WISHES TO STUDY HERE ASKED THE MASTER 
THE STUDENT TOLD THE MASTER HIS NAME 
THAT IS NOT WHAT YOU ARE THAT IS ONLY WHAT YOU ARE CALLED 
WHO ARE YOU WHO WISHES TO STUDY HERE HE ASKED AGAIN 
THE MAN THOUGHT FOR A MOMENT AND REPLIED I AM A PROFESSOR 
THAT IS WHAT YOU DO NOT WHAT YOU ARE 
WHO ARE YOU WHO WISHES TO STUDY HERE 
CONFUSED THE MAN THOUGHT SOME MORE 
FINALLY HE ANSWERED I AM A HUMAN BEING 
THAT IS ONLY YOUR SPECIES NOT WHO YOU ARE 
WHO ARE YOU WHO WISHES TO STUDY HERE ASKED THE MASTER AGAIN 
AFTER A MOMENT OF THOUGHT THE PROFESSOR REPLIED I AM A CONSCIOUSNESS INHABITING AN ARBITRARY BODY 
THAT IS MERELY WHAT YOU ARE NOT WHO YOU ARE 
WHO ARE YOU WHO WISHES TO STUDY HERE 
THE MAN WAS GETTING IRRITATED 
I HE STARTED BUT HE COULD NOT THINK OF ANYTHING ELSE TO SAY SO HE TRAILED OFF""",
    
    68: """THE LOSS OF DIVINITY THE CIRCUMFERENCE PRACTICES THREE BEHAVIORS WHICH CAUSE THE LOSS OF DIVINITY 
CONSUMPTION WE CONSUME TOO MUCH BECAUSE WE BELIEVE THE FOLLOWING TWO ERRORS WITHIN THE DECEPTION 
WE DO NOT HAVE ENOUGH OR THERE IS NOT ENOUGH 
WE HAVE WHAT WE HAVE NOW BY LUCK AND WE WILL NOT BE STRONG ENOUGH LATER TO OBTAIN WHAT WE NEED 
MOST THINGS ARE NOT WORTH CONSUMING"""
}

def text_to_indices(text):
    """Convert text to list of Gematria indices."""
    text = text.upper().replace(' ', '').replace('\n', '')
    result = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_INDEX:
                result.append(LATIN_TO_INDEX[digraph])
                i += 2
                continue
        # Single character
        if text[i] in LATIN_TO_INDEX:
            result.append(LATIN_TO_INDEX[text[i]])
        i += 1
    return result

def runes_to_indices(rune_text):
    """Convert rune string to list of indices."""
    indices = []
    for char in rune_text:
        if char in RUNE_TO_INDEX:
            indices.append(RUNE_TO_INDEX[char])
    return indices

def indices_to_latin(indices):
    """Convert indices to Latin text."""
    return ''.join(INDEX_TO_LATIN.get(i, '?') for i in indices)

def running_key_decrypt(cipher, key, mode='SUB'):
    """Decrypt using running key (key is as long as cipher, taken from source text)."""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]  # Cycle if key is shorter
        if mode == 'SUB':
            result.append((c - k) % ALPHABET_SIZE)
        elif mode == 'ADD':
            result.append((c + k) % ALPHABET_SIZE)
        elif mode == 'SUB_REV':
            result.append((k - c) % ALPHABET_SIZE)
    return result

def calculate_ioc(indices):
    """Calculate Index of Coincidence."""
    if len(indices) < 2:
        return 0.0
    freq = [0] * ALPHABET_SIZE
    for idx in indices:
        freq[idx] += 1
    n = len(indices)
    ioc = sum(f * (f - 1) for f in freq) / (n * (n - 1))
    return ioc

# Common English trigrams
TRIGRAMS = {
    'THE': 100, 'AND': 80, 'ING': 75, 'HER': 65, 'HAT': 60,
    'HIS': 55, 'THA': 50, 'ERE': 48, 'FOR': 45, 'ENT': 43,
    'ION': 42, 'TER': 40, 'WAS': 38, 'YOU': 37, 'ITH': 36,
    'VER': 35, 'ALL': 34, 'WIT': 33, 'THI': 32, 'TIO': 31
}

COMMON_WORDS = [
    'THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'YOU',
    'THIS', 'BUT', 'HIS', 'FROM', 'THEY', 'SAY', 'HER', 'SHE',
    'WILL', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
    'PRIMES', 'SACRED', 'WISDOM', 'TRUTH', 'DIVINITY', 'CIRCUMFERENCE',
    'CONSUMPTION', 'BELIEF', 'KNOWLEDGE', 'ENLIGHTENMENT',
    'WARNING', 'BELIEVE', 'NOTHING', 'KNOW', 'TRUE', 'TEST'
]

def score_text(text):
    """Score decrypted text."""
    score = 0
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in TRIGRAMS:
            score += TRIGRAMS[trigram]
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def load_page(page_num, base_path):
    """Load runes from a page."""
    page_dir = base_path / 'pages' / f'page_{page_num:02d}'
    runes_file = page_dir / 'runes.txt'
    if runes_file.exists():
        with open(runes_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def main():
    print("=" * 70)
    print("SOLVED PAGES AS RUNNING KEY ATTACK")
    print("=" * 70)
    
    base_path = Path(__file__).parent.parent
    
    # Convert solved pages to indices
    solved_keys = {}
    for page_num, plaintext in SOLVED_PAGES.items():
        key = text_to_indices(plaintext)
        solved_keys[page_num] = key
        print(f"Page {page_num} key length: {len(key)}")
    
    # Combine all solved pages into one long key
    combined_key = []
    for page_num in sorted(SOLVED_PAGES.keys()):
        combined_key.extend(solved_keys[page_num])
    print(f"\nCombined key length: {len(combined_key)}")
    
    # Test pages
    test_pages = list(range(18, 55))
    
    results = []
    
    print("\n" + "=" * 70)
    print("TESTING INDIVIDUAL SOLVED PAGES AS KEYS")
    print("=" * 70)
    
    for target_page in test_pages:
        rune_text = load_page(target_page, base_path)
        if not rune_text:
            continue
        
        cipher = runes_to_indices(rune_text)
        if len(cipher) < 50:
            continue
        
        best_result = None
        best_score = 0
        
        # Try each solved page as key
        for key_page, key in solved_keys.items():
            for mode in ['SUB', 'ADD', 'SUB_REV']:
                for offset in [0, 100, 200, 300, 400, 500]:  # Try different starting positions
                    shifted_key = key[offset:] + key[:offset] if offset < len(key) else key
                    plaintext = running_key_decrypt(cipher, shifted_key, mode)
                    text = indices_to_latin(plaintext)
                    score = score_text(text)
                    ioc = calculate_ioc(plaintext)
                    
                    if score > best_score or ioc > 0.055:
                        best_score = score
                        best_result = (key_page, mode, offset, score, ioc, text[:80])
                        
                        if score > 1000 or ioc > 0.06:
                            print(f"\nPage {target_page} | Key=P{key_page} Off={offset} {mode}")
                            print(f"  Score={score} IoC={ioc:.4f}")
                            print(f"  {text[:80]}...")
        
        # Try combined key
        for mode in ['SUB', 'ADD', 'SUB_REV']:
            for offset in range(0, min(1000, len(combined_key)), 100):
                shifted_key = combined_key[offset:] + combined_key[:offset]
                plaintext = running_key_decrypt(cipher, shifted_key, mode)
                text = indices_to_latin(plaintext)
                score = score_text(text)
                ioc = calculate_ioc(plaintext)
                
                if score > best_score:
                    best_score = score
                    best_result = ('COMBINED', mode, offset, score, ioc, text[:80])
                    
                    if score > 1000 or ioc > 0.06:
                        print(f"\nPage {target_page} | COMBINED Off={offset} {mode}")
                        print(f"  Score={score} IoC={ioc:.4f}")
                        print(f"  {text[:80]}...")
        
        if best_result:
            results.append((target_page, best_result))
    
    # Summary
    print("\n" + "=" * 70)
    print("BEST RESULTS SUMMARY")
    print("=" * 70)
    
    for target_page, (key_page, mode, offset, score, ioc, text) in sorted(results, key=lambda x: -x[1][3])[:20]:
        print(f"Page {target_page}: Key=P{key_page} Off={offset} {mode} Score={score} IoC={ioc:.4f}")

if __name__ == '__main__':
    main()

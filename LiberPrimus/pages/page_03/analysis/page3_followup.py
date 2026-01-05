#!/usr/bin/env python3
"""
Follow-up investigation of Page 3 findings:
1. Caesar shift 13 on the key-83 decryption
2. "A PARABLE" as known plaintext
3. Master key offset 91
"""

from pathlib import Path
from collections import Counter

# Constants
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def indices_to_text(indices):
    return "".join(LETTERS[i] for i in indices)

def text_to_indices(text):
    result = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph in LETTERS:
                result.append(LETTERS.index(digraph))
                i += 2
                continue
        if text[i] in LETTERS:
            result.append(LETTERS.index(text[i]))
        i += 1
    return result

def decrypt_sub(cipher, key, offset=0):
    plaintext = []
    for i, c in enumerate(cipher):
        k = key[(i + offset) % len(key)]
        plaintext.append((c - k) % 29)
    return plaintext

def score_english(text):
    text = text.upper()
    score = 0.0
    
    trigrams = {
        'THE': 50, 'AND': 30, 'ING': 25, 'ION': 20, 'ENT': 15,
        'FOR': 15, 'TIO': 15, 'ERE': 15, 'HER': 15, 'ATE': 15,
        'ITH': 12, 'WIT': 12, 'HIS': 12, 'OUR': 12, 'ALL': 12,
    }
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    bigrams = {
        'TH': 20, 'HE': 18, 'IN': 15, 'ER': 14, 'AN': 13,
        'RE': 12, 'ON': 11, 'AT': 11, 'EN': 10, 'ND': 10,
    }
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    keywords = {
        'WISDOM': 100, 'TRUTH': 100, 'DIVINE': 100, 'EMERGE': 100,
        'INSTAR': 120, 'PARABLE': 100, 'PRIMES': 100, 'SACRED': 100,
    }
    for kw, bonus in keywords.items():
        score += text.count(kw) * bonus
    
    return score

def load_page3():
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = content.split('%')
    page3_raw = pages[2]
    indices = [RUNE_TO_INDEX[c] for c in page3_raw if c in RUNE_TO_INDEX]
    return indices

def main():
    cipher = load_page3()
    print(f"Page 3: {len(cipher)} runes")
    
    print("\n" + "=" * 80)
    print("INVESTIGATION 1: Key-83 Decryption + Caesar Shift 13")
    print("=" * 80)
    
    # First decrypt with key-83 (frequency-based)
    key83 = []
    for i in range(83):
        coset = [cipher[j] for j in range(i, len(cipher), 83)]
        if coset:
            most_common = Counter(coset).most_common(1)[0][0]
            key83.append((most_common - 18) % 29)
        else:
            key83.append(0)
    
    plaintext83 = decrypt_sub(cipher, key83)
    
    # Apply Caesar shift 13
    shifted = [(p + 13) % 29 for p in plaintext83]
    shifted_text = indices_to_text(shifted)
    print(f"\nKey-83 + Caesar 13: {shifted_text}")
    print(f"Score: {score_english(shifted_text):.1f}")
    
    # Try all shifts
    print("\nAll Caesar shifts on key-83 decryption:")
    best_shift = 0
    best_score = 0
    for shift in range(29):
        shifted = [(p + shift) % 29 for p in plaintext83]
        text = indices_to_text(shifted)
        score = score_english(text)
        if score > best_score:
            best_score = score
            best_shift = shift
        if score > 400:
            print(f"  Shift {shift:2d}: Score {score:6.1f} | {text[:70]}...")
    
    print(f"\nBest shift: {best_shift} with score {best_score:.1f}")
    best_shifted = [(p + best_shift) % 29 for p in plaintext83]
    best_text = indices_to_text(best_shifted)
    print(f"Text: {best_text}")
    
    print("\n" + "=" * 80)
    print("INVESTIGATION 2: Master Key Offset 91")
    print("=" * 80)
    
    plaintext91 = decrypt_sub(cipher, MASTER_KEY, 91)
    text91 = indices_to_text(plaintext91)
    print(f"\nMaster key offset 91: {text91}")
    print(f"Score: {score_english(text91):.1f}")
    
    # Try Caesar on this too
    print("\nCaesar shifts on master-key-91 decryption:")
    for shift in range(29):
        shifted = [(p + shift) % 29 for p in plaintext91]
        text = indices_to_text(shifted)
        score = score_english(text)
        if score > 400:
            print(f"  Shift {shift:2d}: Score {score:6.1f} | {text[:70]}...")
    
    print("\n" + "=" * 80)
    print("INVESTIGATION 3: 'A PARABLE' as Known Plaintext")
    print("=" * 80)
    
    # If page 3 starts with "A PARABLE"
    known = "APARABLE"
    known_idx = text_to_indices(known)
    print(f"\n'{known}' = indices {known_idx}")
    
    # Derive key from known: key[i] = (cipher[i] - known[i]) mod 29
    derived_key = []
    for i in range(len(known_idx)):
        k = (cipher[i] - known_idx[i]) % 29
        derived_key.append(k)
        print(f"  Position {i}: cipher={cipher[i]} - known={known_idx[i]} = key={k}")
    
    print(f"\nDerived key fragment: {derived_key}")
    
    # Try extending this key to different lengths
    for klen in [71, 79, 83, 89, 97]:
        extended_key = (derived_key * ((klen // len(derived_key)) + 1))[:klen]
        plaintext = decrypt_sub(cipher, extended_key)
        text = indices_to_text(plaintext)
        score = score_english(text)
        print(f"\n  Extended to {klen}: Score {score:.1f}")
        print(f"    {text[:80]}...")
    
    print("\n" + "=" * 80)
    print("INVESTIGATION 4: Direct Key Derivation from Solved Pages")
    print("=" * 80)
    
    # Page 1 key length 71, Page 2 key length 83, Page 3 key length 83
    # What if there's a pattern in how keys are derived?
    
    # Try using first N values of master key where N is our key length
    print("\nUsing first 83 values of master key:")
    partial_master = MASTER_KEY[:83] + MASTER_KEY[:83 - len(MASTER_KEY)] if 83 > len(MASTER_KEY) else MASTER_KEY[:83]
    # Pad if needed
    while len(partial_master) < 83:
        partial_master.append(0)
    
    plaintext_pm = decrypt_sub(cipher, partial_master)
    text_pm = indices_to_text(plaintext_pm)
    print(f"  Text: {text_pm[:100]}...")
    print(f"  Score: {score_english(text_pm):.1f}")
    
    print("\n" + "=" * 80)
    print("INVESTIGATION 5: Word-by-Word Analysis")
    print("=" * 80)
    
    # Parse word boundaries from original
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = content.split('%')
    page3_raw = pages[2]
    
    # Extract words
    words_raw = []
    current = []
    for c in page3_raw:
        if c in RUNE_TO_INDEX:
            current.append(RUNE_TO_INDEX[c])
        elif c in ['-', '.', '/', '&', '$']:
            if current:
                words_raw.append(current)
                current = []
    if current:
        words_raw.append(current)
    
    print(f"\n{len(words_raw)} words found")
    
    # For each word, try to find what it could decrypt to
    print("\nWord analysis with master key offset 91:")
    pos = 0
    for i, word in enumerate(words_raw[:15]):
        word_plain = []
        for j, c in enumerate(word):
            k = MASTER_KEY[(pos + j + 91) % 95]
            p = (c - k) % 29
            word_plain.append(p)
        decrypted_word = indices_to_text(word_plain)
        pos += len(word)
        print(f"  Word {i+1:2d}: {indices_to_text(word):12s} -> {decrypted_word}")

if __name__ == "__main__":
    main()

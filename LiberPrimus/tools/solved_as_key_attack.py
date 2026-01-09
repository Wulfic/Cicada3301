#!/usr/bin/env python3
"""
SOLVED PAGES AS RUNNING KEY ATTACK

Hypothesis: Unsolved pages (18+) use the combined plaintext from solved pages (00-17)
as a running key. This would be classic Cicada style - requiring solved pages to solve new ones.

Tests:
1. Use combined solved page plaintext as running key
2. Use individual solved pages as keys for specific target pages  
3. Use solved pages in reverse order
4. Use key with offsets
"""

import os
import sys
import re

# Gematria Primus mapping (Latin to index)
GP_LATIN_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4,
    'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8,
    'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18,
    'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27,
    'EA': 28
}

GP_INDEX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R',
    5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X',
    15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M',
    20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A',
    25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(SCRIPT_DIR, "..", "pages")
RUNEGLISH_DIR = os.path.join(SCRIPT_DIR, "..", "runeglish_output")

# Known solved page plaintexts (from MASTER_SOLVING_DOC)
SOLVED_PLAINTEXTS = {
    0: "WELCOME",
    1: "PILGRIM TO THE DARK LANDS YOUR SOUL IS BEING TESTED",
    3: "SOME WISDOM THE PRIMES ARE SACRED WITHIN THEM IS FOUND THE FIRST SEVEN PRIMES IN THE FIBONACCI SEQUENCE A CLUE WITHIN YOUR GRASP THE SACRED VORTEX BE OPEN TO THE FOURTH DIMENSION A SACRED SIGN BECKONS",
    5: "TO FIND THE NEXT STOP GO TO THE COORDINATES BELOW AND SPEAK THE PASSPHRASERUNETOINUMBER.COM",
    8: "COMMANDMENTS SPEAK NOT OF YOURSELF NOR TRUST YOUR OWN JUDGEMENT FOR IT IS POOR AND MAKES YOU WEAK",
    9: "BELIEVE NOTHING OF OTHERS AND TRUST NOT IN YOURSELF ONLY",
    10: "COVET NOTHING THAT IS NOT YOURS NEITHER TAKE NOR STEAL NOR HARM FOR IT IS AGAINST THE PRINCIPLES",
    11: "DO NOT KILL YOUR BROTHERS AND SISTERS UNLESS IT IS FOR THEIR OWN GOOD OR YOURS",
    12: "ENSLAVE NOT FOR ALL ARE BORN FREE",
    13: "CHILDREN HAVE MINDS OF THEIR OWN BE OPEN TO THEM FOR THEY ARE YOUR FUTURE",
    14: "SEEK NOT TO WORSHIP FOR YOU ARE ALREADY DIVINE",
    15: "SHUN NOT OTHERS FOR THEIR BELIEFS BUT SEEK TO UNDERSTAND",
    16: "WISDOM IS POWER BUT SHARE IT FREELY",
    17: "EPILOGUE",  # Note: Only title confirmed, body not fully solved
}

def text_to_indices(text: str) -> list[int]:
    """Convert text to Gematria Primus indices."""
    indices = []
    text = text.upper().replace(" ", "").replace("-", "").replace(".", "")
    i = 0
    while i < len(text):
        # Try 3-char combos first
        if i + 2 < len(text):
            tri = text[i:i+3]
            if tri in GP_LATIN_TO_INDEX:
                indices.append(GP_LATIN_TO_INDEX[tri])
                i += 3
                continue
        # Try 2-char combos
        if i + 1 < len(text):
            di = text[i:i+2]
            if di in GP_LATIN_TO_INDEX:
                indices.append(GP_LATIN_TO_INDEX[di])
                i += 2
                continue
        # Single char
        ch = text[i]
        if ch in GP_LATIN_TO_INDEX:
            indices.append(GP_LATIN_TO_INDEX[ch])
        i += 1
    return indices

def indices_to_text(indices: list[int]) -> str:
    """Convert indices back to text."""
    return "".join(GP_INDEX_TO_LATIN.get(i, "?") for i in indices)

def load_runeglish(page_num: int) -> list[int]:
    """Load runeglish and convert to indices."""
    filename = os.path.join(RUNEGLISH_DIR, f"page_{page_num:02d}_runeglish.txt")
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        content = f.read()
    return text_to_indices(content)

def decrypt_sub(cipher: list[int], key: list[int]) -> list[int]:
    """SUB mode: P = (C - K) mod 29"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)] if key else 0
        p = (c - k) % 29
        result.append(p)
    return result

def decrypt_add(cipher: list[int], key: list[int]) -> list[int]:
    """ADD mode: P = (C + K) mod 29"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)] if key else 0
        p = (c + k) % 29
        result.append(p)
    return result

def score_text(text: str) -> float:
    """Score based on English-like patterns."""
    score = 0.0
    common_words = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'THAT', 'WAS',
                    'FOR', 'ON', 'WITH', 'AS', 'AT', 'BY', 'NOT', 'ARE', 'ALL', 'FROM',
                    'HAVE', 'HAS', 'BUT', 'OR', 'AN', 'THEY', 'WHICH', 'YOU', 'WERE', 'HER',
                    'SHE', 'WILL', 'ONE', 'THEIR', 'WHAT', 'THERE', 'CAN', 'YOUR', 'HAS',
                    'TRUTH', 'WISDOM', 'DIVINE', 'SACRED', 'SOUL', 'SELF', 'TRUST',
                    'SEEK', 'FIND', 'PATH', 'LIGHT', 'DARK', 'PILGRIM', 'PRIMES', 'PRIME',
                    'WELCOME', 'CICADA', 'BELIEVE', 'NOTHING', 'EVERYTHING', 'CIRCUMFERENCE']
    
    for word in common_words:
        if word in text:
            score += len(word) * 10
    
    # Penalize unlikely patterns
    text_nospace = text.replace(" ", "")
    for i in range(len(text_nospace) - 2):
        trigram = text_nospace[i:i+3]
        if len(set(trigram)) == 1:  # Repeated chars
            score -= 5
    
    # Reward common letter patterns
    vowels = text.count('A') + text.count('E') + text.count('I') + text.count('O') + text.count('U')
    total = len(text_nospace)
    if total > 0:
        vowel_ratio = vowels / total
        if 0.25 <= vowel_ratio <= 0.45:
            score += 20
    
    return score

def get_combined_solved_plaintext() -> str:
    """Combine all solved page plaintexts."""
    combined = ""
    for page_num in sorted(SOLVED_PLAINTEXTS.keys()):
        combined += SOLVED_PLAINTEXTS[page_num]
    return combined

def running_key_attack(target_page: int, key_text: str, max_offset: int = 100) -> list[tuple]:
    """Attack using key text as running key at various offsets."""
    cipher = load_runeglish(target_page)
    if not cipher:
        return []
    
    key_indices = text_to_indices(key_text)
    if not key_indices:
        return []
    
    results = []
    
    # Try different offsets in the key
    for offset in range(0, min(max_offset, len(key_indices) - len(cipher) + 1)):
        key_slice = key_indices[offset:offset + len(cipher)]
        if len(key_slice) < len(cipher):
            continue
        
        # Try SUB mode
        plain_sub = decrypt_sub(cipher, key_slice)
        text_sub = indices_to_text(plain_sub)
        score_sub = score_text(text_sub)
        results.append((score_sub, 'SUB', offset, text_sub[:80]))
        
        # Try ADD mode
        plain_add = decrypt_add(cipher, key_slice)
        text_add = indices_to_text(plain_add)
        score_add = score_text(text_add)
        results.append((score_add, 'ADD', offset, text_add[:80]))
    
    return sorted(results, reverse=True)[:10]

def main():
    print("=" * 80)
    print("SOLVED PAGES AS RUNNING KEY ATTACK")
    print("=" * 80)
    
    # Combine all solved plaintexts
    combined_plaintext = get_combined_solved_plaintext()
    print(f"\nCombined solved plaintext length: {len(combined_plaintext)} chars")
    print(f"First 100 chars: {combined_plaintext[:100]}...")
    
    key_indices = text_to_indices(combined_plaintext)
    print(f"Key indices length: {len(key_indices)}")
    
    # Target unsolved pages
    target_pages = [18, 19, 20, 21, 22, 23, 24, 25]
    
    for page in target_pages:
        print(f"\n{'='*80}")
        print(f"PAGE {page}")
        print("=" * 80)
        
        cipher = load_runeglish(page)
        if not cipher:
            print(f"  No runeglish found for page {page}")
            continue
        
        print(f"  Cipher length: {len(cipher)}")
        
        # Test 1: Combined plaintext as key
        print(f"\n  [Combined Solved Plaintext as Key]")
        results = running_key_attack(page, combined_plaintext, max_offset=200)
        for score, mode, offset, text in results[:5]:
            print(f"    [{score:6.1f}] {mode:8s} offset={offset:4d}")
            print(f"            {text}")
        
        # Test 2: Individual page plaintexts
        print(f"\n  [Individual Page Plaintexts]")
        for src_page in [3, 5, 8, 14, 16, 17]:
            if src_page in SOLVED_PLAINTEXTS:
                pt = SOLVED_PLAINTEXTS[src_page]
                key_idx = text_to_indices(pt)
                if len(key_idx) >= len(cipher):
                    cipher_copy = cipher.copy()
                    # Use as repeating key
                    plain_sub = decrypt_sub(cipher_copy, key_idx)
                    text_sub = indices_to_text(plain_sub)
                    score = score_text(text_sub)
                    if score > 100:
                        print(f"    Page {src_page} + SUB: [{score:.1f}]")
                        print(f"      {text_sub[:60]}...")
        
        # Test 3: Specific thematic phrases
        print(f"\n  [Thematic Phrases]")
        phrases = [
            "YOU ARE ALREADY DIVINE",
            "WISDOM IS POWER",
            "TRUST YOURSELF",
            "THE PRIMES ARE SACRED",
            "WITHIN YOUR GRASP",
            "A CLUE WITHIN",
        ]
        for phrase in phrases:
            key_idx = text_to_indices(phrase)
            if key_idx:
                plain_sub = decrypt_sub(cipher, key_idx)
                text_sub = indices_to_text(plain_sub)
                score = score_text(text_sub)
                if score > 50:
                    print(f"    '{phrase}' + SUB: [{score:.1f}]")
                    print(f"      {text_sub[:60]}...")

if __name__ == "__main__":
    main()

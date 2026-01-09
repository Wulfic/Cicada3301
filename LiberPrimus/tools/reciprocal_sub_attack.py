#!/usr/bin/env python3
"""
RECIPROCAL SUBSTITUTION ATTACK

Apply the page 59 reciprocal substitution cipher to other unsolved pages.
If Cicada used the same cipher elsewhere, this might solve more pages.

From page 59 SOLUTION.md:
| Rune | English |
| R | A |
| NG | W |
| A | R |
| M | N |
| J | B |
| I | E |
| H | L |
| E | I |
| IA | V |
| AE | O |
| D | K |
| OE | G |
| C | D |
| EO | T |
| N | M |
| P | S |
| S | P |
| X | X |
| EA | F |
| Y | TH |
| TH | Y |
"""

import os

# Gematria Primus mapping
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

# Page 59 reciprocal substitution table (Cipher -> Plain)
# R -> A, NG -> W, A -> R, M -> N, J -> B, I -> E, H -> L, E -> I,
# IA -> V, AE -> O, D -> K, OE -> G, C -> D, EO -> T, N -> M, P -> S,
# S -> P, X -> X, EA -> F, Y -> TH, TH -> Y
PAGE59_CIPHER_TABLE = {
    'R': 'A',
    'NG': 'W',
    'A': 'R',
    'M': 'N',
    'J': 'B',
    'I': 'E',
    'H': 'L',
    'E': 'I',
    'IA': 'V',
    'AE': 'O',
    'D': 'K',
    'OE': 'G',
    'C': 'D',
    'EO': 'T',
    'N': 'M',
    'P': 'S',
    'S': 'P',
    'X': 'X',
    'EA': 'F',
    'Y': 'TH',
    'TH': 'Y'
}

# Fill in missing mappings (assume identity for now)
FULL_CIPHER_TABLE = {
    'F': 'F', 'U': 'U', 'O': 'O', 'G': 'G', 'W': 'W',
    'L': 'L', 'B': 'B', 'T': 'T'
}
FULL_CIPHER_TABLE.update(PAGE59_CIPHER_TABLE)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNEGLISH_DIR = os.path.join(SCRIPT_DIR, "..", "runeglish_output")

def load_runeglish(page_num: int) -> str:
    """Load runeglish text."""
    filename = os.path.join(RUNEGLISH_DIR, f"page_{page_num:02d}_runeglish.txt")
    if not os.path.exists(filename):
        return ""
    with open(filename, 'r') as f:
        return f.read()

def apply_substitution(text: str, table: dict) -> str:
    """Apply monoalphabetic substitution."""
    result = []
    i = 0
    text = text.upper()
    
    while i < len(text):
        # Try 3-char matches
        if i + 2 < len(text):
            tri = text[i:i+3]
            if tri in table:
                result.append(table[tri])
                i += 3
                continue
        # Try 2-char matches
        if i + 1 < len(text):
            di = text[i:i+2]
            if di in table:
                result.append(table[di])
                i += 2
                continue
        # Single char
        ch = text[i]
        if ch in table:
            result.append(table[ch])
        elif ch in ['-', '.', '•', '\n', ' ', '%', '&', '$', '§']:
            result.append(ch)
        else:
            result.append(f'[{ch}]')
        i += 1
    
    return "".join(result)

def score_english(text: str) -> float:
    """Score based on English patterns."""
    score = 0.0
    words = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'THAT', 'FOR',
             'NOT', 'ARE', 'ALL', 'FROM', 'HAVE', 'OR', 'AN', 'THEY', 'YOU',
             'TRUTH', 'WISDOM', 'DIVINE', 'SACRED', 'BELIEVE', 'NOTHING',
             'WARNING', 'BOOK', 'KNOW', 'TRUE', 'TEST', 'FIND', 'EXPERIENCE',
             'DEATH', 'MESSAGE', 'WORDS', 'NUMBERS', 'WITHIN', 'PILGRIM']
    
    for word in words:
        count = text.count(word)
        if count > 0:
            score += len(word) * count * 10
    
    return score

def main():
    print("=" * 80)
    print("RECIPROCAL SUBSTITUTION ATTACK (Page 59 Table)")
    print("=" * 80)
    
    # Test on unsolved pages
    target_pages = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    target_pages += [65, 66, 69, 70, 71]
    
    for page in target_pages:
        print(f"\n{'='*60}")
        print(f"PAGE {page}")
        print("=" * 60)
        
        runeglish = load_runeglish(page)
        if not runeglish:
            print("  No runeglish found")
            continue
        
        # Apply page 59 substitution
        decrypted = apply_substitution(runeglish, FULL_CIPHER_TABLE)
        score = score_english(decrypted)
        
        print(f"  Score: {score:.1f}")
        print(f"  First 200 chars:")
        preview = decrypted[:200].replace('\n', ' ')
        print(f"    {preview}")
        
        if score > 100:
            print(f"\n  *** HIGH SCORE - POTENTIAL MATCH ***")
            print(f"  Full output:")
            print(f"    {decrypted[:500]}")

    # Also check page 59 itself to verify
    print(f"\n{'='*60}")
    print("VERIFICATION: Page 59 (should produce known plaintext)")
    print("=" * 60)
    runeglish = load_runeglish(59)
    decrypted = apply_substitution(runeglish, FULL_CIPHER_TABLE)
    print(f"  {decrypted[:200]}")

if __name__ == "__main__":
    main()

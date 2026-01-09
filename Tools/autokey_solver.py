#!/usr/bin/env python3
"""
AUTOKEY CIPHER SOLVER FOR LIBER PRIMUS

Autokey cipher uses the plaintext itself to extend the key.
Standard Vigenère attacks fail because the key doesn't repeat.

Testing on unsolved pages starting with Page 17.
"""

from pathlib import Path
from collections import Counter

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {l: i for i, l in enumerate(LETTERS)}

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

# Common English word patterns for scoring
COMMON_STARTS = ['THE', 'AN', 'A', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'AT', 
                 'SO', 'WE', 'HE', 'BY', 'OR', 'ON', 'DO', 'IF', 'ME', 'MY',
                 'SOME', 'WISDOM', 'WITHIN', 'WELCOME', 'PILGRIM', 'END',
                 'EPILOGUE', 'PARABLE', 'KOAN', 'WARNING', 'INSTRUCTION']

def text_to_indices(text):
    """Convert text to Gematria indices."""
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[two])
                i += 2
                continue
        one = text[i]
        if one in LETTER_TO_IDX:
            result.append(LETTER_TO_IDX[one])
        i += 1
    return result

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(LETTERS[i] for i in indices)

def load_page(page_num):
    """Load rune text from a page."""
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    rune_file = page_dir / "runes.txt"
    if not rune_file.exists():
        return None
    with open(rune_file, 'r', encoding='utf-8') as f:
        return f.read()

def decrypt_autokey(cipher, primer):
    """
    Decrypt using autokey cipher.
    Key = primer + plaintext (rolling).
    plaintext[i] = (cipher[i] - key[i]) mod 29
    
    For first len(primer) chars, key = primer
    After that, key[i] = plaintext[i - len(primer)]
    """
    primer_idx = text_to_indices(primer)
    plaintext = []
    
    for i, c in enumerate(cipher):
        if i < len(primer_idx):
            k = primer_idx[i]
        else:
            k = plaintext[i - len(primer_idx)]
        
        p = (c - k) % 29
        plaintext.append(p)
    
    return plaintext

def score_text(text):
    """Score text based on English-like patterns."""
    score = 0
    
    # Check for common word starts
    for word in COMMON_STARTS:
        if word in text:
            score += len(word) * 3
    
    # Check for common patterns
    for pattern in ['THE', 'AND', 'ING', 'TION', 'ENT', 'ION', 'TH', 'ER', 'AN', 'RE', 'ED', 'ND', 'AT']:
        if pattern in text:
            score += text.count(pattern) * 2
    
    # Penalize unlikely patterns
    for bad in ['QQQ', 'XXX', 'ZZZ', 'JJJ', 'WWW']:
        if bad in text:
            score -= 10
    
    # Check letter frequency (high frequency of common letters)
    for letter in ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'L']:
        score += text.count(letter)
    
    return score

def brute_force_autokey(cipher, max_primer_len=5):
    """Try all possible primers up to given length."""
    best_score = -1000
    best_result = None
    best_primer = None
    
    total = sum(29**i for i in range(1, max_primer_len + 1))
    checked = 0
    
    def generate_primers(length):
        if length == 0:
            yield []
            return
        for p in generate_primers(length - 1):
            for i in range(29):
                yield p + [i]
    
    for length in range(1, max_primer_len + 1):
        for primer_idx in generate_primers(length):
            checked += 1
            
            # Decrypt
            plaintext = []
            for i, c in enumerate(cipher):
                if i < len(primer_idx):
                    k = primer_idx[i]
                else:
                    k = plaintext[i - len(primer_idx)]
                p = (c - k) % 29
                plaintext.append(p)
            
            text = indices_to_text(plaintext)
            score = score_text(text)
            
            if score > best_score:
                best_score = score
                best_result = text
                best_primer = ''.join(LETTERS[i] for i in primer_idx)
                
                if score > 50:
                    print(f"  Primer '{best_primer}' score {score}: {text[:80]}...")
            
            if checked % 10000 == 0:
                print(f"  Checked {checked}/{total}...")
    
    return best_primer, best_score, best_result

def test_common_primers(cipher):
    """Test primers based on known Cicada patterns."""
    primers = [
        'DIVINITY',
        'PILGRIM',
        'PRIMES',
        'SACRED',
        'TOTIENT',
        'WISDOM',
        'CICADA',
        'LIBER',
        'PRIMUS',
        'THREE',
        'NINETEEN',
        'TRUTH',
        'ENLIGHTENMENT',
        'SELF',
        'RELIANCE',
        'EMERSON',
        'CIRCUMFERENCE',
        'JOURNEY',
        'WITHIN',
        'DEEP',
        'WEB',
        'INSTAR',
        'PARABLE',
        'KOAN',
        'WARNING',
        'INSTRUCTION',
        'EPILOGUE',
        'AN',
        'THE',
        'A',
        'SOME',
        'END',
        'F',  # Just F
        'FU',
        'FUR',
        # Try single letters
    ] + [LETTERS[i] for i in range(29)]
    
    best_score = -1000
    best_result = None
    best_primer = None
    
    for primer in primers:
        plaintext = decrypt_autokey(cipher, primer)
        text = indices_to_text(plaintext)
        score = score_text(text)
        
        if score > best_score:
            best_score = score
            best_result = text
            best_primer = primer
        
        if score > 30:
            print(f"  Primer '{primer}': score {score}")
            print(f"    {text[:100]}")
    
    return best_primer, best_score, best_result

def main():
    print("AUTOKEY CIPHER ANALYSIS")
    print("=" * 80)
    
    # Test on Page 17
    rune_text = load_page(17)
    if not rune_text:
        print("Could not load page 17")
        return
    
    # Parse runes
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    print(f"\nPage 17: {len(cipher)} runes")
    
    print("\n--- Testing common primers ---")
    best_primer, best_score, best_result = test_common_primers(cipher)
    print(f"\nBest from common primers: '{best_primer}' (score {best_score})")
    print(f"  {best_result[:150]}...")
    
    print("\n--- Brute force short primers (length 1-3) ---")
    bf_primer, bf_score, bf_result = brute_force_autokey(cipher[:100], max_primer_len=3)
    print(f"\nBest from brute force: '{bf_primer}' (score {bf_score})")
    if bf_result:
        print(f"  {bf_result[:150]}...")

if __name__ == '__main__':
    main()

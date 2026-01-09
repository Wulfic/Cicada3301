#!/usr/bin/env python3
"""
CHAINED PLAINTEXT KEY ATTACK

Theory: Each page's plaintext is the key for the next page.
"Combine the plaintext of this page with all that follows"

Testing: Use Page 16's plaintext as key for Page 17.
"""

from pathlib import Path

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

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
          223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
          293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
          463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
          569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
          647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
          743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829]

def phi(n):
    """Euler's totient function for prime n."""
    return n - 1

def text_to_indices(text):
    """Convert text to Gematria indices, handling digraphs."""
    result = []
    i = 0
    text = text.upper()
    digraphs = ['TH', 'NG', 'EO', 'OE', 'AE', 'IO', 'EA']
    
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in digraphs and two in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[two])
                i += 2
                continue
        one = text[i]
        if one in LETTER_TO_IDX:
            result.append(LETTER_TO_IDX[one])
        # Handle K, Q, V, Z
        elif one == 'K':
            result.append(LETTER_TO_IDX['C'])
        elif one == 'Q':
            result.append(LETTER_TO_IDX['C'])
        elif one == 'V':
            result.append(LETTER_TO_IDX['U'])
        elif one == 'Z':
            result.append(LETTER_TO_IDX['S'])
        i += 1
    return result

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    rune_file = page_dir / "runes.txt"
    if not rune_file.exists():
        return None
    with open(rune_file, 'r', encoding='utf-8') as f:
        return f.read()

def score_result(text):
    """Score based on common English words."""
    COMMON_WORDS = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'WITH', 'THIS', 'THAT', 'FROM',
        'HAVE', 'WILL', 'WHAT', 'WHEN', 'THERE', 'THEIR', 'WHICH', 'BEING',
        'AN', 'A', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'AT', 'SO', 'WE', 
        'HE', 'BY', 'OR', 'ON', 'DO', 'IF', 'MY', 'SOME', 'WISDOM', 'PILGRIM',
        'QUESTION', 'TRUTH', 'KNOW', 'FOLLOW', 'INSTRUCTION', 'PARABLE',
        'WITHIN', 'DEEP', 'WEB', 'PAGE', 'DUTY', 'SACRED', 'PRIMES'
    ]
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def decrypt_vigenere(cipher, key, add_mode=False):
    """Decrypt cipher with repeating key."""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if add_mode:
            p = (c + k) % 29
        else:
            p = (c - k) % 29
        result.append(p)
    return result

def decrypt_autokey(cipher, primer):
    """Autokey cipher: key = primer then previous plaintext."""
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

def decrypt_phi_prime(cipher):
    """φ(prime) shift cipher like pages 55/73."""
    result = []
    for i, c in enumerate(cipher):
        k = phi(PRIMES[i % len(PRIMES)]) % 29
        p = (c - k) % 29
        result.append(p)
    return result

def main():
    print("CHAINED PLAINTEXT KEY ATTACK")
    print("=" * 80)
    
    # Page 16 plaintext (verified solved)
    page16_text = """AN INSTRUCTION QUESTION ALL THINGS DISCOVER TRUTH INSIDE YOURSELF
FOLLOW YOUR TRUTH
IMPOSE NOTHING ON OTHERS
KNOW THIS"""
    
    page16_key = text_to_indices(page16_text)
    print(f"Page 16 plaintext: {len(page16_key)} indices")
    
    # Load Page 17
    rune_text = load_page(17)
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    print(f"Page 17 cipher: {len(cipher)} runes")
    
    print("\n--- TEST 1: Page 16 as repeating Vigenère key (SUB) ---")
    result = decrypt_vigenere(cipher, page16_key, add_mode=False)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    print("\n--- TEST 2: Page 16 as repeating Vigenère key (ADD) ---")
    result = decrypt_vigenere(cipher, page16_key, add_mode=True)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    print("\n--- TEST 3: Page 16 as autokey primer ---")
    result = decrypt_autokey(cipher, page16_text)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    print("\n--- TEST 4: Standard φ(prime) shift ---")
    result = decrypt_phi_prime(cipher)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    print("\n--- TEST 5: φ(prime) + Page 16 key combined ---")
    # First apply φ(prime), then Vigenère with page 16
    intermediate = decrypt_phi_prime(cipher)
    result = decrypt_vigenere(intermediate, page16_key, add_mode=False)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    print("\n--- TEST 6: Page 16 key + φ(prime) combined (reverse order) ---")
    # First Vigenère, then φ(prime)
    intermediate = decrypt_vigenere(cipher, page16_key, add_mode=False)
    result = decrypt_phi_prime(intermediate)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    # Test with specific key words from solved pages
    print("\n--- TEST 7: Key word tests ---")
    keywords = ["QUESTIONALLTHINGS", "DISCOVERTRUTH", "INSTRUCTION", "FOLLOWYOURTRUTH", 
                "KNOWTHIS", "ANINSTRUCTION", "IMPOSENOTHINGONOTHERS",
                "TRUTHINSIDEYOURSELF", "THEPRIMES", "SACREDTOTIENT"]
    
    best_score = 0
    best_keyword = None
    best_text = None
    
    for keyword in keywords:
        key = text_to_indices(keyword)
        if len(key) == 0:
            continue
            
        result = decrypt_vigenere(cipher, key, add_mode=False)
        text = indices_to_text(result)
        score = score_result(text)
        
        if score > best_score:
            best_score = score
            best_keyword = keyword
            best_text = text
    
    print(f"Best keyword: '{best_keyword}' (score {best_score})")
    if best_text:
        print(f"Preview: {best_text[:150]}...")
    
    # Test combining with known working methods
    print("\n--- TEST 8: DIVINITY key (worked on pages 3-4) ---")
    key = text_to_indices("DIVINITY")
    result = decrypt_vigenere(cipher, key, add_mode=False)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")
    
    print("\n--- TEST 9: FIRFUMFERENFE key (worked on pages 14-15) ---")
    key = text_to_indices("FIRFUMFERENFE")
    result = decrypt_vigenere(cipher, key, add_mode=False)
    text = indices_to_text(result)
    score = score_result(text)
    print(f"Score: {score}")
    print(f"Preview: {text[:150]}...")

if __name__ == '__main__':
    main()

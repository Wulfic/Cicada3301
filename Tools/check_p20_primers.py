
import sys

# Constants match previous
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

COMMON_WORDS = {'THE', 'AND', 'ING', 'ION', 'THAT', 'WITH'}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def autokey_decrypt(cipher, primer, mode='SUB'):
    primer_len = len(primer)
    plain = []
    
    # First segment
    for i in range(min(len(cipher), primer_len)):
        k = primer[i]
        c = cipher[i]
        if mode == 'SUB':
            p = (c - k) % 29
        else:
            p = (c + k) % 29
        plain.append(p)
        
    # Subsequent
    for i in range(primer_len, len(cipher)):
        k = plain[i - primer_len]
        c = cipher[i]
        if mode == 'SUB':
            p = (c - k) % 29
        else:
            p = (c + k) % 29
        plain.append(p)
    return plain

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 10
    return score

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    # 23=D, 12=EO, 4=R
    PRIMERS = {
        'DEOR': [23, 12, 4],
        'WELUND': [7, 18, 20, 1, 9, 23], # W E L U N D
        'THEODRIC': [2, 12, 23, 4, 10, 5], # TH EO D R I C
        'NITHHAD': [9, 10, 2, 8, 24, 23], # N I TH H A D
        'BEADOHILD': [17, 28, 23, 3, 8, 10, 20, 23], # B EA D O H I L D
        'MATHHILD': [19, 24, 2, 8, 10, 20, 23], # M A TH H I L D
        'EORMANRIC': [12, 4, 19, 24, 9, 4, 10, 5], # EO R M A N R I C
        'HEODENINGA': [8, 12, 23, 18, 9, 10, 21, 24], # H EO D E N I NG A
        'HEORRENDA': [8, 12, 4, 4, 18, 9, 23, 24], #H EO R R E N D A
        # From P19
        'PRIMES': [13, 4, 10, 19, 18, 15],
        'NUMBERS': [9, 1, 19, 17, 18, 4, 15],
    }
    
    for name, primer in PRIMERS.items():
        # Clean primer to ensure ints
        p_ints = primer
        
        # SUB
        res = autokey_decrypt(cipher, p_ints, 'SUB')
        txt = text_from_indices(res)
        print(f"{name} (SUB): {txt[:60]} (Score: {score_text(txt)})")
        
        # ADD
        res = autokey_decrypt(cipher, p_ints, 'ADD')
        txt = text_from_indices(res)
        print(f"{name} (ADD): {txt[:60]} (Score: {score_text(txt)})")

if __name__ == "__main__":
    main()

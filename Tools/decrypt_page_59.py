
import os

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

NUM_TO_RUNETEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

CIPHER_MAP = {
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
    'X': 'X'
    # W, Y, F, TH, EA, A (Wait A is mapped), U, O, G, T, B
}

def decrypt_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    
    text = runes.replace('\n', ' • ').replace(' ', ' • ')
    words_raw = text.split('•')
    
    decrypted_words = []
    
    for w in words_raw:
        if not w: continue
        w = w.strip()
        if not w: continue
        
        indices = [RUNE_MAP[c] for c in w if c in RUNE_MAP]
        rune_names = [NUM_TO_RUNETEXT[x] for x in indices]
        
        dec = []
        for name in rune_names:
            if name in CIPHER_MAP:
                dec.append(CIPHER_MAP[name])
            else:
                dec.append(f"[{name}]")
        
        decrypted_words.append("".join(dec))
        
    print(f"--- PAGE {pg} DECRYPTION ---")
    print(" ".join(decrypted_words))

if __name__ == "__main__":
    decrypt_runes("59")

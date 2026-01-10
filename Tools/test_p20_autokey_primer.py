import os
import collections

# GP Mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]
LATIN_TO_VAL = {
    "F": 0, "U": 1, "V": 1, "TH": 2, "O": 3, "R": 4, "C": 5, "K": 5, "Q": 5, 
    "G": 6, "W": 7, "H": 8, "N": 9, "I": 10, "J": 11, "EO": 12, "P": 13, 
    "X": 14, "Z": 15, "S": 15, "T": 16, "B": 17, "E": 18, "M": 19, "L": 20, 
    "NG": 21, "OE": 22, "D": 23, "A": 24, "AE": 25, "Y": 26, "IA": 27, "EA": 28
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def parse_text_to_indices(text):
    text = text.upper().replace(' ', '')
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LATIN_TO_VAL:
                indices.append(LATIN_TO_VAL[two])
                i += 2
                continue
        c = text[i]
        if c in LATIN_TO_VAL:
            indices.append(LATIN_TO_VAL[c])
        i += 1
    return indices

def decrypt_autokey(cipher, primer, mode='SUB'):
    # mode SUB: P = C - K
    # mode ADD: P = C + K
    key = list(primer)
    plain = []
    
    for i in range(len(cipher)):
        k = key[i]
        c = cipher[i]
        
        if mode == 'SUB':
            p = (c - k) % 29
        elif mode == 'ADD':
            p = (c + k) % 29 # P = C + K implies C = P - K? No, P = C + K.
        elif mode == 'REV_SUB':
            p = (k - c) % 29 # P = K - C
            
        plain.append(p)
        key.append(p) # Extend key with Plaintext
        
    return plain

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    primers_text = [
        "REARRANGINGTHEPRIMESNUMBERSWILLSHOWAPATHTOTHEDEOR",
        "REARRANGINGTHEPRIMESNUMBERS",
        "PRIMESNUMBERS",
        "APHATHTOTHEDEOR",
        "DEOR",
        "WELUNDHIMBEWURMAN" # Start of Deor
    ]
    
    modes = ['SUB', 'ADD', 'REV_SUB']
    
    for txt in primers_text:
        primer = parse_text_to_indices(txt)
        print(f"\nExample Primer: {txt} (Len {len(primer)})")
        
        for mode in modes:
            res = decrypt_autokey(cipher, primer, mode)
            
            # IoC
            if len(res) < 2: continue
            c_cnt = collections.Counter(res)
            num = sum(n*(n-1) for n in c_cnt.values())
            den = len(res)*(len(res)-1)
            ioc = num/den * 29.0
            
            preview = "".join([LATIN_TABLE[x] for x in res[:60]])
            print(f"Mode {mode}: IoC={ioc:.4f} | {preview}...")

if __name__ == "__main__":
    main()

import os
import collections

# GP Mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TO_VAL = {
    "F": 0, "U": 1, "V": 1, "TH": 2, "O": 3, "R": 4, "C": 5, "K": 5, "Q": 5, 
    "G": 6, "W": 7, "H": 8, "N": 9, "I": 10, "J": 11, "EO": 12, "P": 13, 
    "X": 14, "Z": 15, "S": 15, "T": 16, "B": 17, "E": 18, "M": 19, "L": 20, 
    "NG": 21, "OE": 22, "D": 23, "A": 24, "AE": 25, "Y": 26, "IA": 27, "EA": 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def parse_text(text):
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

def calc_ioc(indices):
    if len(indices) < 2: return 0
    c = collections.Counter(indices)
    num = sum(n * (n - 1) for n in c.values())
    den = len(indices) * (len(indices) - 1)
    return num / den * 29.0

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    phrases = [
        "REARRANGINGTHEPRIMESNUMBERSWILLSHOWAPATHTOTHEDEOR",
        "REARRANGINGTHEPRIMESNUMBERS",
        "APATHTOTHEDEOR",
        "PRIMESNUMBERS",
        "THEPRIMESNUMBERS",
        # Maybe reverse?
        "REARRANGINGTHEPRIMESNUMBERSWILLSHOWAPATHTOTHEDEOR"[::-1]
    ]
    
    modes = ['C-K', 'K-C', 'C+K']
    
    for phrase in phrases:
        key = parse_text(phrase)
        print(f"\n--- Key Phrase: {phrase} (Len {len(key)}) ---")
        
        for mode in modes:
            res = []
            for i in range(len(cipher)):
                c = cipher[i]
                k = key[i % len(key)]
                
                if mode == 'C-K': val = (c - k) % 29
                elif mode == 'K-C': val = (k - c) % 29
                elif mode == 'C+K': val = (c + k) % 29
                res.append(val)
            
            ioc = calc_ioc(res)
            txt = "".join([LATIN_TABLE[x] for x in res[:60]])
            print(f"Mode {mode}: IoC={ioc:.4f} | {txt}...")

if __name__ == "__main__":
    main()

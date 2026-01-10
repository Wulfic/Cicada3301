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

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def parse_oe_text(text):
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LATIN_TO_VAL:
                indices.append(LATIN_TO_VAL[two])
                i += 2
                continue
            if two == "AE" or two == "Æ": 
                indices.append(25)
                i += (2 if two=="AE" else 1)
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
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    with open(deor_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "MODERN ENGLISH" in content: content = content.split("MODERN ENGLISH")[0]
        if "DEOR POEM (OLD ENGLISH)" in content: content = content.split("DEOR POEM (OLD ENGLISH)")[1]
    
    deor_full = parse_oe_text(content)
    print(f"Deor Key Len: {len(deor_full)}")
    
    limit = len(cipher)
    
    modes = ['C-K', 'K-C', 'C+K']
    best_ioc = 0
    best_res = None
    
    for offset in range(len(deor_full) - 50): # Valid start points
        # Get slice
        length = min(limit, len(deor_full) - offset)
        if length < 50: continue
        
        seg = deor_full[offset : offset+length]
        
        for mode in modes:
            res = []
            for i in range(len(seg)):
                c = cipher[i]
                k = seg[i]
                if mode == 'C-K': val = (c - k) % 29
                elif mode == 'K-C': val = (k - c) % 29
                elif mode == 'C+K': val = (c + k) % 29
                res.append(val)
                
            ioc = calc_ioc(res)
            if ioc > 1.3:
                print(f"HIT! Offset {offset}, Mode {mode}, IoC {ioc:.4f}")
            
            if ioc > best_ioc:
                best_ioc = ioc
                best_res = (offset, mode, ioc)

    print(f"\nBest Result: Offset {best_res[0]}, Mode {best_res[1]}, IoC {best_res[2]:.4f}")

if __name__ == "__main__":
    main()

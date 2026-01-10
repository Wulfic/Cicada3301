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

def parse_oe_text(text):
    # Normalize
    text = text.upper().replace('\n', '')
    indices = []
    i = 0
    while i < len(text):
        # 2 chat check
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LATIN_TO_VAL:
                indices.append(LATIN_TO_VAL[two])
                i += 2
                continue
            # Special chars
            if two == "AE" or two == "Æ": 
                indices.append(25) # AE
                i += (2 if two=="AE" else 1) # wait, AE is 2 chars. Æ is 1.
                continue
        
        # 1 char check
        c = text[i]
        
        # OE characters
        if c == 'Þ' or c == 'Ð': indices.append(2) # TH
        elif c == 'Æ': indices.append(25) # AE
        elif c in LATIN_TO_VAL:
            indices.append(LATIN_TO_VAL[c])
        elif c == ' ': 
            pass
        elif c.isalpha():
             # Fallback
             if c == 'Z': indices.append(15)
        
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
    
    # Load P20
    cipher = load_runes(p20_path)
    
    # Load Deor
    with open(deor_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "MODERN ENGLISH" in content:
            content = content.split("MODERN ENGLISH")[0]
        if "DEOR POEM (OLD ENGLISH)" in content:
            content = content.split("DEOR POEM (OLD ENGLISH)")[1]
            
    deor_indices = parse_oe_text(content)
    
    limit = min(len(cipher), len(deor_indices))
    
    modes = ['C-P', 'P-C', 'C+P']
    
    for mode in modes:
        key_guess = []
        for i in range(limit):
            c = cipher[i]
            p = deor_indices[i]
            
            val = 0
            if mode == 'C-P': val = (c - p) % 29
            elif mode == 'P-C': val = (p - c) % 29
            elif mode == 'C+P': val = (c + p) % 29
            
            key_guess.append(val)
            
        ioc = calc_ioc(key_guess)
        # Convert first 60 to text for preview
        txt = "".join([LATIN_TABLE[x] for x in key_guess[:60]])
        print(f"Mode {mode}: IoC={ioc:.4f} | Preview: {txt}...")

if __name__ == "__main__":
    main()

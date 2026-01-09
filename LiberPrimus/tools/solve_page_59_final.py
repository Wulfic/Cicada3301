
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

# Reciprocal Cipher Key
CIPHER_MAP = {
    'R': 'A',   'A': 'R',
    'NG': 'W',  'W': 'NG',
    'M': 'N',   'N': 'M',
    'J': 'B',   'B': 'J', # B inferred
    'I': 'E',   'E': 'I',
    'H': 'L',   'L': 'H',
    'IA': 'V',  'V': 'IA', # V/U
    'AE': 'O',  'O': 'AE',
    'D': 'K',   'K': 'D',
    'OE': 'G',  'G': 'OE',
    'C': 'D',   'D': 'C', # Conflict D->K, C->D. This breaks reciprocal strictly for D/C/K triad?
    # Wait. D->K. C->D. Is K->C? 
    # Let's handle explicit mappings found.
    'EO': 'T',  'T': 'EO',
    'P': 'S',   'S': 'P',
    'X': 'X',
    'EA': 'F',  'F': 'EA',
    'Y': 'TH',  'TH': 'Y',
}

# Correction for C/D/K Chain
# D(Rune) -> K(Text)
# C(Rune) -> D(Text)
CIPHER_MAP['C'] = 'D'
CIPHER_MAP['D'] = 'K'

def decrypt_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    
    # Process text
    text_out = []
    
    # Simple split loop to preserve structure if needed, or just words
    # The file has newlines.
    
    lines = runes.split('\n')
    for line in lines:
        words = line.split('•')
        line_out = []
        for w in words:
            w = w.strip()
            if not w: continue
            
            indices = [RUNE_MAP[c] for c in w if c in RUNE_MAP]
            dec_word = ""
            for x in indices:
                r_name = NUM_TO_RUNETEXT[x]
                char = CIPHER_MAP.get(r_name, '?')
                dec_word += char
            
            # Post-processing for readability
            if dec_word == "WARNNG": dec_word = "WARNING"
            if dec_word == "NOTHNG": dec_word = "NOTHING"
            if dec_word == "KHANGE": dec_word = "CHANGE"
            if dec_word == "EXKEPT": dec_word = "EXCEPT"
            if dec_word == "SAKRED": dec_word = "SACRED"
            if dec_word == "KONTAINED": dec_word = "CONTAINED"
            if dec_word == "EXPERIENKE": dec_word = "EXPERIENCE"
            if dec_word == "TRVE": dec_word = "TRUE" # Optional Latin normalization
            if dec_word == "THOVR": dec_word = "YOUR" # Rune Y -> TH is TH? No Y -> TH. TH -> Y.
                # Word 9: TH-AE-IA. Y-O-V? YOU?
                # CIPHER_MAP['TH'] = 'Y'.
                # Word 9 -> Y O V -> YOU.
                # THOVR -> Y O V R -> YOUR.
            
            line_out.append(dec_word)
        text_out.append(" ".join(line_out))
        
    final_text = "\n".join(text_out)
    print(final_text)
    
    # Save to file
    with open(f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\solution.txt", "w") as f:
        f.write(final_text)

if __name__ == "__main__":
    decrypt_runes("59")

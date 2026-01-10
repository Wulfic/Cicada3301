
import os
import sys

# --- Constants ---

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

# Manual overrides for the key (Index -> Rune String)
# Based on observations of potential words/patterns
KEY_OVERRIDES = {
    # OF ALL I WILL
    4: 'AE', 5: 'L', 6: 'N', 7: 'S', 8: 'A', 9: 'Y', 10: 'AE', 11: 'W', 13: 'H',
    
    # ASC THE OATH IS SWORN TO THE ONE
    14: 'I', 15: 'A', 16: 'E',
    18: 'F', 19: 'T', 20: 'N', 21: 'R', 22: 'X', 23: 'OE', 24: 'P', 25: 'P', 
    26: 'O', 27: 'EA', 28: 'C', 29: 'NG', 30: 'A', 31: 'M', 32: 'C',
    33: 'U', 34: 'IA', 35: 'X',
    
    # WITHIN THE
    36: 'G', 37: 'B', 38: 'A', 39: 'A', 40: 'OE', 41: 'H', 42: 'D',
    
    # ABOVE THE WAY (Corrected)
    43: 'G', 44: 'OE', 45: 'M', 46: 'TH', 47: 'J', 
    48: 'O', 49: 'M', 50: 'AE', 51: 'S', 52: 'A'
}


# Current working key (re-copy from output)
CURRENT_KEY = [
    11, 6, 1, 20, 6, 25, 25, 26, 13, 11, 22, 10, 19, 3, 20, 28, 6, 
    9, 6, 3, 25, 25, 9, 20, 28, 13, 17, 15, 13, 14, 25, 4, 4, 2, 
    18, 6, 3, 25, 13, 3, 21, 1, 10, 5, 14, 11, 1, 23, 3, 9, 20, 17, 10
]
# Text: SGULGAEAEYPJOEIMOLEAGNGOAEAENLHFBWPXAERRTHEGOAEPONGUICXJUDONLBI

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def decrypt(cipher, key):
    key_len = len(key)
    res = []
    lines = []
    current_line = ""
    
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        p_idx = (c - k) % 29
        char = LATIN_TABLE[p_idx]
        current_line += char
        
        # Word wrap heuristic (just for display)
        if len(current_line) > 60:
            lines.append(current_line)
            current_line = ""
            
    if current_line: lines.append(current_line)
    return "\n".join(lines)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    cipher = load_runes(path)
    
    # Apply overrides
    for idx, char in KEY_OVERRIDES.items():
        # Find index of char
        if char in LATIN_TABLE:
             CURRENT_KEY[idx] = LATIN_TABLE.index(char)
    
    print("--- Decryption with Current Key ---")
    print(f"Key: {''.join([LATIN_TABLE[k] for k in CURRENT_KEY])}")
    print("-" * 40)
    print(decrypt(cipher, CURRENT_KEY))
    print("-" * 40)
    
    # Display Key Columns for Analysis
    print("\n--- Key Column Analysis ---")
    # Print the characters at each key index to see vertical patterns
    # e.g. Column 0 contains chars 0, 53, 106...
    # Helps spot if a key character is wrong based on vertical legibility
    
    for k_idx in range(len(CURRENT_KEY)):
        col_chars = []
        for i in range(k_idx, len(cipher), len(CURRENT_KEY)):
            p_idx = (cipher[i] - CURRENT_KEY[k_idx]) % 29
            col_chars.append(LATIN_TABLE[p_idx])
        print(f"Idx {k_idx:02d} ({LATIN_TABLE[CURRENT_KEY[k_idx]]}): {' '.join(col_chars)}")

if __name__ == "__main__":
    main()

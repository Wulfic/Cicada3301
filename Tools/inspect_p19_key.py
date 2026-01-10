
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

# Key from solve_vigenere_modern.py (KeyLen 47, ADD)
CURRENT_KEY = [
    24, 15, 2, 24, 4, 21, 11, 10, 20, 16, 9, 19, 26, 11, 7, 5, 
    11, 6, 27, 8, 22, 25, 21, 16, 25, 0, 27, 9, 21, 7, 27, 15, 
    21, 9, 3, 16, 5, 22, 18, 4, 5, 18, 23, 
    0, 0, 0, 0 # Missing last 4
]
MODE = 'ADD' # P = (C + K) % 29

KEY_OVERRIDES = {
}


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
        if MODE == 'ADD':
            p_idx = (c + k) % 29
        else:
            p_idx = (c - k) % 29
            
        char = LATIN_TABLE[p_idx]
        current_line += char
        
        # Word wrap heuristic (just for display)
        if len(current_line) > 60:
            lines.append(current_line)
            current_line = ""
            
    if current_line: lines.append(current_line)
    return "\n".join(lines)

def derive_key_from_crib_list(cipher, crib_list, start_index=0):
    updates = {}
    print(f"Deriving key from crib list at index {start_index}")
    
    for i, p_str in enumerate(crib_list):
        if p_str not in LATIN_TABLE:
            print(f"Warning: {p_str} not in Latin Table")
            continue
            
        p_idx = LATIN_TABLE.index(p_str)
        c_idx = cipher[start_index + i]
        k_val = (p_idx - c_idx) % 29
        key_idx = (start_index + i) % len(CURRENT_KEY)
        
        print(f"  i={i} P={p_str} C={LATIN_TABLE[c_idx]} -> K={LATIN_TABLE[k_val]} (Idx {key_idx})")
        updates[key_idx] = LATIN_TABLE[k_val]
    return updates

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "LiberPrimus", "pages", "page_19", "runes.txt")
    
    if not os.path.exists(path):
        print(f"Error: File not found at {path}")
        return

    cipher = load_runes(path)
    
    # Hypothesis: REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE ONE
    crib_words = [
        'R', 'E', 'A', 'R', 'R', 'A', 'NG', 'I', 'NG', # REARRANGING
        'TH', 'E', # THE
        'P', 'R', 'I', 'M', 'E', 'S', # PRIMES
        'N', 'U', 'M', 'B', 'E', 'R', 'S', # NUMBERS
        'W', 'I', 'L', 'L', # WILL
        'S', 'H', 'O', 'W', # SHOW
        'A', 'P', 'A', 'TH', # A PATH
        'T', 'O', # TO
        'TH', 'E', # THE
        'A', 'L', 'L', # ALL
    ]
    
    crib_updates = derive_key_from_crib_list(cipher, crib_words, 0)
    KEY_OVERRIDES.update(crib_updates)
    
    # Apply overrides
    for idx, char in KEY_OVERRIDES.items():

        if char in LATIN_TABLE:
             CURRENT_KEY[idx] = LATIN_TABLE.index(char)
    
    print("--- Decryption with Current Key ---")
    
    # Debug Index 6
    c6 = cipher[6]
    k6 = CURRENT_KEY[6]
    p6 = (c6 + k6) % 29
    print(f"DEBUG Idx 6: C={c6}({LATIN_TABLE[c6]}) K={k6}({LATIN_TABLE[k6]}) P={p6}({LATIN_TABLE[p6]})")

    key_text = ''.join([LATIN_TABLE[k] for k in CURRENT_KEY])
    print(f"Key: {key_text}")
    print("-" * 40)
    print(decrypt(cipher, CURRENT_KEY))
    print("-" * 40)
    
    # Display Key Columns for Analysis
    print("\n--- Key Column Analysis ---")
    
    for k_idx in range(len(CURRENT_KEY)):
        col_chars = []
        for i in range(k_idx, len(cipher), len(CURRENT_KEY)):
            if MODE == 'ADD':
                p_idx = (cipher[i] + CURRENT_KEY[k_idx]) % 29
            else:
                p_idx = (cipher[i] - CURRENT_KEY[k_idx]) % 29
            col_chars.append(LATIN_TABLE[p_idx])
        print(f"Idx {k_idx:02d} ({LATIN_TABLE[CURRENT_KEY[k_idx]]}): {' '.join(col_chars)}")

if __name__ == "__main__":
    main()

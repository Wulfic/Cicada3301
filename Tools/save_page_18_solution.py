
import os

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

# Final Refined Key
KEY_STR_LATIN = "JGULAELNSAYAEWMHIAENFTNRXOEPPOEACNGAMCUIAXGBAAOEHDGOEMTHJOMAESA"

def get_key_indices(latin_key):
    return [LATIN_TABLE.index(c) for c in latin_key if c in LATIN_TABLE]

# Re-map key in case of multi-char lookups (naive split won't work for AE/EO/NG/OE/IA/EA/TH)
# We know the key length is 53.
# Let's reconstruct the indices manually based on the overrides we determined.

KEY_INDICES = [
    11, 6, 1, 20, 25, 20, 9, 15, 24, 26, 25, 7, 19, 8, # JGULAELNSAYAEWMH
    10, 24, 18, 9, 0, 16, 9, 4, 14, 22, 13, 13, # IAENFTNRXOEPP
    3, 28, 5, 21, 24, 19, 5, 1, 27, 14, # OEACNGAMCUIAX
    6, 17, 24, 24, 22, 8, 23, # GBAAOEHD
    6, 22, 19, 2, 11, 3, 19, 25, 15, 24 # GOEMTHJOMAESA
]

# Double check the key string
RECONSTRUCTED_KEY = "".join([LATIN_TABLE[k] for k in KEY_INDICES])
print(f"Target: {KEY_STR_LATIN}")
print(f"Actual: {RECONSTRUCTED_KEY}")

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def decrypt(cipher, key_indices):
    key_len = len(key_indices)
    res = []
    
    for i, c in enumerate(cipher):
        k = key_indices[i % key_len]
        p_idx = (c - k) % 29
        char = LATIN_TABLE[p_idx]
        res.append(char)
        
    return "".join(res)

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    cipher = load_runes(path)
    plaintext = decrypt(cipher, KEY_INDICES)
    
    # Format Plaintext (approximate word spacing)
    # "BEINGOFALLIWILLASCTHEOATHISSWORNTOTHEONEWITHINTHEABOFETHEWAY"
    
    print("\n--- Final Plaintext ---")
    print(plaintext)
    
    # Save
    out_path = os.path.join(repo, "Analysis", "Outputs", "page_18_solution.txt")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"Key: {RECONSTRUCTED_KEY}\n")
        f.write("-" * 40 + "\n")
        f.write(plaintext)
    print(f"\nSaved to {out_path}")

if __name__ == "__main__":
    main()

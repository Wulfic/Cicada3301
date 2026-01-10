
import os

# Gematria Primus Mapping
# Index | Rune | Latin
gp_map = [
    ('ᚠ', 'F'), ('ᚢ', 'U'), ('ᚦ', 'TH'), ('ᚩ', 'O'), ('ᚱ', 'R'), ('ᚳ', 'C'), 
    ('ᚷ', 'G'), ('ᚹ', 'W'), ('ᚻ', 'H'), ('ᚾ', 'N'), ('ᛁ', 'I'), ('ᛂ', 'J'), 
    ('ᛇ', 'EO'), ('ᛈ', 'P'), ('ᛉ', 'X'), ('ᛋ', 'S'), ('ᛏ', 'T'), ('ᛒ', 'B'), 
    ('ᛖ', 'E'), ('ᛗ', 'M'), ('ᛚ', 'L'), ('ᛝ', 'NG'), ('ᛟ', 'OE'), ('ᛞ', 'D'), 
    ('ᚪ', 'A'), ('ᚫ', 'AE'), ('ᚣ', 'Y'), ('ᛡ', 'IA'), ('ᛠ', 'EA')
]

rune_to_index = {r: i for i, (r, _) in enumerate(gp_map)}
index_to_latin = {i: l for i, (_, l) in enumerate(gp_map)}
latin_to_index = {l: i for i, (_, l) in enumerate(gp_map)}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def clean_runes(text):
    return [c for c in text if c in rune_to_index]

def vigenere_decrypt(runes_list, key_indices):
    decrypted_indices = []
    key_len = len(key_indices)
    for i, r_idx in enumerate(runes_list):
        # Decrypt: P = (C - K) % 29
        # Assuming runic Vigenere works this way
        k_idx = key_indices[i % key_len]
        p_idx = (rune_to_index[r_idx] - k_idx) % 29
        decrypted_indices.append(p_idx)
    return decrypted_indices

def indices_to_text(indices):
    return "".join([index_to_latin[i] for i in indices])

def get_key_indices(key_string):
    indices = []
    # If key is Latin, convert to Rune indices
    # We need to map Latin letters to GP indices carefully
    # Splitting by space if multiple letters
    parts = key_string.split()
    if len(parts) == 1 and len(key_string) > 1 and not key_string in latin_to_index:
        # It's a string like "AGUE"
        # We need to iterate characters. But "TH", "EO" etc are digraphs.
        # Simple parser for now: greedy match
        i = 0
        while i < len(key_string):
            # Try 3 chars (ING ? No ING is NG)
            # Try 2 chars
            found = False
            if i + 2 <= len(key_string):
                sub = key_string[i:i+2]
                if sub in latin_to_index:
                    indices.append(latin_to_index[sub])
                    i += 2
                    found = True
            if not found:
                sub = key_string[i]
                if sub in latin_to_index:
                    indices.append(latin_to_index[sub])
                    i += 1
                else:
                    # Skip or fail
                    i += 1
    else:
        # Space separated runes or latin logic
        for p in parts:
            if p in latin_to_index:
                indices.append(latin_to_index[p])
    return indices

def main():
    filepath = 'LiberPrimus/pages/page_06/runes.txt'
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    raw_text = load_runes(filepath)
    runes_only = clean_runes(raw_text)
    
    print(f"Total Runes: {len(runes_only)}")

    keys_to_try = ["AGUE", "IMPERIAL", "IMPERIALAGUE", "SIX", "SIXCUBITS", "DIAGONAL", "FIRFUMFERENFE"]
    
    for key in keys_to_try:
        k_indices = get_key_indices(key)
        print(f"\nTrying Key: {key} {k_indices}")
        
        # Try Decrypt (Subtract)
        decrypted_indices = vigenere_decrypt(runes_only, k_indices)
        text = indices_to_text(decrypted_indices)
        print(f"Decrypt: {text[:100]}")
        
        # Try Encrypt (Add) - sometimes "apply key" means add
        encrypted_indices = []
        for i, r_idx in enumerate(runes_only):
            k_idx = k_indices[i % len(k_indices)]
            p_idx = (rune_to_index[r_idx] + k_idx) % 29
            encrypted_indices.append(p_idx)
        text_enc = indices_to_text(encrypted_indices)
        print(f"Encrypt: {text_enc[:100]}")

if __name__ == "__main__":
    main()

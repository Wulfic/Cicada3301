import os

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
PAGE_NUM = "18"
RUNES_FILE = r"C:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_18\runes.txt"

# ------------------------------------------------------------------
# Gematria Primus (Standard)
# ------------------------------------------------------------------
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def load_runes_keep_punct(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    # Keep runes and hyphens.
    res = []
    for char in text:
        if char in RUNE_MAP:
            res.append(RUNE_MAP[char])
        elif char == '-' or char == '.' or char == '\n' or char == ' ':
            res.append(char)
        # Skip other chars?
    return res

def decrypt_stream_c_plus_k(stream, key_indices, start_offset=0):
    res_str = ""
    key_len = len(key_indices)
    k_idx = start_offset
    
    for item in stream:
        if isinstance(item, int): # Rune index
            k = key_indices[k_idx % key_len]
            p = (item + k) % 29
            letter = LETTERS[p]
            res_str += letter
            k_idx += 1
        else:
            # Punctuation
            res_str += item
            
    return res_str
    
def solve():
    print(f"Solving Page {PAGE_NUM}...")
    
    stream = load_runes_keep_punct(RUNES_FILE)
    
    # Title ends at first newline? Or count?
    # Title runes: 22.
    # Let's verify by counting runes in stream.
    count = 0 
    split_idx = 0
    for i, item in enumerate(stream):
        if isinstance(item, int):
            count += 1
        if count == 22:
            split_idx = i + 1
            break
            
    title_stream = stream[:split_idx]
    body_stream = stream[split_idx:]
    
    key_base = [26, 24, 8, 12, 3, 13, 26, 11] # Y A H EO O P Y J (Index 0..7)
    
    # Shift 7 means key starts at index 7. (J)
    print("\n--- Title Check (Shift 7, C+K) ---")
    print(decrypt_stream_c_plus_k(title_stream, key_base, start_offset=7))
    
    print("\n--- Body Check (Shift 7, C+K - Reset) ---")
    # Assuming Body resets to key index 7?
    print(decrypt_stream_c_plus_k(body_stream, key_base, start_offset=7))

    print("\n--- Body Check (Shift 5, C+K - Continuous) ---")
    # Title len 22. Start 7. End (7+22)%8 = 5. Next = 5.
    print(decrypt_stream_c_plus_k(body_stream, key_base, start_offset=5))

    print("\n--- Body Check (Shift 1, C+K) ---")
    # My manual check of Shift 1 (Index 1) found "BEWIDTH"?
    print(decrypt_stream_c_plus_k(body_stream, key_base, start_offset=1))

if __name__ == "__main__":
    solve()

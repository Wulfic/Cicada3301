import os
import sys

# Configuration
# Rune Mapping
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

SOLUTIONS = {
    58: "CLEAR",
    59: "INTERCONNECTEDNESS", # Tentative, yields "WITH THE..."
    60: "CLEAR",
    61: "DIVINITY",
    62: "CONSUMPTION", # Tentative
    63: "CLEAR",
    64: "KAON", # Tentative
    65: "EULER", # Tentative, yields "THE..."
    66: "MISSING",
    67: "CICADA", # Tentative
    68: "CLEAR",
    69: "EMPTY",
    70: "EMPTY",
    71: "CLEAR",
    72: "FIRFUMFERENFE", # Confirmed
    73: "EMPTY",
    74: "CLEAR"
}

def load_runes(page_num):
    paths = [
        f"LiberPrimus/pages/page_{page_num:02d}/runes.txt",
        os.path.join(os.getcwd(), f"LiberPrimus/pages/page_{page_num:02d}/runes.txt")
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [RUNE_TO_IDX[r] for r in content if r in RUNE_TO_IDX]
    return []

def parse_key(key_str):
    key_indices = []
    i = 0
    while i < len(key_str):
        if i + 1 < len(key_str):
            sub = key_str[i:i+2]
            if sub in IDX_TO_LETTER:
                key_indices.append(IDX_TO_LETTER.index(sub))
                i += 2
                continue
        char = key_str[i]
        if char == 'V': char = 'U'
        elif char == 'K': char = 'C'
        elif char == 'Q': char = 'C'
        elif char == 'Z': char = 'S'
        
        if char in IDX_TO_LETTER:
            key_indices.append(IDX_TO_LETTER.index(char))
        i += 1
    return key_indices

def decrypt(cipher, key_str):
    if not cipher: return ""
    key = parse_key(key_str)
    if not key: return ""
    decrypted = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        decrypted.append((c - k) % 29)
    return "".join([IDX_TO_LETTER[x] for x in decrypted])

def translate_clear(cipher):
    return "".join([IDX_TO_LETTER[x] for x in cipher])

SUMMARY = []

for page, key_info in SOLUTIONS.items():
    if key_info == "MISSING" or key_info == "EMPTY":
        SUMMARY.append(f"Page {page}: {key_info}")
        continue
        
    cipher = load_runes(page)
    if not cipher:
        SUMMARY.append(f"Page {page}: NO DATA FOUND")
        continue
        
    decoded = ""
    if key_info == "CLEAR":
        decoded = translate_clear(cipher)
        SUMMARY.append(f"Page {page}: CLEARTEXT (Length {len(decoded)})")
    elif page == 65:
        # P65 Special: Grid -> Cipher -> Decrypt
        # Grid content is in runes.txt.
        # We need to simulate the grid decode.
        # Hardcoding the extracted ciphertext 'LFNT...' for simplicity as the grid solve is static.
        grid_cipher = "LFNTDSAESBBRAWIOEAEEAEAIONTHLNGNUSISJNGNGHOEWPMDIAENGIONBDTHOGTNJBOEFDIOIEHLTHIEONIBNXDWIORJRUJHXGICLAHRMJLCLNIODHOEYJBMUNGEOBEC"
        # Convert to indices
        p65_indices = []
        i = 0
        while i < len(grid_cipher):
            if i + 1 < len(grid_cipher) and grid_cipher[i:i+2] in LETTER_TO_IDX:
                p65_indices.append(LETTER_TO_IDX[grid_cipher[i:i+2]])
                i += 2
            elif grid_cipher[i] in LETTER_TO_IDX:
                p65_indices.append(LETTER_TO_IDX[grid_cipher[i]])
                i += 1
            else:
                i += 1
        decoded = decrypt(p65_indices, key_info) # key_info is "EULER"
        SUMMARY.append(f"Page {page}: GRID+KEY '{key_info}' -> {decoded[:30]}...")
    elif page == 59:
        # P59 Special: Skip 6-rune title
        body_cipher = cipher[6:]
        decoded = decrypt(body_cipher, key_info)
        SUMMARY.append(f"Page {page}: BODY+KEY '{key_info}' -> {decoded[:30]}...")
    else:
        decoded = decrypt(cipher, key_info)
        SUMMARY.append(f"Page {page}: KEY '{key_info}' -> {decoded[:30]}...")
    
    # Write to file
    out_dir = os.path.join(os.getcwd(), "LiberPrimus", "pages", f"page_{page:02d}")
    if os.path.exists(out_dir):
        with open(os.path.join(out_dir, "decoded.txt"), "w") as f:
            f.write(decoded)

# Write Summary
with open(os.path.join(os.getcwd(), "LiberPrimus", "LP1_INTUS_SOLUTIONS.md"), "w") as f:
    f.write("# Chapter 1 Intus Solutions (Pages 58-74)\n\n")
    for line in SUMMARY:
        f.write(f"- {line}\n")
    f.write("\n## Notes\n")
    f.write("- P59: Key 'RNGRAMW' is tentative (derived from 'R NG R A M W' title). Result starts with FFFFFF.\n")
    f.write("- P65: Decoded using Grid lookup on Pages 0-4 runic text.\n")
    f.write("- P62: 'CONSUMPTION' produces 'EOTATE...', key needs review.\n")

print("Generated LP1 Solutions.")

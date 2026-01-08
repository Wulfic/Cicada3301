
import os
import sympy

# Configuration from MASTER_SOLVING_DOC
PAGES_CONFIG = {
    1: {'key_len': 71, 'primer': None},
    2: {'key_len': 83, 'primer': None},
    3: {'key_len': 83, 'primer': None},
    4: {'key_len': 103, 'primer': None},
    5: {'key_len': 71, 'primer': None},
}

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

TRANS_MAP = {
    0: 'f', 1: 'u', 2: 'þ', 3: 'o', 4: 'r', 5: 'c', 6: 'g', 7: 'w',
    8: 'h', 9: 'n', 10: 'i', 11: 'j', 12: 'eo', 13: 'p', 14: 'x', 15: 's',
    16: 't', 17: 'b', 18: 'e', 19: 'm', 20: 'l', 21: 'ŋ', 22: 'œ', 23: 'd',
    24: 'a', 25: 'æ', 26: 'y', 27: 'ia', 28: 'ea'
}

def generate_first_layer_key(length):
    """
    Tries to generate the key based on frequency analysis (assuming E).
    Since we don't have the exact keys stored, we'll try to derive them 
    or just use the key length to perform analysis if we can't derive.
    
    Actually, for this test, let's just use the key length to check IoC 
    and maybe try to find the key by aligning 'E' to most frequent char?
    """
    pass

def load_runes(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def solve_page(page_num, key_len):
    print(f"\n{'='*40}")
    print(f"Analyzing Page {page_num} (Key Length {key_len})")
    print(f"{'='*40}")
    
    runes_text = load_runes(page_num)
    if not runes_text:
        print("Runes file not found.")
        return

    runes_only = [RUNE_MAP[c] for c in runes_text if c in RUNE_MAP]
    
    key = []
    
    # Strategy switch based on Page Type
    if page_num in [2, 3, 4]:
        # Use EMB crib
        # EMB = [18, 19, 17]
        print("Using EMB crib...")
        primer = [18, 19, 17]
        
        # Derive key from first chars
        # Key[i] = (Cipher[i] - Plain[i]) % 29
        # Assuming Text starts with EMBEMBEMB...
        
        # We need to fill the key. 
        # But we only know the start. 
        # However, Frequency Analysis is likely better for the whole key.
        # But for EMB pages, the text starts with EMB. 
        # Does the WHOLE text follow EMB distribution? No.
        
        # Let's try Frequency Analysis but mapping to different targets
        # Or try to derive full key if the EMB structure is repeating?
        # No, EMB is just prefix.
        
        # Let's try standard frequency analysis but target TH (2) instead of E (18)
        # because these are Old English pages too?
        target = 2 # TH
    else:
        target = 2 # TH
        
    print(f"Targeting Rune: {TRANS_MAP[target]} ({target})")

    for i in range(key_len):
        coset = runes_only[i::key_len]
        if not coset:
            key.append(0)
            continue
        
        counts = collections.Counter(coset)
        most_common = counts.most_common(1)[0][0]
        
        k = (most_common - target) % 29
        key.append(k)
        
    print(f"Derived Key (start): {key[:10]}...")
    
    # Decrypt
    decrypted_chars = []
    key_idx = 0
    
    for char in runes_text:
        if char in RUNE_MAP:
            rune_val = RUNE_MAP[char]
            k = key[key_idx % key_len]
            plain_val = (rune_val - k) % 29
            decrypted_chars.append(TRANS_MAP[plain_val])
            key_idx += 1
        else:
            decrypted_chars.append(char)
            
    result = "".join(decrypted_chars)
    print("Preview (first 200 chars):")
    print(result[:200])
    
    keywords = ["fleþ", "haþen", "dœþ", "gœþ", "eaþþ", "þat", "emb", "ingham", "warn"]
    found_keywords = [w for w in keywords if w in result.lower()]
    if found_keywords:
        print(f"MATCH! Found keywords: {found_keywords}")

import collections
for p_num, config in PAGES_CONFIG.items():
    solve_page(p_num, config['key_len'])



import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

NUM_TO_RUNETEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

TEXT_TO_RUNE = {v: k for k, v in NUM_TO_RUNETEXT.items()}

# KEYS TO TEST
GRID_KEY_STR = "LFNTDSAESBBRAWIOEAEEAEAIONTHLNGNUSISJNGNGHOEWPMDIAENGIONBDTHOGTNJBOEFDIOIEHLTHIEONIBNXDWIORJRUJHXGICLAHRMJLCLNIODHOEYJBMUNGEOBEC"
PAGE59_KEY_STR = "AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETRUETESTTHEKNOWLEDGEFINDYOURTRUTHEXPERIENCEYOURDEATHDONOTEDITORCHANGETHISBOOKORTHEMESSAGECONTAINEDWITHINEITHERTHEWORDSORTHEIRNUMBERSFORALLISSACRED"
TOTIENT_KEY_STR = "TOTIENT"
PRIMUS_KEY_STR = "PRIMUS"
FIRFUMFERENFE_KEY_STR = "FIRFUMFERENFE" # Common old key hypothesis

def parse_key_indices(k_str):
    indices = []
    i = 0
    k_len = len(k_str)
    while i < k_len:
        if i + 1 < k_len:
            two = k_str[i:i+2]
            if two in TEXT_TO_RUNE:
                indices.append(TEXT_TO_RUNE[two])
                i += 2
                continue
        one = k_str[i]
        if one in TEXT_TO_RUNE:
            indices.append(TEXT_TO_RUNE[one])
            i += 1
        else:
            i += 1
    return indices

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    indices = [RUNE_MAP[c] for c in runes if c in RUNE_MAP]
    return indices

def to_txt(indices):
    return "".join([NUM_TO_RUNETEXT.get(x, '?') for x in indices])

def vigenere_decrypt(cipher, key):
    res = []
    kl = len(key)
    if kl == 0: return []
    for i, c in enumerate(cipher):
        k = key[i % kl]
        p = (c - k) % 29
        res.append(p)
    return res

def beaufort_decrypt(cipher, key):
    # P = K - C
    res = []
    kl = len(key)
    if kl == 0: return []
    for i, c in enumerate(cipher):
        k = key[i % kl]
        p = (k - c) % 29
        res.append(p)
    return res

def variant_beaufort_decrypt(cipher, key):
    # P = C + K (Usually Encrypt Vigenere)
    res = []
    kl = len(key)
    if kl == 0: return []
    for i, c in enumerate(cipher):
        k = key[i % kl]
        p = (c + k) % 29
        res.append(p)
    return res

def autokey_decrypt(cipher, key_primer):
    # P[i] = (C[i] - K[i]) % 29
    # K[i+len(primer)] = P[i]
    res = []
    current_key = list(key_primer)
    
    for i, c in enumerate(cipher):
        if i >= len(current_key):
             # Wait, usually Autokey uses Plaintext generated so far
             # P[0] = (C[0] - Primer[0])
             # K[len_primer] = P[0]
             # So we need to access the just-decrypted char.
             pass
        
        k = current_key[i]
        p = (c - k) % 29
        res.append(p)
        current_key.append(p)
        
    return res

def run_tests(pg_num):
    print(f"\n=== TESTING PAGE {pg_num} ===")
    cipher = load_runes(pg_num)
    
    keys = {
        "GRID": parse_key_indices(GRID_KEY_STR),
        "PAGE59": parse_key_indices(PAGE59_KEY_STR),
        "TOTIENT": parse_key_indices(TOTIENT_KEY_STR),
        "PRIMUS": parse_key_indices(PRIMUS_KEY_STR),
        "FIRFUM": parse_key_indices(FIRFUMFERENFE_KEY_STR)
    }
    
    methods = {
        "VIGENERE": vigenere_decrypt,
        "BEAUFORT": beaufort_decrypt,
        "VARIANT": variant_beaufort_decrypt,
        "AUTOKEY": autokey_decrypt
    }
    
    for k_name, k_ind in keys.items():
        if not k_ind: continue
        for m_name, m_func in methods.items():
            dec_ind = m_func(cipher, k_ind)
            txt = to_txt(dec_ind)
            # Simple heuristic: look for "THE"
            score = txt.count("THE") + txt.count("AND") + txt.count("ING")
            
            # Print high scores or specific interesting combos
            if score > 2 or k_name in ["GRID", "PAGE59"]:
                 print(f"[{m_name}] Key={k_name}: {txt[:60]}... (Score: {score})")

if __name__ == "__main__":
    run_tests("71")
    run_tests("18")

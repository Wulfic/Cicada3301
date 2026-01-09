
import os
import sys

# Configurations
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']
KEYS_TO_TEST = [
    "DIVINITY",
    "FIRFUMFERENFE",
    "INSTAR",
    "WELCOME",
    "WARNING",
    "KOAN",
    "PRIME",
    "PRIMES",
    "CICADA",
    "3301",
    "WISDOM",
    "TOTIENT",
    "SACRED",
    "ENCRYPTED",
    "CIRCUMFERENCE",
    "PARABLE",
    "THE",
    "AN",
    "A",
    "SALUTATIONS",
    "GOODLUCK",
    "DEATH",
    "LIFE",
    "CONSUMPTION",
    "PRESERVATION",
    "ADHERENCE",
    "THEINSTAR",
    "EMERGENCE",
    "EPIPHANY",
    "ABSCISSA",
    "MOBIOUS",
    "MOBIUS",
    "KAON",
    "MASTER",
    "PILGRIM",
    "JOURNEY",
    "GREAT",
    "VOID",
    "SHADOWLINGS",
    "SOURCE",
    "INTEGRITY",
    "INTUS",
    "LIBERPRIMUS"
]

def text_to_runes(text):
    # Convert English/Phonetic key to rune indices
    # This is rough mapping
    key_indices = []
    # Using a simple map for standard english keys if possible
    # But keys like DIVINITY are usually mapped via Gematria Prime or direct letter-to-rune
    # Actually, usually they use the Prime Table values.
    # But let's assume the key is in Runes. 
    # "DIVINITY" -> ᛞᛁᚢᛁᚾᛁᛏᚣ ? 
    # Let's try to load the Gematria Primus mapping if possible, or just hardcode some rune keys.
    pass


# Hardcoded Rune Keys (Indices)
# DIVINITY: D(23) I(10) V/U(1) I(10) N(9) I(10) T(16) Y(26)
# KEY_INDICES = {
#     "DIVINITY": [23, 10, 1, 10, 9, 10, 16, 26],
#     "FIRFUMFERENFE": [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18], # F I R F U M F E R E N F E
# }

def text_to_indices(text):
    mapping = {
        'F':0, 'U':1, 'TH':2, 'O':3, 'R':4, 'C':5, 'K':5, 'G':6, 'W':7, 
        'H':8, 'N':9, 'I':10, 'J':11, 'EO':12, 'P':13, 'X':14, 'S':15, 'Z':15,
        'T':16, 'B':17, 'E':18, 'M':19, 'L':20, 'NG':21, 'OE':22, 'D':23, 
        'A':24, 'AE':25, 'Y':26, 'IO':27, 'IA':27, 'EA':28
    }
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i+1 < len(text) and text[i:i+2] in mapping:
            indices.append(mapping[text[i:i+2]])
            i += 2
        elif text[i] in mapping:
            indices.append(mapping[text[i]])
            i += 1
        else:
            i += 1
    return indices

def load_page(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]
    return None

def decrypt(cipher, key):
    if not key: return []
    return [(c - k) % 29 for c, k in zip(cipher, key * (len(cipher) // len(key) + 1))]

def indices_to_text(indices):
    return "".join([IDX_TO_LETTER[i] for i in indices])

def score_text(text):
    # Simple frequent letter check
    common = "ETAOINSHRDLU"
    score = sum(1 for c in text if c in common)
    return score / len(text) if text else 0

def main():
    pages = [58, 60, 63, 65, 66, 68, 69, 70, 71, 72, 73, 74]
    
    # Process KEYS_TO_TEST
    key_dict = {}
    for k in KEYS_TO_TEST:
        key_dict[k] = text_to_indices(k)
        
    for page in pages:
        runes = load_page(page)
        if not runes: continue
        
        print(f"\n--- Page {page} ---")
        best_score = 0
        best_decr = ""
        best_key = ""
        
        for key_name, key in key_dict.items():
            plain = decrypt(runes, key)
            text = indices_to_text(plain)
            # print(f"Key {key_name}: {text[:60]}...")
            
            # Heuristic check: look for "THE"
            if "THE" in text[:30] or "AN" in text[:10]:
                 print(f"Key {key_name}: {text[:60]}... (FOUND 'THE'/'AN')")
            elif "WELCOME" in text[:30]:
                 print(f"Key {key_name}: {text[:60]}... (FOUND 'WELCOME')")
            
            # Or just print score
            s = score_text(text)
            if s > 0.65: # High frequency of common letters
                 print(f"Key {key_name} (Score {s:.2f}): {text[:60]}...")

if __name__ == "__main__":
    main()


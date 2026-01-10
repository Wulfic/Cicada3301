
import os

# Gematria Primus Mapping
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

COMMON_WORDS = ["THE", "AND", "YOU", "ARE", "WHO", "FOR", "NOT", "BUT", "ALL", "THAT", "WITH", "THIS", "HAVE", "FROM", "LOSS", "CIRCUMFERENCE", "DIVINITY", "WELCOME", "BEWARE", "BELIEVE"]

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def clean_runes(text):
    return [c for c in text if c in rune_to_index]

def vigenere_decrypt(runes_list, key_indices):
    decrypted_indices = []
    key_len = len(key_indices)
    if key_len == 0: return []
    for i, r_idx in enumerate(runes_list):
        idx = rune_to_index[r_idx]
        k_idx = key_indices[i % key_len]
        p_idx = (idx - k_idx) % 29
        decrypted_indices.append(p_idx)
    return decrypted_indices

def get_key_indices(key_string):
    indices = []
    # Simple parse for now
    full_string = key_string.replace(" ", "")
    i = 0
    while i < len(full_string):
        found = False
        if not found and i + 2 <= len(full_string):
            sub = full_string[i:i+2]
            if sub in latin_to_index:
                indices.append(latin_to_index[sub])
                i += 2
                found = True
        if not found:
            sub = full_string[i]
            if sub in latin_to_index:
                indices.append(latin_to_index[sub])
                i += 1
            else:
                i += 1
    return indices

def indices_to_text(indices):
    return "".join([index_to_latin[i] for i in indices])

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += 1
    return score

def main():
    filepath = 'LiberPrimus/pages/page_18/runes.txt'
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    raw_text = load_runes(filepath)
    runes_only = clean_runes(raw_text)
    
    keys = [
        "WWPOEAS",
        "WWPOE",
        "POE",
        "EDGARALLANPOE",
        "WWPOEAMS",
        "IMPERIAL",
        "DIAGONAL",
        "SIX",
        "CUBITS",
        "DEARSIXCUBITSDEAD"
    ]
    
    print("--- VIGENERE ATTACK PAGE 18 WITH NEW KEYS ---")
    for key in keys:
        k_indices = get_key_indices(key)
        if not k_indices: 
            continue
        
        res = vigenere_decrypt(runes_only, k_indices)
        txt = indices_to_text(res)
        s = score_text(txt)
        if s > 0:
            print(f"Key [{key}] Score {s}: {txt[:60]}...")

if __name__ == "__main__":
    main()


import os
import re

# RUNE MAP
RUNE_MAP = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23,
    'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

RUNE_CHARS = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
IDX_TO_CHAR = {v: k for k, v in RUNE_CHARS.items()}
NAMES = {v: k for k, v in RUNE_MAP.items()}

def text_to_rune_indices(text):
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        c = text[i]
        if not c.isalpha():
            i += 1
            continue
        
        # Check 2-char combos
        if i + 1 < len(text):
            pair = text[i:i+2]
            if pair in RUNE_MAP:
                indices.append(RUNE_MAP[pair])
                i += 2
                continue
        
        # Check 1-char
        if c in RUNE_MAP:
            indices.append(RUNE_MAP[c])
        elif c == 'K': indices.append(RUNE_MAP['C'])
        elif c == 'V': indices.append(RUNE_MAP['U'])
        elif c == 'Z': indices.append(RUNE_MAP['S'])
        elif c == 'Q': indices.append(RUNE_MAP['C'])
        i += 1
    return indices

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    # Handle separators if necessary? Assuming standard stream.
    idxs = [RUNE_CHARS[c] for c in runes if c in RUNE_CHARS]
    return idxs

def score_ngrams(text):
    # Simple trigram counter
    common = ["THE", "AND", "ING", "ENT", "ION", "HER", "FOR", "THA", "NTH", "INT", "ERE", "TIO", "TER", "EST", "ERS"]
    score = 0
    for w in common:
        score += text.count(w)
    return score

def decrypt(cipher_idxs, key_idxs, start_offset):
    res = []
    kl = len(key_idxs)
    if kl == 0: return []
    for i in range(len(cipher_idxs)):
        k = key_idxs[(start_offset + i) % kl]
        c = cipher_idxs[i]
        p = (c - k) % 29
        if p in IDX_TO_CHAR:
            res.append(IDX_TO_CHAR[p])
        else:
            res.append("?")
    return res

def runes_to_eng_loose(runes_list):
    res = []
    for r in runes_list:
        if r in RUNE_CHARS:
            idx = RUNE_CHARS[r]
            name = NAMES[idx]
            if len(name) == 1: res.append(name)
            elif name == "TH": res.append("th")
            elif name == "NG": res.append("ng")
            elif name == "EO": res.append("eo")
            elif name == "AE": res.append("ae")
            elif name == "OE": res.append("oe")
            elif name == "IA": res.append("ia")
            elif name == "EA": res.append("ea")
            else: res.append(name)
    return "".join(res)

def main():
    # Load corpus
    with open(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\key_search_corpus.txt", 'r', encoding='utf-8') as f:
        corpus = f.read()
    
    # Pre-clean corpus to remove extensive markdown but keep text
    # Or just rely on text_to_rune_indices skipping non-alpha
    
    key_indices = text_to_rune_indices(corpus)
    cipher_indices = load_runes("71")
    
    print(f"Full Corpus Key Length: {len(key_indices)}")
    print(f"Cipher Length: {len(cipher_indices)}")
    
    if len(key_indices) == 0:
        print("Empty key!")
        return

    best_score = -1
    best_off = 0
    best_dec = ""

    # Try every offset in the corpus
    # Optimized: only check first 50 chars for speed? No, check full page roughly.
    # Page 71 length is ~300 runes.
    # Score on result.
    
    print("Brute forcing running key offsets...")
    
    for off in range(len(key_indices) - len(cipher_indices)): # Ensure we have enough key
        # Extract key slice
        # Actually standard Running Key doesn't loop, it just stops. 
        # But we can allow loop or just check segments.
        
        # Don't decrypt full page for speed, test first 100 chars
        sample_len = 100
        if len(key_indices) < off + sample_len: break
        
        # Fast decrypt sample
        # P = C - K
        sample_dec = []
        for i in range(sample_len):
            k = key_indices[off + i]
            c = cipher_indices[i]
            p = (c - k) % 29
            sample_dec.append(p)
            
        # Check trigrams on sample_dec indices
        # Map p to letters?
        # Just use indices logic?
        # Let's map to loose eng string
        
        chk_str = "".join([NAMES[x] for x in sample_dec if x in NAMES and len(NAMES[x])==1]) 
        
        sc = score_ngrams(chk_str)
        if sc > best_score:
            best_score = sc
            best_off = off
            best_dec = chk_str
            # Print intermediate bests
            if sc > 5:
                print(f"New Best: Off={off}, Score={sc}, Txt={chk_str[:50]}...")

    print(f"Final Best Offset: {best_off}, Score: {best_score}")
    
    # Decrypt full page with best
    full_dec_runes = decrypt(cipher_indices, key_indices, best_off)
    final_eng = runes_to_eng_loose(full_dec_runes)
    print("--- DECRYPTION ---")
    print(final_eng)

if __name__ == "__main__":
    main()

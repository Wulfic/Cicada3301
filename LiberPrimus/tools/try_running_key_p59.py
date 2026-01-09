
import os

# RUNE MAP
# We need English -> Rune Value map
# Using standard Gematria Primus values if possible, or standard index 0-28
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

ENGLISH_TEXT = """
A WARNING
BELIEVE NOTHING FROM THIS BOOK
EXCEPT WHAT YOU KNOW TO BE TRUE
TEST THE KNOWLEDGE
FIND YOUR TRUTH
EXPERIENCE YOUR DEATH
DO NOT EDIT OR CHANGE THIS BOOK
OR THE MESSAGE CONTAINED WITHIN
EITHER THE WORDS OR THEIR NUMBERS
FOR ALL IS SACRED
"""

def text_to_rune_indices(text):
    # Heuristic conversion
    # TH -> 2, NG -> 21, EO -> 12, AE -> 25, OE -> 22, IA -> 27, EA -> 28
    # Greedy match
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
        elif c == 'K': indices.append(RUNE_MAP['C']) # K -> C
        elif c == 'V': indices.append(RUNE_MAP['U']) # V -> U
        elif c == 'Z': indices.append(RUNE_MAP['S']) # Z -> S? Or specific? Known usage?
        elif c == 'Q': indices.append(RUNE_MAP['C']) # Q -> K -> C
        else:
            # Skip unknown
            pass
        i += 1
    return indices

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    idxs = [RUNE_CHARS[c] for c in runes if c in RUNE_CHARS]
    return idxs

def score_ngrams(text):
    # Simple trigram counter from common words
    common = ["THE", "AND", "ING", "ENT", "ION", "HER", "FOR", "THA", "NTH", "INT"]
    score = 0
    for w in common:
        score += text.count(w)
    return score

def decrypt(cipher_idxs, key_idxs, start_offset):
    # Vigenere P = (C - K) % 29
    res = []
    kl = len(key_idxs)
    for i in range(len(cipher_idxs)):
        k = key_idxs[(start_offset + i) % kl]
        c = cipher_idxs[i]
        p = (c - k) % 29
        
        # Find rune char for p
        if p in IDX_TO_CHAR:
            res.append(IDX_TO_CHAR[p])
        else:
            res.append("?")
    
    # Convert runes back to english for readability?
    # No, just output runes or convert to english names
    
    return res

NAMES = {v: k for k, v in RUNE_MAP.items()}

def runes_to_eng(runes_list):
    # runes_list is list of rune characters
    res = []
    for r in runes_list:
        if r in RUNE_CHARS:
            idx = RUNE_CHARS[r]
            res.append(NAMES[idx] + " ")
    return "".join(res)

def main():
    key_indices = text_to_rune_indices(ENGLISH_TEXT)
    cipher_indices = load_runes("71")
    
    print(f"Key Length: {len(key_indices)}")
    print(f"Cipher Length: {len(cipher_indices)}")
    
    best_score = -1
    best_off = 0
    best_dec = ""

    # Try all offsets
    for off in range(len(key_indices)):
        dec_runes = decrypt(cipher_indices, key_indices, off)
        # Convert to loose english for scoring
        # Since I don't have a robust rune->eng function here that handles multichars perfectly for scoring,
        # I'll just map single chars.
        
        # Quick map
        eng_str = ""
        for r in dec_runes:
            idx = RUNE_CHARS.get(r, 0)
            name = NAMES[idx]
            if len(name) == 1: eng_str += name
            elif name == "TH": eng_str += "th"
            else: eng_str += name
        
        sc = score_ngrams(eng_str.upper())
        if sc > best_score:
            best_score = sc
            best_off = off
            best_dec = eng_str
            
    print(f"Best Offset: {best_off}, Score: {best_score}")
    print(best_dec[:200]) # First 200 chars

    # Check specific manually
    # We suspect DECRYPTION at word 14 (idx 60)
    # Let's check if the text at correct offset makes DECRYPTION appear
    
if __name__ == "__main__":
    main()

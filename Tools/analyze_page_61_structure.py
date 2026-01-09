
import os
import sys

# ... Imports from previous script (RUNE_MAP, etc) ... 
# copying concise version

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

NUM_TO_TEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

LATIN_TO_NUM = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'OE': 22,
    'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28,
    'V': 1, 'Q': 5, 'Z': 14
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    return runes

def get_indices(runes_text):
    return [RUNE_MAP[c] for c in runes_text if c in RUNE_MAP]

def indices_to_text(indices):
    return "".join([NUM_TO_TEXT[x] for x in indices])

def text_to_indices(text):
    text = text.upper()
    indices = []
    i = 0
    sorted_k = sorted(LATIN_TO_NUM.keys(), key=len, reverse=True)
    while i < len(text):
        matched = False
        for k in sorted_k:
            if text[i:].startswith(k):
                indices.append(LATIN_TO_NUM[k])
                i += len(k)
                matched = True
                break
        if not matched:
            i += 1
    return indices

def score_text(text):
    # Simple bigram scorer or just common words
    common = ["THE", "AND", "ING", "ION", "OF", "TO", "A", "IS", "IT", "THAT", "YOU", "WEL", "COM"]
    score = 0
    for w in common:
        score += text.count(w)
    return score

def main():
    runes = load_runes("61")
    cipher = get_indices(runes)
    
    # Split at 50
    cipher_start = cipher[:50]
    cipher_rest = cipher[50:]
    
    print("Check Part 1 (0-50):")
    div_key = text_to_indices("DIVINITY")
    
    # Analyze window by window for the rest
    # We want to find which Offset is best for each chunk.
    
    window_size = 20
    step = 5
    
    print("\n--- Scanning Remaining Cipher (Index 50+) ---")
    
    for i in range(0, len(cipher_rest), step):
        chunk = cipher_rest[i:i+window_size]
        if len(chunk) < 5: break
        
        best_score = -1
        best_off = -1
        best_txt = ""
        
        for off in range(8):
            # Key for this window
            # Base key is DIVINITY...
            # At index `i` (relative to start of rest), key index would be `i % 8` if no shift.
            # But we apply `off` as an EXTRA shift.
            # Effective key index = (i + off) % 8
            
            # Construct key indices for this chunk
            k_indices = []
            for j in range(len(chunk)):
                k_idx = (i + j + off) % 8
                k_indices.append(div_key[k_idx])
            
            # Decrypt
            plain = []
            for j in range(len(chunk)):
                 p = (chunk[j] - k_indices[j]) % 29
                 plain.append(p)
            
            txt = indices_to_text(plain)
            sc = score_text(txt)
            
            if sc > best_score:
                best_score = sc
                best_off = off
                best_txt = txt
        
        # Only print if score is decent
        if best_score > 0:
            print(f"Index {50+i}: Offset {best_off} -> {best_txt} (Score: {best_score})")

if __name__ == "__main__":
    main()

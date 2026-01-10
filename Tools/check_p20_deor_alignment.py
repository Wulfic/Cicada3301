
import sys
import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

# Mapping from OE Latin transcription to Gematria Indices
CHAR_MAP = {
    'f': 0, 'u': 1, 'o': 3, 'r': 4, 'c': 5, 'k': 5, 'g': 6, 'w': 7, 
    'h': 8, 'n': 9, 'i': 10, 'j': 11, 'p': 13, 'x': 14, 's': 15, 
    't': 16, 'b': 17, 'e': 18, 'm': 19, 'l': 20, 'd': 23, 'a': 24, 'y': 26,
    'þ': 2, 'ð': 2, 'æ': 25
}

# Digraphs
DIGRAPHS = {
    'th': 2, 'eo': 12, 'ng': 21, 'oe': 22, 'ae': 25, 'ia': 27, 'io': 27, 'ea': 28
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def parse_oe_text(text):
    text = text.lower()
    indices = []
    i = 0
    while i < len(text):
        # 3 chars? (none in standard mapping)
        
        # 2 chars
        if i < len(text) - 1:
            pair = text[i:i+2]
            if pair in DIGRAPHS:
                indices.append(DIGRAPHS[pair])
                i += 2
                continue
        
        # 1 char
        c = text[i]
        if c in CHAR_MAP:
            indices.append(CHAR_MAP[c])
        elif c.isalpha():
            # Fallback for letters not in map?
            # 'v' -> 'u'
            if c == 'v': indices.append(1)
            # 'z' -> 's'?
            elif c == 'z': indices.append(15)
            # 'q' -> 'k' -> 'c'
            elif c == 'q': indices.append(5)
            pass 
        i += 1
    return indices

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    deor_path = os.path.join(repo, "Analysis", "Reference_Docs", "deor_poem.txt")
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    # Read Deor text
    with open(deor_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
        # Only take the OE part
        if "MODERN ENGLISH" in full_text:
            oe_text = full_text.split("MODERN ENGLISH")[0]
        else:
            oe_text = full_text
    
    # Remove header if present
    if "DEOR POEM (OLD ENGLISH)" in oe_text:
        oe_text = oe_text.split("DEOR POEM (OLD ENGLISH)")[1]
            
    # Convert Deor to Indices
    deor_indices = parse_oe_text(oe_text)
    print(f"Deor Length (Indices): {len(deor_indices)}")
    print(f"Preview Deor: {text_from_indices(deor_indices[:50])}")
    
    # Read Page 20
    cipher = load_runes(p20_path)
    print(f"P20 Length: {len(cipher)}")
    
    limit = min(len(cipher), len(deor_indices))
    
    # K = C - P (assuming P=Deor, C=P+K)  -> K = C - Deor
    # K = P - C (assuming C=P-K)
    # K = C + P (assuming C=K-P or something weird)
    
    modes = ['C-P', 'P-C', 'C+P']
    
    for mode in modes:
        key_guess = []
        for i in range(limit):
            c = cipher[i]
            p = deor_indices[i]
            
            if mode == 'C-P':
                k = (c - p) % 29
            elif mode == 'P-C':
                k = (p - c) % 29
            elif mode == 'C+P':
                k = (c + p) % 29
                
            key_guess.append(k)
        
        txt = text_from_indices(key_guess)
        print(f"\n--- Mode {mode} ---")
        print(f"Key Preview: {txt[:100]}")
        
        # Check if key looks like English
        # Or if it looks like Primes? 2, 3, 5, 7, 11...
        # Map values to see if they are mostly prime indices?
        
    # Also try sliding deor against cipher
    print("\n--- Sliding Deor Window ---")
    best_ioc = 0
    best_offset = 0
    
    # No, sliding is for finding matches. Here we assume Key coherence.
    # What if Deor starts later?
    
if __name__ == "__main__":
    main()

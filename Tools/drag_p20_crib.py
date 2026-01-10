import os
import collections

# GP Mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TO_VAL = {
    "F": 0, "U": 1, "V": 1, "TH": 2, "O": 3, "R": 4, "C": 5, "K": 5, "Q": 5, 
    "G": 6, "W": 7, "H": 8, "N": 9, "I": 10, "J": 11, "EO": 12, "P": 13, 
    "X": 14, "Z": 15, "S": 15, "T": 16, "B": 17, "E": 18, "M": 19, "L": 20, 
    "NG": 21, "OE": 22, "D": 23, "A": 24, "AE": 25, "Y": 26, "IA": 27, "EA": 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

# GP Values corresponding to indices 0-28
# F=2, U=3, TH=5, O=7, R=11...
GP_VALS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def parse_text(text):
    text = text.upper().replace(' ', '')
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LATIN_TO_VAL:
                indices.append(LATIN_TO_VAL[two])
                i += 2
                continue
        c = text[i]
        if c in LATIN_TO_VAL:
            indices.append(LATIN_TO_VAL[c])
        i += 1
    return indices

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    cribs = [
        "PATHTOTHEDEOR",
        "PRIMESNUMBERS",
        "REARRANGING",
        "THEPRIMES",
        "WELUNDHIMBEWURMAN", # Deor start
        "TOTIENTFUNCTION"
    ]
    
    modes = ['SUB', 'ADD'] # K = C - P or P = C + K -> K = P - C (Wait, P=C+K => K=P-C)
    
    for crib_txt in cribs:
        crib = parse_text(crib_txt)
        print(f"\n--- Crib: {crib_txt} ---")
        
        for offset in range(len(cipher) - len(crib)):
            seg = cipher[offset : offset+len(crib)]
            
            # Key guesses
            # If C = P + K (ADD), then K = (C - P) % 29
            # If C = P - K (SUB), then K = (P - C) % 29 ... NO: C = P - K => K = P - C ? NO. P - K = C => K = P - C.
            # If C = K - P (REV), then K = C + P
            
            # Standard Vigenere ADD: P = (C - K)%29 => K = (C - P)%29
            k_add = [(c - p) % 29 for c, p in zip(seg, crib)]
            
            # Standard Vigenere SUB: P = (C + K)%29 => K = (P - C)%29
            k_sub = [(p - c) % 29 for c, p in zip(seg, crib)]
            
            # Check if K looks like Primes?
            # Primes in Index form: 2, 3, 5, 7, 11, 13 (indices in GP alphabet)?
            # Indices where index itself is Prime?
            # Or Indices that map to Prime GP Values (All of them do).
            
            # Check English Key
            # We assume Key is English for Running Key.
            k_add_txt = "".join([LATIN_TABLE[x] for x in k_add])
            k_sub_txt = "".join([LATIN_TABLE[x] for x in k_sub])
            
            # Minimal heuristic: Count vowels or common letters?
            # Or just print best matches (e.g. if we find "THE")
            
            if "THE" in k_add_txt:
                print(f"Offset {offset} (ADD): KeyPart={k_add_txt}")
            if "THE" in k_sub_txt:
                # print(f"Offset {offset} (SUB): KeyPart={k_sub_txt}")
                pass

if __name__ == "__main__":
    main()

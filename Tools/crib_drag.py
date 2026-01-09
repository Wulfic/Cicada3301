import os

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

ENG_TO_IDX = {
    'F': 0, 'U': 1, 'V': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'Q': 5,
    'G': 6, 'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'Z': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20,
    'NG': 21, 'ING': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IO': 27, 'EA': 28
}

def clean_runes(text):
    return [c for c in text if c in RUNE_MAP]

def runes_to_indices(runes):
    return [RUNE_MAP[r] for r in runes]

def indices_to_eng(indices):
    return "".join([LETTERS[i] for i in indices])

def text_to_indices(text):
    key = []
    i = 0
    text = text.upper().replace(" ", "")
    while i < len(text):
        if i < len(text) - 1:
            two_char = text[i:i+2]
            if two_char in ENG_TO_IDX:
                key.append(ENG_TO_IDX[two_char])
                i += 2
                continue
        char = text[i]
        if char in ENG_TO_IDX:
            key.append(ENG_TO_IDX[char])
        i += 1
    return key

def run():
    runes_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_17\runes.txt"
    with open(runes_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    clean_content = clean_runes(content)
    cipher_indices = runes_to_indices(clean_content)
    atbash_indices = [28 - i for i in cipher_indices]
    
    cribs = [
        "A KOAN", "AN INSTRUCTION", "SOME WISDOM", "WELCOME", "THE LOSS", 
        "WE HAVE", "MOST THINGS", "IT IS", "I AM", "CONSUMPTION", "PRESERVATION",
        "ADHERENCE", "DIVINITY", "CIRCUMFERENCE", "INTERNET", "THE INST AR", "TRUST"
    ]
    
    print("--- CRIB DRAG: NORMAL (Key = C - P) ---")
    for crib in cribs:
        plain_indices = text_to_indices(crib)
        if len(plain_indices) > len(cipher_indices): continue
        
        # Calculate Key
        key = []
        for i in range(len(plain_indices)):
            k = (cipher_indices[i] - plain_indices[i]) % 29
            key.append(k)
        
        # Check if Key looks reasonable (simple heuristic)
        key_str = indices_to_eng(key)
        print(f"Crib '{crib:<15}' -> Key: {key_str}")

    print("\n--- CRIB DRAG: ATBASH (Key = C' - P) ---")
    for crib in cribs:
        plain_indices = text_to_indices(crib)
        if len(plain_indices) > len(atbash_indices): continue
        
        key = []
        for i in range(len(plain_indices)):
            k = (atbash_indices[i] - plain_indices[i]) % 29
            key.append(k)
        
        key_str = indices_to_eng(key)
        print(f"Crib '{crib:<15}' -> Key: {key_str}")

if __name__ == "__main__":
    run()

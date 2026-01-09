
import os

RUNE_MAP = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 'ᚹ': 'W',
    'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 'ᛉ': 'X', 'ᛋ': 'S',
    'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D',
    'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA', 'ᛠ': 'EA'
}

SUBST_MAP = {
    'D': 'D',    # ᛞ -> D (23 -> 23)
    'W': 'E',    # ᚹ -> E (7 -> 18)
    'H': 'C',    # ᚻ -> C (8 -> 5)
    'B': 'R',    # ᛒ -> R (17 -> 4)
    'NG': 'Y',   # ᛝ -> Y (21 -> 26)
    'F': 'P',    # ᚠ -> P (0 -> 13)
    'A': 'T',    # ᚪ -> T (24 -> 16)
    'C': 'I',    # ᚳ -> I (5 -> 10)
    'J': 'O',    # ᛄ -> O (11 -> 3)
    'U': 'N',    # ᚢ -> N (1 -> 9)
    'EA': 'W',   # ᛠ -> W (28 -> 7)
    'E': 'A',    # ᛖ -> A (18 -> 24)
    'I': 'R',    # ᛁ -> R (10 -> 4)
    'G': 'N',    # ᚷ -> N (6 -> 9)
    'X': 'I',    # ᛉ -> I (14 -> 10)
    'S': 'G',    # ᛋ -> G (15 -> 6)
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    return runes

def decrypt_runes(runes, mapping):
    text = runes.replace('\n', ' • ').replace(' ', ' • ')
    res = []
    
    char_to_name = {k: v for k, v in RUNE_MAP.items() if isinstance(k, str) and len(k)==1}
    
    parts = text.split('•')
    for p in parts:
        if not p.strip(): continue
        word_plain = []
        for char in p.strip():
            if char in char_to_name:
                rune_name = char_to_name[char]
                if rune_name in mapping:
                    word_plain.append(mapping[rune_name])
                else:
                    word_plain.append(f"_{rune_name}_")
            else:
                word_plain.append(char)
        res.append("".join(word_plain))
            
    return " ".join(res)

def main():
    runes71 = load_runes("71")
    decrypted = decrypt_runes(runes71, SUBST_MAP)
    print("--- PAGE 71 HOMOPHONIC DECRYPTION ---")
    print(decrypted)

if __name__ == "__main__":
    main()

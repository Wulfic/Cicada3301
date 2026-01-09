import os

# Configurations
RUNE_TO_LETTER = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G', 'ᚹ': 'W',
    'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 'ᛉ': 'X', 'ᛋ': 'S',
    'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L', 'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D',
    'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IO', 'ᛠ': 'EA',
    '•': ' ', '\n': '\n'
}

PAGES_TO_TRANSLATE = [58, 60, 63, 68, 71, 72, 74]

def translate_runes(content):
    res = []
    for char in content:
        if char in RUNE_TO_LETTER:
            res.append(RUNE_TO_LETTER[char])
        else:
            # Keep numbers/other chars
            res.append(char)
    return "".join(res)

def main():
    base_dir = "LiberPrimus/pages"
    
    for p in PAGES_TO_TRANSLATE:
        dir_path = os.path.join(base_dir, f"page_{p:02d}")
        runes_path = os.path.join(dir_path, "runes.txt")
        decoded_path = os.path.join(dir_path, "decoded.txt")
        
        if os.path.exists(runes_path):
            with open(runes_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            translated = translate_runes(content)
            
            print(f"--- Page {p} ---")
            print(translated[:100].replace('\n', ' '))
            
            with open(decoded_path, 'w') as f:
                f.write(f"Key: NONE (Direct Translation)\n")
                f.write(translated)

if __name__ == "__main__":
    main()


KEY = [19, 6, 23, 16, 10, 22, 9, 27, 26, 11, 16, 3, 19, 0, 12, 7, 23, 17, 7, 1, 1, 5, 28, 7, 20, 21, 15, 1, 17, 20, 23, 8, 22, 9, 20, 16, 7, 8, 13, 22, 15, 10, 2, 11, 22, 22, 4, 9, 19, 24, 1, 8, 12, 18, 21, 11, 21, 22, 21, 12, 7, 6, 13, 1, 14, 12, 26, 11, 11, 5, 27, 21, 25, 8, 22, 15, 20, 4, 20, 4, 19, 26, 0, 19, 1, 6, 2, 3, 22, 26, 24, 1, 19, 22, 12, 0, 21, 18, 20, 5, 17, 4, 24, 10, 19, 14, 19, 7, 12, 12, 14, 16, 2]

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

def main():
    with open(r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt', 'r', encoding='utf-8') as f:
        runes_text = f.read()
    
    indices = []
    key_idx = 0
    key_len = len(KEY)
    
    for char in runes_text:
        if char in RUNE_MAP:
            rune_val = RUNE_MAP[char]
            k = KEY[key_idx % key_len]
            plain_val = (rune_val - k) % 29
            indices.append(plain_val)
            key_idx += 1

    # Search for [23, 3, 18, 2] (DOETH)
    search_seq = [23, 3, 18, 2]
    
    found = False
    for i in range(len(indices) - len(search_seq) + 1):
        if indices[i:i+len(search_seq)] == search_seq:
            print(f"Found DOETH at index {i}")
            found = True
            
    if not found:
        print("DOETH not found in indices.")

    # Search for [6, 3, 18, 2] (GOETH)
    search_seq = [6, 3, 18, 2]
    for i in range(len(indices) - len(search_seq) + 1):
        if indices[i:i+len(search_seq)] == search_seq:
            print(f"Found GOETH at index {i}")

    # Search for [8, 24, 2] (HATH)
    search_seq = [8, 24, 2]
    for i in range(len(indices) - len(search_seq) + 1):
        if indices[i:i+len(search_seq)] == search_seq:
            print(f"Found HATH at index {i}")

if __name__ == "__main__":
    main()

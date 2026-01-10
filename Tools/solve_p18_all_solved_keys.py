
import os
import re

# Rune to index mapping (Gematria Primus)
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4,
    'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19,
    'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H', 9: 'N',
    10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M',
    20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

LETTER_TO_IDX = {}
for idx, letters in LATIN_TABLE.items():
    LETTER_TO_IDX[letters] = idx

LETTER_TO_IDX['K'] = 5
LETTER_TO_IDX['Q'] = 5
LETTER_TO_IDX['V'] = 1
LETTER_TO_IDX['Z'] = 15

def text_to_indices(text):
    text = text.upper().replace(' ', '').replace('\n', '')
    indices = []
    i = 0
    digraphs = ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO', 'IA'] 
    
    while i < len(text):
        matched = False
        for dg in digraphs:
            if text[i:i+2] == dg:
                indices.append(LETTER_TO_IDX.get(dg, 0))
                i += 2
                matched = True
                break
        if not matched:
            char = text[i]
            if char in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[char])
            elif char.isalpha():
                 # Handle unmapped chars if any (should be caught by Q,K,V,Z map)
                 pass
            i += 1
    return indices

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def decrypt(cipher_indices, key_indices, mode='SUB'):
    decrypted = []
    key_len = len(key_indices)
    if key_len == 0: return ""
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        if mode == 'SUB':
            p = (c - k) % 29
        elif mode == 'ADD':
            p = (c + k) % 29
        elif mode == 'SUB_REV':
            p = (k - c) % 29
        decrypted.append(LATIN_TABLE[p])
    return "".join(decrypted)

def score_text(text):
    common = ['THE', 'AND', 'ING', 'ION', 'THAT', 'WITH', 'WHO', 'THIS', 'NOT', 'FOR', 'BUT', 'ARE', 'ALL', 'FROM']
    score = 0
    for w in common:
        score += text.count(w) * len(w)
    return score

def main():
    repo_root = r"c:\Users\tyler\Repos\Cicada3301"
    p18_path = os.path.join(repo_root, "LiberPrimus", "pages", "page_18", "runes.txt")
    
    if not os.path.exists(p18_path):
        print("Page 18 runes not found")
        return

    cipher_indices = load_runes(p18_path)
    print(f"Loaded Page 18: {len(cipher_indices)} runes")

    # Scrape solved pages
    solved_texts = {}
    pages_dir = os.path.join(repo_root, "LiberPrimus", "pages")
    for page_name in os.listdir(pages_dir):
        readme_path = os.path.join(pages_dir, page_name, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple extraction: look for code blocks or cleartext sections
                # This is heuristic.
                # Look for "Plaintext Preview" or blocks after "Decrypted"
                # Or simply look for the large run of CAPS text
                matches = re.findall(r'[A-Z ]{20,}', content) 
                # Pick longest match as candidate
                if matches:
                    candidate = max(matches, key=len)
                    if len(candidate) > 50:
                        solved_texts[page_name] = candidate

    print(f"Loaded {len(solved_texts)} solved texts as key candidates.")

    # Also add manually defined Page 17 text since extraction might fail
    solved_texts['page_17_manual'] = "EPILOGUE WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE AND TO FIND IT"
    
    modes = ['SUB', 'ADD', 'SUB_REV']
    best_score = 0
    best_info = ""

    for source, text in solved_texts.items():
        key_indices = text_to_indices(text)
        if len(key_indices) < 5: continue
        
        for mode in modes:
            # Try as exact key (repeating)
            dec = decrypt(cipher_indices, key_indices, mode)
            s = score_text(dec)
            if s > best_score:
                best_score = s
                best_info = f"Source: {source} Mode: {mode} (Repeated)\nResult: {dec[:100]}"

            # Try as running key (if long enough)
            if len(key_indices) >= len(cipher_indices):
                 dec = decrypt(cipher_indices, key_indices[:len(cipher_indices)], mode)
                 s = score_text(dec)
                 if s > best_score:
                    best_score = s
                    best_info = f"Source: {source} Mode: {mode} (Running)\nResult: {dec[:100]}"
            
            # Try running key with offsets (if key is much longer)
            if len(key_indices) > len(cipher_indices) + 10:
                for i in range(0, len(key_indices) - len(cipher_indices), 10):
                     dec = decrypt(cipher_indices, key_indices[i:i+len(cipher_indices)], mode)
                     s = score_text(dec)
                     if s > best_score:
                        best_score = s
                        best_info = f"Source: {source} Mode: {mode} (Offset {i})\nResult: {dec[:100]}"

    print("\nBest Result:")
    print(best_info)

if __name__ == "__main__":
    main()

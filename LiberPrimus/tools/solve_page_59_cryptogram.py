
import os
from collections import Counter

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

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    return runes

def get_word_patterns(runes_text):
    # Split by dot or newline
    # Normalized separators
    text = runes_text.replace('\n', '•').replace(' ', '•')
    words_raw = text.split('•')
    
    analyzed_words = []
    
    for w in words_raw:
        if not w: continue
        indices = [RUNE_MAP[c] for c in w if c in RUNE_MAP]
        if not indices: continue
        
        # Make pattern
        seen = {}
        res = []
        next_code = 0
        for x in indices:
            if x not in seen:
                seen[x] = next_code
                next_code += 1
            res.append(str(seen[x]))
        pattern = ".".join(res)
        
        txt = "-".join([NUM_TO_TEXT[x] for x in indices])
        analyzed_words.append({
            'indices': indices,
            'pattern': pattern,
            'txt': txt,
            'len': len(indices)
        })
    return analyzed_words

def main():
    runes = load_runes("59")
    words = get_word_patterns(runes)
    
    print(f"Found {len(words)} words.")
    
    print("\n--- WORD ANALYSIS ---")
    for i, w in enumerate(words):
        print(f"Word {i}: {w['txt']} (Len {w['len']}, Pat {w['pattern']})")

    # Double Letter Words
    print("\n--- WORDS WITH DOUBLES ---")
    for i, w in enumerate(words):
        has_double = False
        for j in range(len(w['indices'])-1):
            if w['indices'][j] == w['indices'][j+1]:
                has_double = True
                break
        if has_double:
             print(f"Word {i}: {w['txt']}")
             
    # One Letter Words
    print("\n--- ONE LETTER WORDS ---")
    for i, w in enumerate(words):
        if w['len'] == 1:
            print(f"Word {i}: {w['txt']} -> Likely 'A' or 'I'")

    # Word 0 is 'R'. Single letter. Probably 'A'.
    # Word 1 is 'NG-R-A-M-W'. 5 letters. Pattern 0.1.2.3.4? No...
    # Let's re-verify patterns.

if __name__ == "__main__":
    main()

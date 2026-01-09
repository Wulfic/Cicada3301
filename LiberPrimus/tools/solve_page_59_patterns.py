
import os
from collections import Counter
import re

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

def get_indices(runes_text):
    return [RUNE_MAP[c] for c in runes_text if c in RUNE_MAP]

def get_pattern(indices):
    # e.g. [4, 21, 4] -> "0.1.0"
    seen = {}
    res = []
    next_code = 0
    for x in indices:
        if x not in seen:
            seen[x] = next_code
            next_code += 1
        res.append(str(seen[x]))
    return ".".join(res)

def main():
    # Load Dict words
    words = ["THE", "AND", "OF", "TO", "A", "IN", "IS", "I", "THAT", "IT", "FOR", "YOU", "WAS", "WITH", "ON", "AS", "HAVE", "BUT", "BE", "THEY", "PROGRAM", "SYSTEM", "WARNING", "WELCOME", "BELIEVE", "NOTHING", "BOOK", "PRIMUS", "LIBER", "CIPHER", "CODE", "RUNES", "CHAPTER", "INTUS", "SECTION", "AN", "END", "BEGINNING", "PRESERVE", "CONSUME", "ADHERE", "INSTRUCTION", "WISDOM", "WORDS", "INTELLIGENCE", "PRIMES", "TOTIENT", "NUMBERS", "SACRED", "DIVINITY", "CIRCUMFERENCE", "PILGRIM", "JOURNEY", "TITLE", "AUTHOR", "MESSAGE", "SECRET", "HIDDEN", "TRUTH", "BELIEF", "SYSTEMS"]
    
    word_patterns = {}
    for w in words:
        pat = []
        seen = {}
        nc = 0
        for c in w:
            if c not in seen:
                seen[c] = nc
                nc += 1
            pat.append(str(seen[c]))
        key = ".".join(pat)
        if key not in word_patterns: word_patterns[key] = []
        word_patterns[key].append(w)
        
    runes = load_runes("59")
    indices = get_indices(runes)
    
    print("Page 59 Cipher Pattern Search:")
    
    # Try windows of length 4 to 12
    for length in range(4, 13):
        for i in range(len(indices) - length + 1):
            window = indices[i:i+length]
            pat = get_pattern(window)
            if pat in word_patterns:
                candidates = word_patterns[pat]
                window_txt = "-".join([NUM_TO_TEXT[x] for x in window])
                print(f"Match at {i}: {window_txt} -> {candidates}")
                
                # Check for "SYSTEM" specifically
                if "SYSTEM" in candidates:
                    print("!!! FOUND SYSTEM !!!")
                if "WARNING" in candidates:
                    print("!!! FOUND WARNING !!!")
                if "CIPHER" in candidates:
                    print("!!! FOUND CIPHER !!!")

if __name__ == "__main__":
    main()


import os
import random
import collections

# GP Mapping
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def score_text(indices):
    english_freq = {
        0: 0.02, 1: 0.02, 2: 0.05, 3: 0.06, 4: 0.05, 5: 0.03, 6: 0.02, 7: 0.02, 
        8: 0.05, 9: 0.06, 10: 0.06, 11: 0.01, 12: 0.01, 13: 0.02, 14: 0.001, 
        15: 0.05, 16: 0.07, 17: 0.02, 18: 0.10, 19: 0.03, 20: 0.03, 21: 0.01, 
        22: 0.01, 23: 0.03, 24: 0.06, 25: 0.01, 26: 0.02, 27: 0.01, 28: 0.01
    }
    score = 0
    for x in indices:
        score += english_freq.get(x, 0)
    return score

def to_latin(runes):
    return "".join([LATIN_TABLE[r] for r in runes])

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    
    # Extract Prime Columns (Rows horizontal)
    COLS = 29
    ROWS = 28
    prime_cols = [c for c in range(COLS) if is_prime(c)]
    
    stream = []
    # Row by Row to preserve horizontal reading
    for r in range(ROWS):
        for c in prime_cols:
            stream.append(cipher[r*COLS + c])
            
    print(f"Cracking Prime Column Stream (Len {len(stream)})...")
    
    # Hill Climbing (Single Monoalphabetic Shift? NO, likely Vigenere)
    # But try simple shifts first (Caesar)
    print("--- Caesar Check ---")
    for s in range(29):
        plain = [(c - s) % 29 for c in stream]
        # Basic check: THE
        txt = to_latin(plain)
        if "THE" in txt:
            print(f"Shift {s}: {txt[:60]}")
            
    # Try Random Hill Climbing for Vigenere Key (Len 3 to 15)
    print("--- Hill Climbing Vigenere ---")
    
    target_len = len(stream)
    best_overall_score = 0
    best_key = []
    
    for klen in range(3, 15):
        # Init Random Key
        key = [random.randint(0, 28) for _ in range(klen)]
        best_score = -1
        
        # Mutation Loop
        for i in range(2000):
            # Mutate
            new_key = list(key)
            idx = random.randint(0, klen-1)
            new_key[idx] = random.randint(0, 28)
            
            # Score
            plain = []
            for j, c in enumerate(stream):
                k = new_key[j % klen]
                plain.append((c - k) % 29)
                
            s = score_text(plain)
            
            if s > best_score:
                best_score = s
                key = new_key
                
        if best_score > best_overall_score:
            best_overall_score = best_score
            best_key = key
            print(f"New Best (Len {klen}): Score {best_score:.2f} Key {key}")
            plain = [(c - key[j%len(key)]) % 29 for j, c in enumerate(stream)]
            print(f"Preview: {to_latin(plain[:80])}")

if __name__ == "__main__":
    main()

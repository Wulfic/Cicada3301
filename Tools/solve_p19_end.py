
import sys

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

# Column data from inspection
# Idx 43 (F): N E R S I
# Idx 44 (F): M B TH N B
# Idx 45 (F): M L G NG F
# Idx 46 (F): C X C I N

COLS = [
    ['N', 'E', 'R', 'S', 'I'],
    ['M', 'B', 'TH', 'N', 'B'],
    ['M', 'L', 'G', 'NG', 'F'],
    ['C', 'X', 'C', 'I', 'N']
]

COL_VALS = []
for col in COLS:
    vals = [LATIN_TABLE.index(c) for c in col]
    COL_VALS.append(vals)

ENGLISH_FREQ = {
    'E': 12.0, 'T': 9.0, 'A': 8.0, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8,
    'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2, 'Q': 0.1, 'Z': 0.1
}

def get_char_score(char_idx):
    char = LATIN_TABLE[char_idx]
    # Map runes to English approximate freq
    if char == 'TH': return 5.0 # High freq
    if char == 'NG': return 2.0
    if char == 'OE': return 0.5
    if char == 'AE': return 0.5
    if char == 'EA': return 0.5
    if char == 'IA': return 0.2
    if char == 'EO': return 0.2
    return ENGLISH_FREQ.get(char, 0.0)

def solve():
    print("Analyzing last 4 key bytes...")
    
    best_keys = []
    
    # Analyze each column independently first
    for i, col_vals in enumerate(COL_VALS):
        print(f"\nColumn {43+i}:")
        scores = []
        for k in range(29):
            score = 0
            chars = []
            for c in col_vals:
                p = (c + k) % 29
                score += get_char_score(p)
                chars.append(LATIN_TABLE[p])
            scores.append((score, k, LATIN_TABLE[k], chars))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        best_keys.append(scores[:5]) # Keep top 5 candidates
        
        for s, k, kc, chars in scores[:5]:
            print(f"  K={kc} ({k}): Score={s:.1f} -> {chars}")

    # Combine to form words
    print("\nAttempting to form Key words (Indices 43-46):")
    candidates = []
    
    # Iterate through top 5 of each column
    for k0_info in best_keys[0]:
        for k1_info in best_keys[1]:
            for k2_info in best_keys[2]:
                for k3_info in best_keys[3]:
                    key_word = k0_info[2] + k1_info[2] + k2_info[2] + k3_info[2]
                    total_score = k0_info[0] + k1_info[0] + k2_info[0] + k3_info[0]
                    candidates.append((total_score, key_word, k0_info, k1_info, k2_info, k3_info))
                    
    candidates.sort(key=lambda x: x[0], reverse=True)
    
    print("\nTop Key Candidates (by Englishness of Plaintext):")
    for item in candidates[:20]:
        print(f"{item[1]}: {item[0]:.1f}")

if __name__ == "__main__":
    solve()

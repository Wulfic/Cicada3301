
import os
import random
import math
from collections import Counter

# GP Layout
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

# Standard English frequencies (approximate)
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3,
    'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
    'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0,
    'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07, 'TH': 2.0, 'NG': 1.0, 'EO': 0.1, 'AE': 0.1, 'IA': 0.1, 'OE': 0.1, 'EA': 0.1
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    return runes

def get_indices(runes_text):
    return [RUNE_MAP[c] for c in runes_text if c in RUNE_MAP]

def main():
    runes = load_runes("59")
    indices = get_indices(runes)
    
    print(f"Total Runes: {len(indices)}")
    
    # 1. Frequency Analysis
    counts = Counter(indices)
    total = len(indices)
    
    print("\n--- Rune Frequencies ---")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    for idx, count in sorted_counts:
        rune_char = NUM_TO_TEXT[idx]
        freq = (count / total) * 100
        print(f"Rune {idx} ({rune_char}): {count} ({freq:.2f}%)")
        
    print("\n--------------------------")
    print("Compare with English High Freq: E, T, A, O, I, N, S, H, R")
    
    # Suggest mapping
    print("\nPotential Mapping:")
    english_order = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U', 'C', 'M', 'F', 'W', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
    
    mapping = {}
    for i, (idx, count) in enumerate(sorted_counts):
        if i < len(english_order):
            mapping[idx] = english_order[i]
            print(f"{NUM_TO_TEXT[idx]} -> {english_order[i]}")
        else:
            mapping[idx] = '?'
            
    # Custom Mapping Experiment
    print("\n--- Custom Mapping Decryption ---")
    
    # Starting based on Frequencies: E, T, A, O, I, N...
    # I(10, 14%) -> E
    # AE(25, 10%) -> T
    # A(24, 8%) -> A?
    # E(18, 6%) -> O?
    
    # Pattern "SYSTEM?": R(4)=S, NG(21)=Y, A(24)=T, M(19)=E, W(7)=M
    # Conflict: M=E vs I=E.
    
    # Try Mapping based on "SYSTEM" match
    # R->S, NG->Y, A->T, M->E, W->M, J->A, I->T, H->I, E->C
    # SYSTEMATIC?
    
    custom_map = {
        4: 'A',  # R
        21: 'N', # NG
        24: 'G', # A
        19: 'R', # M
        7: 'A',  # W
        11: 'M', # J
        10: 'E', # I  (High Freq)
        # ...
    }
    
    # Let's try to solve ANAGRAM?
    # R(4)=A, NG(21)=N, A(24)=G, M(19)=R, W(7)=A, J(11)=M
    # Text: ANAGRAMME?
    
    decoded = []
    for idx in indices:
        decoded.append(custom_map.get(idx, '_'))
    
    print("".join(decoded))
    
    print("\n--- PATTERN ANALYSIS ---")
    # Look for doubles
    doubles = []
    for i in range(len(indices)-1):
        if indices[i] == indices[i+1]:
            doubles.append(NUM_TO_TEXT[indices[i]])
    print(f"Doubles found: {Counter(doubles)}")
    # English doubles: LL, EE, SS, TT, OO, MM, FF, PP

if __name__ == "__main__":
    main()

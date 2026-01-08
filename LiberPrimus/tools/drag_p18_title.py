from solve_page_18 import load_runes, RUNE_MAP, ENG_TO_IDX, LETTERS, indices_to_eng

def run_crib_drag():
    title_runes = [
        28, 24, 11, 12, 28, 20,  # EA A J EO EA L (6)
        4, 6, 15,                # R G S (3)
        7, 3, 17, 10,            # W O B I (4)
        28, 5,                   # EA C (2)
        10, 23, 11,              # I D J (3)
        18, 19, 4,               # E M R (3)
        6                        # G (1)
    ]
    
    # Structure: 6 3 4 2 3 3 1
    
    cribs_6 = ["WISDOM", "WITHIN", "INSIDE", "FOLLOW", "DIVINE", "BECOME", "TARGET", "SOURCE", "SYSTEM", "NUMBER", "PRIMES"]
    cribs_3 = ["THE", "AND", "FOR", "NOT", "YOU", "ARE", "BUT", "ALL", "ANY", "CAN", "DID", "GET", "HAS", "HIM", "HIS", "HOW", "NEW", "NOW", "OLD", "ONE", "OUT", "OWN", "SAY", "SHE", "SEE", "TOO", "TWO", "USE", "WAY", "WHO", "WHY"]
    
    print("--- Crib Drag Analysis (Title P18) ---")
    
    # Test Word 1 (6 Runes)
    print("\n[Word 1: 6 Runes]")
    c_word1 = title_runes[0:6]
    for crib in cribs_6:
        # Calculate Key if P = Crib
        # C - K = P => K = C - P
        # C + K = P => K = P - C
        
        # Assume Standard: K = C - P
        key_std = []
        for i, r in enumerate(c_word1):
            p_rune = ENG_TO_IDX[crib[i:i+1]] # Assuming crib is 1-char runes
            # Need strict rune handling for cribs
            # Actually cribs might have multi-char runes.
            # Let's simplify and assume 1-char for now or convert properly
            pass
            
    # Better approach: Just try to find a consistent key.
    # The key is likely "related" to P17.
    # P17 Key: YAHEOOPYJ (8)
    
    # Check if Title + P17 Key = Something readable
    key_runes = [26, 24, 8, 12, 3, 13, 26, 11] # Y A H EO O P Y J
    
    print("\nDecrypting Title with offset P17 keys:")
    for shift in range(8):
        rotated_key = key_runes[shift:] + key_runes[:shift]
        
        # Decrypt Standard (C - K)
        res_std = [(c - k) % 29 for c, k in zip(title_runes, rotated_key * 3)]
        print(f"Shift {shift} (C-K): {indices_to_eng(res_std)}")
        
        # Decrypt Variant (C + K)
        res_var = [(c + k) % 29 for c, k in zip(title_runes, rotated_key * 3)]
        
        # Format with word boundaries
        # lengths: 6, 3, 4, 2, 3, 3, 1
        pos = 0
        w_strs = []
        for length in [6, 3, 4, 2, 3, 3, 1]:
            chunk = res_var[pos:pos+length]
            w_strs.append(indices_to_eng(chunk))
            pos += length
            
        print(f"Shift {shift} (C+K): {' '.join(w_strs)}")

if __name__ == "__main__":
    run_crib_drag()


import os

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INV_RUNE_MAP = {v: k for k, v in RUNE_MAP.items()}
ENGLISH_MAP = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W', 8: 'H',
    9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S', 16: 'T',
    17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D', 24: 'A',
    25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    if not os.path.exists(path): return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '').replace(' ', '').replace('•', '')

def runes_to_vals(runes):
    return [RUNE_MAP[r] for r in runes if r in RUNE_MAP]

def vals_to_eng(vals):
    return "".join([ENGLISH_MAP[v] for v in vals])

def decrypt(cipher, key):
    res = []
    for c, k in zip(cipher, key):
        p = (c - k) % 29
        res.append(p)
    return res

def main():
    target_pg = "71"
    cipher_runes = load_runes(target_pg)
    cipher_vals = runes_to_vals(cipher_runes)
    


    # Load English Plaintext from solved pages
    import re
    full_english = ""
    print("Loading translations from pages...")
    for i in range(75):
        pg_name = f"page_{i:02d}"
        trans_path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\{pg_name}\\translation.md"
        if os.path.exists(trans_path):
            with open(trans_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Heuristic cleaning
                # Remove header lines
                content = re.sub(r'#.*', '', content)
                # Keep letters
                cleaned = re.sub(r'[^A-Z]', '', content.upper().replace('\n', ' '))
                full_english += cleaned

    print(f"DEBUG: First 200 chars of extracted English Solutions: {full_english[:200]}")


    
    # Tokenize English to Gematria Vals
    ENG_TO_VAL = {v: k for k, v in ENGLISH_MAP.items()}
    # Sort keys by length descending to match double-chars first
    sorted_tokens = sorted(ENG_TO_VAL.keys(), key=len, reverse=True)
    
    key_vals = []
    i = 0
    N = len(full_english)
    while i < N:
        matched = False
        for token in sorted_tokens:
            if full_english.startswith(token, i):
                key_vals.append(ENG_TO_VAL[token])
                i += len(token)
                matched = True
                break
        if not matched:
            # Skip chars that don't match (shouldn't happen with single letters available, 
            # unless it's Q or Z or something not in Gematria?)
            # Gematria lacks K, Q, V (V is U), Z?
            # ENGLISH_MAP: F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA
            # Missing: K (use C), Q (use CW?), V (use U), Z (use S?).
            # Handle standard mappings for missing letters
            char = full_english[i]
            if char == 'K': key_vals.append(ENG_TO_VAL['C'])
            elif char == 'V': key_vals.append(ENG_TO_VAL['U'])
            elif char == 'Z': key_vals.append(ENG_TO_VAL['S'])
            elif char == 'Q': key_vals.append(ENG_TO_VAL['C']) # Approximation
            else:
                pass # Ignore
            i += 1

    print(f"Extracted English Key Stream length: {len(key_vals)}")
    all_runes = key_vals

    # Target: Word 14 "DECRYPTION"
    # Runes: ᛞᚹᚻᛒᛝᚠᚪᚳᛄᚢ (23, 7, 8, 17, 21, 0, 24, 5, 11, 1)
    # Wait, 'DECRYPTION' vals:
    # D:23, E:18, C:5, R:4, Y:26, P:13, T:16, I:10, O:3, N:9
    # Runes in file at index 60: ᛞ, ᚹ, ᚻ... wait.
    # Let's verify the target runes again in the loop.
    
    target_len = 10
    target_vals = [23, 18, 5, 4, 26, 13, 16, 10, 3, 9] # DECRYPTION
    
    # Find the target segment in the cipher to anchor against
    # We know it starts at index 60 (as established in previous turns)
    # But let's actally locate the runes ᛞ etc.
    # From previous turn:
    # "Found DECRYPTION runes at index 60: [23, 7, 8, 17, 21, 0, 24, 5, 11, 1]"
    # Wait.
    # Plaintext "DECRYPTION" -> [23, 18, 5, 4, 26, 13, 16, 10, 3, 9]
    # Ciphertext at 60      -> [23, 7, 8, 17, 21, 0, 24, 5, 11, 1]
    # Key = (Cipher - Plain) or (Plain - Cipher)?
    # Standard Vigenere: Cipher = (Plain + Key) % 29  => Key = (Cipher - Plain)
    # Variant Beaufort:  Cipher = (Key - Plain) % 29  => Key = (Cipher + Plain) ? No. 
    #   K - P = C => K = C + P
    # Beaufort:          Cipher = (Plain - Key) % 29? No. usually (Key - Plain).
    #
    # If standard: Key = (C - P) % 29.
    # C=[23,7,8,17,21,0,24,5,11,1]
    # P=[23,18,5,4,26,13,16,10,3,9]
    # K[0] = (23-23)=0 (F)
    # K[1] = (7-18)=-11=18 (E)
    # K[2] = (8-5)=3 (O)
    # K[3] = (17-4)=13 (P)
    # K[4] = (21-26)=-5=24 (A)
    # K[5] = (0-13)=-13=16 (T)
    # K[6] = (24-16)=8 (H)
    # K[7] = (5-10)=-5=24 (A)
    # K[8] = (11-3)=8 (H)
    # K[9] = (1-9)=-8=21 (NG)
    # Key segment: F E O P A T H A H NG
    # This looks like English! "FEOPATHAHNG..."
    # "FEOPATH" is "THE POAF..." backwards/scrambled?
    # Or "F E O P A T H" -> The path?
    #
    # We are looking for this key sequence in the generated 'all_runes' (English transcript).
    
    expected_key_segment = []
    cipher_segment = cipher_vals[60:70]
    plain_segment = target_vals
    
    for c, p in zip(cipher_segment, plain_segment):
        expected_key_segment.append( (c - p) % 29 )
        
    print(f"Searching for key segment: {expected_key_segment} (Length {len(expected_key_segment)})")
    print(f"Vals: {vals_to_eng(expected_key_segment)}")
    
    # Heuristic Search for strict matches
    # But also, let's look for "PATH" (13, 24, 16, 8) in the English stream
    # because FEOPATH contains PATH.
    path_seq = [13, 24, 16, 8]
    
    print("\n--- Searching for 'PATH' in Key Stream ---")
    for i in range(len(all_runes) - 4):
        if all_runes[i:i+4] == path_seq:
            # Check context
            # We want to match FEOPATH...
            # expected: F E O P A T H
            #           0 18 3 13 24 16 8
            # The 'PATH' starts at index 3 of the expected key.
            # So if we found PATH at i, the potential match starts at i-3.
            
            start_idx = i - 3
            if start_idx < 0: continue
            
            candidate_segment = all_runes[start_idx : start_idx + len(expected_key_segment)]
            
            print(f"Found PATH at key index {i}. Context ({start_idx}): {vals_to_eng(candidate_segment)}")
            
            # Count matches
            matches = 0
            for k1, k2 in zip(candidate_segment, expected_key_segment):
                if k1 == k2: matches += 1
            
            print(f"  Match Score: {matches}/{len(expected_key_segment)}")
            
            if matches > 6: # Loose match
                print("  >> HIGH PROBABILITY MATCH <<")



            
    # Try running key
    # Slide the corpus over the cipher
    
    best_score = 0
    best_dec = ""
    
    cribs = ["DECRYPTION", "WARNING", "MYCELIUM", "DIVINITY"]
    
    # We simply look for the crib in the decrypted output
    # Convert cribs to values? No, simplistic check first.
    # Actually, DECRYPTION is vals [23, 18, 5, 4, 26, 13, 16, 10, 3, 9]
    
    crib_vals = {
        "DECRYPTION": [23, 18, 5, 4, 26, 13, 16, 10, 3, 9],
        "WARNING": [28, 24, 4, 9, 10, 9, 6], # Using EA=W, E=A ?? No.
        # Plaintext "WARNING" vals: W(7), A(24), R(4), N(9), I(10), N(9), G(6)
        "WARNING_PLAIN": [7, 24, 4, 9, 10, 9, 6],
        "MYCELIUM": [20, 26, 5, 18, 20, 10, 1, 20] # M Y C E L I U M
    }
    
    print(f"Total corpus length: {len(all_runes)}")
    print(f"Cipher length: {len(cipher_vals)}")
    
    for i in range(len(all_runes) - len(cipher_vals) + 1):
        key = all_runes[i : i+len(cipher_vals)]
        plain = decrypt(cipher_vals, key)
        
        # Check for cribs
        # Need to be efficient
        # Just check if likely sequences appear
        
        # Check specific cribs at specific offsets if known?
        # No, we assume the key could start anywhere.
        # But we know where DECRYPTION is located in the Cipher.
        # Word 14.
        # Let's verify location of Word 14 in cipher_vals.
        # Word 1: 1 Rune. Word 2: 8 runes. ...
        # I should perform the check on the generated plaintext.
        
        # Too many checks. Let's just convert to string and search "DECRYPTION".
        # But wait, my vals_to_eng produces "DE", "NG" etc.
        # So "DECRYPTION" becomes "DECRYPTION".
        
        # Optimize: Check if specific segments match
        pass

    # Better approach:
    # Just iterate through all offsets and check if the decrypted chunk at Word 14 matches DECRYPTION
    
    # Word 14 index:
    # Let's count indices.
    txt = load_runes(target_pg) # reload clearly
    parts = load_runes(target_pg).replace('\n', ' ').replace('•', ' ').split()
    # No, load_runes strips everything.
    
    # Let's re-read carefully to find index of Word 14
    with open(f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{target_pg}\\runes.txt", 'r', encoding='utf-8') as f:
        raw = f.read().replace('\n', ' ').replace('•', ' ')
        
    words = [w for w in raw.split() if w]

    # Find the target word in the list
    target_rune_str = "ᛞᚹᚻᛒᛝᚠᚪᚳᛄᚢ"
    try:
        word14_idx_in_list = words.index(target_rune_str)
        print(f"Found DECRYPTION candidate at word index {word14_idx_in_list}")
    except ValueError:
        print("Could not find target word sequence in word list!")
        return

    # Calculate index of start of word in the flattened list
    curr = 0
    for w in words[:word14_idx_in_list]:
        curr += len(runes_to_vals(w))
    
    idx_14 = curr
    word14_len = len(runes_to_vals(words[word14_idx_in_list]))
    print(f"Target word starts at index {idx_14}, len {word14_len}")
    
    # Target vals for DECRYPTION
    target_vals = crib_vals["DECRYPTION"]
    
    for i in range(len(all_runes) - len(cipher_vals) + 1):
        # Key slice for Word 14
        if i + idx_14 + word14_len > len(all_runes): break
        
        key_slice = all_runes[i + idx_14 : i + idx_14 + word14_len]
        cipher_slice = cipher_vals[idx_14 : idx_14 + word14_len]
        
        decrypted_slice = decrypt(cipher_slice, key_slice)
        
        if decrypted_slice == target_vals:
            print(f"MATCH FOUND at Key Offset {i}!")
            print(f"Key segment: {vals_to_eng(key_slice)}")
            # Print surrounding context
            full_key = all_runes[i : i+len(cipher_vals)]
            full_dec = decrypt(cipher_vals, full_key)
            print(f"Full Decryption: {vals_to_eng(full_dec)}")
            return

    print("No Running Key match found in Corpus Runes.")

if __name__ == "__main__":
    main()

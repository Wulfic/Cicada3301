"""
Page 20 - Deor Refrain and Structure Attack
============================================
"Þæs ofereode, þisses swa mæg" = "That passed away, so can this"
"""

import collections

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def decrypt_vigenere(cipher, key, mode='sub'):
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        else:
            result.append((c + k) % 29)
    return result

def text_to_indices(text):
    return [ENGLISH_TO_IDX.get(c.upper(), 0) for c in text if c.upper() in ENGLISH_TO_IDX]

def main():
    print("="*60)
    print("PAGE 20 - DEOR REFRAIN ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    print(f"Grid: {rows} × {cols} = {len(runes)}")
    
    # The refrain: "Þæs ofereode, þisses swa mæg"
    # In modern English: "That passed away, so can this"
    # In Old English letters (removing special chars): THAES OFEREODE THISSES SWA MAEG
    
    refrain_old = "THAESOFEREODETHISSESSWAMAEG"
    refrain_modern = "THATPASSEDAWAYSOCANTHIS"
    
    print(f"\nRefrain (Old English): {refrain_old}")
    print(f"Refrain (Modern English): {refrain_modern}")
    
    # Convert to indices
    refrain_old_idx = text_to_indices(refrain_old)
    refrain_modern_idx = text_to_indices(refrain_modern)
    
    print(f"Old English indices ({len(refrain_old_idx)}): {refrain_old_idx}")
    print(f"Modern English indices ({len(refrain_modern_idx)}): {refrain_modern_idx}")
    
    # Test each refrain as key
    for name, key in [("Old English", refrain_old_idx), ("Modern English", refrain_modern_idx)]:
        print(f"\n--- Testing {name} refrain ---")
        
        extended_key = key * (len(runes) // len(key) + 1)
        extended_key = extended_key[:len(runes)]
        
        for mode in ['sub', 'add']:
            result = decrypt_vigenere(runes, extended_key, mode)
            ioc = calculate_ioc(result)
            print(f"{mode.upper()}: IoC={ioc:.4f}")
            print(f"  Text: {runes_to_latin(result[:80])}")
    
    # What if the refrain is applied only at refrain positions?
    print("\n" + "="*60)
    print("REFRAIN AT SPECIFIC POSITIONS")
    print("="*60)
    
    # The refrain appears after each strophe in Deor (7 times)
    # What if we apply the refrain only every 29 characters (one per row)?
    
    refrain_key = refrain_old_idx[:29]  # Use first 29 chars of refrain
    if len(refrain_key) < 29:
        refrain_key = refrain_key * (29 // len(refrain_key) + 1)
        refrain_key = refrain_key[:29]
    
    print(f"Refrain key (29 chars): {refrain_key}")
    print(f"As Latin: {runes_to_latin(refrain_key)}")
    
    # Apply as row key
    result = []
    for r in range(rows):
        for c in range(cols):
            result.append((grid[r][c] - refrain_key[c]) % 29)
    
    ioc = calculate_ioc(result)
    print(f"\nRefrain as column key (SUB): IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # Try: The 7 strophes correspond to groups of 4 rows (28/7 = 4)
    print("\n" + "="*60)
    print("STROPHE STRUCTURE: 7 strophes × 4 rows")
    print("="*60)
    
    # Extract each strophe (4 rows)
    for strophe in range(7):
        start_row = strophe * 4
        end_row = start_row + 4
        strophe_runes = []
        for r in range(start_row, end_row):
            strophe_runes.extend(grid[r])
        
        ioc = calculate_ioc(strophe_runes)
        print(f"Strophe {strophe + 1} (rows {start_row}-{end_row-1}): IoC={ioc:.4f}, len={len(strophe_runes)}")
    
    # What if prime-numbered strophes (2, 3, 5, 7) have a different key?
    print("\n--- Prime Strophes (2, 3, 5, 7) ---")
    prime_strophe_nums = [2, 3, 5, 7]  # 1-indexed
    prime_strophe_runes = []
    for s in prime_strophe_nums:
        start_row = (s - 1) * 4
        for r in range(start_row, start_row + 4):
            if r < rows:
                prime_strophe_runes.extend(grid[r])
    
    ioc = calculate_ioc(prime_strophe_runes)
    print(f"Prime strophes combined: IoC={ioc:.4f}, len={len(prime_strophe_runes)}")
    print(f"Text: {runes_to_latin(prime_strophe_runes[:100])}")
    
    # Apply refrain to prime strophes only
    extended_refrain = refrain_old_idx * (len(prime_strophe_runes) // len(refrain_old_idx) + 1)
    extended_refrain = extended_refrain[:len(prime_strophe_runes)]
    
    result = decrypt_vigenere(prime_strophe_runes, extended_refrain, 'sub')
    ioc = calculate_ioc(result)
    print(f"After refrain (SUB): IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:100])}")
    
    # What if we need to interleave strophes?
    print("\n" + "="*60)
    print("INTERLEAVING STROPHES")
    print("="*60)
    
    # Read one row from each strophe in turn
    interleaved = []
    for row_in_strophe in range(4):
        for strophe in range(7):
            r = strophe * 4 + row_in_strophe
            if r < rows:
                interleaved.extend(grid[r])
    
    ioc = calculate_ioc(interleaved)
    print(f"Rows interleaved by strophe: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(interleaved[:100])}")
    
    # Apply refrain
    extended_refrain = refrain_old_idx * (len(interleaved) // len(refrain_old_idx) + 1)
    extended_refrain = extended_refrain[:len(interleaved)]
    
    result = decrypt_vigenere(interleaved, extended_refrain, 'sub')
    ioc = calculate_ioc(result)
    print(f"After refrain: IoC={ioc:.4f}")
    
    # What about reading prime-numbered columns?
    print("\n" + "="*60)
    print("PRIME-NUMBERED COLUMNS ONLY")
    print("="*60)
    
    def is_prime(n):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5)+1, 2):
            if n % i == 0: return False
        return True
    
    prime_cols = [c for c in range(cols) if is_prime(c)]
    print(f"Prime columns: {prime_cols}")  # 2, 3, 5, 7, 11, 13, 17, 19, 23
    
    prime_col_runes = []
    for r in range(rows):
        for c in prime_cols:
            prime_col_runes.append(grid[r][c])
    
    ioc = calculate_ioc(prime_col_runes)
    print(f"Prime columns: IoC={ioc:.4f}, len={len(prime_col_runes)}")
    print(f"Text: {runes_to_latin(prime_col_runes[:80])}")
    
    # Apply refrain
    extended_refrain = refrain_old_idx * (len(prime_col_runes) // len(refrain_old_idx) + 1)
    extended_refrain = extended_refrain[:len(prime_col_runes)]
    
    result = decrypt_vigenere(prime_col_runes, extended_refrain, 'sub')
    ioc = calculate_ioc(result)
    print(f"After refrain: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")

if __name__ == "__main__":
    main()

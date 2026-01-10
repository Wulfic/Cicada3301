"""
Page 20 - Deor Strophe Structure Attack
========================================
The Deor poem has 7 strophes with a repeated refrain.
Maybe the key is derived from prime-numbered strophes (2, 3, 5, 7).

Also exploring: 812 = 28 × 29 = 4 × 7 × 29
- 29 = alphabet size
- 7 = number of strophes in Deor
- 4 = could be related to prime strophes (4 primes <= 7: 2, 3, 5, 7)
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

# Approximate English to rune index
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

def main():
    print("="*60)
    print("PAGE 20 - DEOR STROPHE STRUCTURE ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    
    print(f"Loaded {len(runes)} runes")
    print(f"Grid: 28 × 29 = {28*29}")
    print(f"28 = 4 × 7, where 7 = Deor strophes")
    
    # Load and parse Deor into strophes
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    with open(deor_path, 'r', encoding='utf-8') as f:
        deor_text = f.read()
    
    # Split by the refrain "Þæs ofereode, þisses swa mæg"
    # The Old English section has 7 strophes
    oe_section = deor_text.split("DEOR POEM (MODERN ENGLISH")[0]
    
    # Split by blank lines to get strophes
    strophes_raw = oe_section.strip().split("\n\n")
    
    print(f"\nFound {len(strophes_raw)} raw sections")
    
    # Convert each strophe to indices
    strophes = []
    for i, s in enumerate(strophes_raw):
        s_upper = s.upper()
        indices = [ENGLISH_TO_IDX.get(c, 0) for c in s_upper if c in ENGLISH_TO_IDX]
        strophes.append(indices)
        print(f"  Strophe {i}: {len(indices)} chars, starts: {s[:30]}...")
    
    # Use prime-numbered strophes (1-indexed: 2, 3, 5, 7 → 0-indexed: 1, 2, 4, 6)
    prime_strophe_indices = [1, 2, 4, 6]  # 0-indexed
    
    print(f"\n--- Testing Prime Strophes ---")
    
    prime_key = []
    for idx in prime_strophe_indices:
        if idx < len(strophes):
            prime_key.extend(strophes[idx])
            print(f"  Adding strophe {idx+1} (0-idx={idx}): {len(strophes[idx])} chars")
    
    print(f"Total prime strophe key length: {len(prime_key)}")
    
    # Extend key
    extended_key = prime_key * (len(runes) // len(prime_key) + 1)
    extended_key = extended_key[:len(runes)]
    
    # Decrypt
    result = decrypt_vigenere(runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"\nPrime strophes (2,3,5,7) SUB: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:200])}")
    
    result = decrypt_vigenere(runes, extended_key, 'add')
    ioc = calculate_ioc(result)
    print(f"Prime strophes (2,3,5,7) ADD: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:200])}")
    
    # Try the REFRAIN specifically
    print(f"\n--- Testing Refrain ---")
    refrain_oe = "THAESOFEREODETHISTHESSOWAMAEG"  # Approximation of "Þæs ofereode, þisses swa mæg"
    refrain_key = [ENGLISH_TO_IDX.get(c, 0) for c in refrain_oe]
    
    print(f"Refrain: {refrain_oe}")
    print(f"Refrain length: {len(refrain_key)}")
    
    extended_key = refrain_key * (len(runes) // len(refrain_key) + 1)
    extended_key = extended_key[:len(runes)]
    
    result = decrypt_vigenere(runes, extended_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Refrain SUB: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:200])}")
    
    # Try reading by strophe structure
    print(f"\n--- Reading Grid by 7-Row Blocks (Strophe Pattern) ---")
    
    rows, cols = 28, 29
    grid = [runes[r*cols:(r+1)*cols] for r in range(rows)]
    
    # 28 rows = 4 blocks of 7 rows
    # Read each 7-row block differently?
    
    block_size = 7
    num_blocks = 4
    
    # Try reading blocks in prime order
    block_order = [1, 0, 2, 3]  # Prime strophe indices mod 4
    
    reordered = []
    for block_idx in block_order:
        start_row = block_idx * block_size
        for r in range(start_row, min(start_row + block_size, rows)):
            reordered.extend(grid[r])
    
    ioc = calculate_ioc(reordered)
    print(f"Blocks in order [1,0,2,3]: IoC={ioc:.4f}")
    
    # Apply Deor to reordered
    full_deor = []
    for s in strophes:
        full_deor.extend(s)
    
    extended_key = full_deor * (len(reordered) // len(full_deor) + 1)
    extended_key = extended_key[:len(reordered)]
    
    result = decrypt_vigenere(reordered, extended_key, 'sub')
    ioc2 = calculate_ioc(result)
    print(f"After full Deor SUB: IoC={ioc2:.4f}")
    print(f"Text: {runes_to_latin(result[:150])}")
    
    # Try a 7-column pattern
    print(f"\n--- Reading Grid by 7-Column Blocks ---")
    
    # Read columns in groups of 7
    for col_start in [0, 7, 14, 21]:
        col_subset = []
        for r in range(rows):
            for c in range(col_start, min(col_start + 7, cols)):
                col_subset.append(grid[r][c])
        ioc = calculate_ioc(col_subset)
        print(f"Columns {col_start}-{col_start+6}: IoC={ioc:.4f}")
    
    # Try each individual row as key
    print(f"\n--- Testing Each Grid Row as Key ---")
    
    best_ioc = 0
    best_row = -1
    
    for key_row in range(rows):
        row_key = grid[key_row]
        extended_key = row_key * (len(runes) // len(row_key) + 1)
        extended_key = extended_key[:len(runes)]
        
        result = decrypt_vigenere(runes, extended_key, 'sub')
        ioc = calculate_ioc(result)
        
        if ioc > best_ioc:
            best_ioc = ioc
            best_row = key_row
    
    print(f"Best row key: row {best_row} with IoC={best_ioc:.4f}")
    
    # Show best
    row_key = grid[best_row]
    extended_key = row_key * (len(runes) // len(row_key) + 1)
    extended_key = extended_key[:len(runes)]
    result = decrypt_vigenere(runes, extended_key, 'sub')
    print(f"Text: {runes_to_latin(result[:150])}")
    
    # Try running key from sorted rune values
    print(f"\n--- Running Key from Sorted Runes ---")
    
    # Sort positions by rune value
    indexed_runes = [(runes[i], i) for i in range(len(runes))]
    indexed_runes.sort()
    
    sorted_order = [idx for _, idx in indexed_runes]
    
    # Read in sorted order
    reordered = [runes[i] for i in sorted_order]
    ioc = calculate_ioc(reordered)
    print(f"Read in sorted order: IoC={ioc:.4f}")
    
    # Apply Deor
    result = decrypt_vigenere(reordered, extended_key, 'sub')
    ioc2 = calculate_ioc(result)
    print(f"After Deor: IoC={ioc2:.4f}")
    print(f"Text: {runes_to_latin(result[:150])}")

if __name__ == "__main__":
    main()

"""
Page 1 - Two-layer attack: XOR-71 + Transposition

Based on discoveries:
1. XOR with key length 71 produces strong English signal (score 801.50)
2. Output is fragmented, suggesting a transposition layer
3. Columnar transpose width=3 showed improvement

This script systematically tests transposition methods on the XOR-71 output.
"""

import os
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# Optimized key from XOR-71 attack
OPTIMIZED_KEY_71 = [16, 4, 13, 27, 4, 15, 25, 27, 16, 8, 5, 10, 22, 0, 1, 6, 24, 9, 15, 10, 0, 0, 6, 3, 10, 22, 14, 5, 16, 3, 15, 20, 27, 1, 4, 24, 0, 20, 19, 21, 4, 21, 14, 14, 6, 0, 10, 17, 24, 17, 3, 8, 17, 16, 6, 2, 12, 25, 24, 13, 7, 18, 21, 15, 19, 10, 6, 10, 27, 3, 5]

def load_page1():
    """Load Page 1."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_indices = [RUNE_TO_INDEX[c] for c in segments[0] if c in RUNE_TO_INDEX]
    page1_raw = segments[0]
    return page1_indices, page1_raw

def decrypt_xor(cipher_indices, key_indices):
    """XOR decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c ^ k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert to text."""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """Enhanced English scoring."""
    text_upper = text.upper()
    
    # Common words
    common_words = {
        "THE": 5.0, "OF": 4.0, "AND": 4.0, "TO": 3.0, "IN": 3.0,
        "IS": 2.5, "THAT": 3.0, "IT": 2.0, "FOR": 2.5, "AS": 2.0,
        "WITH": 3.0, "WAS": 2.5, "ON": 2.0, "BE": 2.0, "AT": 2.0,
        "BY": 2.0, "THIS": 2.5, "FROM": 2.5, "OR": 2.0, "AN": 2.0,
        "ARE": 2.0, "WHICH": 2.5, "ONE": 2.5, "ALL": 2.5, "THEIR": 2.5,
        "WITHIN": 3.0, "DIVINE": 3.5, "EMERGE": 3.5, "INSTAR": 4.0,
        "CIRCUMFERENCE": 5.0, "TRUTH": 3.0, "WISDOM": 3.0
    }
    
    score = 0.0
    for word, weight in common_words.items():
        # Count whole-word occurrences
        import re
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = len(re.findall(pattern, text_upper))
        score += matches * weight * len(word)
    
    # Common bigrams
    bigrams = ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND"]
    for bg in bigrams:
        score += text_upper.count(bg) * 1.5
    
    # Penalize excessive single-letter repetition
    for letter in "ETAOINS":
        freq = text_upper.count(letter) / max(len(text_upper), 1)
        if freq > 0.15:  # More than 15%
            score *= 0.7
    
    return score

def columnar_transpose(indices, width, direction="rows_to_cols"):
    """
    Apply columnar transposition.
    
    direction="rows_to_cols": write by rows, read by columns
    direction="cols_to_rows": write by columns, read by rows (inverse)
    """
    n = len(indices)
    
    if direction == "rows_to_cols":
        # Write by rows, read by columns
        cols = [[] for _ in range(width)]
        for i, val in enumerate(indices):
            cols[i % width].append(val)
        result = []
        for col in cols:
            result.extend(col)
        return result
    
    elif direction == "cols_to_rows":
        # Write by columns, read by rows (inverse of above)
        height = (n + width - 1) // width
        grid = [[None] * width for _ in range(height)]
        
        idx = 0
        for col in range(width):
            for row in range(height):
                if idx < n:
                    grid[row][col] = indices[idx]
                    idx += 1
        
        result = []
        for row in grid:
            result.extend([x for x in row if x is not None])
        return result
    
    return indices

def rail_fence(indices, rails):
    """Apply rail fence cipher (decode)."""
    n = len(indices)
    if rails <= 1:
        return indices
    
    # Calculate rail lengths
    cycle = 2 * (rails - 1)
    rail_lengths = [0] * rails
    for i in range(n):
        rail = i % cycle
        if rail >= rails:
            rail = cycle - rail
        rail_lengths[rail] += 1
    
    # Distribute indices into rails
    rail_data = []
    idx = 0
    for length in rail_lengths:
        rail_data.append(indices[idx:idx+length])
        idx += length
    
    # Read in zigzag order
    result = []
    rail_pos = [0] * rails
    for i in range(n):
        rail = i % cycle
        if rail >= rails:
            rail = cycle - rail
        result.append(rail_data[rail][rail_pos[rail]])
        rail_pos[rail] += 1
    
    return result

def reverse_sequence(indices):
    """Simple reversal."""
    return list(reversed(indices))

def test_transpositions(base_indices):
    """Test various transposition methods."""
    results = []
    
    print("Testing transpositions...")
    
    # Test columnar (write rows, read cols)
    for width in [2, 3, 4, 5, 6, 7, 127]:
        transposed = columnar_transpose(base_indices, width, "rows_to_cols")
        text = indices_to_text(transposed)
        score = score_english(text)
        results.append(("columnar_r2c", width, score, text))
    
    # Test columnar (write cols, read rows - inverse)
    for width in [2, 3, 4, 5, 6, 7, 127]:
        transposed = columnar_transpose(base_indices, width, "cols_to_rows")
        text = indices_to_text(transposed)
        score = score_english(text)
        results.append(("columnar_c2r", width, score, text))
    
    # Test rail fence
    for rails in [2, 3, 4, 5, 7]:
        transposed = rail_fence(base_indices, rails)
        text = indices_to_text(transposed)
        score = score_english(text)
        results.append(("rail_fence", rails, score, text))
    
    # Test reversal
    reversed_indices = reverse_sequence(base_indices)
    text = indices_to_text(reversed_indices)
    score = score_english(text)
    results.append(("reverse", 0, score, text))
    
    # No transposition (baseline)
    text_base = indices_to_text(base_indices)
    score_base = score_english(text_base)
    results.append(("none", 0, score_base, text_base))
    
    return results

def main():
    print("="*80)
    print("Page 1 - Two-Layer Attack: XOR-71 + Transposition")
    print("="*80)
    
    cipher_indices, raw_text = load_page1()
    
    # Step 1: XOR-71 decrypt
    print("\n--- Step 1: XOR-71 Decryption ---")
    xor_output = decrypt_xor(cipher_indices, OPTIMIZED_KEY_71)
    base_text = indices_to_text(xor_output)
    base_score = score_english(base_text)
    
    print(f"XOR-71 output score: {base_score:.2f}")
    print(f"Preview: {base_text[:150]}")
    
    # Step 2: Test transpositions
    print("\n--- Step 2: Testing Transpositions ---")
    results = test_transpositions(xor_output)
    
    # Sort by score
    results.sort(key=lambda x: x[2], reverse=True)
    
    print("\n" + "="*80)
    print("TOP 10 RESULTS")
    print("="*80)
    
    for i, (method, param, score, text) in enumerate(results[:10]):
        print(f"\n--- Rank {i+1}: {method} (param={param}), score={score:.2f} ---")
        print(text[:200])
    
    # Save top result
    best_method, best_param, best_score, best_text = results[0]
    
    output_path = "tools/PAGE1_TWO_LAYER_BEST.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("Page 1 - Best Two-Layer Result\n")
        f.write("="*80 + "\n\n")
        f.write(f"Layer 1: XOR with key length 71\n")
        f.write(f"Layer 2: {best_method} (param={best_param})\n")
        f.write(f"Score: {best_score:.2f}\n\n")
        f.write("Full plaintext:\n")
        f.write(best_text + "\n")
    
    print(f"\n\nBest result saved to: {output_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test columnar transposition on Page 1 SUB-71 output
Maybe the plaintext needs to be read in columns, not rows
"""

import os
from pathlib import Path
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page1():
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_runes = segments[0]
    page1_indices = [RUNE_TO_INDEX[c] for c in page1_runes if c in RUNE_TO_INDEX]
    
    return page1_indices

def decrypt_sub(cipher_indices, key_indices):
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def indices_to_text(indices):
    return "".join(LETTERS[idx] for idx in indices)

def score_english(text):
    text = text.upper()
    common_words = ['THE', 'AND', 'OF', 'TO', 'IN', 'A', 'IS', 'THAT', 'FOR', 'IT', 'WITH', 'AS', 'WAS', 'ON', 'ARE', 'FROM', 'OR', 'BY', 'THIS', 'WHICH', 'WISDOM', 'DIVINE', 'TRUTH']
    score = sum(text.count(word) * len(word) * 10 for word in common_words)
    
    # Bigrams
    common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
    score += sum(text.count(bg) * 5 for bg in common_bigrams)
    
    return score

def test_columnar_transposition(plaintext_indices, cols):
    """Read text in columnar order"""
    # Fill in a grid
    rows = (len(plaintext_indices) + cols - 1) // cols
    grid = []
    idx = 0
    
    for r in range(rows):
        row = []
        for c in range(cols):
            if idx < len(plaintext_indices):
                row.append(plaintext_indices[idx])
                idx += 1
            else:
                row.append(None)
        grid.append(row)
    
    # Read by columns
    result = []
    for c in range(cols):
        for r in range(rows):
            if grid[r][c] is not None:
                result.append(grid[r][c])
    
    return result

def test_rail_fence(plaintext_indices, rails):
    """Test rail fence cipher"""
    # Create rails
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for idx in plaintext_indices:
        fence[rail].append(idx)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    # Read off rails
    result = []
    for rail in fence:
        result.extend(rail)
    
    return result

BEST_KEY_71 = [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7]

def main():
    print("=" * 80)
    print("PAGE 1 - TESTING TRANSPOSITION CIPHERS")
    print("=" * 80)
    
    cipher_indices = load_page1()
    plaintext_indices = decrypt_sub(cipher_indices, BEST_KEY_71)
    plaintext_text = indices_to_text(plaintext_indices)
    
    print(f"\nOriginal SUB-71 output (length {len(plaintext_text)}):")
    print(plaintext_text[:100] + "...")
    
    base_score = score_english(plaintext_text)
    print(f"\nBase score: {base_score}")
    
    # Test columnar transposition
    print("\n" + "=" * 80)
    print("COLUMNAR TRANSPOSITION (reading by columns)")
    print("=" * 80)
    
    results = []
    
    for cols in range(2, 30):
        transposed = test_columnar_transposition(plaintext_indices, cols)
        text = indices_to_text(transposed)
        score = score_english(text)
        
        results.append({
            'type': 'columnar',
            'cols': cols,
            'score': score,
            'text': text
        })
    
    # Sort by score
    results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)
    
    print(f"\nTop 15 column counts by score:")
    print(f"{'Rank':<6} {'Cols':<6} {'Score':<10} {'Preview'}")
    print("-" * 80)
    
    for i, r in enumerate(results_sorted[:15], 1):
        preview = r['text'][:60]
        print(f"{i:<6} {r['cols']:<6} {r['score']:<10} {preview}")
    
    # Test rail fence
    print("\n" + "=" * 80)
    print("RAIL FENCE CIPHER")
    print("=" * 80)
    
    rail_results = []
    
    for rails in range(2, 20):
        transposed = test_rail_fence(plaintext_indices, rails)
        text = indices_to_text(transposed)
        score = score_english(text)
        
        rail_results.append({
            'rails': rails,
            'score': score,
            'text': text
        })
    
    rail_results_sorted = sorted(rail_results, key=lambda x: x['score'], reverse=True)
    
    print(f"\nTop 10 rail counts by score:")
    print(f"{'Rank':<6} {'Rails':<6} {'Score':<10} {'Preview'}")
    print("-" * 80)
    
    for i, r in enumerate(rail_results_sorted[:10], 1):
        preview = r['text'][:60]
        print(f"{i:<6} {r['rails']:<6} {r['score']:<10} {preview}")
    
    # Find best overall
    all_results = [
        {'type': 'original', 'params': 'none', 'score': base_score, 'text': plaintext_text}
    ] + [{'type': 'columnar', 'params': f'{r["cols"]} cols', 'score': r['score'], 'text': r['text']} for r in results_sorted[:5]] + \
        [{'type': 'rail fence', 'params': f'{r["rails"]} rails', 'score': r['score'], 'text': r['text']} for r in rail_results_sorted[:5]]
    
    best = max(all_results, key=lambda x: x['score'])
    
    print("\n" + "=" * 80)
    print("BEST RESULT")
    print("=" * 80)
    print(f"\nType: {best['type']}")
    print(f"Parameters: {best['params']}")
    print(f"Score: {best['score']} (vs base {base_score})")
    
    if best['score'] > base_score * 1.2:
        print("\n✓ SIGNIFICANT IMPROVEMENT - transposition may be correct!")
    else:
        print("\n⚠ No significant improvement from transposition")
    
    print(f"\nFull text:")
    print(best['text'])
    
    # Test specific width (71 = key length)
    print("\n" + "=" * 80)
    print("TESTING KEY-LENGTH-BASED ARRANGEMENTS")
    print("=" * 80)
    
    for width in [71, 127, 254]:  # Key length, double key, full length
        if width <= len(plaintext_indices):
            transposed = test_columnar_transposition(plaintext_indices, width)
            text = indices_to_text(transposed)
            score = score_english(text)
            print(f"\n{width} columns:")
            print(f"  Score: {score}")
            print(f"  Preview: {text[:80]}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    if best['score'] > base_score * 1.5:
        print(f"\n✓ Found better arrangement: {best['type']} with {best['params']}")
        print("This suggests SUB-71 needs an additional transposition step")
    else:
        print("\n⚠ No transposition significantly improved readability")
        print("Possible explanations:")
        print("  1. The SUB-71 output IS the final plaintext (just unusual format)")
        print("  2. Different type of transformation needed (not simple transposition)")
        print("  3. Key length or operation still not quite right")
        print("  4. Plaintext is intentionally fragmented (word list, cipher-speak, etc.)")

if __name__ == '__main__':
    main()

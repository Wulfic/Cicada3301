#!/usr/bin/env python3
"""
PAGE 55 ANALYSIS - Understanding where the decryption breaks

Let's analyze exactly what's happening at each position.
"""

from pathlib import Path

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {l: i for i, l in enumerate(LETTERS)}

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

def phi(n):
    return n - 1 if n >= 2 else 0

def text_to_indices(text):
    """Convert text to Gematria indices."""
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[two])
                i += 2
                continue
        one = text[i]
        if one in LETTER_TO_IDX:
            result.append(LETTER_TO_IDX[one])
        i += 1
    return result

def load_page(page_num):
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("PAGE 55 POSITION-BY-POSITION ANALYSIS")
    print("=" * 70)
    
    rune_text = load_page(55)
    
    # Extract just the runes (no separators)
    cipher = [(RUNE_MAP[c], c) for c in rune_text if c in RUNE_MAP]
    
    # Expected plaintext
    expected = "ANENDWITHINTHEDEEPWEBTHEREEXISTSAPAGETHATHHASHESTOITISTHEDUTOFEUERYPILGRIMTOSEECOUTTHISPAGE"
    # Actually let me use proper Gematria spelling
    expected = "ANENDWITHINTHEDEEPWEBTHEREEXISTSAPAGETHATHASHESTOITISTHEDUTYFOFEURYPILGRIMTOSEECOUTTHISPAGE"
    
    # Hmm, let me be more careful. Let me derive it word by word:
    words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
             "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
             "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected_indices = []
    for word in words:
        expected_indices.extend(text_to_indices(word))
    
    print(f"Cipher length: {len(cipher)}")
    print(f"Expected indices length: {len(expected_indices)}")
    
    print("\nPosition-by-position analysis:")
    print("-" * 80)
    print(f"{'Pos':>4} {'Rune':>4} {'CIdx':>4} {'Key':>4} {'Plain':>6} {'Exp':>6} {'Match':>5}")
    print("-" * 80)
    
    working_count = 0
    for i, (c_idx, rune) in enumerate(cipher):
        key = phi(PRIMES[i % len(PRIMES)]) % 29
        plain_idx = (c_idx - key) % 29
        plain_letter = LETTERS[plain_idx]
        
        if i < len(expected_indices):
            exp_idx = expected_indices[i]
            exp_letter = LETTERS[exp_idx]
            match = "✓" if plain_idx == exp_idx else "✗"
            if plain_idx == exp_idx:
                working_count += 1
        else:
            exp_letter = "?"
            match = "?"
        
        # Show rune character
        rune_char = rune
        
        if i < 50 or match == "✗":  # Show first 50 and all mismatches
            print(f"{i:>4} {rune_char:>4} {c_idx:>4} {key:>4} {plain_letter:>6} {exp_letter:>6} {match:>5}")
    
    print("-" * 80)
    print(f"Working positions: {working_count}/{len(cipher)}")
    
    # Find first mismatch
    print("\n--- First mismatch analysis ---")
    for i, (c_idx, rune) in enumerate(cipher):
        key = phi(PRIMES[i % len(PRIMES)]) % 29
        plain_idx = (c_idx - key) % 29
        
        if i < len(expected_indices):
            exp_idx = expected_indices[i]
            if plain_idx != exp_idx:
                print(f"First mismatch at position {i}:")
                print(f"  Rune: {rune} (index {c_idx})")
                print(f"  Key used: {key} (φ({PRIMES[i]})%29)")
                print(f"  Got: {LETTERS[plain_idx]} (index {plain_idx})")
                print(f"  Expected: {LETTERS[exp_idx]} (index {exp_idx})")
                print(f"  Required key for expected: {(c_idx - exp_idx) % 29}")
                break
    
    # What word is position 35?
    print("\n--- Word boundary analysis ---")
    cumlen = 0
    for word in words:
        word_len = len(text_to_indices(word))
        print(f"  '{word}': positions {cumlen}-{cumlen + word_len - 1}")
        cumlen += word_len
        if cumlen > 40:
            break

if __name__ == '__main__':
    main()

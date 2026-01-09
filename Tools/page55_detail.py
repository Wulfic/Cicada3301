#!/usr/bin/env python3
"""
PAGE 55 - Check positions 50-60 in detail
"""

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
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
          223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
          293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379]

def phi(n):
    return n - 1 if n >= 2 else 0

def text_to_indices(text):
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

def main():
    from pathlib import Path
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / "page_55"
    with open(page_dir / "runes.txt", 'r', encoding='utf-8') as f:
        rune_text = f.read()
    
    cipher = [(RUNE_MAP[c], c) for c in rune_text if c in RUNE_MAP]
    
    expected_words = ["AN", "END", "WITHIN", "THE", "DEEP", "WEB", 
                     "THERE", "EXISTS", "A", "PAGE", "THAT", "HASHES", "TO",
                     "IT", "IS", "THE", "DUTY", "OF", "EUERY", "PILGRIM", 
                     "TO", "SEEC", "OUT", "THIS", "PAGE"]
    
    expected = []
    word_boundaries = [0]
    for word in expected_words:
        indices = text_to_indices(word)
        expected.extend(indices)
        word_boundaries.append(len(expected))
    
    print("POSITIONS 45-70 IN DETAIL")
    print("=" * 100)
    
    # Show word boundaries
    print("\nWord boundaries (cumulative positions):")
    for i, word in enumerate(expected_words):
        print(f"  {word}: {word_boundaries[i]}-{word_boundaries[i+1]-1}")
    
    print("\n" + "=" * 100)
    print(f"{'Pos':>4} {'Rune':>5} {'CIdx':>4} {'Prime':>6} {'Key':>4} {'Got':>6} {'Exp':>6} {'Match':>5} {'Word':<12}")
    print("-" * 100)
    
    for i in range(45, min(70, len(cipher))):
        c_idx, rune = cipher[i]
        prime = PRIMES[i % len(PRIMES)]
        k = phi(prime) % 29
        p = (c_idx - k) % 29
        
        exp = expected[i] if i < len(expected) else -1
        match = "✓" if p == exp else "✗"
        exp_str = LETTERS[exp] if exp >= 0 else "?"
        
        # Find which word this position belongs to
        word = ""
        for wi, (start, end) in enumerate(zip(word_boundaries[:-1], word_boundaries[1:])):
            if start <= i < end:
                word = expected_words[wi]
                break
        
        is_f_rune = "F!" if rune == 'ᚠ' else ""
        print(f"{i:>4} {rune:>5} {c_idx:>4} {prime:>6} {k:>4} {LETTERS[p]:>6} {exp_str:>6} {match:>5} {word:<12} {is_f_rune}")
    
    # Show the issue clearly
    print("\n" + "=" * 100)
    print("KEY OBSERVATION:")
    print("Position 56 has cipher=0 (F rune), expected=F")
    print("But φ(269)%29 = 7, so we get (0-7)%29 = 22 = OE")
    print("\nIf position 56 is a LITERAL F (not encrypted):")
    print("  - Output F directly")
    print("  - DON'T increment prime counter")
    print("  - Position 57 uses prime[56] instead of prime[57]")
    
    # Test the F-literal theory
    print("\n" + "=" * 100)
    print("TESTING F-LITERAL THEORY:")
    print("-" * 100)
    
    # Positions where cipher is F rune (index 0) AND expected is F (index 0)
    literal_f_positions = []
    for i in range(len(cipher)):
        c_idx, rune = cipher[i]
        exp = expected[i] if i < len(expected) else -1
        if c_idx == 0 and exp == 0:  # Both cipher and expected are F
            literal_f_positions.append(i)
    
    print(f"Positions where cipher=F AND expected=F: {literal_f_positions}")
    
    # Apply F-literal decryption
    prime_idx = 0
    result = []
    
    for i in range(len(cipher)):
        c_idx, rune = cipher[i]
        
        if i in literal_f_positions:
            # This is a literal F
            result.append(('F', 'literal'))
            # DON'T increment prime_idx
        else:
            # Normal decryption
            k = phi(PRIMES[prime_idx % len(PRIMES)]) % 29
            p = (c_idx - k) % 29
            result.append((LETTERS[p], f'p[{prime_idx}]'))
            prime_idx += 1
    
    print(f"\nAfter F-literal adjustment (prime counter only increments for non-literal-F):")
    print("-" * 100)
    
    correct = 0
    for i in range(45, min(70, len(result))):
        got, method = result[i]
        exp = expected[i] if i < len(expected) else -1
        exp_str = LETTERS[exp] if exp >= 0 else "?"
        match = "✓" if (got == exp_str or (got == 'F' and exp == 0)) else "✗"
        if got == exp_str or (got == 'F' and exp == 0):
            correct += 1
        print(f"  {i}: got={got:>4} ({method:<10}), expected={exp_str:>4} {match}")
    
    # Full decryption
    print("\n" + "=" * 100)
    print("FULL F-LITERAL DECRYPTION:")
    print("-" * 100)
    
    decrypted = ''.join(r[0] for r in result)
    # Format with word breaks from original
    formatted = []
    idx = 0
    for c in rune_text:
        if c in RUNE_MAP:
            if idx < len(result):
                formatted.append(result[idx][0])
            idx += 1
        elif c == '-':
            formatted.append(' ')
        elif c == '.':
            formatted.append('. ')
        elif c == '\n':
            formatted.append('\n')
    
    print(''.join(formatted))

if __name__ == '__main__':
    main()

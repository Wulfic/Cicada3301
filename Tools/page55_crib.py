#!/usr/bin/env python3
"""
PAGE 55 CRIB ATTACK

We know the expected plaintext for the broken part:
"IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE"

Let's use this to find the correct key!
"""

from pathlib import Path

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {}
for i, l in enumerate(LETTERS):
    LETTER_TO_IDX[l] = i

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]

def text_to_indices(text):
    """Convert plaintext to Gematria indices."""
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Check for two-letter combinations first
        if i < len(text) - 1:
            two = text[i:i+2]
            if two in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[two])
                i += 2
                continue
        # Single letter
        one = text[i]
        if one in LETTER_TO_IDX:
            result.append(LETTER_TO_IDX[one])
        i += 1
    return result

def load_page_55():
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / "page_55"
    runes_file = page_dir / "runes.txt"
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        rune_text = f.read()
    
    return rune_text

def main():
    print("PAGE 55 CRIB ATTACK")
    print("=" * 70)
    
    rune_text = load_page_55()
    
    # Parse into sentences (separated by .)
    sentences = []
    current = []
    for c in rune_text:
        if c in RUNE_MAP:
            current.append(RUNE_MAP[c])
        elif c == '.':
            if current:
                sentences.append(current)
                current = []
    if current:
        sentences.append(current)
    
    print(f"Number of sentences: {len(sentences)}")
    for i, s in enumerate(sentences):
        print(f"  Sentence {i}: {len(s)} runes")
    
    # The working part: "AN END. WITHIN THE DEEP WEB. THERE EXISTS A PAGE THAT HASHES TO."
    # = sentences 0, 1, 2 = 45 total runes
    working = sentences[0] + sentences[1] + sentences[2]
    
    # The broken part: "IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE"
    broken = sentences[3] + sentences[4] if len(sentences) > 4 else sentences[3]
    
    print(f"\nWorking part: {len(working)} runes (sentences 0-2)")
    print(f"Broken part: {len(broken)} runes (sentences 3+)")
    
    # Expected plaintext for broken part
    # Note: Need to handle word boundaries from runes
    # Let's look at the structure
    print("\n--- Analyzing broken sentences ---")
    
    # Parse with word boundaries for sentence 3+
    sentence_3_4 = []
    in_broken = False
    sentence_idx = 0
    word = []
    
    for c in rune_text:
        if c == '.':
            if word:
                sentence_3_4.append(('word', word))
                word = []
            sentence_3_4.append(('dot', None))
            sentence_idx += 1
            if sentence_idx >= 3:
                in_broken = True
        elif c == '-':
            if word:
                sentence_3_4.append(('word', word))
                word = []
            if in_broken:
                sentence_3_4.append(('dash', None))
        elif c in RUNE_MAP:
            if in_broken:
                word.append(RUNE_MAP[c])
    
    if word:
        sentence_3_4.append(('word', word))
    
    # Filter to just the broken part
    broken_struct = [x for x in sentence_3_4 if x[0] == 'word' or (x[0] == 'dash')]
    
    print("Broken part structure:")
    broken_words = []
    for t, v in broken_struct:
        if t == 'word':
            broken_words.append(v)
            print(f"  Word: {len(v)} chars - {v}")
    
    # Expected plaintext words
    expected_words = ["IT", "IS", "THE", "DUTY", "OF", "EVERY", "PILGRIM", "TO", "SEEK", "OUT", "THIS", "PAGE"]
    expected_indices = [text_to_indices(w) for w in expected_words]
    
    print("\nExpected words (indices):")
    for w, idx in zip(expected_words, expected_indices):
        print(f"  {w}: {idx}")
    
    # Calculate required key for each word
    print("\n--- CRIB ATTACK: Finding required key values ---")
    
    if len(broken_words) >= len(expected_indices):
        for wi, (cipher_word, expected_word, expected_idx) in enumerate(zip(broken_words, expected_words, expected_indices)):
            print(f"\nWord '{expected_word}':")
            if len(cipher_word) != len(expected_idx):
                print(f"  Length mismatch: cipher={len(cipher_word)}, expected={len(expected_idx)}")
                continue
            
            keys = []
            for i, (c, p) in enumerate(zip(cipher_word, expected_idx)):
                k = (c - p) % 29
                keys.append(k)
            print(f"  Required keys: {keys}")
            
            # Check if keys match phi(primes) pattern with some offset
            for offset in range(200):
                matches = True
                for ki, k in enumerate(keys):
                    expected_k = (PRIMES[(offset + ki) % len(PRIMES)] - 1) % 29
                    if expected_k != k:
                        matches = False
                        break
                if matches:
                    print(f"  ✓ Matches φ(primes) starting at index {offset} (prime={PRIMES[offset]})")
                    break
    
    # Also try global position approach
    print("\n--- Testing: What if key resets at position 45? ---")
    cipher_all = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    broken_cipher = cipher_all[45:]
    
    # Expected full broken text
    expected_broken = "ITISTHEDUTYPFEOERYPILGRIMTPSEEKPUTTHISPAGE"  # Best guess, treating OF as P
    # Wait, need proper conversion
    expected_text = "IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE"
    expected_flat = text_to_indices(expected_text.replace(" ", ""))
    
    print(f"Broken cipher length: {len(broken_cipher)}")
    print(f"Expected plain length: {len(expected_flat)}")
    
    if len(broken_cipher) == len(expected_flat):
        required_keys = [(c - p) % 29 for c, p in zip(broken_cipher, expected_flat)]
        print(f"Required key sequence: {required_keys[:20]}...")
        
        # Check patterns
        print("\nPattern analysis:")
        # Check if it's phi(primes) with different start
        for start in range(100):
            phi_keys = [(PRIMES[(start + i) % len(PRIMES)] - 1) % 29 for i in range(len(required_keys))]
            if phi_keys == required_keys:
                print(f"  ✓ Matches φ(primes) starting at index {start}")
                break
            
        # Check if it's constant offset
        diffs = [required_keys[i+1] - required_keys[i] for i in range(len(required_keys)-1)]
        if len(set(diffs)) == 1:
            print(f"  Constant difference: {diffs[0]}")
    else:
        print(f"  Length mismatch - adjusting expected text")
        
        # The issue might be that the expected text isn't quite right
        # Let me analyze what's actually there
        print(f"\nBroken cipher first 10: {broken_cipher[:10]}")
        
        # If key resets to position 0:
        plain_reset_0 = [(c - (PRIMES[i % len(PRIMES)] - 1)) % 29 for i, c in enumerate(broken_cipher)]
        text_reset_0 = ''.join(LETTERS[p] for p in plain_reset_0)
        print(f"If key resets to prime[0]: {text_reset_0}")

if __name__ == '__main__':
    main()

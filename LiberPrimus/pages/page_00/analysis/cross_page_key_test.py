#!/usr/bin/env python3
"""
Cross-Page Key Relationship Test
=================================
Test if the plaintext from one page can be used as a key for another.
Theory: The pages might be related - decrypted Page N is key for Page N+1.
"""

# First layer outputs as indices (not text)
# We need to convert back to indices to use as keys

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                   'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                   'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Reverse mapping (simplified for single letters)
LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19,
    'L': 20, 'D': 23, 'A': 24, 'Y': 26
}

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9,
    'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18,
    'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# First layer plaintext (as strings)
PAGE0_PLAIN = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

PAGE1_PLAIN = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTOOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

def text_to_indices(text):
    """Convert text to indices using simple mapping."""
    indices = []
    i = 0
    while i < len(text):
        # Check for multi-char patterns
        if text[i:i+2] == 'TH':
            indices.append(2)  # TH = index 2
            i += 2
        elif text[i:i+2] == 'NG':
            indices.append(21)  # NG = index 21
            i += 2
        elif text[i:i+2] == 'OE':
            indices.append(22)  # OE = index 22
            i += 2
        elif text[i:i+2] == 'AE':
            indices.append(25)  # AE = index 25
            i += 2
        elif text[i:i+2] == 'IA':
            indices.append(27)  # IA = index 27
            i += 2
        elif text[i:i+2] == 'EA':
            indices.append(28)  # EA = index 28
            i += 2
        elif text[i:i+2] == 'EO':
            indices.append(12)  # EO = index 12
            i += 2
        elif text[i:i+3] == 'C/K':
            indices.append(5)  # C/K = index 5
            i += 3
        elif text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
            i += 1
        else:
            i += 1  # Skip unknown
    return indices

def load_runes(filepath):
    """Load runes from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [RUNE_TO_INDEX[c] for c in text if c in RUNE_TO_INDEX]

def sub_decrypt(cipher, key):
    """SUB operation: plaintext[i] = (cipher[i] - key[i mod len(key)]) mod 29"""
    return [(cipher[i] - key[i % len(key)]) % 29 for i in range(len(cipher))]

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(INDEX_TO_LETTER[i] for i in indices)

def score_text(text):
    """Simple scoring based on common patterns."""
    score = 0
    score += text.count('THE') * 3
    score += text.count('AND') * 2
    score += text.count('TH') * 1
    score += text.count('NG') * 1
    score += text.count('ING') * 2
    score += text.count('ER') * 1
    score += text.count('ES') * 1
    return score

def main():
    print("=" * 60)
    print("CROSS-PAGE KEY RELATIONSHIP TEST")
    print("=" * 60)
    
    # Load cipher pages
    base_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    
    pages = {}
    for i in range(5):
        path = f"{base_path}/page_{i:02d}/runes.txt"
        pages[i] = load_runes(path)
        print(f"Page {i}: {len(pages[i])} runes")
    
    # Convert first-layer plaintext to indices
    print("\n" + "-" * 60)
    print("Converting first-layer plaintext to indices...")
    print("-" * 60)
    
    p0_indices = text_to_indices(PAGE0_PLAIN)
    p1_indices = text_to_indices(PAGE1_PLAIN)
    
    print(f"Page 0 plaintext as indices: {len(p0_indices)} values")
    print(f"  First 20: {p0_indices[:20]}")
    print(f"Page 1 plaintext as indices: {len(p1_indices)} values")
    print(f"  First 20: {p1_indices[:20]}")
    
    # Test 1: Use Page 0 plaintext as key for Page 1 cipher
    print("\n" + "-" * 60)
    print("TEST 1: Page 0 plaintext as key for Page 1 cipher")
    print("-" * 60)
    
    result = sub_decrypt(pages[1], p0_indices)
    result_text = indices_to_text(result)
    score = score_text(result_text)
    print(f"Score: {score}")
    print(f"Result: {result_text[:100]}...")
    
    # Test 2: Use Page 1 plaintext as key for Page 2 cipher
    print("\n" + "-" * 60)
    print("TEST 2: Page 1 plaintext as key for Page 2 cipher")
    print("-" * 60)
    
    result = sub_decrypt(pages[2], p1_indices)
    result_text = indices_to_text(result)
    score = score_text(result_text)
    print(f"Score: {score}")
    print(f"Result: {result_text[:100]}...")
    
    # Test 3: XOR instead of SUB
    print("\n" + "-" * 60)
    print("TEST 3: XOR operations")
    print("-" * 60)
    
    # XOR Page 0 plaintext with Page 1 cipher
    result = [(pages[1][i] ^ p0_indices[i % len(p0_indices)]) % 29 for i in range(len(pages[1]))]
    result_text = indices_to_text(result)
    score = score_text(result_text)
    print(f"Page 1 XOR Page 0 plain: Score {score}")
    print(f"  Result: {result_text[:80]}...")
    
    # Test 4: ADD instead of SUB
    print("\n" + "-" * 60)
    print("TEST 4: ADD operations")
    print("-" * 60)
    
    result = [(pages[1][i] + p0_indices[i % len(p0_indices)]) % 29 for i in range(len(pages[1]))]
    result_text = indices_to_text(result)
    score = score_text(result_text)
    print(f"Page 1 ADD Page 0 plain: Score {score}")
    print(f"  Result: {result_text[:80]}...")
    
    # Test 5: Page 1 plaintext as key for Page 0 cipher (reverse order)
    print("\n" + "-" * 60)
    print("TEST 5: Reverse - Page 1 plaintext as key for Page 0 cipher")
    print("-" * 60)
    
    result = sub_decrypt(pages[0], p1_indices)
    result_text = indices_to_text(result)
    score = score_text(result_text)
    print(f"Score: {score}")
    print(f"Result: {result_text[:100]}...")
    
    # Test 6: Combine Page 0 and Page 1 plaintexts
    print("\n" + "-" * 60)
    print("TEST 6: Combined plaintext as key for Page 2")
    print("-" * 60)
    
    combined = p0_indices + p1_indices
    result = sub_decrypt(pages[2], combined)
    result_text = indices_to_text(result)
    score = score_text(result_text)
    print(f"Score: {score}")
    print(f"Result: {result_text[:100]}...")
    
    # Test 7: Difference between plaintext sequences
    print("\n" + "-" * 60)
    print("TEST 7: Difference between Page 0 and Page 1 plaintexts")
    print("-" * 60)
    
    min_len = min(len(p0_indices), len(p1_indices))
    diff = [(p0_indices[i] - p1_indices[i]) % 29 for i in range(min_len)]
    diff_text = indices_to_text(diff)
    print(f"Difference: {diff_text[:80]}...")
    
    # Look for patterns
    from collections import Counter
    diff_counts = Counter(diff)
    print(f"Most common differences: {diff_counts.most_common(5)}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
LIBER PRIMUS PAGE 3 - CIRCUMFERENCE VIGENERE SOLVER

Based on the solved Onion 6 pages (107.jpg, 167.jpg), the key was discovered to be:
- Key: "FIRFUMFERENFE" (CIRCUMFERENCE with 'C' → 'F')
- F = shift of 0
- Special rule: F-runes in "OF" and "CIRCUMFERENCE" are ignored (no key increment)

This script tests whether the same methodology applies to Liber Primus Page 3.
"""

from collections import Counter

# ============================================================================
# GEMATRIA PRIMUS - 29 Character Alphabet
# ============================================================================

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

# Letters with digraphs
LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

LETTER_TO_INDEX = {l: i for i, l in enumerate(LETTERS)}

# ============================================================================
# PAGE 3 DATA
# ============================================================================

PAGE3_RUNES = """ᛟᛗ-ᚢ.ᚻᛏ-ᛒᛇᛚᛞᚻᛒᛗ-ᛠᚱᛒ-ᚾᚻᛒᛖᚷᛇ-
ᛞᛚᚹᛇᛡᛈᚩ-ᚻᛖᛠ-ᚹᛁᚱᛁᚻ-ᚢᚦᚻᚣ-ᚾᛉᛒᚷᛄ
ᛈᚢ-ᛝᛠᚠᚾᛁᛖᛞᛡᛝᚱ-ᛞᛒᛄᛡᛟᛗᛁ-ᚠᛏ-ᛄ
ᛞᛁᚦᚱᛚᛋ-ᛖᛇᚩᚷᛒᛏᛞ-ᚦᚪᚾᚳᚣ-ᛡᛋᚦᛞ-ᛝᚠᛚ
ᛖᚷᚻᚳ-ᛖᚩᛁᛏᚾᛉ-ᛈᛏᚠᚻᚱᛞᛖᚠᛏ-ᚫᚹᚻ-ᛒ
ᚳ-ᚠ-ᛈᚪᛚᚢᛠᚾᛚᛄ-ᛄᚳᛚᚹᛠᛞᚢᛞᛇ-ᛠᛉ
ᛞᚹᚻᛠ-ᚦᛡᚫᚳᛚᛏᚹᛖᛁᚳ-ᛈᛟᛞᚳ-ᚾᚻᚪ-ᚱᛁᚷ
ᚦᛠᛖᛏᚷ-ᚦᚻᚩᛡᚹᚫᛄᛖ-ᛝᛠᛞ-ᚩᚫ-ᚪᛚ-ᛒᛄ
ᚳᚢᛉᛏᚪᛒᛄᛈ-ᚠᛠ-ᚻᛞᚾᛡᚢᛈᛋᚢᚹ."""

def extract_runes(text):
    """Extract only runes from text (remove punctuation)"""
    return [RUNE_TO_INDEX[r] for r in text if r in RUNE_TO_INDEX]

# ============================================================================
# VIGENERE CIPHER FUNCTIONS
# ============================================================================

def text_to_key_indices(key_text):
    """Convert text like 'CIRCUMFERENCE' to indices"""
    indices = []
    i = 0
    while i < len(key_text):
        # Try digraphs first
        if i + 2 <= len(key_text):
            digraph = key_text[i:i+2].upper()
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        # Single letter
        letter = key_text[i].upper()
        if letter in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[letter])
        i += 1
    return indices

def vigenere_decrypt(cipher_indices, key_indices):
    """
    Vigenere decryption: plaintext = (cipher - key) mod 29
    """
    plaintext = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        p = (c - k) % 29
        plaintext.append(p)
    return plaintext

def vigenere_encrypt(plaintext_indices, key_indices):
    """
    Vigenere encryption: cipher = (plaintext + key) mod 29
    """
    cipher = []
    key_len = len(key_indices)
    for i, p in enumerate(plaintext_indices):
        k = key_indices[i % key_len]
        c = (p + k) % 29
        cipher.append(c)
    return cipher

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices)

def indices_to_runes(indices):
    """Convert indices back to runes"""
    return "".join(INDEX_TO_RUNE[i] for i in indices)

# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def score_english(text):
    """Score English-likeness using n-grams and keywords"""
    text = text.upper()
    score = 0.0
    
    # Common trigrams (weighted)
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'YOU': 10, 'OUR': 10, 'OUT': 8, 'ALL': 8, 'ONE': 8,
        'OWN': 8, 'HAT': 8, 'HIS': 8, 'WAS': 8, 'NOT': 8
    }
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    # Common bigrams
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TO': 7, 'IT': 7, 'IS': 7, 'ED': 7, 'OR': 7
    }
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    # Cicada-specific keywords (bonus)
    keywords = ['WISDOM', 'TRUTH', 'DIVINE', 'EMERGE', 'INSTAR', 
                'CIRCUMFERENCE', 'KNOWLEDGE', 'SEEK', 'FIND', 'PATH',
                'PARABLE', 'KOAN', 'MASTER', 'STUDENT', 'LESSON',
                'VOICE', 'HEAD', 'ENLIGHTEN', 'QUESTION', 'INSTRUCTION']
    for kw in keywords:
        if kw in text:
            score += 100
    
    return score

# ============================================================================
# KEY VARIATIONS
# ============================================================================

def generate_circumference_keys():
    """Generate different variations of CIRCUMFERENCE as key"""
    keys = {
        # Original CIRCUMFERENCE
        'CIRCUMFERENCE': 'CIRCUMFERENCE',
        
        # Onion 6 variant: C → F 
        'FIRFUMFERENFE': 'FIRFUMFERENFE',
        
        # Without F (shift 0) characters
        'IRCUMFERENCE': 'IRCUMFERENCE',
        
        # CIRCUMFERENCE spelled in rune letters (with C = K)
        'KIRCUMFERENCE': 'CIRCUMFERENCE',
        
        # Try shorter keys
        'CIRCUM': 'CIRCUM',
        'CIRCUIT': 'CIRCUIT',
        
        # Related words from Onion 6 content
        'KOAN': 'KOAN',
        'LESSON': 'LESSON', 
        'MASTER': 'MASTER',
        'VOICE': 'VOICE',
        
        # Thematic words
        'PRIMUS': 'PRIMUS',
        'LIBER': 'LIBER',
        'DIVINITY': 'DIVINITY',
        'WISDOM': 'WISDOM',
        'TRUTH': 'TRUTH',
        'INSTAR': 'INSTAR',
        'EMERGE': 'EMERGE',
        'PARABLE': 'PARABLE',
        
        # Numbers from cicada (as text)
        'THREETHREEZERONE': 'THREETHREEZERONE',
    }
    return keys

def main():
    print("=" * 80)
    print("LIBER PRIMUS PAGE 3 - CIRCUMFERENCE VIGENERE ANALYSIS")
    print("=" * 80)
    
    # Extract cipher
    cipher = extract_runes(PAGE3_RUNES)
    print(f"\nPage 3 cipher length: {len(cipher)} runes")
    print(f"Cipher (first 30): {indices_to_text(cipher[:30])}...")
    
    # ========================================================================
    # TEST 1: Try CIRCUMFERENCE variations
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 1: CIRCUMFERENCE VARIATIONS AS VIGENERE KEY")
    print("=" * 80)
    
    keys = generate_circumference_keys()
    results = []
    
    for key_name, key_text in keys.items():
        key_indices = text_to_key_indices(key_text)
        if not key_indices:
            continue
            
        plaintext = vigenere_decrypt(cipher, key_indices)
        text = indices_to_text(plaintext)
        score = score_english(text)
        
        # Check reversibility
        re_encrypted = vigenere_encrypt(plaintext, key_indices)
        reversible = cipher == re_encrypted
        
        results.append((key_name, len(key_indices), score, reversible, text))
    
    results.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n{'Key':<20} {'Len':>4} {'Score':>6} {'Rev':>4} Plaintext (first 60)")
    print("-" * 100)
    for key_name, key_len, score, rev, text in results[:15]:
        rev_mark = '✓' if rev else '✗'
        print(f"{key_name:<20} {key_len:>4} {score:>6.0f} {rev_mark:>4} {text[:60]}...")
    
    # ========================================================================
    # TEST 2: Try the exact Onion 6 key with F-skip rule
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 2: ONION 6 EXACT METHOD (FIRFUMFERENFE with F-skip)")
    print("=" * 80)
    
    # Key: FIRFUMFERENFE (CIRCUMFERENCE with C→F)
    # Special rule: When decrypting, F-runes in certain words are ignored
    
    firfumferenfe = text_to_key_indices("FIRFUMFERENFE")
    print(f"Key FIRFUMFERENFE: {firfumferenfe} (length {len(firfumferenfe)})")
    print(f"Key as text: {indices_to_text(firfumferenfe)}")
    
    plaintext = vigenere_decrypt(cipher, firfumferenfe)
    text = indices_to_text(plaintext)
    score = score_english(text)
    
    print(f"\nStandard Vigenere with FIRFUMFERENFE:")
    print(f"Score: {score}")
    print(f"Plaintext: {text}")
    
    # Try with different starting positions (offsets)
    print("\n" + "-" * 80)
    print("Testing different key offsets (0-13):")
    
    best_offset_results = []
    for offset in range(len(firfumferenfe)):
        shifted_key = firfumferenfe[offset:] + firfumferenfe[:offset]
        plaintext = vigenere_decrypt(cipher, shifted_key)
        text = indices_to_text(plaintext)
        score = score_english(text)
        best_offset_results.append((offset, score, text))
    
    best_offset_results.sort(key=lambda x: x[1], reverse=True)
    for offset, score, text in best_offset_results[:5]:
        print(f"  Offset {offset:2d}: Score {score:6.0f} | {text[:70]}...")
    
    # ========================================================================
    # TEST 3: Known-plaintext attack with "A KOAN"
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 3: KNOWN-PLAINTEXT ATTACK WITH 'A KOAN'")
    print("=" * 80)
    
    # From Onion 6, we know the solved pages start with "A KOAN: DURING A LESSON..."
    # If Page 3 uses the same format, test if it starts with similar phrases
    
    known_starts = [
        "AKOAN",
        "APARABLE", 
        "ANINSTRUCTION",
        "ACOMMAND",
        "SOMESODOM",  # From Parable
        "ALESION",
        "THEMSTER",
        "DURINGAL",
        "THEVOICE",
        "THELOSFOF",  # Loss of divinity
        "THECIRCUM",
        "CONSUMPT",
        "PRESERV",
    ]
    
    print("\nDeriving keys from known plaintext starts:")
    print(f"{'Assumed Start':<15} Key Prefix -> Score | Plaintext")
    print("-" * 100)
    
    kp_results = []
    for known in known_starts:
        known_indices = text_to_key_indices(known)
        if len(known_indices) == 0:
            continue
        
        # Derive key: key = (cipher - plaintext) mod 29
        derived_key = []
        for i in range(min(len(known_indices), len(cipher))):
            k = (cipher[i] - known_indices[i]) % 29
            derived_key.append(k)
        
        # Try extending this key to full length
        if len(derived_key) >= 3:
            # Repeat the derived key for full decryption
            extended_key = (derived_key * ((len(cipher) // len(derived_key)) + 1))[:len(cipher)]
            
            plaintext = vigenere_decrypt(cipher, extended_key)
            text = indices_to_text(plaintext)
            score = score_english(text)
            
            key_text = indices_to_text(derived_key)
            kp_results.append((known, key_text, score, text))
    
    kp_results.sort(key=lambda x: x[2], reverse=True)
    for known, key_text, score, text in kp_results[:10]:
        print(f"{known:<15} {key_text[:15]:<15} -> {score:>5.0f} | {text[:50]}...")
    
    # ========================================================================
    # TEST 4: Frequency analysis (which letter → E?)
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 4: FREQUENCY ANALYSIS")
    print("=" * 80)
    
    freq = Counter(cipher)
    total = len(cipher)
    
    print(f"\nRune frequency (expecting E-rune ᛖ [18] to be most common):")
    for idx, count in freq.most_common(10):
        pct = count / total * 100
        print(f"  {INDEX_TO_RUNE[idx]} ({LETTERS[idx]:>2}, idx={idx:2d}): {count:3d} ({pct:5.1f}%)")
    
    # If the most common isn't E, try a simple substitution
    most_common_idx = freq.most_common(1)[0][0]
    if most_common_idx != 18:  # E = index 18
        print(f"\nMost common rune is {LETTERS[most_common_idx]} (idx={most_common_idx}), not E (idx=18)")
        shift = (most_common_idx - 18) % 29
        print(f"Trying Caesar shift of {shift}:")
        
        shifted = [(c - shift) % 29 for c in cipher]
        shifted_text = indices_to_text(shifted)
        print(f"  Shifted plaintext: {shifted_text[:80]}...")
        print(f"  Score: {score_english(shifted_text)}")
    
    # ========================================================================
    # TEST 5: Compare with known Onion 6 encryption
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 5: ENCRYPTION PATTERN COMPARISON")
    print("=" * 80)
    
    # The Onion 6 plaintext for "A KOAN" portion
    onion6_plaintext_start = "AKOANDUR"  # Beginning of solved text
    onion6_plain_indices = text_to_key_indices(onion6_plaintext_start)
    
    print(f"\nIf Page 3 is encrypted the same way as Onion 6 'A KOAN' pages:")
    print(f"Onion 6 used key: FIRFUMFERENFE")
    print(f"If Page 3 starts with 'A KOAN', we can verify the key...")
    
    # Check what key would make Page 3 start with "A KOAN"
    if len(onion6_plain_indices) <= len(cipher):
        implied_key = [(cipher[i] - onion6_plain_indices[i]) % 29 for i in range(len(onion6_plain_indices))]
        print(f"\nImplied key if Page 3 → 'AKOAN': {indices_to_text(implied_key)}")
        print(f"Indices: {implied_key}")
        print(f"Expected FIRFUMFEREN...: {firfumferenfe[:len(implied_key)]}")
        
        if implied_key == firfumferenfe[:len(implied_key)]:
            print("✓ MATCH! Page 3 uses FIRFUMFERENFE starting from beginning!")
        else:
            print("✗ Does not match FIRFUMFERENFE at position 0")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    print("""
Based on Onion 6 solving documentation:
- The key "FIRFUMFERENFE" (CIRCUMFERENCE with C→F) was used for Onion 6 pages
- F represents a shift of 0 in the Gematria Primus
- The Liber Primus may use a different encryption method

Next steps:
1. Check if the PDF shows which specific LP pages use Vigenere
2. Verify if Page 3 content matches any known solved format
3. Try other key lengths and patterns from the solved material
""")

if __name__ == "__main__":
    main()

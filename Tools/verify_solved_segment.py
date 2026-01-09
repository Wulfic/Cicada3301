#!/usr/bin/env python3
"""
Verify cipher implementation against known solved segments from rtkd/iddqd.
Tests our cipher methods against community-documented keys and expected plaintext.
"""

# Gematria Primus: rune to index (0-28)
RUNE_TO_IDX = {
    'ᚠ': 0,   # F
    'ᚢ': 1,   # U
    'ᚦ': 2,   # TH
    'ᚩ': 3,   # O
    'ᚱ': 4,   # R
    'ᚳ': 5,   # C/K
    'ᚷ': 6,   # G
    'ᚹ': 7,   # W
    'ᚻ': 8,   # H
    'ᚾ': 9,   # N
    'ᛁ': 10,  # I
    'ᛄ': 11,  # J
    'ᛇ': 12,  # EO
    'ᛈ': 13,  # P
    'ᛉ': 14,  # X
    'ᛋ': 15,  # S/Z
    'ᛏ': 16,  # T
    'ᛒ': 17,  # B
    'ᛖ': 18,  # E
    'ᛗ': 19,  # M
    'ᛚ': 20,  # L
    'ᛝ': 21,  # ING/NG
    'ᛟ': 22,  # OE
    'ᛞ': 23,  # D
    'ᚪ': 24,  # A
    'ᚫ': 25,  # AE
    'ᚣ': 26,  # Y
    'ᛡ': 27,  # IA/IO
    'ᛠ': 28,  # EA
}

IDX_TO_LETTER = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X',
    15: 'S', 16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG',
    22: 'OE', 23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IO', 28: 'EA'
}

# Segment 0.1 - WELCOME (from rtkd transcription)
# 0.1.0.0 = WELCOME (headline)
# Key: divinity (23,10,1,10,9,10,16,26)

# From rtkd: 0.1.0.0 headline is at the start of segment 0.1
# The first word should decrypt to WELCOME with key divinity

# Let's get the actual runes for WELCOME headline from rtkd
# Looking at the transcription: segment 0.1 starts with WELCOME as plaintext

# Test data from rtkd
# 0.1.0.0 ᚢᛠᛝᛋᛇᚠᚳ = WELCOME (using key divinity)
# Wait - the solved pages show WELCOME in plaintext, meaning the key already worked

# Let me test what we can verify:
# The key "divinity" in numeric form: D=23, I=10, V=1(?), I=10, N=9, I=10, T=16, Y=26
# But wait - V is not in Gematria. Let me check the actual mapping.

# From keys file: divinity (23,10,1,10,9,10,16,26)
# This is: 23=D, 10=I, 1=U(?), 10=I, 9=N, 10=I, 16=T, 26=Y
# Hmm, "DIUNITY" not "DIVINITY"... maybe V maps to U in this context

# The key numeric values: [23, 10, 1, 10, 9, 10, 16, 26]

def decrypt_vigenere_with_fskip(runes, key, skip_f=True):
    """
    Decrypt runes using Vigenère with optional F-skip.
    F-skip: Clear text F (index 0) is not encrypted, skip it in key cycle.
    """
    result = []
    key_pos = 0
    key_len = len(key)
    
    for rune in runes:
        if rune not in RUNE_TO_IDX:
            continue
        
        idx = RUNE_TO_IDX[rune]
        
        if skip_f and idx == 0:  # F rune
            # F is not encrypted, output as-is, don't advance key
            result.append('F')
        else:
            # Normal Vigenère: (cipher - key) mod 29
            k = key[key_pos % key_len]
            plain_idx = (idx - k) % 29
            result.append(IDX_TO_LETTER[plain_idx])
            key_pos += 1
    
    return ''.join(result)

def decrypt_vigenere_simple(runes, key):
    """Simple Vigenère without F-skip."""
    result = []
    key_len = len(key)
    
    for i, rune in enumerate(runes):
        if rune not in RUNE_TO_IDX:
            continue
        
        idx = RUNE_TO_IDX[rune]
        k = key[i % key_len]
        plain_idx = (idx - k) % 29
        result.append(IDX_TO_LETTER[plain_idx])
    
    return ''.join(result)

def decrypt_inverted_gematria(runes):
    """Simple substitution with inverted gematria (28 - idx)."""
    result = []
    for rune in runes:
        if rune not in RUNE_TO_IDX:
            continue
        idx = RUNE_TO_IDX[rune]
        plain_idx = (28 - idx) % 29
        result.append(IDX_TO_LETTER[plain_idx])
    return ''.join(result)

def decrypt_shift(runes, shift):
    """Simple Caesar shift."""
    result = []
    for rune in runes:
        if rune not in RUNE_TO_IDX:
            continue
        idx = RUNE_TO_IDX[rune]
        plain_idx = (idx - shift) % 29
        result.append(IDX_TO_LETTER[plain_idx])
    return ''.join(result)

# Test segments from rtkd transcription
# Segment 0.0 (A WARNING) - uses "Substitution. Invert Gematria"
# First line: ᚱ ᛝᚱᚪᛗᚹ = A WARNING

print("=" * 60)
print("VERIFYING CIPHER IMPLEMENTATION AGAINST SOLVED SEGMENTS")
print("=" * 60)

# Test 1: Segment 0.0 - Invert Gematria
print("\n[TEST 1] Segment 0.0 - A WARNING")
print("Method: Substitution, Invert Gematria")
print("-" * 40)

# First word from 0.0: ᚱ should become A (with invert gematria)
# ᚱ = index 4, inverted = 28 - 4 = 24 = A ✓
# ᛝᚱᚪᛗᚹ should become WARNING

test_0_0 = "ᚱ"  # Should be A
result = decrypt_inverted_gematria(test_0_0)
print(f"  ᚱ -> {result} (expected: A)")

test_0_0_word = "ᛝᚱᚪᛗᚹ"  # Should be WARNING
result = decrypt_inverted_gematria(test_0_0_word)
print(f"  ᛝᚱᚪᛗᚹ -> {result}")
# Let's decode manually:
# ᛝ = 21, inverted = 28-21 = 7 = W ✓
# ᚱ = 4, inverted = 28-4 = 24 = A ✓
# ᚪ = 24, inverted = 28-24 = 4 = R ✓
# ᛗ = 19, inverted = 28-19 = 9 = N ✓
# ᚹ = 7, inverted = 28-7 = 21 = NG? (should be I)
# Hmm, doesn't quite match. Let me check other methods.

# Maybe it's just direct mapping without inversion?
print("\n  Testing direct mapping:")
for rune in "ᛝᚱᚪᛗᚹ":
    idx = RUNE_TO_IDX[rune]
    print(f"    {rune} = idx {idx} = {IDX_TO_LETTER[idx]}")

# Test 2: Segment 0.1 - Polyalphabetic with key divinity
print("\n[TEST 2] Segment 0.1 - WELCOME")
print("Method: Polyalphabetic, F-skip, key: divinity")
print("-" * 40)

# From rtkd transcription, first line of 0.1 is:
# 0.1.0.0 - this should be a headline that decrypts to WELCOME
# But we need to find the actual runes for that headline

# From the sentences file: 0.1.0.0 appears to be at line ~30
# Looking for the actual WELCOME ciphertext...

# From rtkd translation file, 0.1.0.0 = WELCOME
# From transcription, we need the runes that produce WELCOME with divinity key

# Actually, the solved pages are in PLAINTEXT in the translation file
# meaning we need to work backwards to verify

# Let's test with known plaintext: WELCOME
# Key: divinity = [23, 10, 1, 10, 9, 10, 16, 26]

# WELCOME in gematria: W=7, E=18, L=20, C=5, O=3, M=19, E=18
# Expected ciphertext with key (plain + key) mod 29:
# W(7) + D(23) = 30 mod 29 = 1 = U
# E(18) + I(10) = 28 = EA
# L(20) + ?(1) = 21 = NG
# C(5) + I(10) = 15 = S
# O(3) + N(9) = 12 = EO
# M(19) + I(10) = 0 = F
# E(18) + T(16) = 34 mod 29 = 5 = C

# Wait, F-skip means F is not encrypted, so:
# If ciphertext F appears, it's already plaintext F

# Let's verify with what rtkd actually shows for 0.1
# Looking at the sentences file, 0.1 section shows runes...

# From rtkd transcription-sentences line 32:
# 0.1.0.1 ᚱᛇᚢᚷᛈᛠᛠ ᚠᚹᛉᛏᚳᛚᛠ ᚣᛗ ᛠᛇ ᛏᚳᚾᚫ ᛝᛗᛡᛡᛗᛗᚹ ᚫᛈᛞᛝᛡᚱ ...

# Let's try this with divinity key
key_divinity = [23, 10, 1, 10, 9, 10, 16, 26]

# From translation, 0.1.0.1 should be something like the second sentence of WELCOME section
# Looking at translation line ~32: continues the welcome text

# Let's test with a different approach: known rune -> known plaintext

print("\n  Testing segment 0.3 (simpler: shift by 3)")
print("  Method: Substitution. Invert Gematria. Key: 3")
print("-" * 40)

# Segment 0.3 uses "Substitution. Invert Gematria. Key: 3"
# This likely means: invert gematria THEN shift by 3, or just shift by 3

# From translation 0.3.0.0 = THE LOSS OF DIVINITY
# We need the runes for this headline

# For now, let's verify our basic cipher operations work
print("\n[SUMMARY OF FINDINGS]")
print("=" * 60)
print("""
1. Segment 0.0: Invert Gematria means (28 - idx) mod 29
   - ᚱ(4) -> 24(A) ✓
   - But full words don't match expected output
   - May need additional processing

2. Segment 0.1: Polyalphabetic with divinity key
   - Key: [23, 10, 1, 10, 9, 10, 16, 26]
   - F-skip: When F appears in ciphertext, it's plaintext F
   - Need actual ciphertext->plaintext pairs to verify

3. Segment 0.3: Invert Gematria + Key 3
   - Combined operation unclear

4. CRITICAL: The solved segments (0.0-0.4) are pages 1-16 in rtkd
   - These are NOT in our repository
   - Our page_00 = rtkd page 17 = segment 0.5 (UNSOLVED body)

5. Community keys work for HEADLINES only in unsolved segments
   - Body text remains uncracked for segments 0.5-0.12
   - Our IoC analysis is finding first-layer patterns in body text
""")

# Test segment 0.5 headline with firfumferenfe
print("\n[TEST 3] Segment 0.5 Headline")
print("Method: Polyalphabetic, F-skip, key: firfumferenfe")
print("-" * 40)

key_firfumferenfe = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]

# From rtkd: 0.5.0.0 = ᛋᚻᛖᚩᚷᛗᛡᚠ ᛋᚣᛖᛝᚳ
# This should decrypt to something readable with the key

headline_0_5 = "ᛋᚻᛖᚩᚷᛗᛡᚠ"  # First word of 0.5 headline
result_fskip = decrypt_vigenere_with_fskip(headline_0_5, key_firfumferenfe, skip_f=True)
result_simple = decrypt_vigenere_simple(headline_0_5, key_firfumferenfe)

print(f"  Headline: ᛋᚻᛖᚩᚷᛗᛡᚠ")
print(f"  With F-skip: {result_fskip}")
print(f"  Simple Vig:  {result_simple}")

# Manual decode of first word:
print("\n  Manual decode (c - key) mod 29:")
for i, rune in enumerate(headline_0_5):
    idx = RUNE_TO_IDX.get(rune, -1)
    if idx == -1:
        continue
    k = key_firfumferenfe[i % len(key_firfumferenfe)]
    plain = (idx - k) % 29
    print(f"    {rune}({idx}) - {k} = {plain} = {IDX_TO_LETTER[plain]}")

print("\n  Trying (c + key) mod 29:")
for i, rune in enumerate(headline_0_5):
    idx = RUNE_TO_IDX.get(rune, -1)
    if idx == -1:
        continue
    k = key_firfumferenfe[i % len(key_firfumferenfe)]
    plain = (idx + k) % 29
    print(f"    {rune}({idx}) + {k} = {plain} = {IDX_TO_LETTER[plain]}")

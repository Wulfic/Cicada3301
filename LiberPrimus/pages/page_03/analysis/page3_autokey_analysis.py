#!/usr/bin/env python3
"""
LIBER PRIMUS PAGE 3 - AUTOKEY CIPHER ANALYSIS

The derived key "IAILEAUUHMENGWTMOEADNGWSYBOF..." doesn't show simple repetition.
This could indicate an AUTOKEY cipher where:
- Key = seed + plaintext (plaintext-autokey)
- Key = seed + ciphertext (ciphertext-autokey)

Also testing if the key itself contains a meaningful message (keyword cipher).
"""

from collections import Counter

# ============================================================================
# GEMATRIA PRIMUS
# ============================================================================

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

LETTER_TO_INDEX = {l: i for i, l in enumerate(LETTERS)}

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
    return [RUNE_TO_INDEX[r] for r in text if r in RUNE_TO_INDEX]

def text_to_indices(text):
    indices = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text):
            digraph = text[i:i+2].upper()
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        letter = text[i].upper()
        if letter in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[letter])
        i += 1
    return indices

def indices_to_text(indices):
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    text = text.upper()
    score = 0.0
    
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'YOU': 10, 'OUR': 10, 'OUT': 8, 'ALL': 8, 'ONE': 8
    }
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7
    }
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    keywords = [
        'WISDOM', 'TRUTH', 'DIVINE', 'EMERGE', 'INSTAR',
        'CIRCUMFERENCE', 'KNOWLEDGE', 'SEEK', 'FIND', 'PATH',
        'PARABLE', 'KOAN', 'MASTER', 'STUDENT', 'LESSON',
        'QUESTION', 'INSTRUCTION', 'CONSUMPTION', 'PRESERVATION',
        'DIVINITY', 'PRIMALITY', 'PROGRAM', 'MIND', 'REALITY'
    ]
    for kw in keywords:
        if kw in text:
            score += len(kw) * 15
    
    return score

# ============================================================================
# AUTOKEY CIPHER FUNCTIONS
# ============================================================================

def autokey_decrypt_plaintext(cipher, seed):
    """
    Plaintext-autokey decryption:
    key = seed + plaintext (each decrypted char becomes part of key)
    """
    seed_indices = text_to_indices(seed) if isinstance(seed, str) else seed
    plaintext = []
    key_stream = list(seed_indices)
    
    for i, c in enumerate(cipher):
        k = key_stream[i]
        p = (c - k) % 29
        plaintext.append(p)
        key_stream.append(p)  # Plaintext extends the key
    
    return plaintext

def autokey_decrypt_ciphertext(cipher, seed):
    """
    Ciphertext-autokey decryption:
    key = seed + ciphertext (each cipher char becomes part of key)
    """
    seed_indices = text_to_indices(seed) if isinstance(seed, str) else seed
    plaintext = []
    key_stream = list(seed_indices)
    
    for i, c in enumerate(cipher):
        k = key_stream[i]
        p = (c - k) % 29
        plaintext.append(p)
        key_stream.append(c)  # Ciphertext extends the key
    
    return plaintext

def vigenere_decrypt(cipher, key):
    return [(cipher[i] - key[i % len(key)]) % 29 for i in range(len(cipher))]

def main():
    print("=" * 80)
    print("LIBER PRIMUS PAGE 3 - AUTOKEY CIPHER ANALYSIS")
    print("=" * 80)
    
    cipher = extract_runes(PAGE3_RUNES)
    print(f"\nCipher length: {len(cipher)} runes")
    
    # ========================================================================
    # TEST 1: Plaintext Autokey with various seeds
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 1: PLAINTEXT AUTOKEY (key = seed + decrypted plaintext)")
    print("=" * 80)
    
    seeds = [
        "A", "AN", "THE", "INSTRUCTION", "PARABLE", "KOAN",
        "WISDOM", "TRUTH", "DIVINE", "INSTAR", "EMERGE",
        "CIRCUMFERENCE", "FIRFUMFERENFE", "LIBER", "PRIMUS",
        "QUESTION", "DISCOVER", "FOLLOW", "IMPOSE",
        "LOSS", "DIVINITY", "CONSUMPTION",
        "F", "U", "TH", "O", "R", "C",  # Single rune starts
    ]
    
    results = []
    for seed in seeds:
        plaintext = autokey_decrypt_plaintext(cipher, seed)
        text = indices_to_text(plaintext)
        score = score_english(text)
        results.append(('PL-AUTOKEY', seed, score, text))
    
    results.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n{'Type':<12} {'Seed':<15} {'Score':>6} Plaintext (first 60)")
    print("-" * 100)
    for typ, seed, score, text in results[:15]:
        print(f"{typ:<12} {seed:<15} {score:>6.0f} {text[:60]}...")
    
    # ========================================================================
    # TEST 2: Ciphertext Autokey with various seeds
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 2: CIPHERTEXT AUTOKEY (key = seed + ciphertext)")
    print("=" * 80)
    
    results = []
    for seed in seeds:
        plaintext = autokey_decrypt_ciphertext(cipher, seed)
        text = indices_to_text(plaintext)
        score = score_english(text)
        results.append(('CT-AUTOKEY', seed, score, text))
    
    results.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n{'Type':<12} {'Seed':<15} {'Score':>6} Plaintext (first 60)")
    print("-" * 100)
    for typ, seed, score, text in results[:15]:
        print(f"{typ:<12} {seed:<15} {score:>6.0f} {text[:60]}...")
    
    # ========================================================================
    # TEST 3: Analyze the derived key as possible message
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 3: KEY AS MESSAGE (Is the key itself meaningful?)")
    print("=" * 80)
    
    # If we assume "AN INSTRUCTION" start, the key we derived was:
    known_start = "ANINSTRUCTIONQUESTIONALLTHINGS"
    known_indices = text_to_indices(known_start)
    derived_key = [(cipher[i] - known_indices[i]) % 29 for i in range(len(known_indices))]
    key_text = indices_to_text(derived_key)
    
    print(f"Derived key from 'AN INSTRUCTION...' start:")
    print(f"  {key_text}")
    print(f"  Length: {len(derived_key)}")
    
    # What if the key is shifted?
    print("\nTrying Caesar shifts on the key:")
    for shift in range(29):
        shifted = [(k + shift) % 29 for k in derived_key]
        shifted_text = indices_to_text(shifted)
        score = score_english(shifted_text)
        if score > 50:
            print(f"  Shift {shift:2d}: {shifted_text} (score: {score})")
    
    # ========================================================================
    # TEST 4: What if the key is the plaintext itself? (Beaufort variant)
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 4: BEAUFORT-STYLE CIPHER (plaintext = key - cipher mod 29)")
    print("=" * 80)
    
    for seed in ['CIRCUMFERENCE', 'FIRFUMFERENFE', 'WISDOM', 'TRUTH', 'DIVINE']:
        seed_indices = text_to_indices(seed)
        # Beaufort: plaintext = (key - cipher) mod 29
        plaintext = [(seed_indices[i % len(seed_indices)] - cipher[i]) % 29 for i in range(len(cipher))]
        text = indices_to_text(plaintext)
        score = score_english(text)
        print(f"Beaufort with '{seed}': {text[:70]}... (score: {score})")
    
    # ========================================================================
    # TEST 5: Running key from known Cicada texts
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 5: RUNNING KEY FROM KNOWN CICADA TEXTS")
    print("=" * 80)
    
    # The Parable (Page 57) as running key
    parable = "PARABLELIKETHEINSTARTUNNELINGTOTHESURFACEWEMUSTSHEDOUROWNCIRCUMFERENCESFINDTHEDIVINITYWITHINANDEMERGE"
    parable_indices = text_to_indices(parable)
    
    if len(parable_indices) >= len(cipher):
        key = parable_indices[:len(cipher)]
        plaintext = vigenere_decrypt(cipher, key)
        text = indices_to_text(plaintext)
        score = score_english(text)
        print(f"Running key = Parable: {text[:70]}... (score: {score})")
    
    # Loss of Divinity as running key
    loss = "THELOSSOFDIVINIYTHECIRCUMFERENCEPRACTICESTHREEBEHAVIORSWHICHCAUSETHELOSSOFDIVINITY"
    loss_indices = text_to_indices(loss)
    
    if len(loss_indices) >= len(cipher):
        key = loss_indices[:len(cipher)]
        plaintext = vigenere_decrypt(cipher, key)
        text = indices_to_text(plaintext)
        score = score_english(text)
        print(f"Running key = Loss of Div: {text[:70]}... (score: {score})")
    
    # A Koan as running key
    koan = "AKOANDURINGALESSONTHEMASTEREXPLAINEDTHEITHEISTHEVOICEOFTHECIRCUMFERENCEHESAIDWHENASKEDBYASTUDENTTOEXPLAINWHATTHATMEAN"
    koan_indices = text_to_indices(koan)
    
    if len(koan_indices) >= len(cipher):
        key = koan_indices[:len(cipher)]
        plaintext = vigenere_decrypt(cipher, key)
        text = indices_to_text(plaintext)
        score = score_english(text)
        print(f"Running key = A Koan: {text[:70]}... (score: {score})")
    
    # ========================================================================
    # TEST 6: Check if it's just direct rune-to-letter (plaintext)
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST 6: CHECKING IF PAGE 3 IS PLAINTEXT (no encryption)")
    print("=" * 80)
    
    direct_text = indices_to_text(cipher)
    score = score_english(direct_text)
    print(f"Direct translation (no decryption):")
    print(f"  {direct_text}")
    print(f"  Score: {score}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    print("""
KEY FINDINGS:

1. The CIRCUMFERENCE/FIRFUMFERENFE Vigenere key from Onion 6 does NOT directly
   apply to LP Page 3. The Onion 6 pages (107.jpg, 167.jpg) used this key, but
   they are separate from the main Liber Primus pages.

2. When assuming "AN INSTRUCTION" as the start, the derived key shows no simple
   repeating pattern, suggesting either:
   - A running key (autokey) cipher
   - A completely different encryption method
   - The content is NOT "AN INSTRUCTION"

3. The highest scoring autokey attempts don't produce coherent English.

4. The most promising results from previous analysis were:
   - Key length 83 with SUB mod 29 (100% reversibility, fragmented output)
   - This may indicate interleaved/columnar encryption

NEXT STEPS:
- Explore columnar transposition before/after substitution
- Test different page content hypotheses
- Look for prime-based key patterns (like Page 56)
""")

if __name__ == "__main__":
    main()

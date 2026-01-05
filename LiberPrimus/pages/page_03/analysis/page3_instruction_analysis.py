#!/usr/bin/env python3
"""
LIBER PRIMUS PAGE 3 - INSTRUCTION ANALYSIS

Based on the CIRCUMFERENCE Vigenere analysis, "AN INSTRUCTION" scored highest (453)
as a known plaintext candidate. This matches the format from Onion 6 page 3:
"AN INSTRUCTION: QUESTION ALL THINGS..."

This script deeply explores this lead.
"""

from collections import Counter
import itertools

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

# ============================================================================
# PAGE 3 CIPHER
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

def text_to_indices(text):
    """Convert text to indices, handling digraphs"""
    indices = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i + 2 <= len(text):
            digraph = text[i:i+2].upper()
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        # Single letter
        letter = text[i].upper()
        if letter in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[letter])
        i += 1
    return indices

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices)

def vigenere_decrypt(cipher, key):
    """Vigenere decryption: plaintext = (cipher - key) mod 29"""
    return [(cipher[i] - key[i % len(key)]) % 29 for i in range(len(cipher))]

def vigenere_encrypt(plaintext, key):
    """Vigenere encryption: cipher = (plaintext + key) mod 29"""
    return [(plaintext[i] + key[i % len(key)]) % 29 for i in range(len(plaintext))]

# ============================================================================
# SCORING
# ============================================================================

def score_english(text):
    """Score English-likeness"""
    text = text.upper()
    score = 0.0
    
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'YOU': 10, 'OUR': 10, 'OUT': 8, 'ALL': 8, 'ONE': 8,
        'OWN': 8, 'HAT': 8, 'HIS': 8, 'WAS': 8, 'NOT': 8,
        'EST': 8, 'TRU': 8, 'WIS': 8
    }
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TO': 7, 'IT': 7, 'IS': 7, 'ED': 7, 'OR': 7
    }
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    # Cicada keywords
    keywords = [
        'WISDOM', 'TRUTH', 'DIVINE', 'EMERGE', 'INSTAR',
        'CIRCUMFERENCE', 'KNOWLEDGE', 'SEEK', 'FIND', 'PATH',
        'PARABLE', 'KOAN', 'MASTER', 'STUDENT', 'LESSON',
        'VOICE', 'HEAD', 'ENLIGHTEN', 'QUESTION', 'INSTRUCTION',
        'LOSS', 'DIVINITY', 'CONSUMPTION', 'PRESERVATION',
        'ADHERENCE', 'DOGMA', 'REASON', 'BELONG', 'DEATH',
        'PRIMALITY', 'WEALTH', 'ATTACHED', 'DESTROY', 'PROGRAM',
        'MIND', 'REALITY', 'YOURSELF', 'FOLLOW', 'IMPOSE', 'DISCOVER',
        'BEING', 'SELF', 'WITHIN', 'WITHOUT', 'SURFACE', 'TUNNELING',
        'SHED', 'SKIN', 'COMMAND', 'EYES', 'DEAD', 'AWAKE'
    ]
    for kw in keywords:
        if kw in text:
            score += len(kw) * 15
    
    return score

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("=" * 80)
    print("LIBER PRIMUS PAGE 3 - 'AN INSTRUCTION' ANALYSIS")
    print("=" * 80)
    
    cipher = extract_runes(PAGE3_RUNES)
    print(f"\nCipher length: {len(cipher)} runes")
    
    # ========================================================================
    # ANALYSIS 1: Known Onion 6 Page 3 content
    # ========================================================================
    print("\n" + "=" * 80)
    print("KNOWN ONION 6 PAGE 3 (229.jpg) CONTENT:")
    print("=" * 80)
    
    onion6_page3_text = """AN INSTRUCTION: QUESTION ALL
THINGS. DISCOVER TRUTH INSIDE
YOURSELF. FOLLOW YOUR TRU
TH. IMPOSE NOTHING ON OTHERS"""
    
    print(onion6_page3_text)
    print("\nConverted to continuous text:")
    onion6_clean = "ANINSTRUCTIONQUESTIONALLTHINGSDISCOVERTRUTHINSIDEYOURSELFFOLLOWOURTRUTHIMPOSENOTHINGONOTHERS"
    print(onion6_clean[:80] + "...")
    
    # ========================================================================
    # ANALYSIS 2: Derive full key from known start
    # ========================================================================
    print("\n" + "=" * 80)
    print("DERIVING KEY FROM 'AN INSTRUCTION' START")
    print("=" * 80)
    
    known_start = "ANINSTRUCTIONQUESTIONALLTHINGS"
    known_indices = text_to_indices(known_start)
    
    print(f"Known plaintext: {known_start}")
    print(f"Length: {len(known_indices)} characters")
    
    # Derive key positions
    derived_key = [(cipher[i] - known_indices[i]) % 29 for i in range(len(known_indices))]
    print(f"\nDerived key indices: {derived_key}")
    print(f"Derived key as text: {indices_to_text(derived_key)}")
    
    # ========================================================================
    # ANALYSIS 3: Look for patterns in derived key
    # ========================================================================
    print("\n" + "=" * 80)
    print("PATTERN ANALYSIS OF DERIVED KEY")
    print("=" * 80)
    
    key_text = indices_to_text(derived_key)
    print(f"Key: {key_text}")
    
    # Check for repeating patterns
    for period in range(2, 16):
        pattern_counts = Counter()
        for i in range(len(derived_key) - period + 1):
            pattern = tuple(derived_key[i:i+period])
            pattern_counts[pattern] += 1
        
        repeats = [(p, c) for p, c in pattern_counts.items() if c > 1]
        if repeats:
            print(f"\nPeriod {period}: Found {len(repeats)} repeating patterns")
            for pattern, count in sorted(repeats, key=lambda x: -x[1])[:3]:
                print(f"  {indices_to_text(list(pattern))} appears {count}x")
    
    # Check if key looks like a word
    print("\n" + "-" * 40)
    print("Checking if key segments are words:")
    
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
        'WISDOM', 'TRUTH', 'DIVINE', 'PRIMES', 'CICADA',
        'CIRCUMFERENCE', 'LIBER', 'PRIMUS', 'INSTAR', 'EMERGE'
    ]
    
    for word in common_words:
        word_indices = text_to_indices(word)
        for start in range(len(derived_key) - len(word_indices) + 1):
            if derived_key[start:start + len(word_indices)] == word_indices:
                print(f"  Found '{word}' at position {start}!")
    
    # ========================================================================
    # ANALYSIS 4: Try different key lengths
    # ========================================================================
    print("\n" + "=" * 80)
    print("TESTING KEY LENGTHS")
    print("=" * 80)
    
    # If the key repeats, find the period
    results = []
    
    for key_len in range(3, 30):
        # Create repeating key from first key_len values
        repeating_key = derived_key[:key_len]
        plaintext = vigenere_decrypt(cipher, repeating_key)
        text = indices_to_text(plaintext)
        score = score_english(text)
        
        # Check if it starts correctly
        starts_correct = text.startswith("ANINSTRUCTION")
        
        results.append((key_len, score, starts_correct, text, indices_to_text(repeating_key)))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n{'KLen':>4} {'Score':>6} {'Start OK':>8} Key -> Plaintext (first 60)")
    print("-" * 100)
    for key_len, score, starts_ok, text, key_text in results[:15]:
        ok = '✓' if starts_ok else ''
        print(f"{key_len:>4} {score:>6.0f} {ok:>8} {key_text[:15]:<15} -> {text[:50]}...")
    
    # ========================================================================
    # ANALYSIS 5: Full decryption with best keys
    # ========================================================================
    print("\n" + "=" * 80)
    print("FULL DECRYPTIONS WITH TOP KEYS")
    print("=" * 80)
    
    # Show full decryption for top 3
    for key_len, score, starts_ok, text, key_text in results[:3]:
        print(f"\n--- Key Length {key_len} (Score: {score}) ---")
        print(f"Key: {key_text}")
        print(f"\nPlaintext:\n{text}")
        
        # Check reversibility
        repeating_key = derived_key[:key_len]
        plaintext = vigenere_decrypt(cipher, repeating_key)
        re_encrypted = vigenere_encrypt(plaintext, repeating_key)
        if cipher == re_encrypted:
            print("\n✓ Reversibility: PERFECT (100%)")
        else:
            match_count = sum(1 for a, b in zip(cipher, re_encrypted) if a == b)
            print(f"\n✗ Reversibility: {match_count}/{len(cipher)}")
    
    # ========================================================================
    # ANALYSIS 6: Compare with Onion 6 expected content
    # ========================================================================
    print("\n" + "=" * 80)
    print("COMPARISON WITH EXPECTED CONTENT")
    print("=" * 80)
    
    # If Page 3 of Liber Primus = Onion 6 page 3 content
    expected_full = "ANINSTRUCTIONQUESTIONALLTHINGSDISCOVERTRUTHINSIDEYOURSELFFOLLOWOURTRUTHIMPOSENOTHINGONOTHERS"
    expected_indices = text_to_indices(expected_full)
    
    print(f"Expected content length: {len(expected_indices)}")
    print(f"Cipher length: {len(cipher)}")
    
    if len(expected_indices) <= len(cipher):
        # Derive full key
        full_derived_key = [(cipher[i] - expected_indices[i]) % 29 for i in range(len(expected_indices))]
        print(f"\nDerived key from full expected content:")
        print(f"  {indices_to_text(full_derived_key)}")
        
        # Check for period
        print("\nChecking for key period...")
        for period in range(2, 20):
            is_periodic = True
            for i in range(len(full_derived_key)):
                if full_derived_key[i] != full_derived_key[i % period]:
                    is_periodic = False
                    break
            if is_periodic:
                print(f"  Key repeats with period {period}: {indices_to_text(full_derived_key[:period])}")
                break
        else:
            print("  No simple period found - key may be a running key or non-repeating")
    
    # ========================================================================
    # ANALYSIS 7: Check if LP Page 3 matches any Onion 6 content
    # ========================================================================
    print("\n" + "=" * 80)
    print("CHECKING ALL ONION 6 CONTENT PATTERNS")
    print("=" * 80)
    
    # All known Onion 6 solved content
    onion6_contents = {
        'KOAN_START': 'AKOANDURINGALESSONTHEMASTEREXPLAINEDTHEI',
        'KOAN_FULL': 'AKOANDURINGALESSONTHEMASTEREXPLAINEDTHEITHEISTHEVOICEOFTHECIRCUMFERENCEHESAIDWHENASKEDBYASTUDENTOEXPLAINWHATTHATMEANTTHEMASTERSAIDITISOICEINSEADHEADIDONTHAVEAOICEINEADTHOUGHTTHESTUDENTANDHERAISEDHISHANDTOTELLTHEMASTERTHEMASTERSTOPP',
        'INSTRUCTION': 'ANINSTRUCTIONQUESTIONALLTHINGSDISCOVERTRUTHINSIDEYOURSELFFOLLOWOURTRUTHIMPOSENOTHINGONOTHERS',
        'LOSS_OF_DIVINITY': 'THELOSSODIVINITYTHECIRCUMFERENCEPRACTICESTHREEBEHAVIORSWHICHCAUSETHELOSSODIVINITYCONSUMPTIONWECONSUMETOOMUCHBECAUSEWEBELIETHEFOLLWINGTWOERRORSWITHINTHEDECPTION',
    }
    
    for name, content in onion6_contents.items():
        content_indices = text_to_indices(content)
        if len(content_indices) > len(cipher):
            content_indices = content_indices[:len(cipher)]
        
        # Derive key
        key = [(cipher[i] - content_indices[i]) % 29 for i in range(len(content_indices))]
        key_text = indices_to_text(key)
        
        # Check for known patterns
        checks = {
            'FIRFUMFERENFE': text_to_indices('FIRFUMFERENFE'),
            'CIRCUMFERENCE': text_to_indices('CIRCUMFERENCE'),
            'All zeros (plaintext)': [0] * 13,
        }
        
        print(f"\n{name}:")
        print(f"  Key (first 26): {key_text[:26]}...")
        
        for check_name, check_pattern in checks.items():
            if key[:len(check_pattern)] == check_pattern:
                print(f"  ✓ Matches {check_name}!")
            elif key_text.startswith(indices_to_text(check_pattern)[:8]):
                print(f"  ~ Partial match with {check_name}")

    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("""
The 'AN INSTRUCTION' plaintext gives a high score but the derived key doesn't
show an obvious repeating pattern like 'CIRCUMFERENCE'.

Possible interpretations:
1. LP Page 3 uses a DIFFERENT encryption than Onion 6 pages
2. The key is a running key (autokey cipher) rather than a repeating key
3. LP Page 3 content is different from Onion 6 content

The CIRCUMFERENCE key was specifically for Onion 6's encrypted pages (107.jpg, 167.jpg).
LP Page 3 may require a different approach entirely.
""")

if __name__ == "__main__":
    main()

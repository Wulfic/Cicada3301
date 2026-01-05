#!/usr/bin/env python3
"""
Analyze the SOLVED pages to understand how the cipher works.
Then apply the same method to unsolved pages.
"""

RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

# The Parable (Page 57) - SOLVED - this is the plaintext
PARABLE = """ADIVINITYMUSTAMUSEITSELFINSOMEFASHADIVINESELFCONTEMPLATIONISPERHAPSTHEONLYPASTTIMETHATSUITSETHEREALITYASONEWHOHASEXHAUSTEALLLOTHERPASTTIMESITBEGANTOPLAYAGAMEWITHITSELFTOBETHISITCASTOFAPARTOFITSELFANDINTHECRUELESTFASHIONMADEITFORGETTHATITWASDIVINECASTINTODAPRISIONOFFLESHTOBECONFINEDFORGENETATIONSINTHISCRUELGAMEONENEEDNOTBECURSEDBUTONEMUSTHAVEFORGOTTENONESORIGINSANDDEVELOPAOPENINGBYTHISOPENINGWEESCAPETHEPRISONOFFLESHANDEXISTENCEITSELFISONLYAFORMWEHAVEFORGOTTENTHATONCEWETOOCOULDFLY"""

# Page 0 - encrypted version of The Parable
PAGE0 = "ᚱᛠᚣᚦᛚᚢᛖᚦᛈᚹᛁᛟᛗᛖᚫᛄᚱᛗᛠᚦᛟᛏᛖᚫᛈᚢᛟᛈᛚᛠᚳᛚᚪᚦᛠᛁᛗᛏᛗᛁᚷᛈᚻᛡᛗᛖᛝᚣᛏᛠᛝᛁᚱᛠᛗᛗᛁᛚᛚᛈᚱᚱᛏᚳᛝᛇᛟᛄᛋᛏᚹᛞᚣᛖᚷᛄᛟᛚᛠᛡᛠᛖᛚᛈᛄᛋᚱᛋᚷᛇᚣᚪᛡᛒᛠᛠᛏᛟ"

# Page 54 - also encrypted version of The Parable
PAGE54 = "ᚦᛠᛡᛟᚷᚠᛈᛗᛁᚱᚢᛁᛚᚱᚱᛡᛠᛠᚹᛗᚢᚫᛡᚣᚪᛗᛗᚦᛁᛄᛇᚢᛒᛄᛇᚪᛡᛁᛈᛄᛋᚦᛗᛈᚪᚦᚱᚣᛗᛡᛚᛈᛄᚢᛠᚾᛇᛄᚱᛗᚱᛠᛄᛖᛒᛝᛁᛋᛏᛗᚣᚳᚳᚾᛟᛖᛡᛈᛗᛡᛁᚢᛁᚾᚳᛠᛠᛋᛇ"

# Our master key derived from (Page0 - Parable) mod 29
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def text_to_indices(text):
    """Convert plain text (like DIVINITY) to indices."""
    indices = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Try to match longest rune first
        matched = False
        for length in [2, 1]:  # Try 2-char runes first, then 1-char
            if i + length <= len(text):
                substr = text[i:i+length]
                if substr in RUNE_TO_IDX:
                    indices.append(RUNE_TO_IDX[substr])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1  # Skip unknown character
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i % 29] for i in indices)

print("=" * 80)
print("🔬 ANALYZING SOLVED PAGES")
print("=" * 80)

# Convert everything to indices
parable_indices = text_to_indices(PARABLE)
page0_indices = unicode_to_indices(PAGE0)
page54_indices = unicode_to_indices(PAGE54)

print(f"\nParable length: {len(parable_indices)} indices")
print(f"Page 0 length: {len(page0_indices)} indices")
print(f"Page 54 length: {len(page54_indices)} indices")
print(f"Master key length: {len(MASTER_KEY)} indices")

# Verify the key derivation
print("\n📐 Verifying key derivation:")
min_len = min(len(page0_indices), len(parable_indices))
derived_key = [(page0_indices[i] - parable_indices[i]) % 29 for i in range(min_len)]
print(f"Key derived from Page0 - Parable (first {min_len}): {derived_key[:20]}...")
print(f"Our master key:                              {MASTER_KEY[:20]}...")
print(f"Match for first {min(min_len, 95)}: {derived_key[:min(min_len,95)] == MASTER_KEY[:min(min_len,95)]}")

# Check if Page 54 uses the same key
print("\n📐 Checking Page 54:")
# Try decrypting Page 54 with the master key
for operation in ['sub', 'add', 'xor']:
    for rotation in range(29):
        for offset in range(min(10, len(MASTER_KEY))):
            decrypted = []
            for i, idx in enumerate(page54_indices):
                key_val = MASTER_KEY[(i + offset) % len(MASTER_KEY)]
                if operation == 'sub':
                    dec = (idx - key_val - rotation) % 29
                elif operation == 'add':
                    dec = (idx + key_val + rotation) % 29
                elif operation == 'xor':
                    dec = (idx ^ key_val ^ rotation) % 29
                decrypted.append(dec)
            
            # Check if it matches the parable
            text = indices_to_text(decrypted).upper()
            if 'DIVINITY' in text or 'AMUSE' in text:
                print(f"  {operation} rot={rotation} off={offset}: FOUND!")
                print(f"  Text: {text[:60]}...")

# The relationship between pages
print("\n" + "=" * 80)
print("📊 RELATIONSHIP ANALYSIS")
print("=" * 80)

# Page 0 - Parable = Key (we know this)
# What about Page 54?
print("\nComparing Page 0 and Page 54:")
if len(page0_indices) == len(page54_indices):
    diff_0_54 = [(page0_indices[i] - page54_indices[i]) % 29 for i in range(len(page0_indices))]
    print(f"Page0 - Page54: {diff_0_54[:20]}...")
    print(f"Is constant?: {len(set(diff_0_54)) == 1}")
    if len(set(diff_0_54)) <= 5:
        print(f"Unique values: {set(diff_0_54)}")
else:
    print(f"Different lengths: {len(page0_indices)} vs {len(page54_indices)}")

# Check XOR relationship
print("\nChecking XOR relationships:")
xor_0_54 = [(page0_indices[i] ^ page54_indices[i]) % 29 for i in range(min(len(page0_indices), len(page54_indices)))]
print(f"Page0 XOR Page54: {xor_0_54[:20]}...")

# Now let's understand how other solved pages work
print("\n" + "=" * 80)
print("📖 UNDERSTANDING THE CIPHER")
print("=" * 80)

# The solved pages show: Ciphertext = Plaintext + Key (mod 29)
# So: Plaintext = Ciphertext - Key (mod 29)
# This is a Vigenère cipher with the rune alphabet

print("""
KNOWN FACTS:
1. Page 0 = Parable + Key (mod 29)
2. Page 54 = Parable + Key' (mod 29) where Key' may differ
3. Master Key length = 95, sum = 1331 = 11³
4. The cipher is a Vigenère-style addition/subtraction

HYPOTHESIS:
Each unsolved page uses the same key but possibly with:
- Different rotation (Caesar shift on key values)
- Different offset (starting position in key)
- Possibly XOR instead of addition/subtraction
""")

# Let's test our hypothesis on unsolved pages
print("\n" + "=" * 80)
print("🧪 TESTING HYPOTHESIS ON UNSOLVED PAGES")
print("=" * 80)

UNSOLVED_PAGES = {
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# Try straight subtraction (no rotation, no offset)
print("\nTrying straight subtraction (rot=0, off=0):")
for page_num, page_unicode in UNSOLVED_PAGES.items():
    indices = unicode_to_indices(page_unicode)
    
    # Straight subtraction
    decrypted = []
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[i % len(MASTER_KEY)]
        dec = (idx - key_val) % 29
        decrypted.append(dec)
    
    text = indices_to_text(decrypted)
    
    # Count English-like patterns
    text_upper = text.upper()
    the_count = text_upper.count('THE')
    and_count = text_upper.count('AND')
    
    print(f"Page {page_num}: THE={the_count} AND={and_count}")
    print(f"  {text[:60]}...")

print("\n✅ Analysis complete!")

# Final insight
print("\n" + "=" * 80)
print("💡 KEY INSIGHT")
print("=" * 80)
print("""
The master key was derived from Page 0 and the Parable using SUBTRACTION.
This means: Ciphertext - Key = Plaintext

For unsolved pages, we need to find:
1. Whether they use the same key
2. What rotation/offset applies
3. Whether any pages share content (like Pages 0 and 54)

The high scores we're getting with XOR suggest that some pages may use
a different operation than simple subtraction.
""")

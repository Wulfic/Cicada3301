"""
Definitive analysis of the 166-stream and interleaved version
Goal: Create a coherent reading of the plaintext
"""

# The 166-stream from P20 prime positions + Deor Beaufort cipher
STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Interleaved version (column read of 2x83 grid)
first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))

print("="*70)
print("FULL INTERLEAVED TEXT")
print("="*70)
print(INTERLEAVED)
print(f"\nLength: {len(INTERLEAVED)}")

# Let me mark the known word positions
print("\n" + "="*70)
print("KNOWN ENGLISH WORDS")
print("="*70)

# Words found with positions
word_positions = [
    (2, 'OF'),
    (7, 'ODE'),      # or EO-DE 
    (10, 'EOME'),    # EO-ME "I go"?
    (11, 'MET'),
    (14, 'BID'),
    (17, 'AM'),
    (19, 'SE'),      # or SEFA (heart)
    (22, 'ALT'),
    (25, 'THE'),
    (28, 'LONE'),
    (29, 'ONE'),
    (32, 'TN'),      # Then?
    (34, 'HER'),
    (76, 'SAY'),
    (78, 'YFTH'),    # ?
    (90, 'DO'),
]

# Let me manually annotate
annotated = list(INTERLEAVED)
print("\nWith spacing based on word boundaries:")

# Try to segment with word knowledge
def manual_segment(text):
    """Manually segment based on known words"""
    # Known words in order of position
    segments = []
    pos = 0
    
    # Position 0-1: HF - unclear
    segments.append(("HF", "?"))
    
    # Position 2-3: OF
    # Actually let's just mark found words
    
    known_words = [
        (2, "OF"),
        (7, "ODE"),  # or start of EO-DE-O
        (11, "MET"),
        (14, "BID"),
        (17, "AM"),
        (22, "ALT"),
        (25, "THE"),
        (28, "LONE"),
        (34, "HER"),
        (76, "SAY"),
    ]
    
    result = []
    i = 0
    while i < len(text):
        found = False
        for pos, word in known_words:
            if i == pos:
                result.append(f"[{word}]")
                i += len(word)
                found = True
                break
        if not found:
            result.append(text[i])
            i += 1
    
    return result

segmented = manual_segment(INTERLEAVED)
print("".join(segmented[:80]))

# Now let's try to read between the lines
print("\n" + "="*70)
print("PARSING WITH RUNEGLISH DIGRAPHS")
print("="*70)

# Gematria Primus with digraphs
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

DIGRAPHS = ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA']

def parse_digraphs(text):
    """Parse text recognizing digraphs"""
    tokens = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            pair = text[i:i+2]
            if pair in DIGRAPHS:
                tokens.append(pair)
                i += 2
                continue
        tokens.append(text[i])
        i += 1
    return tokens

tokens = parse_digraphs(INTERLEAVED)
print(f"Tokens: {' '.join(tokens[:50])}...")
print(f"Total tokens: {len(tokens)}")

# Now look for Old English words in the token stream
print("\n" + "="*70)
print("OLD ENGLISH INTERPRETATION")
print("="*70)

# Common Old English words that might appear:
# - EODE = went, departed (past tense of "gan" - to go)
# - SEFA = heart, mind, spirit
# - MONN = man
# - HE = he
# - HIM = him
# - IS = is
# - SE = the (masc. nom.)
# - ÞÆT = that
# - WÆS = was
# - ON = on

# The interleaved text: HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIO...

# Possible parsing:
# HF OF E E EO DE O MET BID AM SEFA LT THE LONE TN HER A AU IO...
# or
# H FO FEE EODE [O/Ō] MET BID AM SEFA[L/LT] THE LONE [something] HER...

print("Attempt 1: Old English parsing")
print("  HF OF E E EO DE O MET BID AM SEFA LT THE LONE T N HER A A U IO A E T IO AE...")
print()
print("Attempt 2: Grouping")
print("  H FO FEE | EODE | O MET | BID AM | SEFALT | THE LONE | TN HER...")
print()

# Let's see if this forms a sentence
# EODE = "went/departed"
# O MET = "O, I met" or "Ō met" (Oh, I met)
# BID AM = "I bid/asked am" or "Bid am" (I bade)
# SEFALT = SEFA + LT? "heart-less"? Or "SELF ALT" (self alter)
# THE LONE = "the lone one"
# TN HER = "then her"?

print("="*70)
print("BEST INTERPRETATION ATTEMPT")
print("="*70)

print("""
Based on the token analysis, the most likely reading is:

Old English / Archaic English Message:
--------------------------------------
"HF OF [FEE?] EODE, O MET [and] BID AM SEFA[LT], THE LONE [ONE] TN HER..."

Translation Attempt:
-------------------
"[Ho!] For [fee/purpose I] departed, Oh I met [and] bade my heart/self,
 [to] the lone one, then her..."

This appears to be a first-person spiritual/mystical text about:
- Departing on a journey (EODE = went/departed)
- Meeting and commanding one's own heart/self (SEFA = heart/mind)
- The "lone one" - possibly the seeker or the divine
- "Her" - possibly wisdom, the goddess, or the inner feminine

Key Old English terms:
- EODE: past tense of "gan" (to go) - "went, departed"
- SEFA: "heart, mind, spirit, understanding"
- THE LONE: Modern English "the solitary/alone one"

This matches Cicada 3301's themes of:
- Individual spiritual journey
- Self-knowledge (knowing one's own heart/mind)
- The solitary path of the seeker
""")

# Let's also check if there's a simpler message hidden
print("="*70)
print("CHECKING FOR HIDDEN PATTERN")
print("="*70)

# Read every Nth character
for n in [2, 3, 5, 7]:
    print(f"Every {n}th char: {INTERLEAVED[::n][:40]}...")

# Reverse
print(f"Reversed: {INTERLEAVED[::-1][:40]}...")

# Acrostic of known words
known_words = ['OF', 'ODE', 'MET', 'BID', 'AM', 'ALT', 'THE', 'LONE', 'HER', 'SAY']
acrostic = ''.join(w[0] for w in known_words)
print(f"Acrostic of found words: {acrostic}")

"""
Attempt to read the P24 decryption result as English
=====================================================
Tokens: D EA S I X C U D EA D L P N R NG J R EA P E R IA L X G U EA TH EA EO NG 
H W AE IA EO E P TH EA J L AE I R S I O L EA U I U A H NG EA NG J U E S F Y NG 
M EA N L EO G D IA G O W W EO I E W P IA

83 tokens = 83 runic characters
"""

# The tokenized stream
tokens = ['D', 'EA', 'S', 'I', 'X', 'C', 'U', 'D', 'EA', 'D', 'L', 'P', 'N', 'R', 'NG', 'J', 'R', 'EA', 'P', 'E', 'R', 'IA', 'L', 'X', 'G', 'U', 'EA', 'TH', 'EA', 'EO', 'NG', 'H', 'W', 'AE', 'IA', 'EO', 'E', 'P', 'TH', 'EA', 'J', 'L', 'AE', 'I', 'R', 'S', 'I', 'O', 'L', 'EA', 'U', 'I', 'U', 'A', 'H', 'NG', 'EA', 'NG', 'J', 'U', 'E', 'S', 'F', 'Y', 'NG', 'M', 'EA', 'N', 'L', 'EO', 'G', 'D', 'IA', 'G', 'O', 'W', 'W', 'EO', 'I', 'E', 'W', 'P', 'IA']

print(f"Token count: {len(tokens)}")

# Convert to string for analysis
flat = "".join(tokens)
print(f"Flat: {flat}")

# Try to segment into words
# Looking at the pattern:
# D-EA-S  IX  C-U  D-EA-D  L-P-N-R-NG  J  R-EA-P-E-R  IA-L  X  G-U  EA-TH-EA  EO-NG  H-W  AE-IA-EO  E-P  TH-EA  J-L-AE  I-R  S-I-O-L-EA  U-I-U-A  H-NG-EA-NG  J-U-E-S  F-Y-NG  M-EA-N  L-EO-G  D-IA  G-O  W-W-EO  I-E-W  P-IA

print("\n--- Possible Word Segmentation ---")

# Attempt 1: Looking for known patterns
# DEASIX = "DEATH SIX"? No, it says DEASIX not DEATHIX
# But wait - in Runeglish, TH is a single character!
# So "DEATH" would be D-EA-TH, not D-E-A-T-H

# Let me look at it differently:
# If we have D-EA and the stream says "DEAD", we need D-EA-D
# That means positions 0-2 = D EA D = "DEAD" (missing a D)

# Actually looking at raw: "DEASIXCUDEADLPNR..."
# DEA | SIX | CU | DEAD | ...

# In Runeglish: D-EA | S-I-X | C-U | D-EA-D | L-P-N-R | NG-J | R-EA-P-E-R | ...

# Hmm, "REAPER" = R-EA-P-E-R in Runeglish

# Let me try segmenting based on known words:
segments = []
i = 0
while i < len(tokens):
    # Try longest matches first
    found = False
    
    # Check 6-token words
    if i + 5 < len(tokens):
        word6 = "".join(tokens[i:i+6])
        if word6 in ['REAPER', 'THEAEO']:  # THEAEO isn't a word
            segments.append(word6)
            i += 6
            found = True
            continue
    
    # Check 5-token words
    if i + 4 < len(tokens):
        word5 = "".join(tokens[i:i+5])
        if word5 in ['REAPE', 'DEATH', 'THEAN', 'MEANI', 'SINGL']:
            segments.append(word5)
            i += 5
            found = True
            continue
    
    # Check 4-token words
    if i + 3 < len(tokens):
        word4 = "".join(tokens[i:i+4])
        if word4 in ['DEAD', 'MEAN', 'AEON', 'DIAL', 'GOAL', 'LEOG', 'WWEO']:
            segments.append(word4)
            i += 4
            found = True
            continue
    
    # Check 3-token words
    if i + 2 < len(tokens):
        word3 = "".join(tokens[i:i+3])
        if word3 in ['DEA', 'THE', 'SIX', 'CUD', 'LPN', 'RNG', 'IAL', 'GUE', 'ENG', 'HWA', 
                     'EOE', 'JAL', 'AIR', 'SIO', 'LEA', 'UIU', 'AHN', 'JUE', 'SFY', 'NGM',
                     'NLE', 'DIA', 'GOW', 'WEO', 'IEW', 'PIA']:
            segments.append(word3)
            i += 3
            found = True
            continue
    
    # Check 2-token words
    if i + 1 < len(tokens):
        word2 = "".join(tokens[i:i+2])
        if word2 in ['GO', 'WE', 'HE', 'TO', 'IS', 'IT', 'EA', 'IA', 'OE', 'AE']:
            segments.append(word2)
            i += 2
            found = True
            continue
    
    # Single token
    if not found:
        segments.append(tokens[i])
        i += 1

print(f"Segments: {segments}")

# Alternative: Try anagramming or transposing
print("\n--- Transpose the 83 tokens ---")
# 83 is prime, so can't do rectangular transpose
# But maybe read every Nth token

for skip in [2, 3, 5, 7, 11, 13]:
    reordered = []
    for start in range(skip):
        for i in range(start, len(tokens), skip):
            reordered.append(tokens[i])
    result = "".join(reordered)
    print(f"Skip {skip}: {result[:50]}...")

# What if the message needs to be reversed?
print("\n--- Reversed ---")
reversed_tokens = tokens[::-1]
print("".join(reversed_tokens))

# Check for common Cicada phrases
print("\n--- Looking for Cicada themes ---")
cicada_words = ['WITHIN', 'PILGRIM', 'DIVINITY', 'INSTAR', 'CIRCUMFERENCE', 'WISDOM', 
                'SACRED', 'PRIMES', 'TOTIENT', 'EMERGE', 'JOURNEY', 'END', 'BEGIN']

for w in cicada_words:
    if w in flat:
        print(f"  Found: {w}")

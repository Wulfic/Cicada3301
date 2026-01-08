"""
Analyze the non-word segments - are they noise or hidden message?
"""

# Non-word characters from DP segmentation
NONWORD = "HHTHRTHTHDENSHLTHCKHDTHBTMHHLLNMEDTHNCKLYDXTHTPLDTHHSGUPTNHTHWHJRDEDNDTXTHMGMTXWHPHXHPTHPL"

print("="*70)
print("NON-WORD CHARACTER ANALYSIS")
print("="*70)

print(f"Non-word string: {NONWORD}")
print(f"Length: {len(NONWORD)}")

# Character frequency
from collections import Counter
freq = Counter(NONWORD)
print(f"\nCharacter frequency:")
for c, count in freq.most_common():
    print(f"  {c}: {count} ({count/len(NONWORD)*100:.1f}%)")

# H and T are very common - might be TH split up
print(f"\nH count: {freq['H']}, T count: {freq['T']}")
print("If these are split TH, that would explain the pattern")

# Look for patterns
print(f"\n{'='*70}")
print("PATTERN ANALYSIS")
print("="*70)

# Check for repeated substrings
for length in range(3, 8):
    substrings = [NONWORD[i:i+length] for i in range(len(NONWORD)-length+1)]
    repeated = [s for s, count in Counter(substrings).items() if count > 1]
    if repeated:
        print(f"Repeated {length}-grams: {repeated}")

# Check if it's every Nth character of something
print(f"\n{'='*70}")
print("READ AS DIFFERENT PATTERNS")
print("="*70)

# Every 2nd char
even = NONWORD[::2]
odd = NONWORD[1::2]
print(f"Even positions: {even}")
print(f"Odd positions: {odd}")

# Reverse
print(f"Reversed: {NONWORD[::-1]}")

# What if these are positions that should be spaces?
# Count TH patterns in non-word string
th_count = NONWORD.count('TH')
print(f"\nTH occurrences: {th_count}")

# Positions of TH in non-word string
import re
th_positions = [m.start() for m in re.finditer('TH', NONWORD)]
print(f"TH positions: {th_positions}")

# Hypothesis: These are artifacts from TH overcount
# If we remove TH from non-word string
no_th = re.sub('TH', '', NONWORD)
print(f"\nWith TH removed: {no_th}")
print(f"Remaining length: {len(no_th)}")

print(f"\n{'='*70}")
print("CHECK IF NON-WORDS ARE AT SPECIFIC POSITIONS")
print("="*70)

# From the segmentation, non-word positions were:
# [4, 6, 14, 15, 16, 18, 19, 22, 23, 24, 30, 31, 34, 39, 42, 45, 46, 48, 49, 50, 53, 56, 57, 58, 59, 60, 66, 72, 73, 78]...

nonword_positions = [4, 6, 14, 15, 16, 18, 19, 22, 23, 24, 30, 31, 34, 39, 42, 45, 46, 48, 49, 50, 53, 56, 57, 58, 59, 60, 66, 72, 73, 78, 79, 83, 87, 90, 91, 95, 96, 97, 98, 99, 100, 114, 119, 120, 127, 131, 132, 133, 139, 140, 146, 150, 154, 157, 163, 165, 166, 167, 168, 172, 173, 177, 192, 193, 194, 197, 200, 201, 207, 210]

# Check mod patterns
for mod in [2, 3, 4, 5, 7, 11, 13]:
    residues = [p % mod for p in nonword_positions]
    print(f"mod {mod}: {Counter(residues)}")

# Differences between positions
diffs = [nonword_positions[i+1] - nonword_positions[i] for i in range(len(nonword_positions)-1)]
print(f"\nPosition differences: {diffs}")
print(f"Difference distribution: {Counter(diffs)}")

print(f"\n{'='*70}")
print("HYPOTHESIS: These H's are from split THE/TH patterns")
print("="*70)

# In the DP segmentation, [THE] and [HE] might be appearing where there should be [TH]+[E]
# Let's check what words contain these non-word chars

# Looking at segmentation output:
# "[AE] [THAT] [AE] [YET] H [EST] H [EST] [HE]..."
# The H between YET and EST is interesting

# What if the real pattern is:
# AE THAT AE YE-THE-STHE-STHE...
# i.e., "ye the sthe sthe" where STHE is a word or pattern

print("Looking at context around non-word H:")
print("  '[YET] H [EST]' could be 'YETHEST' = 'YE THEST'?")
print("  '[EST] H [EST]' could be 'ESTHEST' = 'ES THEST'?")

# What if we rejoin and try different segmentation?
rejoined = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

# Try different word boundaries starting with known Cicada phrases
print("\n" + "="*70)
print("TRYING KNOWN CICADA PHRASE MATCHING")
print("="*70)

cicada_phrases = [
    'LIKE THE INSTAR',
    'THE DIVINITY WITHIN',
    'FIND THE DIVINITY',
    'WITHIN AND EMERGE',
    'SHED OUR CIRCUMFERENCE',
    'A WARNING',
    'BELIEVE NOTHING',
    'TEST THE KNOWLEDGE',
    'FIND YOUR TRUTH',
    'EXPERIENCE YOUR DEATH',
    'PRIMES ARE SACRED',
    'TOTIENT FUNCTION',
    'ALL THINGS SHOULD BE',
    'AN INSTRUCTION',
    'LOSS OF DIVINITY',
]

for phrase in cicada_phrases:
    simplified = phrase.replace(' ', '')
    if simplified in rejoined:
        print(f"Found: '{phrase}'")
        idx = rejoined.find(simplified)
        print(f"  at position {idx}")
        print(f"  context: ...{rejoined[max(0,idx-10):idx+len(simplified)+10]}...")

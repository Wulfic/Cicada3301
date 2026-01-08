"""
Deep analysis of TH rune distribution - looking for patterns
"""

# Digraphs in Gematria Primus
DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

# Gematria Primus mapping
GEMATRIA = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'D': 22,
    'OE': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

def parse_to_runes(text):
    """Convert text to rune sequence with indices"""
    text = text.upper()
    runes = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in DIGRAPHS:
                runes.append((digraph, GEMATRIA.get(digraph, -1)))
                i += 2
                continue
        if text[i].isalpha():
            runes.append((text[i], GEMATRIA.get(text[i], -1)))
        i += 1
    return runes

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)

print("="*70)
print("TH DISTRIBUTION ANALYSIS")
print("="*70)

# Find all TH positions
th_positions = []
for i, (rune, val) in enumerate(runes):
    if rune == 'TH':
        th_positions.append(i)

print(f"\nTotal runes: {len(runes)}")
print(f"TH count: {len(th_positions)}")
print(f"TH percentage: {len(th_positions)/len(runes)*100:.1f}%")

# Analyze gaps between TH
gaps = []
for i in range(1, len(th_positions)):
    gaps.append(th_positions[i] - th_positions[i-1])

print(f"\nGaps between TH positions: {gaps}")
print(f"Average gap: {sum(gaps)/len(gaps):.2f}")
print(f"Min gap: {min(gaps)}, Max gap: {max(gaps)}")

# Check for periodicity
from collections import Counter
gap_counts = Counter(gaps)
print(f"\nGap frequency distribution:")
for gap, count in sorted(gap_counts.items()):
    print(f"  Gap {gap}: {count} times")

# Check if TH appears at regular intervals
print(f"\n{'='*70}")
print("CHECKING FOR PERIODIC PATTERN")
print("="*70)

# Test if gaps have a common divisor
import math
if len(gaps) > 1:
    overall_gcd = math.gcd(gaps[0], gaps[1])
    for g in gaps[2:]:
        overall_gcd = math.gcd(overall_gcd, g)
    print(f"GCD of all gaps: {overall_gcd}")
    
# Check TH positions modulo various values
print(f"\nTH position modulo analysis:")
for mod in [2, 3, 4, 5, 7, 11, 13]:
    residues = [p % mod for p in th_positions]
    residue_counts = Counter(residues)
    print(f"  mod {mod}: {dict(sorted(residue_counts.items()))}")

# Check what comes AFTER TH
print(f"\n{'='*70}")
print("WHAT FOLLOWS TH?")
print("="*70)

following = []
for i, (rune, val) in enumerate(runes):
    if rune == 'TH' and i+1 < len(runes):
        following.append(runes[i+1][0])

follow_counts = Counter(following)
print(f"Runes following TH:")
for rune, count in sorted(follow_counts.items(), key=lambda x: -x[1]):
    print(f"  TH + {rune}: {count} times ({count/len(following)*100:.1f}%)")

# Check what comes BEFORE TH
print(f"\n{'='*70}")
print("WHAT PRECEDES TH?")
print("="*70)

preceding = []
for i, (rune, val) in enumerate(runes):
    if rune == 'TH' and i > 0:
        preceding.append(runes[i-1][0])

precede_counts = Counter(preceding)
print(f"Runes preceding TH:")
for rune, count in sorted(precede_counts.items(), key=lambda x: -x[1]):
    print(f"  {rune} + TH: {count} times ({count/len(preceding)*100:.1f}%)")

# Check the numerical indices
print(f"\n{'='*70}")
print("GEMATRIA INDEX ANALYSIS")
print("="*70)

# TH has index 2 in Gematria Primus
print("TH has Gematria index: 2")

# What would these TH positions be if they should be something else?
print("\nIf we shift TH (index 2) by various amounts:")
for shift in range(-5, 6):
    new_idx = (2 + shift) % 29
    # Find what rune has this index
    for r, v in GEMATRIA.items():
        if v == new_idx:
            print(f"  Shift {shift:+d}: {r} (index {new_idx})")
            break

# Could there be a consistent shift applied to specific positions?
print(f"\n{'='*70}")
print("PATTERN HYPOTHESIS: Is TH always appearing at specific mod positions?")
print("="*70)

# If TH is at 28.2% but should be at ~5%, we have ~4.5x too many
# That means ~60 of 73 TH should be something else

# Let's see if there's a pattern in which TH are "extra"
# Check if TH appears at positions that are multiples of something

prime_pos_th = []
non_prime_pos_th = []

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

for pos in th_positions:
    if is_prime(pos):
        prime_pos_th.append(pos)
    else:
        non_prime_pos_th.append(pos)

print(f"TH at prime positions: {len(prime_pos_th)}")
print(f"TH at non-prime positions: {len(non_prime_pos_th)}")

# Check even/odd
even_th = [p for p in th_positions if p % 2 == 0]
odd_th = [p for p in th_positions if p % 2 == 1]
print(f"TH at even positions: {len(even_th)}")
print(f"TH at odd positions: {len(odd_th)}")

print(f"\n{'='*70}")
print("HYPOTHESIS: THE might be a 'word' that appears where spaces would be")
print("="*70)

# Count TH+E sequences
the_positions = []
for i in range(len(runes) - 1):
    if runes[i][0] == 'TH' and runes[i+1][0] == 'E':
        the_positions.append(i)

print(f"THE (TH+E) positions: {the_positions}")
print(f"THE count: {len(the_positions)}")

# Gaps between THE
if len(the_positions) > 1:
    the_gaps = []
    for i in range(1, len(the_positions)):
        the_gaps.append(the_positions[i] - the_positions[i-1])
    print(f"Gaps between THE: {the_gaps}")
    print(f"Average gap: {sum(the_gaps)/len(the_gaps):.2f}")

# THE at beginning of segments?
print("\nContext around each THE:")
for pos in the_positions[:10]:  # First 10
    start = max(0, pos-2)
    end = min(len(runes), pos+4)
    context = ' '.join([r[0] for r in runes[start:end]])
    print(f"  Pos {pos}: {context}")

#!/usr/bin/env python3
"""
Compare first-layer output with known Parable text.
Page 57 contains: "LIKE THE INSTAR TUNNELING TO THE SURFACE.
WE MUST SHED OUR OWN CIRCUMFERENCES.
FIND THE DIVINITY WITHIN AND EMERGE::"
"""

GP = ['F','U','TH','O','R','C','K','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','ING','OE','D','A','AE','Y','EA']

def gp_to_idx(text):
    """Convert GP text to indices"""
    indices = []
    i = 0
    while i < len(text):
        found = False
        for length in [3, 2, 1]:  # Try longest first
            if i + length <= len(text):
                chunk = text[i:i+length]
                if chunk in GP:
                    indices.append(GP.index(chunk))
                    i += length
                    found = True
                    break
        if not found:
            i += 1  # Skip unknown
    return indices

def idx_to_gp(indices):
    """Convert indices to GP text"""
    return ''.join(GP[i % 29] for i in indices)

# First layer outputs
PAGES = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGTHEESTHENGTTHEATHEATHTHEAHENGTHETHTHRAAINGTHETHEATETHWAETHEAINGWHIATTHETHATHENGRHEATHEATHETHISOFRAETHOFITHEAEMTHEINGENGTHEHETHEATHFMHTHENGWNGETHEHETHEBDEHEADTHEINGTHEINGTHEAOINGETHIINGITNGTTHWEOTHEHENGTHEATHTHENGNGATHESTWTHETHTHEATHNGETHEIREOENGNG",
}

# Known Parable text (from Page 57)
PARABLE = """LIKE THE INSTAR TUNNELING TO THE SURFACE WE MUST SHED OUR OWN CIRCUMFERENCES FIND THE DIVINITY WITHIN AND EMERGE"""

# Strip spaces from parable
PARABLE_STRIPPED = PARABLE.replace(' ', '').replace('.', '').replace(':', '')

print("=" * 70)
print("PARABLE COMPARISON ANALYSIS")
print("=" * 70)

print(f"\nKnown Parable text (stripped): {PARABLE_STRIPPED[:80]}...")
print(f"Length: {len(PARABLE_STRIPPED)}")

# Convert to GP indices
parable_idx = gp_to_idx(PARABLE_STRIPPED)
print(f"Parable as GP indices: {parable_idx[:30]}...")

# Page 0 first 100 chars
p0 = PAGES[0][:100]
p0_idx = gp_to_idx(p0)

print(f"\nPage 0 first 100 chars: {p0}")
print(f"Page 0 as GP indices: {p0_idx[:30]}...")

# Calculate difference between Page 0 and Parable
print("\n" + "-" * 70)
print("DIFFERENCE ANALYSIS (Page 0 vs Parable)")
print("-" * 70)

min_len = min(len(p0_idx), len(parable_idx))
diffs = [(p0_idx[i] - parable_idx[i]) % 29 for i in range(min_len)]
print(f"Position differences mod 29: {diffs[:40]}...")

# Check if differences form a pattern
from collections import Counter
diff_counts = Counter(diffs)
print(f"Most common differences: {diff_counts.most_common(10)}")

# Check for repeating key
for key_len in [7, 11, 13, 17, 19, 23, 29]:
    matches = 0
    for i in range(min(key_len, len(diffs))):
        if all(diffs[j] == diffs[i] for j in range(i, len(diffs), key_len)):
            matches += 1
    if matches > 0:
        print(f"Key length {key_len}: {matches} matching positions")

# Try subtracting parable from Page 0 to reveal key
print("\n" + "-" * 70)
print("KEY EXTRACTION (if Page 0 = Parable + key)")
print("-" * 70)

# p0 = parable + key  =>  key = p0 - parable
key_as_diff = diffs[:50]
print(f"Extracted key (first 50): {key_as_diff}")
key_as_text = idx_to_gp(key_as_diff)
print(f"Key as GP text: {key_as_text}")

# Check if key is meaningful
known_keys = ['DIVINITY', 'CIRCUMFERENCE', 'INSTAR', 'EMERGE', 'PRIMES', 'TOTIENT']
for kw in known_keys:
    if kw in key_as_text:
        print(f"  *** FOUND '{kw}' in extracted key! ***")

# Try reversing - is parable = Page0 - something?
print("\n" + "-" * 70)
print("REVERSE: Try to find transformation to get Parable from Page 0")
print("-" * 70)

# What if we need to find where Parable appears in the pages?
print("Searching for Parable fragments in first-layer outputs...")

# Key fragments from Parable
parable_fragments = ['INSTAR', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE', 'SURFACE', 'TUNNELING']
for pnum, text in PAGES.items():
    print(f"\nPage {pnum}:")
    for frag in parable_fragments:
        if frag in text:
            print(f"  Found '{frag}'!")
        # Also check shifted versions
        for shift in range(1, 29):
            shifted = idx_to_gp([(gp_to_idx(frag)[i] + shift) % 29 for i in range(len(gp_to_idx(frag)))])
            if shifted in text:
                print(f"  Found shifted({shift}) '{frag}' -> '{shifted}'")

# Different approach: What if the first layer is almost correct but needs word rearrangement?
print("\n" + "-" * 70)
print("WORD FREQUENCY COMPARISON")
print("-" * 70)

parable_trigrams = [PARABLE_STRIPPED[i:i+3] for i in range(len(PARABLE_STRIPPED)-2)]
p0_trigrams = [PAGES[0][i:i+3] for i in range(len(PAGES[0])-2)]

common = set(parable_trigrams) & set(p0_trigrams)
print(f"Common trigrams between Parable and Page 0: {len(common)}")
print(f"Examples: {list(common)[:20]}")

# The solved page 56 uses prime shift
print("\n" + "-" * 70)
print("TESTING PRIME SHIFT (Page 56 method)")
print("-" * 70)

# Formula: plaintext[i] = (cipher[i] - (prime[i] + 57)) mod 29
PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
          101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,
          193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,
          293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401]

p0_full_idx = gp_to_idx(PAGES[0])
prime_shifted = [(p0_full_idx[i] - (PRIMES[i % len(PRIMES)] + 57)) % 29 for i in range(len(p0_full_idx))]
result = idx_to_gp(prime_shifted)
print(f"Page 0 with -(prime[i]+57) shift: {result[:80]}...")

# Try just -prime[i]
simple_prime = [(p0_full_idx[i] - PRIMES[i % len(PRIMES)]) % 29 for i in range(len(p0_full_idx))]
result2 = idx_to_gp(simple_prime)
print(f"Page 0 with -prime[i] shift: {result2[:80]}...")

# Try +prime[i]+57
plus_prime = [(p0_full_idx[i] + (PRIMES[i % len(PRIMES)] + 57)) % 29 for i in range(len(p0_full_idx))]
result3 = idx_to_gp(plus_prime)
print(f"Page 0 with +(prime[i]+57) shift: {result3[:80]}...")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

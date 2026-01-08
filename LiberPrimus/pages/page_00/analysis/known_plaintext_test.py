#!/usr/bin/env python3
"""
Final hypothesis testing based on observations:
1. Old English vocabulary is present (DOETH, LEARETH, HATH, THEE)
2. THE appears frequently but may be an artifact
3. Text might need a simple substitution or rotation we missed

Test: What if Page 0 decrypts to "A WARNING" (first solved page)?
"""

GP = ['F','U','TH','O','R','C','K','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','ING','OE','D','A','AE','Y','EA']

def gp_to_idx(text):
    """Convert GP text to indices"""
    indices = []
    i = 0
    while i < len(text):
        found = False
        for length in [3, 2, 1]:
            if i + length <= len(text):
                chunk = text[i:i+length]
                if chunk in GP:
                    indices.append(GP.index(chunk))
                    i += length
                    found = True
                    break
        if not found:
            i += 1
    return indices

def idx_to_gp(indices):
    return ''.join(GP[i % 29] for i in indices)

# First layer outputs
PAGE0 = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

# Known solved texts (from Onion pages)
A_WARNING = "AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETRUETEST"
WELCOME_START = "WELCOMEWELCOMEPILGRIMTOTHEGREATJOURNEY"

print("=" * 70)
print("KNOWN PLAINTEXT COMPARISON")
print("=" * 70)

p0_idx = gp_to_idx(PAGE0)
warning_idx = gp_to_idx(A_WARNING)

print(f"Page 0 length: {len(p0_idx)}")
print(f"A_WARNING length: {len(warning_idx)}")

# Try to find shift that makes Page 0 start with "A WARNING"
print("\n" + "-" * 70)
print("Testing if Page 0 = A WARNING + constant shift")
print("-" * 70)

for shift in range(29):
    shifted = [(p0_idx[i] - shift) % 29 for i in range(min(15, len(p0_idx)))]
    result = idx_to_gp(shifted)
    if result.startswith('A'):
        print(f"Shift {shift}: {result}")

# Try to find key assuming Page 0 = A WARNING
print("\n" + "-" * 70)
print("Extract key assuming Page 0 plaintext = A_WARNING")
print("-" * 70)

min_len = min(len(p0_idx), len(warning_idx))
key_attempt = [(p0_idx[i] - warning_idx[i]) % 29 for i in range(min_len)]
print(f"Extracted key (first 40): {key_attempt[:40]}")
print(f"Key as text: {idx_to_gp(key_attempt[:40])}")

# Check if key has pattern
from collections import Counter
key_counts = Counter(key_attempt)
print(f"Key value frequency: {key_counts.most_common(10)}")

# Apply this key to decrypt more of Page 0
# If the key works, it should repeat
print("\n" + "-" * 70)
print("Testing extracted key repetition")
print("-" * 70)

# Check if key repeats
for test_len in range(5, min(50, len(key_attempt))):
    matches = 0
    for i in range(len(key_attempt) - test_len):
        if key_attempt[i] == key_attempt[(i + test_len) % test_len]:
            matches += 1
    ratio = matches / (len(key_attempt) - test_len)
    if ratio > 0.8:
        print(f"Key length {test_len}: {ratio*100:.1f}% match")

# What about testing with WELCOME?
print("\n" + "-" * 70)
print("Testing if Page 0 = WELCOME + constant shift")
print("-" * 70)

welcome_idx = gp_to_idx(WELCOME_START)

for shift in range(29):
    shifted = [(p0_idx[i] - shift) % 29 for i in range(min(15, len(p0_idx)))]
    result = idx_to_gp(shifted)
    # Also check shifted + atbash
    atbash_shifted = [(28 - (p0_idx[i] - shift)) % 29 for i in range(min(15, len(p0_idx)))]
    result_ab = idx_to_gp(atbash_shifted)
    if 'WELCOME' in result or 'WELCOME' in result_ab:
        print(f"Found WELCOME at shift {shift}!")
    if 'PILGRIM' in result or 'PILGRIM' in result_ab:
        print(f"Found PILGRIM at shift {shift}!")

# Try CIRCMFERENCE as Vigenere key (from solved pages)
print("\n" + "-" * 70)
print("Testing CIRCUMFERENCE as Vigenere key")
print("-" * 70)

CIRCUMFERENCE = "CIRCUMFERENCE"
circ_idx = gp_to_idx(CIRCUMFERENCE)
print(f"CIRCUMFERENCE as indices: {circ_idx}")

# Apply Vigenere with CIRCUMFERENCE
circ_decrypted = []
for i in range(len(p0_idx)):
    k = circ_idx[i % len(circ_idx)]
    circ_decrypted.append((p0_idx[i] - k) % 29)

result = idx_to_gp(circ_decrypted)
print(f"Page 0 - CIRCUMFERENCE: {result[:80]}...")

# Score this
def score_english(text):
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
    score = 0
    for bg in bigrams:
        score += text.count(bg) * 10
    trigrams = ['THE', 'AND', 'ING', 'HER', 'HAT']
    for tg in trigrams:
        score += text.count(tg) * 20
    return score

print(f"Score: {score_english(result)}")

# Try Atbash first, then CIRCUMFERENCE
print("\n" + "-" * 70)
print("Testing Atbash then CIRCUMFERENCE")
print("-" * 70)

atbash = [(28 - p0_idx[i]) % 29 for i in range(len(p0_idx))]
atbash_circ = [(atbash[i] - circ_idx[i % len(circ_idx)]) % 29 for i in range(len(atbash))]
result2 = idx_to_gp(atbash_circ)
print(f"Atbash(Page 0) - CIRCUMFERENCE: {result2[:80]}...")
print(f"Score: {score_english(result2)}")

# Try DIVINITY key
print("\n" + "-" * 70)
print("Testing DIVINITY as Vigenere key (on Atbash)")
print("-" * 70)

DIVINITY = "DIVINITY"
div_idx = gp_to_idx(DIVINITY)
print(f"DIVINITY as indices: {div_idx}")

atbash_div = [(atbash[i] - div_idx[i % len(div_idx)]) % 29 for i in range(len(atbash))]
result3 = idx_to_gp(atbash_div)
print(f"Atbash(Page 0) - DIVINITY: {result3[:80]}...")
print(f"Score: {score_english(result3)}")

# What about prime-based shift like Page 56?
print("\n" + "-" * 70)
print("Testing Atbash + Prime shift")
print("-" * 70)

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
          101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,
          193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283]

# Atbash then prime shift (like Page 56 but on Atbash)
atbash_prime = [(atbash[i] - (PRIMES[i % len(PRIMES)] + 57)) % 29 for i in range(len(atbash))]
result4 = idx_to_gp(atbash_prime)
print(f"Atbash(Page 0) - (prime+57): {result4[:80]}...")
print(f"Score: {score_english(result4)}")

# Prime without +57
atbash_prime2 = [(atbash[i] - PRIMES[i % len(PRIMES)]) % 29 for i in range(len(atbash))]
result5 = idx_to_gp(atbash_prime2)
print(f"Atbash(Page 0) - prime: {result5[:80]}...")
print(f"Score: {score_english(result5)}")

print("\n" + "=" * 70)
print("SUMMARY: All tests on Page 0 first-layer output")
print("=" * 70)
print(f"Original score: {score_english(PAGE0)}")
print(f"CIRCUMFERENCE: {score_english(result)}")
print(f"Atbash+CIRCUMFERENCE: {score_english(result2)}")
print(f"Atbash+DIVINITY: {score_english(result3)}")
print(f"Atbash+(prime+57): {score_english(result4)}")
print(f"Atbash+prime: {score_english(result5)}")

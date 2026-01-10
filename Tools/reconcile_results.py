"""
Page 20 - Reconciling the Two Decryption Results
==================================================
We have TWO promising results from the 166-stream:

1. INTERLEAVED (column read): "...THE LONE...HER...MET...SELF ALT..."
   - IoC: 1.8952 (preserved)
   - Contains readable English fragments

2. PAIR-SUM + P24 KEY: "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEON..."
   - IoC: 1.1164 (LOWERED)
   - Contains: DEAD, REAPER, THE AEON, SIX, MEAN, DIAG

Question: Are these related? Is one the KEY for the other?
"""

from collections import Counter

# The two streams
STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Interleaved version (column read of 83x2)
first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))

# Pair-sum + P24 key result
PAIRSUM_RESULT = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIRSIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

def to_int_single(text):
    single_gp = {k: v for k, v in GP_MAP.items() if len(k) == 1}
    return [single_gp[c] for c in text if c in single_gp]

def to_int_digraph(text):
    """Parse with digraphs"""
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in GP_MAP:
            result.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            result.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return result

def to_str(nums):
    return "".join(INV_MAP[n % 29] for n in nums)

print("="*70)
print("COMPARISON OF TWO DECRYPTION APPROACHES")
print("="*70)

inter_ints = to_int_single(INTERLEAVED)
pair_ints = to_int_digraph(PAIRSUM_RESULT)

print(f"\n1. INTERLEAVED stream:")
print(f"   Length: {len(INTERLEAVED)} chars, {len(inter_ints)} indices")
print(f"   Text: {INTERLEAVED[:60]}...")
print(f"   Words: THE LONE, HER, MET, SELF ALT, ODE, SAY, OF")

print(f"\n2. PAIR-SUM + P24 result:")
print(f"   Length: {len(PAIRSUM_RESULT)} chars, {len(pair_ints)} indices (digraphs)")
print(f"   Text: {PAIRSUM_RESULT[:60]}...")
print(f"   Words: DEAD, REAPER, THE AEON, SIX, MEAN, DIAG")

# Check if one could be a key for the other
print("\n" + "="*70)
print("TRYING TO USE ONE AS KEY FOR THE OTHER")
print("="*70)

# Use pair-sum result as key for interleaved
print("\n--- Using PAIR-SUM as key for INTERLEAVED ---")
key = pair_ints
cipher = inter_ints[:len(key)]

# Vigenere subtract
result = [(c - k) % 29 for c, k in zip(cipher, key)]
result_text = to_str(result)
print(f"Vigenere (C-K): {result_text}")

# Beaufort
result2 = [(k - c) % 29 for c, k in zip(cipher, key)]
result_text2 = to_str(result2)
print(f"Beaufort (K-C): {result_text2}")

# Use interleaved as key for pair-sum
print("\n--- Using INTERLEAVED as key for PAIR-SUM ---")
key = inter_ints[:len(pair_ints)]
cipher = pair_ints

result = [(c - k) % 29 for c, k in zip(cipher, key)]
result_text = to_str(result)
print(f"Vigenere (C-K): {result_text}")

result2 = [(k - c) % 29 for c, k in zip(cipher, key)]
result_text2 = to_str(result2)
print(f"Beaufort (K-C): {result_text2}")

# XOR-like operation
print("\n--- XOR-like operations ---")
result3 = [(c + k) % 29 for c, k in zip(inter_ints[:len(pair_ints)], pair_ints)]
print(f"Add: {to_str(result3)}")

# What about comparing character positions?
print("\n" + "="*70)
print("PATTERN ANALYSIS")
print("="*70)

# Find common substrings
print("\nCommon words in both:")
common = []
for word in ['THE', 'HE', 'A', 'I', 'ME', 'AN', 'EA', 'AE', 'EO', 'IA', 'NG', 'TH']:
    in_inter = word in INTERLEAVED
    in_pair = word in PAIRSUM_RESULT
    if in_inter and in_pair:
        common.append(word)
print(f"  {common}")

# Position comparison
print("\nPositions of 'THE' in each:")
for name, text in [("INTERLEAVED", INTERLEAVED), ("PAIRSUM", PAIRSUM_RESULT)]:
    pos = 0
    positions = []
    while True:
        idx = text.find('THE', pos)
        if idx == -1:
            break
        positions.append(idx)
        pos = idx + 1
    print(f"  {name}: {positions}")

# Perhaps the two results are COMPLEMENTARY?
print("\n" + "="*70)
print("HYPOTHESIS: COMPLEMENTARY MESSAGES")
print("="*70)

print("""
The two approaches may reveal different aspects of the same message:

INTERLEAVED (spatial rearrangement):
  "...O MET BID AM SELF ALT THE LONE TN HER..."
  Themes: Self, Lone, Her, Met

PAIR-SUM + KEY (mathematical transformation):  
  "...DEAD REAPER THE AEON... MEAN... DIAG..."
  Themes: Death, Reaper, Aeon, Diagonal

These could be:
1. Two halves of the same message
2. The same message encoded twice for redundancy
3. Instructions (DIAG) + Content (THE LONE)

The "DIAG" in PAIR-SUM might be instruction to read diagonally,
which leads to THE LONE in the INTERLEAVED result!
""")

# Test: what if we combine them?
print("="*70)
print("COMBINED MESSAGE ATTEMPT")
print("="*70)

# Extract key phrases from each
inter_phrase = "O MET BID AM SELF ALT THE LONE TN HER"
pair_phrase = "DEAD SIX REAPER THE AEON MEAN DIAG"

print(f"\nFrom INTERLEAVED: {inter_phrase}")
print(f"From PAIR-SUM:    {pair_phrase}")

# Try interleaving the phrases
words1 = inter_phrase.split()
words2 = pair_phrase.split()

interleaved_words = []
for i in range(max(len(words1), len(words2))):
    if i < len(words1):
        interleaved_words.append(words1[i])
    if i < len(words2):
        interleaved_words.append(words2[i])

print(f"\nInterleaved words: {' '.join(interleaved_words)}")

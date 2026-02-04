"""
Deep analysis of the interleaved 166-stream to extract full plaintext
"""

STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))

print("="*70)
print("FULL INTERLEAVED TEXT ANALYSIS")
print("="*70)
print(f"Length: {len(INTERLEAVED)}")
print(f"\nFull text:\n{INTERLEAVED}")

# Manual word parsing attempt
print("\n" + "="*70)
print("MANUAL PARSING ATTEMPT")
print("="*70)

# Let me break this down carefully character by character
text = INTERLEAVED

# Known word positions from the analysis:
# - THE at 25
# - LONE at 28
# - HER at 34
# - ALT at 22
# - MET at 11
# - ODE at 7
# - AM at 17
# - BID at 14
# - SAY at 76

# Let me mark up the text with spaces
marked = list(text)

# Insert spaces before known words
word_positions = [
    (2, 'OF'),      # position 2
    (7, 'ODE'),     # position 7 - but this overlaps with DEOR?
    (11, 'MET'),    # position 11
    (14, 'BID'),    # position 14
    (17, 'AM'),     # position 17
    (19, 'SELF'),   # S at 19? - need to check
    (22, 'ALT'),    # position 22
    (25, 'THE'),    # position 25
    (28, 'LONE'),   # position 28
    (32, 'THEN'),   # T at 32? Could be THEN
    (34, 'HER'),    # HER at 34 or after?
]

print("\nChecking what's at each position:")
for pos, word in word_positions:
    if pos + len(word) <= len(text):
        actual = text[pos:pos+len(word)]
        match = "✓" if actual == word else "✗"
        print(f"  Position {pos}: expected '{word}', found '{actual}' {match}")

# Try different parsing starting points
print("\n" + "="*70)
print("DIFFERENT PARSING APPROACHES")
print("="*70)

# Approach 1: Read from beginning, look for common English words
english_words_3plus = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'OLD', 'SEE',
    'WAY', 'WHO', 'BOY', 'DID', 'GET', 'HIM', 'NOW', 'OWN', 'SAY', 'SHE', 'TOO', 'USE',
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL',
    'SELF', 'LONE', 'THEN', 'WHEN', 'WHAT', 'THERE', 'THEIR', 'WHICH',
    'THEE', 'THOU', 'THINE', 'ALT', 'ALTER', 'FATE', 'DEATH', 'DEAD',
    'MET', 'MEET', 'BID', 'BADE', 'ODE', 'DEOR', 'PATH', 'PRIME',
]

def find_all_words(text):
    """Find all English words at each position"""
    results = {}
    for i in range(len(text)):
        for word in english_words_3plus:
            if text[i:i+len(word)] == word:
                if i not in results:
                    results[i] = []
                results[i].append(word)
    return results

word_map = find_all_words(text)
print("\nWords found at each position:")
for pos in sorted(word_map.keys()):
    words = word_map[pos]
    print(f"  Position {pos}: {words}")
    print(f"    Context: ...{text[max(0,pos-3):pos]}[{text[pos:pos+max(len(w) for w in words)]}]{text[pos+max(len(w) for w in words):pos+max(len(w) for w in words)+5]}...")

# Let me try a different approach - look at the structure
print("\n" + "="*70)
print("STRUCTURE ANALYSIS")
print("="*70)

# The interleaved comes from taking alternate chars from two halves
print("\nFirst half (83 chars):")
print(f"  {first_half}")
print("\nSecond half (83 chars):")
print(f"  {second_half}")

# What if the two halves are two different messages?
# Or one is key and one is ciphertext?

print("\n" + "="*70)
print("HALF-BY-HALF ANALYSIS")
print("="*70)

# Find words in each half
print("\nWords in FIRST half:")
words1 = find_all_words(first_half)
for pos in sorted(words1.keys()):
    print(f"  Position {pos}: {words1[pos]}")

print("\nWords in SECOND half:")
words2 = find_all_words(second_half)
for pos in sorted(words2.keys()):
    print(f"  Position {pos}: {words2[pos]}")

# What if first half minus second half gives plaintext?
print("\n" + "="*70)
print("TRYING HALF-OPERATIONS")
print("="*70)

GP_MAP = {'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9, 
          'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
          'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28}
single_gp = {k: v for k, v in GP_MAP.items() if len(k) == 1}
INV_MAP = {v: k for k, v in GP_MAP.items()}

def to_idx(c):
    return single_gp.get(c, -1)

def from_idx(i):
    return INV_MAP.get(i % 29, '?')

# Try C1 - C2 mod 29
result_sub = []
for c1, c2 in zip(first_half, second_half):
    i1, i2 = to_idx(c1), to_idx(c2)
    if i1 >= 0 and i2 >= 0:
        result_sub.append(from_idx((i1 - i2) % 29))
print(f"First - Second (mod 29):")
print(f"  {''.join(result_sub)}")

# Try C2 - C1 mod 29
result_sub2 = []
for c1, c2 in zip(first_half, second_half):
    i1, i2 = to_idx(c1), to_idx(c2)
    if i1 >= 0 and i2 >= 0:
        result_sub2.append(from_idx((i2 - i1) % 29))
print(f"Second - First (mod 29):")
print(f"  {''.join(result_sub2)}")

# Try C1 + C2 mod 29
result_add = []
for c1, c2 in zip(first_half, second_half):
    i1, i2 = to_idx(c1), to_idx(c2)
    if i1 >= 0 and i2 >= 0:
        result_add.append(from_idx((i1 + i2) % 29))
print(f"First + Second (mod 29):")
print(f"  {''.join(result_add)}")

# Find words in the operation results
print("\n" + "="*70)
print("WORDS IN OPERATION RESULTS")
print("="*70)

for name, result in [("First-Second", ''.join(result_sub)), 
                      ("Second-First", ''.join(result_sub2)),
                      ("First+Second", ''.join(result_add))]:
    words = find_all_words(result)
    if words:
        print(f"\n{name}:")
        for pos in sorted(words.keys()):
            print(f"  Position {pos}: {words[pos]}")

"""
Page 20 - 166-Stream Focused Analysis
======================================
The 166-rune stream (Deor@primes - P20@primes) has IoC=1.8952
This is extremely high - almost like English!

Let's try ALL possible transpositions and anagramming to find readable text.
"""

import os
from collections import Counter
from itertools import permutations

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# The 166-rune stream
STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

print(f"166-stream: {len(STREAM_166)} characters")
print(f"Stream: {STREAM_166}")

# Calculate character frequencies
freq = Counter(STREAM_166)
print(f"\nFrequencies: {dict(freq.most_common())}")

# English letter frequencies for comparison
eng_freq = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 
            'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
            'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0}

# Our frequencies as percentages
our_freq = {c: count/len(STREAM_166)*100 for c, count in freq.items()}
print("\nOur frequencies vs English:")
for c in sorted(our_freq, key=our_freq.get, reverse=True)[:10]:
    eng = eng_freq.get(c, 0)
    print(f"  {c}: {our_freq[c]:.1f}% (English: {eng:.1f}%)")

# The 'E' and 'O' are over-represented - could be due to digraphs
# E: 19.3% vs 12.7% English
# O: 13.9% vs 7.5% English

# Let's look for patterns
print("\n=== PATTERN ANALYSIS ===")

# Look for repeated 2,3,4-grams
for n in [2, 3, 4]:
    ngrams = [STREAM_166[i:i+n] for i in range(len(STREAM_166)-n+1)]
    counts = Counter(ngrams)
    repeated = [(ng, c) for ng, c in counts.items() if c > 1]
    repeated.sort(key=lambda x: -x[1])
    if repeated:
        print(f"{n}-grams repeated: {repeated[:10]}")

# Try reading every Nth character
print("\n=== SKIP PATTERNS (every Nth) ===")

for skip in [2, 3, 4, 5, 6, 7, 8, 11, 13, 17]:
    for start in range(skip):
        result = STREAM_166[start::skip]
        if len(result) >= 10:
            # Look for words
            words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'ONE', 'HER',
                     'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN',
                     'DEATH', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'LONE', 'SELF', 'PRIME']
            found = [w for w in words if w in result]
            if found:
                print(f"Skip {skip}, start {start}: {result}")
                print(f"  Found: {found}")

# Try column reading for various grid sizes
print("\n=== GRID COLUMN READING ===")

for rows in range(2, 20):
    cols = len(STREAM_166) // rows
    if rows * cols != len(STREAM_166):
        continue
    
    # Read by columns
    col_read = ""
    for c in range(cols):
        for r in range(rows):
            col_read += STREAM_166[r * cols + c]
    
    words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'ONE', 'HER',
             'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN',
             'DEATH', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'LONE', 'SELF', 'PRIME', 'MEAN']
    found = [w for w in words if w in col_read]
    
    if len(found) >= 2:
        print(f"Grid {rows}x{cols}: {col_read[:60]}")
        print(f"  Found: {found}")

# Try the 83x2 that we know works well
print("\n=== 83x2 INTERLEAVED (known good) ===")
rows, cols = 83, 2
col_read = ""
for c in range(cols):
    for r in range(rows):
        idx = r * cols + c
        if idx < len(STREAM_166):
            col_read += STREAM_166[idx]

print(f"Result: {col_read}")

# Dictionary-based word segmentation using dynamic programming
print("\n=== DICTIONARY WORD SEGMENTATION ===")

# Extended word list
WORDS = set(['A', 'I', 'AM', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 
             'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
             'ALL', 'AND', 'ANY', 'ARE', 'BUT', 'CAN', 'DID', 'FOR', 'GOT', 'HAD', 'HAS', 
             'HER', 'HIM', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'MET', 'NOT', 'NOW', 'OLD', 
             'ONE', 'OUR', 'OUT', 'OWN', 'SAY', 'SEE', 'SHE', 'THE', 'TOO', 'TWO', 'WAY',
             'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'SAID', 'EACH',
             'WHICH', 'THEIR', 'WILL', 'WOULD', 'THERE', 'ABOUT', 'COULD', 'THESE',
             'DEATH', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'LONE', 'SELF', 'PRIME', 'MEAN',
             'DEAD', 'LIFE', 'SEEK', 'SEEKER', 'WISDOM', 'SACRED', 'AEON', 'REAPER',
             'ODE', 'MET', 'BID', 'ALT', 'EO', 'AE', 'EA', 'IA', 'NG', 'TH', 'OE',
             'THEE', 'THOU', 'THINE', 'HATH', 'DOTH', 'YET', 'LO', 'ART', 'WAS', 'ERE',
             'SONG', 'TELL', 'TOLD', 'KNOW', 'KNEW', 'SEEN', 'CAME', 'COME', 'WENT', 'GONE',
             'HO', 'OH', 'AH', 'YE', 'MATH', 'EAT', 'ATE', 'MEAT', 'HEAT', 'SEAT',
             'DEOR', 'WELA', 'MUND', 'HELM', 'WARD', 'WYRD', 'WEALD', 'MEOD',
             'HEAL', 'HEED', 'FEED', 'NEED', 'DEED', 'SEED', 'MEAD', 'LEAD', 'READ',
             'DOE', 'FOE', 'HOE', 'WOE', 'TOE', 'ROE',
             'OFT', 'SIN', 'WIN', 'TIN', 'FIN', 'BIN', 'DIN', 'KIN', 'PIN',
             'THY', 'WHY', 'TRY', 'CRY', 'DRY', 'FRY', 'PRY', 'SHY', 'SKY', 'SPY'])

def segment_dp(text):
    """Dynamic programming word segmentation"""
    n = len(text)
    dp = [None] * (n + 1)
    dp[0] = []
    
    for i in range(1, n + 1):
        for j in range(i):
            word = text[j:i]
            if word in WORDS and dp[j] is not None:
                candidate = dp[j] + [word]
                if dp[i] is None or len(candidate) < len(dp[i]):
                    dp[i] = candidate
    
    return dp[n] if dp[n] else []

# Segment the interleaved result
result = segment_dp(col_read)
if result:
    print(f"Segmented: {' '.join(result)}")
    print(f"Words found: {len(result)}")
else:
    print("No complete segmentation found")
    # Try partial segmentation
    best_partial = []
    for start in range(min(20, len(col_read))):
        for end in range(len(col_read), max(0, len(col_read)-20), -1):
            result = segment_dp(col_read[start:end])
            if len(result) > len(best_partial):
                best_partial = result
                print(f"Partial [{start}:{end}]: {' '.join(result)}")

# Try with longer word list
print("\n=== ANAGRAM ANALYSIS ===")
print("Looking for anagrams of known words/phrases...")

# Count letters
letter_counts = Counter(col_read)
print(f"Letters: {dict(letter_counts.most_common())}")
print(f"Total: {sum(letter_counts.values())}")

# Check for key phrases
phrases = [
    "THE LONE SEEKER",
    "DEATH COMES FOR",
    "PRIME PATH",
    "SACRED WISDOM",
    "THE DEAD REAPER",
    "FIND THE TRUTH",
    "SEEK AND FIND",
    "THE AEON AWAITS",
]

for phrase in phrases:
    phrase_counts = Counter(phrase.replace(' ', ''))
    can_make = all(letter_counts.get(c, 0) >= phrase_counts[c] for c in phrase_counts)
    if can_make:
        remaining = sum((letter_counts - phrase_counts).values())
        print(f"Can make '{phrase}' ({remaining} letters remain)")

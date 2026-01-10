"""
Page 20 - Deep investigation of high-IoC skip patterns
========================================================
Skip(15,8) gave IoC=3.69 - investigate this!
"""

from collections import Counter

STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

def to_int_single(text):
    single_gp = {k: v for k, v in GP_MAP.items() if len(k) == 1}
    return [single_gp[c] for c in text if c in single_gp]

def to_str(nums):
    return "".join(INV_MAP[n % 29] for n in nums)

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

stream_ints = to_int_single(STREAM_166)
print(f"Stream: {STREAM_166}")
print(f"Length: {len(STREAM_166)} chars, {len(stream_ints)} single-char indices")
print(f"Base IoC: {calc_ioc(stream_ints):.4f}")

# Investigate all high-IoC skip patterns
print("\n=== High-IoC Skip Patterns ===")
skip_results = []

for skip in range(2, 50):
    for start in range(skip):
        result = stream_ints[start::skip]
        if len(result) >= 5:
            ioc = calc_ioc(result)
            text = to_str(result)
            skip_results.append((ioc, skip, start, len(result), text))

skip_results.sort(reverse=True)

print("\nTop 20 skip patterns by IoC:")
for ioc, skip, start, length, text in skip_results[:20]:
    print(f"  skip({skip:2},{start:2}): len={length:3}, IoC={ioc:.4f}, '{text}'")

# The high IoC might be due to short length - investigate
print("\n=== Analysis of Top Skip Patterns ===")

for ioc, skip, start, length, text in skip_results[:5]:
    print(f"\nSkip({skip},{start}): '{text}'")
    print(f"  Length: {length}")
    print(f"  IoC: {ioc:.4f}")
    
    # Character frequency
    freq = Counter(text)
    print(f"  Freq: {dict(freq.most_common(5))}")
    
    # Is this a subset that repeats?
    if len(text) < 20:
        print(f"  NOTE: Very short - IoC may be inflated")

# Now look at the columnar/diagonal results with "THE LONE"
print("\n" + "="*60)
print("=== Analyzing 'THE LONE' patterns ===")
print("="*60)

# Columnar 83 = interleaved (first half, second half)
first_half = STREAM_166[:83]
second_half = STREAM_166[83:]

interleaved = "".join(first_half[i] + second_half[i] for i in range(min(len(first_half), len(second_half))))
print(f"\nInterleaved: {interleaved[:100]}...")
print(f"THE at: {interleaved.find('THE')}")
print(f"LONE at: {interleaved.find('LONE')}")

# What comes around THE LONE?
idx = interleaved.find('THELONE')
if idx >= 0:
    context = interleaved[max(0,idx-20):idx+30]
    print(f"\nContext around 'THELONE': '{context}'")
    
    # Try to segment into words
    segment = interleaved[idx-15:idx+40]
    print(f"Segment to parse: '{segment}'")
    
    # Manual word-finding
    words_in_segment = []
    test_words = ['THE', 'LONE', 'ONE', 'HER', 'HE', 'A', 'I', 'TO', 'IN', 'OF', 'IT', 'IS',
                  'AM', 'ME', 'MY', 'BE', 'SO', 'WE', 'AT', 'OR', 'BY', 'AS', 'DO', 'IF', 'NO',
                  'ALONE', 'STONE', 'DONE', 'TONE', 'BONE', 'GONE', 'NONE',
                  'THEM', 'THEN', 'THERE', 'THESE', 'THEY', 'THIS', 'THOSE',
                  'FALT', 'FAULT', 'HALT', 'SALT', 'MALT', 'WALT',
                  'HEAR', 'HEART', 'EARTH', 'HEARTH',
                  'ODE', 'MODE', 'CODE', 'NODE', 'BODE', 'RODE',
                  'MET', 'SET', 'GET', 'LET', 'BET', 'YET', 'NET', 'WET',
                  'OMIT', 'EMIT', 'SUBMIT',
                  'DAME', 'SAME', 'FAME', 'GAME', 'LAME', 'NAME', 'TAME',
                  'SELF', 'HELP', 'FELT', 'MELT', 'BELT', 'DEALT']
    
    for w in test_words:
        if w in segment:
            idx_w = segment.find(w)
            words_in_segment.append((idx_w, w))
    
    words_in_segment.sort()
    print(f"\nWords found in segment:")
    for idx_w, w in words_in_segment:
        print(f"  {idx_w:3}: {w}")

# Try reading with digraph parsing
print("\n=== Runeglish Digraph Parsing ===")
digraphs = ['TH', 'NG', 'EA', 'OE', 'AE', 'EO', 'IA']

def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in digraphs:
            tokens.append(text[i:i+2])
            i += 2
        else:
            tokens.append(text[i])
            i += 1
    return tokens

tokens = tokenize(interleaved)
print(f"Tokens ({len(tokens)}): {' '.join(tokens[:50])}...")

# Look for word boundaries
print("\n=== Attempting Word Segmentation ===")
# The segment around THE LONE
segment = "AMSEFALTTHELONETNHERAAUIOAETIOAEAYOME"

# Possible parses:
print("Segment: AMSEFALTTHELONETNHERAAUIOAETIOAEAYOME")
print("\nPossible word boundaries:")
print("  AM SELF ALT THE LONE TN HER A AU IO AET IO AE A YO ME")
print("  AM SE FALT THE LONE TN HER AA U IO AET IO AE A YO ME")
print("  A M SELF ALT THE LONE T N HER A AU IO AET IO AE A YO ME")
print("  AM S E FALT THE LONE T N HE RA AU IO AET IO AE A YO ME")

# Check for SELF
if 'SELF' in interleaved:
    print(f"\n'SELF' found at position {interleaved.find('SELF')}")
if 'FALT' in interleaved:
    print(f"'FALT' found at position {interleaved.find('FALT')}")
if 'ALT' in interleaved:
    print(f"'ALT' found at position {interleaved.find('ALT')}")

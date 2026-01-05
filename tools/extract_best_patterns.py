#!/usr/bin/env python3
"""
Extract and analyze the top-scoring positional patterns from SUB-71 plaintext
"""

PLAINTEXT = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTHMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

print("=" * 80)
print("TOP POSITIONAL EXTRACTIONS FROM SUB-71")
print("=" * 80)

# Best patterns from the analysis
patterns = [
    ("every-2nd from offset 1", 1, 2, 255.00),
    ("every-2nd from offset 0", 0, 2, 239.00),
    ("every-5th from offset 1", 1, 5, 233.00),
    ("every-3rd from offset 1", 1, 3, 213.00),
    ("every-3rd from offset 2", 2, 3, 201.00),
]

for name, offset, step, score in patterns:
    extracted = PLAINTEXT[offset::step]
    print(f"\n{name} (score: {score}):")
    print(f"Length: {len(extracted)}")
    print(f"Text: {extracted}")
    print()

# Specifically analyze the BEST one
print("=" * 80)
print("DETAILED ANALYSIS OF BEST PATTERN (every-2nd from offset 1)")
print("=" * 80)

best = PLAINTEXT[1::2]
print(f"\nFull text ({len(best)} chars):")
print(best)

print("\n\nWord-like segments:")
# Try to identify word boundaries
segments = []
current = ""
for i, char in enumerate(best):
    current += char
    # Look for common English patterns
    if len(current) >= 3 and current[-3:] in ['THE', 'ING', 'AND', 'HER', 'HAT', 'ITH', 'TER']:
        segments.append((current, i - len(current) + 1, i))
        current = ""

if current:
    segments.append((current, len(best) - len(current), len(best) - 1))

for seg, start, end in segments:
    if len(seg) >= 3:
        print(f"  [{start:3d}-{end:3d}]: {seg}")

# Check for repeating patterns in the best extraction
print("\n\nRepeating patterns in best extraction:")
for n in [3, 4, 5]:
    ngrams = {}
    for i in range(len(best) - n + 1):
        ngram = best[i:i+n]
        if ngram in ngrams:
            ngrams[ngram].append(i)
        else:
            ngrams[ngram] = [i]
    
    repeated = {k: v for k, v in ngrams.items() if len(v) > 1}
    if repeated:
        print(f"\n{n}-grams (appearing 2+ times):")
        sorted_repeated = sorted(repeated.items(), key=lambda x: len(x[1]), reverse=True)
        for ngram, positions in sorted_repeated[:5]:
            print(f"  '{ngram}': {len(positions)} times")

print("\n" + "=" * 80)
print("INTERPRETATION")
print("=" * 80)
print("""
The every-2nd-character extraction (from offset 1) scores HIGHER than the
full plaintext. This suggests:

1. The SUB-71 decryption produces an INTERLEAVED message
2. Two separate streams are interwoven:
   - Stream 1 (offset 0): positions 0, 2, 4, 6, ...
   - Stream 2 (offset 1): positions 1, 3, 5, 7, ... (BEST)

3. Stream 2 contains the actual message (or most of it)

4. This explains why the full plaintext seems fragmented - it's two
   messages merged together!

Next steps:
- Analyze Stream 1 (offset 0) separately
- Check if streams combine in specific way
- Test if Stream 2 alone is fully readable
- Consider if one stream is padding/noise
""")

print("\n" + "=" * 80)
print("STREAM 1 (every-2nd from offset 0)")
print("=" * 80)

stream1 = PLAINTEXT[0::2]
print(f"Length: {len(stream1)}")
print(f"Text: {stream1}")

print("\n" + "=" * 80)
print("STREAM 2 (every-2nd from offset 1) - THE MAIN MESSAGE")
print("=" * 80)

stream2 = PLAINTEXT[1::2]
print(f"Length: {len(stream2)}")
print(f"Text: {stream2}")
print("\nThis stream has the highest English-likeness score!")

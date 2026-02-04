"""
Compare original stream vs interleaved for word content
"""

STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))

# Find words in both
WORDS = ['THE', 'LONE', 'HER', 'ONE', 'ALT', 'MET', 'ODE', 'AM', 'BID', 'SAY', 'OF', 'AN', 'ON',
         'ME', 'WE', 'HE', 'BE', 'DO', 'TO', 'IT', 'AT', 'AS', 'MY', 'OR', 'IF', 'IN', 'IS',
         'DEATH', 'DEAD', 'PATH', 'FATE', 'SELF', 'THEE', 'THOU', 'THY', 'THINE',
         'EODE', 'SEFA', 'MONN', 'DEOR', 'WYRD']

def find_words(text, words):
    found = {}
    for word in words:
        pos = 0
        while True:
            idx = text.find(word, pos)
            if idx == -1:
                break
            if word not in found:
                found[word] = []
            found[word].append(idx)
            pos = idx + 1
    return found

print("="*70)
print("WORD COMPARISON: ORIGINAL vs INTERLEAVED")
print("="*70)

print("\nOriginal 166-stream:")
found_orig = find_words(STREAM_166, WORDS)
print(f"  Found {len(found_orig)} unique words")
for word in sorted(found_orig.keys(), key=lambda x: -len(x)):
    print(f"    {word}: {found_orig[word]}")

print("\nInterleaved version:")
found_inter = find_words(INTERLEAVED, WORDS)
print(f"  Found {len(found_inter)} unique words")
for word in sorted(found_inter.keys(), key=lambda x: -len(x)):
    print(f"    {word}: {found_inter[word]}")

print("\n" + "="*70)
print("ANALYSIS")
print("="*70)

print(f"\nOriginal has {len(found_orig)} words, Interleaved has {len(found_inter)} words")

# Count total word occurrences
orig_count = sum(len(v) for v in found_orig.values())
inter_count = sum(len(v) for v in found_inter.values())
print(f"Original: {orig_count} word instances, Interleaved: {inter_count} word instances")

# Longest words in each
orig_longest = max(found_orig.keys(), key=len) if found_orig else ""
inter_longest = max(found_inter.keys(), key=len) if found_inter else ""
print(f"Longest word in original: {orig_longest}")
print(f"Longest word in interleaved: {inter_longest}")

# The interleaved version has THE LONE which is significant
if 'LONE' in found_inter:
    print("\n*** INTERLEAVED contains 'LONE' - suggests this is the correct reading ***")

# Try to form meaningful phrase from interleaved
print("\n" + "="*70)
print("ATTEMPTING COHERENT MESSAGE FROM INTERLEAVED")
print("="*70)

# Extract the section around THE LONE
the_pos = INTERLEAVED.find('THE')
lone_pos = INTERLEAVED.find('LONE')
her_pos = INTERLEAVED.find('HER')

print(f"\nKey phrase section (positions 0-50):")
section = INTERLEAVED[:50]
print(f"  {section}")

# Manual parsing attempt
print("\nManual word segmentation:")
print("  H | FO | FEE | E | ODE | O | MET | BID | AM | SEFA | LT | THE | LONE | T | N | HER...")
print()
print("Interpretation:")
print("  'HO! FOR FEE [I] EODE [went], O MET BID AM SEFA [heart], LT THE LONE TN HER...'")
print("  = 'Ho! For reward I went. O, I met and bade my heart, the lone one, then her...'")

# Alternative: What if some letters need to be dropped/added?
print("\n" + "="*70)
print("CHECKING IF TEXT NEEDS SIMPLE ADJUSTMENT")
print("="*70)

# Try dropping first N characters
for n in range(1, 10):
    adjusted = INTERLEAVED[n:]
    if 'THE' in adjusted and 'LONE' in adjusted:
        the_pos = adjusted.find('THE')
        if the_pos < 30:  # THE should be early
            print(f"Dropping first {n} chars: {adjusted[:50]}...")
            break

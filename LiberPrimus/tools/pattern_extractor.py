#!/usr/bin/env python3
"""
Pattern Extractor - Deep analysis of IP-decoded text
Looking for hidden messages within the regular patterns
"""

import re
from collections import Counter

# IP-decoded texts
text2 = 'UFUTHEAFEATHMTHFTHIATHFOEAUEATHEAOEAOIATHIATHEAREATHEAUFEAEFTHEAOFTHIAOYOYTHEAOIAFTHEOFOEOIAUEOIAEOEAEOEAFOETHEATHFOEATHIATHOIATHATHEATHFOEAOFOEFTHYTHEOAOEEOIETHEAOFOETHEAOFTHEOFOEOIATHEAOYTHOIATHEAOYOEAOIAOIAEOFTHEOFOEOEFTHEOTHEAFOEYEOIEFTHFTHEHYATHRTHTHATHMTHEAYJAATYEAYODFMTHAYSEETHAJTHYFRXSTHAIWTHFSETHHAEHWFTHLLTHEOESJMTHTAXTEOYOHTHAHNMETHCFCFNTHENTHFTHETHTHOFTHETH'

text3 = 'YOFTHEAOFTHFCEATHIAOYOYUYTHEATHIATHEAEOEATHAEUAEUEAOEATHEAOEATHIATHEATHEATHEATHEATHEATHEATHEAOIATHIATHEATHEATHEATHEATHEATHEATHFTHEATHEATHEATHEAOEATHEATHEAOEEOAEEOSONXBEAOEOEOEONGCCYJUDEAEANGGYTHRJEOTHTHSSDMIBFOEFEOHDEOINXAEYFNIEAWEAEAYJAOEDSGYGWOLLAEIAAFTHEOTHEOAENGEOYAETHUXEHSEAYEASDELFRNGNMTEAOJCCTHTH'

text4 = 'OEATHAEUEAFEATHEAUEAOIAUFOIATHEATHYTHIAUEATHEAFEAOEAOIATHEAOFTHYOIAOFTHEAOFOEATHIATHFTHFTHEAOEATHEATHYOEAOIATHEATHFTHFTHEATHEAUIATHFTHEATHEATHEAOEAUFTHFUEAOUTHEAUOAOBNOERCUSEATHEOTHXTHMWIAPNNGNFEANGEAOEEOEOBNGOEPAEHTHFHFEAEAEOCIHEOEOTHCYTHTHMLEAGHTHDDFHSOSNPDAETHSNJMAEIATAEXTHEOEIOWLTSNCHSEOAEEONXOELSGGU'

def analyze_between_pattern(text, pattern):
    """Extract characters between occurrences of a pattern"""
    parts = re.split(pattern, text)
    print(f"\n=== Characters between {pattern} occurrences ===")
    between = []
    for i, p in enumerate(parts):
        if p:
            between.append(p)
            print(f'{i}: "{p}"')
    return between

def extract_first_chars(text, pattern):
    """Get first character after each pattern occurrence"""
    parts = re.split(pattern, text)
    first_chars = [p[0] if p else '' for p in parts[1:] if p]  # Skip first part (before first THE)
    return ''.join(first_chars)

def find_regularity_breaks(text):
    """Find where regular patterns break"""
    # The dominant pattern seems to be THEA repeating
    # Find sections that deviate
    print("\n=== Finding pattern breaks ===")
    
    # Look for long runs of THEA
    thea_pattern = r'(THEA)+'
    matches = list(re.finditer(thea_pattern, text))
    for m in matches:
        print(f"THEA run at {m.start()}-{m.end()}: length {m.end()-m.start()}")
    
    # Look for non-THEA sections
    non_thea = re.split(r'(?:THEA)+', text)
    print("\nNon-THEA sections:")
    for i, s in enumerate(non_thea):
        if s and len(s) > 2:
            print(f"  {i}: {s}")

def ngram_analysis(text, n=4):
    """Analyze n-gram frequency"""
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    c = Counter(ngrams)
    print(f"\n=== Most common {n}-grams ===")
    for gram, count in c.most_common(10):
        print(f"  {gram}: {count}")

def look_for_acrostic(text, pattern):
    """Look for acrostic message in first char after pattern"""
    parts = re.split(pattern, text)
    
    # First char after each occurrence
    first = [p[0] if p else '' for p in parts[1:] if p]
    
    # Last char before each occurrence
    last = [p[-1] if p else '' for p in parts[:-1] if p]
    
    print(f"\n=== Potential acrostic from {pattern} ===")
    print(f"First char after each {pattern}: {''.join(first)}")
    print(f"Last char before each {pattern}: {''.join(last)}")
    
    return first, last

def test_alternating_null(text):
    """Test if alternating characters form a message (null cipher)"""
    even = text[::2]
    odd = text[1::2]
    print("\n=== Alternating character extraction ===")
    print(f"Even positions: {even[:80]}...")
    print(f"Odd positions: {odd[:80]}...")
    
    # Check which looks more English-like
    for s, label in [(even, "Even"), (odd, "Odd")]:
        the_count = s.count('THE')
        vowel_ratio = sum(1 for c in s if c in 'AEIOU') / len(s) if s else 0
        print(f"{label}: THE count={the_count}, vowel ratio={vowel_ratio:.2%}")

def position_mod_analysis(text, mod_val):
    """Extract every Nth character"""
    print(f"\n=== Every position mod {mod_val} ===")
    for offset in range(mod_val):
        extracted = text[offset::mod_val]
        the_count = extracted.count('THE')
        print(f"Offset {offset}: {extracted[:60]}... (THE count: {the_count})")

print("=" * 70)
print("PAGE 2 ANALYSIS")
print("=" * 70)

analyze_between_pattern(text2, 'THE')
print("\n=== First char after each THE ===")
fc2 = extract_first_chars(text2, 'THE')
print(fc2)

look_for_acrostic(text2, 'THE')
ngram_analysis(text2)
test_alternating_null(text2)

print("\n" + "=" * 70)
print("PAGE 3 ANALYSIS")
print("=" * 70)

analyze_between_pattern(text3, 'THE')
print("\n=== First char after each THE ===")
fc3 = extract_first_chars(text3, 'THE')
print(fc3)

look_for_acrostic(text3, 'THE')
find_regularity_breaks(text3)
ngram_analysis(text3)

# The interesting bit - extracting from the highly regular section
print("\n" + "=" * 70)
print("HIGHLY REGULAR SECTION OF PAGE 3")
print("=" * 70)

regular = text3[40:180]
print("Section:", regular)
print()

# What if we take every 4th character (THEA = 4)?
print("Every 4th char from offset 0:", regular[0::4])
print("Every 4th char from offset 1:", regular[1::4])
print("Every 4th char from offset 2:", regular[2::4])
print("Every 4th char from offset 3:", regular[3::4])

# What if we extract just the positions that AREN'T T, H, E, or A?
non_thea = ''.join(c for c in regular if c not in 'THEA')
print("\nCharacters that are NOT T, H, E, or A:", non_thea)

print("\n" + "=" * 70)
print("PAGE 4 ANALYSIS")
print("=" * 70)

look_for_acrostic(text4, 'THE')
print("\n=== First char after each THE ===")
fc4 = extract_first_chars(text4, 'THE')
print(fc4)

print("\n" + "=" * 70)
print("COMBINED ACROSTIC")
print("=" * 70)
print("First chars after THE across all pages:")
print(f"Page 2: {fc2}")
print(f"Page 3: {fc3}")
print(f"Page 4: {fc4}")

# What about TH instead of THE?
print("\n=== First char after each TH ===")
th2 = extract_first_chars(text2, 'TH')
th3 = extract_first_chars(text3, 'TH')
th4 = extract_first_chars(text4, 'TH')
print(f"Page 2: {th2}")
print(f"Page 3: {th3}")
print(f"Page 4: {th4}")

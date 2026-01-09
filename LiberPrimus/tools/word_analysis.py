#!/usr/bin/env python3
"""
Word-Based Analysis of Unsolved Pages
======================================
The unsolved pages have clear word boundaries (hyphens and periods).
Let's analyze word patterns and try word-based attacks.
"""

import os
import re
from collections import Counter

GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

def runes_to_runeglish(runes):
    return ''.join(INDEX_TO_RUNEGLISH[GP_RUNE_TO_INDEX[r]] if r in GP_RUNE_TO_INDEX else r for r in runes)

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_words(content):
    """Extract words separated by hyphens or periods."""
    # Split on newlines, hyphens, and periods
    words = re.split(r'[-.\n\r\s]+', content)
    # Keep only words with runes
    words = [w for w in words if any(c in GP_RUNE_TO_INDEX for c in w)]
    return words

# Analyze word patterns across all unsolved pages
print("="*70)
print("WORD-BASED ANALYSIS OF UNSOLVED PAGES")
print("="*70)

all_words = []
word_lengths = []

for page in range(18, 55):
    filepath = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page:02d}/runes.txt"
    if not os.path.exists(filepath):
        continue
    
    content = read_file(filepath)
    words = extract_words(content)
    all_words.extend(words)
    
    for word in words:
        rune_count = sum(1 for c in word if c in GP_RUNE_TO_INDEX)
        if rune_count > 0:
            word_lengths.append(rune_count)

print(f"Total words across pages 18-54: {len(all_words)}")
print(f"Word length distribution:")
length_counter = Counter(word_lengths)
for length in sorted(length_counter.keys()):
    print(f"  Length {length}: {length_counter[length]} words ({length_counter[length]/len(word_lengths)*100:.1f}%)")

# Most common 1-letter words (likely THE, A, I, etc.)
print("\n" + "="*70)
print("SINGLE-LETTER WORDS (likely function words)")
print("="*70)

single_words = [w for w in all_words if sum(1 for c in w if c in GP_RUNE_TO_INDEX) == 1]
single_counter = Counter(single_words)
print("Most common single-rune words:")
for word, count in single_counter.most_common(10):
    runeglish = runes_to_runeglish(word)
    print(f"  {word} ({runeglish}): {count}")

# In English, single letter words are: A, I, O (rarely)
# In Runeglish: A, I, O (no single-letter function words map to digraphs)

# Most common 3-letter patterns (likely THE, AND, FOR, etc.)
print("\n" + "="*70)
print("THREE-LETTER WORDS (likely THE, AND, etc.)")
print("="*70)

three_words = [w for w in all_words if sum(1 for c in w if c in GP_RUNE_TO_INDEX) == 3]
three_counter = Counter(three_words)
print("Most common 3-rune words:")
for word, count in three_counter.most_common(15):
    runeglish = runes_to_runeglish(word)
    print(f"  {word} ({runeglish}): {count}")

# Pattern analysis: Find repeated word patterns
print("\n" + "="*70)
print("REPEATED WORD PATTERNS")
print("="*70)

word_patterns = Counter()
for word in all_words:
    rune_only = ''.join(c for c in word if c in GP_RUNE_TO_INDEX)
    if len(rune_only) >= 3:
        word_patterns[rune_only] += 1

print("Most repeated words (rune patterns):")
for pattern, count in word_patterns.most_common(20):
    if count >= 5:  # Only show patterns that repeat significantly
        runeglish = runes_to_runeglish(pattern)
        print(f"  {pattern} ({runeglish}): {count} occurrences")

# Attempt substitution based on frequency
print("\n" + "="*70)
print("SUBSTITUTION ATTEMPT BASED ON WORD FREQUENCY")
print("="*70)

# The most common 3-letter word in English is "THE"
# Let's see if the most common 3-rune word could be "THE"
if three_words:
    most_common_3 = three_counter.most_common(1)[0][0]
    mc3_runes = [c for c in most_common_3 if c in GP_RUNE_TO_INDEX]
    if len(mc3_runes) == 3:
        print(f"Most common 3-rune word: {most_common_3}")
        print(f"  If this is 'THE' (TH-E in runeglish = indices 2,18):")
        print(f"  Rune 1 ({mc3_runes[0]}) = TH")
        print(f"  Rune 2 ({mc3_runes[1]}) = (could be H if TH split)")
        print(f"  Rune 3 ({mc3_runes[2]}) = E")

# Look for page 59's solved words in the word patterns
print("\n" + "="*70)
print("SEARCHING FOR KNOWN WORDS FROM PAGE 59")
print("="*70)

# From page 59's cipher:
# "A WARNING" -> starts with single letter A
# "BELIEVE" has 7 letters
# "NOTHING" has 7 letters  
# "TRUTH" has 5 letters

# Look for 5-rune words (could be TRUTH)
five_words = [w for w in all_words if sum(1 for c in w if c in GP_RUNE_TO_INDEX) == 5]
five_counter = Counter(five_words)
print("Most common 5-rune words (could be TRUTH, THEIR, THERE, etc.):")
for word, count in five_counter.most_common(10):
    runeglish = runes_to_runeglish(word)
    print(f"  {word} ({runeglish}): {count}")

# Check first word of page 18
print("\n" + "="*70)
print("FIRST WORDS OF UNSOLVED PAGES")
print("="*70)

for page in [18, 19, 20, 21, 22, 23, 24, 25]:
    filepath = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page:02d}/runes.txt"
    if not os.path.exists(filepath):
        continue
    
    content = read_file(filepath)
    words = extract_words(content)
    if words:
        first_word = words[0]
        runeglish = runes_to_runeglish(first_word)
        word_len = sum(1 for c in first_word if c in GP_RUNE_TO_INDEX)
        print(f"Page {page:02d} first word: {first_word} ({runeglish}) - {word_len} runes")

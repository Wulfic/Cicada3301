"""
Analyze the P24 key decryption result
=====================================
The result "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIR..." 
contains: DEAD, REAPER, THE, AEON, etc.

This might be readable with proper word segmentation!
"""

# The decryption result
text = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIR SIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"

# Remove the space I accidentally added
text = text.replace(' ', '')

print("="*60)
print("ANALYZING P24 KEY DECRYPTION RESULT")
print("="*60)

print(f"\nFull text ({len(text)} chars):")
print(text)

# Look for English words
words = [
    'THE', 'AND', 'DEATH', 'DEAD', 'REAPER', 'AEON', 'PATH', 'WAY', 'SONG', 
    'POEM', 'KEY', 'FIND', 'THIS', 'THAT', 'WHO', 'WHAT', 'WHERE', 'WHEN',
    'IS', 'ARE', 'WAS', 'WERE', 'WILL', 'WOULD', 'COULD', 'SHOULD',
    'ALL', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT',
    'DIVINE', 'DIVINITY', 'SACRED', 'PRIMES', 'PRIME', 'NUMBER',
    'CICADA', 'PILGRIM', 'INSTAR', 'EMERGE', 'WITHIN',
    'REAL', 'TRUE', 'TRUTH', 'WISE', 'WISDOM',
    'MEAN', 'MEANING', 'LIFE', 'LIVE', 'SOUL', 'SPIRIT',
    'GUIDE', 'LEAD', 'LEADER', 'FOLLOW',
    'RATIO', 'LENGTH', 'ANGEL', 'DIAL', 'GO', 'SEE', 'SAW',
    'IA', 'EA', 'OE', 'AE',  # Runic digraphs
    'EAR', 'EYE', 'LEG', 'AGE', 'ERA',
    'OWE', 'OWN', 'NEW', 'OLD',
    'USE', 'SING', 'SONG', 'SUNG',
    'ONG', 'ENG', 'ANG',  # NG digraph words
    'REAP', 'SOWING', 'SOW', 'WEEP',
    'GLOW', 'SLOW', 'FLOW', 'GROW',
]

print("\n--- Words Found ---")
found = []
for w in words:
    if w in text.upper():
        pos = text.upper().find(w)
        found.append((w, pos))
        print(f"  {w} at position {pos}")

# Try to segment the text
print("\n--- Manual Segmentation Attempt ---")

# Break down:
# DEA SIX CU DEAD LP NR NG J REAPER IA L X GU EA THE AEON G HW AE IA EO EP THE AJ LAE IR
# SIOLE AU IU AH NG EA NG JU ES FY NG MEAN LE OG DIA GO WW EO IE W PIA

# Let me try different segmentations
segments = [
    "DEA", "SIX", "CU", "DEAD", "LP", "NR", "NG", "J", "REAPER", "IA", "L", "X", 
    "GU", "EA", "THE", "AEON", "G", "HW", "AE", "IA", "EO", "EP", "THE", "AJ", "LAE", "IR",
    "SIOLE", "AU", "IU", "AH", "NG", "EA", "NG", "JU", "ES", "FY", "NG", "MEAN", 
    "LE", "OG", "DIA", "GO", "WW", "EO", "IE", "W", "PIA"
]

print("Possible segmentation:")
print(" ".join(segments))

# Alternative reading - maybe it's an anagram or needs reordering?
print("\n--- Character Frequency ---")
from collections import Counter
freq = Counter(text.upper())
print(dict(sorted(freq.items(), key=lambda x: -x[1])))

# What if some letters are meant to be digraphs?
print("\n--- Converting to Runeglish with digraphs ---")
# Map single letters to their runic equivalents
# EA, IA, OE, AE, NG, TH, EO should be considered

i = 0
runeglish = []
while i < len(text):
    # Check for digraphs first
    if i + 1 < len(text):
        pair = text[i:i+2].upper()
        if pair in ['TH', 'EA', 'IA', 'OE', 'AE', 'NG', 'EO']:
            runeglish.append(pair)
            i += 2
            continue
    runeglish.append(text[i].upper())
    i += 1

print("Runeglish tokens:", " ".join(runeglish))
print(f"Token count: {len(runeglish)}")

# Look for words in the tokenized version
print("\n--- Searching Runeglish for words ---")
runeglish_str = "".join(runeglish)
for w in ['THE', 'DEATH', 'DEAD', 'REAPER', 'AEON', 'MEAN', 'MEANING', 'REAL', 'DIAL', 'GO']:
    if w in runeglish_str:
        print(f"  Found: {w}")

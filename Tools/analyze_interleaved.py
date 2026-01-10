"""
Page 20 - Analyze the interleaved stream in detail
====================================================
The interleaved/column-read version: 
HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYW...
contains 'THE' and 'LONE' - let's segment it!
"""

INTERLEAVED = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"

print("Interleaved Stream Analysis")
print("="*60)
print(f"Stream: {INTERLEAVED}")
print(f"Length: {len(INTERLEAVED)}")

# Find all English words
import re

english_words = [
    # 3+ letter words
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'OLD', 'SEE',
    'WAY', 'WHO', 'BOY', 'DID', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'MAN', 'NEW', 'NOW',
    'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'HE', 'WE', 'SO', 'IF', 'TO', 'OF', 'IN', 'IT',
    # Content words
    'DEATH', 'DEAD', 'REAPER', 'AEON', 'LONE', 'ALONE', 'STONE', 'TONE', 'BONE', 'ZONE',
    'MEATH', 'SHEATH', 'BREATH', 'WREATH', 'BENEATH', 'HEATH',
    'PATH', 'MATH', 'BATH', 'WRATH', 'OATH',
    'PRIME', 'NUMBER', 'RATIO', 'LENGTH', 'MEAN', 'SUM', 'TOTAL',
    'DEOR', 'SONG', 'POEM', 'VERSE', 'LINE', 'WORD', 'RUNE',
    'KEY', 'FIND', 'SEEK', 'SOLVE', 'OPEN', 'LOCK', 'DOOR',
    'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE',
    'DIAGONAL', 'DIAG', 'COLUMN', 'ROW', 'GRID', 'SQUARE',
    # Old English / Runeglish
    'THINE', 'THEE', 'THOU', 'HATH', 'DOTH', 'FORTH', 'HENCE', 'THUS', 'YEA', 'NAY',
    'WYRD', 'FATE', 'DOOM', 'RECK', 'WEAL', 'WOE', 'BANE', 'BOON',
    # More specific
    'THEME', 'THESE', 'THEM', 'THEN', 'THERE', 'THEY', 'THOSE',
    'HOME', 'COME', 'SOME', 'DOME', 'ROME', 'TOME', 'NOME', 'GNOME',
    'LONER', 'OWNER', 'TONER',
    'FALTER', 'FALSE', 'FAULT',
]

found = []
for word in english_words:
    idx = INTERLEAVED.find(word)
    if idx >= 0:
        found.append((idx, word))

found.sort()
print("\nWords found with positions:")
for idx, word in found:
    # Show context
    start = max(0, idx - 3)
    end = min(len(INTERLEAVED), idx + len(word) + 3)
    context = INTERLEAVED[start:end]
    marker = "..." if start > 0 else ""
    marker2 = "..." if end < len(INTERLEAVED) else ""
    print(f"  {idx:3}: {word:10} in '{marker}{context}{marker2}'")

# Try to segment manually based on found words
print("\n=== Manual Segmentation Attempt ===")
print("Looking at: HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOME...")
print()
print("Possible reads:")
print("  H-F-O-F-E-E-E-O-D-E-O-M-E-T-B-I-D-A-M-S-E-F-A-L-T-THE-LONE-TN-HE-R-A-A-U-I-O-A-E-T-I-O-A-E-A-Y-O-M-E...")
print("  Or: HE F OF E EE ODE OME TB ID AM SEF ALT THE LONE TN HER AA UIO AET IOA EAY OME...")
print()

# The presence of 'THE LONE' is intriguing
# Let me check if there's a pattern

print("=== Checking for 'THE LONE' context ===")
idx = INTERLEAVED.find('THELONE')
context = INTERLEAVED[idx-10:idx+20]
print(f"Context around THELONE: '{context}'")

# Could this be: "THE LONE ... THE ... "?
print("\n=== Looking for repeated THE ===")
pos = 0
while True:
    idx = INTERLEAVED.find('THE', pos)
    if idx == -1:
        break
    context = INTERLEAVED[max(0,idx-5):min(len(INTERLEAVED),idx+10)]
    print(f"  THE at {idx}: '{context}'")
    pos = idx + 1

# What about reading as Runeglish (with digraphs)?
print("\n=== Runeglish Digraph Reading ===")
# In Runeglish, TH, NG, EA, OE, AE, EO, IA are single characters
runeglish_digraphs = ['TH', 'NG', 'EA', 'OE', 'AE', 'EO', 'IA']

def tokenize_runeglish(text):
    tokens = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in runeglish_digraphs:
            tokens.append(text[i:i+2])
            i += 2
        else:
            tokens.append(text[i])
            i += 1
    return tokens

tokens = tokenize_runeglish(INTERLEAVED)
print(f"Token count: {len(tokens)}")
print(f"Tokens: {' '.join(tokens[:40])}...")

# Count digraphs
digraph_count = sum(1 for t in tokens if len(t) == 2)
print(f"Digraphs: {digraph_count}")
print(f"Singles: {len(tokens) - digraph_count}")

# The stream might be the key with transposition needed
print("\n=== Hypothesis ===")
print("The interleaved stream contains:")
print("  - THE (at position 25)")
print("  - LONE (at position 28)")
print("  - HE (at positions 31, 75)")
print()
print("'THE LONE' could be 'THE LONE [something]' or 'ALONE' split")
print("This is promising but needs further decryption or rearrangement.")

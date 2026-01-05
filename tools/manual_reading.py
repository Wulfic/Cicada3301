#!/usr/bin/env python3
"""
Analyze the most promising results from Page 28.
Try to manually segment and read the text.
"""

RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

PAGE28 = "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ"

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i % 29] for i in indices)

# Most promising results
BEST_RESULTS = [
    {'rot': 21, 'off': 82, 'the_count': 5, 'desc': 'Most THE occurrences'},
    {'rot': 1, 'off': 73, 'the_count': 4, 'desc': 'Starts with THR'},
    {'rot': 21, 'off': 17, 'the_count': 4, 'desc': 'Has ISTHE pattern'},
    {'rot': 1, 'off': 14, 'the_count': 4, 'desc': 'Has THEOFF THE'},
    {'rot': 15, 'off': 90, 'score': 91.5, 'desc': 'High score, starts with TO'},
    {'rot': 16, 'off': 52, 'score': 85.0, 'desc': 'Starts with AN'},
    {'rot': 11, 'off': 47, 'score': 71.0, 'desc': 'Starts with AN, has ANGNGTHE'},
]

print("=" * 80)
print("📖 MANUAL READING ANALYSIS - PAGE 28")
print("=" * 80)

indices = unicode_to_indices(PAGE28)

for result in BEST_RESULTS:
    rot = result['rot']
    off = result['off']
    
    decrypted = []
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + off) % len(MASTER_KEY)]
        dec = (idx ^ key_val ^ rot) % 29
        decrypted.append(dec)
    
    text = indices_to_text(decrypted)
    
    print(f"\n{'='*60}")
    print(f"XOR rot={rot}, off={off}: {result['desc']}")
    print(f"{'='*60}")
    print(f"Full text ({len(text)} chars):")
    print(text)
    
    # Try to manually segment
    print(f"\n🔤 Attempting segmentation:")
    
    # Common word patterns to look for
    words = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'FOR', 'BE', 'AS', 'AT', 
             'BY', 'OR', 'AN', 'SO', 'IF', 'ON', 'NO', 'WE', 'HE', 'ME', 'MY',
             'THEY', 'THAT', 'THIS', 'WITH', 'FROM', 'HAVE', 'WILL', 'YOUR',
             'THEIR', 'WHAT', 'WHEN', 'WHICH', 'THERE', 'EACH', 'SOME', 'THEM',
             'ARE', 'WAS', 'WERE', 'NOT', 'BUT', 'ALL', 'ONE', 'TWO', 'OUT',
             'HIM', 'HIS', 'HER', 'SHE', 'YOU', 'WHO', 'HOW', 'NOW', 'OLD', 'NEW']
    
    text_upper = text.upper()
    
    # Find positions of all words
    found = []
    for word in words:
        pos = 0
        while True:
            pos = text_upper.find(word, pos)
            if pos == -1:
                break
            found.append((pos, pos + len(word), word))
            pos += 1
    
    found.sort()
    
    # Try to build a coherent segmentation
    print(f"Words found: {[(w[0], w[2]) for w in found]}")
    
    # Segment character by character
    i = 0
    segments = []
    current = ""
    while i < len(text_upper):
        # Check if any word starts at this position
        matching_words = [w for w in found if w[0] == i]
        if matching_words:
            if current:
                segments.append(current.lower())
                current = ""
            # Take the longest matching word
            longest = max(matching_words, key=lambda w: len(w[2]))
            segments.append(longest[2])
            i = longest[1]
        else:
            current += text_upper[i]
            i += 1
    if current:
        segments.append(current.lower())
    
    # Print segmented version
    print(f"\nSegmented: {' '.join(segments)}")
    
    # Calculate what percentage is recognized words
    recognized = sum(len(s) for s in segments if s.upper() in words)
    total = len(text_upper)
    print(f"Word coverage: {recognized}/{total} ({100*recognized/total:.1f}%)")

# Now try to read the best one more carefully
print("\n" + "=" * 80)
print("🔎 DEEP ANALYSIS OF BEST RESULT")
print("=" * 80)

# Best: rot=21, off=82 - has 5 THE occurrences
rot, off = 21, 82
decrypted = []
for i, idx in enumerate(indices):
    key_val = MASTER_KEY[(i + off) % len(MASTER_KEY)]
    dec = (idx ^ key_val ^ rot) % 29
    decrypted.append(dec)

text = indices_to_text(decrypted)
print(f"\nText: {text}")

# Find all THE positions
text_upper = text.upper()
the_positions = []
pos = 0
while True:
    pos = text_upper.find('THE', pos)
    if pos == -1:
        break
    the_positions.append(pos)
    pos += 1

print(f"\n'THE' found at positions: {the_positions}")

# Extract text between THE occurrences
print("\nText segments around 'THE':")
for i, pos in enumerate(the_positions):
    start = max(0, pos - 10)
    end = min(len(text_upper), pos + 13)
    context = text_upper[start:end]
    print(f"  [{pos:3d}]: ...{context}...")

# Try reading with different word boundaries
print("\n" + "=" * 80)
print("📚 POTENTIAL READINGS")
print("=" * 80)

# The text: FMTHEOAUYGTHAUAOTHDFTHRSTHEOYUIAJTLEOMFOEYLYTDIANGEAMFNYLAETHMGBXHNGEAUDPBIHEOEA

print("\nReading attempt 1 (naive splits on THE):")
splits = text_upper.split('THE')
print(f"Splits: {splits}")

print("\nReading attempt 2 (trying to find meaning):")
# FMTHEOAUYGTHAUAOTHDFTHRSTHEOYUIAJTLEOMFOEYLYTDIANGEAMFNYLAETHMGBXHNGEAUDPBIHEOEA
# F M THE O A U Y G TH A U A O TH D F TH R S THE O Y U I A J T L E O M F O E Y L Y T D I A NG E A M F N Y L A E TH M G B X H NG E A U D P B I H E O E A

# Let's try different interpretations
interpretations = [
    "F M THE O A U Y G TH A U A O TH D F TH R S THE O Y U I A ...",
    "FM THE O AU Y G TH AU A O TH DF TH RS THE OY U IA ...",
    "F M THE OAU Y G THAU A O TH DF THR S THE OY U IA JT LE OM FOE Y LY T DI A NG EAM F NY LA E THM GB XH NGE AU DP BI HE OE A",
]

for interp in interpretations:
    print(f"  {interp}")

print("\n✅ Analysis complete!")

# Also check if the text contains any Cicada-related words
print("\n" + "=" * 80)
print("🔍 CHECKING FOR CICADA-RELATED TERMS")
print("=" * 80)

cicada_words = ['PRIME', 'PRIMES', 'CICADA', 'TRUTH', 'WISDOM', 'DIVINE', 'SACRED', 
                'LIGHT', 'DARKNESS', 'PATH', 'SEEK', 'FIND', 'WITHIN', 'WITHOUT',
                'ABOVE', 'BELOW', 'KNOWLEDGE', 'POWER', 'LOVE', 'SELF', 'MIND',
                'LIBER', 'PRIMUS', 'INSTAR', 'EMERGE', 'PILGRIM', 'JOURNEY']

for result in BEST_RESULTS[:3]:
    rot = result['rot']
    off = result['off']
    
    decrypted = []
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + off) % len(MASTER_KEY)]
        dec = (idx ^ key_val ^ rot) % 29
        decrypted.append(dec)
    
    text = indices_to_text(decrypted).upper()
    
    found_cicada = []
    for word in cicada_words:
        if word in text:
            found_cicada.append(word)
    
    if found_cicada:
        print(f"rot={rot}, off={off}: Found {found_cicada}")
    else:
        print(f"rot={rot}, off={off}: No Cicada terms found")

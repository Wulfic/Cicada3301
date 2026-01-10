"""
Page 20 - Deep Analysis of 2x83 Grid Reading
==============================================
The 2x83 column reading reveals "THE LONE" - let's analyze it deeply
"""

# The 166-stream in 2x83 grid reading
STREAM_2x83 = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"

print("2x83 Grid Reading Analysis")
print("=" * 50)
print(f"Full text ({len(STREAM_2x83)} chars):")
print(STREAM_2x83)
print()

# Look for words manually with sliding window
print("\n=== WORD DETECTION ===")

# Extended word list including Old English
WORDS = [
    # Modern English
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'SAID', 'WOULD', 'ABOUT',
    'DEATH', 'DEAD', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'KNOW', 'LONE', 'ALONE', 'SELF',
    'MEAN', 'PRIME', 'SACRED', 'WISDOM', 'DEOR', 'SONG', 'REAPER', 'AEON', 'SEEKER',
    'MET', 'BID', 'SAY', 'SEE', 'HO', 'OH', 'AH', 'LO', 'YET', 'ERE', 'ART', 'WAS',
    'ODE', 'FEE', 'OFT', 'ALT', 'AGE', 'ATE', 'EAT', 'EYE', 'ICE', 'ACE',
    
    # Short words
    'A', 'I', 'O', 'AM', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN',
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
    
    # Digraphs (runeglish)
    'TH', 'EO', 'NG', 'OE', 'AE', 'EA', 'IA',
    
    # Old English / Anglo-Saxon
    'EODE', 'MEOD', 'WYRD', 'WEALD', 'HELM', 'WEARD', 'HLAFORD', 'FREOND',
    'FEOND', 'GODSPEL', 'SAWOL', 'HEOFON', 'FOLC', 'CYNING', 'EALDOR',
    'SEFA', 'MOD', 'HEORTE', 'LICHAMA', 'SAWLE', 'GAST', 'WITA', 'EAGE',
    'EARE', 'MUTHA', 'TUNGE', 'HAND', 'FOT', 'HEAFOD', 'BREOST',
    'THONE', 'THANE', 'THAW', 'THAN', 'THAT', 'THINE', 'THEE', 'THOU',
    
    # Words from Deor poem
    'WELUND', 'WURMAN', 'WRAECES', 'CUNNADE', 'ANHYDIG', 'EORL', 'EARFOTHA',
    'DREAG', 'GESITHE', 'SORGE', 'LONGATH', 'WINTERCEALDE', 'WRAECE', 'WEAN',
    'NITHAD', 'SWONCRE', 'SEONOBENDE', 'SYLLAN', 'OFEREODE', 'THISSES',
    
    # Potential keywords
    'HIDDEN', 'SECRET', 'CIPHER', 'CODE', 'KEY', 'RUNE', 'RUNIC', 'PRIMUS',
    'CICADA', 'THREE', 'THIRTEEN', 'PRIME', 'NUMBER', 'PATTERN',
]

# Sort by length (longer first for greedy matching)
WORDS.sort(key=len, reverse=True)

text = STREAM_2x83.upper()
found_positions = []

for word in WORDS:
    pos = 0
    while True:
        idx = text.find(word, pos)
        if idx == -1:
            break
        found_positions.append((idx, idx + len(word), word))
        pos = idx + 1

# Sort by position
found_positions.sort()
print(f"Found {len(found_positions)} word occurrences:")
for start, end, word in found_positions:
    if len(word) >= 2:  # Skip single letters for readability
        context = text[max(0, start-5):min(len(text), end+5)]
        print(f"  [{start:3d}-{end:3d}] {word:12s} in ...{context}...")

# Try parsing with non-overlapping words
print("\n=== NON-OVERLAPPING PARSE ===")

def greedy_parse(text, words):
    """Greedy parsing from left to right"""
    result = []
    i = 0
    while i < len(text):
        found = False
        for word in words:  # Already sorted by length desc
            if text[i:i+len(word)] == word:
                result.append(word)
                i += len(word)
                found = True
                break
        if not found:
            result.append(text[i])
            i += 1
    return result

parsed = greedy_parse(text, WORDS)
print(f"Greedy parse: {' '.join(parsed)}")

# Now let's look at specific segments
print("\n=== SEGMENT ANALYSIS ===")

# The key phrase area around "THE LONE"
idx = text.find("THELONE")
if idx >= 0:
    context = text[max(0, idx-20):min(len(text), idx+25)]
    print(f"Around 'THE LONE': {context}")
    
    # Analyze characters before and after
    before = text[max(0, idx-15):idx]
    after = text[idx+7:min(len(text), idx+22)]
    print(f"  Before: '{before}'")
    print(f"  After:  '{after}'")

# Look for potential sentence structure
print("\n=== POTENTIAL SENTENCE STRUCTURE ===")

# Try to segment into potential words
segments = []
i = 0
while i < len(text):
    # Try to find longest word match
    best = None
    for length in range(8, 0, -1):  # Max word length 8
        candidate = text[i:i+length]
        if candidate in WORDS:
            best = candidate
            break
    
    if best:
        segments.append(best)
        i += len(best)
    else:
        segments.append(text[i])
        i += 1

# Join with spaces for readability
segmented = ' '.join(segments)
print(f"Segmented: {segmented[:200]}...")

# Count recognized vs unrecognized
recognized = sum(1 for s in segments if len(s) > 1)
unrecognized = sum(1 for s in segments if len(s) == 1)
print(f"\nRecognized words: {recognized}")
print(f"Unrecognized chars: {unrecognized}")

# Look for runeglish digraph patterns
print("\n=== RUNEGLISH DIGRAPH ANALYSIS ===")

digraphs = ['TH', 'EO', 'NG', 'OE', 'AE', 'EA', 'IA']
for dg in digraphs:
    count = text.count(dg)
    if count > 0:
        print(f"  {dg}: {count} occurrences")

# Replace digraphs with single tokens
def runeglish_tokens(text):
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in digraphs:
            result.append(text[i:i+2])
            i += 2
        else:
            result.append(text[i])
            i += 1
    return result

tokens = runeglish_tokens(text)
print(f"\nAs runeglish tokens ({len(tokens)} tokens):")
print(''.join(f"[{t}]" if len(t) > 1 else t for t in tokens[:50]) + "...")

# Try reading with known structure
print("\n=== MANUAL INTERPRETATION ===")

# Based on "THE LONE" being clear, let's try to read around it
manual_parse = """
HFO FEE EOD EO ME T BID AM SELF ALT THE LONE TN HER A AU IO AE TIO AE AY OME YC FGY W TEX JEJ CDC BLO TEP TSA YF THOF BNG IG A DO T CHDH WWY GGL DAHRC L FE PESP MCX MME OSX YE EO OOO EANE EIO TCY THWY FOM TTH HTT HGY EWHS GMW
"""

# Highlight readable parts
readable_words = ['FEE', 'ME', 'BID', 'AM', 'SELF', 'ALT', 'THE', 'LONE', 'HER', 'AY', 'OME', 'BLO', 'DO']
print("Potential reading (manually segmented):")
print(manual_parse.strip())
print(f"\nClearly readable: {[w for w in readable_words if w in manual_parse]}")

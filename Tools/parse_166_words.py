"""
Parse the 166-stream and interleaved version with proper digraph handling
to find readable words
"""

STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Create interleaved version
first_half = STREAM_166[:83]
second_half = STREAM_166[83:]
INTERLEAVED = "".join(first_half[i] + second_half[i] for i in range(83))

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# All possible digraphs in the Gematria Primus
DIGRAPHS = {'TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA'}

def parse_with_digraphs(text):
    """Parse text, recognizing GP digraphs"""
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in DIGRAPHS:
            result.append(text[i:i+2])
            i += 2
        else:
            result.append(text[i])
            i += 1
    return result

def find_words(text, words):
    """Find all occurrences of words in text"""
    found = {}
    for word in words:
        pos = 0
        positions = []
        while True:
            idx = text.find(word, pos)
            if idx == -1:
                break
            positions.append(idx)
            pos = idx + 1
        if positions:
            found[word] = positions
    return found

# Common English words
COMMON_WORDS = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'OLD', 'SEE',
    'WAY', 'WHO', 'BOY', 'DID', 'GET', 'HIM', 'INTO', 'JUST', 'MADE', 'MANY', 'SOME',
    'THEM', 'THEN', 'THERE', 'THESE', 'THEY', 'THIS', 'WILL', 'WITH', 'WOULD',
    'SELF', 'ALT', 'ALTER', 'ALONE', 'LONE', 'DEATH', 'DEAD', 'REAPER', 'AEON', 'ETHER',
    'BEING', 'WITHIN', 'PATH', 'PRIME', 'SACRED', 'WISDOM', 'CIPHER', 'KEY', 'MEAN',
    'DIAG', 'DIAGONAL', 'SIX', 'MET', 'MEET', 'HER', 'HE', 'SHE', 'WE', 'ME', 'BE',
    'AM', 'I', 'OF', 'TO', 'IN', 'IS', 'IT', 'AT', 'OR', 'AS', 'NO', 'SO', 'IF',
    'AN', 'ON', 'UP', 'BY', 'MY', 'DO', 'GO', 'WE', 'THEE', 'THOU',
    'ODE', 'SAY', 'BID', 'ASK', 'ALL', 'YEA', 'NAY', 'DEOR', 'FATE',
]

print("="*70)
print("WORD FINDING IN 166-STREAM AND INTERLEAVED VERSION")
print("="*70)

print(f"\nOriginal 166-stream:")
print(f"  {STREAM_166}")
tokens = parse_with_digraphs(STREAM_166)
print(f"  With digraphs: {' '.join(tokens[:30])}...")

print(f"\nInterleaved version:")
print(f"  {INTERLEAVED}")
tokens_inter = parse_with_digraphs(INTERLEAVED)
print(f"  With digraphs: {' '.join(tokens_inter[:30])}...")

# Find words
print("\n" + "="*70)
print("WORDS FOUND IN ORIGINAL 166-STREAM")
print("="*70)
found = find_words(STREAM_166, COMMON_WORDS)
for word, positions in sorted(found.items(), key=lambda x: -len(x[0])):
    print(f"  '{word}' at positions: {positions}")

print("\n" + "="*70)
print("WORDS FOUND IN INTERLEAVED VERSION")
print("="*70)
found_inter = find_words(INTERLEAVED, COMMON_WORDS)
for word, positions in sorted(found_inter.items(), key=lambda x: -len(x[0])):
    print(f"  '{word}' at positions: {positions}")

# Try to manually parse the interleaved version for meaning
print("\n" + "="*70)
print("MANUAL PARSING OF INTERLEAVED")
print("="*70)

print(f"\nFull text: {INTERLEAVED}")
print(f"\nBreaking at found words:")

# Find significant words and their positions
key_words = ['THELONET', 'SELFALT', 'THELONE', 'SELFALTE', 'HER', 'MET', 'THE']
for word in key_words:
    if word in INTERLEAVED:
        idx = INTERLEAVED.find(word)
        print(f"  '{word}' at position {idx}")
        context_start = max(0, idx - 10)
        context_end = min(len(INTERLEAVED), idx + len(word) + 10)
        print(f"    Context: ...{INTERLEAVED[context_start:context_end]}...")

# Look for word boundaries using frequency analysis
print("\n" + "="*70)
print("ATTEMPTING WORD SEGMENTATION")
print("="*70)

# Simple greedy word segmentation
def segment_greedy(text, vocabulary):
    """Try to segment text into known words (greedy, longest match)"""
    vocab = sorted(vocabulary, key=lambda x: -len(x))  # Longest first
    result = []
    remaining = text
    
    while remaining:
        matched = False
        for word in vocab:
            if remaining.startswith(word):
                result.append(word)
                remaining = remaining[len(word):]
                matched = True
                break
        if not matched:
            # Take single character
            result.append(remaining[0])
            remaining = remaining[1:]
    
    return result

# Try segmentation on portions
segments = segment_greedy(INTERLEAVED, COMMON_WORDS)
print(f"Greedy segmentation: {' | '.join(segments[:50])}...")

# Count meaningful words
meaningful = [s for s in segments if len(s) > 1 and s in COMMON_WORDS]
print(f"\nMeaningful words found: {meaningful}")

# Look for patterns in spacing
print("\n" + "="*70)
print("LOOKING FOR 'THE LONE' CONTEXT")
print("="*70)

idx = INTERLEAVED.find('THELONE')
if idx != -1:
    print(f"Found 'THELONE' at position {idx}")
    print(f"Full context (pos {max(0,idx-20)} to {idx+30}):")
    print(f"  '{INTERLEAVED[max(0,idx-20):idx+30]}'")
    
    # What comes before and after?
    before = INTERLEAVED[max(0,idx-30):idx]
    after = INTERLEAVED[idx+7:idx+37]
    print(f"\n  Before THELONE: '{before}'")
    print(f"  After THELONE:  '{after}'")

# Maybe the text needs Caesar shift?
print("\n" + "="*70)
print("TRYING CAESAR SHIFTS ON INTERLEAVED")
print("="*70)

GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

def to_indices(text):
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in GP_MAP:
            result.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            result.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return result

def to_text(indices):
    return "".join(INV_MAP[i % 29] for i in indices)

inter_indices = to_indices(INTERLEAVED)

for shift in range(29):
    shifted = [(i - shift) % 29 for i in inter_indices]
    text = to_text(shifted)
    
    # Count English words
    word_count = sum(1 for w in COMMON_WORDS if w in text and len(w) > 2)
    if word_count >= 5:
        print(f"Shift {shift}: {word_count} words found")
        print(f"  '{text[:60]}...'")

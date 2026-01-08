"""
Deep investigation of interleaved streams - especially the 4-stream pattern
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

OLD_ENGLISH_WORDS = [
    'THE', 'THAT', 'THIS', 'THESE', 'THOSE', 'THERE', 'THEN', 'THUS',
    'THING', 'THINGS', 'THOUGHT', 'TRUTH',
    'DOETH', 'GOETH', 'HATH', 'DOTH', 'SAITH', 'COMETH', 'GIVETH',
    'TAKETH', 'MAKETH', 'SEEKETH', 'FINDETH', 'KNOWETH', 'SPEAKETH',
    'HEARETH', 'SEETH', 'BELIEVETH', 'LIVETH', 'LOVETH',
    'EARTH', 'HEAVEN', 'DEATH', 'BREATH', 'PATH',
    'THOU', 'THEE', 'THY', 'THINE', 'YE', 'WE', 'I', 'A',
    'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT', 'SO',
    'WITH', 'FROM', 'FOR', 'ALL', 'NOT', 'BUT', 'ARE', 'WAS',
    'HAVE', 'WILL', 'SHALL', 'MUST',
    'HEART', 'MIND', 'SOUL', 'SPIRIT',
    'WISDOM', 'DIVINE', 'DIVINITY', 'EMERGE', 'SACRED', 'PRIMES',
    'WITHIN', 'WITHOUT', 'FIND', 'SEEK', 'KNOW', 'BEING',
    'NOTHING', 'SOMETHING', 'EVERYTHING',
    'AE', 'EA', 'EO', 'IA', 'OE', 'NG',
    'AN', 'ETH', 'ERE', 'OUR', 'OWN',
]

def parse_to_runes(text):
    text = text.upper().replace('/', '').replace(' ', '')
    runes = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in DIGRAPHS:
                runes.append(digraph)
                i += 2
                continue
        if text[i].isalpha():
            runes.append(text[i])
        i += 1
    return runes

def find_words(text):
    """Find all known words in text"""
    found = []
    for word in OLD_ENGLISH_WORDS:
        if word in text and len(word) > 2:
            count = text.count(word)
            found.append((word, count))
    return sorted(found, key=lambda x: -len(x[0]))

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)
N = len(runes)

print("="*70)
print("4-STREAM DEEP ANALYSIS")
print("="*70)

# Extract 4 streams
streams = [[] for _ in range(4)]
for i, r in enumerate(runes):
    streams[i % 4].append(r)

for s in range(4):
    text = ''.join(streams[s])
    words = find_words(text)
    print(f"\nStream {s} ({len(streams[s])} runes):")
    print(f"  Text: {text}")
    print(f"  Words: {words}")

print("\n" + "="*70)
print("TRYING TO RECOMBINE STREAMS IN DIFFERENT ORDERS")
print("="*70)

# Try all permutations of 4 streams
from itertools import permutations

best_score = 0
best_order = None
best_text = None

for perm in permutations([0, 1, 2, 3]):
    # Recombine streams in this order
    combined = []
    max_len = max(len(s) for s in streams)
    for i in range(max_len):
        for s_idx in perm:
            if i < len(streams[s_idx]):
                combined.append(streams[s_idx][i])
    
    text = ''.join(combined)
    words = find_words(text)
    score = sum(len(w) * count for w, count in words)
    
    if score > best_score:
        best_score = score
        best_order = perm
        best_text = text

print(f"Best order: {best_order}")
print(f"Best score: {best_score}")
print(f"Best text: {best_text[:100]}...")
print(f"Words: {find_words(best_text)}")

print("\n" + "="*70)
print("CHECKING SPECIFIC STREAM COMBINATIONS")
print("="*70)

# Maybe only 2 streams carry the message?
from itertools import combinations

for combo in combinations([0, 1, 2, 3], 2):
    # Merge just these two streams
    combined = []
    s1, s2 = combo
    for i in range(max(len(streams[s1]), len(streams[s2]))):
        if i < len(streams[s1]):
            combined.append(streams[s1][i])
        if i < len(streams[s2]):
            combined.append(streams[s2][i])
    
    text = ''.join(combined)
    words = find_words(text)
    score = sum(len(w) * count for w, count in words)
    
    if score > 50:
        print(f"\nStreams {combo}: Score {score}")
        print(f"  Text: {text[:60]}...")
        print(f"  Words: {words[:5]}")

print("\n" + "="*70)
print("TEST: STREAM 3 ALONE (had THAT, HATH, THEE)")
print("="*70)

stream3_text = ''.join(streams[3])
print(f"Stream 3: {stream3_text}")
print(f"Words: {find_words(stream3_text)}")

# Try to segment stream 3 into words
def greedy_segment(text, words):
    """Greedy word segmentation"""
    result = []
    i = 0
    while i < len(text):
        best_word = None
        best_len = 0
        for word in sorted(words, key=len, reverse=True):
            if text[i:].startswith(word):
                best_word = word
                best_len = len(word)
                break
        if best_word:
            result.append(f"[{best_word}]")
            i += best_len
        else:
            result.append(text[i])
            i += 1
    return ' '.join(result)

print(f"\nSegmented: {greedy_segment(stream3_text, OLD_ENGLISH_WORDS)}")

print("\n" + "="*70)
print("ANALYSIS: Check TH distribution per stream")
print("="*70)

for s in range(4):
    th_count = streams[s].count('TH')
    total = len(streams[s])
    print(f"Stream {s}: {th_count}/{total} TH runes ({th_count/total*100:.1f}%)")

# If TH is evenly distributed, it's probably part of the message
# If concentrated in certain streams, might be a pattern

print("\n" + "="*70)
print("TEST: What if TH marks stream boundaries?")
print("="*70)

# Split at TH positions and interleave
th_positions = [i for i, r in enumerate(runes) if r == 'TH']
print(f"TH positions: {th_positions[:20]}...")

# Segments between TH
segments = []
last = 0
for pos in th_positions:
    segment = runes[last:pos]
    if segment:
        segments.append(''.join(segment))
    last = pos + 1
segments.append(''.join(runes[last:]))

print(f"\nSegments between TH ({len(segments)}):")
for i, seg in enumerate(segments[:15]):
    print(f"  {i}: {seg}")

# Average segment length
avg_len = sum(len(s) for s in segments) / len(segments) if segments else 0
print(f"\nAverage segment length: {avg_len:.2f}")

# If segments are uniform length, TH might be a period/delimiter
from collections import Counter
len_dist = Counter(len(s) for s in segments)
print(f"Segment length distribution: {dict(sorted(len_dist.items()))}")

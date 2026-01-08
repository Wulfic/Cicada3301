"""
Investigate if TH at certain positions should be different runes
Key insight: Stream 3 has 42.2% TH - way too high
What if we replace some TH based on position?
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

GEMATRIA = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'D': 22,
    'OE': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

REVERSE_GEMATRIA = {v: k for k, v in GEMATRIA.items() if k not in ['K', 'ING', 'IO']}

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

def runes_to_text(rune_list):
    return ''.join(rune_list)

OLD_ENGLISH_WORDS = [
    'THE', 'THAT', 'THIS', 'THESE', 'THOSE', 'THERE', 'THEN', 'THUS',
    'THING', 'THINGS', 'THOUGHT', 'TRUTH', 'THROUGH',
    'DOETH', 'GOETH', 'HATH', 'DOTH', 'SAITH', 'COMETH', 'GIVETH',
    'TAKETH', 'MAKETH', 'SEEKETH', 'FINDETH', 'KNOWETH', 
    'EARTH', 'HEAVEN', 'DEATH', 'BREATH', 'PATH', 'WRATH',
    'THOU', 'THEE', 'THY', 'THINE', 'YE', 'WE', 'I', 'A',
    'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT', 'SO', 'OR',
    'WITH', 'FROM', 'FOR', 'ALL', 'NOT', 'BUT', 'ARE', 'WAS',
    'WISDOM', 'DIVINE', 'EMERGE', 'SACRED',
    'WITHIN', 'WITHOUT', 'FIND', 'SEEK', 'KNOW', 'BEING',
    'AN', 'ON', 'OUR', 'OWN', 'HIS', 'HER',
]

def score_words(text):
    """Count words found"""
    score = 0
    for word in OLD_ENGLISH_WORDS:
        if len(word) > 2:
            score += text.count(word) * len(word)
    return score

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)
N = len(runes)

original_text = runes_to_text(runes)
original_score = score_words(original_text)

print(f"Total runes: {N}")
print(f"Original score: {original_score}")

# Find TH positions by stream
th_positions = [i for i, r in enumerate(runes) if r == 'TH']
stream_th = {0: [], 1: [], 2: [], 3: []}
for pos in th_positions:
    stream_th[pos % 4].append(pos)

print(f"\nTH by stream:")
for s in range(4):
    print(f"  Stream {s}: {len(stream_th[s])} TH")

print("\n" + "="*70)
print("TEST: Replace TH at stream 3 positions (mod 4 = 3)")
print("="*70)

# TH has index 2. What common runes might it be replacing?
# O (3), R (4), A (24), E (18), N (9), I (10)

test_replacements = [
    ('O', 3),   # TH -> O (shift +1)
    ('R', 4),   # TH -> R (shift +2)
    ('N', 9),   # TH -> N (shift +7)
    ('I', 10),  # TH -> I (shift +8)
    ('S', 15),  # TH -> S (shift +13)
    ('T', 16),  # TH -> T (shift +14)
    ('E', 18),  # TH -> E (shift +16)
    ('A', 24),  # TH -> A (shift +22)
    (' ', -1),  # TH -> space (remove it)
]

for new_rune, new_val in test_replacements:
    modified = list(runes)
    
    # Replace TH at stream 3 positions only
    for pos in stream_th[3]:
        if new_rune == ' ':
            modified[pos] = ''  # Remove TH
        else:
            modified[pos] = new_rune
    
    text = ''.join(modified)
    score = score_words(text)
    
    if score >= original_score * 0.5:  # Show if at least 50% of original
        print(f"TH[mod4=3] -> {new_rune}: Score {score}")
        print(f"  Text: {text[:80]}...")
        
        # Show specific words
        words_found = []
        for word in OLD_ENGLISH_WORDS:
            if len(word) > 3 and word in text:
                words_found.append(f"{word}({text.count(word)})")
        if words_found:
            print(f"  Words: {words_found}")

print("\n" + "="*70)
print("TEST: Replace TH everywhere with space equivalent")
print("="*70)

# What if TH is a word separator?
segments = []
current = []
for r in runes:
    if r == 'TH':
        if current:
            segments.append(''.join(current))
            current = []
    else:
        current.append(r)
if current:
    segments.append(''.join(current))

# Try to match words
matched = []
unmatched = []
for seg in segments:
    found = False
    for word in OLD_ENGLISH_WORDS:
        if seg == word:
            matched.append(seg)
            found = True
            break
    if not found:
        unmatched.append(seg)

print(f"Segments matching words: {len(matched)}/{len(segments)}")
print(f"Matched: {matched[:20]}")
print(f"Unmatched examples: {unmatched[:20]}")

print("\n" + "="*70)
print("HYPOTHESIS: TH alternates between real TH and space/separator")
print("="*70)

# Every other TH is a separator?
for pattern in ['01', '10', '001', '010', '100', '011', '101', '110']:
    modified = list(runes)
    th_idx = 0
    
    for i, r in enumerate(modified):
        if r == 'TH':
            if pattern[th_idx % len(pattern)] == '1':
                modified[i] = ' '  # Replace with space
            th_idx += 1
    
    text = ''.join(modified)
    # Remove spaces and score
    text_no_space = text.replace(' ', '')
    score = score_words(text_no_space)
    
    # Count valid words in space-separated segments
    segments = [s for s in text.split() if s]
    word_count = sum(1 for s in segments if s in OLD_ENGLISH_WORDS)
    
    if word_count > 5:
        print(f"Pattern {pattern}: {word_count} words matched")
        print(f"  Segments: {segments[:15]}...")

print("\n" + "="*70)
print("TEST: What if TH+vowel = word, lone TH = separator?")
print("="*70)

# Look at what follows each TH
th_contexts = []
for i, r in enumerate(runes):
    if r == 'TH':
        next_r = runes[i+1] if i+1 < N else None
        th_contexts.append((i, next_r))

# TH followed by vowel = keep as word
# TH followed by consonant = maybe separator
vowels = ['A', 'E', 'I', 'O', 'U', 'Y', 'EA', 'EO', 'AE', 'IA', 'OE']

th_vowel = [(i, n) for i, n in th_contexts if n in vowels]
th_cons = [(i, n) for i, n in th_contexts if n not in vowels and n]

print(f"TH + vowel: {len(th_vowel)} occurrences")
print(f"TH + consonant: {len(th_cons)} occurrences")

# Replace TH+consonant with just the consonant (remove TH)
modified = list(runes)
removed_positions = [i for i, n in th_cons]
for pos in sorted(removed_positions, reverse=True):
    modified.pop(pos)

text = ''.join(modified)
print(f"\nWith TH+consonant THs removed:")
print(f"  Text ({len(modified)} runes): {text[:80]}...")
print(f"  Score: {score_words(text)}")

# Try the opposite
modified = list(runes)
for i, n in th_cons:
    modified[i] = ' '

text = ''.join(modified)
print(f"\nWith TH+consonant replaced by space:")
print(f"  Text: {text[:80]}...")

"""
Attempt to segment Page 0 output using Old English dictionary and word patterns
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

GEMATRIA = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'D': 22,
    'OE': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

def parse_to_runes(text):
    """Convert text to rune list"""
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

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)
print(f"Total runes: {len(runes)}")

# Extended Old English / Cicada vocabulary
OLD_ENGLISH_WORDS = [
    # Articles and pronouns
    'THE', 'A', 'AN', 'I', 'WE', 'YE', 'THEE', 'THOU', 'THY', 'THINE',
    # Common Old English
    'THAT', 'THIS', 'THESE', 'THOSE', 'THERE', 'THEN', 'THUS', 'THENCE',
    'THING', 'THINGS', 'THROUGH', 'THOUGHT', 'THOUGHTS',
    # Verb forms (-ETH endings)
    'DOETH', 'GOETH', 'HATH', 'DOTH', 'SAITH', 'COMETH', 'GIVETH',
    'TAKETH', 'MAKETH', 'SEEKETH', 'FINDETH', 'KNOWETH', 'SPEAKETH',
    'HEARETH', 'SEETH', 'BELIEVETH', 'LIVETH', 'LOVETH', 'MOVETH',
    'LEARNETH', 'LEARETH', 'TEACHETH', 'REACHETH', 'REMAINETH',
    # Nature/cosmic
    'EARTH', 'HEAVEN', 'DEATH', 'BREATH', 'HEARTH', 'PATH', 'WRATH',
    'NORTH', 'SOUTH', 'BENEATH', 'TRUTH', 'YOUTH', 'GROWTH',
    # Cicada themes
    'DIVINITY', 'DIVINE', 'WISDOM', 'EMERGE', 'INSTAR', 'PILGRIM',
    'SACRED', 'PRIMES', 'TOTIENT', 'ENCRYPT', 'CIRCUMFERENCE',
    'WITHIN', 'WITHOUT', 'LOSS', 'FIND', 'SEEK', 'KNOW', 'BEING',
    'CONSUME', 'PRESERVE', 'ADHERE', 'SHED', 'SURFACE', 'TUNNEL',
    # Old English common
    'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT', 'SO', 'OR',
    'IF', 'ON', 'FOR', 'BY', 'WITH', 'FROM', 'ARE', 'WAS', 'NOT', 'ALL',
    'HAVE', 'HAD', 'HAS', 'WILL', 'CAN', 'MAY', 'SHALL', 'MUST', 'SHOULD',
    'THEIR', 'WHAT', 'WHEN', 'WHERE', 'WHICH', 'WHO', 'WHOSE', 'WHY', 'HOW',
    # Body/soul
    'HEART', 'MIND', 'SOUL', 'BODY', 'SPIRIT', 'FLESH', 'BONE',
    # Actions
    'COME', 'GO', 'SEE', 'HEAR', 'SPEAK', 'THINK', 'FEEL', 'KNOW',
    'LEARN', 'TEACH', 'GIVE', 'TAKE', 'MAKE', 'FIND', 'SEEK', 'KEEP',
    # Single runes that are words
    'O', 'AE', 'EA', 'IA', 'EO', 'OE',  # Digraphs as words
    # -ING forms
    'BEING', 'DOING', 'GOING', 'COMING', 'SEEING', 'KNOWING',
    'SEEKING', 'FINDING', 'LEARNING', 'EMERGING', 'TUNNELING',
    # More common
    'NOTHING', 'SOMETHING', 'EVERYTHING', 'ANYTHING',
    'ONE', 'OWN', 'OUR', 'OUT',
    'HE', 'SHE', 'HIS', 'HER', 'THEM',
    # -TH nouns
    'WEALTH', 'HEALTH', 'STEALTH', 'LENGTH', 'STRENGTH', 'DEPTH', 'WIDTH',
    # Verbs with prefixes
    'UNTO', 'UPON', 'INTO', 'ONTO', 'AMONG', 'ALONG', 'BEYOND',
    # Old English particles
    'ETH', 'EST', 'ERE', 'EAN', 'AEN', 'YEA', 'NAY',
]

# Add -ETH versions of common verbs
for base in ['DO', 'GO', 'HA', 'SA', 'CO', 'GI', 'TA', 'MA', 'SE', 'FI', 'KN', 'SP', 'HE', 'BE', 'LI', 'LO', 'MO', 'LE', 'TE', 'RE']:
    OLD_ENGLISH_WORDS.append(base + 'ETH')

# Normalize to uppercase
OLD_ENGLISH_WORDS = list(set([w.upper() for w in OLD_ENGLISH_WORDS]))

# Convert words to rune format
def word_to_runes(word):
    """Convert a word to its rune representation"""
    return parse_to_runes(word)

WORD_RUNES = {tuple(word_to_runes(w)): w for w in OLD_ENGLISH_WORDS}

# Try to find longest matching words
def find_words_greedy(rune_list):
    """Greedy word segmentation - find longest matching word at each position"""
    result = []
    i = 0
    while i < len(rune_list):
        best_word = None
        best_len = 0
        
        # Try lengths from longest to shortest
        for length in range(min(15, len(rune_list) - i), 0, -1):
            segment = tuple(rune_list[i:i+length])
            if segment in WORD_RUNES:
                best_word = WORD_RUNES[segment]
                best_len = length
                break
        
        if best_word:
            result.append(best_word)
            i += best_len
        else:
            result.append(rune_list[i])  # Single rune
            i += 1
    
    return result

print("="*70)
print("GREEDY WORD SEGMENTATION")
print("="*70)

words = find_words_greedy(runes)
print(f"Segmented ({len(words)} segments):")

# Group into lines for readability
line = []
for w in words:
    if isinstance(w, str) and len(w) > 1:
        line.append(f"[{w}]")
    else:
        line.append(w)
    if len(' '.join(line)) > 70:
        print(' '.join(line))
        line = []
if line:
    print(' '.join(line))

# Count identified words
identified_words = [w for w in words if isinstance(w, str) and len(w) > 1]
single_runes = [w for w in words if isinstance(w, str) and len(w) == 1]
print(f"\nIdentified words: {len(identified_words)}")
print(f"Single runes: {len(single_runes)}")
print(f"Word coverage: {sum(len(word_to_runes(w)) for w in identified_words) / len(runes) * 100:.1f}%")

# Show unique words found
unique_words = set(identified_words)
print(f"\nUnique words found ({len(unique_words)}): {sorted(unique_words)}")

# Try to read as sentence
print("\n" + "="*70)
print("POTENTIAL READING (words only)")
print("="*70)
print(' '.join(identified_words))

# Count THE specifically
the_count = identified_words.count('THE')
print(f"\n'THE' count: {the_count}")

print("\n" + "="*70)
print("PATTERN ANALYSIS: What follows each word?")
print("="*70)

# Build a simple n-gram model of word transitions
from collections import defaultdict
transitions = defaultdict(list)

for i in range(len(words) - 1):
    if isinstance(words[i], str) and len(words[i]) > 1:
        transitions[words[i]].append(words[i+1] if isinstance(words[i+1], str) else f"<{words[i+1]}>")

print("Word transitions (most common):")
for word in ['THE', 'THAT', 'DOETH', 'GOETH', 'AND', 'HATH']:
    if word in transitions:
        print(f"  {word} -> {transitions[word][:5]}")

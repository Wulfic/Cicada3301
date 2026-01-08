"""
Advanced word extraction using dynamic programming
Try to find the MAXIMUM coverage of known English/Old English words
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

# Comprehensive Old English / Cicada vocabulary
WORD_SET = {
    # The main articles and pronouns
    'THE', 'A', 'AN', 'I', 'WE', 'YE', 'THEE', 'THOU', 'THY', 'THINE', 'HE', 'SHE', 'IT',
    'THAT', 'THIS', 'THESE', 'THOSE', 'THEY', 'THEM', 'THEIR',
    'THERE', 'HERE', 'WHERE', 'WHEN', 'THEN', 'THUS', 'THENCE',
    'WHAT', 'WHICH', 'WHO', 'WHOM', 'WHOSE', 'WHY', 'HOW',
    
    # Verbs (-ETH endings)
    'DOETH', 'GOETH', 'HATH', 'DOTH', 'SAITH', 'COMETH', 'GIVETH', 'TAKETH', 'MAKETH',
    'SEEKETH', 'FINDETH', 'KNOWETH', 'SPEAKETH', 'HEARETH', 'SEETH', 'BELIEVETH',
    'LIVETH', 'LOVETH', 'MOVETH', 'LEARNETH', 'LEARETH', 'TEACHETH', 'REACHETH',
    'REMAINETH', 'LEADETH', 'BRINGETH', 'THINKETH', 'SEEMETH', 'BEGINNETH',
    
    # Nature/cosmic
    'EARTH', 'HEAVEN', 'DEATH', 'BREATH', 'HEARTH', 'PATH', 'WRATH', 'TRUTH', 'YOUTH',
    'NORTH', 'SOUTH', 'BENEATH', 'GROWTH', 'HEART', 'MIND', 'SOUL', 'SPIRIT', 'FLESH',
    'LIGHT', 'DARK', 'SUN', 'MOON', 'STAR', 'SKY', 'SEA', 'WIND', 'FIRE', 'WATER',
    
    # Cicada themes
    'DIVINITY', 'DIVINE', 'WISDOM', 'EMERGE', 'INSTAR', 'PILGRIM', 'SACRED', 'PRIMES',
    'TOTIENT', 'ENCRYPT', 'CIRCUMFERENCE', 'WITHIN', 'WITHOUT', 'LOSS', 'FIND', 'SEEK',
    'KNOW', 'BEING', 'NOTHING', 'SOMETHING', 'EVERYTHING', 'ANYTHING', 'CONSUME',
    'PRESERVE', 'ADHERE', 'SHED', 'SURFACE', 'TUNNEL', 'WARNING', 'BELIEVE', 'TEST',
    'EXPERIENCE', 'JOURNEY', 'END', 'BEGINNING', 'WAY', 'KOAN', 'PARABLE', 'INSTRUCTION',
    
    # Common words
    'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'BE', 'AS', 'AT', 'SO', 'OR', 'IF', 'ON', 'FOR',
    'BY', 'WITH', 'FROM', 'ARE', 'WAS', 'NOT', 'ALL', 'HAVE', 'HAD', 'HAS', 'WILL', 'CAN',
    'MAY', 'SHALL', 'MUST', 'SHOULD', 'WOULD', 'COULD', 'DO', 'DID', 'DOES', 'DONE',
    'GO', 'WENT', 'GONE', 'COME', 'CAME', 'GIVE', 'GAVE', 'TAKE', 'TOOK', 'MAKE', 'MADE',
    'SAY', 'SAID', 'SEE', 'SAW', 'SEEN', 'HEAR', 'HEARD', 'KNOW', 'KNEW', 'KNOWN',
    'THINK', 'THOUGHT', 'FEEL', 'FELT', 'FIND', 'FOUND', 'LEAVE', 'LEFT', 'TELL', 'TOLD',
    
    # -TH nouns
    'WEALTH', 'HEALTH', 'STEALTH', 'LENGTH', 'STRENGTH', 'DEPTH', 'WIDTH', 'THING', 'THINGS',
    
    # Prepositions and conjunctions
    'UNTO', 'UPON', 'INTO', 'ONTO', 'AMONG', 'ALONG', 'BEYOND', 'BEFORE', 'AFTER', 'THROUGH',
    'BETWEEN', 'ABOVE', 'BELOW', 'UNDER', 'OVER', 'AGAINST', 'TOWARD', 'TOWARDS',
    'BUT', 'YET', 'NOR', 'NEITHER', 'EITHER', 'BOTH', 'ALSO', 'TOO', 'ONLY', 'JUST',
    
    # Old English specific
    'ETH', 'EST', 'ERE', 'EAN', 'AEN', 'YEA', 'NAY', 'AYE', 'HITHER', 'THITHER', 'WHITHER',
    'HENCE', 'WHENCE', 'WHILST', 'WHEREFORE', 'THEREOF', 'HEREOF', 'WHEREBY',
    
    # Numbers and amounts
    'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',
    'FIRST', 'SECOND', 'THIRD', 'MANY', 'MUCH', 'MORE', 'MOST', 'FEW', 'SOME', 'ANY',
    'NONE', 'EACH', 'EVERY', 'OWN', 'OUR', 'YOUR', 'HIS', 'HER', 'ITS',
    
    # Single-letter words
    'A', 'I', 'O',
    
    # Digraph words
    'AE', 'EA', 'EO', 'IA', 'OE', 'NG',
}

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

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)
text = ''.join(runes)
N = len(text)

print(f"Text length: {N} characters")
print(f"Vocabulary size: {len(WORD_SET)} words")

# Dynamic programming for optimal word segmentation
def dp_segment(text, word_set, max_word_len=20):
    """
    Find segmentation that maximizes word coverage
    Returns (coverage_score, segmentation)
    """
    n = len(text)
    
    # dp[i] = (best_score, best_segmentation) for text[0:i]
    # Score = sum of lengths of matched words
    dp = [(0, [])] * (n + 1)
    dp[0] = (0, [])
    
    for i in range(1, n + 1):
        best = dp[i-1][0], dp[i-1][1] + [text[i-1]]  # Single char (not a word)
        
        for length in range(1, min(i, max_word_len) + 1):
            word = text[i-length:i]
            if word in word_set:
                prev_score, prev_seg = dp[i-length]
                # Score bonus for longer words
                word_score = len(word) if len(word) > 1 else 0.5
                new_score = prev_score + word_score
                if new_score > best[0]:
                    best = (new_score, prev_seg + [f"[{word}]"])
        
        dp[i] = best
    
    return dp[n]

print("\n" + "="*70)
print("DYNAMIC PROGRAMMING WORD SEGMENTATION")
print("="*70)

score, segmentation = dp_segment(text, WORD_SET)

print(f"Coverage score: {score:.1f}")
print(f"Total segments: {len(segmentation)}")

# Count word vs non-word segments
word_segs = [s for s in segmentation if s.startswith('[')]
nonword_segs = [s for s in segmentation if not s.startswith('[')]

print(f"Word segments: {len(word_segs)}")
print(f"Non-word characters: {len(nonword_segs)}")

# Calculate coverage
word_chars = sum(len(s) - 2 for s in word_segs)  # -2 for [ ]
print(f"Characters in words: {word_chars}/{N} ({word_chars/N*100:.1f}%)")

# Show segmentation
print(f"\nSegmentation:")
line = []
for seg in segmentation:
    line.append(seg)
    if len(' '.join(line)) > 70:
        print(' '.join(line))
        line = []
if line:
    print(' '.join(line))

# Extract just the words
words_only = [s[1:-1] for s in word_segs]
print(f"\n{'='*70}")
print("WORDS FOUND (in order)")
print("="*70)
print(' '.join(words_only))

# Analyze word frequency
from collections import Counter
word_freq = Counter(words_only)
print(f"\nMost common words:")
for word, count in word_freq.most_common(20):
    print(f"  {word}: {count}")

# Check non-word segments for patterns
print(f"\n{'='*70}")
print("NON-WORD SEGMENTS ANALYSIS")
print("="*70)

nonword_chars = ''.join(nonword_segs)
print(f"Non-word characters: {nonword_chars}")
print(f"Length: {len(nonword_chars)}")

# Are non-words concentrated or distributed?
nonword_positions = [i for i, seg in enumerate(segmentation) if not seg.startswith('[')]
print(f"Non-word positions: {nonword_positions[:30]}...")

# Check if non-words spell something
if len(nonword_chars) > 5:
    print(f"\nNon-word characters might spell: {nonword_chars}")
    # Check for hidden words
    for word in ['DIVINITY', 'WISDOM', 'EMERGE', 'SACRED', 'PRIMES', 'WARNING']:
        if word in nonword_chars:
            print(f"  Found hidden word: {word}")

print(f"\n{'='*70}")
print("POTENTIAL READING (filtering noise)")
print("="*70)

# Try to read as sentence, grouping nearby words
meaningful_words = [w for w in words_only if len(w) > 1]
print(' '.join(meaningful_words))

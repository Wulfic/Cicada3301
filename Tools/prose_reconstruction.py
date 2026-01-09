"""
Try to read Page 0 as prose by using TH as word delimiters
and finding the best interpretation
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

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
print(f"Total runes: {len(runes)}")

# Build segments between THE specifically (not just TH)
# Because THE is a common article that would start/end phrases

# Find all THE positions (TH followed by E)
the_positions = []
for i in range(len(runes) - 1):
    if runes[i] == 'TH' and runes[i+1] == 'E':
        the_positions.append(i)

print(f"THE positions: {the_positions}")
print(f"THE count: {len(the_positions)}")

# Create segments around THE
print("\n" + "="*70)
print("SEGMENTS AROUND 'THE'")
print("="*70)

for i, pos in enumerate(the_positions[:15]):
    # Get context before and after
    start = max(0, pos - 5)
    end = min(len(runes), pos + 7)
    before = ' '.join(runes[start:pos])
    after = ' '.join(runes[pos:end])
    print(f"THE #{i+1} at pos {pos}:")
    print(f"  ...{before} | THE | {' '.join(runes[pos+2:end])}...")

# Hypothesis: THE is the definite article, text follows pattern "THE [noun]..."
print("\n" + "="*70)
print("TRYING TO PARSE AS SENTENCES")
print("="*70)

# Look for patterns like "THE X" where X might be a noun
# Common Old English nouns: EARTH, HEAVEN, TRUTH, PATH, HEART, SOUL, MIND, THING

nouns = ['EARTH', 'HEAVEN', 'TRUTH', 'PATH', 'HEART', 'SOUL', 'MIND', 'THING', 
         'WISDOM', 'DIVINITY', 'LOSS', 'WAY', 'END', 'BEGINNING', 'DEATH', 'LIFE',
         'LIGHT', 'DARKNESS', 'WORLD', 'SPIRIT', 'BODY', 'FLESH', 'BLOOD']

# After each THE, look for potential nouns
text = ''.join(runes)
for pos in the_positions[:10]:
    char_pos = sum(len(r) for r in runes[:pos])  # Convert to char position
    remaining = text[char_pos+3:]  # Skip 'THE'
    
    for noun in nouns:
        if remaining.startswith(noun):
            print(f"Found: THE {noun} at position {pos}")
            break

# More sophisticated approach: sliding window
print("\n" + "="*70)
print("SCANNING FOR MEANINGFUL PHRASES")
print("="*70)

meaningful_patterns = [
    'THEART', 'THEEARTH', 'THEHEART', 'THETRUTH', 'THEPATH', 'THESOUL',
    'THEMIND', 'THETHING', 'THEWISDOM', 'THELOSS', 'THEWAY', 'THEEND',
    'DOETH', 'GOETH', 'HATH', 'SAITH', 'COMETH', 'FINDETH', 'SEEKETH',
    'THATWHICH', 'THOSEWHON', 'THOUHAST', 'THOUSHALT',
    'ANDTHE', 'OFTHE', 'INTHE', 'TOTHE', 'FORTHE', 'BYTHE', 'WITHTHE',
]

for pattern in meaningful_patterns:
    if pattern in text:
        idx = text.find(pattern)
        context = text[max(0, idx-10):idx+len(pattern)+10]
        print(f"Found '{pattern}' at {idx}: ...{context}...")

# Try to extract a reading using common word patterns
print("\n" + "="*70)
print("MANUAL PHRASE EXTRACTION")
print("="*70)

# Based on what we've seen, try to reconstruct:
# AETHATAEYETHESTHESTHEAEATHEOR...

# Parse this manually:
# AE THAT AE YE THE S THE S THE AE A THE OR NG THR O THI A S TH DIA...
# Could be: "Æ that Æ ye the...the...the..."

# Let's check if there's a pattern of meaningful fragments
text_str = ''.join(runes)

# Extract all 5+ letter words that are dictionary words
import re

VALID_WORDS = {'THERE', 'THING', 'EARTH', 'HEART', 'TRUTH', 'DEATH', 'DOETH', 'GOETH', 
               'HATH', 'THOU', 'THEE', 'THINE', 'THAT', 'THESE', 'THOSE', 'WHERE',
               'WHICH', 'WHOSE', 'THEIR', 'ABOUT', 'AFTER', 'AGAIN', 'ALONG', 'AMONG',
               'BEING', 'BELOW', 'COULD', 'EVERY', 'FOUND', 'GREAT', 'NEVER', 'OTHER',
               'SHALL', 'SHOULD', 'SINCE', 'STILL', 'THEIR', 'THERE', 'THESE', 'THINK',
               'THOSE', 'THREE', 'THROUGH', 'UNDER', 'UNTIL', 'WHERE', 'WHICH', 'WHILE',
               'WHOSE', 'WORLD', 'WOULD', 'YOUNG', 'WISDOM', 'SACRED', 'DIVINE'}

found_words = []
for length in range(5, 15):
    for i in range(len(text_str) - length + 1):
        word = text_str[i:i+length]
        if word in VALID_WORDS:
            found_words.append((word, i))

print("Found valid words (5+ letters):")
for word, pos in sorted(found_words, key=lambda x: x[1]):
    context = text_str[max(0,pos-5):pos+len(word)+5]
    print(f"  {word} at {pos}: ...{context}...")

print("\n" + "="*70)
print("RUNE-LEVEL INTERPRETATION") 
print("="*70)

# Print the first 50 runes with spaces
print("First 50 runes:")
print(' '.join(runes[:50]))

# Now try to group into meaningful chunks
# Looking for patterns like:
# AE = Æ (Old English letter)
# TH = Þ (thorn)
# EA, EO = vowel digraphs

print("\nAttempting Old English interpretation:")
print("AE = æ (ash), TH = þ (thorn)")

# Replace with symbols for readability
interpreted = []
for r in runes[:80]:
    if r == 'AE':
        interpreted.append('æ')
    elif r == 'TH':
        interpreted.append('þ')
    elif r == 'EA':
        interpreted.append('ea')
    elif r == 'EO':
        interpreted.append('eo')
    elif r == 'IA':
        interpreted.append('ia')
    elif r == 'OE':
        interpreted.append('œ')
    elif r == 'NG':
        interpreted.append('ŋ')
    else:
        interpreted.append(r.lower())

print(''.join(interpreted))

# Try adding spaces at likely word boundaries
# Words in Old English often end with: -ETH, -NG, -TH, vowels
print("\nWith guessed word boundaries:")
words = []
current = []
for r in interpreted:
    current.append(r)
    word = ''.join(current)
    # Check for word endings
    if word.endswith('eþ') or word in ['þe', 'a', 'æ', 'i', 'is', 'in', 'of', 'to', 'on', 'be']:
        words.append(word)
        current = []
    elif len(word) > 8:  # Force break long "words"
        words.append(word)
        current = []

if current:
    words.append(''.join(current))

print(' '.join(words))

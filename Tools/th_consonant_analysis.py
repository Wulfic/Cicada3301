"""
Investigate TH+consonant positions specifically
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
N = len(runes)

vowels = ['A', 'E', 'I', 'O', 'U', 'Y', 'EA', 'EO', 'AE', 'IA', 'OE']

print("="*70)
print("TH+CONSONANT ANALYSIS")
print("="*70)

th_cons_positions = []
for i in range(N-1):
    if runes[i] == 'TH':
        next_r = runes[i+1]
        if next_r not in vowels:
            th_cons_positions.append(i)
            
            # Get context
            start = max(0, i-3)
            end = min(N, i+5)
            context = ' '.join(runes[start:end])
            print(f"Position {i}: {context}")
            print(f"  TH followed by: {next_r}")

print(f"\nTotal TH+consonant: {len(th_cons_positions)}")
print(f"Positions: {th_cons_positions}")

# Check if these positions have a pattern
print(f"\n{'='*70}")
print("POSITION PATTERN ANALYSIS")
print("="*70)

# mod patterns
for mod in [2, 3, 4, 5, 7, 11, 13]:
    residues = [p % mod for p in th_cons_positions]
    from collections import Counter
    print(f"mod {mod}: {dict(Counter(residues))}")

# Differences between consecutive positions
diffs = [th_cons_positions[i+1] - th_cons_positions[i] for i in range(len(th_cons_positions)-1)]
print(f"\nGaps between TH+consonant positions: {diffs}")

print(f"\n{'='*70}")
print("HYPOTHESIS: These THs should be E (word endings)")
print("="*70)

# In Old English, -ETH is common verb ending
# What if some TH got shifted from E due to key error?

# Replace TH at these specific positions with E
modified = list(runes)
for pos in th_cons_positions:
    modified[pos] = 'E'

text = ''.join(modified)
print(f"Modified text (TH->E at consonant positions):")
print(f"  {text[:100]}...")

# Look for -ETH endings now
import re
eth_matches = re.findall(r'[A-Z]+ETH', text)
print(f"\n-ETH endings found: {eth_matches}")

# Score
OLD_ENGLISH_WORDS = ['THE', 'THAT', 'THERE', 'THEN', 'THING', 'DOETH', 'GOETH', 'HATH', 
                     'THOU', 'THEE', 'THY', 'EARTH', 'HEART', 'DEATH', 'TRUTH', 'WISDOM']
score = sum(text.count(w) * len(w) for w in OLD_ENGLISH_WORDS)
print(f"Score: {score}")

print(f"\n{'='*70}")
print("HYPOTHESIS: THR should be 'R', THD should be 'D', etc.")
print("="*70)

# What if TH before consonant is absorbing that consonant?
# THR -> R, THD -> D, etc.

# Check the consonants that follow TH
th_cons_letters = [runes[pos+1] for pos in th_cons_positions]
from collections import Counter
print(f"Consonants after TH: {Counter(th_cons_letters)}")

# Try replacing THX with just X
modified = list(runes)
to_remove = []
for pos in sorted(th_cons_positions, reverse=True):
    # Remove the TH, keep the consonant
    to_remove.append(pos)

for pos in to_remove:
    modified.pop(pos)

text = ''.join(modified)
print(f"\nWith TH removed (keeping consonants):")
print(f"  {text[:100]}...")

score = sum(text.count(w) * len(w) for w in OLD_ENGLISH_WORDS)
print(f"Score: {score}")

print(f"\n{'='*70}")
print("CHECK ORIGINAL CIPHERTEXT AT THESE POSITIONS")
print("="*70)

# Load original ciphertext for Page 0
try:
    with open(r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_00\runes.txt', 'r', encoding='utf-8') as f:
        cipher_text = f.read().strip()
    
    cipher_runes = parse_to_runes(cipher_text)
    print(f"Original cipher has {len(cipher_runes)} runes")
    
    # What are the cipher runes at TH+consonant positions?
    print(f"\nCipher runes at TH+consonant output positions:")
    for pos in th_cons_positions:
        if pos < len(cipher_runes):
            print(f"  Pos {pos}: Cipher={cipher_runes[pos]}, Output=TH")
except Exception as e:
    print(f"Could not load cipher: {e}")

print(f"\n{'='*70}")
print("ANALYSIS: What should TH+D, TH+R, etc. become?")  
print("="*70)

# THR is common in THROUGH, THREE, THRONE
# THD is not common
# What Old English words contain these patterns?

test_patterns = ['THR', 'THD', 'THN', 'THP', 'THX', 'THT', 'THB', 'THL', 'THM', 'THS', 'THW', 'THY']
for pat in test_patterns:
    # Common English words with this pattern
    examples = {
        'THR': ['THROUGH', 'THREE', 'THRONE', 'THROW', 'THREAD'],
        'THD': [],  # Very rare
        'THN': [],  # Very rare
        'THP': [],  # Very rare
        'THX': [],  # Not in English
        'THT': [],  # Not in English 
        'THB': [],  # Very rare
        'THL': [],  # Very rare
        'THM': [],  # Very rare
        'THS': ['OATHS', 'PATHS', 'MOTHS'],  # -THS plural
        'THW': ['THWART'],
        'THY': ['THY', 'THYSELF'],
    }
    
    in_text = text.count(pat) if text else 0
    print(f"{pat}: in text {in_text}x, examples: {examples.get(pat, [])}")

#!/usr/bin/env python3
"""
Advanced word boundary detection for Old English text.
The presence of DOETH, GOETH, LEARETH, HATH, THEE, THOU suggests
the plaintext is in archaic English style.

Strategy: Try to find word boundaries using Old English patterns.
"""

# First layer outputs
PAGES = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGTHEESTHENGTTHEATHEATHTHEAHENGTHETHTHRAAINGTHETHEATETHWAETHEAINGWHIATTHETHATHENGRHEATHEATHETHISOFRAETHOFITHEAEMTHEINGENGTHEHETHEATHFMHTHENGWNGETHEHETHEBDEHEADTHEINGTHEINGTHEAOINGETHIINGITNGTTHWEOTHEHENGTHEATHTHENGNGATHESTWTHETHTHEATHNGETHEIREOENGNG",
    2: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHEAHNGOOEOHISRAEOITHLEAAONGAAAHREINGOFOTHTBTHENREINGTHEAYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHEKSINGTHBCFAJITHATHEUINTHEMTHETHEOREAOEINGOMTHEEEATHEOEHEJSOHENGIINGHINGINGEAITHEIAHEOYNGTHEAISHNRFEOIAHEFANEIAHEOEHEOEHENGTHETHEORNG",
    2: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHEAHNGOOEOHISRAEOITHLEAAONGAAAHREINGOFOTHTBTHENREINGTHEAYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHEKSINGTHBCFAJITHATHEUINTHEMTHETHEOREAOEINGOMTHEEEATHEOEHEJSOHENGIINGHINGINGEAITHEIAHEOYNGTHEAISHNRFEOIAHEFANEIAHEOEHEOEHENGTHETHEORNG",
    3: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBITHETHETHATHENGEHEITHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSO",
    4: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHETHETOSOTHETHEOTHIHTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATHETHIHETHENGTHENGEOINGEOINGEITHTBTBETHEOTHETHINGHEETHHEINGHENGATHETHETSOTSOTHEOHEOTHETHENGTHETHEITHEOFEATHTHETHTHETOITSATTHETHETHENG"
}

# Common Old English words and patterns
OLD_ENGLISH_VOCAB = [
    # Common words
    'THE', 'THAT', 'THIS', 'WHAT', 'WHICH', 'WHO', 'WHOM',
    'THEE', 'THOU', 'THY', 'THINE', 'YE', 'YOU', 'YOUR',
    'HE', 'SHE', 'IT', 'WE', 'THEY', 'HIM', 'HER', 'US', 'THEM',
    'IS', 'ARE', 'WAS', 'WERE', 'BE', 'BEEN', 'BEING',
    'HAVE', 'HAS', 'HAD', 'HATH', 'HAST',
    'DO', 'DOES', 'DID', 'DOTH', 'DOST', 'DOETH',
    'GO', 'GOES', 'WENT', 'GONE', 'GOETH',
    'COME', 'COMES', 'CAME', 'COMETH',
    'MAKE', 'MAKES', 'MADE', 'MAKETH',
    'TAKE', 'TAKES', 'TOOK', 'TAKEN', 'TAKETH',
    'GIVE', 'GIVES', 'GAVE', 'GIVEN', 'GIVETH',
    'SAY', 'SAYS', 'SAID', 'SAITH', 'SAYETH',
    'KNOW', 'KNOWS', 'KNEW', 'KNOWN', 'KNOWETH',
    'SEE', 'SEES', 'SAW', 'SEEN', 'SEETH',
    'FIND', 'FINDS', 'FOUND', 'FINDETH',
    'SEEK', 'SEEKS', 'SOUGHT', 'SEEKETH',
    'LEARN', 'LEARNS', 'LEARNT', 'LEARNED', 'LEARETH', 'LEARNETH',
    'THINK', 'THINKS', 'THOUGHT', 'THINKETH',
    'WILL', 'SHALL', 'WOULD', 'SHOULD', 'COULD', 'MAY', 'MIGHT',
    'WILT', 'SHALT', 'WOULDST', 'SHOULDST', 'COULDST', 'MAYEST', 'MIGHTEST',
    'CAN', 'CANST',
    # Prepositions and conjunctions
    'OF', 'TO', 'IN', 'FOR', 'ON', 'WITH', 'AT', 'BY', 'FROM',
    'INTO', 'UNTO', 'UPON', 'ABOUT', 'AFTER', 'BEFORE', 'BETWEEN', 'THROUGH',
    'AND', 'OR', 'BUT', 'IF', 'WHEN', 'WHERE', 'WHILE', 'AS', 'THAN',
    'BECAUSE', 'ALTHOUGH', 'UNLESS', 'UNTIL', 'SINCE', 'WHETHER',
    # Articles and determiners
    'A', 'AN', 'SOME', 'ANY', 'NO', 'ALL', 'EACH', 'EVERY', 'MANY', 'MUCH',
    'FEW', 'LITTLE', 'BOTH', 'EITHER', 'NEITHER', 'OTHER', 'ANOTHER',
    # Adverbs
    'NOT', 'NOW', 'THEN', 'HERE', 'THERE', 'WHERE', 'WHEN', 'HOW', 'WHY',
    'WELL', 'ALSO', 'ONLY', 'EVEN', 'JUST', 'STILL', 'ALREADY', 'ALWAYS',
    'NEVER', 'OFTEN', 'SOMETIMES', 'EVER', 'YET', 'THUS', 'HENCE', 'THEREFORE',
    # Adjectives
    'GOOD', 'GREAT', 'NEW', 'OLD', 'HIGH', 'LOW', 'LONG', 'SHORT',
    'TRUE', 'FALSE', 'RIGHT', 'WRONG', 'FIRST', 'LAST', 'SAME', 'OWN',
    'DIVINE', 'SACRED', 'HOLY', 'WISE', 'FOOLISH',
    # Religious/mystical vocabulary (Cicada)
    'DIVINITY', 'WISDOM', 'TRUTH', 'KNOWLEDGE', 'PILGRIM', 'JOURNEY',
    'EMERGE', 'INSTAR', 'CIRCUMFERENCE', 'TOTIENT', 'PRIME', 'PRIMES',
    'CONSUMPTION', 'ADHERENCE', 'PRESERVATION', 'LOSS', 'DEATH',
    'ENLIGHTEN', 'ENLIGHTENED', 'ENLIGHTENMENT',
    # Numbers
    'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',
]

def find_all_words(text, vocab):
    """Find all occurrences of vocabulary words"""
    found = []
    for word in vocab:
        start = 0
        while True:
            pos = text.find(word, start)
            if pos == -1:
                break
            found.append((pos, pos + len(word), word))
            start = pos + 1
    return sorted(found, key=lambda x: (x[0], -len(x[2])))

def greedy_parse(text, vocab):
    """Greedy left-to-right parsing trying longest words first"""
    vocab_sorted = sorted(vocab, key=len, reverse=True)
    result = []
    pos = 0
    while pos < len(text):
        matched = False
        for word in vocab_sorted:
            if text[pos:pos+len(word)] == word:
                result.append(word)
                pos += len(word)
                matched = True
                break
        if not matched:
            # Take single character as unknown
            result.append('[' + text[pos] + ']')
            pos += 1
    return result

def optimal_parse(text, vocab, max_len=10):
    """Dynamic programming for optimal word coverage"""
    n = len(text)
    # dp[i] = (best_score, best_path) ending at position i
    dp = [None] * (n + 1)
    dp[0] = (0, [])
    
    vocab_set = set(vocab)
    
    for i in range(n):
        if dp[i] is None:
            continue
        
        # Try each possible word length
        for wlen in range(1, min(max_len + 1, n - i + 1)):
            word = text[i:i+wlen]
            if word in vocab_set:
                new_score = dp[i][0] + len(word)  # Score = total matched chars
                new_path = dp[i][1] + [word]
                
                if dp[i + wlen] is None or new_score > dp[i + wlen][0]:
                    dp[i + wlen] = (new_score, new_path)
            elif wlen == 1:
                # Allow single unknown chars to continue
                new_score = dp[i][0]
                new_path = dp[i][1] + ['[' + word + ']']
                
                if dp[i + 1] is None or new_score > dp[i + 1][0]:
                    dp[i + 1] = (new_score, new_path)
    
    if dp[n]:
        return dp[n][1], dp[n][0]
    return [], 0

def analyze_word_boundaries(text, name):
    """Analyze potential word boundaries"""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {name}")
    print(f"{'='*60}")
    print(f"Length: {len(text)} characters")
    
    # Find all vocabulary words
    all_found = find_all_words(text, OLD_ENGLISH_VOCAB)
    unique_words = sorted(set([w for _, _, w in all_found]), key=lambda x: -len(x))
    print(f"\nVocabulary words found ({len(unique_words)} unique):")
    for word in unique_words[:20]:
        count = sum(1 for _, _, w in all_found if w == word)
        print(f"  {word}: {count}")
    
    # Greedy parse
    print(f"\nGreedy parsing (first 30 tokens):")
    parsed = greedy_parse(text, OLD_ENGLISH_VOCAB)
    print(' '.join(parsed[:30]) + '...')
    
    # Count matched vs unmatched
    matched = sum(1 for t in parsed if not t.startswith('['))
    unmatched = len(parsed) - matched
    print(f"Matched tokens: {matched}, Unmatched chars: {unmatched}")
    print(f"Coverage: {sum(len(t) if not t.startswith('[') else 0 for t in parsed)}/{len(text)} = {100*sum(len(t) if not t.startswith('[') else 0 for t in parsed)/len(text):.1f}%")
    
    # Optimal parse (expensive, only first 200 chars)
    print(f"\nOptimal parsing (first 200 chars):")
    text_short = text[:200]
    parsed_opt, score = optimal_parse(text_short, OLD_ENGLISH_VOCAB, max_len=12)
    print(' '.join(parsed_opt[:30]) + '...')
    print(f"Score: {score}/{len(text_short)} = {100*score/len(text_short):.1f}% coverage")

# Analyze each page
print("=" * 60)
print("OLD ENGLISH WORD BOUNDARY ANALYSIS")
print("=" * 60)

for pnum, text in sorted(PAGES.items()):
    # Strip EMB prefix for pages 2-4
    if pnum >= 2:
        # Find where EMB ends
        i = 0
        while i < len(text) - 2 and text[i:i+3] == 'EMB':
            i += 3
        stripped = text[i:]
        analyze_word_boundaries(stripped, f"Page {pnum} (after EMB strip)")
    else:
        analyze_word_boundaries(text, f"Page {pnum}")

# Special analysis: Look for "THAT HE" pattern in Page 0
print("\n" + "=" * 60)
print("SPECIAL: Pattern recognition in Page 0")
print("=" * 60)

p0 = PAGES[0]
# Check if AETHATAEYETHES... could be "AE THAT A [E/EYE] THE S..."
patterns = [
    ('AE THAT A EYE THE S THE S', 'Word boundary hypothesis 1'),
    ('A ETH AT A EYE THES THE S', 'Word boundary hypothesis 2'),
    ('AETH AT AE YETH ES THES', 'Word boundary hypothesis 3'),
]

print("Page 0 starts with: AETHATAEYETHESTHES...")
print("Possible interpretations:")
for pattern, desc in patterns:
    print(f"  {desc}: {pattern}")

# Check for THE as consistent boundary marker
the_positions = []
pos = 0
while True:
    pos = p0.find('THE', pos)
    if pos == -1:
        break
    the_positions.append(pos)
    pos += 1

print(f"\n'THE' appears at {len(the_positions)} positions")
print(f"Positions: {the_positions[:20]}...")

# Look at gaps between THE occurrences
gaps = [the_positions[i+1] - the_positions[i] for i in range(len(the_positions)-1)]
print(f"Gaps between THE: {gaps[:20]}...")
from collections import Counter
gap_counts = Counter(gaps)
print(f"Most common gaps: {gap_counts.most_common(10)}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

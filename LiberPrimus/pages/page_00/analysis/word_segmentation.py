#!/usr/bin/env python3
"""
Word segmentation using dynamic programming.
The first-layer output has the HIGHEST English score (2680),
suggesting it may be correct plaintext with spaces removed.

This script attempts to find optimal word boundaries.
"""

import math
from collections import Counter

# First layer outputs (only Pages 0-1 which are most English-like)
PAGES = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGTHEESTHENGTTHEATHEATHTHEAHENGTHETHTHRAAINGTHETHEATETHWAETHEAINGWHIATTHETHATHENGRHEATHEATHETHISOFRAETHOFITHEAEMTHEINGENGTHEHETHEATHFMHTHENGWNGETHEHETHEBDEHEADTHEINGTHEINGTHEAOINGETHIINGITNGTTHWEOTHEHENGTHEATHTHENGNGATHESTWTHETHTHEATHNGETHEIREOENGNG",
}

# Dictionary of English words (common + Old English)
DICTIONARY = set([
    # Common modern words
    'THE', 'A', 'AN', 'AND', 'OR', 'BUT', 'IF', 'IS', 'ARE', 'WAS', 'WERE', 'BE', 'BEEN',
    'BEING', 'HAVE', 'HAS', 'HAD', 'DO', 'DOES', 'DID', 'WILL', 'WOULD', 'SHALL', 'SHOULD',
    'CAN', 'COULD', 'MAY', 'MIGHT', 'MUST', 'OF', 'TO', 'IN', 'FOR', 'ON', 'WITH', 'AT',
    'BY', 'FROM', 'AS', 'INTO', 'THROUGH', 'DURING', 'BEFORE', 'AFTER', 'ABOVE', 'BELOW',
    'BETWEEN', 'UNDER', 'AGAIN', 'FURTHER', 'THEN', 'ONCE', 'HERE', 'THERE', 'WHEN',
    'WHERE', 'WHY', 'HOW', 'ALL', 'EACH', 'EVERY', 'BOTH', 'FEW', 'MORE', 'MOST', 'OTHER',
    'SOME', 'SUCH', 'NO', 'NOR', 'NOT', 'ONLY', 'OWN', 'SAME', 'SO', 'THAN', 'TOO', 'VERY',
    'I', 'ME', 'MY', 'MYSELF', 'WE', 'OUR', 'OURS', 'OURSELVES', 'YOU', 'YOUR', 'YOURS',
    'YOURSELF', 'YOURSELVES', 'HE', 'HIM', 'HIS', 'HIMSELF', 'SHE', 'HER', 'HERS', 'HERSELF',
    'IT', 'ITS', 'ITSELF', 'THEY', 'THEM', 'THEIR', 'THEIRS', 'THEMSELVES', 'WHAT', 'WHICH',
    'WHO', 'WHOM', 'THIS', 'THAT', 'THESE', 'THOSE', 'AM', 'JUST', 'NOW', 'SAY', 'SAYS',
    'SAID', 'GO', 'GOES', 'WENT', 'GONE', 'COME', 'COMES', 'CAME', 'TAKE', 'TAKES', 'TOOK',
    'TAKEN', 'MAKE', 'MAKES', 'MADE', 'GET', 'GETS', 'GOT', 'GIVE', 'GIVES', 'GAVE', 'GIVEN',
    'FIND', 'FINDS', 'FOUND', 'THINK', 'THINKS', 'THOUGHT', 'KNOW', 'KNOWS', 'KNEW', 'KNOWN',
    'SEE', 'SEES', 'SAW', 'SEEN', 'WANT', 'WANTS', 'WANTED', 'USE', 'USES', 'USED',
    'LOOK', 'LOOKS', 'LOOKED', 'WORK', 'WORKS', 'WORKED', 'LIKE', 'LIKES', 'LIKED',
    'NEED', 'NEEDS', 'NEEDED', 'MEAN', 'MEANS', 'MEANT', 'KEEP', 'KEEPS', 'KEPT',
    'LET', 'LETS', 'PUT', 'PUTS', 'SEEM', 'SEEMS', 'SEEMED', 'HELP', 'HELPS', 'HELPED',
    'SHOW', 'SHOWS', 'SHOWED', 'HEAR', 'HEARS', 'HEARD', 'FEEL', 'FEELS', 'FELT',
    'LEAVE', 'LEAVES', 'LEFT', 'TRY', 'TRIES', 'TRIED', 'CALL', 'CALLS', 'CALLED',
    'BECOME', 'BECOMES', 'BECAME', 'ASK', 'ASKS', 'ASKED', 'TELL', 'TELLS', 'TOLD',
    'RUN', 'RUNS', 'RAN', 'BRING', 'BRINGS', 'BROUGHT', 'BEGIN', 'BEGINS', 'BEGAN',
    'WRITE', 'WRITES', 'WROTE', 'WRITTEN', 'READ', 'READS', 'LEARN', 'LEARNS', 'LEARNED',
    'STAND', 'STANDS', 'STOOD', 'TURN', 'TURNS', 'TURNED', 'MOVE', 'MOVES', 'MOVED',
    'LIVE', 'LIVES', 'LIVED', 'BELIEVE', 'BELIEVES', 'BELIEVED', 'HOLD', 'HOLDS', 'HELD',
    'OPEN', 'OPENS', 'OPENED', 'CLOSE', 'CLOSES', 'CLOSED', 'END', 'ENDS', 'ENDED',
    'PART', 'PARTS', 'PLACE', 'PLACES', 'WORLD', 'WORDS', 'HOME', 'HAND', 'HANDS',
    'WORD', 'MAN', 'MEN', 'WOMAN', 'WOMEN', 'CHILD', 'CHILDREN', 'YEAR', 'YEARS',
    'DAY', 'DAYS', 'TIME', 'TIMES', 'WAY', 'WAYS', 'THING', 'THINGS', 'LIFE', 'LIVES',
    'PEOPLE', 'FIRST', 'LAST', 'LONG', 'GREAT', 'LITTLE', 'OWN', 'OLD', 'RIGHT',
    'BIG', 'HIGH', 'DIFFERENT', 'SMALL', 'LARGE', 'NEXT', 'EARLY', 'YOUNG', 'IMPORTANT',
    'NEW', 'GOOD', 'BAD', 'TRUE', 'FALSE', 'SACRED', 'DIVINE', 'HOLY', 'WISE',
    
    # Old English / Archaic words
    'THEE', 'THOU', 'THY', 'THINE', 'YE', 'HATH', 'HAST', 'DOTH', 'DOST', 'SHALT', 'WILT',
    'CANST', 'WOULDST', 'SHOULDST', 'COULDST', 'MAYEST', 'MIGHTEST', 'ART', 'WERT',
    'DOETH', 'GOETH', 'COMETH', 'TAKETH', 'MAKETH', 'GIVETH', 'FINDETH', 'THINKETH',
    'KNOWETH', 'SEETH', 'SPEAKETH', 'HEARETH', 'LEARNETH', 'LEARETH', 'LIVETH',
    'SAITH', 'SAYETH', 'WHEREFORE', 'WHENCE', 'THENCE', 'HENCE', 'VERILY', 'FORSOOTH',
    'UNTO', 'UPON', 'AMONGST', 'BETWIXT', 'BENEATH', 'MAYHAP', 'PERCHANCE',
    'HEARKEN', 'BEHOLD', 'ARISE', 'ABIDE', 'YEA', 'NAY', 'AYE', 'ERE', 'ANON',
    'AE', 'EYE', 'EYES', 'EAR', 'EARS', 'HEART', 'HEARTS', 'SOUL', 'SOULS',
    
    # Cicada vocabulary
    'DIVINITY', 'WISDOM', 'TRUTH', 'KNOWLEDGE', 'PILGRIM', 'JOURNEY', 'EMERGE',
    'INSTAR', 'CIRCUMFERENCE', 'TOTIENT', 'PRIME', 'PRIMES', 'CONSUMPTION',
    'ADHERENCE', 'PRESERVATION', 'LOSS', 'DEATH', 'ENLIGHTEN', 'SACRED',
    'WARNING', 'BELIEVE', 'NOTHING', 'BOOK', 'EXCEPT', 'TEST',
    
    # Two-letter words
    'HE', 'IT', 'AS', 'AT', 'ON', 'IN', 'TO', 'OF', 'IS', 'OR', 'AN', 'IF', 'SO',
    'BY', 'UP', 'NO', 'DO', 'GO', 'BE', 'WE', 'ME', 'MY', 'US',
    
    # Common endings as standalone (for partial matches)
    'ING', 'ED', 'ER', 'LY', 'EST', 'ETH', 'EN', 'NESS',
])

# Add NG as a word (frequent in output)
DICTIONARY.add('NG')
DICTIONARY.add('TH')
DICTIONARY.add('EA')
DICTIONARY.add('OE')
DICTIONARY.add('AE')

def word_prob(word, dictionary):
    """Score a word - higher if in dictionary, lower if not"""
    if word in dictionary:
        return len(word) * 10  # Prefer longer dictionary words
    elif len(word) == 1:
        return 1  # Single letters are okay
    elif len(word) == 2:
        return 2  # Two-letter non-words are marginal
    else:
        return -len(word)  # Penalize non-dictionary words by length

def segment_dp(text, dictionary, max_word_len=15):
    """
    Dynamic programming to find optimal word segmentation.
    Returns (best_score, best_segmentation)
    """
    n = len(text)
    # dp[i] = (best_score ending at i, previous position, word)
    dp = [(-float('inf'), -1, '')] * (n + 1)
    dp[0] = (0, -1, '')
    
    for i in range(1, n + 1):
        for j in range(max(0, i - max_word_len), i):
            word = text[j:i]
            score = dp[j][0] + word_prob(word, dictionary)
            if score > dp[i][0]:
                dp[i] = (score, j, word)
    
    # Backtrack to get segmentation
    words = []
    i = n
    while i > 0:
        _, prev, word = dp[i]
        if word:
            words.append(word)
        i = prev
    
    words.reverse()
    return dp[n][0], words

print("=" * 70)
print("WORD SEGMENTATION ANALYSIS")
print("=" * 70)

for pnum, text in sorted(PAGES.items()):
    print(f"\n{'='*60}")
    print(f"PAGE {pnum}")
    print(f"{'='*60}")
    print(f"Length: {len(text)} characters")
    print(f"Raw: {text[:80]}...")
    
    # Segment first 150 characters (DP is expensive)
    short_text = text[:150]
    score, words = segment_dp(short_text, DICTIONARY)
    
    print(f"\nOptimal segmentation (first 150 chars):")
    print(f"Score: {score}")
    print(f"Words: {' '.join(words)}")
    
    # Count dictionary vs non-dictionary words
    dict_words = [w for w in words if w in DICTIONARY]
    non_dict = [w for w in words if w not in DICTIONARY]
    
    print(f"\nDictionary words ({len(dict_words)}): {dict_words}")
    print(f"Non-dictionary ({len(non_dict)}): {non_dict}")
    
    # Calculate coverage
    dict_chars = sum(len(w) for w in dict_words)
    total_chars = len(short_text)
    print(f"Dictionary coverage: {dict_chars}/{total_chars} = {100*dict_chars/total_chars:.1f}%")

# Try just Page 0 with full text
print("\n" + "=" * 70)
print("FULL PAGE 0 SEGMENTATION (may take a moment)")
print("=" * 70)

text = PAGES[0]
score, words = segment_dp(text, DICTIONARY)

print(f"Score: {score}")
print(f"Word count: {len(words)}")
print(f"\nFull segmentation:")
print(' '.join(words))

# Count patterns
word_counts = Counter(words)
print(f"\nMost common words:")
for word, count in word_counts.most_common(20):
    in_dict = "✓" if word in DICTIONARY else "✗"
    print(f"  {word}: {count} {in_dict}")

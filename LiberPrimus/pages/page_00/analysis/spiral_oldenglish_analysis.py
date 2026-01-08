#!/usr/bin/env python3
"""
Spiral reading patterns and Old English vocabulary analysis.
Based on finding: LEARETH, DOETH, HATH, THEE, THINE suggest archaic text.
"""

import os

# Gematria Primus
GP = ['F','U','TH','O','R','C','K','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','ING','OE','D','A','AE','Y','EA']

# First layer outputs (hardcoded from previous analysis)
PAGES = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGTHEESTHENGTTHEATHEATHTHEAHENGTHETHTHRAAINGTHETHEATETHWAETHEAINGWHIATTHETHATHENGRHEATHEATHETHISOFRAETHOFITHEAEMTHEINGENGTHEHETHEATHFMHTHENGWNGETHEHETHEBDEHEADTHEINGTHEINGTHEAOINGETHIINGITNGTTHWEOTHEHENGTHEATHTHENGNGATHESTWTHETHTHEATHNGETHEIREOENGNG",
    2: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHEAHNGOOEOHISRAEOITHLEAAONGAAAHREINGOFOTHTBTHENREINGTHEAYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHEKSINGTHBCFAJITHATHEUINTHEMTHETHEOREAOEINGOMTHEEEATHEOEHEJSOHENGIINGHINGINGEAITHEIAHEOYNGTHEAISHNRFEOIAHEFANEIAHEOEHEOEHENGTHETHEORNG",
    3: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBITHETHETHATHENGEHEITHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSO",
    4: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHETHETOSOTHETHEOTHIHTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATHETHIHETHENGTHENGEOINGEOINGEITHTBTBETHEOTHETHINGHEETHHEINGHENGATHETHETSOTSOTHEOHEOTHETHENGTHETHEITHEOFEATHTHETHTHETOITSATTHETHETHENG"
}

def load_first_layer():
    """Load first layer outputs"""
    return PAGES

def spiral_read(text, width):
    """Read text in spiral pattern from grid"""
    height = (len(text) + width - 1) // width
    grid = []
    idx = 0
    for _ in range(height):
        row = []
        for _ in range(width):
            if idx < len(text):
                row.append(text[idx])
            else:
                row.append(' ')
            idx += 1
        grid.append(row)
    
    # Spiral read: right, down, left, up
    result = []
    top, bottom, left, right = 0, height - 1, 0, width - 1
    
    while top <= bottom and left <= right:
        # Right
        for i in range(left, right + 1):
            if top < len(grid) and i < len(grid[top]):
                result.append(grid[top][i])
        top += 1
        
        # Down
        for i in range(top, bottom + 1):
            if i < len(grid) and right < len(grid[i]):
                result.append(grid[i][right])
        right -= 1
        
        # Left
        if top <= bottom:
            for i in range(right, left - 1, -1):
                if bottom < len(grid) and i < len(grid[bottom]):
                    result.append(grid[bottom][i])
            bottom -= 1
        
        # Up
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if i < len(grid) and left < len(grid[i]):
                    result.append(grid[i][left])
            left += 1
    
    return ''.join(result).replace(' ', '')

def diagonal_read(text, width):
    """Read text diagonally from grid"""
    height = (len(text) + width - 1) // width
    grid = []
    idx = 0
    for _ in range(height):
        row = []
        for _ in range(width):
            if idx < len(text):
                row.append(text[idx])
            else:
                row.append(' ')
            idx += 1
        grid.append(row)
    
    result = []
    # Read all diagonals from top-left to bottom-right
    for d in range(height + width - 1):
        for i in range(max(0, d - width + 1), min(d + 1, height)):
            j = d - i
            if j < len(grid[i]):
                result.append(grid[i][j])
    
    return ''.join(result).replace(' ', '')

def boustrophedon_read(text, width):
    """Read alternating left-right, right-left (like plowing a field)"""
    height = (len(text) + width - 1) // width
    result = []
    for row in range(height):
        start = row * width
        end = min(start + width, len(text))
        segment = text[start:end]
        if row % 2 == 1:  # Odd rows reversed
            segment = segment[::-1]
        result.append(segment)
    return ''.join(result)

# Old English word patterns to search for
OLD_ENGLISH_WORDS = [
    # Common Old/Middle English
    'THEE', 'THOU', 'THINE', 'THY', 'HATH', 'DOTH', 'DOETH',
    'SHALT', 'WILT', 'CANST', 'MAYEST', 'SHOULDST',
    'WHEREFORE', 'WHENCE', 'THENCE', 'HENCE',
    'VERILY', 'FORSOOTH', 'MAYHAP', 'PERCHANCE',
    'UNTO', 'UPON', 'AMONGST', 'BETWIXT', 'BENEATH',
    'HEARKEN', 'BEHOLD', 'ARISE', 'ABIDE',
    'YEA', 'NAY', 'AYE', 'ERE', 'ANON',
    'SEEKETH', 'FINDETH', 'KNOWETH', 'COMETH', 'GOETH',
    'LEARETH', 'SPEAKETH', 'TAKETH', 'GIVETH', 'LIVETH',
    # -ETH verb endings (search for pattern)
    'EATH', 'ETHE',
    # Religious/mystical
    'DIVINE', 'DIVINITY', 'SACRED', 'PILGRIM', 'WISDOM',
    'TRUTH', 'KNOWLEDGE', 'ENLIGHTEN', 'EMERGE', 'INSTAR',
    # Cicada vocabulary
    'CIRCUMFERENCE', 'TOTIENT', 'PRIME', 'PRIMES',
    'CONSUMPTION', 'ADHERENCE', 'PRESERVATION',
]

def find_old_english(text, words):
    """Find Old English words in text"""
    found = {}
    for word in words:
        if word in text:
            count = text.count(word)
            found[word] = count
    return found

def find_eth_verbs(text):
    """Find -ETH verb endings which are characteristic of Old English"""
    eth_verbs = []
    i = 0
    while i < len(text) - 3:
        if text[i:i+3] == 'ETH':
            # Look back for the verb stem
            start = max(0, i - 10)
            context = text[start:i+3]
            eth_verbs.append((i, context))
        i += 1
    return eth_verbs

def score_english(text):
    """Score text for English-like patterns"""
    # Common English bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND',
               'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR']
    score = 0
    for bg in bigrams:
        score += text.count(bg) * 10
    # Common trigrams
    trigrams = ['THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE', 'FOR',
                'ENT', 'ION', 'TER', 'WAS', 'YOU', 'ITH', 'VER', 'ALL', 'WIT']
    for tg in trigrams:
        score += text.count(tg) * 20
    return score

print("=" * 60)
print("SPIRAL AND OLD ENGLISH ANALYSIS")
print("=" * 60)

pages = load_first_layer()

# Key lengths for grid widths
KEY_LENGTHS = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

print("\n" + "-" * 60)
print("TEST 1: SPIRAL READ (using key length as width)")
print("-" * 60)

for pnum, text in pages.items():
    width = KEY_LENGTHS[pnum]
    spiral = spiral_read(text, width)
    score = score_english(spiral)
    print(f"Page {pnum}: Width {width}, Score={score}")
    print(f"  First 70 chars: {spiral[:70]}...")
    
    # Also try smaller widths
    for w in [7, 11, 13, 17, 19, 23, 29]:
        s = spiral_read(text, w)
        sc = score_english(s)
        if sc > score:
            print(f"  Width {w}: Score={sc} (better!) - {s[:50]}...")

print("\n" + "-" * 60)
print("TEST 2: DIAGONAL READ (using key length as width)")
print("-" * 60)

for pnum, text in pages.items():
    width = KEY_LENGTHS[pnum]
    diag = diagonal_read(text, width)
    score = score_english(diag)
    print(f"Page {pnum}: Width {width}, Score={score}")
    print(f"  First 70 chars: {diag[:70]}...")

print("\n" + "-" * 60)
print("TEST 3: BOUSTROPHEDON (ALTERNATING DIRECTION)")
print("-" * 60)

for pnum, text in pages.items():
    width = KEY_LENGTHS[pnum]
    boust = boustrophedon_read(text, width)
    score = score_english(boust)
    print(f"Page {pnum}: Width {width}, Score={score}")
    print(f"  First 70 chars: {boust[:70]}...")
    
    # Try prime widths
    for w in [7, 11, 13, 17, 19, 23, 29, 31]:
        b = boustrophedon_read(text, w)
        sc = score_english(b)
        if sc > score:
            print(f"  Width {w}: Score={sc} (better!) - {b[:50]}...")

print("\n" + "-" * 60)
print("TEST 4: OLD ENGLISH VOCABULARY SEARCH")
print("-" * 60)

for pnum, text in pages.items():
    found = find_old_english(text, OLD_ENGLISH_WORDS)
    if found:
        print(f"Page {pnum}: {len(found)} Old English words found")
        for word, count in sorted(found.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count}")
    else:
        print(f"Page {pnum}: No Old English words found")

print("\n" + "-" * 60)
print("TEST 5: -ETH VERB ENDINGS (Old English pattern)")
print("-" * 60)

for pnum, text in pages.items():
    eth_verbs = find_eth_verbs(text)
    print(f"Page {pnum}: Found {len(eth_verbs)} -ETH patterns")
    for pos, context in eth_verbs[:10]:  # Show first 10
        print(f"  Position {pos}: ...{context}...")

print("\n" + "-" * 60)
print("TEST 6: STRIP 'THE' AND ANALYZE REMAINDER")
print("-" * 60)

for pnum, text in pages.items():
    # Remove all THE occurrences
    stripped = text.replace('THE', '')
    score_orig = score_english(text)
    score_strip = score_english(stripped)
    print(f"Page {pnum}: Original score={score_orig}, After strip={score_strip}")
    print(f"  Stripped (first 70): {stripped[:70]}...")
    
    # Look for words in stripped version
    words_4plus = []
    for word in OLD_ENGLISH_WORDS:
        if len(word) >= 4 and word in stripped:
            words_4plus.append(word)
    if words_4plus:
        print(f"  Words found: {words_4plus}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

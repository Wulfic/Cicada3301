#!/usr/bin/env python3
"""
Test Atbash and other simple transformations on first-layer output.
Atbash was used in the Onion pages - might be a second layer here.

Atbash for Gematria: new_index = 28 - old_index
"""

# Gematria Primus - 29 characters
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S/Z', 'T', 'B', 'E', 'M',
            'L', 'ING', 'OE', 'D', 'A', 'AE', 'Y', 'IA/IO', 'EA']

PRIME_VALUES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                73, 79, 83, 89, 97, 101, 103, 107, 109]

# First-layer decrypted outputs
PLAINTEXTS = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"
}

def text_to_indices(text):
    """Convert text to Gematria indices"""
    indices = []
    i = 0
    while i < len(text):
        found = False
        # Try multi-char first
        for length in [3, 2, 1]:
            if i + length <= len(text):
                chunk = text[i:i+length].upper()
                for j, glyph in enumerate(GEMATRIA):
                    if glyph == chunk or (len(glyph) > 1 and chunk in glyph.split('/')):
                        indices.append(j)
                        i += length
                        found = True
                        break
                if found:
                    break
        if not found:
            char = text[i].upper()
            for j, glyph in enumerate(GEMATRIA):
                if char in glyph.split('/')[0]:
                    indices.append(j)
                    break
            i += 1
    return indices

def indices_to_text(indices):
    """Convert indices to text"""
    result = []
    for idx in indices:
        if 0 <= idx < 29:
            glyph = GEMATRIA[idx]
            if '/' in glyph:
                glyph = glyph.split('/')[0]
            result.append(glyph)
    return ''.join(result)

def score_english(text):
    """Score how English-like the text is"""
    text = text.upper()
    english_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 
                       'OR', 'AR', 'ES', 'EA', 'TI', 'TE', 'IS', 'IT', 'TO', 'NG']
    common_words = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'FOR', 'THAT', 'WAS',
                    'BE', 'AS', 'ARE', 'WITH', 'NOT', 'HAS', 'WE', 'THIS', 'HAVE', 'FROM']
    
    score = 0
    for bigram in english_bigrams:
        score += text.count(bigram) * 2
    for word in common_words:
        score += text.count(word) * 10
    return score

print("=" * 60)
print("ATBASH AND SIMPLE CIPHER ANALYSIS")
print("=" * 60)
print()

# Test 1: Atbash (index reversal)
print("-" * 60)
print("TEST 1: ATBASH - new_index = 28 - old_index")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    new_indices = [(28 - idx) % 29 for idx in indices]
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Test 2: Atbash + various shifts
print("-" * 60)
print("TEST 2: ATBASH + SHIFT(n)")
print("-" * 60)

best_results = {}
for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    best_score = 0
    best_shift = 0
    best_text = ""
    
    for shift in range(29):
        new_indices = [(28 - idx + shift) % 29 for idx in indices]
        new_text = indices_to_text(new_indices)
        score = score_english(new_text)
        if score > best_score:
            best_score = score
            best_shift = shift
            best_text = new_text
    
    best_results[page_num] = (best_shift, best_score, best_text)
    print(f"Page {page_num}: best shift={best_shift}, score={best_score}")
    print(f"  First 100: {best_text[:100]}")
    print()

# Test 3: Double application - Atbash on Atbash (should restore)
print("-" * 60)
print("TEST 3: DOUBLE ATBASH (should restore original)")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    atbash1 = [(28 - idx) % 29 for idx in indices]
    atbash2 = [(28 - idx) % 29 for idx in atbash1]
    restored = indices_to_text(atbash2)
    match = "✓ MATCH" if text_to_indices(restored) == indices else "✗ NO MATCH"
    print(f"Page {page_num}: {match}")
print()

# Test 4: Subtract from prime values
print("-" * 60)
print("TEST 4: PRIME VALUE ATBASH - new = (109 - prime_value[idx]) mod 29")
print("109 is the largest prime in Gematria")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    new_indices = [(109 - PRIME_VALUES[idx]) % 29 for idx in indices]
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Test 5: Simple shift (ROT-N) on first layer output
print("-" * 60)
print("TEST 5: BEST SIMPLE SHIFT on first layer output")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    best_score = 0
    best_shift = 0
    best_text = ""
    
    for shift in range(29):
        new_indices = [(idx + shift) % 29 for idx in indices]
        new_text = indices_to_text(new_indices)
        score = score_english(new_text)
        if score > best_score:
            best_score = score
            best_shift = shift
            best_text = new_text
    
    print(f"Page {page_num}: best shift={best_shift}, score={best_score}")
    print(f"  First 100: {best_text[:100]}")
    print()

# Test 6: Progressive shift (position-based)
print("-" * 60)
print("TEST 6: PROGRESSIVE SHIFT - shift increases by 1 each position")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    
    # Progressive add
    new_indices = [(idx + i) % 29 for i, idx in enumerate(indices)]
    new_text = indices_to_text(new_indices)
    score_add = score_english(new_text)
    
    # Progressive subtract
    new_indices2 = [(idx - i) % 29 for i, idx in enumerate(indices)]
    new_text2 = indices_to_text(new_indices2)
    score_sub = score_english(new_text2)
    
    print(f"Page {page_num}: +i score={score_add}, -i score={score_sub}")
    if score_add > score_sub:
        print(f"  Best (+i): {new_text[:100]}")
    else:
        print(f"  Best (-i): {new_text2[:100]}")
    print()

# Test 7: Alternating Atbash (apply to odd positions only)
print("-" * 60)
print("TEST 7: ALTERNATING ATBASH - apply only to odd positions")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    new_indices = [(28 - idx) % 29 if i % 2 == 1 else idx for i, idx in enumerate(indices)]
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("Original first-layer scores:")
for page_num, plaintext in PLAINTEXTS.items():
    print(f"  Page {page_num}: {score_english(plaintext)}")

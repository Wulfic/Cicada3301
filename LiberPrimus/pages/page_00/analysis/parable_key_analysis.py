#!/usr/bin/env python3
"""
Test the Parable text (Page 57) as a running key for first-layer output.
The Parable is the final solved page and may contain the key.

Also test word extraction from first-layer output using THE as word boundaries.
"""

# Gematria Primus - 29 characters
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S/Z', 'T', 'B', 'E', 'M',
            'L', 'ING', 'OE', 'D', 'A', 'AE', 'Y', 'IA/IO', 'EA']

# The Parable - Page 57 (plaintext)
PARABLE = """PARABLE
LIKE THE INSTAR
TUNNELING TO THE SURFACE
WE MUST SHED OUR OWN CIRCUMFERENCES
FIND THE DIVINITY WITHIN AND EMERGE"""

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
    # Strip spaces and convert
    clean = ''.join(text.upper().split())
    indices = []
    i = 0
    while i < len(clean):
        found = False
        for length in [3, 2, 1]:
            if i + length <= len(clean):
                chunk = clean[i:i+length]
                for j, glyph in enumerate(GEMATRIA):
                    if glyph == chunk or (len(glyph) > 1 and chunk in glyph.split('/')):
                        indices.append(j)
                        i += length
                        found = True
                        break
                if found:
                    break
        if not found:
            char = clean[i]
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
print("PARABLE AS RUNNING KEY")
print("=" * 60)
print()

parable_indices = text_to_indices(PARABLE)
parable_text = indices_to_text(parable_indices)
print(f"Parable as indices ({len(parable_indices)} chars): {parable_text}")
print()

# Test 1: Apply Parable as running key (repeating)
print("-" * 60)
print("TEST 1: PARABLE AS VIGENÈRE KEY (repeating)")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    pt_indices = text_to_indices(plaintext)
    
    # SUB with parable key
    result_sub = []
    for i, idx in enumerate(pt_indices):
        key_idx = parable_indices[i % len(parable_indices)]
        new_idx = (idx - key_idx) % 29
        result_sub.append(new_idx)
    
    # ADD with parable key
    result_add = []
    for i, idx in enumerate(pt_indices):
        key_idx = parable_indices[i % len(parable_indices)]
        new_idx = (idx + key_idx) % 29
        result_add.append(new_idx)
    
    sub_text = indices_to_text(result_sub)
    add_text = indices_to_text(result_add)
    
    print(f"Page {page_num}:")
    print(f"  SUB (score={score_english(sub_text)}): {sub_text[:60]}...")
    print(f"  ADD (score={score_english(add_text)}): {add_text[:60]}...")
    print()

# Test 2: Use specific key phrases from Parable/Onion
print("-" * 60)
print("TEST 2: KEY PHRASES FROM PARABLE/ONION CONTENT")
print("-" * 60)

key_phrases = [
    "THEINSTARTUNNELINGTOTHESURFACE",
    "SHEDYOUROWNCIRCUMFERENCE",
    "FINDTHEDIVINITYWITHINANDEMERGE",
    "CONSUMPTIONPRESERVATIONADHERENCE",
    "THETOTIENTFUNCTIONISSACRED",
    "THEPRIMESARESACRED"
]

for key_phrase in key_phrases:
    key_indices = text_to_indices(key_phrase)
    print(f"Key: {key_phrase[:30]}... ({len(key_indices)} chars)")
    
    for page_num in [0, 1]:  # Test on THE-heavy pages
        pt_indices = text_to_indices(PLAINTEXTS[page_num])
        
        result_sub = []
        for i, idx in enumerate(pt_indices):
            key_idx = key_indices[i % len(key_indices)]
            new_idx = (idx - key_idx) % 29
            result_sub.append(new_idx)
        
        sub_text = indices_to_text(result_sub)
        print(f"  Page {page_num} SUB (score={score_english(sub_text)}): {sub_text[:50]}...")
    print()

# Test 3: Extract words using THE as delimiter
print("-" * 60)
print("TEST 3: THE AS WORD BOUNDARY - Extract between THEs")
print("-" * 60)

for page_num in [0, 1]:
    plaintext = PLAINTEXTS[page_num].upper()
    
    # Split by THE
    segments = plaintext.split('THE')
    
    # Extract first char of each segment
    first_chars = [seg[0] if seg else '' for seg in segments if seg]
    first_char_msg = ''.join(first_chars)
    
    # Extract last char of each segment
    last_chars = [seg[-1] if seg else '' for seg in segments if seg]
    last_char_msg = ''.join(last_chars)
    
    # Full segments
    segment_lengths = [len(seg) for seg in segments if seg]
    
    print(f"Page {page_num}:")
    print(f"  THE count: {plaintext.count('THE')}")
    print(f"  First char after each THE: {first_char_msg[:50]}")
    print(f"  Last char before each THE: {last_char_msg[:50]}")
    print(f"  Segment lengths (first 20): {segment_lengths[:20]}")
    
    # Try interpreting segment lengths as indices
    length_indices = [l % 29 for l in segment_lengths]
    length_text = indices_to_text(length_indices)
    print(f"  Lengths as indices: {length_text[:50]}")
    print()

# Test 4: Anagram detection - check if output is anagrammed
print("-" * 60)
print("TEST 4: CHECK FOR ANAGRAM PATTERNS")
print("-" * 60)

def get_char_frequency(text):
    """Get character frequency distribution"""
    freq = {}
    for c in text.upper():
        freq[c] = freq.get(c, 0) + 1
    return freq

# Compare frequency to known Cicada texts
for page_num in [0, 1]:
    pt_freq = get_char_frequency(PLAINTEXTS[page_num])
    parable_freq = get_char_frequency(PARABLE)
    
    print(f"Page {page_num} top 10 letters: {sorted(pt_freq.items(), key=lambda x: -x[1])[:10]}")

print(f"Parable top 10: {sorted(parable_freq.items(), key=lambda x: -x[1])[:10]}")
print()

# Test 5: Autokey cipher using output itself
print("-" * 60)
print("TEST 5: AUTOKEY - Using plaintext itself as key")
print("-" * 60)

for page_num in [0, 1]:
    pt_indices = text_to_indices(PLAINTEXTS[page_num])
    
    # Autokey: key starts with seed, then uses plaintext
    for seed_word in ['THE', 'DIVINITY', 'INSTAR', 'PARABLE']:
        seed_indices = text_to_indices(seed_word)
        
        result = []
        key = seed_indices[:]
        
        for i, idx in enumerate(pt_indices):
            if i < len(key):
                key_idx = key[i]
            else:
                # Use previous plaintext as key
                key_idx = result[i - len(seed_indices)]
            
            new_idx = (idx - key_idx) % 29
            result.append(new_idx)
        
        result_text = indices_to_text(result)
        score = score_english(result_text)
        
        if score > 100:  # Only show promising results
            print(f"Page {page_num}, seed='{seed_word}': score={score}")
            print(f"  {result_text[:60]}...")
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

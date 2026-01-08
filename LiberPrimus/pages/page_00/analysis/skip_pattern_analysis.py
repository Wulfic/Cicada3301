#!/usr/bin/env python3
"""
Test F-rune (index 0) skipping pattern - used in Onion Vigenere.
Also test reading at specific character intervals that skip certain chars.
"""

# Gematria Primus - 29 characters
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S/Z', 'T', 'B', 'E', 'M',
            'L', 'ING', 'OE', 'D', 'A', 'AE', 'Y', 'IA/IO', 'EA']

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
print("F-RUNE SKIPPING AND SELECTIVE READING ANALYSIS")
print("=" * 60)
print()

# Test 1: Skip all F-runes (index 0) when reading
print("-" * 60)
print("TEST 1: Skip positions with F-rune (index 0)")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    filtered = [idx for idx in indices if idx != 0]
    new_text = indices_to_text(filtered)
    score = score_english(new_text)
    f_count = sum(1 for idx in indices if idx == 0)
    print(f"Page {page_num}: F-runes found={f_count}, new score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Test 2: Read only non-THE positions
print("-" * 60)
print("TEST 2: Skip THE trigram positions (read remainder)")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    text = plaintext.upper()
    
    # Find positions that are part of THE
    skip_positions = set()
    i = 0
    while i < len(text) - 2:
        if text[i:i+3] == 'THE':
            skip_positions.add(i)
            skip_positions.add(i+1)
            skip_positions.add(i+2)
            i += 3
        else:
            i += 1
    
    # Map text positions to index positions (approximate)
    remaining = [char for i, char in enumerate(text) if i not in skip_positions]
    remaining_text = ''.join(remaining)
    score = score_english(remaining_text)
    print(f"Page {page_num}: THE skipped={len(skip_positions)//3}, remaining={len(remaining_text)}, score={score}")
    print(f"  First 100: {remaining_text[:100]}")
    print()

# Test 3: Read only high-frequency letters (E, M, B) from Pages 2-4
print("-" * 60)
print("TEST 3: Read only E/M/B positions from Pages 2-4")
print("-" * 60)

emb_indices = {18, 19, 17}  # E, M, B
for page_num in [2, 3, 4]:
    plaintext = PLAINTEXTS[page_num]
    indices = text_to_indices(plaintext)
    
    emb_only = [idx for idx in indices if idx in emb_indices]
    non_emb = [idx for idx in indices if idx not in emb_indices]
    
    emb_text = indices_to_text(emb_only)
    non_emb_text = indices_to_text(non_emb)
    
    print(f"Page {page_num}:")
    print(f"  E/M/B section ({len(emb_only)} chars): {emb_text[:60]}...")
    print(f"  Non-E/M/B section ({len(non_emb)} chars, score={score_english(non_emb_text)}): {non_emb_text[:60]}...")
    print()

# Test 4: Vigenere with DIVINITY on first-layer output
print("-" * 60)
print("TEST 4: VIGENERE with DIVINITY on first-layer output")
print("-" * 60)

def vigenere_decrypt(indices, key_word):
    """Apply Vigenere decryption with a keyword"""
    key_indices = text_to_indices(key_word)
    result = []
    for i, idx in enumerate(indices):
        key_idx = key_indices[i % len(key_indices)]
        new_idx = (idx - key_idx) % 29
        result.append(new_idx)
    return result

for key in ['DIVINITY', 'CIRCUMFERENCE', 'INSTAR', 'EMERGE', 'LOSS']:
    print(f"Key: {key}")
    for page_num, plaintext in PLAINTEXTS.items():
        indices = text_to_indices(plaintext)
        new_indices = vigenere_decrypt(indices, key)
        new_text = indices_to_text(new_indices)
        score = score_english(new_text)
        print(f"  Page {page_num}: score={score}, first 50: {new_text[:50]}")
    print()

# Test 5: Read every Nth character
print("-" * 60)
print("TEST 5: SKIP PATTERNS - Read every Nth character")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    print(f"Page {page_num}:")
    indices = text_to_indices(plaintext)
    best_score = 0
    best_n = 0
    best_text = ""
    
    for n in range(2, 8):
        for offset in range(n):
            selected = [indices[i] for i in range(offset, len(indices), n)]
            text = indices_to_text(selected)
            score = score_english(text)
            if score > best_score:
                best_score = score
                best_n = n
                best_offset = offset
                best_text = text
    
    print(f"  Best: every {best_n} starting at offset {best_offset}, score={best_score}")
    print(f"  Text: {best_text[:80]}")
    print()

# Test 6: Interleave extraction (de-interleave)
print("-" * 60)
print("TEST 6: DE-INTERLEAVE - Split into N streams")
print("-" * 60)

for page_num in [0, 1]:  # THE-heavy pages
    plaintext = PLAINTEXTS[page_num]
    indices = text_to_indices(plaintext)
    print(f"Page {page_num}:")
    
    for n_streams in [2, 3, 4]:
        streams = [[] for _ in range(n_streams)]
        for i, idx in enumerate(indices):
            streams[i % n_streams].append(idx)
        
        stream_texts = [indices_to_text(s) for s in streams]
        stream_scores = [score_english(t) for t in stream_texts]
        
        print(f"  {n_streams} streams: scores={stream_scores}")
        for i, (text, score) in enumerate(zip(stream_texts, stream_scores)):
            if score > 100:  # Only show promising streams
                print(f"    Stream {i}: {text[:60]}...")
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

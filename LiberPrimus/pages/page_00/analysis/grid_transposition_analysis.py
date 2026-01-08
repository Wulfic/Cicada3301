#!/usr/bin/env python3
"""
Test grid transposition with Shift(19) which gave the best score (1160) for Page 0.
Also try stripping EMB prefix from Pages 2-4.

Grid transposition: Write text into grid of width W, read by columns
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

def apply_shift(indices, shift):
    """Apply simple shift to all indices"""
    return [(idx + shift) % 29 for idx in indices]

def columnar_read(text, width):
    """Write text row-wise into grid of given width, read column-wise"""
    # Pad text to fill grid
    height = (len(text) + width - 1) // width
    padded = text + 'X' * (height * width - len(text))
    
    # Write into grid
    grid = []
    for i in range(0, len(padded), width):
        grid.append(padded[i:i+width])
    
    # Read by columns
    result = []
    for col in range(width):
        for row in grid:
            if col < len(row):
                result.append(row[col])
    
    return ''.join(result)

def columnar_read_reverse(text, width):
    """Read column-wise assuming text was written column-wise (reverse operation)"""
    height = (len(text) + width - 1) // width
    padded = text + 'X' * (height * width - len(text))
    
    # Write into grid by columns
    grid = [['' for _ in range(width)] for _ in range(height)]
    idx = 0
    for col in range(width):
        for row in range(height):
            if idx < len(padded):
                grid[row][col] = padded[idx]
                idx += 1
    
    # Read by rows
    result = []
    for row in grid:
        result.extend(row)
    
    return ''.join(result)

print("=" * 60)
print("GRID TRANSPOSITION + SHIFT ANALYSIS")
print("=" * 60)
print()

# Test 1: Apply Shift(19) then columnar transposition
print("-" * 60)
print("TEST 1: SHIFT(19) + COLUMNAR READ (Page 0)")
print("-" * 60)

page0_indices = text_to_indices(PLAINTEXTS[0])
shifted_indices = apply_shift(page0_indices, 19)
shifted_text = indices_to_text(shifted_indices)
original_score = score_english(shifted_text)
print(f"After Shift(19): score={original_score}")
print(f"Text: {shifted_text[:80]}...")
print()

# Try different grid widths
best_score = 0
best_width = 0
best_text = ""

for width in range(5, 50):
    transposed = columnar_read(shifted_text, width)
    score = score_english(transposed)
    if score > best_score:
        best_score = score
        best_width = width
        best_text = transposed

print(f"Best columnar width: {best_width}, score: {best_score}")
print(f"Text: {best_text[:100]}...")
print()

# Also try reverse columnar
best_rev_score = 0
best_rev_width = 0
best_rev_text = ""

for width in range(5, 50):
    transposed = columnar_read_reverse(shifted_text, width)
    score = score_english(transposed)
    if score > best_rev_score:
        best_rev_score = score
        best_rev_width = width
        best_rev_text = transposed

print(f"Best reverse columnar width: {best_rev_width}, score: {best_rev_score}")
print(f"Text: {best_rev_text[:100]}...")
print()

# Test 2: Strip EMB prefix from Pages 2-4
print("-" * 60)
print("TEST 2: STRIP EMB PREFIX (Pages 2-4)")
print("-" * 60)

emb_indices = {18, 19, 17}  # E, M, B

for page_num in [2, 3, 4]:
    indices = text_to_indices(PLAINTEXTS[page_num])
    
    # Find where EMB section ends (first non-EMB character after initial EMB run)
    emb_end = 0
    for i, idx in enumerate(indices):
        if idx not in emb_indices:
            # Check if we're past initial EMB section
            emb_count = sum(1 for j in range(i) if indices[j] in emb_indices)
            if emb_count > 10:  # Significant EMB prefix
                emb_end = i
                break
    
    # Also check for transition point (where English-like content starts)
    transition_point = 0
    window = 10
    for i in range(len(indices) - window):
        segment = indices_to_text(indices[i:i+window])
        if score_english(segment) > 20:  # Some English detected
            transition_point = i
            break
    
    full_text = indices_to_text(indices)
    stripped_text = indices_to_text(indices[emb_end:])
    transition_text = indices_to_text(indices[transition_point:])
    
    print(f"Page {page_num}:")
    print(f"  Full length: {len(indices)}, EMB ends at: {emb_end}, Transition at: {transition_point}")
    print(f"  Full score: {score_english(full_text)}")
    print(f"  After EMB ({len(indices)-emb_end} chars, score={score_english(stripped_text)}): {stripped_text[:60]}...")
    print(f"  From transition ({len(indices)-transition_point} chars, score={score_english(transition_text)}): {transition_text[:60]}...")
    print()

# Test 3: Apply Shift(3) to Pages 2-4 and strip EMB
print("-" * 60)
print("TEST 3: SHIFT(3) + STRIP EMB (Pages 2-4)")
print("-" * 60)

for page_num in [2, 3, 4]:
    indices = text_to_indices(PLAINTEXTS[page_num])
    shifted = apply_shift(indices, 3)
    shifted_text = indices_to_text(shifted)
    
    # Find transition point after shift
    transition_point = 0
    window = 10
    for i in range(len(shifted) - window):
        segment = indices_to_text(shifted[i:i+window])
        if score_english(segment) > 20:
            transition_point = i
            break
    
    full_score = score_english(shifted_text)
    transition_text = indices_to_text(shifted[transition_point:])
    transition_score = score_english(transition_text)
    
    print(f"Page {page_num}: Shift(3)")
    print(f"  Full score: {full_score}")
    print(f"  From pos {transition_point} ({len(shifted)-transition_point} chars, score={transition_score}): {transition_text[:80]}...")
    print()

# Test 4: Key lengths as grid widths
print("-" * 60)
print("TEST 4: USE KEY LENGTHS AS GRID WIDTHS")
print("-" * 60)

key_lengths = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

for page_num, plaintext in PLAINTEXTS.items():
    kl = key_lengths[page_num]
    indices = text_to_indices(plaintext)
    
    # Width = key length
    text = indices_to_text(indices)
    col_text = columnar_read(text, kl)
    col_score = score_english(col_text)
    
    rev_text = columnar_read_reverse(text, kl)
    rev_score = score_english(rev_text)
    
    # Width = sqrt(length) approximately
    sqrt_width = int(len(indices) ** 0.5)
    sqrt_text = columnar_read(text, sqrt_width)
    sqrt_score = score_english(sqrt_text)
    
    print(f"Page {page_num}:")
    print(f"  Original: {score_english(text)}")
    print(f"  Width={kl} (key length): {col_score}")
    print(f"  Width={kl} reverse: {rev_score}")
    print(f"  Width={sqrt_width} (sqrt): {sqrt_score}")
    print()

# Test 5: Combine Pages 2-4 post-EMB sections
print("-" * 60)
print("TEST 5: COMBINE POST-EMB SECTIONS OF PAGES 2-4")
print("-" * 60)

combined_indices = []
for page_num in [2, 3, 4]:
    indices = text_to_indices(PLAINTEXTS[page_num])
    
    # Find transition point
    transition_point = 0
    window = 10
    for i in range(len(indices) - window):
        segment = indices_to_text(indices[i:i+window])
        if score_english(segment) > 15:
            transition_point = i
            break
    
    combined_indices.extend(indices[transition_point:])

combined_text = indices_to_text(combined_indices)
print(f"Combined post-EMB: {len(combined_indices)} chars, score={score_english(combined_text)}")
print(f"Text: {combined_text[:150]}...")
print()

# Try grid on combined
best_comb_score = 0
best_comb_width = 0
for width in range(5, 50):
    transposed = columnar_read(combined_text, width)
    score = score_english(transposed)
    if score > best_comb_score:
        best_comb_score = score
        best_comb_width = width

print(f"Best columnar on combined: width={best_comb_width}, score={best_comb_score}")

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

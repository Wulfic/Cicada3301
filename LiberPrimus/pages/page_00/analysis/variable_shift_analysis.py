#!/usr/bin/env python3
"""
Test variable shift patterns - shift amount varies by position.
Also test dictionary-based word extraction from first-layer output.
"""

# Gematria Primus - 29 characters
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S/Z', 'T', 'B', 'E', 'M',
            'L', 'ING', 'OE', 'D', 'A', 'AE', 'Y', 'IA/IO', 'EA']

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
          157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
          239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
          331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
          421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
          509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
          613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
          709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
          821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
          919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
          1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091,
          1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181,
          1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277,
          1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361,
          1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451,
          1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531,
          1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609,
          1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699]

PLAINTEXTS = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"
}

# Common English words for dictionary matching
ENGLISH_WORDS = set([
    'THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'FOR', 'THAT', 'WAS', 'BE', 'AS', 
    'ARE', 'WITH', 'NOT', 'HAS', 'WE', 'THIS', 'HAVE', 'FROM', 'AT', 'OR', 'AN',
    'THEY', 'HE', 'SHE', 'BUT', 'ALL', 'WHICH', 'THERE', 'THEIR', 'WHAT', 'SO',
    'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'HAS', 'BEEN', 'WHEN', 'WILL', 'NO',
    'EACH', 'MAKE', 'MAY', 'THAN', 'THEM', 'MADE', 'FIND', 'WORK', 'MUST', 'INTO',
    'THEN', 'THING', 'THINGS', 'OTHER', 'ITS', 'OUR', 'ONLY', 'THESE', 'THOSE',
    'TRUTH', 'SACRED', 'PRIMES', 'DIVINITY', 'CIRCUMFERENCE', 'EMERGE', 'INSTAR',
    'PARABLE', 'WISDOM', 'KNOWLEDGE', 'JOURNEY', 'PILGRIM', 'WITHIN', 'SURFACE',
    'SHED', 'TUNNEL', 'DEATH', 'LIFE', 'CONSUMPTION', 'PRESERVATION', 'ADHERENCE',
    'BELIEVE', 'NOTHING', 'BOOK', 'EXCEPT', 'KNOW', 'TRUE', 'TEST', 'EXPERIENCE',
    'EDIT', 'CHANGE', 'MESSAGE', 'WORDS', 'NUMBERS', 'END', 'WAY', 'EASY', 'TRIP',
    'NECESSARY', 'WELCOME', 'GREAT', 'TOWARD', 'INSTRUCTION', 'UNREASONABLE',
    'WARNING', 'KOAN', 'LOSS', 'PRACTICES', 'BEHAVIORS', 'CAUSE', 'DOES', 'DOETH',
    'LEARETH', 'UPON', 'AFTER', 'BEFORE', 'THROUGH', 'BEING', 'EARTH', 'HEART',
    'HEAR', 'EAR', 'HEAT', 'THERE', 'HERE', 'WHERE', 'NEAR', 'FEAR', 'YEAR', 'DEAR',
    'HANG', 'RANG', 'SANG', 'THEE', 'THY', 'THINE', 'ART', 'DOTH', 'HATH', 'ETH',
    'GOTO', 'RUNG', 'SONG', 'LONG', 'AMONG', 'ALONG', 'WRONG', 'STRONG', 'YOUNG'
])

def text_to_indices(text):
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
            for j, glyph in enumerate(GEMATRIA):
                if clean[i] in glyph.split('/')[0]:
                    indices.append(j)
                    break
            i += 1
    return indices

def indices_to_text(indices):
    result = []
    for idx in indices:
        idx = idx % 29
        glyph = GEMATRIA[idx]
        if '/' in glyph:
            glyph = glyph.split('/')[0]
        result.append(glyph)
    return ''.join(result)

def score_english(text):
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
print("VARIABLE SHIFT AND DICTIONARY ANALYSIS")
print("=" * 60)
print()

# Test 1: Variable shift by position (shift = i mod 29)
print("-" * 60)
print("TEST 1: VARIABLE SHIFT - shift = i mod 29")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    
    # Forward: subtract i mod 29
    new_sub = [(indices[i] - (i % 29)) % 29 for i in range(len(indices))]
    sub_text = indices_to_text(new_sub)
    sub_score = score_english(sub_text)
    
    # Add i mod 29
    new_add = [(indices[i] + (i % 29)) % 29 for i in range(len(indices))]
    add_text = indices_to_text(new_add)
    add_score = score_english(add_text)
    
    print(f"Page {page_num}: -i mod 29 score={sub_score}, +i mod 29 score={add_score}")
    if sub_score > add_score:
        print(f"  Best (-i): {sub_text[:70]}...")
    else:
        print(f"  Best (+i): {add_text[:70]}...")
    print()

# Test 2: Shift by prime[i] mod 29
print("-" * 60)
print("TEST 2: VARIABLE SHIFT - shift = prime[i] mod 29")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    
    new_sub = [(indices[i] - (PRIMES[i] % 29)) % 29 for i in range(len(indices))]
    sub_text = indices_to_text(new_sub)
    sub_score = score_english(sub_text)
    
    new_add = [(indices[i] + (PRIMES[i] % 29)) % 29 for i in range(len(indices))]
    add_text = indices_to_text(new_add)
    add_score = score_english(add_text)
    
    print(f"Page {page_num}: -prime[i] mod 29 score={sub_score}, +prime[i] mod 29 score={add_score}")
    best = sub_text if sub_score > add_score else add_text
    print(f"  Best: {best[:70]}...")
    print()

# Test 3: Shift by Fibonacci sequence mod 29
print("-" * 60)
print("TEST 3: VARIABLE SHIFT - shift = fib[i] mod 29")
print("-" * 60)

def fib_up_to(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

fibs = fib_up_to(300)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    
    new_sub = [(indices[i] - (fibs[i] % 29)) % 29 for i in range(len(indices))]
    sub_text = indices_to_text(new_sub)
    sub_score = score_english(sub_text)
    
    print(f"Page {page_num}: -fib[i] mod 29 score={sub_score}")
    print(f"  Text: {sub_text[:70]}...")
    print()

# Test 4: Dictionary word extraction
print("-" * 60)
print("TEST 4: DICTIONARY WORD EXTRACTION")
print("-" * 60)

def find_all_words(text, min_len=3):
    """Find all valid English words in text"""
    text = text.upper()
    found = {}
    for word in ENGLISH_WORDS:
        if len(word) >= min_len:
            count = text.count(word)
            if count > 0:
                found[word] = count
    return found

for page_num, plaintext in PLAINTEXTS.items():
    words = find_all_words(plaintext)
    sorted_words = sorted(words.items(), key=lambda x: (-len(x[0]), -x[1]))
    
    print(f"Page {page_num}: Found {len(words)} dictionary words")
    # Show longest words first
    long_words = [(w, c) for w, c in sorted_words if len(w) >= 4]
    print(f"  4+ char words: {long_words[:15]}")
    print()

# Test 5: Sliding window word search
print("-" * 60)
print("TEST 5: SLIDING WINDOW - Find runs of valid words")
print("-" * 60)

def score_window(text, window_size=20):
    """Score how many dictionary words are in a sliding window"""
    best_score = 0
    best_pos = 0
    best_text = ""
    
    for i in range(len(text) - window_size):
        window = text[i:i+window_size]
        score = sum(window.count(w) * len(w) for w in ENGLISH_WORDS if w in window)
        if score > best_score:
            best_score = score
            best_pos = i
            best_text = window
    
    return best_pos, best_score, best_text

for page_num, plaintext in PLAINTEXTS.items():
    pos, score, text = score_window(plaintext, 40)
    print(f"Page {page_num}: Best 40-char window at pos {pos}")
    print(f"  Score: {score}, Text: '{text}'")
    print()

# Test 6: Rail fence cipher
print("-" * 60)
print("TEST 6: RAIL FENCE CIPHER (2-5 rails)")
print("-" * 60)

def rail_fence_decrypt(text, rails):
    """Decrypt rail fence cipher"""
    n = len(text)
    if rails <= 1 or rails >= n:
        return text
    
    # Calculate pattern lengths
    cycle = 2 * (rails - 1)
    result = [''] * n
    
    index = 0
    for rail in range(rails):
        step1 = 2 * (rails - 1 - rail) if rail != rails - 1 else cycle
        step2 = 2 * rail if rail != 0 else cycle
        
        pos = rail
        use_step1 = True
        
        while pos < n and index < n:
            result[pos] = text[index]
            index += 1
            if use_step1:
                pos += step1 if step1 else step2
            else:
                pos += step2 if step2 else step1
            use_step1 = not use_step1
    
    return ''.join(result)

for page_num in [0, 1]:
    plaintext = PLAINTEXTS[page_num]
    print(f"Page {page_num}:")
    for rails in range(2, 6):
        decrypted = rail_fence_decrypt(plaintext, rails)
        score = score_english(decrypted)
        print(f"  {rails} rails: score={score}, text: {decrypted[:50]}...")
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

#!/usr/bin/env python3
"""
Test the Totient function hint from Onion pages:
"THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED"

Euler's totient function φ(n) counts integers 1..n that are coprime to n.
For prime p: φ(p) = p - 1

Theories to test:
1. Apply totient to indices: new_index = φ(index)
2. Use totient values as key
3. Map positions based on totient of position number
4. Use totient of the Gematria prime values
"""

# Gematria Primus - 29 characters
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S/Z', 'T', 'B', 'E', 'M',
            'L', 'ING', 'OE', 'D', 'A', 'AE', 'Y', 'IA/IO', 'EA']

PRIME_VALUES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                73, 79, 83, 89, 97, 101, 103, 107, 109]

def totient(n):
    """Euler's totient function"""
    if n < 1:
        return 0
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def get_primes_up_to(n):
    """Get list of primes up to n"""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

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
            # Single character fallback
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
            # Use first variant if there are options
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
print("TOTIENT FUNCTION ANALYSIS")
print("=" * 60)
print()

# Precompute totients
totients = [totient(i) for i in range(300)]
primes = get_primes_up_to(300)

print("First 30 totient values:")
print([totient(i) for i in range(30)])
print()

print("Totient of first 29 primes (Gematria prime values):")
prime_totients = [totient(p) for p in PRIME_VALUES]
print(prime_totients)
print("(Note: φ(prime) = prime - 1)")
print()

# Theory 1: Replace each index with φ(index)
print("-" * 60)
print("THEORY 1: Apply φ(index) to each character position")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    new_indices = [totient(idx + 1) % 29 for idx in indices]  # +1 because φ(0)=0
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Theory 2: Apply φ to the Gematria prime value at each position
print("-" * 60)
print("THEORY 2: Use φ(prime_value[index]) as new index")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    new_indices = []
    for idx in indices:
        if 0 <= idx < 29:
            pv = PRIME_VALUES[idx]
            phi = totient(pv)
            new_idx = phi % 29
            new_indices.append(new_idx)
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Theory 3: Read only positions where position is a totient
print("-" * 60)
print("THEORY 3: Read chars at positions that are totient values")
print("-" * 60)

totient_positions = set(totients[:100])  # Totient values up to φ(100)
for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    selected = [GEMATRIA[indices[i]] for i in range(len(indices)) if i in totient_positions]
    result = ''.join(selected)
    print(f"Page {page_num}: {''.join(selected[:80])}")
print()

# Theory 4: Use position mod totient(key_length)
print("-" * 60)
print("THEORY 4: Position mod φ(key_length) as key stream")
print("-" * 60)

key_lengths = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}
for page_num, plaintext in PLAINTEXTS.items():
    kl = key_lengths[page_num]
    phi_kl = totient(kl)
    indices = text_to_indices(plaintext)
    
    # Generate key: position mod φ(key_length)
    key = [i % phi_kl for i in range(len(indices))]
    new_indices = [(indices[i] - key[i]) % 29 for i in range(len(indices))]
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: φ({kl})={phi_kl}, score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Theory 5: Totient of prime at each position as offset
print("-" * 60)
print("THEORY 5: φ(prime[position]) as shift key")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    new_indices = []
    for i, idx in enumerate(indices):
        prime_i = primes[i % len(primes)]
        phi_prime = totient(prime_i)
        new_idx = (idx - phi_prime) % 29
        new_indices.append(new_idx)
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

# Theory 6: Totient sequence as key
print("-" * 60)
print("THEORY 6: Totient sequence [φ(1), φ(2), ...] as key")
print("-" * 60)

for page_num, plaintext in PLAINTEXTS.items():
    indices = text_to_indices(plaintext)
    key = [totient(i+1) for i in range(len(indices))]
    new_indices = [(indices[i] - key[i]) % 29 for i in range(len(indices))]
    new_text = indices_to_text(new_indices)
    score = score_english(new_text)
    print(f"Page {page_num}: score={score}")
    print(f"  First 100: {new_text[:100]}")
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

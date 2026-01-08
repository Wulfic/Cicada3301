#!/usr/bin/env python3
"""
Prime Position Analysis
=======================
"THE PRIMES ARE SACRED" - what if we read characters at prime positions?
Also test Fibonacci, perfect square, and other mathematical sequences.
"""

import math

# First layer outputs
PAGE0 = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

PAGE1 = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTOOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

PAGE2_ENGLISH = "THICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE"

PAGE3_ENGLISH = "THEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE"

PAGE4_ENGLISH = "THEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_up_to(n):
    return [i for i in range(2, n) if is_prime(i)]

def get_fibonacci_up_to(n):
    fibs = [1, 2]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    return [f for f in fibs if f < n]

def get_squares_up_to(n):
    return [i*i for i in range(1, int(math.sqrt(n)) + 1) if i*i < n]

def get_triangular_up_to(n):
    return [i*(i+1)//2 for i in range(1, n) if i*(i+1)//2 < n]

def extract_at_positions(text, positions):
    """Extract characters at given positions (0-indexed)."""
    return ''.join(text[p] if p < len(text) else '' for p in positions)

def analyze_with_sequence(text, name, positions, seq_name):
    """Extract and analyze characters at sequence positions."""
    result = extract_at_positions(text, positions)
    # Remove any special characters
    result = result.replace('/', '')
    return result

def main():
    print("=" * 60)
    print("PRIME AND MATHEMATICAL POSITION ANALYSIS")
    print("=" * 60)
    
    texts = [
        ("Page 0", PAGE0),
        ("Page 1", PAGE1),
        ("Page 2 English", PAGE2_ENGLISH),
        ("Page 3 English", PAGE3_ENGLISH),
        ("Page 4 English", PAGE4_ENGLISH),
    ]
    
    # Get sequences
    max_len = max(len(t) for _, t in texts)
    primes = get_primes_up_to(max_len)
    fibs = get_fibonacci_up_to(max_len)
    squares = get_squares_up_to(max_len)
    triangular = get_triangular_up_to(max_len)
    
    # 0-indexed versions
    primes_0 = [p - 1 for p in primes]  # Convert to 0-indexed
    fibs_0 = [f - 1 for f in fibs]
    squares_0 = [s - 1 for s in squares]
    
    print(f"\nPrime positions (1-indexed): {primes[:20]}...")
    print(f"Fibonacci positions: {fibs[:15]}...")
    print(f"Square positions: {squares[:15]}...")
    
    sequences = [
        ("Prime (1-indexed)", primes_0),
        ("Fibonacci", fibs_0),
        ("Squares", squares_0),
        ("Non-prime", [i for i in range(max_len) if i+1 not in primes]),
    ]
    
    for name, text in texts:
        print(f"\n{'='*60}")
        print(f"{name} (length {len(text)})")
        print("="*60)
        
        for seq_name, positions in sequences:
            result = analyze_with_sequence(text, name, positions, seq_name)
            print(f"\n{seq_name} positions:")
            print(f"  {result[:60]}...")
    
    # Combined primes across all pages
    print("\n" + "=" * 60)
    print("PRIME POSITIONS - ALL PAGES COMBINED")
    print("=" * 60)
    
    all_primes = []
    for name, text in texts:
        result = extract_at_positions(text, primes_0)
        all_primes.append(result)
        print(f"{name}: {result}")
    
    # Concatenate prime-position characters
    concat_primes = ''.join(all_primes)
    print(f"\nAll prime-position chars concatenated ({len(concat_primes)} chars):")
    print(concat_primes)
    
    # Look for common words
    words = ['THE', 'AND', 'THAT', 'FIND', 'EMERGE', 'SHED', 'MUST', 
             'WITHIN', 'DIVINITY', 'CIRCUMFERENCE', 'INSTAR', 'SURFACE',
             'LIKE', 'TUNNELING', 'WE', 'OUR', 'OWN', 'PRIMES', 'SACRED']
    
    print("\nLooking for known words...")
    for word in words:
        if word in concat_primes:
            print(f"  Found: {word}")
    
    # Try prime-th character from each THE segment
    print("\n" + "=" * 60)
    print("PRIME-TH CHARACTER FROM EACH 'THE' SEGMENT")
    print("=" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        segments = text.split('THE')
        prime_chars = []
        
        for i, segment in enumerate(segments):
            if i < len(primes):
                prime_idx = primes[i] - 1  # 0-indexed position in segment
                if prime_idx < len(segment):
                    prime_chars.append(segment[prime_idx])
                elif len(segment) > 0:
                    prime_chars.append(segment[-1])  # fallback to last char
        
        print(f"{name}: {''.join(prime_chars)}")
    
    # Every Nth prime position
    print("\n" + "=" * 60)
    print("TESTING DIFFERENT PRIME SKIP PATTERNS")
    print("=" * 60)
    
    concat_all = ''.join(t for _, t in texts)
    
    for skip in [2, 3, 5, 7]:
        result = extract_at_positions(concat_all, primes_0[::skip])
        print(f"Every {skip}th prime: {result[:50]}...")
    
    # Gematria prime values (2, 3, 5, 7, 11, 13, 17, 19, 23, 29...)
    gematria_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                       53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    print("\n" + "=" * 60)
    print("GEMATRIA PRIME VALUE POSITIONS")
    print("=" * 60)
    
    for name, text in texts:
        gp_0 = [p - 1 for p in gematria_primes if p <= len(text)]
        result = extract_at_positions(text, gp_0)
        print(f"{name}: {result}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Manual Analysis of Page 0 First-Layer Output.

Taking a careful look at the text to find meaningful word boundaries
by human pattern recognition, not just dictionary matching.
"""

# Page 0 first-layer output
TEXT = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKKHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

# Let me manually identify possible word boundaries
# Looking for common patterns:
# - THE appears frequently
# - DOETH, GOETH are Old English verb forms
# - HATH is a verb
# - Pronouns: THY, THEE, THOU

def find_all_occurrences(text, pattern):
    """Find all positions where pattern occurs."""
    positions = []
    start = 0
    while True:
        pos = text.find(pattern, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions

def analyze():
    print("Manual Analysis of Page 0 First-Layer Output")
    print("=" * 70)
    print(f"\nText length: {len(TEXT)} characters")
    print(f"\nText: {TEXT}")
    
    # Find key patterns
    patterns = [
        'THE', 'DOETH', 'GOETH', 'HATH', 'LETHE', 'LEARETH',
        'THY', 'THEE', 'THOU', 'THERE', 'THEN', 'THAT',
        'AE', 'EA', 'TH', 'NG', 'IA', 'OE', 'EO',
        'AND', 'OF', 'IN', 'ON', 'AT', 'TO', 'IT',
        'ART', 'EST', 'ETH',
    ]
    
    print("\n" + "=" * 70)
    print("Pattern occurrences:")
    print("=" * 70)
    
    for pattern in sorted(patterns, key=lambda x: -len(x)):
        positions = find_all_occurrences(TEXT, pattern)
        if positions:
            print(f"{pattern}: {len(positions)}x at positions {positions[:10]}{'...' if len(positions) > 10 else ''}")
    
    # Let me try to parse this manually by looking at the structure
    print("\n" + "=" * 70)
    print("Attempt at manual word boundary identification:")
    print("=" * 70)
    
    # The text seems to have "AE THAT A EYE THE ST HE S THE AE A THE OR NG..."
    # But that doesn't make sense. Let's try another approach.
    
    # What if the digraphs (TH, NG, EA, AE, IA, EO, OE) are single runes
    # and we're seeing them as patterns?
    
    # Let me look at consecutive THE patterns
    print("\nSections between THE occurrences:")
    the_positions = find_all_occurrences(TEXT, 'THE')
    
    for i in range(min(15, len(the_positions))):
        start = the_positions[i]
        if i + 1 < len(the_positions):
            end = the_positions[i + 1]
            section = TEXT[start:end]
        else:
            section = TEXT[start:start+20]
        print(f"  {i}: {section}")
    
    # Look for Old English verbs
    print("\n" + "=" * 70)
    print("Old English verbs found:")
    print("=" * 70)
    
    verbs = ['DOETH', 'GOETH', 'HATH', 'DOTH', 'SAITH', 'TAKETH', 
             'MAKETH', 'COMETH', 'SEEKETH', 'FINDETH', 'KNOWETH']
    
    for verb in verbs:
        positions = find_all_occurrences(TEXT, verb)
        if positions:
            for pos in positions:
                context = TEXT[max(0, pos-10):pos+len(verb)+10]
                print(f"  {verb} at {pos}: ...{context}...")
    
    # Try to build sentences by looking at context around key words
    print("\n" + "=" * 70)
    print("Context analysis:")
    print("=" * 70)
    
    # "AETHATAEYETHEST" at start
    print("\nStart of text: AETHATAEYETHEST")
    print("  Possible: AE THAT A EYE THEST (thirst? test?)")
    print("  Or: AE THAT AE YE THEST")
    print("  Or: A ETHA TAE YET HEST")
    
    # "DOETH" at position 110
    doeth_pos = TEXT.find('DOETH')
    print(f"\nAround DOETH ({doeth_pos}): {TEXT[max(0,doeth_pos-15):doeth_pos+20]}")
    print("  Possible: ...MING DOETH EST HI THE ON THE ATH LA THE...")
    
    # "GOETH" at position 164
    goeth_pos = TEXT.find('GOETH')
    print(f"\nAround GOETH ({goeth_pos}): {TEXT[max(0,goeth_pos-15):goeth_pos+20]}")
    
    # "HATH" at position 279
    hath_pos = TEXT.find('HATH')
    print(f"\nAround HATH ({hath_pos}): {TEXT[max(0,hath_pos-15):hath_pos+20]}")
    
    # Check for THERE AN UP
    there_pos = TEXT.find('THEREANUP')
    if there_pos >= 0:
        print(f"\nAround THEREANUP ({there_pos}): {TEXT[max(0,there_pos-15):there_pos+25]}")
        print("  This could be: THERE AN UP (a clear phrase!)")
    
    # Look for complete phrases
    print("\n" + "=" * 70)
    print("Potential complete phrases/sentences:")
    print("=" * 70)
    
    # Known Cicada phrases
    cicada_phrases = [
        "DIVINITY", "CIRCUMFERENCE", "SACRED", "PRIMES", "TOTIENT",
        "WISDOM", "JOURNEY", "PILGRIM", "INSTAR", "EMERGE",
        "BELIEVE NOTHING", "TEST THE KNOWLEDGE", "FIND YOUR TRUTH"
    ]
    
    for phrase in cicada_phrases:
        if phrase.replace(' ', '') in TEXT:
            print(f"  Found: {phrase}")
    
    # Look at character after each THE
    print("\n" + "=" * 70)
    print("Characters following THE:")
    print("=" * 70)
    
    the_next = []
    for pos in the_positions:
        if pos + 3 < len(TEXT):
            next_chars = TEXT[pos+3:pos+8]
            the_next.append(next_chars)
    
    for i, chars in enumerate(the_next[:20]):
        print(f"  THE{chars}")

if __name__ == "__main__":
    analyze()

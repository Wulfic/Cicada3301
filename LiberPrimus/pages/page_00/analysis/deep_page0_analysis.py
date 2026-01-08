#!/usr/bin/env python3
"""
Deep dive into Page 0 - trying to extract actual readable text.

Based on analysis:
- "THEREANUP" = "THERE AN UP" (clear phrase)
- DOETH, GOETH, HATH are present
- Heavy THE pattern

Let me try to manually parse sections and see if coherent text emerges.
"""

TEXT = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKKHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

# Try to parse this as if THE is not a word but part of words
# What if this is just heavily THE-infused text?

def try_parse_around_verbs():
    """Parse sections around known verbs."""
    
    print("=" * 70)
    print("PARSING AROUND KNOWN OLD ENGLISH VERBS")
    print("=" * 70)
    
    # DOETH at 110
    print("\n1. Around DOETH (pos 110):")
    section = TEXT[95:140]
    print(f"   Raw: {section}")
    # THEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLA
    # THE AD THE O TH BT MING DOETH EST HI THE ON THE ATH LA
    # Or: THEADTH EOTHBT MING DOETH EST HI THEON THE ATH LA
    print("   Parse attempt: THE AD THE OTH BT MING DOETH EST HI THE ON THE ATH LA")
    print("   Meaning: ? ... (something) MING DOETH (does) EST (is?) HI (high?) THE ON THE ...")
    
    # GOETH at 183
    print("\n2. Around GOETH (pos 183):")
    section = TEXT[168:210]
    print(f"   Raw: {section}")
    # EESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANT
    print("   Parse attempt: EES THE O THE A THE A GOETH N THE O C KLY D THE AX THANT")
    
    # HATH at 258
    print("\n3. Around HATH (pos 258):")
    section = TEXT[243:285]
    print(f"   Raw: {section}")
    # NTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHE
    print("   Parse attempt: N THE O THE ATH ING N THE OF HATH EN THE AS TH WIAS THE")
    print("   Better: ...THE OF HATH EN THE AS TH WI AS THE...")
    
    # THERE AN UP at 229
    print("\n4. THERE AN UP (pos 229-240):")
    section = TEXT[214:255]
    print(f"   Raw: {section}")
    # ADTHTHEATHAESIGTHEREANUPTTHEOTHEATHING
    print("   Parse: AD TH THE ATHAESIG THERE AN UPT THE O THE ATHING")
    print("   Better: ...ATHAESIG THERE AN UP T THE O THE ATHING...")
    
def try_different_segmentation():
    """Try a completely different approach - what if THE is part of other words?"""
    
    print("\n" + "=" * 70)
    print("ALTERNATIVE: THE AS PART OF WORDS")
    print("=" * 70)
    
    # What words contain THE?
    the_words = [
        'ATHEIST', 'ETHER', 'WEATHER', 'FEATHER', 'LEATHER', 'WHETHER',
        'GATHER', 'FATHER', 'MOTHER', 'BROTHER', 'OTHER', 'BOTHER',
        'RATHER', 'HITHER', 'THITHER', 'EITHER', 'NEITHER',
        'TOGETHER', 'ALTOGETHER', 'ANOTHER',
        'THEMSELVES', 'THEMSELVES', 
        'NONETHELESS', 'NEVERTHELESS',
        'CLOTHE', 'BREATHE', 'SOOTHE', 'BATHE',
        'THESE', 'THOSE', 'THENCE', 'THINE', 'THERE', 'THEIR',
        'THEOREM', 'THEORY', 'THERAPY', 'THEME',
    ]
    
    # Check which appear
    found = []
    for word in the_words:
        if word in TEXT:
            found.append(word)
    
    print(f"Words containing THE found: {found}")
    
    # What about partial matches?
    print("\nLooking for word fragments:")
    
    fragments = [
        ('ESTHE', 'ESTHESIA/ESTHETIC?'),
        ('THEA', 'THEATER? THE A?'),
        ('OTHE', 'OTHER? O THE?'),
        ('ATHE', 'ATHEIST? A THE?'),
    ]
    
    for frag, meaning in fragments:
        count = TEXT.count(frag)
        if count > 0:
            print(f"  {frag}: {count}x - possible: {meaning}")

def analyze_positions():
    """Analyze positions and gaps."""
    
    print("\n" + "=" * 70)
    print("POSITION ANALYSIS")
    print("=" * 70)
    
    # Find all THE positions
    positions = []
    start = 0
    while True:
        pos = TEXT.find('THE', start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    # Calculate gaps
    gaps = []
    for i in range(1, len(positions)):
        gap = positions[i] - positions[i-1]
        gaps.append(gap)
    
    print(f"THE positions: {len(positions)} occurrences")
    print(f"Average gap: {sum(gaps)/len(gaps):.1f} chars")
    print(f"Gap distribution: min={min(gaps)}, max={max(gaps)}")
    
    # Check if gaps encode something
    print(f"\nFirst 20 gaps: {gaps[:20]}")
    print(f"Gap mod 29: {[g % 29 for g in gaps[:20]]}")

def check_if_real_english():
    """Check if the text could be real English with noise."""
    
    print("\n" + "=" * 70)
    print("IS THIS REAL ENGLISH?")
    print("=" * 70)
    
    # Try removing all THE and see what's left
    without_the = TEXT.replace('THE', ' ')
    print(f"\nWith THE removed (replaced by space):")
    print(without_the)
    
    # Count meaningful words in this
    meaningful = ['AND', 'THAT', 'DOETH', 'GOETH', 'HATH', 'THY', 'OF', 'IN', 'ON', 
                  'THERE', 'THEN', 'AN', 'UP', 'EST', 'ART']
    
    print(f"\nMeaningful words still present:")
    for word in meaningful:
        if word in without_the:
            print(f"  {word}: yes")

def look_for_sentences():
    """Try to find sentence structures."""
    
    print("\n" + "=" * 70)
    print("LOOKING FOR SENTENCE STRUCTURES")
    print("=" * 70)
    
    # Common sentence patterns in Old English/Biblical:
    # "X DOETH Y" - subject does action
    # "THE X OF Y" - possessive
    # "THERE IS/ARE" - existential
    # "HATH X" - has X
    
    # Find "DOETH" and look for subject before it
    doeth_pos = TEXT.find('DOETH')
    if doeth_pos > 0:
        before = TEXT[max(0, doeth_pos-20):doeth_pos]
        after = TEXT[doeth_pos+5:doeth_pos+25]
        print(f"\nDOETH context:")
        print(f"  Before: ...{before}")
        print(f"  After: {after}...")
        print(f"  Possible: MING DOETH EST HI THE ON")
        print(f"  Meaning: ? [subject] DOETH (does) ?")
    
    # "OF HATH"
    of_hath = TEXT.find('OFHATH')
    if of_hath >= 0:
        context = TEXT[of_hath-15:of_hath+15]
        print(f"\nOF HATH: ...{context}...")
    
    # Check for "THE OF" - strange in English
    the_of = TEXT.find('THEOF')
    if the_of >= 0:
        print(f"\nTHE OF at {the_of}: {TEXT[the_of-5:the_of+15]}")
        print("  This is grammatically odd - suggests THE isn't always a word")

def main():
    print("Deep Analysis of Page 0 First-Layer Output")
    print("=" * 70)
    print(f"\nFull text ({len(TEXT)} chars):")
    print(TEXT)
    
    try_parse_around_verbs()
    try_different_segmentation()
    analyze_positions()
    check_if_real_english()
    look_for_sentences()
    
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
1. THE appears 47 times - this is excessive for normal text
2. Old English verbs (DOETH, GOETH, HATH) are present
3. "THERE AN UP" is a clear phrase at position 229
4. The text has English-like patterns but is heavily fragmented
5. THE might be:
   a) An actual word that's over-represented
   b) Part of other words (ETHER, OTHER, etc.)
   c) A result of the cipher producing T-H-E frequently
6. The gaps between THE occurrences don't show obvious patterns
7. There may be a transposition or interleaving we haven't detected
    """)

if __name__ == "__main__":
    main()

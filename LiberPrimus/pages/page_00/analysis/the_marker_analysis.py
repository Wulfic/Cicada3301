#!/usr/bin/env python3
"""
THE Marker Analysis
===================
Theory: THE is used as a marker/separator, and the message is encoded
in what comes between the THEs or in specific positions relative to THE.
"""

# First layer outputs (THE-heavy pages)
PAGE0 = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

PAGE1 = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTOOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

def split_on_the(text):
    """Split text on THE and return segments."""
    return text.split('THE')

def get_chars_after_the(text, n=1):
    """Get first N characters after each THE."""
    parts = text.split('THE')
    result = []
    for part in parts[1:]:  # Skip first part (before first THE)
        if len(part) >= n:
            result.append(part[:n])
    return result

def get_chars_before_the(text, n=1):
    """Get last N characters before each THE."""
    parts = text.split('THE')
    result = []
    for part in parts[:-1]:  # Skip last part (after last THE)
        if len(part) >= n:
            result.append(part[-n:])
    return result

def analyze_the_patterns(text, name):
    """Analyze patterns around THE markers."""
    print(f"\n{'='*60}")
    print(f"{name} - THE Pattern Analysis")
    print(f"{'='*60}")
    
    parts = split_on_the(text)
    print(f"Parts (split on THE): {len(parts)}")
    
    # First chars after THE
    first_1 = get_chars_after_the(text, 1)
    first_2 = get_chars_after_the(text, 2)
    first_3 = get_chars_after_the(text, 3)
    
    print(f"\nFirst 1 char after each THE: {''.join(first_1)}")
    print(f"First 2 chars after each THE: {' '.join(first_2)}")
    
    # Last chars before THE
    last_1 = get_chars_before_the(text, 1)
    last_2 = get_chars_before_the(text, 2)
    
    print(f"\nLast 1 char before each THE: {''.join(last_1)}")
    print(f"Last 2 chars before each THE: {' '.join(last_2)}")
    
    # Segment lengths
    lengths = [len(p) for p in parts]
    print(f"\nSegment lengths: {lengths}")
    
    # Try interpreting lengths as letters (length mod 26 = A-Z)
    length_letters = ''.join(chr(65 + (l % 26)) for l in lengths)
    print(f"Lengths as letters (mod 26): {length_letters}")
    
    # Try interpreting as Gematria indices (mod 29)
    INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                       'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                       'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
    length_gematria = ''.join(INDEX_TO_LETTER[l % 29] for l in lengths)
    print(f"Lengths as Gematria (mod 29): {length_gematria}")
    
    return first_1, first_2, lengths

def try_segment_acrostic(parts, position='first'):
    """Try reading acrostic from segments."""
    if position == 'first':
        return ''.join(p[0] if p else '' for p in parts)
    elif position == 'last':
        return ''.join(p[-1] if p else '' for p in parts)
    elif position == 'middle':
        return ''.join(p[len(p)//2] if p else '' for p in parts)

def main():
    print("THE MARKER ANALYSIS")
    print("=" * 60)
    
    # Analyze both pages
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        first_1, first_2, lengths = analyze_the_patterns(text, name)
    
    # Combined analysis
    print("\n" + "=" * 60)
    print("COMBINED ANALYSIS")
    print("=" * 60)
    
    # Concatenate first chars after THE from both pages
    p0_first = ''.join(get_chars_after_the(PAGE0, 1))
    p1_first = ''.join(get_chars_after_the(PAGE1, 1))
    
    print(f"\nPage 0 - First char after each THE ({len(p0_first)} chars): {p0_first}")
    print(f"Page 1 - First char after each THE ({len(p1_first)} chars): {p1_first}")
    
    # Try interleaving the first-char results
    print(f"\nInterleaved: ", end='')
    combined = []
    for i in range(max(len(p0_first), len(p1_first))):
        if i < len(p0_first):
            combined.append(p0_first[i])
        if i < len(p1_first):
            combined.append(p1_first[i])
    print(''.join(combined))
    
    # Check for words in first-char results
    print("\n" + "-" * 60)
    print("LOOKING FOR WORDS")
    print("-" * 60)
    
    words = ['LIKE', 'THE', 'INSTAR', 'TUNNELING', 'SURFACE', 'WE', 'MUST', 
             'SHED', 'OUR', 'OWN', 'CIRCUMFERENCES', 'FIND', 'DIVINITY',
             'WITHIN', 'AND', 'EMERGE', 'WARN', 'BELIEVE', 'NOTHING', 'TRUE',
             'WISDOM', 'PRIMES', 'SACRED', 'TOTIENT']
    
    for result in [p0_first, p1_first, ''.join(combined)]:
        found = []
        for word in words:
            if word in result:
                found.append(word)
        if found:
            print(f"Found in '{result[:30]}...': {found}")
    
    # Analyze segment content
    print("\n" + "-" * 60)
    print("SEGMENT ANALYSIS")
    print("-" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        parts = split_on_the(text)
        
        print(f"\n{name} segments:")
        for i, part in enumerate(parts[:10]):
            print(f"  {i}: '{part}'")
        
        # Try acrostic reading
        acro_first = try_segment_acrostic(parts, 'first')
        acro_last = try_segment_acrostic(parts, 'last')
        
        print(f"\n  First letters of segments: {acro_first}")
        print(f"  Last letters of segments: {acro_last}")
    
    # The A pattern
    print("\n" + "-" * 60)
    print("THE 'A' PATTERN (THEA appears often)")
    print("-" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        thea_count = text.count('THEA')
        the_count = text.count('THE')
        print(f"{name}: THE={the_count}, THEA={thea_count}, ratio={thea_count/the_count:.2f}")
        
        # What follows THEA?
        after_thea = []
        idx = 0
        while True:
            pos = text.find('THEA', idx)
            if pos == -1:
                break
            if pos + 4 < len(text):
                after_thea.append(text[pos+4:pos+6])
            idx = pos + 1
        
        print(f"  After THEA: {after_thea}")

if __name__ == "__main__":
    main()

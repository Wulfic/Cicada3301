#!/usr/bin/env python3
"""
Second Layer Analysis
=====================
Try to decode the second layer of encryption on Pages 0-4.
Based on observations:
- Pages 0,1: Heavy THE patterns, looks like English with noise
- Pages 2,3,4: Heavy EMB patterns at start, then transitions to English-like

Theories to test:
1. THE pattern extraction - maybe THE is a marker/separator
2. Remove THE patterns and analyze remaining text
3. Look at what letters appear between THE instances
4. Check if EMB at start of Pages 2-4 encode metadata
"""

# First layer decrypted plaintext
PAGE0 = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

PAGE1 = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTOOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

PAGE2 = "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE"

PAGE3 = "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE"

PAGE4 = "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"

def extract_between_the(text):
    """Extract text segments between THE patterns."""
    parts = text.split('THE')
    # Filter meaningful parts (length 2-15, not just single chars)
    meaningful = [p for p in parts if 2 <= len(p) <= 15 and not all(c == 'E' for c in p)]
    return meaningful

def remove_the_patterns(text):
    """Remove all THE patterns and see what's left."""
    return text.replace('THE', '')

def analyze_emb_section(text):
    """Analyze EMB-heavy section at start of Pages 2-4."""
    # Find where EMB pattern ends and English-like begins
    # Look for first occurrence of "TH" pattern
    
    for i in range(len(text) - 1):
        if text[i:i+2] == 'TH':
            return text[:i], text[i:]
    
    return text, ""

def letter_to_index():
    """Get letter to Gematria index mapping."""
    INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                       'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                       'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
    
    mapping = {}
    for i, letter in enumerate(INDEX_TO_LETTER):
        mapping[letter] = i
    return mapping

def try_vigenere_on_between_the(text, key):
    """Try Vigenère decryption on text between THE markers."""
    INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N',
                       'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                       'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
    
    LETTER_TO_INDEX = {letter: i for i, letter in enumerate(INDEX_TO_LETTER)}
    
    # Convert text to indices (simple single-char mapping)
    simple_map = {'F': 0, 'U': 1, 'O': 3, 'R': 4, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
                  'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 
                  'E': 18, 'M': 19, 'L': 20, 'D': 23, 'A': 24, 'Y': 26}
    
    key_indices = [simple_map.get(c, 0) for c in key]
    
    result = []
    ki = 0
    for char in text:
        if char in simple_map:
            idx = simple_map[char]
            new_idx = (idx - key_indices[ki % len(key_indices)]) % 29
            # Find letter for new_idx
            for letter, val in simple_map.items():
                if val == new_idx:
                    result.append(letter)
                    break
            else:
                result.append('?')
            ki += 1
        else:
            result.append(char)
    
    return ''.join(result)

def main():
    print("=" * 60)
    print("SECOND LAYER ANALYSIS")
    print("=" * 60)
    
    # Theory 1: THE as separator
    print("\n" + "=" * 60)
    print("THEORY 1: Text between THE markers")
    print("=" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        segments = extract_between_the(text)
        print(f"\n{name}:")
        print(f"  Segments: {segments[:15]}...")
        
        # Try concatenating first letters
        first_letters = ''.join(s[0] if s else '' for s in segments)
        print(f"  First letters: {first_letters}")
        
        # Try last letters
        last_letters = ''.join(s[-1] if s else '' for s in segments)
        print(f"  Last letters: {last_letters}")
    
    # Theory 2: Remove THE and analyze
    print("\n" + "=" * 60)
    print("THEORY 2: Text with THE removed")
    print("=" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        cleaned = remove_the_patterns(text)
        print(f"\n{name}:")
        print(f"  Original length: {len(text)}")
        print(f"  After removing THE: {len(cleaned)}")
        print(f"  Cleaned text: {cleaned[:100]}...")
    
    # Theory 3: EMB prefix analysis for Pages 2-4
    print("\n" + "=" * 60)
    print("THEORY 3: EMB Prefix Analysis (Pages 2-4)")
    print("=" * 60)
    
    for name, text in [("Page 2", PAGE2), ("Page 3", PAGE3), ("Page 4", PAGE4)]:
        emb_section, english_section = analyze_emb_section(text)
        print(f"\n{name}:")
        print(f"  EMB section length: {len(emb_section)}")
        print(f"  EMB section: {emb_section}")
        print(f"  English section starts: {english_section[:60]}...")
        
        # Try interpreting EMB as numbers
        # E=18, M=19, B=17 in Gematria
        # Or maybe E=0, M=1, B=2 as base-3?
        base3 = ''
        for c in emb_section:
            if c == 'E':
                base3 += '0'
            elif c == 'M':
                base3 += '1'
            elif c == 'B':
                base3 += '2'
            else:
                base3 += '_'
        
        print(f"  As base-3: {base3[:50]}...")
        
        # Convert base-3 groups to decimal
        clean_base3 = base3.replace('_', '')
        if clean_base3:
            decimals = []
            for i in range(0, len(clean_base3) - 2, 3):
                try:
                    val = int(clean_base3[i:i+3], 3)
                    decimals.append(val)
                except:
                    pass
            print(f"  Base-3 to decimal (3-digit groups): {decimals[:15]}")
            
            # As ASCII?
            ascii_chars = ''.join(chr(d + 65) if 0 <= d <= 25 else '?' for d in decimals)
            print(f"  As letters (A=0): {ascii_chars}")
    
    # Theory 4: Vigenère with known keys on cleaned text
    print("\n" + "=" * 60)
    print("THEORY 4: Vigenère with known keys")
    print("=" * 60)
    
    keys = ['DIVINITY', 'INSTAR', 'EMERGE', 'PARABLE', 'SURFACE', 'SHED']
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        cleaned = remove_the_patterns(text)
        
        print(f"\n{name}:")
        for key in keys:
            result = try_vigenere_on_between_the(cleaned, key)
            print(f"  {key}: {result[:50]}...")
    
    # Theory 5: Check if THE positions encode something
    print("\n" + "=" * 60)
    print("THEORY 5: THE Position Analysis")
    print("=" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        positions = [i for i in range(len(text) - 2) if text[i:i+3] == 'THE']
        gaps = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
        
        print(f"\n{name}:")
        print(f"  THE positions: {positions[:15]}...")
        print(f"  Gaps between THE: {gaps[:15]}...")
        
        # Gaps as letters (mod 26)?
        gap_letters = ''.join(chr(65 + (g % 26)) for g in gaps)
        print(f"  Gaps as letters (mod 26): {gap_letters[:20]}")
        
        # Gaps as Gematria indices?
        from collections import Counter
        gap_counts = Counter(gaps)
        print(f"  Most common gaps: {gap_counts.most_common(5)}")

if __name__ == "__main__":
    main()

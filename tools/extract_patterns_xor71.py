"""
Extract structured patterns from the XOR-71 output.

The output has strong English bigrams but isn't readable prose.
Test if there's a positional encoding:
- Every Nth character
- Word-initial letters
- Acrostic patterns
"""

# XOR-71 output (best result)
XOR71_OUTPUT = "THEOTHATHEATHIATHEDTHMTHWTHATHEOOTHNLRIAXUMEANYNGEATHETHEATHEATHATHWITHERTHTHETHEATHTHTHATHTTHNGTHETHEATHNGATHANGEOFWTHEOTHETHEATHATHEOFTHNYSTHANGNTHEANGTHASTHEATHYITHENGGTREATHEOEOTHHEATHRTHEATHEANGTHEOTHEATHEATHUMAEOEONTHEORTHEANGTHPOBWTTEOCRTHELMTHWITHBNGTHTHECUYTHENGUTTHEORINGTHEAFTHENTHTHANGATUEONGDTHDLYOERTHEATOEITHEOOEOGBAEYFGNTHTHERTHETNODTHTHEANGUTHEOINGEATHEONGIALTHEFPDEOFBO"

def every_nth_character(text, n, offset=0):
    """Extract every Nth character starting at offset."""
    return text[offset::n]

def word_initials(text):
    """Extract first letter of each 'word' (assuming spaces would be between rune-token words)."""
    # In our case, we need to split on transitions - but the text is continuous
    # Try splitting on common word boundaries
    
    # Method 1: Look for capital letters after lowercase (but all caps here)
    # Method 2: Look for pattern breaks
    
    # For now, just split on every occurrence of THE and take next letter
    words = text.split("THE")
    initials = "".join(w[0] if w else "" for w in words if w)
    return initials

def find_patterns(text):
    """Look for repeating patterns."""
    print("="*80)
    print("Pattern Analysis")
    print("="*80)
    
    # Most common trigrams
    trigrams = {}
    for i in range(len(text) - 2):
        tri = text[i:i+3]
        trigrams[tri] = trigrams.get(tri, 0) + 1
    
    print("\nMost common trigrams:")
    sorted_tri = sorted(trigrams.items(), key=lambda x: x[1], reverse=True)
    for tri, count in sorted_tri[:20]:
        print(f"  {tri}: {count}")
    
    # Look for "THE" positions
    print("\n'THE' appears at positions:")
    the_positions = []
    pos = 0
    while True:
        pos = text.find("THE", pos)
        if pos == -1:
            break
        the_positions.append(pos)
        pos += 1
    
    print(f"  Total occurrences: {len(the_positions)}")
    if len(the_positions) > 1:
        gaps = [the_positions[i+1] - the_positions[i] for i in range(len(the_positions)-1)]
        print(f"  Gaps between occurrences: {gaps[:20]}")
        
        # Check if gaps have a pattern
        from collections import Counter
        gap_freq = Counter(gaps)
        print(f"  Most common gaps: {gap_freq.most_common(10)}")

def test_every_nth(text):
    """Test various N values for every-Nth-character extraction."""
    print("\n" + "="*80)
    print("Every-Nth-Character Extraction")
    print("="*80)
    
    for n in [2, 3, 4, 5, 7, 11, 13, 71]:
        for offset in range(min(n, 3)):  # Try first few offsets
            extracted = every_nth_character(text, n, offset)
            if len(extracted) < 10:
                continue
            
            # Quick readability check
            readable_words = ["THE", "OF", "AND", "TO", "IN", "IS", "THAT", "WITH"]
            score = sum(extracted.count(word) for word in readable_words)
            
            if score > 2 or n <= 5:  # Show if high score or small N
                print(f"\nn={n}, offset={offset}: {extracted[:80]}")
                if score > 0:
                    print(f"  (score: {score})")

def main():
    print("="*80)
    print("Structured Pattern Extraction - Page 1 XOR-71 Output")
    print("="*80)
    
    print(f"\nFull text length: {len(XOR71_OUTPUT)} characters")
    print(f"\nFirst 200 chars:")
    print(XOR71_OUTPUT[:200])
    
    # Pattern analysis
    find_patterns(XOR71_OUTPUT)
    
    # Every-Nth test
    test_every_nth(XOR71_OUTPUT)
    
    # Word initials
    print("\n" + "="*80)
    print("Word Initials (splitting on 'THE')")
    print("="*80)
    initials = word_initials(XOR71_OUTPUT)
    print(f"\nExtracted initials: {initials[:100]}")
    
    # Check if removing "TH" pattern helps
    print("\n" + "="*80)
    print("Removing repetitive patterns")
    print("="*80)
    
    # Try removing all "TH" to see underlying structure
    no_th = XOR71_OUTPUT.replace("TH", "")
    print(f"\nWithout 'TH': {no_th[:200]}")
    
    # Try keeping only consonants or only vowels
    vowels = "AEIOU"
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    
    only_vowels = "".join(c for c in XOR71_OUTPUT if c in vowels)
    only_consonants = "".join(c for c in XOR71_OUTPUT if c in consonants)
    
    print(f"\nOnly vowels: {only_vowels[:100]}")
    print(f"\nOnly consonants: {only_consonants[:100]}")

if __name__ == "__main__":
    main()

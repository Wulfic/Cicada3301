#!/usr/bin/env python3
"""
Gematria-Aware Parsing of Page 0.

Key insight: In Gematria Primus, TH, NG, EA, AE, IA, EO, OE are SINGLE RUNES
representing digraphs. So "THE" in our output is actually just TWO runes:
  - TH (ᚦ, index 2)
  - E (ᛖ, index 18)

This changes how we should parse the text!

The original runes translate to these letters:
TH = ᚦ (a single rune meaning TH)
NG = ᛝ (a single rune meaning NG or ING)
EA = ᛠ (a single rune)
etc.

So when we see "THE" in our output, it's really:
  - TH (one rune) + E (another rune)

This means "AETHATAEYETHEST" might be:
  - AE + TH + A + T + A + E + Y + E + TH + E + S + T (12 runes)
"""

# The first layer output
TEXT = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKKHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

# Gematria letters (single characters in the runic alphabet)
GEMATRIA_LETTERS = [
    'F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
    'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
    'A', 'AE', 'Y', 'IA', 'EA'
]

# Sort by length descending to match digraphs first
GEMATRIA_SORTED = sorted(GEMATRIA_LETTERS, key=lambda x: -len(x))

def text_to_rune_letters(text):
    """Convert text to list of Gematria letters (each representing one rune)."""
    result = []
    i = 0
    while i < len(text):
        matched = False
        for letter in GEMATRIA_SORTED:
            if text[i:i+len(letter)] == letter:
                result.append(letter)
                i += len(letter)
                matched = True
                break
        if not matched:
            # Unknown character, keep it
            result.append(text[i])
            i += 1
    return result

def analyze_as_runes():
    """Analyze the text as a sequence of runes."""
    rune_letters = text_to_rune_letters(TEXT)
    
    print(f"Original text length: {len(TEXT)} characters")
    print(f"As rune sequence: {len(rune_letters)} runes")
    print(f"\nRune sequence (first 50):")
    print(' '.join(rune_letters[:50]))
    
    # Count rune frequencies
    from collections import Counter
    freq = Counter(rune_letters)
    
    print(f"\nRune frequencies:")
    for rune, count in freq.most_common(15):
        pct = 100 * count / len(rune_letters)
        print(f"  {rune}: {count}x ({pct:.1f}%)")
    
    # Check if TH-E is still common
    the_count = 0
    for i in range(len(rune_letters) - 1):
        if rune_letters[i] == 'TH' and rune_letters[i+1] == 'E':
            the_count += 1
    
    print(f"\nTH+E pairs (as two-rune sequence): {the_count}")
    
    return rune_letters

def find_english_words_from_runes(rune_letters):
    """Try to find English words from the rune sequence."""
    
    # Common Old English words in Gematria spelling
    WORD_PATTERNS = {
        # Article/Pronouns
        ('TH', 'E'): 'THE',
        ('A',): 'A',
        ('I',): 'I',
        ('TH', 'Y'): 'THY',
        ('TH', 'E', 'E'): 'THEE',
        ('TH', 'O', 'V'): 'THOU',
        ('TH', 'E', 'I', 'R'): 'THEIR',
        
        # Verbs
        ('D', 'O', 'E', 'TH'): 'DOETH',
        ('G', 'O', 'E', 'TH'): 'GOETH',
        ('H', 'A', 'TH'): 'HATH',
        ('I', 'S'): 'IS',
        ('A', 'R', 'E'): 'ARE',
        ('W', 'A', 'S'): 'WAS',
        
        # Prepositions
        ('O', 'F'): 'OF',
        ('I', 'N'): 'IN',
        ('O', 'N'): 'ON',
        ('T', 'O'): 'TO',
        ('F', 'O', 'R'): 'FOR',
        ('A', 'T'): 'AT',
        ('B', 'Y'): 'BY',
        
        # Conjunctions
        ('A', 'N', 'D'): 'AND',
        ('O', 'R'): 'OR',
        ('B', 'V', 'T'): 'BUT',
        
        # Nouns
        ('TH', 'NG'): 'THING',  # In runic, TH+ING might be TH+NG
        ('TH', 'I', 'NG'): 'THING',
        ('M', 'A', 'N'): 'MAN',
        ('G', 'O', 'D'): 'GOD',
        
        # Others
        ('TH', 'E', 'R', 'E'): 'THERE',
        ('TH', 'E', 'N'): 'THEN',
        ('TH', 'A', 'T'): 'THAT',
        ('W', 'H', 'E', 'N'): 'WHEN',
        ('A', 'N'): 'AN',
        ('V', 'P'): 'UP',  # U becomes V in Gematria
    }
    
    print("\n" + "=" * 70)
    print("WORD PATTERN SEARCH")
    print("=" * 70)
    
    # Search for patterns
    for pattern, word in sorted(WORD_PATTERNS.items(), key=lambda x: -len(x[0])):
        count = 0
        positions = []
        for i in range(len(rune_letters) - len(pattern) + 1):
            if tuple(rune_letters[i:i+len(pattern)]) == pattern:
                count += 1
                positions.append(i)
        
        if count > 0:
            print(f"  {word} ({'-'.join(pattern)}): {count}x at positions {positions[:5]}{'...' if len(positions) > 5 else ''}")
    
    return

def try_word_boundaries():
    """Try to insert word boundaries manually."""
    
    rune_letters = text_to_rune_letters(TEXT)
    
    print("\n" + "=" * 70)
    print("MANUAL WORD BOUNDARY ATTEMPT")
    print("=" * 70)
    
    # Looking at the start: AE TH A T A E Y E TH E S T H E S TH E AE A TH E O R NG
    #                       AE TH-AT-A-EYE-TH-E-ST-HE-S-THE-AE-A-THE-OR-NG
    #                       AE THAT A EYE THEST HES THE AE A THE OR NG ?
    
    # Let's try: AE THAT AE YETHEST HES THE AE EAT HE OR NG ...
    
    print("\nFirst 30 runes:")
    print(' '.join(rune_letters[:30]))
    
    # Try manual parsing
    print("\nManual parse attempt 1:")
    attempt1 = "AE THAT A EYE TH-EST HE S TH-E AE A TH-E OR-NG TH-RO-TH-I-A-S-TH-D-IA TH-E TH-E AN-G-E-N-EA TH-E-S TH-E A-A-E-TH-A-TH TH-E OF LE TH-E A-TH THY"
    print(attempt1)
    
    print("\nManual parse attempt 2 (treating as Old English):")
    # In Old English, common patterns:
    # -ETH endings for verbs (doeth, goeth)
    # THAT as conjunction
    # THE as article
    
    # AE could be the Old English ǣ (ash) meaning "law" or "ever"
    # Perhaps: "AE (ever/law) THAT A EYE THEST (thou test?) ..."
    
    print("Possible meaning:")
    print("  AE = Old English 'ever' or 'law'")
    print("  THAT = 'that' (conjunction)")
    print("  A = 'a' (article)")
    print("  EYE = 'eye'")
    print("  TH + EST = 'thou art' (archaic 'you are')?")
    print("  Or: THE + ST = 'the' + 'st' (saint?)?")

def main():
    print("Gematria-Aware Parsing of Page 0")
    print("=" * 70)
    
    rune_letters = analyze_as_runes()
    find_english_words_from_runes(rune_letters)
    try_word_boundaries()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT")
    print("=" * 70)
    print("""
In Gematria Primus:
- THE is just 2 runes: TH (ᚦ) + E (ᛖ)
- THING could be: TH + I + NG (3 runes) or TH + NG (2 runes)
- NG is a single rune (ᛝ) that can mean 'NG' or 'ING'

So when we count "THE" as 47 occurrences, we're counting 47 TH+E pairs.
This is actually 94 rune positions out of ~262 total = 36% of the text!

This is still very high. Either:
1. THE is genuinely common in the plaintext (Old English article)
2. Our decryption is biased toward producing TH and E together
3. There's still another layer we haven't decoded
    """)

if __name__ == "__main__":
    main()

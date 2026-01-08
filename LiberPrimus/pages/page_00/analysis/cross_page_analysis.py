#!/usr/bin/env python3
"""
Cross-Page Pattern Analysis
============================
Analyze the patterns in first-layer decrypted output across Pages 0-4.
Looking for:
1. Common word patterns
2. The "EEMMBBB" pattern in Pages 2-4
3. Potential second cipher layer clues
"""

# First layer decrypted plaintext for each page
PAGE0 = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

PAGE1 = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTOOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

PAGE2 = "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE"

PAGE3 = "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE"

PAGE4 = "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"

# The Parable (plaintext reference)
PARABLE = "PARABLE.LIKE THE INSTAR TUNNELING TO THE SURFACE.WE MUST SHED OUR OWN CIRCUMFERENCES.FIND THE DIVINITY WITHIN AND EMERGE."

def analyze_letter_frequency(text, label):
    """Analyze letter frequency in text."""
    from collections import Counter
    
    # Remove non-letters
    text = text.replace('/', '').replace('.', '').replace(' ', '')
    
    counts = Counter(text)
    total = len(text)
    
    print(f"\n{label} (length {total}):")
    print("-" * 40)
    
    # Top 10 letters
    for letter, count in counts.most_common(10):
        pct = count / total * 100
        bar = '█' * int(pct)
        print(f"  {letter:3}: {count:4} ({pct:5.1f}%) {bar}")
    
    return counts

def find_word_patterns(text):
    """Find potential word patterns."""
    # Split on THE
    parts = text.split('THE')
    
    words = []
    for part in parts:
        if 2 <= len(part) <= 10:
            words.append(part)
    
    return words

def analyze_emb_pattern(text):
    """Analyze the EEMMBBB pattern at start of pages 2-4."""
    # Count consecutive runs
    runs = []
    current_char = None
    current_count = 0
    
    for char in text:
        if char == current_char:
            current_count += 1
        else:
            if current_char and current_count > 0:
                runs.append((current_char, current_count))
            current_char = char
            current_count = 1
    
    if current_char:
        runs.append((current_char, current_count))
    
    return runs[:20]  # First 20 runs

def check_numerical_encoding():
    """Check if E/M/B might encode binary or other numerical values."""
    print("\n" + "=" * 60)
    print("CHECKING NUMERICAL ENCODING HYPOTHESIS")
    print("=" * 60)
    
    # E=18 (index in Gematria), M=19, B=17
    # Or by position: E=5, M=13, B=2 in Latin
    
    # Extract EMB-heavy prefixes
    page2_prefix = PAGE2[:70]
    page3_prefix = PAGE3[:80]
    page4_prefix = PAGE4[:85]
    
    print(f"\nPage 2 prefix: {page2_prefix}")
    print(f"Page 3 prefix: {page3_prefix}")
    print(f"Page 4 prefix: {page4_prefix}")
    
    # Try interpreting as binary (E=1, other=0)
    for name, prefix in [("Page2", page2_prefix), ("Page3", page3_prefix), ("Page4", page4_prefix)]:
        binary = ''.join('1' if c == 'E' else '0' for c in prefix)
        print(f"\n{name} binary (E=1): {binary[:40]}...")
        
        # Try 5-bit groupings
        fivebit = []
        for i in range(0, len(binary) - 4, 5):
            val = int(binary[i:i+5], 2)
            fivebit.append(val)
        print(f"  5-bit values: {fivebit[:10]}")
        
        # Try as letters (A=0, B=1, etc)
        letters = ''.join(chr(65 + v) if v < 26 else '?' for v in fivebit[:10])
        print(f"  As letters: {letters}")

def main():
    print("=" * 60)
    print("CROSS-PAGE PATTERN ANALYSIS")
    print("=" * 60)
    
    # Letter frequency analysis
    print("\n" + "=" * 60)
    print("LETTER FREQUENCY ANALYSIS")
    print("=" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1), 
                       ("Page 2", PAGE2), ("Page 3", PAGE3), ("Page 4", PAGE4)]:
        analyze_letter_frequency(text, name)
    
    # Analyze EMB pattern
    print("\n" + "=" * 60)
    print("EMB RUN PATTERNS (Pages 2-4)")
    print("=" * 60)
    
    for name, text in [("Page 2", PAGE2), ("Page 3", PAGE3), ("Page 4", PAGE4)]:
        runs = analyze_emb_pattern(text)
        print(f"\n{name} runs: {runs}")
    
    # Check numerical encoding
    check_numerical_encoding()
    
    # Word pattern analysis
    print("\n" + "=" * 60)
    print("WORD PATTERNS (split on THE)")
    print("=" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        words = find_word_patterns(text)
        print(f"\n{name} fragments between THE:")
        print(f"  {words[:20]}")
    
    # Common patterns across pages
    print("\n" + "=" * 60)
    print("CROSS-PAGE OBSERVATIONS")
    print("=" * 60)
    
    # Check if pages share common sequences
    all_texts = [PAGE0, PAGE1, PAGE2, PAGE3, PAGE4]
    
    # Find common 4-letter sequences
    from collections import Counter
    
    all_4grams = Counter()
    for text in all_texts:
        for i in range(len(text) - 3):
            gram = text[i:i+4]
            all_4grams[gram] += 1
    
    print("\nMost common 4-grams across all pages:")
    for gram, count in all_4grams.most_common(15):
        print(f"  {gram}: {count}")
    
    # Check THE positions
    print("\n\nTHE Pattern Analysis:")
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        the_positions = [i for i in range(len(text)-2) if text[i:i+3] == 'THE']
        gaps = [the_positions[i+1] - the_positions[i] for i in range(len(the_positions)-1)]
        print(f"\n{name}:")
        print(f"  THE count: {len(the_positions)}")
        print(f"  Average gap: {sum(gaps)/len(gaps):.1f}" if gaps else "  No gaps")
        print(f"  Gap distribution: {sorted(set(gaps))[:10]}")

if __name__ == "__main__":
    main()

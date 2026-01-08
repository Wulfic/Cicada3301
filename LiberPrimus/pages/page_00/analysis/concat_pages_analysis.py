#!/usr/bin/env python3
"""
Concatenated Pages Analysis
===========================
Try analyzing all Pages 0-4 as a single stream.
Also extract only the English-like portions (after EMB prefix in pages 2-4).
"""

# First layer outputs
PAGE0 = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

PAGE1 = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTOOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

PAGE2 = "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE"

PAGE3 = "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE"

PAGE4 = "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"

def extract_english_section(text):
    """Extract the English-like section (after first 'TH' pattern)."""
    for i in range(len(text) - 1):
        if text[i:i+2] == 'TH':
            return text[i:]
    return text

def find_common_ngrams(texts, n=4):
    """Find n-grams common across all texts."""
    from collections import Counter
    
    ngram_sets = []
    for text in texts:
        ngrams = Counter()
        for i in range(len(text) - n + 1):
            ngrams[text[i:i+n]] += 1
        ngram_sets.append(set(ngrams.keys()))
    
    # Find intersection
    common = ngram_sets[0]
    for s in ngram_sets[1:]:
        common &= s
    
    return common

def score_english_words(text):
    """Score text based on common English words found."""
    words = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'YOU', 
             'THIS', 'BUT', 'FROM', 'THEY', 'ARE', 'ONE', 'ALL', 'THEIR',
             'WHAT', 'THERE', 'OUT', 'INTO', 'WHEN', 'SOME', 'WOULD', 'THEM',
             'THING', 'THINGS', 'FIND', 'EMERGE', 'WITHIN', 'SHED', 'MUST']
    
    score = 0
    found = []
    for word in words:
        count = text.count(word)
        if count > 0:
            score += count * len(word)
            found.append((word, count))
    
    return score, found

def try_interleave(texts, pattern):
    """Try interleaving multiple texts according to pattern."""
    result = []
    indices = [0] * len(texts)
    
    for p in pattern * 1000:  # Repeat pattern many times
        text_idx = p % len(texts)
        if indices[text_idx] < len(texts[text_idx]):
            result.append(texts[text_idx][indices[text_idx]])
            indices[text_idx] += 1
        if all(indices[i] >= len(texts[i]) for i in range(len(texts))):
            break
    
    return ''.join(result)

def try_read_every_nth(text, n, offset=0):
    """Read every Nth character starting at offset."""
    return text[offset::n]

def main():
    print("=" * 60)
    print("CONCATENATED PAGES ANALYSIS")
    print("=" * 60)
    
    pages = [PAGE0, PAGE1, PAGE2, PAGE3, PAGE4]
    
    # Full concatenation
    print("\n" + "-" * 60)
    print("FULL CONCATENATION (Pages 0-4)")
    print("-" * 60)
    
    concat_full = ''.join(pages)
    print(f"Total length: {len(concat_full)}")
    
    score, found = score_english_words(concat_full)
    print(f"English word score: {score}")
    print(f"Found words: {found}")
    
    # Extract English sections from Pages 2-4
    print("\n" + "-" * 60)
    print("ENGLISH SECTIONS ONLY (removing EMB prefix)")
    print("-" * 60)
    
    page2_english = extract_english_section(PAGE2)
    page3_english = extract_english_section(PAGE3)
    page4_english = extract_english_section(PAGE4)
    
    print(f"Page 2 English section ({len(page2_english)} chars): {page2_english[:80]}...")
    print(f"Page 3 English section ({len(page3_english)} chars): {page3_english[:80]}...")
    print(f"Page 4 English section ({len(page4_english)} chars): {page4_english[:80]}...")
    
    # Concatenate English sections
    concat_english = PAGE0 + PAGE1 + page2_english + page3_english + page4_english
    print(f"\nEnglish concat length: {len(concat_english)}")
    
    score, found = score_english_words(concat_english)
    print(f"English word score: {score}")
    print(f"Found words: {found}")
    
    # Try reading every Nth character
    print("\n" + "-" * 60)
    print("SKIP CIPHER TESTS (every Nth character)")
    print("-" * 60)
    
    for n in [2, 3, 4, 5, 6, 7, 8]:
        for offset in range(n):
            result = try_read_every_nth(concat_english, n, offset)
            score, _ = score_english_words(result)
            if score > 20:
                print(f"N={n}, offset={offset}: Score {score}")
                print(f"  Result: {result[:60]}...")
    
    # Find common n-grams across all pages
    print("\n" + "-" * 60)
    print("COMMON 4-GRAMS ACROSS ALL PAGES")
    print("-" * 60)
    
    common = find_common_ngrams([PAGE0, PAGE1, page2_english, page3_english, page4_english])
    print(f"Common 4-grams: {sorted(common)[:20]}")
    
    # Try interleaving Pages 0 and 1 (the THE-heavy pages)
    print("\n" + "-" * 60)
    print("INTERLEAVING TESTS (Pages 0 and 1)")
    print("-" * 60)
    
    # Simple alternation
    for pattern in [[0,1], [1,0], [0,0,1], [0,1,1], [0,1,0,1,1]]:
        result = try_interleave([PAGE0, PAGE1], pattern)
        score, found = score_english_words(result)
        if score > 50:
            print(f"Pattern {pattern}: Score {score}")
            print(f"  Result: {result[:80]}...")
    
    # Remove THE and see what's left
    print("\n" + "-" * 60)
    print("TEXT WITH 'THE' REMOVED")
    print("-" * 60)
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        no_the = text.replace('THE', '')
        print(f"\n{name} without THE ({len(no_the)} chars):")
        print(f"  {no_the[:100]}...")
        
        score, found = score_english_words(no_the)
        print(f"  Word score: {score}, Found: {found}")
    
    # Look for repeated patterns
    print("\n" + "-" * 60)
    print("REPEATED SEQUENCE ANALYSIS")
    print("-" * 60)
    
    def find_repeated_sequences(text, min_len=5, min_count=2):
        from collections import Counter
        seqs = Counter()
        for length in range(min_len, min(20, len(text) // 2)):
            for i in range(len(text) - length):
                seq = text[i:i+length]
                if seq.count('THE') <= 1:  # Avoid THE-dominated sequences
                    seqs[seq] += 1
        return [(s, c) for s, c in seqs.most_common(20) if c >= min_count]
    
    for name, text in [("Page 0", PAGE0), ("Page 1", PAGE1)]:
        repeated = find_repeated_sequences(text, min_len=5, min_count=2)
        print(f"\n{name} repeated sequences:")
        for seq, count in repeated[:10]:
            print(f"  '{seq}': {count}x")

if __name__ == "__main__":
    main()

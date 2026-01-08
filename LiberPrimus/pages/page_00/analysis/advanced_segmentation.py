#!/usr/bin/env python3
"""
Advanced Word Segmentation for Liber Primus First-Layer Output.

This script implements a sophisticated word segmentation algorithm that:
1. Uses a comprehensive Old English + Modern English dictionary
2. Prioritizes longer words over shorter ones
3. Recognizes common suffixes (-ETH, -LY, -ING, etc.)
4. Uses dynamic programming for optimal segmentation
5. Outputs readable text with word boundaries

Key insight: The first-layer output appears to be Old English prose with spaces removed.
"""

import re

# First layer outputs from SUB mod 29 decryption
FIRST_LAYER = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKKHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBNTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"
}

# Comprehensive dictionary prioritizing Old English and philosophical terms
DICTIONARY = {
    # Old English verb forms (highest priority - these appear in Cicada texts)
    'DOETH': 100, 'GOETH': 100, 'HATH': 100, 'DOTH': 100, 'LEARETH': 100,
    'LOVETH': 100, 'MOVETH': 100, 'TAKETH': 100, 'MAKETH': 100, 'COMETH': 100,
    'SEEKETH': 100, 'FINDETH': 100, 'KNOWETH': 100, 'THINKETH': 100,
    'SAITH': 100, 'SPEAKETH': 100, 'HEARETH': 100, 'SEETH': 100,
    'BELIEVETH': 100, 'LIVETH': 100, 'DIETH': 100, 'RISETH': 100,
    
    # Old English pronouns and determiners
    'THEE': 100, 'THOU': 100, 'THY': 100, 'THINE': 100, 'YE': 100,
    'THYSELF': 100, 'WHEREFORE': 100, 'WHENCE': 100, 'HITHER': 100,
    'THITHER': 100, 'HENCE': 100, 'THEREOF': 100, 'WHEREIN': 100,
    
    # Common English words (high frequency)
    'THE': 90, 'AND': 90, 'THAT': 90, 'WITH': 90, 'THIS': 90,
    'THERE': 90, 'THEIR': 90, 'THEY': 90, 'THEM': 90, 'THEN': 90,
    'THAN': 90, 'THESE': 90, 'THOSE': 90, 'WHERE': 90, 'WHEN': 90,
    'WHAT': 90, 'WHICH': 90, 'WHO': 90, 'WHOM': 90, 'WHOSE': 90,
    
    # Philosophical/Cicada vocabulary
    'DIVINITY': 95, 'DIVINE': 95, 'WISDOM': 95, 'TRUTH': 95,
    'CIRCUMFERENCE': 95, 'INSTAR': 95, 'EMERGE': 95, 'SACRED': 95,
    'PILGRIM': 95, 'JOURNEY': 95, 'KNOWLEDGE': 95, 'PRIMES': 95,
    'TOTIENT': 95, 'ENCRYPTED': 95, 'DECEPTION': 95,
    'CONSCIOUSNESS': 95, 'REALITY': 95, 'ILLUSION': 95,
    'ADHERENCE': 95, 'CONSUMPTION': 95, 'PRESERVATION': 95,
    'PRIMALITY': 95, 'FIBONACCI': 95, 'INSTRUCTION': 95,
    'WARNING': 95, 'WELCOME': 95, 'PARABLE': 95, 'KOAN': 95,
    
    # Common verbs
    'HAVE': 85, 'BEEN': 85, 'WERE': 85, 'BEING': 85, 'HAVING': 85,
    'DOES': 85, 'DOING': 85, 'DONE': 85, 'MAKE': 85, 'MADE': 85,
    'TAKE': 85, 'TOOK': 85, 'TAKEN': 85, 'COME': 85, 'CAME': 85,
    'FIND': 85, 'FOUND': 85, 'THINK': 85, 'THOUGHT': 85,
    'KNOW': 85, 'KNEW': 85, 'KNOWN': 85, 'SEE': 85, 'SAW': 85,
    'SEEN': 85, 'HEAR': 85, 'HEARD': 85, 'SPEAK': 85, 'SPOKE': 85,
    'GIVE': 85, 'GAVE': 85, 'GIVEN': 85, 'SEEK': 85, 'SOUGHT': 85,
    'LEARN': 85, 'TEACH': 85, 'TAUGHT': 85, 'TELL': 85, 'TOLD': 85,
    
    # Common nouns
    'THING': 85, 'THINGS': 85, 'PLACE': 85, 'PLACES': 85,
    'TIME': 85, 'TIMES': 85, 'WORD': 85, 'WORDS': 85,
    'LIFE': 85, 'DEATH': 85, 'WORLD': 85, 'EARTH': 85,
    'MIND': 85, 'SOUL': 85, 'BODY': 85, 'SPIRIT': 85,
    'HEART': 85, 'HEAD': 85, 'HAND': 85, 'HANDS': 85,
    'EYE': 85, 'EYES': 85, 'EAR': 85, 'EARS': 85,
    'SELF': 85, 'OTHER': 85, 'OTHERS': 85, 'NOTHING': 85,
    'SOMETHING': 85, 'EVERYTHING': 85, 'ANYTHING': 85,
    
    # Prepositions and conjunctions
    'FROM': 80, 'INTO': 80, 'UNTO': 80, 'UPON': 80, 'WITHIN': 80,
    'WITHOUT': 80, 'BEFORE': 80, 'AFTER': 80, 'UNDER': 80, 'OVER': 80,
    'THROUGH': 80, 'BETWEEN': 80, 'AMONG': 80, 'AGAINST': 80,
    'ABOUT': 80, 'ABOVE': 80, 'BELOW': 80, 'BEYOND': 80,
    'BECAUSE': 80, 'THEREFORE': 80, 'HOWEVER': 80, 'ALTHOUGH': 80,
    
    # Adjectives and adverbs
    'GREAT': 80, 'GOOD': 80, 'TRUE': 80, 'REAL': 80,
    'HOLY': 80, 'SACRED': 80, 'DIVINE': 80, 'ETERNAL': 80,
    'FIRST': 80, 'LAST': 80, 'ONLY': 80, 'ALSO': 80,
    'MANY': 80, 'SOME': 80, 'MORE': 80, 'MOST': 80, 'LESS': 80,
    'ALL': 80, 'EACH': 80, 'EVERY': 80, 'ANY': 80, 'NONE': 80,
    'HERE': 80, 'NOW': 80, 'EVER': 80, 'NEVER': 80, 'ALWAYS': 80,
    
    # Short common words
    'IS': 75, 'IT': 75, 'AS': 75, 'AT': 75, 'BE': 75, 'BY': 75,
    'DO': 75, 'GO': 75, 'IF': 75, 'IN': 75, 'NO': 75, 'OF': 75,
    'ON': 75, 'OR': 75, 'SO': 75, 'TO': 75, 'UP': 75, 'WE': 75,
    'AN': 75, 'HE': 75, 'ME': 75, 'MY': 75, 'US': 75,
    
    # Single letters (lowest priority)
    'A': 50, 'I': 50, 'O': 50,
    
    # Additional Old English / archaic terms
    'ART': 80, 'DOST': 80, 'WILT': 80, 'SHALT': 80, 'CANST': 80,
    'WHILST': 80, 'AMONGST': 80, 'BETWIXT': 80, 'VERILY': 80,
    'NIGH': 80, 'FORSOOTH': 80, 'PERCHANCE': 80, 'MAYHAP': 80,
    
    # More vocabulary
    'FOR': 85, 'NOT': 85, 'BUT': 85, 'ARE': 85, 'WAS': 85,
    'HAS': 85, 'HAD': 85, 'CAN': 85, 'MAY': 85, 'WILL': 85,
    'WOULD': 85, 'COULD': 85, 'SHOULD': 85, 'MUST': 85,
    'LET': 85, 'SAY': 85, 'GET': 85, 'PUT': 85, 'SET': 85,
    
    # Gematria-specific digraphs that may appear
    'TH': 60, 'NG': 60, 'EA': 60, 'AE': 60, 'IA': 60, 'EO': 60, 'OE': 60,
    
    # Additional words found in previous analysis
    'EST': 70, 'ETH': 70, 'YET': 80, 'HIS': 80, 'HER': 80,
    'OUR': 80, 'YOUR': 80, 'YOURSELVES': 80, 'OURSELVES': 80,
}

def segment_text(text, dictionary):
    """
    Dynamic programming approach to find optimal word segmentation.
    Prioritizes longer words and higher-value dictionary entries.
    """
    text = text.upper()
    n = len(text)
    
    # dp[i] = (best_score, best_segmentation) for text[0:i]
    dp = [None] * (n + 1)
    dp[0] = (0, [])
    
    for i in range(1, n + 1):
        best = None
        
        # Try all possible last words ending at position i
        for j in range(max(0, i - 20), i):  # Max word length 20
            word = text[j:i]
            
            if dp[j] is None:
                continue
            
            prev_score, prev_words = dp[j]
            
            if word in dictionary:
                # Dictionary word - add its value
                word_score = dictionary[word]
                # Bonus for longer words
                length_bonus = len(word) * 5
                new_score = prev_score + word_score + length_bonus
                
                if best is None or new_score > best[0]:
                    best = (new_score, prev_words + [word])
            
            elif len(word) <= 2:
                # Allow very short unknown fragments with penalty
                new_score = prev_score - 10
                if best is None or new_score > best[0]:
                    best = (new_score, prev_words + [f'[{word}]'])
        
        if best is not None:
            dp[i] = best
    
    return dp[n]

def segment_greedy(text, dictionary):
    """
    Greedy approach: always take the longest matching word.
    """
    text = text.upper()
    words = []
    i = 0
    
    while i < len(text):
        # Try longest matches first
        best_word = None
        best_len = 0
        
        for length in range(min(20, len(text) - i), 0, -1):
            word = text[i:i+length]
            if word in dictionary:
                if length > best_len:
                    best_word = word
                    best_len = length
        
        if best_word:
            words.append(best_word)
            i += best_len
        else:
            # No match - take single character
            words.append(f'[{text[i]}]')
            i += 1
    
    return words

def analyze_page(page_num, text):
    """Analyze and segment a page's first-layer output."""
    print(f"\n{'='*70}")
    print(f"PAGE {page_num}")
    print(f"{'='*70}")
    
    # Remove EMB prefix if present
    clean_text = text
    if text.startswith('EMBEMB'):
        # Find where EMB pattern ends
        i = 0
        while i < len(text) - 2 and text[i:i+3] == 'EMB':
            i += 3
        clean_text = text[i:]
        print(f"Removed EMB prefix ({i} chars)")
        print(f"Remaining text: {len(clean_text)} chars")
    
    print(f"\nOriginal length: {len(text)} chars")
    print(f"First 80 chars: {text[:80]}...")
    
    # Greedy segmentation
    print("\n--- GREEDY SEGMENTATION ---")
    greedy_words = segment_greedy(clean_text, DICTIONARY)
    
    # Count dictionary vs unknown
    dict_words = [w for w in greedy_words if not w.startswith('[')]
    unknown = [w for w in greedy_words if w.startswith('[')]
    
    print(f"Words found: {len(dict_words)} dictionary, {len(unknown)} unknown")
    print(f"Coverage: {100 * sum(len(w) for w in dict_words) / len(clean_text):.1f}%")
    
    # Show segmentation
    result = ' '.join(greedy_words)
    print(f"\nSegmented text:")
    print(result[:500])
    if len(result) > 500:
        print("...")
    
    # Word frequency
    word_counts = {}
    for w in dict_words:
        word_counts[w] = word_counts.get(w, 0) + 1
    
    print(f"\nMost common words:")
    for word, count in sorted(word_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {word}: {count}x")
    
    # Dynamic programming segmentation
    print("\n--- OPTIMAL (DP) SEGMENTATION ---")
    dp_result = segment_text(clean_text, DICTIONARY)
    
    if dp_result:
        score, dp_words = dp_result
        dict_words_dp = [w for w in dp_words if not w.startswith('[')]
        unknown_dp = [w for w in dp_words if w.startswith('[')]
        
        print(f"Score: {score}")
        print(f"Words found: {len(dict_words_dp)} dictionary, {len(unknown_dp)} unknown")
        print(f"Coverage: {100 * sum(len(w.strip('[]')) for w in dict_words_dp) / len(clean_text):.1f}%")
        
        result_dp = ' '.join(dp_words)
        print(f"\nSegmented text:")
        print(result_dp[:500])
        if len(result_dp) > 500:
            print("...")
    else:
        print("No valid segmentation found")
    
    return greedy_words, dp_result

def main():
    print("Advanced Word Segmentation for Liber Primus")
    print("=" * 70)
    print("\nHypothesis: First-layer output is Old English with spaces removed.")
    print("Goal: Recover word boundaries to produce readable text.")
    
    for page_num in sorted(FIRST_LAYER.keys()):
        analyze_page(page_num, FIRST_LAYER[page_num])
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nIf coverage is high (>80%), text is likely correctly decrypted.")
    print("Remaining '[X]' fragments may be:")
    print("  - Proper nouns or names")
    print("  - Archaic words not in dictionary")
    print("  - Errors in transcription or decryption")

if __name__ == "__main__":
    main()

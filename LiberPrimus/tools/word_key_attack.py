#!/usr/bin/env python3
"""
WORD-BASED KEY ATTACK
=====================

Tests single words from Liber Primus / Cicada 3301 vocabulary as Vigenère keys
on the first-layer decrypted output to see if they produce more readable text.

Hypothesis: The second layer cipher uses a keyword related to the work.

Key insight: The TH anomaly (28.2% vs expected 5.3%) may be caused by the 
transforms - trying different word keys may resolve this.
"""

import os
import sys
from collections import Counter
from pathlib import Path

# ============================================================================
# CONSTANTS
# ============================================================================

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}

# ============================================================================
# CICADA VOCABULARY - Words from Liber Primus, Parable, and Related Works
# ============================================================================

CICADA_VOCABULARY = [
    # From The Parable (Page 57)
    "INSTAR", "CIRCUMFERENCE", "DIVINITY", "EMERGE", "SHED", "SURFACE",
    "TUNNELING", "WITHIN", "FIND", "MUST", "LIKE", "OUR", "OWN",
    
    # Common Cicada themes
    "WISDOM", "TRUTH", "KNOWLEDGE", "ENLIGHTEN", "ENLIGHTENMENT",
    "SEEK", "SEEKER", "SEEKERS", "PATH", "JOURNEY", "QUEST",
    "PRIMUS", "LIBER", "LIBERPRIMUS", "CICADA", "PRIME", "PRIMES",
    
    # Old English / Religious (found in outputs)
    "DOETH", "GOETH", "HATH", "THOU", "THEE", "THY", "THINE",
    "DOTH", "HAVETH", "SPEAKETH", "SAYETH", "FINDETH", "SEEKETH",
    "DIVINE", "SACRED", "HOLY", "GOD", "GODS", "LORD", "SPIRIT",
    
    # Mystical / Occult
    "GEMATRIA", "CIPHER", "SECRET", "HIDDEN", "MYSTERY", "MYSTERIES",
    "RUNE", "RUNES", "RUNIC", "FUTHARK", "ELDER", "ANGLO", "SAXON",
    "ALCHEMY", "HERMETIC", "ESOTERIC", "OCCULT", "ARCANE", "ANCIENT",
    
    # Numbers / Math
    "THREE", "SEVEN", "ELEVEN", "THIRTEEN", "SEVENTEEN", "NINETEEN",
    "TWENTYTHREE", "TWENTYNINE", "THIRTYONE", "THIRTYSEVEN",
    
    # Potential keywords
    "WARNING", "WELCOME", "BEGIN", "BEGINNING", "END", "ENDING",
    "INSTRUCTION", "INSTRUCTIONS", "LESSON", "LESSONS", "LEARN", "TEACH",
    "ANSWER", "QUESTION", "SOLVE", "SOLUTION", "KEY", "KEYS",
    "LIGHT", "DARK", "DARKNESS", "SHADOW", "SHADOWS",
    
    # Latin / Greek influences
    "VERITAS", "LUX", "VIA", "LOGOS", "GNOSIS", "SOPHIA", "NOUS",
    "COGITO", "ERGO", "SUM", "VENI", "VIDI", "VICI",
    
    # More compound words from Parable
    "FINDTHEDIVINITY", "DIVINITYWITHIN", "SHEDOURCIRCUMFERENCE",
    "ANDEMERGE", "LIKETHE", "LIKETHEINSTAR",
    
    # Shorter variations
    "AN", "A", "THE", "TO", "OF", "IN", "IT", "IS", "AS", "AT", "ON",
    "BE", "DO", "GO", "WE", "HE", "ME", "MY", "BY", "UP", "NO", "SO",
    "IF", "OR", "AM", "US", "ALL", "ONE", "TWO", "SIX", "TEN",
    
    # Specific Cicada references
    "THREEOHONE", "THREETHREEOHONE", "LEAKS", "PGP", "ONION", "TOR",
    "PILGRIM", "PILGRIMAGE", "AWAKEN", "AWAKENING", "TRANSFORM",
    
    # Additional Old English / Archaic
    "VERILY", "FORSOOTH", "HEREIN", "THEREIN", "WHEREIN", "BEHOLD",
    "UNTO", "UPON", "THENCE", "HENCE", "WHENCE", "WHILST", "AMONGST",
    
    # Single letter Gematria (for testing)
    "F", "U", "O", "R", "C", "G", "W", "H", "N", "I", "J", "P", "X",
    "S", "T", "B", "E", "M", "L", "D", "A", "Y",
    
    # Digraphs as words
    "TH", "EO", "NG", "OE", "AE", "IA", "EA",
]

# Add all uppercase versions
CICADA_VOCABULARY = list(set([w.upper() for w in CICADA_VOCABULARY]))

# ============================================================================
# FIRST LAYER OUTPUTS (from previous decryption)
# ============================================================================

FIRST_LAYER_OUTPUTS = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL",
}

# ============================================================================
# TEXT CONVERSION
# ============================================================================

def text_to_indices(text):
    """Convert text (like 'THE') to indices using Gematria mapping"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        # Single letter
        if text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
            i += 1
        elif text[i] == 'K':  # K maps to C
            indices.append(LETTER_TO_INDEX['C'])
            i += 1
        else:
            # Skip non-letter characters
            i += 1
    return indices

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices if 0 <= i < 29)

def parse_first_layer_to_indices(text):
    """Parse first layer output (which uses LETTERS) back to indices"""
    text = text.upper().replace("/", "").replace("-", "")
    indices = []
    i = 0
    while i < len(text):
        matched = False
        # Try digraphs first (longest match)
        for length in [2, 1]:
            if i + length <= len(text):
                segment = text[i:i+length]
                if segment in LETTER_TO_INDEX:
                    indices.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1  # Skip unknown
    return indices

# ============================================================================
# VIGENÈRE OPERATIONS
# ============================================================================

def vigenere_decrypt(cipher_indices, key_indices, operation='sub'):
    """
    Apply Vigenère decryption with given key.
    
    operation='sub': plaintext = (cipher - key) mod 29
    operation='add': plaintext = (cipher + key) mod 29
    """
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if operation == 'sub':
            plaintext.append((c - k) % 29)
        else:  # add
            plaintext.append((c + k) % 29)
    return plaintext

def vigenere_decrypt_variant(cipher_indices, key_indices, variant='standard'):
    """
    Try different Vigenère variants to handle the TH anomaly.
    
    Variants:
    - 'standard': (cipher - key) mod 29
    - 'reverse': (key - cipher) mod 29
    - 'add': (cipher + key) mod 29
    - 'negadd': (-cipher - key) mod 29
    """
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if variant == 'standard':
            plaintext.append((c - k) % 29)
        elif variant == 'reverse':
            plaintext.append((k - c) % 29)
        elif variant == 'add':
            plaintext.append((c + k) % 29)
        elif variant == 'negadd':
            plaintext.append((-c - k) % 29)
    return plaintext

# ============================================================================
# SCORING
# ============================================================================

def score_english(text):
    """Score English-likeness"""
    text = text.upper()
    score = 0.0
    
    # Common trigrams
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8,
        'ERS': 7, 'HIS': 7, 'RES': 7, 'ILL': 7, 'ARE': 7,
        'WIT': 6, 'ITH': 6, 'OUT': 6, 'ALL': 6, 'OUR': 6
    }
    
    # Common bigrams
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TI': 6, 'ES': 6, 'OR': 6, 'TE': 6, 'OF': 6,
        'ED': 5, 'IS': 5, 'IT': 5, 'AL': 5, 'AR': 5
    }
    
    # Cicada-specific keywords
    keywords = {
        'WISDOM': 50, 'TRUTH': 50, 'DIVINE': 50, 'EMERGE': 50,
        'INSTAR': 60, 'CIRCUMFERENCE': 70, 'KNOWLEDGE': 50,
        'SEEK': 40, 'FIND': 40, 'PATH': 40, 'WITHIN': 45,
        'ENLIGHTEN': 50, 'WARNING': 40, 'INSTRUCTION': 45,
    }
    
    for i in range(len(text) - 2):
        if text[i:i+3] in trigrams:
            score += trigrams[text[i:i+3]]
    
    for i in range(len(text) - 1):
        if text[i:i+2] in bigrams:
            score += bigrams[text[i:i+2]]
    
    for kw, bonus in keywords.items():
        score += text.count(kw) * bonus
    
    return score

def get_th_frequency(text):
    """Calculate TH frequency as percentage"""
    text = text.upper()
    th_count = text.count('TH')
    total_digraphs = max(1, len(text) - 1)
    return (th_count / total_digraphs) * 100

def score_with_th_penalty(text):
    """Score with penalty for excessive TH (to address anomaly)"""
    base_score = score_english(text)
    th_freq = get_th_frequency(text)
    
    # Expected TH frequency is ~3-5% in English
    # Penalize if >10%
    if th_freq > 10:
        penalty = (th_freq - 10) * 5  # Penalty per % over 10
        return base_score - penalty, th_freq
    return base_score, th_freq

# ============================================================================
# MAIN ATTACK
# ============================================================================

def test_word_key(page_num, word, verbose=False):
    """Test a single word as a Vigenère key on the first-layer output"""
    if page_num not in FIRST_LAYER_OUTPUTS:
        return None
    
    first_layer = FIRST_LAYER_OUTPUTS[page_num]
    cipher_indices = parse_first_layer_to_indices(first_layer)
    key_indices = text_to_indices(word)
    
    if not key_indices:
        return None
    
    results = []
    
    # Test all variants
    for variant in ['standard', 'reverse', 'add', 'negadd']:
        plaintext_indices = vigenere_decrypt_variant(cipher_indices, key_indices, variant)
        plaintext_text = indices_to_text(plaintext_indices)
        score, th_freq = score_with_th_penalty(plaintext_text)
        
        results.append({
            'word': word,
            'variant': variant,
            'score': score,
            'th_freq': th_freq,
            'plaintext': plaintext_text[:100] + "..." if len(plaintext_text) > 100 else plaintext_text,
            'full_plaintext': plaintext_text
        })
    
    return results

def attack_page_with_vocabulary(page_num, top_n=20, verbose=True):
    """Test all vocabulary words against a page"""
    print(f"\n{'='*60}")
    print(f"WORD KEY ATTACK - PAGE {page_num}")
    print(f"{'='*60}")
    
    if page_num not in FIRST_LAYER_OUTPUTS:
        print(f"Error: No first-layer output for page {page_num}")
        return
    
    # Get baseline score
    first_layer = FIRST_LAYER_OUTPUTS[page_num]
    baseline_score = score_english(first_layer)
    baseline_th = get_th_frequency(first_layer)
    print(f"\nBaseline (first layer):")
    print(f"  Score: {baseline_score:.2f}")
    print(f"  TH frequency: {baseline_th:.2f}%")
    print(f"  Text: {first_layer[:80]}...")
    
    all_results = []
    
    print(f"\nTesting {len(CICADA_VOCABULARY)} vocabulary words...")
    
    for word in CICADA_VOCABULARY:
        results = test_word_key(page_num, word)
        if results:
            all_results.extend(results)
    
    # Sort by score (highest first)
    all_results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n{'='*60}")
    print(f"TOP {top_n} RESULTS")
    print(f"{'='*60}")
    
    for i, result in enumerate(all_results[:top_n]):
        improvement = result['score'] - baseline_score
        th_improvement = baseline_th - result['th_freq']
        
        print(f"\n{i+1}. Word: {result['word']}, Variant: {result['variant']}")
        print(f"   Score: {result['score']:.2f} ({'+' if improvement >= 0 else ''}{improvement:.2f} vs baseline)")
        print(f"   TH freq: {result['th_freq']:.2f}% ({'+' if th_improvement >= 0 else ''}{th_improvement:.2f}%)")
        print(f"   Text: {result['plaintext']}")
        
        # Mark potential breakthroughs
        if result['score'] > baseline_score * 1.2:
            print(f"   ⭐ POTENTIAL BREAKTHROUGH!")
        if result['th_freq'] < 10 and result['score'] > baseline_score:
            print(f"   ✓ TH normalized and score improved!")
    
    # Save detailed results
    return all_results

def find_best_across_pages(top_n=10):
    """Find the best word keys across all pages"""
    print("\n" + "="*70)
    print("CROSS-PAGE WORD KEY ANALYSIS")
    print("="*70)
    
    page_results = {}
    for page_num in FIRST_LAYER_OUTPUTS.keys():
        results = attack_page_with_vocabulary(page_num, top_n=5, verbose=False)
        if results:
            page_results[page_num] = results
    
    # Find words that work well across multiple pages
    word_scores = Counter()
    for page_num, results in page_results.items():
        for result in results[:10]:
            key = (result['word'], result['variant'])
            word_scores[key] += result['score']
    
    print("\n" + "="*70)
    print("WORDS THAT WORK BEST ACROSS ALL PAGES")
    print("="*70)
    
    for (word, variant), total_score in word_scores.most_common(top_n):
        print(f"\n{word} ({variant}): Total score {total_score:.2f}")
        for page_num, results in page_results.items():
            matching = [r for r in results if r['word'] == word and r['variant'] == variant]
            if matching:
                r = matching[0]
                print(f"  Page {page_num}: score {r['score']:.2f}, TH {r['th_freq']:.2f}%")

# ============================================================================
# ADDITIONAL EXPERIMENTS
# ============================================================================

def test_key_length_words(page_num):
    """
    Test words whose length matches the key length for that page.
    Key lengths: Page 0=113, Page 1=71, Page 2=83, Page 3=83, Page 4=103
    """
    key_lengths = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}
    
    if page_num not in key_lengths:
        return
    
    klen = key_lengths[page_num]
    print(f"\nSearching for {klen}-character phrases...")
    
    # Generate phrases by repeating/combining words to target length
    phrases = []
    
    # Single word repeated
    for word in CICADA_VOCABULARY:
        word_indices = text_to_indices(word)
        if not word_indices:
            continue
        word_len = len(word_indices)
        if klen % word_len == 0:
            repeated = word * (klen // word_len)
            phrases.append((repeated, f"{word} x {klen // word_len}"))
    
    print(f"Found {len(phrases)} phrases matching key length {klen}")
    
    # Test each phrase
    results = []
    for phrase, desc in phrases[:50]:  # Limit for speed
        result = test_word_key(page_num, phrase)
        if result:
            best = max(result, key=lambda x: x['score'])
            best['description'] = desc
            results.append(best)
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\nTop 10 phrases for Page {page_num}:")
    for r in results[:10]:
        print(f"  {r.get('description', r['word'])}: score {r['score']:.2f}")

def exhaustive_short_key_search(page_num, max_len=4):
    """
    Exhaustively search all short keys (1-4 characters).
    This helps identify if there's a simple pattern.
    """
    print(f"\n{'='*60}")
    print(f"EXHAUSTIVE SHORT KEY SEARCH - PAGE {page_num}")
    print(f"{'='*60}")
    
    if page_num not in FIRST_LAYER_OUTPUTS:
        return
    
    first_layer = FIRST_LAYER_OUTPUTS[page_num]
    cipher_indices = parse_first_layer_to_indices(first_layer)
    baseline = score_english(first_layer)
    
    best_results = []
    
    # Generate all possible keys up to max_len
    def generate_keys(length):
        if length == 0:
            return [[]]
        shorter = generate_keys(length - 1)
        result = []
        for key in shorter:
            for i in range(29):
                result.append(key + [i])
        return result
    
    for klen in range(1, max_len + 1):
        print(f"\nTesting keys of length {klen} ({29**klen} combinations)...")
        
        if 29**klen > 100000:
            print(f"  Skipping (too many combinations)")
            continue
        
        keys = generate_keys(klen)
        local_best = None
        local_best_score = baseline
        
        for key in keys:
            for variant in ['standard', 'add']:
                plain = vigenere_decrypt_variant(cipher_indices, key, variant)
                text = indices_to_text(plain)
                score = score_english(text)
                
                if score > local_best_score:
                    local_best_score = score
                    local_best = {
                        'key': key,
                        'key_text': indices_to_text(key),
                        'variant': variant,
                        'score': score,
                        'plaintext': text[:100]
                    }
        
        if local_best:
            print(f"  Best at length {klen}:")
            print(f"    Key: {local_best['key']} ({local_best['key_text']})")
            print(f"    Score: {local_best['score']:.2f} (baseline: {baseline:.2f})")
            print(f"    Text: {local_best['plaintext'][:80]}...")
            best_results.append(local_best)
    
    return best_results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Word-based key attack on Liber Primus")
    parser.add_argument('--page', type=int, default=0, help='Page number to attack')
    parser.add_argument('--all', action='store_true', help='Attack all pages')
    parser.add_argument('--cross', action='store_true', help='Cross-page analysis')
    parser.add_argument('--short', action='store_true', help='Exhaustive short key search')
    parser.add_argument('--keylength', action='store_true', help='Test key-length matching phrases')
    parser.add_argument('--top', type=int, default=20, help='Number of top results to show')
    
    args = parser.parse_args()
    
    if args.cross:
        find_best_across_pages(args.top)
    elif args.all:
        for page in FIRST_LAYER_OUTPUTS.keys():
            attack_page_with_vocabulary(page, args.top)
    elif args.short:
        exhaustive_short_key_search(args.page, max_len=3)
    elif args.keylength:
        test_key_length_words(args.page)
    else:
        attack_page_with_vocabulary(args.page, args.top)

#!/usr/bin/env python3
"""
COMBINED APPROACH - BEST KEY CANDIDATES
========================================

Based on discoveries:
1. First layer decryption: SUB with prime-length key (IoC analysis)
2. Second layer: Word-based Vigenère with thematic key

Testing the best combinations from our analysis:
- Page 0: FIBONACCI (on raw) or IP (on first-layer)  
- Page 1: BEWARE, EMERGE, NUMBERS
- Page 2: PATH, SEEK, WORDS + IP pattern
- Page 3: DIVINITY, ROAD, MAP + IP pattern
- Page 4: LIBER, EMERGE + PI pattern

Also testing the clue words: WORDS, MEANING, NUMBERS, MAP, ROAD, DIRECTION
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

PRIME_VALUES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Known good key lengths from IoC analysis
KEY_LENGTHS = {0: 113, 1: 71, 2: 83, 3: 83, 4: 103}

# First layer outputs
FIRST_LAYER_OUTPUTS = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL",
}

# ============================================================================
# FUNCTIONS
# ============================================================================

def load_page_runes(page_num):
    """Load original runes from page files"""
    base_path = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}" / "runes.txt"
    if base_path.exists():
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
        runes = [c for c in content if c in RUNE_TO_INDEX]
        return runes
    return None

def runes_to_indices(runes):
    return [RUNE_TO_INDEX[r] for r in runes]

def indices_to_text(indices):
    return "".join(LETTERS[i] for i in indices if 0 <= i < 29)

def text_to_indices(text):
    """Parse text to indices"""
    text = text.upper().replace("/", "").replace("-", "")
    indices = []
    i = 0
    while i < len(text):
        matched = False
        for length in [2, 1]:
            if i + length <= len(text):
                segment = text[i:i+length]
                if segment in LETTER_TO_INDEX:
                    indices.append(LETTER_TO_INDEX[segment])
                    i += length
                    matched = True
                    break
        if not matched:
            i += 1
    return indices

def word_to_indices(word):
    """Convert a word to indices"""
    return text_to_indices(word)

def decrypt_vigenere(cipher_indices, key_indices, operation='sub'):
    """Vigenère decryption"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if operation == 'sub':
            plaintext.append((c - k) % 29)
        else:
            plaintext.append((c + k) % 29)
    return plaintext

def score_english(text):
    """Score English-likeness"""
    text = text.upper()
    score = 0.0
    
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8,
        'ERS': 7, 'HIS': 7, 'RES': 7, 'ARE': 7, 'WIT': 6,
    }
    
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TI': 6, 'ES': 6, 'OR': 6, 'OF': 6, 'TE': 6,
    }
    
    keywords = {
        'WISDOM': 50, 'TRUTH': 50, 'DIVINE': 50, 'EMERGE': 50,
        'INSTAR': 60, 'CIRCUMFERENCE': 70, 'KNOWLEDGE': 50,
        'SEEK': 40, 'FIND': 40, 'PATH': 40, 'WITHIN': 45,
        'WARNING': 40, 'LIBER': 50, 'PRIMUS': 50, 'PARABLE': 50,
        'WAY': 30, 'MAP': 30, 'ROAD': 30, 'NUMBERS': 40,
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

def get_letter_distribution(text):
    """Get letter frequency distribution"""
    text = text.upper()
    total = len(text)
    freq = Counter(text)
    return {k: (v/total)*100 for k, v in freq.most_common(10)}

# ============================================================================
# COMBINED LAYER ATTACK
# ============================================================================

def combined_attack(page_num):
    """
    Try combining first-layer decryption with second-layer word key.
    """
    print(f"\n{'='*70}")
    print(f"COMBINED LAYER ATTACK - PAGE {page_num}")
    print(f"{'='*70}")
    
    # Load original runes
    runes = load_page_runes(page_num)
    if not runes:
        print(f"Could not load runes for page {page_num}")
        return
    
    raw_indices = runes_to_indices(runes)
    
    # Also get first-layer output
    first_layer_text = FIRST_LAYER_OUTPUTS.get(page_num, "")
    first_layer_indices = text_to_indices(first_layer_text) if first_layer_text else []
    
    print(f"Raw runes: {len(runes)}")
    print(f"First layer indices: {len(first_layer_indices)}")
    
    # Clue words from 2016 message
    clue_words = [
        # Direct from clue
        "WORDS", "MAP", "ROAD", "NUMBERS", "DIRECTION", "MEANING", "WAY",
        "BEWARE", "VERIFY",
        # Thematic
        "PRIMUS", "LIBER", "LIBERPRIMUS", "DIVINITY", "EMERGE", "INSTAR",
        "CIRCUMFERENCE", "PATH", "SEEK", "FIND", "WITHIN", "TRUTH", "WISDOM",
        # Fibonacci related
        "FIBONACCI", "PRIME", "PRIMES",
        # IP pattern words
        "IP", "PI",
    ]
    
    results = []
    
    # Test 1: Word key directly on raw runes
    print("\n--- Method 1: Word key on raw runes ---")
    for word in clue_words:
        key = word_to_indices(word)
        if not key:
            continue
        
        for op in ['sub', 'add']:
            plain = decrypt_vigenere(raw_indices, key, op)
            text = indices_to_text(plain)
            score = score_english(text)
            
            results.append({
                'method': f'raw_{op}',
                'word': word,
                'score': score,
                'text': text
            })
    
    # Test 2: Word key on first-layer output
    print("--- Method 2: Word key on first-layer output ---")
    if first_layer_indices:
        for word in clue_words:
            key = word_to_indices(word)
            if not key:
                continue
            
            for op in ['sub', 'add']:
                plain = decrypt_vigenere(first_layer_indices, key, op)
                text = indices_to_text(plain)
                score = score_english(text)
                
                results.append({
                    'method': f'layer1_{op}',
                    'word': word,
                    'score': score,
                    'text': text
                })
    
    # Test 3: Two-word combinations
    print("--- Method 3: Two-word combinations ---")
    key_combos = [
        ("LIBER", "PRIMUS"), ("FIND", "PATH"), ("SEEK", "TRUTH"),
        ("WORDS", "NUMBERS"), ("MAP", "ROAD"), ("WAY", "DIRECTION"),
        ("EMERGE", "WITHIN"), ("DIVINE", "WISDOM"),
    ]
    
    for word1, word2 in key_combos:
        key = word_to_indices(word1 + word2)
        if not key:
            continue
        
        for op in ['sub', 'add']:
            plain = decrypt_vigenere(raw_indices, key, op)
            text = indices_to_text(plain)
            score = score_english(text)
            
            results.append({
                'method': f'combo_{op}',
                'word': f'{word1}+{word2}',
                'score': score,
                'text': text
            })
    
    # Sort and display
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Get baselines
    raw_baseline = score_english(indices_to_text(raw_indices))
    layer1_baseline = score_english(first_layer_text) if first_layer_text else 0
    
    print(f"\nBaselines:")
    print(f"  Raw: {raw_baseline:.2f}")
    print(f"  First layer: {layer1_baseline:.2f}")
    
    print(f"\n{'='*70}")
    print(f"TOP 20 RESULTS FOR PAGE {page_num}")
    print(f"{'='*70}")
    
    for i, r in enumerate(results[:20]):
        print(f"{i+1:2}. {r['method']:12} {r['word']:20} score={r['score']:7.2f}")
        if i < 5:
            print(f"    Text: {r['text'][:70]}...")
    
    return results

def test_clue_pattern():
    """
    Test the pattern suggested by the clue:
    "its words are the map, their meaning is the road, and their numbers are the direction"
    
    Maybe the key is structured: [word-derived][meaning-derived][number-derived]
    """
    print("\n" + "="*70)
    print("TESTING CLUE PATTERN: WORDS + MEANING + NUMBERS")
    print("="*70)
    
    # The clue suggests a three-part structure
    # Words -> Map (navigation structure)
    # Meaning -> Road (path to follow)  
    # Numbers -> Direction (prime values guide)
    
    # Try using parts of the Parable as key
    parable = "LIKE THE INSTAR TUNNELING TO THE SURFACE WE MUST SHED OUR OWN CIRCUMFERENCES FIND THE DIVINITY WITHIN AND EMERGE"
    
    # Extract key phrases
    key_phrases = [
        "FINDTHEDIVINITY",
        "DIVINITYWITHIN", 
        "SHEDCIRCUMFERENCE",
        "EMERGE",
        "INSTAR",
        "LIKETHE",
        "MUSTSHED",
        "WITHINANDEMERGE",
    ]
    
    for page_num in range(5):
        runes = load_page_runes(page_num)
        if not runes:
            continue
        
        raw_indices = runes_to_indices(runes)
        baseline = score_english(indices_to_text(raw_indices))
        
        print(f"\nPage {page_num} (baseline: {baseline:.2f}):")
        
        best_result = None
        best_score = 0
        
        for phrase in key_phrases:
            key = word_to_indices(phrase)
            if not key:
                continue
            
            for op in ['sub', 'add']:
                plain = decrypt_vigenere(raw_indices, key, op)
                text = indices_to_text(plain)
                score = score_english(text)
                
                if score > best_score:
                    best_score = score
                    best_result = (phrase, op, text)
        
        if best_result:
            phrase, op, text = best_result
            print(f"  Best: {phrase} ({op}) score={best_score:.2f} (+{best_score-baseline:.2f})")
            print(f"  Text: {text[:80]}...")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("LIBER PRIMUS - COMBINED APPROACH ANALYSIS")
    print("="*70)
    print("\nBased on clue: 'its words are the map, their meaning is the road,")
    print("and their numbers are the direction'")
    
    # Run combined attack on all pages
    for page in range(5):
        combined_attack(page)
    
    # Test clue pattern
    test_clue_pattern()

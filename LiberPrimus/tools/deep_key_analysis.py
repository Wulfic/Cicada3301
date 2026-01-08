#!/usr/bin/env python3
"""
DEEP KEY ANALYSIS
=================

Analyzes the "IP" pattern discovery and explores related keys.
Based on finding that key [10, 13] (IP) significantly improves Pages 2-4.

I = index 10
P = index 13

This pattern may relate to:
- "In Principio" (In the beginning - Latin)
- "Inner Path"
- Or simply a mathematical relationship to resolve the TH anomaly
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

def parse_first_layer_to_indices(text):
    """Parse first layer output back to indices"""
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

def indices_to_text(indices):
    """Convert indices to readable text"""
    return "".join(LETTERS[i] for i in indices if 0 <= i < 29)

def vigenere_decrypt(cipher_indices, key_indices, operation='add'):
    """Apply Vigenère with given key"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if operation == 'sub':
            plaintext.append((c - k) % 29)
        else:  # add
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
    }
    
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
    }
    
    keywords = {
        'WISDOM': 50, 'TRUTH': 50, 'DIVINE': 50, 'EMERGE': 50,
        'INSTAR': 60, 'CIRCUMFERENCE': 70, 'KNOWLEDGE': 50,
        'SEEK': 40, 'FIND': 40, 'PATH': 40, 'WITHIN': 45,
        'ENLIGHTEN': 50, 'WARNING': 40, 'INSTRUCTION': 45,
        'LIBER': 50, 'PRIMUS': 50, 'PARABLE': 50,
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

def get_letter_frequency(text):
    """Get letter frequency as Counter"""
    text = text.upper()
    return Counter(text)

def analyze_key_on_page(page_num, key_indices, key_name):
    """Apply key and analyze the result"""
    if page_num not in FIRST_LAYER_OUTPUTS:
        return None
    
    cipher = parse_first_layer_to_indices(FIRST_LAYER_OUTPUTS[page_num])
    
    results = []
    for op in ['add', 'sub']:
        plain = vigenere_decrypt(cipher, key_indices, op)
        text = indices_to_text(plain)
        score = score_english(text)
        
        # Calculate TH frequency
        th_count = text.count('TH')
        th_freq = (th_count / max(1, len(text) - 1)) * 100
        
        results.append({
            'key_name': key_name,
            'operation': op,
            'score': score,
            'th_freq': th_freq,
            'plaintext': text,
        })
    
    return results

def main():
    print("="*70)
    print("DEEP KEY ANALYSIS: EXPLORING IP/PI PATTERN")
    print("="*70)
    
    # Keys to test
    keys_to_test = [
        # Original discoveries
        ([10, 13], "IP"),
        ([13, 10], "PI"),
        
        # Single letters I and P
        ([10], "I"),
        ([13], "P"),
        
        # Extended patterns
        ([10, 13, 10], "IPI"),
        ([13, 10, 13], "PIP"),
        ([10, 10, 13, 13], "IIPP"),
        ([13, 13, 10, 10], "PPII"),
        
        # Related words/phrases as indices
        # "INSTAR" = [10, 9, 15, 16, 24, 4]
        ([10, 9, 15, 16, 24, 4], "INSTAR"),
        # "PATH" = [13, 24, 16, 8] (P, A, T, H)
        ([13, 24, 16, 8], "PATH"),
        # "FIND" = [0, 10, 9, 23] (F, I, N, D)
        ([0, 10, 9, 23], "FIND"),
        # "SEEK" = [15, 18, 18, 5] (S, E, E, K)
        ([15, 18, 18, 5], "SEEK"),
        
        # Mathematical patterns related to I=10, P=13
        ([10, 13, 10, 13], "IPIP"),
        ([13, 10, 13, 10], "PIPI"),
        
        # Prime-related (indices 10 and 13 are both interesting)
        # Index 10 = I (prime value 31, 11th prime)
        # Index 13 = P (prime value 43, 14th prime)
        ([10, 13, 23], "IPD"),  # D=23, prime value 89
        
        # Offset patterns
        ([11, 14], "JX"),  # IP + 1
        ([9, 12], "NEO"),  # IP - 1
        
        # "LIBER" = [20, 10, 17, 18, 4]
        ([20, 10, 17, 18, 4], "LIBER"),
        # "PRIMUS" = [13, 4, 10, 19, 1, 15]
        ([13, 4, 10, 19, 1, 15], "PRIMUS"),
        
        # Testing if it's a constant shift
        ([23], "D"),  # Difference: 10+13 = 23
        ([3], "O"),   # 13-10 = 3
    ]
    
    # Analyze each key on all pages
    for page_num in sorted(FIRST_LAYER_OUTPUTS.keys()):
        print(f"\n{'='*70}")
        print(f"PAGE {page_num}")
        print(f"{'='*70}")
        
        baseline = FIRST_LAYER_OUTPUTS[page_num]
        baseline_score = score_english(baseline)
        print(f"Baseline score: {baseline_score:.2f}")
        print(f"Baseline (first 80 chars): {baseline[:80]}...")
        
        all_results = []
        
        for key_indices, key_name in keys_to_test:
            results = analyze_key_on_page(page_num, key_indices, key_name)
            if results:
                all_results.extend(results)
        
        # Sort by score
        all_results.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\nTop 10 results:")
        print("-"*70)
        
        for i, r in enumerate(all_results[:10]):
            improvement = r['score'] - baseline_score
            print(f"{i+1}. {r['key_name']:12} ({r['operation']:3}): score {r['score']:7.2f} "
                  f"({'+' if improvement >= 0 else ''}{improvement:7.2f}) TH={r['th_freq']:5.2f}%")
            
            # Show the full plaintext for the best result
            if i == 0:
                print(f"   Plaintext: {r['plaintext'][:100]}...")
    
    # Additional analysis: Word-level parsing
    print("\n" + "="*70)
    print("WORD EXTRACTION ANALYSIS (Best decryptions)")
    print("="*70)
    
    # Common English words to look for
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
        'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS',
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM',
        'THEY', 'BEEN', 'CALL', 'FIND', 'SEEK', 'PATH', 'TRUTH',
        'DIVINE', 'WISDOM', 'INSTAR', 'EMERGE', 'WITHIN', 'PRIMUS',
    ]
    
    for page_num in [2, 3, 4]:  # Focus on pages that improved most
        cipher = parse_first_layer_to_indices(FIRST_LAYER_OUTPUTS[page_num])
        
        # Use best key for this page
        if page_num in [2, 3]:
            key = [10, 13]  # IP
        else:
            key = [13, 10]  # PI
        
        plain = vigenere_decrypt(cipher, key, 'add')
        text = indices_to_text(plain)
        
        print(f"\nPage {page_num} with key {'IP' if page_num in [2,3] else 'PI'} (add):")
        print(f"Full text: {text}")
        
        # Find words
        found_words = []
        for word in common_words:
            if word in text:
                found_words.append(word)
        
        if found_words:
            print(f"Found words: {', '.join(found_words)}")

if __name__ == "__main__":
    main()

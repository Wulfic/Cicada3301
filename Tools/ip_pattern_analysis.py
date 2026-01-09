#!/usr/bin/env python3
"""
IP PATTERN DEEP DIVE
====================

The discovery that "IP" (indices [10, 13]) dramatically improves decryption
suggests there may be deeper meaning:

I = index 10 = prime value 31 (11th prime)
P = index 13 = prime value 43 (14th prime)

Possible meanings:
1. "IP" as in "In Principio" (In the beginning - Latin, like the Vulgate Bible)
2. Mathematical relationship: 10 and 13 are related (10+3=13, 13-10=3)
3. Fibonacci connection: F(5)=5, F(6)=8, F(7)=13 (13 is a Fibonacci number!)
4. Prime indices: 10 is not prime, 13 is prime
5. Gematria sum: 31+43=74 or 10+13=23 (23 is a prime, and 9th prime)

This script explores these connections and tries to extract readable text.
"""

import os
import sys
from collections import Counter
from pathlib import Path
import re

# ============================================================================
# CONSTANTS
# ============================================================================

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]
LETTER_TO_INDEX = {L: i for i, L in enumerate(LETTERS)}

PRIME_VALUES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# First layer outputs
FIRST_LAYER_OUTPUTS = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL",
}

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

def indices_to_text(indices):
    return "".join(LETTERS[i] for i in indices if 0 <= i < 29)

def decrypt_with_key(cipher_indices, key_indices, operation='add'):
    """Vigenère decryption"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        if operation == 'sub':
            plaintext.append((c - k) % 29)
        else:
            plaintext.append((c + k) % 29)
    return plaintext

# ============================================================================
# WORD EXTRACTION
# ============================================================================

# Common English words that could appear (digraph-aware)
ENGLISH_WORDS = [
    # Common short words
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
    'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HAD', 'HIM', 'HOW', 'MAN',
    'ITS', 'LET', 'OLD', 'SEE', 'WAY', 'WHO', 'DID', 'GET', 'OWN', 'SAY',
    
    # Medium words
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
    'FIND', 'SEEK', 'PATH', 'TRUTH', 'WORD', 'THEM', 'THEN', 'THAN', 'INTO',
    'ONLY', 'COME', 'MAKE', 'KNOW', 'TAKE', 'SOME', 'WHAT', 'TIME', 'VERY',
    
    # Cicada-specific
    'WISDOM', 'DIVINE', 'EMERGE', 'INSTAR', 'WITHIN', 'PRIMUS', 'LIBER',
    'CIRCUMFERENCE', 'ENLIGHTEN', 'KNOWLEDGE', 'PARABLE', 'TUNNEL',
    
    # Old English
    'THEE', 'THOU', 'THINE', 'HATH', 'DOTH', 'DOETH', 'GOETH', 'UNTO',
    'VERILY', 'BEHOLD', 'FORSOOTH', 'HENCE', 'THENCE', 'WHENCE',
    
    # Religious
    'GOD', 'LORD', 'SPIRIT', 'SOUL', 'HOLY', 'SACRED', 'DIVINE', 'LIGHT',
]

def find_words_in_text(text):
    """Find English words in the decrypted text"""
    text = text.upper()
    found = []
    
    for word in ENGLISH_WORDS:
        count = text.count(word)
        if count > 0:
            # Find positions
            positions = []
            start = 0
            while True:
                pos = text.find(word, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            found.append((word, count, positions))
    
    # Sort by word length (longer words more significant)
    found.sort(key=lambda x: len(x[0]), reverse=True)
    return found

def segment_text(text):
    """Try to segment text into words using found word boundaries"""
    text = text.upper()
    
    # Find all word matches
    matches = []
    for word in ENGLISH_WORDS:
        start = 0
        while True:
            pos = text.find(word, start)
            if pos == -1:
                break
            matches.append((pos, pos + len(word), word))
            start = pos + 1
    
    # Sort by position
    matches.sort(key=lambda x: x[0])
    
    # Try to build non-overlapping segmentation
    result = []
    last_end = 0
    
    for start, end, word in matches:
        if start >= last_end:
            if start > last_end:
                result.append(f"[{text[last_end:start]}]")
            result.append(word)
            last_end = end
    
    if last_end < len(text):
        result.append(f"[{text[last_end:]}]")
    
    return " ".join(result)

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def analyze_ip_decryption(page_num):
    """Analyze the IP-decrypted text for Page"""
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - IP PATTERN ANALYSIS")
    print(f"{'='*70}")
    
    first_layer = FIRST_LAYER_OUTPUTS.get(page_num, "")
    if not first_layer:
        return
    
    cipher = text_to_indices(first_layer)
    
    # Apply IP key
    if page_num in [2, 3]:
        key = [10, 13]  # IP
        key_name = "IP"
    else:
        key = [13, 10]  # PI
        key_name = "PI"
    
    plain = decrypt_with_key(cipher, key, 'add')
    text = indices_to_text(plain)
    
    print(f"\nKey: {key_name} (indices {key})")
    print(f"Full decrypted text ({len(text)} chars):")
    print(text)
    
    # Find words
    print(f"\n--- Words Found ---")
    found_words = find_words_in_text(text)
    
    total_word_chars = 0
    for word, count, positions in found_words[:20]:
        print(f"  {word}: {count}x at positions {positions[:5]}{'...' if len(positions) > 5 else ''}")
        total_word_chars += len(word) * count
    
    print(f"\nWord coverage: {total_word_chars}/{len(text)} chars ({100*total_word_chars/len(text):.1f}%)")
    
    # Try segmentation
    print(f"\n--- Attempted Segmentation ---")
    segmented = segment_text(text)
    print(segmented[:500] + "..." if len(segmented) > 500 else segmented)
    
    # Frequency analysis
    print(f"\n--- Letter Frequency ---")
    freq = Counter(text)
    for letter, count in freq.most_common(10):
        print(f"  {letter}: {count} ({100*count/len(text):.1f}%)")

def explore_ip_meaning():
    """Explore what IP might mean mathematically"""
    print("\n" + "="*70)
    print("EXPLORING IP MEANING")
    print("="*70)
    
    I_idx = 10
    P_idx = 13
    I_prime = PRIME_VALUES[I_idx]  # 31
    P_prime = PRIME_VALUES[P_idx]  # 43
    
    print(f"\nI = index {I_idx}, prime value {I_prime} (11th prime)")
    print(f"P = index {P_idx}, prime value {P_prime} (14th prime)")
    
    print(f"\nMathematical relationships:")
    print(f"  Sum of indices: {I_idx + P_idx} = 23 (9th prime, also a Fibonacci number!)")
    print(f"  Difference: {P_idx - I_idx} = 3 (2nd prime)")
    print(f"  Sum of primes: {I_prime + P_prime} = 74")
    print(f"  Difference of primes: {P_prime - I_prime} = 12")
    
    print(f"\nFibonacci connection:")
    print(f"  13 is the 7th Fibonacci number (F(7) = 13)")
    print(f"  Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...")
    
    print(f"\nPossible interpretations:")
    print(f"  1. 'IP' = 'In Principio' (In the beginning) - Biblical/Latin")
    print(f"  2. IP address reference (Internet Protocol)")
    print(f"  3. Intellectual Property")
    print(f"  4. Simply the most common pair in cipher statistics")
    
    # Test if 23 (sum) is significant as a key
    print(f"\n--- Testing sum=23 as shift key ---")
    for page_num in range(5):
        first_layer = FIRST_LAYER_OUTPUTS.get(page_num, "")
        if not first_layer:
            continue
        cipher = text_to_indices(first_layer)
        plain = [(c + 23) % 29 for c in cipher]
        text = indices_to_text(plain)
        words = find_words_in_text(text)
        word_count = sum(w[1] for w in words)
        print(f"  Page {page_num}: {word_count} word occurrences found")

def test_alternating_patterns():
    """Test if IP works because of alternating shift pattern"""
    print("\n" + "="*70)
    print("TESTING ALTERNATING PATTERNS")
    print("="*70)
    
    # IP means: position 0 +10, position 1 +13, position 2 +10, etc.
    # This alternates between even (+10) and odd (+13) positions
    
    for page_num in [2, 3]:
        first_layer = FIRST_LAYER_OUTPUTS.get(page_num, "")
        cipher = text_to_indices(first_layer)
        
        # Extract even and odd positions
        even_indices = cipher[::2]
        odd_indices = cipher[1::2]
        
        even_text = indices_to_text(even_indices)
        odd_text = indices_to_text(odd_indices)
        
        print(f"\nPage {page_num}:")
        print(f"  Even positions (shift +10): {even_text[:50]}...")
        print(f"  Odd positions (shift +13): {odd_text[:50]}...")
        
        # What if we apply different keys to even/odd?
        even_plain = [(c + 10) % 29 for c in even_indices]
        odd_plain = [(c + 13) % 29 for c in odd_indices]
        
        print(f"  Even +10: {indices_to_text(even_plain)[:50]}...")
        print(f"  Odd +13: {indices_to_text(odd_plain)[:50]}...")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    explore_ip_meaning()
    
    for page in range(5):
        analyze_ip_decryption(page)
    
    test_alternating_patterns()

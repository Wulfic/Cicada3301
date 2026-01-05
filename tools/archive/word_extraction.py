#!/usr/bin/env python3
"""
WORD EXTRACTION ANALYSIS - Analyze top results for word boundaries
and semantic meaning. Try to extract readable text.
"""

import json
import re
from collections import Counter

# =============================================================================
# CONSTANTS
# =============================================================================
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
         'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
NUM_RUNES = 29

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# Word lists
COMMON_WORDS = [
    'A', 'I', 
    'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 'MY', 
    'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
    'ALL', 'AND', 'ANY', 'ARE', 'BUT', 'CAN', 'DAY', 'DID', 'FOR', 'GET', 'HAD', 
    'HAS', 'HER', 'HIM', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'NEW', 'NOT', 'NOW', 
    'OLD', 'ONE', 'OUR', 'OUT', 'OWN', 'SAY', 'SEE', 'SHE', 'THE', 'TOO', 'TWO', 
    'USE', 'WAY', 'WHO', 'WHY', 'YOU',
    'BEEN', 'EACH', 'FIND', 'FROM', 'GIVE', 'GOOD', 'HAVE', 'HERE', 'INTO', 'JUST', 
    'KNOW', 'LIKE', 'LONG', 'LOOK', 'MADE', 'MAKE', 'MORE', 'MOST', 'MUCH', 'MUST', 
    'NAME', 'NEED', 'ONLY', 'OVER', 'PART', 'SAID', 'SAME', 'SELF', 'SUCH', 'TAKE', 
    'TELL', 'THAN', 'THAT', 'THEM', 'THEN', 'THEY', 'THIS', 'TIME', 'TRUE', 'WANT', 
    'WELL', 'WERE', 'WHAT', 'WHEN', 'WITH', 'WORD', 'WORK', 'YEAR', 'YOUR',
    'ABOUT', 'AFTER', 'AGAIN', 'BEING', 'COULD', 'EVERY', 'FIRST', 'FOUND', 'GREAT', 
    'KNOWN', 'LIGHT', 'MIGHT', 'OTHER', 'RIGHT', 'SHALL', 'STILL', 'THEIR', 'THERE', 
    'THESE', 'THING', 'THINK', 'THOSE', 'THREE', 'TRUTH', 'UNDER', 'WATER', 'WHERE', 
    'WHICH', 'WHILE', 'WORDS', 'WORLD', 'WOULD', 'WRITE',
    # Cicada-specific
    'WISDOM', 'WITHIN', 'SACRED', 'SPIRIT', 'DIVINE', 'HIDDEN', 'SECRET', 'CIPHER',
    'PRIMES', 'CICADA', 'INSTAR', 'EMERGE', 'SHADOW', 'PARABLE', 'MASTER', 'DISCIPLE',
    'PILGRIM', 'COMMAND', 'BELIEVE', 'CONSUME', 'BEGINNING', 'ENLIGHTEN', 'INSTRUCTION',
]

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i] for i in indices)

def decrypt_sub(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_xor(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = ((idx - offset) ^ key_val) % NUM_RUNES
        result.append(plain_idx)
    return result

# =============================================================================
# WORD SEGMENTATION
# =============================================================================

def find_words_greedy(text, word_list):
    """Greedy longest-match word segmentation."""
    words_found = []
    i = 0
    while i < len(text):
        best_word = None
        best_len = 0
        # Try to find longest word starting at position i
        for word in word_list:
            if text[i:i+len(word)] == word and len(word) > best_len:
                best_word = word
                best_len = len(word)
        if best_word:
            words_found.append(best_word)
            i += best_len
        else:
            i += 1
    return words_found

def segment_score(text, word_list):
    """Score text by how much can be segmented into words."""
    words = find_words_greedy(text, word_list)
    covered = sum(len(w) for w in words)
    return covered, words

def find_all_words_in_text(text, word_list):
    """Find all word occurrences (overlapping allowed)."""
    found = []
    for word in word_list:
        idx = 0
        while idx < len(text):
            pos = text.find(word, idx)
            if pos == -1:
                break
            found.append((pos, word))
            idx = pos + 1
    found.sort()
    return found

# =============================================================================
# ANALYZE TOP RESULTS
# =============================================================================

def analyze_top_results():
    """Load and deeply analyze top results."""
    
    # Our best results from previous runs
    top_results = [
        {'page': 52, 'method': 'sub', 'rot': 71, 'off': 1, 'score': 136.0},
        {'page': 48, 'method': 'double_xor_sub', 'rot1': 60, 'off1': 5, 'rot2': 80, 'off2': 5, 'score': 134.0},
        {'page': 31, 'method': 'double_xor_sub', 'rot1': 40, 'off1': 0, 'rot2': 20, 'off2': 20, 'score': 132.5},
        {'page': 28, 'method': 'double_add_xor', 'rot1': 10, 'off1': 25, 'rot2': 90, 'off2': 10, 'score': 131.5},
        {'page': 28, 'method': 'double_xor_xor', 'rot1': 80, 'off1': 5, 'rot2': 10, 'off2': 25, 'score': 127.0},
        {'page': 27, 'method': 'double_xor_sub', 'rot1': 70, 'off1': 10, 'rot2': 80, 'off2': 10, 'score': 125.5},
        {'page': 44, 'method': 'xor', 'rot': 77, 'off': 1, 'score': 109.5},
    ]
    
    print("=" * 80)
    print("🔍 WORD EXTRACTION ANALYSIS")
    print("=" * 80)
    
    for result in top_results:
        page = result['page']
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        
        # Decrypt
        if 'double' in result['method']:
            if 'xor_sub' in result['method']:
                dec1 = decrypt_xor(indices, result['rot1'], result['off1'])
                dec2 = decrypt_sub(dec1, result['rot2'], result['off2'])
            elif 'add_xor' in result['method']:
                dec1 = []
                for i, idx in enumerate(indices):
                    key_val = MASTER_KEY[(i + result['rot1']) % 95]
                    plain_idx = (idx + key_val + result['off1']) % NUM_RUNES
                    dec1.append(plain_idx)
                dec2 = decrypt_xor(dec1, result['rot2'], result['off2'])
            elif 'xor_xor' in result['method']:
                dec1 = decrypt_xor(indices, result['rot1'], result['off1'])
                dec2 = decrypt_xor(dec1, result['rot2'], result['off2'])
            else:
                continue
            text = indices_to_text(dec2)
        elif result['method'] == 'sub':
            text = indices_to_text(decrypt_sub(indices, result['rot'], result['off']))
        elif result['method'] == 'xor':
            text = indices_to_text(decrypt_xor(indices, result['rot'], result['off']))
        else:
            continue
        
        print(f"\n{'=' * 60}")
        print(f"PAGE {page} - {result['method']} (Score: {result['score']})")
        print("=" * 60)
        print(f"Full text: {text}")
        
        # Find all words
        all_words = find_all_words_in_text(text, COMMON_WORDS)
        print(f"\nWords found ({len(all_words)}):")
        for pos, word in all_words:
            print(f"  Position {pos:3d}: {word}")
        
        # Try word segmentation
        coverage, segments = segment_score(text, COMMON_WORDS)
        print(f"\nSegmentation coverage: {coverage}/{len(text)} = {100*coverage/len(text):.1f}%")
        print(f"Segments: {' '.join(segments)}")
        
        # Character frequency
        freq = Counter(text)
        print(f"\nCharacter frequency: {dict(freq.most_common(10))}")
        
        # Try to manually insert word breaks where we see patterns
        print(f"\nManual word break attempts:")
        
        # Look for THE
        for i in range(len(text) - 2):
            if text[i:i+3] == 'THE':
                # Try to extend the word
                for j in range(min(15, len(text) - i), 2, -1):
                    word = text[i:i+j]
                    if word in COMMON_WORDS:
                        print(f"  Found: '{word}' at position {i}")
                        break

def analyze_page_52_deeply():
    """Deep analysis of the best result (Page 52)."""
    print("\n" + "=" * 80)
    print("🔬 DEEP ANALYSIS OF PAGE 52 (BEST RESULT)")
    print("=" * 80)
    
    indices = unicode_to_indices(UNSOLVED_PAGES[52])
    
    # Best parameters: rot=71, off=1, sub
    text = indices_to_text(decrypt_sub(indices, 71, 1))
    print(f"\nDecrypted text (rot=71, off=1):")
    print(text)
    
    # Try every offset to see if we can improve word boundaries
    print("\n🔄 Testing all offsets for Page 52 (rot=71):")
    best_coverage = 0
    best_off = 0
    for off in range(29):
        dec_text = indices_to_text(decrypt_sub(indices, 71, off))
        coverage, _ = segment_score(dec_text, COMMON_WORDS)
        if coverage > best_coverage:
            best_coverage = coverage
            best_off = off
        if off < 10 or coverage > 30:
            print(f"  Off={off:2d}: coverage={coverage:3d} | {dec_text[:60]}")
    
    print(f"\n✅ Best offset for rot=71: off={best_off} (coverage={best_coverage})")
    
    # Try nearby rotations
    print("\n🔄 Testing nearby rotations (off=1):")
    for rot in range(65, 78):
        dec_text = indices_to_text(decrypt_sub(indices, rot, 1))
        coverage, _ = segment_score(dec_text, COMMON_WORDS)
        words = find_all_words_in_text(dec_text, COMMON_WORDS)
        print(f"  Rot={rot:2d}: coverage={coverage:3d}, words={len(words):2d} | {dec_text[:60]}")

def analyze_patterns():
    """Look for patterns across all results."""
    print("\n" + "=" * 80)
    print("📊 PATTERN ANALYSIS ACROSS ALL PAGES")
    print("=" * 80)
    
    # For each page, find the rotation that produces most words
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        best_score = 0
        best_params = None
        best_text = ""
        
        for rot in range(95):
            for off in range(29):
                dec_text = indices_to_text(decrypt_sub(indices, rot, off))
                coverage, segments = segment_score(dec_text, COMMON_WORDS)
                if coverage > best_score:
                    best_score = coverage
                    best_params = (rot, off)
                    best_text = dec_text
        
        results.append({
            'page': page,
            'rot': best_params[0],
            'off': best_params[1],
            'coverage': best_score,
            'text': best_text[:80]
        })
        
        print(f"Page {page}: rot={best_params[0]:2d}, off={best_params[1]:2d}, coverage={best_score:3d}/{len(indices)}")
    
    # Check if there's a pattern in the best rotations
    rots = [r['rot'] for r in results]
    offs = [r['off'] for r in results]
    print(f"\nRotation distribution: {Counter(rots)}")
    print(f"Offset distribution: {Counter(offs)}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    analyze_top_results()
    analyze_page_52_deeply()
    analyze_patterns()
    
    print("\n" + "=" * 80)
    print("🎯 WORD EXTRACTION ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
DEEP BRUTE FORCE - Fine-grained testing around best results.
Also tries multi-layer combinations more exhaustively.
"""

import sys
import json
import time
from collections import Counter

# =============================================================================
# CONSTANTS (same as before)
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

# Extended word lists for scoring
ENGLISH_WORDS = [
    # 3-letter
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'OLD', 'SEE',
    'NOW', 'WAY', 'WHO', 'DID', 'GET', 'HIM', 'OWN', 'SAY', 'SHE', 'TOO', 'USE',
    # 4-letter
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL',
    'EACH', 'INTO', 'MAKE', 'THAN', 'THEM', 'THEN', 'LOOK', 'ONLY', 'OVER', 'SUCH',
    'TAKE', 'COME', 'MADE', 'FIND', 'MORE', 'LONG', 'HERE', 'KNOW', 'SELF', 'SEEK',
    'TRUE', 'MIND', 'SOUL', 'PATH', 'WORD', 'LIFE', 'DEAD', 'DARK', 'DEEP',
    # 5-letter  
    'THERE', 'THEIR', 'ABOUT', 'WOULD', 'THESE', 'OTHER', 'WORDS', 'COULD', 'WRITE',
    'FIRST', 'WATER', 'AFTER', 'WHERE', 'RIGHT', 'THINK', 'THREE', 'BEING', 'TRUTH',
    'LIGHT', 'THING', 'WHICH', 'SHALL', 'THOSE', 'EVERY', 'GREAT', 'WORLD', 'STILL',
    # 6+ letter
    'SACRED', 'WITHIN', 'WISDOM', 'PRIMES', 'DIVINE', 'SPIRIT', 'CICADA', 'HIDDEN',
    'SECRET', 'ANSWER', 'PUZZLE', 'CIPHER', 'ENIGMA', 'INSTAR', 'EMERGE', 'SHADOW',
    'KNOWLEDGE', 'ENCRYPTED', 'TOTIENT', 'FUNCTION', 'INSTRUCTION', 'NOTHING',
]

LATIN_WORDS = [
    'ET', 'AD', 'DE', 'IN', 'AB', 'EX', 'UT', 'NE', 'SI', 'AC', 'AT', 'AN', 'ID',
    'DEO', 'SOL', 'LUX', 'AER', 'EST', 'SUB', 'PER', 'PRO', 'SED', 'CUM', 'IAM',
    'VIA', 'VIS', 'REX', 'LEX', 'PAX', 'NOX', 'VOX', 'DUX', 'LIS',
    'HAEC', 'QUOD', 'QUIA', 'ERGO', 'IDEM', 'IPSE', 'OPUS', 'VITA', 'MORS',
    'VERITAS', 'LIBERTAS', 'AETERNITAS', 'COGITO', 'SPIRITUS', 'ANIMA',
    'OMNIA', 'NIHIL', 'PRIMA', 'FINIS', 'INITIUM', 'DIVINUS',
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

def score_text(text):
    score = 0
    for word in ENGLISH_WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word) * 3
    for word in LATIN_WORDS:
        count = text.count(word)
        if count > 0:
            score += count * len(word) * 2
    # Digraphs
    for dg in ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE', 'ED', 'ND', 'HA', 'AT', 'EN']:
        score += text.count(dg) * 0.5
    return score

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

def decrypt_add(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx + key_val + offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_interleaved(indices, rot1, rot2, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        rotation = rot1 if i % 2 == 0 else rot2
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_triple_interleaved(indices, rot1, rot2, rot3, offset):
    """Interleave with 3 different rotations."""
    result = []
    key_len = len(MASTER_KEY)
    rotations = [rot1, rot2, rot3]
    for i, idx in enumerate(indices):
        rotation = rotations[i % 3]
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def columnar_transpose(text, width):
    if width <= 0 or width >= len(text):
        return text
    rows = [text[i:i+width] for i in range(0, len(text), width)]
    result = []
    for col in range(width):
        for row in rows:
            if col < len(row):
                result.append(row[col])
    return ''.join(result)

def columnar_untranspose(text, width):
    if width <= 0 or width >= len(text):
        return text
    n = len(text)
    full_rows = n // width
    remainder = n % width
    result = [''] * n
    pos = 0
    for col in range(width):
        col_len = full_rows + (1 if col < remainder else 0)
        for row in range(col_len):
            result[row * width + col] = text[pos]
            pos += 1
    return ''.join(result)

# =============================================================================
# FINE-GRAINED TESTING AROUND BEST RESULTS
# =============================================================================

# Best results from previous run
BEST_RESULTS = [
    {'page': 52, 'method': 'sub', 'rot': 71, 'off': 1, 'score': 117.5},
    {'page': 29, 'method': 'columnar', 'rot': 15, 'off': 12, 'width': 13, 'score': 111.0},
    {'page': 29, 'method': 'reversed_xor', 'rot': 63, 'off': 4, 'score': 109.5},
    {'page': 44, 'method': 'xor', 'rot': 77, 'off': 1, 'score': 108.0},
    {'page': 45, 'method': 'interleaved', 'rot1': 40, 'rot2': 15, 'off': 21, 'score': 105.0},
    {'page': 48, 'method': 'interleaved', 'rot1': 50, 'rot2': 20, 'off': 6, 'score': 103.5},
    {'page': 30, 'method': 'add', 'rot': 37, 'off': 21, 'score': 102.0},
    {'page': 40, 'method': 'xor', 'rot': 33, 'off': 15, 'score': 99.0},
]

def fine_tune_around_best():
    """Fine-tune parameters around the best results."""
    results = []
    
    for best in BEST_RESULTS:
        page = best['page']
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        
        if best['method'] == 'sub':
            base_rot = best['rot']
            base_off = best['off']
            
            # Test nearby parameters
            for rot in range(max(0, base_rot - 5), min(95, base_rot + 6)):
                for off in range(29):
                    decrypted = decrypt_sub(indices, rot, off)
                    text = indices_to_text(decrypted)
                    score = score_text(text)
                    if score >= 100:
                        results.append({
                            'page': page, 'method': 'sub_fine',
                            'params': {'rot': rot, 'off': off},
                            'score': score, 'text': text[:100]
                        })
        
        elif best['method'] == 'xor':
            base_rot = best['rot']
            base_off = best['off']
            
            for rot in range(max(0, base_rot - 5), min(95, base_rot + 6)):
                for off in range(29):
                    decrypted = decrypt_xor(indices, rot, off)
                    text = indices_to_text(decrypted)
                    score = score_text(text)
                    if score >= 100:
                        results.append({
                            'page': page, 'method': 'xor_fine',
                            'params': {'rot': rot, 'off': off},
                            'score': score, 'text': text[:100]
                        })
        
        elif best['method'] == 'interleaved':
            base_rot1 = best['rot1']
            base_rot2 = best['rot2']
            base_off = best['off']
            
            # Fine-tune interleaved
            for rot1 in range(max(0, base_rot1 - 10), min(95, base_rot1 + 11)):
                for rot2 in range(max(0, base_rot2 - 10), min(95, base_rot2 + 11)):
                    for off in range(29):
                        decrypted = decrypt_interleaved(indices, rot1, rot2, off)
                        text = indices_to_text(decrypted)
                        score = score_text(text)
                        if score >= 100:
                            results.append({
                                'page': page, 'method': 'interleaved_fine',
                                'params': {'rot1': rot1, 'rot2': rot2, 'off': off},
                                'score': score, 'text': text[:100]
                            })
    
    return results

def test_triple_interleaved():
    """Test 3-way interleaved keys."""
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        # Test triple interleaved with step 15
        for rot1 in range(0, 95, 15):
            for rot2 in range(0, 95, 15):
                for rot3 in range(0, 95, 15):
                    for off in range(0, 29, 5):
                        decrypted = decrypt_triple_interleaved(indices, rot1, rot2, rot3, off)
                        text_out = indices_to_text(decrypted)
                        score = score_text(text_out)
                        if score >= 100:
                            results.append({
                                'page': page, 'method': 'triple_interleaved',
                                'params': {'rot1': rot1, 'rot2': rot2, 'rot3': rot3, 'off': off},
                                'score': score, 'text': text_out[:100]
                            })
    
    return results

def test_decrypt_then_decrypt():
    """Test double decryption with various operations."""
    results = []
    ops = [('sub', decrypt_sub), ('xor', decrypt_xor), ('add', decrypt_add)]
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        for op1_name, op1 in ops:
            for rot1 in range(0, 95, 10):
                for off1 in range(0, 29, 5):
                    dec1 = op1(indices, rot1, off1)
                    
                    for op2_name, op2 in ops:
                        for rot2 in range(0, 95, 10):
                            for off2 in range(0, 29, 5):
                                dec2 = op2(dec1, rot2, off2)
                                text_out = indices_to_text(dec2)
                                score = score_text(text_out)
                                if score >= 120:
                                    results.append({
                                        'page': page, 'method': f'double_{op1_name}_{op2_name}',
                                        'params': {'rot1': rot1, 'off1': off1, 'rot2': rot2, 'off2': off2},
                                        'score': score, 'text': text_out[:100]
                                    })
    
    return results

def test_all_columnar_widths():
    """Test all columnar transposition widths exhaustively."""
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        page_len = len(indices)
        
        for rot in range(95):
            for off in range(29):
                decrypted = decrypt_sub(indices, rot, off)
                text_dec = indices_to_text(decrypted)
                
                # Test all possible widths
                for width in range(2, min(50, page_len)):
                    transposed = columnar_transpose(text_dec, width)
                    score = score_text(transposed)
                    if score >= 120:
                        results.append({
                            'page': page, 'method': 'columnar_exhaustive',
                            'params': {'rot': rot, 'off': off, 'width': width},
                            'score': score, 'text': transposed[:100]
                        })
                    
                    # Also try untranspose
                    untransposed = columnar_untranspose(text_dec, width)
                    score = score_text(untransposed)
                    if score >= 120:
                        results.append({
                            'page': page, 'method': 'columnar_inv_exhaustive',
                            'params': {'rot': rot, 'off': off, 'width': width},
                            'score': score, 'text': untransposed[:100]
                        })
    
    return results

def test_position_dependent_offset():
    """Test position-dependent offset patterns."""
    results = []
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        # Pattern 1: offset increases by 1 for each position
        for base_rot in range(0, 95, 5):
            for base_off in range(29):
                decrypted = []
                for i, idx in enumerate(indices):
                    key_val = MASTER_KEY[(i + base_rot) % 95]
                    pos_off = (base_off + i) % 29
                    plain_idx = (idx - key_val - pos_off) % NUM_RUNES
                    decrypted.append(plain_idx)
                
                text_out = indices_to_text(decrypted)
                score = score_text(text_out)
                if score >= 100:
                    results.append({
                        'page': page, 'method': 'pos_offset_linear',
                        'params': {'rot': base_rot, 'base_off': base_off},
                        'score': score, 'text': text_out[:100]
                    })
        
        # Pattern 2: offset based on position mod prime
        for prime in [3, 5, 7, 11, 13]:
            for base_rot in range(0, 95, 10):
                for base_off in range(29):
                    decrypted = []
                    for i, idx in enumerate(indices):
                        key_val = MASTER_KEY[(i + base_rot) % 95]
                        pos_off = (base_off + (i % prime)) % 29
                        plain_idx = (idx - key_val - pos_off) % NUM_RUNES
                        decrypted.append(plain_idx)
                    
                    text_out = indices_to_text(decrypted)
                    score = score_text(text_out)
                    if score >= 100:
                        results.append({
                            'page': page, 'method': f'pos_offset_mod{prime}',
                            'params': {'rot': base_rot, 'base_off': base_off, 'prime': prime},
                            'score': score, 'text': text_out[:100]
                        })
    
    return results

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔥 DEEP BRUTE FORCE - FINE-GRAINED ANALYSIS")
    print("=" * 80)
    
    all_results = []
    
    # Phase 1: Fine-tune around best results
    print("\n📊 Phase 1: Fine-tuning around best results...")
    start = time.time()
    results = fine_tune_around_best()
    all_results.extend(results)
    print(f"  Found {len(results)} results ({time.time()-start:.1f}s)")
    
    # Phase 2: Triple interleaved
    print("\n📊 Phase 2: Triple interleaved testing...")
    start = time.time()
    results = test_triple_interleaved()
    all_results.extend(results)
    print(f"  Found {len(results)} results ({time.time()-start:.1f}s)")
    
    # Phase 3: Double decryption
    print("\n📊 Phase 3: Double decryption testing...")
    start = time.time()
    results = test_decrypt_then_decrypt()
    all_results.extend(results)
    print(f"  Found {len(results)} results ({time.time()-start:.1f}s)")
    
    # Phase 4: Position-dependent offset
    print("\n📊 Phase 4: Position-dependent offset testing...")
    start = time.time()
    results = test_position_dependent_offset()
    all_results.extend(results)
    print(f"  Found {len(results)} results ({time.time()-start:.1f}s)")
    
    # Phase 5: Exhaustive columnar (limited pages)
    print("\n📊 Phase 5: Exhaustive columnar testing (pages 52, 44, 29)...")
    start = time.time()
    results = []
    for page in [52, 44, 29]:
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        page_len = len(indices)
        
        for rot in range(0, 95, 2):
            for off in range(0, 29, 2):
                decrypted = decrypt_sub(indices, rot, off)
                text_dec = indices_to_text(decrypted)
                
                for width in range(2, min(40, page_len)):
                    transposed = columnar_transpose(text_dec, width)
                    score = score_text(transposed)
                    if score >= 120:
                        results.append({
                            'page': page, 'method': 'columnar_exhaustive',
                            'params': {'rot': rot, 'off': off, 'width': width},
                            'score': score, 'text': transposed[:100]
                        })
    all_results.extend(results)
    print(f"  Found {len(results)} results ({time.time()-start:.1f}s)")
    
    # Sort and display
    all_results.sort(key=lambda x: -x['score'])
    
    print("\n" + "=" * 80)
    print("🏆 TOP 30 RESULTS FROM DEEP ANALYSIS")
    print("=" * 80)
    
    seen = set()
    count = 0
    for result in all_results:
        key = (result['page'], result['text'][:50])
        if key in seen:
            continue
        seen.add(key)
        count += 1
        if count > 30:
            break
        
        print(f"\n#{count} - Page {result['page']}: Score {result['score']:.1f}")
        print(f"   Method: {result['method']}")
        print(f"   Params: {result['params']}")
        print(f"   Text: {result['text']}")
    
    # Save results
    with open('c:/Users/tyler/Repos/Cicada3301/tools/deep_brute_results.json', 'w') as f:
        json.dump(all_results[:500], f, indent=2)
    
    print(f"\n💾 Saved {len(all_results)} results")
    print("\n" + "=" * 80)
    print("🎯 DEEP ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
BRUTE FORCE ANALYSIS - Test ALL combinations with maximum processing power.
Tests: All rotations, all offsets, all transpositions, all operations, all pages.
"""

import sys
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import Counter
import time
import json

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

# Common English words for scoring
ENGLISH_WORDS = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 
                 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS',
                 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY',
                 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'WILL', 'WHAT',
                 'WHEN', 'YOUR', 'SOME', 'THEM', 'INTO', 'WHICH', 'THERE', 'THEIR',
                 'TRUTH', 'BEING', 'LIGHT', 'WISDOM', 'KNOW', 'THING', 'SACRED', 'PRIME',
                 'WITHIN', 'DEEP', 'PAGE', 'SEEK', 'FIND', 'PATH', 'SELF', 'MIND']

LATIN_WORDS = ['ET', 'AD', 'DE', 'IN', 'AB', 'EX', 'UT', 'NE', 'SI', 'AC', 'DEO', 'SOL',
               'LUX', 'AER', 'EST', 'SUB', 'PER', 'PRO', 'HAEC', 'HOC', 'HIC', 'DUM',
               'SUM', 'DUO', 'VIA', 'VERITAS', 'VITA', 'AMOR', 'MORS', 'DEUS']

DIGRAPHS = ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE', 'ED', 'ND', 'HA', 'AT', 'EN',
            'ES', 'OF', 'OR', 'NT', 'EA', 'TI', 'TO', 'IT', 'ST', 'IO', 'LE', 'IS']

def unicode_to_indices(text):
    """Convert Unicode runes to indices."""
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(RUNES[i] for i in indices)

def score_text(text):
    """Score text for English/Latin readability."""
    score = 0
    for word in ENGLISH_WORDS:
        score += text.count(word) * len(word) * 3
    for word in LATIN_WORDS:
        score += text.count(word) * len(word) * 2
    for dg in DIGRAPHS:
        score += text.count(dg) * 0.5
    return score

# =============================================================================
# DECRYPTION FUNCTIONS
# =============================================================================

def decrypt_sub(indices, rotation, offset):
    """Subtraction decryption."""
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_xor(indices, rotation, offset):
    """XOR decryption."""
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = ((idx - offset) ^ key_val) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_add(indices, rotation, offset):
    """Addition decryption."""
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx + key_val + offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_interleaved(indices, rot1, rot2, offset):
    """Interleaved key decryption."""
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        rotation = rot1 if i % 2 == 0 else rot2
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

# =============================================================================
# TRANSPOSITION FUNCTIONS
# =============================================================================

def columnar_transpose(text, width):
    """Apply columnar transposition."""
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
    """Reverse columnar transposition."""
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

def rail_fence_encrypt(text, rails):
    """Apply rail fence cipher."""
    if rails <= 1 or rails >= len(text):
        return text
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(text, rails):
    """Decrypt rail fence cipher."""
    if rails <= 1 or rails >= len(text):
        return text
    n = len(text)
    fence = [[None] * n for _ in range(rails)]
    rail = 0
    direction = 1
    for i in range(n):
        fence[rail][i] = True
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    idx = 0
    for r in range(rails):
        for c in range(n):
            if fence[r][c]:
                fence[r][c] = text[idx]
                idx += 1
    result = []
    rail = 0
    direction = 1
    for i in range(n):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(result)

def skip_cipher(text, skip, start=0):
    """Read every Nth character."""
    return ''.join(text[i] for i in range(start, len(text), skip))

def reverse_text(text):
    """Reverse the text."""
    return text[::-1]

# =============================================================================
# BRUTE FORCE TEST FUNCTIONS
# =============================================================================

def test_page_basic(page, indices):
    """Test all basic rotation/offset combinations."""
    results = []
    for rotation in range(95):
        for offset in range(29):
            for op_name, op_func in [('sub', decrypt_sub), ('xor', decrypt_xor), ('add', decrypt_add)]:
                decrypted = op_func(indices, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score >= 80:
                    results.append({
                        'page': page,
                        'method': f'basic_{op_name}',
                        'params': {'rot': rotation, 'off': offset},
                        'score': score,
                        'text': text[:80]
                    })
    return results

def test_page_interleaved(page, indices):
    """Test interleaved key combinations."""
    results = []
    for rot1 in range(0, 95, 5):  # Step by 5 for speed
        for rot2 in range(0, 95, 5):
            for offset in range(0, 29, 3):
                decrypted = decrypt_interleaved(indices, rot1, rot2, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score >= 80:
                    results.append({
                        'page': page,
                        'method': 'interleaved',
                        'params': {'rot1': rot1, 'rot2': rot2, 'off': offset},
                        'score': score,
                        'text': text[:80]
                    })
    return results

def test_page_transpose_after_decrypt(page, indices):
    """Test transposition after decryption."""
    results = []
    # Test subset of rotations for speed
    for rotation in range(0, 95, 3):
        for offset in range(0, 29, 2):
            decrypted = decrypt_sub(indices, rotation, offset)
            text = indices_to_text(decrypted)
            
            # Columnar transposition
            for width in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
                transposed = columnar_transpose(text, width)
                score = score_text(transposed)
                if score >= 100:
                    results.append({
                        'page': page,
                        'method': 'decrypt_then_columnar',
                        'params': {'rot': rotation, 'off': offset, 'width': width},
                        'score': score,
                        'text': transposed[:80]
                    })
                
                # Also try untranspose
                untransposed = columnar_untranspose(text, width)
                score = score_text(untransposed)
                if score >= 100:
                    results.append({
                        'page': page,
                        'method': 'decrypt_then_columnar_inv',
                        'params': {'rot': rotation, 'off': offset, 'width': width},
                        'score': score,
                        'text': untransposed[:80]
                    })
            
            # Rail fence
            for rails in [3, 4, 5, 6, 7]:
                rf_enc = rail_fence_encrypt(text, rails)
                score = score_text(rf_enc)
                if score >= 100:
                    results.append({
                        'page': page,
                        'method': 'decrypt_then_railfence',
                        'params': {'rot': rotation, 'off': offset, 'rails': rails},
                        'score': score,
                        'text': rf_enc[:80]
                    })
                
                rf_dec = rail_fence_decrypt(text, rails)
                score = score_text(rf_dec)
                if score >= 100:
                    results.append({
                        'page': page,
                        'method': 'decrypt_then_railfence_inv',
                        'params': {'rot': rotation, 'off': offset, 'rails': rails},
                        'score': score,
                        'text': rf_dec[:80]
                    })
    return results

def test_page_transpose_before_decrypt(page, indices):
    """Test transposition before decryption."""
    results = []
    text = indices_to_text(indices)
    
    for width in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        # Columnar transpose then decrypt
        transposed = columnar_transpose(text, width)
        trans_indices = [RUNE_TO_IDX.get(r, 0) for r in [transposed[i:i+2] if transposed[i:i+2] in RUNE_TO_IDX else transposed[i] for i in range(len(transposed))]]
        # Re-parse properly
        trans_runes = []
        i = 0
        while i < len(transposed):
            if i + 1 < len(transposed) and transposed[i:i+2] in RUNE_TO_IDX:
                trans_runes.append(RUNE_TO_IDX[transposed[i:i+2]])
                i += 2
            elif transposed[i] in RUNE_TO_IDX:
                trans_runes.append(RUNE_TO_IDX[transposed[i]])
                i += 1
            else:
                i += 1
        
        for rotation in range(0, 95, 5):
            for offset in range(0, 29, 3):
                if trans_runes:
                    decrypted = decrypt_sub(trans_runes, rotation, offset)
                    dec_text = indices_to_text(decrypted)
                    score = score_text(dec_text)
                    if score >= 100:
                        results.append({
                            'page': page,
                            'method': 'columnar_then_decrypt',
                            'params': {'width': width, 'rot': rotation, 'off': offset},
                            'score': score,
                            'text': dec_text[:80]
                        })
    return results

def test_page_skip_cipher(page, indices):
    """Test skip cipher after decryption."""
    results = []
    for rotation in range(0, 95, 5):
        for offset in range(0, 29, 3):
            decrypted = decrypt_sub(indices, rotation, offset)
            text = indices_to_text(decrypted)
            
            for skip in [2, 3, 5, 7, 11]:
                for start in range(min(skip, 3)):
                    skipped = skip_cipher(text, skip, start)
                    score = score_text(skipped)
                    if score >= 50:
                        results.append({
                            'page': page,
                            'method': 'decrypt_then_skip',
                            'params': {'rot': rotation, 'off': offset, 'skip': skip, 'start': start},
                            'score': score,
                            'text': skipped[:80]
                        })
    return results

def test_page_reversed(page, indices):
    """Test reversed indices."""
    results = []
    reversed_indices = list(reversed(indices))
    
    for rotation in range(0, 95, 3):
        for offset in range(0, 29, 2):
            for op_name, op_func in [('sub', decrypt_sub), ('xor', decrypt_xor)]:
                decrypted = op_func(reversed_indices, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score >= 80:
                    results.append({
                        'page': page,
                        'method': f'reversed_{op_name}',
                        'params': {'rot': rotation, 'off': offset},
                        'score': score,
                        'text': text[:80]
                    })
    return results

def test_page_double_key(page, indices):
    """Test applying key twice with different parameters."""
    results = []
    for rot1 in range(0, 95, 10):
        for off1 in range(0, 29, 5):
            # First decryption
            decrypted1 = decrypt_sub(indices, rot1, off1)
            
            for rot2 in range(0, 95, 10):
                for off2 in range(0, 29, 5):
                    # Second decryption
                    decrypted2 = decrypt_sub(decrypted1, rot2, off2)
                    text = indices_to_text(decrypted2)
                    score = score_text(text)
                    if score >= 100:
                        results.append({
                            'page': page,
                            'method': 'double_decrypt',
                            'params': {'rot1': rot1, 'off1': off1, 'rot2': rot2, 'off2': off2},
                            'score': score,
                            'text': text[:80]
                        })
    return results

def test_page_prime_formulas(page, indices):
    """Test prime-based formulas."""
    results = []
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 311, 1033, 3301]
    
    for p in primes:
        for formula in ['mult', 'add', 'sub', 'xor_prime']:
            if formula == 'mult':
                rot = (page * p) % 95
                off = (page * p) % 29
            elif formula == 'add':
                rot = (page + p) % 95
                off = (page + p) % 29
            elif formula == 'sub':
                rot = (p - page) % 95
                off = (p - page) % 29
            else:
                rot = (page ^ p) % 95
                off = (page ^ p) % 29
            
            for op_name, op_func in [('sub', decrypt_sub), ('xor', decrypt_xor)]:
                decrypted = op_func(indices, rot, off)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score >= 80:
                    results.append({
                        'page': page,
                        'method': f'prime_{formula}_{op_name}',
                        'params': {'prime': p, 'rot': rot, 'off': off},
                        'score': score,
                        'text': text[:80]
                    })
    return results

def test_single_page(args):
    """Test a single page with all methods."""
    page, page_text = args
    indices = unicode_to_indices(page_text)
    
    all_results = []
    all_results.extend(test_page_basic(page, indices))
    all_results.extend(test_page_interleaved(page, indices))
    all_results.extend(test_page_transpose_after_decrypt(page, indices))
    all_results.extend(test_page_skip_cipher(page, indices))
    all_results.extend(test_page_reversed(page, indices))
    all_results.extend(test_page_double_key(page, indices))
    all_results.extend(test_page_prime_formulas(page, indices))
    
    return all_results

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔥 BRUTE FORCE ANALYSIS - MAXIMUM POWER")
    print("=" * 80)
    print(f"Testing {len(UNSOLVED_PAGES)} pages with ALL combinations...")
    print()
    
    start_time = time.time()
    all_results = []
    
    # Process each page
    for page, page_text in sorted(UNSOLVED_PAGES.items()):
        print(f"🔄 Processing Page {page}...", end=" ", flush=True)
        page_start = time.time()
        
        results = test_single_page((page, page_text))
        all_results.extend(results)
        
        page_time = time.time() - page_start
        print(f"Done! ({len(results)} results, {page_time:.1f}s)")
    
    total_time = time.time() - start_time
    print()
    print(f"✅ Total: {len(all_results)} high-scoring results in {total_time:.1f}s")
    print()
    
    # Sort by score
    all_results.sort(key=lambda x: -x['score'])
    
    # Print top results
    print("=" * 80)
    print("🏆 TOP 50 RESULTS")
    print("=" * 80)
    
    for i, result in enumerate(all_results[:50]):
        print(f"\n#{i+1} - Page {result['page']}: Score {result['score']:.1f}")
        print(f"   Method: {result['method']}")
        print(f"   Params: {result['params']}")
        print(f"   Text: {result['text']}")
    
    # Group by page
    print()
    print("=" * 80)
    print("📊 BEST RESULT PER PAGE")
    print("=" * 80)
    
    best_per_page = {}
    for result in all_results:
        page = result['page']
        if page not in best_per_page or result['score'] > best_per_page[page]['score']:
            best_per_page[page] = result
    
    for page in sorted(best_per_page.keys()):
        result = best_per_page[page]
        print(f"\nPage {page}: Score {result['score']:.1f}")
        print(f"  Method: {result['method']}, Params: {result['params']}")
        print(f"  Text: {result['text'][:60]}...")
    
    # Save all results to file
    output_file = 'c:/Users/tyler/Repos/Cicada3301/tools/brute_force_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results[:1000], f, indent=2)  # Save top 1000
    print(f"\n💾 Saved top 1000 results to {output_file}")
    
    # Look for patterns in winning methods
    print()
    print("=" * 80)
    print("📈 METHOD FREQUENCY IN TOP 100")
    print("=" * 80)
    
    method_counts = Counter(r['method'] for r in all_results[:100])
    for method, count in method_counts.most_common():
        print(f"  {method}: {count}")
    
    print()
    print("=" * 80)
    print("🎯 ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

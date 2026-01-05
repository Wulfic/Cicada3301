#!/usr/bin/env python3
"""
MULTI-LAYER DEEP ANALYSIS - Focus on double/triple decryption
and advanced transposition patterns that are scoring highest.
"""

import sys
import json
import time
from collections import Counter
import itertools

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

# Extended word lists
ENGLISH_WORDS = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'OLD', 'SEE',
    'NOW', 'WAY', 'WHO', 'DID', 'GET', 'HIM', 'OWN', 'SAY', 'SHE', 'TOO', 'USE',
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL',
    'EACH', 'INTO', 'MAKE', 'THAN', 'THEM', 'THEN', 'LOOK', 'ONLY', 'OVER', 'SUCH',
    'TAKE', 'COME', 'MADE', 'FIND', 'MORE', 'LONG', 'HERE', 'KNOW', 'SELF', 'SEEK',
    'TRUE', 'MIND', 'SOUL', 'PATH', 'WORD', 'LIFE', 'DEAD', 'DARK', 'DEEP',
    'THERE', 'THEIR', 'ABOUT', 'WOULD', 'THESE', 'OTHER', 'WORDS', 'COULD', 'WRITE',
    'FIRST', 'WATER', 'AFTER', 'WHERE', 'RIGHT', 'THINK', 'THREE', 'BEING', 'TRUTH',
    'LIGHT', 'THING', 'WHICH', 'SHALL', 'THOSE', 'EVERY', 'GREAT', 'WORLD', 'STILL',
    'SACRED', 'WITHIN', 'WISDOM', 'PRIMES', 'DIVINE', 'SPIRIT', 'CICADA', 'HIDDEN',
    'SECRET', 'ANSWER', 'PUZZLE', 'CIPHER', 'ENIGMA', 'INSTAR', 'EMERGE', 'SHADOW',
    'KNOWLEDGE', 'ENCRYPTED', 'TOTIENT', 'FUNCTION', 'INSTRUCTION', 'NOTHING',
    # From Parable
    'PARABLE', 'MASTER', 'DISCIPLE', 'BROTHER', 'PILGRIM', 'CIRCUMFERENCE',
    'BEGINNING', 'ENLIGHTEN', 'CONSUME', 'COMMAND', 'INSTRUCTION', 'BELIEVE',
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
    for dg in ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE', 'ED', 'ND', 'HA', 'AT', 'EN', 'EA', 'NG', 'OF']:
        score += text.count(dg) * 0.5
    return score

# =============================================================================
# DECRYPTION OPERATIONS
# =============================================================================

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

# =============================================================================
# INTENSIVE DOUBLE DECRYPTION SEARCH
# =============================================================================

def intensive_double_decrypt():
    """Test double decryption with finer granularity."""
    results = []
    ops = [
        ('sub', decrypt_sub),
        ('xor', decrypt_xor),
        ('add', decrypt_add),
    ]
    
    # Focus on best-scoring pages from previous runs
    priority_pages = [52, 48, 31, 28, 27, 30, 40, 29]
    
    print(f"\n  Testing {len(priority_pages)} priority pages with double decryption...")
    
    for page in priority_pages:
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        best_for_page = None
        
        for op1_name, op1 in ops:
            for op2_name, op2 in ops:
                # Use step of 5 for first layer, 3 for second
                for rot1 in range(0, 95, 5):
                    for off1 in range(0, 29, 3):
                        dec1 = op1(indices, rot1, off1)
                        
                        for rot2 in range(0, 95, 5):
                            for off2 in range(0, 29, 3):
                                dec2 = op2(dec1, rot2, off2)
                                text_out = indices_to_text(dec2)
                                score = score_text(text_out)
                                
                                if score >= 140:
                                    results.append({
                                        'page': page, 
                                        'method': f'double_{op1_name}_{op2_name}',
                                        'params': {'rot1': rot1, 'off1': off1, 'rot2': rot2, 'off2': off2},
                                        'score': score, 
                                        'text': text_out[:100]
                                    })
                                    if best_for_page is None or score > best_for_page:
                                        best_for_page = score
        
        if best_for_page:
            print(f"    Page {page}: best={best_for_page:.1f}")
    
    return results

def fine_tune_double_decrypt():
    """Fine-tune around the best double decryption results."""
    print("\n  Fine-tuning around best double decryption results...")
    
    # Best results from Phase 3
    best_combos = [
        {'page': 48, 'op1': 'xor', 'op2': 'sub', 'rot1': 60, 'off1': 5, 'rot2': 80, 'off2': 5},
        {'page': 31, 'op1': 'xor', 'op2': 'sub', 'rot1': 40, 'off1': 0, 'rot2': 20, 'off2': 20},
        {'page': 28, 'op1': 'add', 'op2': 'xor', 'rot1': 10, 'off1': 25, 'rot2': 90, 'off2': 10},
        {'page': 28, 'op1': 'xor', 'op2': 'xor', 'rot1': 80, 'off1': 5, 'rot2': 10, 'off2': 25},
        {'page': 27, 'op1': 'xor', 'op2': 'sub', 'rot1': 70, 'off1': 10, 'rot2': 80, 'off2': 10},
        {'page': 30, 'op1': 'add', 'op2': 'xor', 'rot1': 20, 'off1': 0, 'rot2': 60, 'off2': 25},
    ]
    
    ops_map = {'sub': decrypt_sub, 'xor': decrypt_xor, 'add': decrypt_add}
    results = []
    
    for combo in best_combos:
        page = combo['page']
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        op1 = ops_map[combo['op1']]
        op2 = ops_map[combo['op2']]
        
        # Search around the best parameters
        for rot1 in range(max(0, combo['rot1']-8), min(95, combo['rot1']+9)):
            for off1 in range(29):
                dec1 = op1(indices, rot1, off1)
                
                for rot2 in range(max(0, combo['rot2']-8), min(95, combo['rot2']+9)):
                    for off2 in range(29):
                        dec2 = op2(dec1, rot2, off2)
                        text_out = indices_to_text(dec2)
                        score = score_text(text_out)
                        
                        if score >= 140:
                            results.append({
                                'page': page,
                                'method': f'double_{combo["op1"]}_{combo["op2"]}_tuned',
                                'params': {'rot1': rot1, 'off1': off1, 'rot2': rot2, 'off2': off2},
                                'score': score,
                                'text': text_out[:100]
                            })
    
    return results

def test_triple_decrypt():
    """Test triple layer decryption."""
    print("\n  Testing triple layer decryption...")
    results = []
    ops = [('sub', decrypt_sub), ('xor', decrypt_xor), ('add', decrypt_add)]
    
    for page in [52, 48, 31, 28]:  # Focus on best pages
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        
        for op1_name, op1 in ops:
            for op2_name, op2 in ops:
                for op3_name, op3 in ops:
                    # Coarse search for triple decrypt
                    for rot1 in range(0, 95, 15):
                        for rot2 in range(0, 95, 15):
                            for rot3 in range(0, 95, 15):
                                for off1 in range(0, 29, 7):
                                    for off2 in range(0, 29, 7):
                                        for off3 in range(0, 29, 7):
                                            dec1 = op1(indices, rot1, off1)
                                            dec2 = op2(dec1, rot2, off2)
                                            dec3 = op3(dec2, rot3, off3)
                                            text_out = indices_to_text(dec3)
                                            score = score_text(text_out)
                                            
                                            if score >= 150:
                                                results.append({
                                                    'page': page,
                                                    'method': f'triple_{op1_name}_{op2_name}_{op3_name}',
                                                    'params': {
                                                        'rot1': rot1, 'off1': off1,
                                                        'rot2': rot2, 'off2': off2,
                                                        'rot3': rot3, 'off3': off3
                                                    },
                                                    'score': score,
                                                    'text': text_out[:100]
                                                })
    
    return results

def test_decrypt_transpose_decrypt():
    """Test decrypt -> transpose -> decrypt patterns."""
    print("\n  Testing decrypt -> transpose -> decrypt...")
    results = []
    
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
    
    ops = [('sub', decrypt_sub), ('xor', decrypt_xor)]
    
    for page in [52, 48, 31, 28, 29]:
        indices = unicode_to_indices(UNSOLVED_PAGES[page])
        page_len = len(indices)
        
        for op1_name, op1 in ops:
            for rot1 in range(0, 95, 10):
                for off1 in range(0, 29, 5):
                    dec1 = op1(indices, rot1, off1)
                    text1 = indices_to_text(dec1)
                    
                    for width in [7, 9, 10, 11, 12, 13, 14, 15, 17, 19, 23, 29]:
                        if width >= page_len:
                            continue
                        
                        transposed = columnar_transpose(text1, width)
                        trans_indices = [RUNE_TO_IDX[r] for r in transposed.split() if r in RUNE_TO_IDX]
                        if len(trans_indices) == 0:
                            # Handle multi-char runes
                            trans_indices = []
                            i = 0
                            while i < len(transposed):
                                if i + 1 < len(transposed) and transposed[i:i+2] in RUNE_TO_IDX:
                                    trans_indices.append(RUNE_TO_IDX[transposed[i:i+2]])
                                    i += 2
                                elif transposed[i] in RUNE_TO_IDX:
                                    trans_indices.append(RUNE_TO_IDX[transposed[i]])
                                    i += 1
                                else:
                                    i += 1
                        
                        if len(trans_indices) < 10:
                            # Direct string processing
                            for op2_name, op2 in ops:
                                for rot2 in range(0, 95, 10):
                                    for off2 in range(0, 29, 5):
                                        # Re-decrypt the transposed text
                                        text2 = transposed
                                        score = score_text(text2)
                                        if score >= 130:
                                            results.append({
                                                'page': page,
                                                'method': f'{op1_name}_transpose_{width}',
                                                'params': {'rot1': rot1, 'off1': off1, 'width': width},
                                                'score': score,
                                                'text': text2[:100]
                                            })
    
    return results

def test_reverse_operations():
    """Test reverse key and reverse text combinations."""
    print("\n  Testing reverse operations...")
    results = []
    
    reversed_key = MASTER_KEY[::-1]
    
    for page, text in UNSOLVED_PAGES.items():
        indices = unicode_to_indices(text)
        
        # Test with reversed key
        for rot in range(0, 95, 3):
            for off in range(29):
                dec = []
                for i, idx in enumerate(indices):
                    key_val = reversed_key[(i + rot) % 95]
                    plain_idx = (idx - key_val - off) % NUM_RUNES
                    dec.append(plain_idx)
                
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                if score >= 120:
                    results.append({
                        'page': page, 'method': 'reversed_key',
                        'params': {'rot': rot, 'off': off},
                        'score': score, 'text': text_out[:100]
                    })
        
        # Test with reversed indices then decrypt
        rev_indices = indices[::-1]
        for rot in range(0, 95, 3):
            for off in range(29):
                dec = decrypt_sub(rev_indices, rot, off)
                text_out = indices_to_text(dec)
                score = score_text(text_out)
                if score >= 120:
                    results.append({
                        'page': page, 'method': 'reversed_text_then_sub',
                        'params': {'rot': rot, 'off': off},
                        'score': score, 'text': text_out[:100]
                    })
    
    return results

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔥 MULTI-LAYER DEEP ANALYSIS")
    print("=" * 80)
    
    all_results = []
    
    # Phase 1: Intensive double decrypt (finer granularity)
    print("\n📊 Phase 1: Intensive double decryption...")
    start = time.time()
    results = intensive_double_decrypt()
    all_results.extend(results)
    print(f"  → Found {len(results)} results (score >= 140) [{time.time()-start:.1f}s]")
    
    # Phase 2: Fine-tune around best double decrypts
    print("\n📊 Phase 2: Fine-tuning best double decrypts...")
    start = time.time()
    results = fine_tune_double_decrypt()
    all_results.extend(results)
    print(f"  → Found {len(results)} results [{time.time()-start:.1f}s]")
    
    # Phase 3: Triple decryption
    print("\n📊 Phase 3: Triple layer decryption...")
    start = time.time()
    results = test_triple_decrypt()
    all_results.extend(results)
    print(f"  → Found {len(results)} results [{time.time()-start:.1f}s]")
    
    # Phase 4: Reverse operations
    print("\n📊 Phase 4: Reverse key/text operations...")
    start = time.time()
    results = test_reverse_operations()
    all_results.extend(results)
    print(f"  → Found {len(results)} results [{time.time()-start:.1f}s]")
    
    # Sort and display
    all_results.sort(key=lambda x: -x['score'])
    
    print("\n" + "=" * 80)
    print("🏆 TOP 30 HIGHEST-SCORING RESULTS")
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
    with open('c:/Users/tyler/Repos/Cicada3301/tools/multi_layer_results.json', 'w') as f:
        json.dump(all_results[:500], f, indent=2)
    
    print(f"\n💾 Saved {len(all_results)} total results")
    
    # Summary stats
    print("\n" + "=" * 80)
    print("📈 SCORE DISTRIBUTION")
    print("=" * 80)
    score_ranges = [(150, float('inf')), (145, 150), (140, 145), (135, 140), (130, 135)]
    for low, high in score_ranges:
        count = sum(1 for r in all_results if low <= r['score'] < high)
        if count > 0:
            print(f"  {low}+ : {count} results")
    
    print("\n🎯 MULTI-LAYER ANALYSIS COMPLETE")

if __name__ == '__main__':
    main()

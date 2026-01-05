#!/usr/bin/env python3
"""
DEEP DIVE ON BEST RESULTS
==========================

Focus on the most promising findings:
1. Columnar transposition with width 29 (score 137!)
2. GCD-based formula (score 117!)
3. 311-mod formula (scores 104+)
4. Latin text detection

Also test:
- Different prime widths for columnar transposition
- Combinations of decryption + transposition
- Row-by-row reading vs column-by-column
"""

import numpy as np
from pathlib import Path
import re
from collections import Counter
import math

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                       20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                       17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                       5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                       14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)

ENGLISH_WORDS = {
    'THE', 'OF', 'AND', 'A', 'TO', 'IN', 'IS', 'IT', 'YOU', 'THAT', 
    'HE', 'WAS', 'FOR', 'ON', 'ARE', 'AS', 'WITH', 'HIS', 'THEY', 
    'I', 'AT', 'BE', 'THIS', 'HAVE', 'FROM', 'OR', 'ONE', 'HAD', 
    'BY', 'NOT', 'BUT', 'WHAT', 'ALL', 'WERE', 'WE', 'WHEN', 'YOUR',
    'WILL', 'UP', 'OTHER', 'ABOUT', 'OUT', 'MANY', 'THEN', 'THEM',
    'WISDOM', 'TRUTH', 'DIVINE', 'DIVINITY', 'SOUL', 'MIND', 'LIGHT',
    'DARKNESS', 'PATH', 'KNOWLEDGE', 'ENLIGHTEN', 'EMERGE', 'PRIME',
    'CIRCUMFERENCE', 'INSTAR', 'PARABLE', 'BEING', 'BECOMING', 'SELF'
}

LATIN_WORDS = {
    'ET', 'IN', 'EST', 'NON', 'QUI', 'AD', 'UT', 'CUM', 'SED', 'EX',
    'AB', 'DE', 'PER', 'SI', 'NE', 'PRO', 'SUB', 'DUM', 'AC', 'ATQUE',
    'QUOD', 'QUAE', 'QUID', 'HIC', 'HAEC', 'HOC', 'ILLE', 'ILLA', 'ILLUD',
    'OMNIS', 'SUM', 'ESSE', 'FUIT', 'SUNT', 'ERAT', 'ERIT',
    'DEUS', 'DEI', 'DEO', 'LUX', 'LUCIS', 'VIA', 'VIAM', 'VITA', 'VITAE',
    'VERITAS', 'AMOR', 'MORS', 'HOMO', 'ANIMA', 'SPIRITUS', 'CORPUS', 
    'TERRA', 'CAELUM', 'IGNIS', 'AQUA', 'AER', 'MUNDUS', 'SOL', 'LUNA',
    'LIBER', 'PRIMUS', 'UNUS', 'DUO', 'TRES', 'NIHIL', 'OMNIA', 'PARS'
}

def runes_to_indices(runes):
    return np.array([RUNE_TO_IDX[r] for r in runes if r in RUNE_TO_IDX], dtype=np.int32)

def indices_to_text(indices):
    return ''.join(IDX_TO_LETTER[i % 29] for i in indices)

def extend_key(key, length):
    return np.tile(key, (length // len(key) + 1))[:length]

def load_all_pages():
    data_file = Path(r"C:\Users\tyler\Repos\Cicada3301\EXTRA WIKI PAGES\Liber Primus Ideas and Suggestions\RuneSolver.py")
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pages = {}
    pattern = r'Page(\d+)\s*=\s*["\']([^"\']*)["\']'
    for match in re.finditer(pattern, content):
        page_num = int(match.group(1))
        page_text = match.group(2)
        runes_only = ''.join(c for c in page_text if c in RUNE_TO_IDX)
        if runes_only:
            pages[page_num] = runes_to_indices(runes_only)
    return pages

def score_text(text):
    eng = sum(text.upper().count(w) for w in ENGLISH_WORDS)
    lat = sum(text.upper().count(w) for w in LATIN_WORDS)
    return eng + lat * 1.5

def columnar_transpose(text, width):
    """Columnar transposition - read by columns."""
    cols = ['' for _ in range(width)]
    for i, c in enumerate(text):
        cols[i % width] += c
    return ''.join(cols)

def columnar_untranspose(text, width):
    """Reverse columnar transposition - undo the column read."""
    rows = len(text) // width + (1 if len(text) % width else 0)
    full_cols = len(text) % width if len(text) % width else width
    
    result = [''] * len(text)
    pos = 0
    for col in range(width):
        col_len = rows if col < full_cols else rows - 1
        for row in range(col_len):
            idx = row * width + col
            if idx < len(text):
                result[idx] = text[pos]
                pos += 1
    return ''.join(result)

def test_decrypt_then_transpose(pages):
    """Test decryption followed by transposition."""
    print("\n" + "="*80)
    print("🔄 DECRYPT THEN TRANSPOSE")
    print("="*80)
    
    results = []
    
    # Best decryption configs
    decrypt_configs = [
        (47, 18, 'sub', "rot=page, off=page"),
        (30, 1, 'sub', "rot=page+1, off=page+1"),
        (52, 23, 'sub', "rot=page, off=page"),
        (67, 28, 'xor', "rot=95-page, off=page"),  # For page 28
        (1, 1, 'xor', "gcd-based"),  # General gcd formula
    ]
    
    # Prime widths to test
    widths = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        for rot, off, op, desc in decrypt_configs:
            # Adjust rot/off based on description
            if "page" in desc:
                actual_rot = pg_num % 95 if "rot=page" in desc else (pg_num + 1) % 95
                actual_off = pg_num % 29 if "off=page" in desc else (pg_num + 1) % 29
                if "95-page" in desc:
                    actual_rot = (95 - pg_num) % 95
            elif "gcd" in desc:
                actual_rot = math.gcd(pg_num, 95) if pg_num > 0 else 1
                actual_off = math.gcd(pg_num, 29) if pg_num > 0 else 1
            else:
                actual_rot = rot
                actual_off = off
            
            rotated = np.roll(MASTER_KEY, actual_rot)
            key = (rotated + actual_off) % 29
            extended = extend_key(key, len(pg_idx))
            
            if op == 'xor':
                decrypted = (pg_idx ^ extended) % 29
            else:
                decrypted = (pg_idx - extended) % 29
            
            text = indices_to_text(decrypted)
            
            # Test various transposition widths
            for width in widths:
                if width >= len(text):
                    continue
                
                transposed = columnar_transpose(text, width)
                score = score_text(transposed)
                
                if score >= 100:
                    results.append((pg_num, desc, op, actual_rot, actual_off, width, score, transposed[:80]))
                    print(f"  ⭐ Page {pg_num}: {desc}, {op}, width={width} -> score={score:.1f}")
                    print(f"       {transposed[:60]}...")
                
                # Also test un-transpose (reverse)
                untransposed = columnar_untranspose(text, width)
                score2 = score_text(untransposed)
                
                if score2 >= 100:
                    results.append((pg_num, desc + "_reverse", op, actual_rot, actual_off, width, score2, untransposed[:80]))
                    print(f"  ⭐ Page {pg_num}: {desc} REVERSE, {op}, width={width} -> score={score2:.1f}")
                    print(f"       {untransposed[:60]}...")
    
    return results

def test_transpose_then_decrypt(pages):
    """Test transposition of ciphertext, THEN decryption."""
    print("\n" + "="*80)
    print("🔀 TRANSPOSE THEN DECRYPT")
    print("="*80)
    
    results = []
    widths = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        for width in widths:
            if width >= len(pg_idx):
                continue
            
            # Transpose the indices first
            transposed_idx = np.zeros_like(pg_idx)
            cols = [[] for _ in range(width)]
            for i, idx in enumerate(pg_idx):
                cols[i % width].append(idx)
            
            pos = 0
            for col in cols:
                for val in col:
                    if pos < len(transposed_idx):
                        transposed_idx[pos] = val
                        pos += 1
            
            # Now decrypt
            for rot in range(0, 95, 10):  # Sample rotations
                for off in range(0, 29, 5):  # Sample offsets
                    rotated = np.roll(MASTER_KEY, rot)
                    key = (rotated + off) % 29
                    extended = extend_key(key, len(transposed_idx))
                    
                    for op in ['sub', 'xor']:
                        if op == 'xor':
                            decrypted = (transposed_idx ^ extended) % 29
                        else:
                            decrypted = (transposed_idx - extended) % 29
                        
                        text = indices_to_text(decrypted)
                        score = score_text(text)
                        
                        if score >= 90:
                            results.append((pg_num, width, rot, off, op, score, text[:60]))
                            print(f"  Page {pg_num}: width={width}, rot={rot}, off={off}, {op} -> {score:.1f}")
                            print(f"       {text[:50]}...")
    
    return results

def test_311_pattern(pages):
    """Deep dive on the 311-mod pattern that worked well."""
    print("\n" + "="*80)
    print("📊 311-MOD PATTERN ANALYSIS")
    print("="*80)
    
    results = []
    
    # 311 is special: 3*11 + 3*1 + 1 = 37, or maybe 3+1+1 = 5
    # Also 311 mod 29 = 21 (311 = 10*29 + 21)
    # And 311 mod 95 = 26 (311 = 3*95 + 26)
    
    print("311 mod 29 = 21")
    print("311 mod 95 = 26")
    print("1033 mod 29 = 17 (1033 = 35*29 + 18)")
    print("1033 mod 95 = 83 (1033 = 10*95 + 83)")
    print("3301 mod 29 = 24 (3301 = 113*29 + 24)")
    print("3301 mod 95 = 71 (3301 = 34*95 + 71)")
    print()
    
    # Test 311-based formulas more comprehensively
    formulas = [
        ("page*311 mod 95, page*311 mod 29", lambda p: ((p*311) % 95, (p*311) % 29)),
        ("311*page mod 95, page mod 29", lambda p: ((311*p) % 95, p % 29)),
        ("page+311 mod 95, page+311 mod 29", lambda p: ((p+311) % 95, (p+311) % 29)),
        ("311-page mod 95, 311-page mod 29", lambda p: ((311-p) % 95, (311-p) % 29)),
        ("page mod 31, page mod 11", lambda p: (p % 31, p % 11)),  # 31 and 11 from 311
        ("page*31 mod 95, page*11 mod 29", lambda p: ((p*31) % 95, (p*11) % 29)),
        ("(page+3)*(page+11) mod 95, page mod 29", lambda p: (((p+3)*(p+11)) % 95, p % 29)),
    ]
    
    for formula_name, formula_fn in formulas:
        print(f"\nFormula: {formula_name}")
        
        for pg_num, pg_idx in sorted(pages.items()):
            if pg_num in [0, 54, 56, 57]:
                continue
            
            try:
                rot, off = formula_fn(pg_num)
            except:
                continue
            
            rotated = np.roll(MASTER_KEY, rot)
            key = (rotated + off) % 29
            extended = extend_key(key, len(pg_idx))
            
            for op in ['sub', 'xor']:
                if op == 'xor':
                    decrypted = (pg_idx ^ extended) % 29
                else:
                    decrypted = (pg_idx - extended) % 29
                
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score >= 80:
                    results.append((pg_num, formula_name, op, rot, off, score, text[:60]))
                    
                    # Find Latin words
                    latin_found = [w for w in LATIN_WORDS if w in text.upper()]
                    eng_found = [w for w in ENGLISH_WORDS if w in text.upper() and len(w) >= 4]
                    
                    print(f"  Page {pg_num}: {op}, rot={rot}, off={off} -> {score:.1f}")
                    if latin_found:
                        print(f"    Latin: {latin_found[:5]}")
                    if eng_found:
                        print(f"    English: {eng_found[:5]}")
    
    return results

def test_interleaved_keys(pages):
    """Test if keys are interleaved or alternating."""
    print("\n" + "="*80)
    print("🔀 INTERLEAVED KEY TESTING")
    print("="*80)
    
    results = []
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Test: Odd positions use one key, even use another
        for rot1 in range(0, 95, 15):
            for rot2 in range(0, 95, 15):
                key1 = np.roll(MASTER_KEY, rot1)
                key2 = np.roll(MASTER_KEY, rot2)
                
                extended1 = extend_key(key1, len(pg_idx))
                extended2 = extend_key(key2, len(pg_idx))
                
                # Interleave: even positions use key1, odd use key2
                interleaved = np.where(np.arange(len(pg_idx)) % 2 == 0, extended1, extended2)
                
                decrypted = (pg_idx - interleaved) % 29
                text = indices_to_text(decrypted)
                score = score_text(text)
                
                if score >= 80:
                    results.append((pg_num, "interleaved", rot1, rot2, score, text[:60]))
                    print(f"  Page {pg_num}: rot1={rot1}, rot2={rot2} -> {score:.1f}")
                    print(f"       {text[:50]}...")
    
    return results

def main():
    pages = load_all_pages()
    
    print("="*80)
    print("🎯 DEEP DIVE ON BEST RESULTS")
    print("="*80)
    print(f"Analyzing {len(pages)} pages")
    
    all_results = {}
    
    # Run focused tests
    all_results['decrypt_transpose'] = test_decrypt_then_transpose(pages)
    all_results['transpose_decrypt'] = test_transpose_then_decrypt(pages)
    all_results['311_pattern'] = test_311_pattern(pages)
    all_results['interleaved'] = test_interleaved_keys(pages)
    
    # Summary
    print("\n" + "="*80)
    print("📋 DEEP DIVE SUMMARY")
    print("="*80)
    
    total = sum(len(v) for v in all_results.values())
    print(f"\nTotal high-scoring results: {total}")
    
    for name, results in all_results.items():
        print(f"  {name}: {len(results)} results")

if __name__ == "__main__":
    main()

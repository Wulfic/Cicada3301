#!/usr/bin/env python3
"""
COMPREHENSIVE CIPHER TESTING SUITE
===================================

Testing ALL possibilities:
1. Prime number formulas (3301, 1033, 311, 31, etc.)
2. Latin text detection
3. Transposition ciphers
4. Letter frequency analysis
5. Word boundary detection
6. Combined operations
7. Out-of-the-box approaches

Cicada 3301's favorite primes: 3301, 1033, 311, 31, 3, 11, 7
"""

import numpy as np
from pathlib import Path
import re
from collections import Counter
from itertools import permutations, combinations
import math

# ============== CONSTANTS ==============

RUNES = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
           'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 
           'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Gematria Primus values (consecutive primes)
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

MASTER_KEY = np.array([11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
                       20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
                       17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
                       5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
                       14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23], dtype=np.int32)

# Cicada's favorite primes
CICADA_PRIMES = [3, 7, 11, 13, 17, 29, 31, 41, 59, 311, 1033, 3301]

# ============== HELPER FUNCTIONS ==============

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

# ============== SCORING FUNCTIONS ==============

# English common words
ENGLISH_WORDS = {
    'THE', 'OF', 'AND', 'A', 'TO', 'IN', 'IS', 'IT', 'YOU', 'THAT', 
    'HE', 'WAS', 'FOR', 'ON', 'ARE', 'AS', 'WITH', 'HIS', 'THEY', 
    'I', 'AT', 'BE', 'THIS', 'HAVE', 'FROM', 'OR', 'ONE', 'HAD', 
    'BY', 'NOT', 'BUT', 'WHAT', 'ALL', 'WERE', 'WE', 'WHEN', 'YOUR',
    'CAN', 'SAID', 'EACH', 'WHICH', 'SHE', 'DO', 'HOW', 'THEIR',
    'WILL', 'UP', 'OTHER', 'ABOUT', 'OUT', 'MANY', 'THEN', 'THEM',
    'THESE', 'SO', 'SOME', 'HER', 'WOULD', 'MAKE', 'LIKE', 'INTO',
    'HIM', 'TIME', 'HAS', 'LOOK', 'TWO', 'MORE', 'GO', 'SEE', 'NO',
    'WAY', 'COULD', 'PEOPLE', 'MY', 'THAN', 'FIRST', 'BEEN', 'CALL',
    # Philosophical/Cicada words
    'WISDOM', 'TRUTH', 'DIVINE', 'DIVINITY', 'SOUL', 'MIND', 'LIGHT',
    'DARKNESS', 'PATH', 'KNOWLEDGE', 'ENLIGHTEN', 'EMERGE', 'PRIME',
    'CIRCUMFERENCE', 'INSTAR', 'PARABLE', 'BEING', 'BECOMING', 'SELF',
    'WITHIN', 'WITHOUT', 'SEEK', 'FIND', 'KNOW', 'UNDERSTAND'
}

# Latin common words (Cicada uses Latin!)
LATIN_WORDS = {
    'ET', 'IN', 'EST', 'NON', 'QUI', 'AD', 'UT', 'CUM', 'SED', 'EX',
    'AB', 'DE', 'PER', 'SI', 'NE', 'PRO', 'SUB', 'DUM', 'AC', 'ATQUE',
    'QUOD', 'QUAE', 'QUID', 'HIC', 'HAEC', 'HOC', 'ILLE', 'ILLA', 'ILLUD',
    'OMNIS', 'OMNIBUS', 'SUM', 'ESSE', 'FUIT', 'SUNT', 'ERAT', 'ERIT',
    'DEUS', 'DEI', 'DEO', 'LUX', 'LUCIS', 'VIA', 'VIAM', 'VITA', 'VITAE',
    'VERITAS', 'VERITATIS', 'AMOR', 'AMORIS', 'MORS', 'MORTIS',
    'HOMO', 'HOMINIS', 'ANIMA', 'ANIMAE', 'SPIRITUS', 'CORPUS', 
    'TERRA', 'CAELUM', 'IGNIS', 'AQUA', 'AER', 'MUNDUS', 'ORBIS',
    'TEMPUS', 'LOCUS', 'DIES', 'NOX', 'NOCTIS', 'SOL', 'LUNA',
    'LIBER', 'LIBRI', 'PRIMUS', 'SECUNDUS', 'TERTIUS', 'QUARTUS',
    'UNUS', 'DUO', 'TRES', 'QUATTUOR', 'QUINQUE', 'SEX', 'SEPTEM',
    'OCTO', 'NOVEM', 'DECEM', 'CENTUM', 'MILLE',
    'BONUS', 'MALUS', 'MAGNUS', 'PARVUS', 'NOVUS', 'VETUS',
    'VERUS', 'FALSUS', 'SANCTUS', 'SACER', 'DIVINUS',
    'COGITO', 'ERGO', 'AGO', 'FACIO', 'VIDEO', 'AUDIO', 'SCIO',
    'CREDO', 'SPERO', 'AMO', 'VIVO', 'MORIOR', 'VENIO', 'VADO',
    'NIHIL', 'NEMO', 'OMNIA', 'TOTUM', 'PARS', 'INITIUM', 'FINIS'
}

def score_english(text):
    count = 0
    text_upper = text.upper()
    for word in ENGLISH_WORDS:
        count += text_upper.count(word)
    return count

def score_latin(text):
    count = 0
    text_upper = text.upper()
    for word in LATIN_WORDS:
        count += text_upper.count(word)
    return count

def score_combined(text):
    return score_english(text) + score_latin(text) * 1.5  # Weight Latin slightly higher

# English letter frequency (approx %)
ENGLISH_FREQ = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 
                'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
                'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
                'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
                'Q': 0.10, 'Z': 0.07}

# Latin letter frequency (approx %)
LATIN_FREQ = {'I': 11.3, 'E': 10.5, 'A': 8.9, 'U': 8.4, 'T': 7.5, 'S': 7.1,
              'N': 6.4, 'R': 6.2, 'O': 5.2, 'M': 4.8, 'C': 4.0, 'L': 3.0,
              'P': 2.9, 'D': 2.5, 'B': 1.5, 'Q': 1.3, 'V': 1.0, 'G': 0.9,
              'F': 0.8, 'H': 0.5, 'X': 0.4}

def analyze_frequency(text):
    """Analyze letter frequency and compare to English/Latin."""
    # Expand digraphs
    expanded = text.replace('TH', 'T').replace('NG', 'N').replace('EO', 'E').replace('OE', 'O')
    expanded = expanded.replace('AE', 'A').replace('IA', 'I').replace('EA', 'E')
    
    letter_counts = Counter(expanded.upper())
    total = sum(letter_counts.values())
    
    if total == 0:
        return 0, 0
    
    # Calculate chi-squared against English and Latin
    english_chi = 0
    latin_chi = 0
    
    for letter, exp_eng in ENGLISH_FREQ.items():
        observed = (letter_counts.get(letter, 0) / total) * 100
        english_chi += ((observed - exp_eng) ** 2) / (exp_eng + 0.1)
    
    for letter, exp_lat in LATIN_FREQ.items():
        observed = (letter_counts.get(letter, 0) / total) * 100
        latin_chi += ((observed - exp_lat) ** 2) / (exp_lat + 0.1)
    
    return english_chi, latin_chi

# ============== PRIME NUMBER TESTS ==============

def test_prime_formulas(pages):
    """Test formulas based on Cicada's favorite primes."""
    print("\n" + "="*80)
    print("🔢 PRIME NUMBER FORMULA TESTING")
    print("="*80)
    
    results = []
    
    # Test with different prime-based formulas
    prime_formulas = [
        ("rot=3301 mod 95, off=3301 mod 29", lambda p: (3301 % 95, 3301 % 29)),
        ("rot=1033 mod 95, off=1033 mod 29", lambda p: (1033 % 95, 1033 % 29)),
        ("rot=page*3301 mod 95, off=page mod 29", lambda p: ((p * 3301) % 95, p % 29)),
        ("rot=page*1033 mod 95, off=page mod 29", lambda p: ((p * 1033) % 95, p % 29)),
        ("rot=page+3301 mod 95, off=page+3301 mod 29", lambda p: ((p + 3301) % 95, (p + 3301) % 29)),
        ("rot=3301-page mod 95, off=1033 mod 29", lambda p: ((3301 - p) % 95, 1033 % 29)),
        ("rot=page*31 mod 95, off=page*31 mod 29", lambda p: ((p * 31) % 95, (p * 31) % 29)),
        ("rot=page*311 mod 95, off=page*311 mod 29", lambda p: ((p * 311) % 95, (p * 311) % 29)),
        ("rot=page mod 31, off=page mod 29", lambda p: (p % 31, p % 29)),
        ("rot=page^2 mod 95, off=page^2 mod 29", lambda p: ((p*p) % 95, (p*p) % 29)),
        ("rot=gcd(page,95), off=gcd(page,29)", lambda p: (math.gcd(p, 95), math.gcd(p, 29) if p > 0 else 0)),
        # Fibonacci-prime combos
        ("rot=fib(page mod 10) mod 95, off=prime(page mod 10) mod 29", 
         lambda p: ([1,1,2,3,5,8,13,21,34,55][p % 10] % 95, [2,3,5,7,11,13,17,19,23,29][p % 10] % 29)),
    ]
    
    for formula_name, formula_fn in prime_formulas:
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
            
            for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                                ('xor', lambda x, k: (x ^ k) % 29)]:
                decrypted = op(pg_idx, extended)
                text = indices_to_text(decrypted)
                
                eng_score = score_english(text)
                lat_score = score_latin(text)
                total_score = eng_score + lat_score * 1.5
                
                if total_score >= 50:
                    results.append((pg_num, formula_name, op_name, rot, off, eng_score, lat_score, total_score, text[:60]))
    
    # Sort by total score
    results.sort(key=lambda x: -x[7])
    
    print(f"\nTop results (English + Latin scoring):")
    for pg, formula, op, rot, off, eng, lat, total, text in results[:20]:
        print(f"  Page {pg}: {formula[:40]}, {op}")
        print(f"    rot={rot}, off={off}, Eng={eng}, Lat={lat}, Total={total:.1f}")
        print(f"    Text: {text}...")
        print()
    
    return results

# ============== LATIN TEXT DETECTION ==============

def test_latin_detection(pages):
    """Test if any decryptions contain Latin text."""
    print("\n" + "="*80)
    print("🏛️ LATIN TEXT DETECTION")
    print("="*80)
    
    best_latin = []
    
    # Test various configurations
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Test many rotation/offset combinations
        for rot in range(0, 95, 5):  # Sample every 5th rotation
            for off in range(29):
                rotated = np.roll(MASTER_KEY, rot)
                key = (rotated + off) % 29
                extended = extend_key(key, len(pg_idx))
                
                for op_name, op in [('sub', lambda x, k: (x - k) % 29), 
                                    ('xor', lambda x, k: (x ^ k) % 29)]:
                    decrypted = op(pg_idx, extended)
                    text = indices_to_text(decrypted)
                    
                    lat_score = score_latin(text)
                    if lat_score >= 10:
                        best_latin.append((pg_num, op_name, rot, off, lat_score, text[:80]))
    
    best_latin.sort(key=lambda x: -x[4])
    
    print(f"\nTop Latin-scoring results:")
    for pg, op, rot, off, score, text in best_latin[:15]:
        print(f"  Page {pg}: {op}, rot={rot}, off={off}, Latin score={score}")
        print(f"    Text: {text}...")
        
        # Highlight any Latin words found
        latin_found = [w for w in LATIN_WORDS if w in text.upper()]
        if latin_found:
            print(f"    Latin words: {latin_found[:10]}")
        print()
    
    return best_latin

# ============== TRANSPOSITION TESTS ==============

def test_transpositions(pages):
    """Test various transposition ciphers on best decryptions."""
    print("\n" + "="*80)
    print("🔀 TRANSPOSITION CIPHER TESTING")
    print("="*80)
    
    # Best decryptions from previous testing
    best_configs = [
        (47, 47, 18, 'sub'),
        (29, 30, 1, 'sub'),
        (28, 67, 28, 'xor'),
        (52, 52, 23, 'sub'),
    ]
    
    results = []
    
    for pg_num, rot, off, op in best_configs:
        pg_idx = pages[pg_num]
        
        rotated = np.roll(MASTER_KEY, rot)
        key = (rotated + off) % 29
        extended = extend_key(key, len(pg_idx))
        
        if op == 'xor':
            decrypted = (pg_idx ^ extended) % 29
        else:
            decrypted = (pg_idx - extended) % 29
        
        text = indices_to_text(decrypted)
        
        print(f"\nPage {pg_num} original: {text[:50]}...")
        
        # Test columnar transposition with various widths
        for width in CICADA_PRIMES[:8]:  # Try prime widths
            if width >= len(text):
                continue
            
            # Read by columns
            cols = ['' for _ in range(width)]
            for i, c in enumerate(text):
                cols[i % width] += c
            transposed = ''.join(cols)
            
            score = score_combined(transposed)
            if score > 30:
                results.append((pg_num, f"columnar-{width}", score, transposed[:60]))
                print(f"  Columnar width {width}: score={score}, {transposed[:40]}...")
        
        # Test rail fence with various rails
        for rails in [2, 3, 5, 7]:
            if rails >= len(text) // 2:
                continue
            
            # Rail fence decode
            fence = [[] for _ in range(rails)]
            rail = 0
            direction = 1
            for i in range(len(text)):
                fence[rail].append(i)
                rail += direction
                if rail == 0 or rail == rails - 1:
                    direction *= -1
            
            # Flatten and read
            positions = []
            for f in fence:
                positions.extend(f)
            
            transposed = ''.join(text[positions[i]] if i < len(positions) and positions[i] < len(text) else '' 
                                for i in range(len(text)))
            
            score = score_combined(transposed)
            if score > 30:
                results.append((pg_num, f"railfence-{rails}", score, transposed[:60]))
                print(f"  Rail fence {rails}: score={score}, {transposed[:40]}...")
        
        # Test every-nth-letter (skip cipher)
        for skip in [2, 3, 5, 7, 11]:
            for start in range(skip):
                extracted = text[start::skip]
                score = score_combined(extracted)
                if score > 20:
                    results.append((pg_num, f"skip-{skip}-start{start}", score, extracted[:60]))
                    print(f"  Skip {skip} start {start}: score={score}, {extracted[:40]}...")
        
        # Reverse
        reversed_text = text[::-1]
        score = score_combined(reversed_text)
        if score > 30:
            results.append((pg_num, "reversed", score, reversed_text[:60]))
            print(f"  Reversed: score={score}, {reversed_text[:40]}...")
    
    return results

# ============== FREQUENCY ANALYSIS ==============

def analyze_all_frequencies(pages):
    """Analyze letter frequencies for all decryptions."""
    print("\n" + "="*80)
    print("📊 LETTER FREQUENCY ANALYSIS")
    print("="*80)
    
    results = []
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        # Test key configurations
        configs = [
            (pg_num % 95, pg_num % 29, 'sub'),
            (pg_num % 95, pg_num % 29, 'xor'),
            ((pg_num + 1) % 95, (pg_num + 1) % 29, 'sub'),
        ]
        
        for rot, off, op in configs:
            rotated = np.roll(MASTER_KEY, rot)
            key = (rotated + off) % 29
            extended = extend_key(key, len(pg_idx))
            
            if op == 'xor':
                decrypted = (pg_idx ^ extended) % 29
            else:
                decrypted = (pg_idx - extended) % 29
            
            text = indices_to_text(decrypted)
            eng_chi, lat_chi = analyze_frequency(text)
            
            # Lower chi-squared = better match
            results.append((pg_num, rot, off, op, eng_chi, lat_chi, text[:40]))
    
    # Sort by lowest chi-squared (best match to English)
    results.sort(key=lambda x: x[4])
    
    print("\nBest matches to English letter frequency:")
    for pg, rot, off, op, eng_chi, lat_chi, text in results[:10]:
        print(f"  Page {pg}: rot={rot}, off={off}, {op}")
        print(f"    English χ²={eng_chi:.1f}, Latin χ²={lat_chi:.1f}")
        print(f"    Text: {text}...")
        print()
    
    # Sort by lowest Latin chi-squared
    results.sort(key=lambda x: x[5])
    
    print("\nBest matches to Latin letter frequency:")
    for pg, rot, off, op, eng_chi, lat_chi, text in results[:10]:
        print(f"  Page {pg}: rot={rot}, off={off}, {op}")
        print(f"    English χ²={eng_chi:.1f}, Latin χ²={lat_chi:.1f}")
        print(f"    Text: {text}...")
        print()
    
    return results

# ============== OUT-OF-THE-BOX TESTS ==============

def test_creative_approaches(pages):
    """Try creative, out-of-the-box approaches."""
    print("\n" + "="*80)
    print("💡 CREATIVE/OUT-OF-THE-BOX APPROACHES")
    print("="*80)
    
    results = []
    
    for pg_num, pg_idx in sorted(pages.items()):
        if pg_num in [0, 54, 56, 57]:
            continue
        
        print(f"\nPage {pg_num}:")
        
        # 1. Use Gematria values directly
        print("  Testing Gematria-based decryption...")
        gematria_key = np.array([GEMATRIA[i] % 29 for i in MASTER_KEY], dtype=np.int32)
        extended = extend_key(gematria_key, len(pg_idx))
        decrypted = (pg_idx - extended) % 29
        text = indices_to_text(decrypted)
        score = score_combined(text)
        if score > 30:
            print(f"    Gematria key: score={score}, {text[:50]}...")
            results.append((pg_num, "gematria_key", score, text))
        
        # 2. XOR with page content itself (autokey variant)
        print("  Testing self-XOR...")
        if len(pg_idx) > 95:
            key = pg_idx[:95]
            extended = extend_key(key, len(pg_idx))
            decrypted = (pg_idx ^ extended) % 29
            text = indices_to_text(decrypted)
            score = score_combined(text)
            if score > 30:
                print(f"    Self-XOR: score={score}, {text[:50]}...")
                results.append((pg_num, "self_xor", score, text))
        
        # 3. Key based on page length
        print("  Testing length-based key...")
        length = len(pg_idx)
        rot = length % 95
        off = length % 29
        rotated = np.roll(MASTER_KEY, rot)
        key = (rotated + off) % 29
        extended = extend_key(key, length)
        decrypted = (pg_idx - extended) % 29
        text = indices_to_text(decrypted)
        score = score_combined(text)
        if score > 40:
            print(f"    Length-based (rot={rot}, off={off}): score={score}, {text[:50]}...")
            results.append((pg_num, f"length_based_r{rot}_o{off}", score, text))
        
        # 4. Modular arithmetic with 3301
        print("  Testing 3301-modular...")
        for divisor in [3301, 1033, 311]:
            rot = (pg_num * divisor) % 95
            off = (pg_num * divisor) % 29
            rotated = np.roll(MASTER_KEY, rot)
            key = (rotated + off) % 29
            extended = extend_key(key, len(pg_idx))
            
            for op in ['sub', 'xor']:
                if op == 'xor':
                    decrypted = (pg_idx ^ extended) % 29
                else:
                    decrypted = (pg_idx - extended) % 29
                
                text = indices_to_text(decrypted)
                score = score_combined(text)
                if score > 50:
                    print(f"    {divisor}-mod ({op}): score={score}, {text[:50]}...")
                    results.append((pg_num, f"{divisor}_mod_{op}", score, text))
        
        # 5. Double encryption (apply key twice)
        print("  Testing double encryption...")
        extended = extend_key(MASTER_KEY, len(pg_idx))
        first = (pg_idx - extended) % 29
        decrypted = (first - extended) % 29
        text = indices_to_text(decrypted)
        score = score_combined(text)
        if score > 30:
            print(f"    Double sub: score={score}, {text[:50]}...")
            results.append((pg_num, "double_sub", score, text))
        
        # 6. Sum of indices as key position
        print("  Testing sum-based offset...")
        idx_sum = np.sum(pg_idx)
        rot = idx_sum % 95
        off = idx_sum % 29
        rotated = np.roll(MASTER_KEY, rot)
        key = (rotated + off) % 29
        extended = extend_key(key, len(pg_idx))
        decrypted = (pg_idx - extended) % 29
        text = indices_to_text(decrypted)
        score = score_combined(text)
        if score > 40:
            print(f"    Sum-based (sum={idx_sum}, rot={rot}, off={off}): score={score}, {text[:50]}...")
            results.append((pg_num, f"sum_based_r{rot}_o{off}", score, text))
    
    return results

# ============== MAIN ==============

def main():
    pages = load_all_pages()
    
    print("="*80)
    print("🔬 COMPREHENSIVE CIPHER TESTING SUITE")
    print("="*80)
    print(f"Loaded {len(pages)} pages")
    print(f"Testing with Cicada primes: {CICADA_PRIMES}")
    
    all_results = {}
    
    # Run all tests
    all_results['prime'] = test_prime_formulas(pages)
    all_results['latin'] = test_latin_detection(pages)
    all_results['transposition'] = test_transpositions(pages)
    all_results['frequency'] = analyze_all_frequencies(pages)
    all_results['creative'] = test_creative_approaches(pages)
    
    # Final summary
    print("\n" + "="*80)
    print("📋 FINAL SUMMARY")
    print("="*80)
    
    print(f"\nPrime formula tests: {len(all_results['prime'])} results with score >= 50")
    print(f"Latin detection: {len(all_results['latin'])} results with Latin score >= 10")
    print(f"Transposition tests: {len(all_results['transposition'])} promising results")
    print(f"Creative approaches: {len(all_results['creative'])} notable results")

if __name__ == "__main__":
    main()

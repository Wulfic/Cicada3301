"""
Page 20 - Comprehensive Attack Suite
=====================================
Uses multiprocessing to brute-force various cipher approaches.
Target: Find the correct transposition/key for both the 166-stream and full P20.
"""

import os
import sys
import itertools
import multiprocessing as mp
from collections import Counter
from functools import partial
import time

# Gematria Primus
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# Common English words for scoring
COMMON_WORDS = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
    'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY', 'OLD', 'SEE', 'WAY',
    'WHO', 'DID', 'GET', 'HIM', 'NOW', 'SAY', 'SHE', 'TOO', 'USE', 'HE', 'WE', 'SO',
    'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'SAID', 'EACH', 'WHICH',
    'THEIR', 'WILL', 'WOULD', 'THERE', 'WHAT', 'ABOUT', 'WHEN', 'MAKE', 'LIKE', 'TIME',
    'DEATH', 'DEAD', 'REAPER', 'AEON', 'LONE', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'KNOW',
    'PRIME', 'SACRED', 'DIVINE', 'WISDOM', 'PILGRIM', 'WITHIN', 'EMERGE', 'INSTAR',
    'CIRCUMFERENCE', 'DIVINITY', 'TOTIENT', 'ENCRYPT', 'DEOR', 'SONG', 'POEM',
    'DIAGONAL', 'MEAN', 'SUM', 'RATIO', 'LENGTH', 'NUMBER', 'RUNE', 'KEY',
}

# 166-rune stream
STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# P24 key
P24_KEY = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 
           15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 
           11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 
           22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 
           15, 13, 15]

def to_int_single(text):
    """Convert text to indices (single chars only)"""
    single_gp = {k: v for k, v in GP_MAP.items() if len(k) == 1}
    return [single_gp[c] for c in text if c in single_gp]

def to_str(nums):
    return "".join(INV_MAP[n % 29] for n in nums)

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def word_score(text):
    """Score text by number of common English words found"""
    score = 0
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) ** 2  # Weight longer words more
    return score

def load_p20():
    """Load P20 runes from file"""
    path = "LiberPrimus/pages/page_20/runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

# ============ TRANSPOSITION ATTACKS ============

def columnar_transpose(data, width):
    """Read data by columns after arranging in rows of given width"""
    if len(data) % width != 0:
        return None
    height = len(data) // width
    result = []
    for c in range(width):
        for r in range(height):
            result.append(data[r * width + c])
    return result

def rail_fence(data, rails):
    """Rail fence cipher decode"""
    if rails < 2 or rails >= len(data):
        return None
    
    fence = [[None] * len(data) for _ in range(rails)]
    rail = 0
    direction = 1
    
    for i in range(len(data)):
        fence[rail][i] = True
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    idx = 0
    for r in range(rails):
        for c in range(len(data)):
            if fence[r][c] and idx < len(data):
                fence[r][c] = data[idx]
                idx += 1
    
    result = []
    rail = 0
    direction = 1
    for i in range(len(data)):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    return result

def skip_read(data, skip, start=0):
    """Read every nth character"""
    return data[start::skip]

def diagonal_read(data, width, step=1):
    """Read diagonally with given step"""
    if len(data) % width != 0:
        return None
    height = len(data) // width
    result = []
    
    for start_c in range(width):
        r, c = 0, start_c
        while r < height:
            result.append(data[r * width + c])
            r += 1
            c = (c + step) % width
    
    return result

def permute_columns(data, width, perm):
    """Reorder columns by permutation"""
    if len(data) % width != 0 or len(perm) != width:
        return None
    height = len(data) // width
    result = []
    for r in range(height):
        for c in perm:
            result.append(data[r * width + c])
    return result

def test_transposition(args):
    """Test a single transposition configuration"""
    method, params, stream_ints = args
    
    try:
        if method == 'columnar':
            result = columnar_transpose(stream_ints, params)
        elif method == 'rail':
            result = rail_fence(stream_ints, params)
        elif method == 'skip':
            skip, start = params
            result = skip_read(stream_ints, skip, start)
        elif method == 'diagonal':
            width, step = params
            result = diagonal_read(stream_ints, width, step)
        else:
            return None
        
        if result is None or len(result) < 10:
            return None
        
        text = to_str(result)
        ioc = calc_ioc(result)
        wscore = word_score(text)
        
        if wscore > 50 or ioc > 2.0:  # Promising result
            return (method, params, ioc, wscore, text[:80])
    except:
        pass
    
    return None

# ============ VIGENERE KEY SEARCH ============

def vigenere_decrypt(cipher, key):
    """Vigenere decryption: P = C - K mod 29"""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        result.append((c - k) % 29)
    return result

def test_key(args):
    """Test a single key"""
    key, cipher = args
    
    decrypted = vigenere_decrypt(cipher, key)
    text = to_str(decrypted)
    ioc = calc_ioc(decrypted)
    wscore = word_score(text)
    
    if wscore > 100 or ioc > 1.5:
        return (key, ioc, wscore, text[:60])
    return None

def generate_keys(length, alphabet_size=29):
    """Generate random keys for testing"""
    import random
    while True:
        yield [random.randint(0, alphabet_size-1) for _ in range(length)]

# ============ MAIN ATTACK ============

def attack_166_transposition():
    """Comprehensive transposition attack on 166-stream"""
    print("="*60)
    print("ATTACK 1: Transposition on 166-rune stream")
    print("="*60)
    
    stream_ints = to_int_single(STREAM_166)
    n = len(stream_ints)
    print(f"Stream length: {n}")
    print(f"Base IoC: {calc_ioc(stream_ints):.4f}")
    
    # Generate all transposition configurations to test
    configs = []
    
    # Columnar transpositions
    for width in range(2, 84):
        if n % width == 0:
            configs.append(('columnar', width, stream_ints))
    
    # Rail fence
    for rails in range(2, 20):
        configs.append(('rail', rails, stream_ints))
    
    # Skip ciphers
    for skip in range(2, 30):
        for start in range(min(skip, 10)):
            configs.append(('skip', (skip, start), stream_ints))
    
    # Diagonal reads
    for width in [2, 7, 11, 14, 83]:
        if n % width == 0:
            for step in range(1, width):
                configs.append(('diagonal', (width, step), stream_ints))
    
    print(f"Testing {len(configs)} transposition configurations...")
    
    # Parallel execution
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(test_transposition, configs)
    
    # Filter and sort results
    valid_results = [r for r in results if r is not None]
    valid_results.sort(key=lambda x: (x[3], x[2]), reverse=True)  # Sort by word score, then IoC
    
    print(f"\nTop results (word score > 50 or IoC > 2.0):")
    for method, params, ioc, wscore, text in valid_results[:10]:
        print(f"  {method}({params}): IoC={ioc:.4f}, Words={wscore}, '{text[:50]}...'")
    
    return valid_results

def attack_p20_keys():
    """Key search on full P20"""
    print("\n" + "="*60)
    print("ATTACK 2: Key search on full P20")
    print("="*60)
    
    os.chdir(r"c:\Users\tyler\Repos\Cicada3301")
    p20 = load_p20()
    print(f"P20 length: {len(p20)} runes")
    print(f"Base IoC: {calc_ioc(p20):.4f}")
    
    # Test known keys and their variations
    known_keys = [
        ('P24_KEY', P24_KEY),
        ('P24_REV', P24_KEY[::-1]),
        ('DIVINITY', to_int_single('DIVINITY')),
        ('CIRCUMFERENCE', to_int_single('CIRCUMFERENCE')),
        ('FIRFUMFERENFE', to_int_single('FIRFUMFERENFE')),
        ('DEOR', to_int_single('DEOR')),
        ('YAHEOOPYJ', to_int_single('YAHEOOPYJ')),
        ('PRIMES', to_int_single('PRIMES')),
        ('DIAGONAL', to_int_single('DIAGONAL')),
    ]
    
    print("\nTesting known keys:")
    best_result = None
    
    for name, key in known_keys:
        if not key:
            continue
        
        # Try forward and reverse
        for direction in ['fwd', 'rev']:
            k = key if direction == 'fwd' else key[::-1]
            
            # Try different operations
            for op_name, op in [('sub', lambda c, k: (c-k)%29), 
                                ('add', lambda c, k: (c+k)%29),
                                ('beaufort', lambda c, k: (k-c)%29)]:
                decrypted = [op(c, k[i % len(k)]) for i, c in enumerate(p20)]
                ioc = calc_ioc(decrypted)
                text = to_str(decrypted)
                wscore = word_score(text)
                
                if ioc > 1.3 or wscore > 50:
                    print(f"  {name}_{direction}_{op_name}: IoC={ioc:.4f}, Words={wscore}")
                    print(f"    '{text[:60]}...'")
                
                if best_result is None or wscore > best_result[2]:
                    best_result = (f"{name}_{direction}_{op_name}", ioc, wscore, text)
    
    # Random key search
    print("\nRandom key search (10000 keys per length)...")
    
    for key_len in [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]:
        best_for_len = None
        
        for _ in range(10000):
            key = [__import__('random').randint(0, 28) for _ in range(key_len)]
            decrypted = vigenere_decrypt(p20, key)
            ioc = calc_ioc(decrypted)
            
            if ioc > 1.4:
                text = to_str(decrypted)
                wscore = word_score(text)
                if best_for_len is None or ioc > best_for_len[0]:
                    best_for_len = (ioc, wscore, key, text[:50])
        
        if best_for_len and best_for_len[0] > 1.3:
            print(f"  Len {key_len}: Best IoC={best_for_len[0]:.4f}, Words={best_for_len[1]}")
    
    return best_result

def attack_diagonal_grid():
    """Systematic diagonal reading of P20 28x29 grid"""
    print("\n" + "="*60)
    print("ATTACK 3: Diagonal grid reading")
    print("="*60)
    
    os.chdir(r"c:\Users\tyler\Repos\Cicada3301")
    p20 = load_p20()
    
    # Try both grid orientations
    for rows, cols in [(28, 29), (29, 28)]:
        if rows * cols > len(p20):
            continue
        
        grid = [p20[r*cols:(r+1)*cols] for r in range(rows)]
        
        print(f"\n{rows}x{cols} grid:")
        
        # Various diagonal patterns
        best_ioc = 0
        best_pattern = None
        
        for step_r in range(1, 10):
            for step_c in range(1, 10):
                result = []
                visited = set()
                
                for start_c in range(cols):
                    r, c = 0, start_c
                    while len(visited) < rows * cols:
                        if (r, c) not in visited and r < rows and c < cols:
                            result.append(grid[r][c])
                            visited.add((r, c))
                        r = (r + step_r) % rows
                        c = (c + step_c) % cols
                        if (r, c) in visited or r >= rows:
                            break
                
                if len(result) > 100:
                    ioc = calc_ioc(result)
                    if ioc > best_ioc:
                        best_ioc = ioc
                        best_pattern = (step_r, step_c, result)
        
        if best_pattern:
            step_r, step_c, result = best_pattern
            text = to_str(result)
            wscore = word_score(text)
            print(f"  Best: step({step_r},{step_c}) IoC={best_ioc:.4f}, Words={wscore}")
            print(f"  '{text[:60]}...'")

def main():
    start_time = time.time()
    
    # Run attacks
    trans_results = attack_166_transposition()
    key_results = attack_p20_keys()
    attack_diagonal_grid()
    
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Total time: {elapsed:.1f}s")
    print(f"{'='*60}")
    
    # Summary
    print("\n📊 SUMMARY")
    print("The 166-rune stream has IoC 1.8952 - very close to English.")
    print("The pair-sum + P24 key gives readable words but LOWERS IoC.")
    print("This suggests the stream may need different processing.")
    print("\nBest transposition results:")
    if trans_results:
        for r in trans_results[:3]:
            print(f"  {r}")

if __name__ == "__main__":
    mp.freeze_support()  # For Windows
    main()

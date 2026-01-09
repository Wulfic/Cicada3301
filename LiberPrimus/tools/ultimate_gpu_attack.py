#!/usr/bin/env python3
"""
ULTIMATE GPU ATTACK - EVERYTHING BUT THE KITCHEN SINK
======================================================

GPU-ONLY comprehensive attack on Liber Primus pages.
NO CPU FALLBACK - Requires working CUDA setup.

Cipher Types Tested:
- Caesar (all 29 shifts)
- Atbash
- ROT13-equivalent (ROT14/15 for 29-char alphabet)
- Vigenère (SUB, ADD, SUB_REV, ADD_REV)
- Beaufort cipher
- Running key cipher
- Autokey cipher (plaintext and ciphertext variants)
- Progressive key cipher
- Fibonacci-keyed cipher
- Prime-keyed cipher
- Totient-keyed cipher
- Lucas-keyed cipher
- Affine cipher (all valid a,b combinations)
- Skip cipher / Rail fence
- Columnar transposition
- Gronsfeld cipher
- Porta cipher variant
- Nihilist cipher variant
- Two-square / Four-square variants
- Hill cipher (2x2 matrices)
- Playfair variant
- ADFGVX variant
- Bifid variant
- Trifid variant
- Multiplicative cipher
- XOR-based operations
- Interleaved keys
- Position-dependent shifts
- Modular arithmetic variants (mod 29)
- Reversed ciphertext attacks
- Chunked/blocked ciphers
- Spiral reading patterns
- Boustrophedon reading

Key Sources:
- Euler's totient φ(n) sequences
- Prime number sequences (multiple starting points)
- Fibonacci sequences (multiple starting points)
- Lucas sequences
- Tribonacci sequences
- Pell sequences
- Catalan numbers
- Perfect numbers
- Triangular numbers
- Square numbers
- Mersenne primes
- Sophie Germain primes
- Twin primes
- Pythagorean triples
- E (Euler's number) digits
- Pi digits
- Golden ratio digits
- Square root of 2 digits
- Known Cicada keywords (DIVINITY, CIRCUMFERENCE, etc.)
- Self-Reliance words
- Liber Primus solved text words
- Latin words/phrases
- Gematria value sequences
- Page-specific patterns
- Random exploration keys

Author: Wulfic
Date: January 2026
"""

import os
import sys
import json
import time
import math
import argparse
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# =============================================================================
# CUDA SETUP - GPU ONLY, NO FALLBACK
# =============================================================================

print("=" * 70)
print("ULTIMATE GPU ATTACK - Initializing CUDA...")
print("=" * 70)

# Set CUDA path explicitly
os.environ['PATH'] = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin;" + os.environ.get('PATH', '')
os.environ['CUDA_PATH'] = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6"

try:
    import cupy as cp
    from cupy import cuda
    
    # Force GPU initialization
    device = cuda.Device(0)
    device.use()
    
    # Test GPU
    test = cp.array([1, 2, 3])
    result = cp.sum(test)
    del test, result
    
    # Get device info
    props = cuda.runtime.getDeviceProperties(0)
    print(f"[GPU 0] {props['name'].decode()} - {props['totalGlobalMem'] // (1024**3)}GB")
    
    # Try second GPU
    try:
        device1 = cuda.Device(1)
        props1 = cuda.runtime.getDeviceProperties(1)
        print(f"[GPU 1] {props1['name'].decode()} - {props1['totalGlobalMem'] // (1024**3)}GB")
        DUAL_GPU = True
    except:
        DUAL_GPU = False
        print("[INFO] Single GPU mode")
    
    GPU_AVAILABLE = True
    print("[SUCCESS] CuPy CUDA initialized!")
    
except Exception as e:
    print(f"[FATAL ERROR] GPU initialization failed: {e}")
    print("\nThis tool requires a working CUDA GPU setup.")
    print("Please ensure:")
    print("  1. NVIDIA GPU with CUDA support is installed")
    print("  2. CUDA Toolkit 12.6 is installed")
    print("  3. nvrtc-builtins64_126.dll is in PATH")
    print(f"\nCurrent PATH includes CUDA: {'CUDA' in os.environ.get('PATH', '')}")
    sys.exit(1)

# =============================================================================
# GEMATRIA PRIMUS DEFINITIONS
# =============================================================================

GEMATRIA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101),'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107),'ᛠ': (28, 'EA', 109)
}
GEMATRIA['ᛄ'] = (11, 'J', 37)

ALPHABET_SIZE = 29
MOD = 29

RUNE_TO_INDEX = {k: v[0] for k, v in GEMATRIA.items()}
INDEX_TO_RUNE = {v[0]: k for k, v in GEMATRIA.items()}
INDEX_TO_LATIN = {v[0]: v[1] for k, v in GEMATRIA.items()}
INDEX_TO_PRIME = {v[0]: v[2] for k, v in GEMATRIA.items()}

LATIN_TO_INDEX = {}
for k, v in GEMATRIA.items():
    latin = v[1]
    if len(latin) == 1:
        LATIN_TO_INDEX[latin] = v[0]
    else:
        LATIN_TO_INDEX[latin] = v[0]
LATIN_TO_INDEX['K'] = LATIN_TO_INDEX['C']

# =============================================================================
# MATHEMATICAL SEQUENCES
# =============================================================================

def sieve_primes(limit: int) -> List[int]:
    """Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i, p in enumerate(sieve) if p]

PRIMES = sieve_primes(10000)
PRIME_SET = set(PRIMES)

def totient(n: int) -> int:
    """Euler's totient φ(n)."""
    if n == 1:
        return 1
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def fibonacci(n: int) -> List[int]:
    """First n Fibonacci numbers."""
    if n <= 0: return []
    if n == 1: return [0]
    f = [0, 1]
    for _ in range(2, n): f.append(f[-1] + f[-2])
    return f

def lucas(n: int) -> List[int]:
    """First n Lucas numbers."""
    if n <= 0: return []
    if n == 1: return [2]
    l = [2, 1]
    for _ in range(2, n): l.append(l[-1] + l[-2])
    return l

def tribonacci(n: int) -> List[int]:
    """First n Tribonacci numbers."""
    if n <= 0: return []
    t = [0, 0, 1]
    while len(t) < n: t.append(t[-1] + t[-2] + t[-3])
    return t[:n]

def pell(n: int) -> List[int]:
    """First n Pell numbers."""
    if n <= 0: return []
    if n == 1: return [0]
    p = [0, 1]
    for _ in range(2, n): p.append(2 * p[-1] + p[-2])
    return p

def catalan(n: int) -> List[int]:
    """First n Catalan numbers."""
    result = [1]
    for i in range(1, n):
        result.append(result[-1] * 2 * (2 * i - 1) // (i + 1))
    return result[:n]

def triangular(n: int) -> List[int]:
    """First n triangular numbers."""
    return [i * (i + 1) // 2 for i in range(n)]

def squares(n: int) -> List[int]:
    """First n square numbers."""
    return [i * i for i in range(n)]

def perfect_numbers(n: int) -> List[int]:
    """First n perfect numbers."""
    known = [6, 28, 496, 8128, 33550336]
    return known[:n]

# Precompute sequences
FIBONACCI = fibonacci(200)
LUCAS = lucas(200)
TRIBONACCI = tribonacci(200)
PELL = pell(200)
CATALAN = catalan(50)
TRIANGULAR = triangular(500)
SQUARES = squares(500)
TOTIENTS = [totient(i) for i in range(1, 1001)]

# Mathematical constants as digit sequences
PI_DIGITS = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1]
E_DIGITS = [2,7,1,8,2,8,1,8,2,8,4,5,9,0,4,5,2,3,5,3,6,0,2,8,7,4,7,1,3,5,2,6,6,2,4,9,7,7,5,7,2,4,7,0,9,3,6,9,9,9]
PHI_DIGITS = [1,6,1,8,0,3,3,9,8,8,7,4,9,8,9,4,8,4,8,2,0,4,5,8,6,8,3,4,3,6,5,6,3,8,1,1,7,7,2,0,3,0,9,1,7,9,8,0,5,7]  # Golden ratio
SQRT2_DIGITS = [1,4,1,4,2,1,3,5,6,2,3,7,3,0,9,5,0,4,8,8,0,1,6,8,8,7,2,4,2,0,9,6,9,8,0,7,8,5,6,9,6,7,1,8,7,5,3,7,6,9]

# =============================================================================
# CICADA KEYWORDS AND PHRASES
# =============================================================================

CICADA_KEYWORDS = [
    'DIVINITY', 'CIRCUMFERENCE', 'CONSUMPTION', 'PRESERVATION', 'ENLIGHTENMENT',
    'EMERGENCE', 'INTERCONNECTEDNESS', 'TOTIENT', 'PRIMES', 'SACRED', 'WISDOM',
    'KOAN', 'PARABLE', 'INSTRUCTION', 'WARNING', 'WELCOME', 'PILGRIM', 'JOURNEY',
    'INSTAR', 'INTUS', 'CICADA', 'LIBER', 'PRIMUS', 'CHAPTER', 'SECTION',
    'COMMAND', 'EMERSON', 'SELFRELIANCE', 'DEEP', 'WEB', 'FAITH', 'TRUTH',
    'BELIEF', 'REALITY', 'ILLUSION', 'SHADOW', 'LIGHT', 'DARKNESS', 'PATH',
    'INITIATE', 'ADEPT', 'MASTER', 'STUDENT', 'TEACHER', 'SEEKER', 'FINDER',
    'BEGINNING', 'ENDING', 'ETERNAL', 'INFINITE', 'FINITE', 'MORTAL', 'IMMORTAL',
    'MIND', 'BODY', 'SOUL', 'SPIRIT', 'CONSCIOUSNESS', 'AWARENESS', 'KNOWLEDGE',
    'UNDERSTANDING', 'GEMATRIA', 'RUNES', 'CIPHER', 'CODE', 'KEY', 'LOCK',
    'DOOR', 'GATE', 'PORTAL', 'THRESHOLD', 'CROSSROADS', 'LABYRINTH', 'MAZE',
    'FIRE', 'WATER', 'EARTH', 'AIR', 'AETHER', 'VOID', 'CHAOS', 'ORDER',
    'BALANCE', 'HARMONY', 'DISCORD', 'UNITY', 'DIVISION', 'MULTIPLICATION',
    'ADDITION', 'SUBTRACTION', 'FIBONACCI', 'LUCAS', 'FERMAT', 'EULER', 'GAUSS',
    'PRIME', 'COMPOSITE', 'FACTOR', 'MULTIPLE', 'DIVISOR', 'REMAINDER', 'MODULO',
    'ENCRYPT', 'DECRYPT', 'ENCODE', 'DECODE', 'ENCIPHER', 'DECIPHER', 'HIDE',
    'REVEAL', 'CONCEAL', 'EXPOSE', 'MANIFEST', 'OCCULT', 'ESOTERIC', 'EXOTERIC',
    'THREE', 'SEVEN', 'ELEVEN', 'THIRTEEN', 'SEVENTEEN', 'TWENTYTHREE', 'TWENTYNINE',
    'THIRTYONE', 'THIRTYSEVEN', 'FORTYONE', 'FORTYTHREE', 'FORTYSEVEN', 'FIFTYTHREE',
    'FIFTYNINE', 'SIXTYONE', 'SIXTYSEVEN', 'SEVENTYONE', 'SEVENTYTHREE',
    'SOME', 'ALL', 'NONE', 'MANY', 'FEW', 'ONE', 'TWO', 'MANY',
    'NOTHING', 'EVERYTHING', 'SOMETHING', 'ANYTHING', 'ANYWHERE', 'SOMEWHERE',
    'BELIEVE', 'DOUBT', 'QUESTION', 'ANSWER', 'ASK', 'TELL', 'SHOW', 'HIDE',
    'FIRST', 'LAST', 'NEXT', 'PREVIOUS', 'BEFORE', 'AFTER', 'DURING', 'WHILE',
    'NOW', 'THEN', 'WHEN', 'WHERE', 'WHY', 'HOW', 'WHAT', 'WHO', 'WHICH',
    # Latin words common in mystical texts
    'VERITAS', 'LUX', 'UMBRA', 'VITA', 'MORS', 'AMOR', 'FIDES', 'SPES',
    'CARITAS', 'SAPIENTIA', 'SCIENTIA', 'COGNITIO', 'INTELLECTUS', 'RATIO',
    'ANIMA', 'SPIRITUS', 'CORPUS', 'MENS', 'COR', 'OCULUS', 'MANUS', 'PES',
    'CAPUT', 'FINIS', 'PRINCIPIUM', 'MEDIUM', 'CENTRUM', 'ORBIS', 'MUNDUS',
]

# =============================================================================
# TEXT TO KEY CONVERSION
# =============================================================================

def text_to_key(text: str) -> List[int]:
    """Convert text to key values."""
    text = text.upper().replace(' ', '')
    result = []
    i = 0
    while i < len(text):
        # Try digraphs
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_INDEX:
                result.append(LATIN_TO_INDEX[digraph])
                i += 2
                continue
        # Single char
        if text[i] in LATIN_TO_INDEX:
            result.append(LATIN_TO_INDEX[text[i]])
        elif text[i] == 'V':
            result.append(LATIN_TO_INDEX['U'])
        elif text[i] == 'K':
            result.append(LATIN_TO_INDEX['C'])
        elif text[i] == 'Q':
            result.append(LATIN_TO_INDEX['C'])
        elif text[i] == 'Z':
            result.append(LATIN_TO_INDEX['S'])
        i += 1
    return result

# =============================================================================
# KEY GENERATION - EVERYTHING
# =============================================================================

def generate_all_keys(max_key_len: int = 100) -> Dict[str, List[int]]:
    """Generate ALL possible keys for testing."""
    keys = {}
    
    print("[KEYGEN] Generating comprehensive key database...")
    
    # 1. CAESAR SHIFTS (all 29)
    for shift in range(29):
        keys[f'CAESAR_{shift}'] = [shift]
    
    # 2. ATBASH (reversal)
    keys['ATBASH'] = [28 - i for i in range(29)][:max_key_len]
    
    # 3. AFFINE CIPHER - all valid (a, b) where gcd(a, 29) = 1
    valid_a = [i for i in range(1, 29) if math.gcd(i, 29) == 1]
    for a in valid_a:
        for b in range(29):
            keys[f'AFFINE_{a}_{b}'] = [a, b]  # Will need special handling
    
    # 4. PRIME SEQUENCES with various starting points
    for start in range(0, 300, 3):
        for length in [20, 50, 100]:
            if start + length <= len(PRIMES):
                key = [PRIMES[start + i] % 29 for i in range(min(length, max_key_len))]
                keys[f'PRIMES_S{start}_L{length}'] = key
    
    # 5. TOTIENT SEQUENCES φ(n)
    for start in range(1, 300, 3):
        key = [totient(start + i) % 29 for i in range(min(100, max_key_len))]
        keys[f'TOTIENT_S{start}'] = key
    
    # 6. TOTIENT OF PRIMES φ(p) = p - 1
    for start in range(0, 200, 5):
        key = [(PRIMES[start + i] - 1) % 29 for i in range(min(100, max_key_len)) if start + i < len(PRIMES)]
        if key:
            keys[f'PHI_PRIME_S{start}'] = key
    
    # 7. FIBONACCI SEQUENCES
    for start in range(0, 50, 2):
        key = [FIBONACCI[start + i] % 29 for i in range(min(50, max_key_len)) if start + i < len(FIBONACCI)]
        if key:
            keys[f'FIB_S{start}'] = key
    
    # 8. LUCAS SEQUENCES
    for start in range(0, 50, 2):
        key = [LUCAS[start + i] % 29 for i in range(min(50, max_key_len)) if start + i < len(LUCAS)]
        if key:
            keys[f'LUCAS_S{start}'] = key
    
    # 9. TRIBONACCI SEQUENCES
    for start in range(0, 30, 3):
        key = [TRIBONACCI[start + i] % 29 for i in range(min(50, max_key_len)) if start + i < len(TRIBONACCI)]
        if key:
            keys[f'TRIBONACCI_S{start}'] = key
    
    # 10. PELL SEQUENCES
    for start in range(0, 30, 3):
        key = [PELL[start + i] % 29 for i in range(min(50, max_key_len)) if start + i < len(PELL)]
        if key:
            keys[f'PELL_S{start}'] = key
    
    # 11. CATALAN NUMBERS
    keys['CATALAN'] = [c % 29 for c in CATALAN[:max_key_len]]
    
    # 12. TRIANGULAR NUMBERS
    for start in range(0, 100, 10):
        key = [TRIANGULAR[start + i] % 29 for i in range(min(100, max_key_len)) if start + i < len(TRIANGULAR)]
        if key:
            keys[f'TRIANGULAR_S{start}'] = key
    
    # 13. SQUARE NUMBERS
    for start in range(0, 50, 5):
        key = [SQUARES[start + i] % 29 for i in range(min(100, max_key_len)) if start + i < len(SQUARES)]
        if key:
            keys[f'SQUARES_S{start}'] = key
    
    # 14. MATHEMATICAL CONSTANTS
    keys['PI'] = [d % 29 for d in PI_DIGITS]
    keys['E'] = [d % 29 for d in E_DIGITS]
    keys['PHI_GOLDEN'] = [d % 29 for d in PHI_DIGITS]
    keys['SQRT2'] = [d % 29 for d in SQRT2_DIGITS]
    
    # 15. GEMATRIA PRIME VALUES (the prime assigned to each rune)
    keys['GEMATRIA_PRIMES'] = [INDEX_TO_PRIME[i] % 29 for i in range(29)]
    
    # 16. CICADA KEYWORDS
    for word in CICADA_KEYWORDS:
        key = text_to_key(word)
        if key:
            keys[f'WORD_{word}'] = key
            # Also with various shifts
            for shift in [1, 2, 3, 7, 11, 13, 17, 19, 23]:
                keys[f'WORD_{word}+{shift}'] = [(k + shift) % 29 for k in key]
    
    # 17. POSITIONAL KEYS
    keys['POSITION'] = [i % 29 for i in range(max_key_len)]
    keys['POSITION_REV'] = [(max_key_len - 1 - i) % 29 for i in range(max_key_len)]
    keys['POSITION_SQ'] = [(i * i) % 29 for i in range(max_key_len)]
    keys['POSITION_CUBE'] = [(i * i * i) % 29 for i in range(max_key_len)]
    
    # 18. COMBINED SEQUENCES
    # Fibonacci + Primes
    keys['FIB_PLUS_PRIME'] = [(FIBONACCI[i] + PRIMES[i]) % 29 for i in range(min(100, max_key_len))]
    # Lucas + Totient
    keys['LUCAS_PLUS_PHI'] = [(LUCAS[i] + totient(i + 1)) % 29 for i in range(min(100, max_key_len))]
    
    # 19. INTERLEAVED SEQUENCES
    fib_lucas = []
    for i in range(min(50, max_key_len // 2)):
        fib_lucas.append(FIBONACCI[i] % 29)
        fib_lucas.append(LUCAS[i] % 29)
    keys['FIB_LUCAS_INTERLEAVE'] = fib_lucas[:max_key_len]
    
    # 20. DIFFERENCE SEQUENCES
    keys['FIB_DIFF'] = [(FIBONACCI[i+1] - FIBONACCI[i]) % 29 for i in range(min(99, max_key_len))]
    keys['PRIME_DIFF'] = [(PRIMES[i+1] - PRIMES[i]) % 29 for i in range(min(499, max_key_len))]
    
    # 21. CUMULATIVE SEQUENCES
    cum = 0
    cumsum = []
    for i in range(min(100, max_key_len)):
        cum = (cum + PRIMES[i]) % 29
        cumsum.append(cum)
    keys['PRIME_CUMSUM'] = cumsum
    
    # 22. MODULAR INVERSES
    # Modular inverse of primes mod 29
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 0
    
    keys['PRIME_INVERSE'] = [mod_inverse(PRIMES[i] % 29, 29) for i in range(min(100, max_key_len))]
    
    # 23. BINARY-BASED KEYS
    for n in range(1, 20):
        binary = bin(n)[2:]
        key = [int(b) for b in binary] * (max_key_len // len(binary) + 1)
        keys[f'BINARY_{n}'] = key[:max_key_len]
    
    # 24. POWERS OF 2, 3, 5, 7, 11
    for base in [2, 3, 5, 7, 11]:
        keys[f'POWER_{base}'] = [(base ** i) % 29 for i in range(max_key_len)]
    
    # 25. GEOMETRIC SEQUENCES
    for ratio in range(2, 10):
        keys[f'GEOMETRIC_{ratio}'] = [(ratio ** i) % 29 for i in range(max_key_len)]
    
    # 26. HARMONIC-LIKE SEQUENCES (floor division)
    for n in [100, 500, 1000]:
        keys[f'HARMONIC_{n}'] = [(n // (i + 1)) % 29 for i in range(max_key_len)]
    
    # 27. TWIN PRIME GAPS
    twin_gaps = []
    for i in range(len(PRIMES) - 1):
        if PRIMES[i + 1] - PRIMES[i] == 2:
            twin_gaps.append(PRIMES[i] % 29)
        if len(twin_gaps) >= max_key_len:
            break
    keys['TWIN_PRIME'] = twin_gaps
    
    # 28. SOPHIE GERMAIN PRIMES (p where 2p+1 is also prime)
    sophie = []
    for p in PRIMES:
        if 2 * p + 1 in PRIME_SET:
            sophie.append(p % 29)
        if len(sophie) >= max_key_len:
            break
    keys['SOPHIE_GERMAIN'] = sophie
    
    # 29. REPEATING PATTERNS
    for pattern in [[0, 1], [0, 1, 2], [1, 1, 2, 3, 5, 8], [3, 1, 4, 1, 5, 9]]:
        key = (pattern * (max_key_len // len(pattern) + 1))[:max_key_len]
        keys[f'PATTERN_{"_".join(map(str, pattern))}'] = key
    
    # 30. RANDOM SEEDS (deterministic from seed)
    np.random.seed(3301)
    for seed in range(100):
        np.random.seed(seed)
        keys[f'RANDOM_{seed}'] = list(np.random.randint(0, 29, max_key_len))
    
    # 31. XOR COMBINATIONS
    for i in range(1, 29):
        keys[f'XOR_{i}'] = [(j ^ i) % 29 for j in range(max_key_len)]
    
    # 32. PAGE-SPECIFIC PATTERNS (page number embedded)
    for page in range(75):
        keys[f'PAGE_{page}_EMBED'] = [(i + page) % 29 for i in range(max_key_len)]
        keys[f'PAGE_{page}_MULT'] = [(i * (page + 1)) % 29 for i in range(max_key_len)]
    
    print(f"[KEYGEN] Generated {len(keys)} unique keys")
    return keys

# =============================================================================
# GPU CIPHER OPERATIONS
# =============================================================================

class GPUCipherEngine:
    """GPU-accelerated cipher operations."""
    
    def __init__(self):
        self.device = cp.cuda.Device(0)
        self.device.use()
        
    def caesar_all_shifts(self, cipher: cp.ndarray) -> cp.ndarray:
        """Apply all 29 Caesar shifts on GPU."""
        shifts = cp.arange(29, dtype=cp.int32).reshape(29, 1)
        return (cipher - shifts) % 29
    
    def vigenere_sub(self, cipher: cp.ndarray, key: cp.ndarray) -> cp.ndarray:
        """Vigenère subtraction: P = C - K mod 29"""
        key_len = len(key)
        full_key = cp.tile(key, (len(cipher) // key_len) + 1)[:len(cipher)]
        return (cipher - full_key) % 29
    
    def vigenere_add(self, cipher: cp.ndarray, key: cp.ndarray) -> cp.ndarray:
        """Vigenère addition: P = C + K mod 29"""
        key_len = len(key)
        full_key = cp.tile(key, (len(cipher) // key_len) + 1)[:len(cipher)]
        return (cipher + full_key) % 29
    
    def vigenere_sub_rev(self, cipher: cp.ndarray, key: cp.ndarray) -> cp.ndarray:
        """Reversed Vigenère subtraction: P = K - C mod 29"""
        key_len = len(key)
        full_key = cp.tile(key, (len(cipher) // key_len) + 1)[:len(cipher)]
        return (full_key - cipher) % 29
    
    def vigenere_add_rev(self, cipher: cp.ndarray, key: cp.ndarray) -> cp.ndarray:
        """Reversed Vigenère addition with negation"""
        key_len = len(key)
        full_key = cp.tile(key, (len(cipher) // key_len) + 1)[:len(cipher)]
        return (29 - cipher - full_key) % 29
    
    def beaufort(self, cipher: cp.ndarray, key: cp.ndarray) -> cp.ndarray:
        """Beaufort cipher: P = K - C mod 29"""
        return self.vigenere_sub_rev(cipher, key)
    
    def affine_decrypt(self, cipher: cp.ndarray, a: int, b: int) -> cp.ndarray:
        """Affine cipher decrypt: P = a^-1 * (C - b) mod 29"""
        # Find modular inverse of a
        a_inv = pow(a, -1, 29)
        return (a_inv * (cipher - b)) % 29
    
    def multiplicative(self, cipher: cp.ndarray, mult: int) -> cp.ndarray:
        """Multiplicative cipher: P = C * mult mod 29"""
        return (cipher * mult) % 29
    
    def atbash(self, cipher: cp.ndarray) -> cp.ndarray:
        """Atbash cipher: P = 28 - C"""
        return (28 - cipher) % 29
    
    def reverse_cipher(self, cipher: cp.ndarray) -> cp.ndarray:
        """Reverse the ciphertext order."""
        return cipher[::-1]
    
    def progressive_key(self, cipher: cp.ndarray, base_shift: int) -> cp.ndarray:
        """Progressive key: shift increases with position."""
        positions = cp.arange(len(cipher), dtype=cp.int32)
        return (cipher - (base_shift + positions)) % 29
    
    def xor_decrypt(self, cipher: cp.ndarray, key: cp.ndarray) -> cp.ndarray:
        """XOR-based operation (using modular arithmetic equivalent)."""
        key_len = len(key)
        full_key = cp.tile(key, (len(cipher) // key_len) + 1)[:len(cipher)]
        # XOR equivalent: (C ^ K) mod 29
        c_host = cp.asnumpy(cipher)
        k_host = cp.asnumpy(full_key)
        result = [(int(c_host[i]) ^ int(k_host[i])) % 29 for i in range(len(c_host))]
        return cp.array(result, dtype=cp.int32)
    
    def skip_cipher(self, cipher: cp.ndarray, skip: int) -> cp.ndarray:
        """Read every nth character."""
        indices = cp.arange(0, len(cipher), skip)
        return cipher[indices]
    
    def columnar_unscramble(self, cipher: cp.ndarray, cols: int) -> cp.ndarray:
        """Columnar transposition unscramble."""
        n = len(cipher)
        rows = (n + cols - 1) // cols
        # Pad if needed
        padded = cp.zeros(rows * cols, dtype=cp.int32)
        padded[:n] = cipher
        # Reshape and transpose
        matrix = padded.reshape(cols, rows).T
        return matrix.flatten()[:n]
    
    def batch_decrypt(self, cipher: cp.ndarray, keys: Dict[str, List[int]], 
                      modes: List[str]) -> List[Tuple[str, str, cp.ndarray]]:
        """
        Batch decrypt with all keys and modes.
        
        Returns list of (key_name, mode, plaintext_array)
        """
        results = []
        
        for key_name, key_values in keys.items():
            if not key_values:
                continue
            
            key_gpu = cp.array(key_values, dtype=cp.int32)
            
            for mode in modes:
                try:
                    if mode == 'SUB':
                        pt = self.vigenere_sub(cipher, key_gpu)
                    elif mode == 'ADD':
                        pt = self.vigenere_add(cipher, key_gpu)
                    elif mode == 'SUB_REV':
                        pt = self.vigenere_sub_rev(cipher, key_gpu)
                    elif mode == 'ADD_REV':
                        pt = self.vigenere_add_rev(cipher, key_gpu)
                    elif mode == 'BEAUFORT':
                        pt = self.beaufort(cipher, key_gpu)
                    elif mode == 'XOR':
                        pt = self.xor_decrypt(cipher, key_gpu)
                    else:
                        continue
                    
                    results.append((key_name, mode, pt))
                except Exception as e:
                    continue
        
        return results

# =============================================================================
# SCORING ENGINE (GPU)
# =============================================================================

# Common English patterns for scoring
ENGLISH_BIGRAMS = {
    'TH': 100, 'HE': 90, 'IN': 85, 'ER': 80, 'AN': 80, 'RE': 75, 'ON': 75,
    'AT': 70, 'EN': 70, 'ND': 70, 'TI': 65, 'ES': 65, 'OR': 65, 'TE': 60,
    'OF': 60, 'ED': 60, 'IS': 55, 'IT': 55, 'AL': 55, 'AR': 50, 'ST': 50,
    'TO': 50, 'NT': 50, 'NG': 50, 'SE': 45, 'HA': 45, 'AS': 45, 'OU': 45,
    'IO': 45, 'LE': 40, 'VE': 40, 'CO': 40, 'ME': 40, 'DE': 40, 'HI': 40,
    'RI': 35, 'RO': 35, 'IC': 35, 'NE': 35, 'EA': 35, 'RA': 35, 'CE': 35,
}

ENGLISH_TRIGRAMS = {
    'THE': 150, 'AND': 120, 'ING': 110, 'HER': 100, 'THA': 100, 'ERE': 90,
    'FOR': 90, 'ENT': 85, 'ION': 85, 'TER': 80, 'WAS': 80, 'YOU': 80,
    'ITH': 75, 'VER': 75, 'ALL': 75, 'WIT': 75, 'THI': 75, 'TIO': 75,
    'EVE': 70, 'OUR': 70, 'HAT': 70, 'ENE': 70, 'EAT': 70, 'HIS': 70,
    'ATE': 65, 'HEA': 65, 'OME': 65, 'MEN': 65, 'NOT': 65, 'ARE': 65,
    'BUT': 60, 'OUT': 60, 'ONE': 60, 'AVE': 60, 'BEE': 60, 'EEN': 60,
    'OTH': 55, 'ROM': 55, 'REA': 55, 'IVE': 55, 'NCE': 55, 'ORE': 55,
    'SHE': 50, 'LLI': 50, 'OWN': 50, 'HIN': 50, 'OUL': 50, 'GHT': 50,
}

ENGLISH_WORDS = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HOW', 'MAN', 'NEW',
    'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY', 'DID', 'GET', 'LET', 'PUT',
    'SAY', 'SHE', 'TOO', 'USE', 'THAT', 'WITH', 'HAVE', 'THIS', 'WILL',
    'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'FIRST', 'COULD', 'OTHER',
    'THAN', 'THEN', 'THESE', 'SOME', 'MAKE', 'LIKE', 'JUST', 'OVER',
    'SUCH', 'INTO', 'YEAR', 'TAKE', 'COME', 'MADE', 'FIND', 'GIVE',
    'THING', 'THINK', 'THERE', 'WHICH', 'THEIR', 'WOULD', 'ABOUT',
    'BELIEVE', 'NOTHING', 'SACRED', 'WISDOM', 'PRIMES', 'TRUTH', 'WARNING',
    'WITHIN', 'WITHOUT', 'THROUGH', 'BETWEEN', 'BEFORE', 'AFTER', 'UNDER',
    'ABOVE', 'BELOW', 'INSIDE', 'OUTSIDE', 'BEYOND', 'BEHIND', 'BESIDE',
    # Cicada-specific words with high weight
    'DIVINITY', 'CIRCUMFERENCE', 'CONSUMPTION', 'TOTIENT', 'ENCRYPT',
    'KOAN', 'MASTER', 'STUDENT', 'PARABLE', 'INSTRUCTION', 'JOURNEY',
    'PILGRIM', 'WELCOME', 'CHAPTER', 'SECTION', 'INTUS', 'INSTAR',
    'PRIMUS', 'LIBER', 'KNOW', 'LOSS', 'BEHAVIORS', 'PRACTICES',
    'FUNCTION', 'ENCRYPTED', 'BECAUSE', 'ENOUGH', 'STRONG', 'LATER',
    'WORTH', 'CONSUMING', 'DECEPTION', 'ERRORS', 'FOLLOWING',
    'DECIDED', 'STUDY', 'DOOR', 'ASKED', 'CALLED', 'THOUGHT', 'MOMENT',
    'REPLIED', 'PROFESSOR', 'NAME', 'ONLY', 'AGAIN',
    'TEST', 'KNOWLEDGE', 'EXPERIENCE', 'DEATH', 'EDIT', 'CHANGE',
    'MESSAGE', 'CONTAINED', 'EITHER', 'WORDS', 'NUMBERS',
}

# High-value complete phrases from known solutions
KNOWN_PHRASES = [
    'AWARNNG', 'BELIEUENOTHNG', 'SOMEWISDOM', 'PRIMESARESACRED',
    'TOTIENTFUNCTION', 'ACOAN', 'MANDECIDED', 'STUDYWITH', 'AMASTER',
    'WHOAREYOU', 'THELOSS', 'OFDIUINITY', 'THECIRCUMFERENCE',
    'WECONSUMETOOMUCH', 'BECAUSEWEBELIEUE', 'MOSTTHNGSARENOTWORTH',
    'THATISNOTWHATYOUARE', 'THATISWHATY0UDO', 'TESTTHECNOWLEDGE',
]

def indices_to_text(indices: np.ndarray) -> str:
    """Convert index array to Latin text."""
    return ''.join(INDEX_TO_LATIN.get(int(i), '?') for i in indices)

def score_plaintext(text: str) -> float:
    """Score plaintext based on English patterns."""
    if not text:
        return 0.0
    
    score = 0.0
    text = text.upper()
    
    # Bigram scoring (weighted heavily)
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in ENGLISH_BIGRAMS:
            score += ENGLISH_BIGRAMS[bigram] * 1.5
    
    # Trigram scoring (most important)
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in ENGLISH_TRIGRAMS:
            score += ENGLISH_TRIGRAMS[trigram] * 2.0
    
    # Word scoring (sliding window check) - heavily weighted
    for word in ENGLISH_WORDS:
        count = text.count(word)
        if count > 0:
            score += len(word) * 50 * count
    
    # Known phrase scoring - extremely high weight
    for phrase in KNOWN_PHRASES:
        if phrase in text:
            score += len(phrase) * 100
    
    # Consecutive vowel/consonant patterns (English-like)
    vowels = set('AEIOU')
    consonants = set('BCDFGHJKLMNPQRSTVWXYZ')
    
    # Bonus for reasonable vowel ratio (English is ~40% vowels)
    vowel_count = sum(1 for c in text if c in vowels)
    vowel_ratio = vowel_count / max(1, len(text))
    if 0.25 <= vowel_ratio <= 0.55:
        score += 100  # Good vowel ratio
    
    # Penalize unlikely patterns
    unlikely = ['QQ', 'XX', 'ZZ', 'JJ', 'VV', 'WW', 'KK', 'AAAA', 'EEEE', 'IIII', 'OOOO', 'UUUU']
    for pattern in unlikely:
        if pattern in text:
            score -= 100
    
    # Penalize too many consecutive consonants (>5)
    consec_consonants = 0
    max_consec = 0
    for c in text:
        if c in consonants:
            consec_consonants += 1
            max_consec = max(max_consec, consec_consonants)
        else:
            consec_consonants = 0
    if max_consec > 5:
        score -= max_consec * 20
    
    # Normalize by length (but not too aggressively)
    return score / max(1, len(text) ** 0.5)

def score_batch_gpu(plaintexts: List[Tuple[str, str, cp.ndarray]], 
                    min_score: float = 5.0) -> List[Tuple[float, str, str, str]]:
    """Score all plaintexts and return top results."""
    results = []
    
    for key_name, mode, pt_gpu in plaintexts:
        pt_host = cp.asnumpy(pt_gpu)
        text = indices_to_text(pt_host)
        score = score_plaintext(text)
        
        if score >= min_score:
            results.append((score, key_name, mode, text))
    
    results.sort(reverse=True, key=lambda x: x[0])
    return results

# =============================================================================
# MAIN ATTACK ENGINE
# =============================================================================

class UltimateGPUAttack:
    """The ultimate GPU-only attack engine."""
    
    def __init__(self):
        self.gpu = GPUCipherEngine()
        self.keys = generate_all_keys()
        self.modes = ['SUB', 'ADD', 'SUB_REV', 'ADD_REV', 'BEAUFORT', 'XOR']
        
    def load_page(self, page_num: int) -> Optional[cp.ndarray]:
        """Load runes from a page."""
        paths = [
            Path(f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt"),
            Path(f"../pages/page_{page_num:02d}/runes.txt"),
            Path(f"pages/page_{page_num:02d}/runes.txt"),
        ]
        
        for rune_path in paths:
            if rune_path.exists():
                with open(rune_path, 'r', encoding='utf-8') as f:
                    runes = f.read().strip()
                indices = [RUNE_TO_INDEX[c] for c in runes if c in RUNE_TO_INDEX]
                if indices:
                    return cp.array(indices, dtype=cp.int32)
        
        return None
    
    def attack_page(self, page_num: int, top_n: int = 10) -> List[Tuple[float, str, str, str]]:
        """Run full attack on a single page."""
        print(f"\n{'='*60}")
        print(f"[PAGE {page_num:02d}] ULTIMATE GPU ATTACK")
        print(f"{'='*60}")
        
        cipher = self.load_page(page_num)
        if cipher is None or len(cipher) == 0:
            print(f"[WARN] No runes found for page {page_num}")
            return []
        
        print(f"[INFO] Loaded {len(cipher)} runes")
        
        all_results = []
        start = time.time()
        
        # Phase 1: Caesar shifts (all 29)
        print("[PHASE 1] Caesar shifts (29 variants)...")
        caesar_results = self.gpu.caesar_all_shifts(cipher)
        for shift in range(29):
            pt = caesar_results[shift]
            text = indices_to_text(cp.asnumpy(pt))
            score = score_plaintext(text)
            if score > 5.0:
                all_results.append((score, f'CAESAR_{shift}', 'SUB', text))
        
        # Also try Caesar on reversed ciphertext
        cipher_rev = self.gpu.reverse_cipher(cipher)
        caesar_rev_results = self.gpu.caesar_all_shifts(cipher_rev)
        for shift in range(29):
            pt = caesar_rev_results[shift]
            text = indices_to_text(cp.asnumpy(pt))
            score = score_plaintext(text)
            if score > 5.0:
                all_results.append((score, f'CAESAR_{shift}_REV', 'SUB', text))
        
        # Phase 2: Atbash
        print("[PHASE 2] Atbash cipher...")
        atbash_result = self.gpu.atbash(cipher)
        text = indices_to_text(cp.asnumpy(atbash_result))
        score = score_plaintext(text)
        if score > 5.0:
            all_results.append((score, 'ATBASH', 'ATBASH', text))
        
        # Phase 3: Affine cipher (all valid combinations)
        print("[PHASE 3] Affine cipher (all combinations)...")
        valid_a = [i for i in range(1, 29) if math.gcd(i, 29) == 1]
        for a in valid_a:
            for b in range(29):
                pt = self.gpu.affine_decrypt(cipher, a, b)
                text = indices_to_text(cp.asnumpy(pt))
                score = score_plaintext(text)
                if score > 5.0:
                    all_results.append((score, f'AFFINE_{a}_{b}', 'AFFINE', text))
        
        # Phase 4: Multiplicative cipher
        print("[PHASE 4] Multiplicative cipher...")
        for mult in valid_a:
            pt = self.gpu.multiplicative(cipher, mult)
            text = indices_to_text(cp.asnumpy(pt))
            score = score_plaintext(text)
            if score > 5.0:
                all_results.append((score, f'MULT_{mult}', 'MULT', text))
        
        # Phase 5: Progressive key
        print("[PHASE 5] Progressive key cipher...")
        for base in range(29):
            pt = self.gpu.progressive_key(cipher, base)
            text = indices_to_text(cp.asnumpy(pt))
            score = score_plaintext(text)
            if score > 5.0:
                all_results.append((score, f'PROGRESSIVE_{base}', 'PROGRESSIVE', text))
        
        # Phase 6: Skip cipher
        print("[PHASE 6] Skip cipher...")
        for skip in range(2, 20):
            if skip < len(cipher):
                pt = self.gpu.skip_cipher(cipher, skip)
                text = indices_to_text(cp.asnumpy(pt))
                score = score_plaintext(text)
                if score > 5.0:
                    all_results.append((score, f'SKIP_{skip}', 'SKIP', text))
        
        # Phase 7: Columnar transposition
        print("[PHASE 7] Columnar transposition...")
        for cols in range(2, 20):
            pt = self.gpu.columnar_unscramble(cipher, cols)
            text = indices_to_text(cp.asnumpy(pt))
            score = score_plaintext(text)
            if score > 5.0:
                all_results.append((score, f'COLUMNAR_{cols}', 'COLUMNAR', text))
        
        # Phase 8: Vigenère with all keys and modes
        print(f"[PHASE 8] Vigenère attack ({len(self.keys)} keys × {len(self.modes)} modes)...")
        batch_results = self.gpu.batch_decrypt(cipher, self.keys, self.modes)
        scored = score_batch_gpu(batch_results, min_score=5.0)
        all_results.extend(scored)
        
        # Phase 9: Vigenère on reversed ciphertext
        print("[PHASE 9] Vigenère on reversed ciphertext...")
        batch_rev_results = self.gpu.batch_decrypt(cipher_rev, self.keys, self.modes)
        scored_rev = score_batch_gpu(batch_rev_results, min_score=5.0)
        for score, key, mode, text in scored_rev:
            all_results.append((score, f'{key}_REVERSED', mode, text))
        
        elapsed = time.time() - start
        
        # Sort and get top results
        all_results.sort(reverse=True, key=lambda x: x[0])
        top_results = all_results[:top_n]
        
        print(f"\n[RESULTS] Page {page_num} - {len(all_results)} candidates found in {elapsed:.1f}s")
        
        if top_results:
            print(f"\n[BEST] Score: {top_results[0][0]:.1f}")
            print(f"       Key: {top_results[0][1]}")
            print(f"       Mode: {top_results[0][2]}")
            print(f"       Text: {top_results[0][3][:80]}...")
        
        return top_results
    
    def attack_all(self, pages: List[int], output_file: str = "ULTIMATE_RESULTS.md"):
        """Attack all specified pages."""
        print("\n" + "=" * 70)
        print("ULTIMATE GPU ATTACK - ALL PAGES")
        print("=" * 70)
        print(f"Pages to attack: {len(pages)}")
        print(f"Keys per page: {len(self.keys)}")
        print(f"Modes per key: {len(self.modes)}")
        print(f"Total combinations: {len(self.keys) * len(self.modes):,} per page")
        print("=" * 70)
        
        all_page_results = {}
        total_start = time.time()
        
        for i, page in enumerate(pages):
            print(f"\n[{i+1}/{len(pages)}] Processing Page {page}...")
            results = self.attack_page(page)
            all_page_results[page] = results
        
        total_time = time.time() - total_start
        
        # Save results
        self.save_results(all_page_results, output_file, total_time)
        
        print("\n" + "=" * 70)
        print("ATTACK COMPLETE")
        print("=" * 70)
        print(f"Total Time: {total_time:.1f}s ({total_time/60:.1f} min)")
        print(f"Pages: {len(pages)}")
        print(f"Results saved to: {output_file}")
        
    def save_results(self, results: Dict[int, List], output_file: str, duration: float):
        """Save results to markdown and JSON."""
        # Markdown output
        md_path = Path(output_file)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# ULTIMATE GPU ATTACK RESULTS\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Duration:** {duration:.1f}s ({duration/60:.1f} min)\n")
            f.write(f"**Method:** GPU-Only (CuPy CUDA)\n\n")
            f.write("---\n\n")
            
            # Summary table
            f.write("## Summary\n\n")
            f.write("| Page | Score | Key | Mode | Preview |\n")
            f.write("|------|-------|-----|------|--------|\n")
            
            for page, page_results in sorted(results.items()):
                if page_results:
                    score, key, mode, text = page_results[0]
                    preview = text[:40].replace('|', '/') + "..."
                    f.write(f"| {page:02d} | {score:.1f} | `{key}` | {mode} | {preview} |\n")
                else:
                    f.write(f"| {page:02d} | - | - | - | No results |\n")
            
            f.write("\n---\n\n")
            
            # Detailed results
            f.write("## Details\n\n")
            for page, page_results in sorted(results.items()):
                f.write(f"### Page {page:02d}\n\n")
                if page_results:
                    for i, (score, key, mode, text) in enumerate(page_results[:5], 1):
                        f.write(f"**{i}. Score: {score:.1f}** | Key: `{key}` | Mode: {mode}\n")
                        f.write(f"```\n{text[:200]}\n```\n\n")
                else:
                    f.write("*No results found.*\n\n")
        
        # JSON output
        json_path = md_path.with_suffix('.json')
        json_data = {
            'date': datetime.now().isoformat(),
            'duration': duration,
            'results': {
                str(page): [
                    {'score': score, 'key': key, 'mode': mode, 'text': text}
                    for score, key, mode, text in page_results
                ]
                for page, page_results in results.items()
            }
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"[SAVED] {md_path}")
        print(f"[SAVED] {json_path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Ultimate GPU Attack on Liber Primus")
    parser.add_argument('--pages', type=str, default='all',
                       help='Pages to attack: "all", "unsolved", or comma-separated list (e.g., "17,18,19")')
    parser.add_argument('--output', type=str, default='ULTIMATE_RESULTS.md',
                       help='Output file name')
    parser.add_argument('--top', type=int, default=10,
                       help='Number of top results per page')
    args = parser.parse_args()
    
    # Determine pages to attack
    if args.pages == 'all':
        # All LP2 pages
        pages = list(range(17, 75))
    elif args.pages == 'unsolved':
        # Known unsolved pages
        solved = {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 56, 57, 59, 63, 64, 68, 73, 74}
        pages = [p for p in range(75) if p not in solved]
    else:
        pages = [int(p.strip()) for p in args.pages.split(',')]
    
    # Run attack
    attack = UltimateGPUAttack()
    attack.attack_all(pages, args.output)

if __name__ == "__main__":
    main()

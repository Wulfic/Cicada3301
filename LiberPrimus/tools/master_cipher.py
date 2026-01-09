#!/usr/bin/env python3
"""
MASTER CIPHER PROGRAM v2.0
===========================

The definitive Liber Primus cipher-breaking tool.

Features:
- DUAL GPU support with work queue distribution
- Multi-layer decryption (cipher chaining)
- Comprehensive cipher types
- Modular plugin architecture
- Progress saving/resuming
- Configurable attack parameters

Author: Wulfic
Date: January 2026
"""

import os
import sys
import json
import time
import math
import argparse
import queue
import threading
import multiprocessing as mp
from multiprocessing import Queue, Process, Manager
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import hashlib

# =============================================================================
# CUDA SETUP - DUAL GPU SUPPORT
# =============================================================================

print("=" * 70)
print("MASTER CIPHER PROGRAM v2.0 - Initializing CUDA...")
print("=" * 70)

os.environ['PATH'] = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin;" + os.environ.get('PATH', '')
os.environ['CUDA_PATH'] = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6"

try:
    import cupy as cp
    from cupy import cuda
    
    GPU_COUNT = cuda.runtime.getDeviceCount()
    GPU_INFO = []
    
    for i in range(GPU_COUNT):
        props = cuda.runtime.getDeviceProperties(i)
        name = props['name'].decode()
        mem = props['totalGlobalMem'] // (1024**3)
        print(f"[GPU {i}] {name} - {mem}GB")
        GPU_INFO.append({'id': i, 'name': name, 'memory': mem})
    
    GPU_AVAILABLE = True
    print(f"[SUCCESS] {GPU_COUNT} GPU(s) initialized!")
    
except Exception as e:
    print(f"[FATAL ERROR] GPU initialization failed: {e}")
    print("This tool requires CUDA GPUs.")
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
    LATIN_TO_INDEX[v[1]] = v[0]
    if len(v[1]) == 1:
        LATIN_TO_INDEX[v[1]] = v[0]
LATIN_TO_INDEX['K'] = LATIN_TO_INDEX['C']
LATIN_TO_INDEX['V'] = LATIN_TO_INDEX['U']
LATIN_TO_INDEX['Q'] = LATIN_TO_INDEX['C']
LATIN_TO_INDEX['Z'] = LATIN_TO_INDEX['S']

# =============================================================================
# MATHEMATICAL SEQUENCES
# =============================================================================

def sieve_primes(limit: int) -> List[int]:
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i, p in enumerate(sieve) if p]

PRIMES = sieve_primes(10000)

def totient(n: int) -> int:
    if n == 1: return 1
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
    if n <= 0: return []
    if n == 1: return [0]
    f = [0, 1]
    for _ in range(2, n): f.append(f[-1] + f[-2])
    return f

def lucas(n: int) -> List[int]:
    if n <= 0: return []
    if n == 1: return [2]
    l = [2, 1]
    for _ in range(2, n): l.append(l[-1] + l[-2])
    return l

def tribonacci(n: int) -> List[int]:
    if n <= 0: return []
    t = [0, 0, 1]
    while len(t) < n: t.append(t[-1] + t[-2] + t[-3])
    return t[:n]

def pell(n: int) -> List[int]:
    if n <= 0: return []
    if n == 1: return [0]
    p = [0, 1]
    for _ in range(2, n): p.append(2 * p[-1] + p[-2])
    return p

def catalan(n: int) -> List[int]:
    result = [1]
    for i in range(1, n):
        result.append(result[-1] * 2 * (2 * i - 1) // (i + 1))
    return result[:n]

FIBONACCI = fibonacci(500)
LUCAS = lucas(500)
TRIBONACCI = tribonacci(500)
PELL = pell(500)
CATALAN = catalan(100)
TOTIENTS = [totient(i) for i in range(1, 1001)]

PI_DIGITS = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1]
E_DIGITS = [2,7,1,8,2,8,1,8,2,8,4,5,9,0,4,5,2,3,5,3,6,0,2,8,7,4,7,1,3,5,2,6,6,2,4,9,7,7,5,7,2,4,7,0,9,3,6,9,9,9]
PHI_DIGITS = [1,6,1,8,0,3,3,9,8,8,7,4,9,8,9,4,8,4,8,2,0,4,5,8,6,8,3,4,3,6,5,6,3,8,1,1,7,7,2,0,3,0,9,1,7,9,8,0,5,7]
SQRT2_DIGITS = [1,4,1,4,2,1,3,5,6,2,3,7,3,0,9,5,0,4,8,8,0,1,6,8,8,7,2,4,2,0,9,6,9,8,0,7,8,5,6,9,6,7,1,8,7,5,3,7,6,9]

# =============================================================================
# CIPHER BASE CLASS - PLUGIN ARCHITECTURE
# =============================================================================

@dataclass
class CipherResult:
    """Result from a cipher operation."""
    plaintext: str
    score: float
    cipher_name: str
    key_name: str
    mode: str
    details: Dict = field(default_factory=dict)

class BaseCipher(ABC):
    """Abstract base class for all cipher types."""
    
    name: str = "BaseCipher"
    
    @abstractmethod
    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray, mode: str = 'SUB') -> np.ndarray:
        """Decrypt ciphertext with given key."""
        pass
    
    @abstractmethod
    def get_modes(self) -> List[str]:
        """Return list of supported modes."""
        pass

class SubstitutionCipher(BaseCipher):
    """Vigenère-style substitution cipher."""
    
    name = "SUBSTITUTION"
    
    def get_modes(self) -> List[str]:
        return ['SUB', 'ADD', 'SUB_REV', 'ADD_REV', 'BEAUFORT', 'XOR']
    
    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray, mode: str = 'SUB') -> np.ndarray:
        n = len(ciphertext)
        key_len = len(key)
        extended_key = np.array([key[i % key_len] for i in range(n)])
        
        if mode == 'SUB':
            return (ciphertext - extended_key) % MOD
        elif mode == 'ADD':
            return (ciphertext + extended_key) % MOD
        elif mode == 'SUB_REV':
            return (extended_key - ciphertext) % MOD
        elif mode == 'ADD_REV':
            return (MOD - ciphertext - extended_key) % MOD
        elif mode == 'BEAUFORT':
            return (extended_key - ciphertext) % MOD
        elif mode == 'XOR':
            return ciphertext ^ extended_key
        else:
            return (ciphertext - extended_key) % MOD

class CaesarCipher(BaseCipher):
    """Simple shift cipher."""
    
    name = "CAESAR"
    
    def get_modes(self) -> List[str]:
        return ['SHIFT']
    
    def decrypt(self, ciphertext: np.ndarray, shift: int, mode: str = 'SHIFT') -> np.ndarray:
        return (ciphertext - shift) % MOD

class AtbashCipher(BaseCipher):
    """Atbash mirror cipher."""
    
    name = "ATBASH"
    
    def get_modes(self) -> List[str]:
        return ['MIRROR']
    
    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray = None, mode: str = 'MIRROR') -> np.ndarray:
        return (MOD - 1 - ciphertext) % MOD

class AffineCipher(BaseCipher):
    """Affine cipher: ax + b mod 29."""
    
    name = "AFFINE"
    
    def get_modes(self) -> List[str]:
        return ['AFFINE']
    
    def decrypt(self, ciphertext: np.ndarray, params: Tuple[int, int], mode: str = 'AFFINE') -> np.ndarray:
        a, b = params
        # Find modular inverse of a
        a_inv = pow(a, -1, MOD) if math.gcd(a, MOD) == 1 else None
        if a_inv is None:
            return ciphertext  # Invalid, return unchanged
        return (a_inv * (ciphertext - b)) % MOD

class HillCipher(BaseCipher):
    """Hill cipher with 2x2 matrix."""
    
    name = "HILL"
    
    def get_modes(self) -> List[str]:
        return ['2x2']
    
    def decrypt(self, ciphertext: np.ndarray, matrix: np.ndarray, mode: str = '2x2') -> np.ndarray:
        # Pad to even length
        if len(ciphertext) % 2 != 0:
            ciphertext = np.append(ciphertext, [0])
        
        # Matrix inverse mod 29
        det = int((matrix[0,0] * matrix[1,1] - matrix[0,1] * matrix[1,0]) % MOD)
        if math.gcd(det, MOD) != 1:
            return ciphertext[:len(ciphertext)]  # Invalid matrix
        
        det_inv = pow(det, -1, MOD)
        inv_matrix = np.array([
            [matrix[1,1], -matrix[0,1]],
            [-matrix[1,0], matrix[0,0]]
        ]) * det_inv % MOD
        
        # Decrypt in pairs
        result = []
        for i in range(0, len(ciphertext), 2):
            pair = np.array([ciphertext[i], ciphertext[i+1]])
            decrypted_pair = inv_matrix @ pair % MOD
            result.extend(decrypted_pair.astype(int))
        
        return np.array(result[:len(ciphertext)])

class RailFenceCipher(BaseCipher):
    """Rail fence transposition cipher."""
    
    name = "RAILFENCE"
    
    def get_modes(self) -> List[str]:
        return ['RAILS']
    
    def decrypt(self, ciphertext: np.ndarray, rails: int, mode: str = 'RAILS') -> np.ndarray:
        n = len(ciphertext)
        if rails < 2 or rails >= n:
            return ciphertext
        
        # Build pattern
        fence = [[None] * n for _ in range(rails)]
        rail = 0
        direction = 1
        for i in range(n):
            fence[rail][i] = True
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Fill in values
        idx = 0
        for r in range(rails):
            for c in range(n):
                if fence[r][c]:
                    fence[r][c] = int(ciphertext[idx])
                    idx += 1
        
        # Read off
        result = []
        rail = 0
        direction = 1
        for i in range(n):
            result.append(fence[rail][i])
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return np.array(result)

class AutokeyCipher(BaseCipher):
    """Autokey cipher using plaintext as key extension."""
    
    name = "AUTOKEY"
    
    def get_modes(self) -> List[str]:
        return ['PLAINTEXT', 'CIPHERTEXT']
    
    def decrypt(self, ciphertext: np.ndarray, primer: np.ndarray, mode: str = 'PLAINTEXT') -> np.ndarray:
        result = []
        key = list(primer)
        
        for i, c in enumerate(ciphertext):
            if i < len(key):
                k = key[i]
            else:
                if mode == 'PLAINTEXT':
                    k = result[i - len(primer)]
                else:  # CIPHERTEXT
                    k = ciphertext[i - len(primer)]
            
            p = (c - k) % MOD
            result.append(p)
        
        return np.array(result)

class ColumnarCipher(BaseCipher):
    """Columnar transposition cipher."""
    
    name = "COLUMNAR"
    
    def get_modes(self) -> List[str]:
        return ['COLUMNAR']
    
    def decrypt(self, ciphertext: np.ndarray, key_order: List[int], mode: str = 'COLUMNAR') -> np.ndarray:
        n = len(ciphertext)
        cols = len(key_order)
        rows = math.ceil(n / cols)
        
        # Calculate column lengths
        full_cols = n % cols if n % cols != 0 else cols
        col_lens = [rows if i < full_cols else rows - 1 for i in range(cols)]
        
        # Reorder columns
        sorted_order = sorted(range(cols), key=lambda x: key_order[x])
        
        # Read off
        grid = []
        pos = 0
        for col_idx in sorted_order:
            col_len = col_lens[col_idx]
            grid.append(list(ciphertext[pos:pos + col_len]))
            pos += col_len
        
        # Unsort
        unsorted_grid = [None] * cols
        for i, col_idx in enumerate(sorted_order):
            unsorted_grid[col_idx] = grid[i]
        
        # Read row by row
        result = []
        for row in range(rows):
            for col in range(cols):
                if row < len(unsorted_grid[col]):
                    result.append(unsorted_grid[col][row])
        
        return np.array(result[:n])

class PortaCipher(BaseCipher):
    """Porta cipher - reciprocal cipher with 13 alphabets."""
    
    name = "PORTA"
    
    def get_modes(self) -> List[str]:
        return ['PORTA']
    
    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray, mode: str = 'PORTA') -> np.ndarray:
        """Porta is reciprocal - encrypt = decrypt."""
        result = []
        key_len = len(key)
        half = MOD // 2  # 14 for mod 29
        
        for i, c in enumerate(ciphertext):
            k = key[i % key_len]
            tableau_row = k // 2  # Which of 14 tableaux to use
            
            if c < half:
                # First half: shift by tableau + half
                p = (c + tableau_row + half) % MOD
            else:
                # Second half: shift back
                p = (c - tableau_row - half) % MOD
            result.append(p)
        
        return np.array(result)

class GronsfeldCipher(BaseCipher):
    """Gronsfeld cipher - Vigenère variant using only digits 0-9."""
    
    name = "GRONSFELD"
    
    def get_modes(self) -> List[str]:
        return ['SUB', 'ADD']
    
    def decrypt(self, ciphertext: np.ndarray, digits: List[int], mode: str = 'SUB') -> np.ndarray:
        """Decrypt using digit key (each digit 0-9)."""
        result = []
        key_len = len(digits)
        
        for i, c in enumerate(ciphertext):
            d = digits[i % key_len] % 10  # Ensure 0-9
            if mode == 'SUB':
                p = (c - d) % MOD
            else:
                p = (c + d) % MOD
            result.append(p)
        
        return np.array(result)

class BifidCipher(BaseCipher):
    """Bifid cipher using Polybius square fractionation."""
    
    name = "BIFID"
    
    def get_modes(self) -> List[str]:
        return ['PERIOD_5', 'PERIOD_7', 'PERIOD_11', 'FULL']
    
    def decrypt(self, ciphertext: np.ndarray, period: int = 5, mode: str = 'PERIOD_5') -> np.ndarray:
        """Decrypt Bifid cipher."""
        n = len(ciphertext)
        
        # Use a 6x5 grid for 29 chars (close approximation)
        grid_size = 6  # 6x5 = 30 positions
        
        # Extract period from mode
        if mode == 'FULL':
            period = n
        elif mode.startswith('PERIOD_'):
            period = int(mode.split('_')[1])
        
        result = []
        
        # Process in periods
        for start in range(0, n, period):
            block = ciphertext[start:start + period]
            block_len = len(block)
            
            # Convert to row/col coordinates
            rows = [int(c) // grid_size for c in block]
            cols = [int(c) % grid_size for c in block]
            
            # Interleave (reverse of encryption)
            combined = rows + cols
            
            # De-interleave
            for i in range(block_len):
                r = combined[i]
                c = combined[i + block_len] if i + block_len < len(combined) else 0
                p = (r * grid_size + c) % MOD
                result.append(p)
        
        return np.array(result[:n])

class SkipCipher(BaseCipher):
    """Skip/Scytale cipher - read every nth character."""
    
    name = "SKIP"
    
    def get_modes(self) -> List[str]:
        return ['SKIP']
    
    def decrypt(self, ciphertext: np.ndarray, skip: int, mode: str = 'SKIP') -> np.ndarray:
        """Read every skip-th character."""
        n = len(ciphertext)
        if skip < 2 or skip >= n:
            return ciphertext
        
        result = [0] * n
        pos = 0
        for i, c in enumerate(ciphertext):
            result[(i * skip) % n] = c
            
        return np.array(result)

class ProgressiveKeyCipher(BaseCipher):
    """Progressive key cipher - key shifts with each position."""
    
    name = "PROGRESSIVE"
    
    def get_modes(self) -> List[str]:
        return ['LINEAR', 'QUADRATIC', 'FIBONACCI']
    
    def decrypt(self, ciphertext: np.ndarray, base_key: np.ndarray, mode: str = 'LINEAR') -> np.ndarray:
        """Decrypt with progressively shifting key."""
        result = []
        key_len = len(base_key)
        
        for i, c in enumerate(ciphertext):
            base_k = base_key[i % key_len]
            
            if mode == 'LINEAR':
                k = (base_k + i) % MOD
            elif mode == 'QUADRATIC':
                k = (base_k + i * i) % MOD
            elif mode == 'FIBONACCI':
                fib_shift = FIBONACCI[min(i, len(FIBONACCI) - 1)] if FIBONACCI else i
                k = (base_k + fib_shift) % MOD
            else:
                k = base_k
            
            p = (c - k) % MOD
            result.append(p)
        
        return np.array(result)

class InterruptedKeyCipher(BaseCipher):
    """Interrupted key cipher - key resets at certain positions."""
    
    name = "INTERRUPTED"
    
    def get_modes(self) -> List[str]:
        return ['PRIME_RESET', 'TOTIENT_RESET']
    
    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray, mode: str = 'PRIME_RESET') -> np.ndarray:
        """Decrypt with key that resets at special positions."""
        result = []
        key_len = len(key)
        key_pos = 0
        
        for i, c in enumerate(ciphertext):
            # Check if we should reset key position
            if mode == 'PRIME_RESET' and i in PRIME_SET:
                key_pos = 0
            elif mode == 'TOTIENT_RESET' and i < len(TOTIENTS) and TOTIENTS[i] == i - 1:
                key_pos = 0  # Reset at primes (φ(p) = p-1)
            
            k = key[key_pos % key_len]
            p = (c - k) % MOD
            result.append(p)
            key_pos += 1
        
        return np.array(result)

class RunningKeyCipher(BaseCipher):
    """Running key cipher using text as key."""
    
    name = "RUNNING_KEY"
    
    def get_modes(self) -> List[str]:
        return ['SUB', 'ADD']
    
    def decrypt(self, ciphertext: np.ndarray, running_text: np.ndarray, mode: str = 'SUB') -> np.ndarray:
        """Decrypt using running key text."""
        result = []
        key_len = len(running_text)
        
        for i, c in enumerate(ciphertext):
            k = running_text[i % key_len]
            if mode == 'SUB':
                p = (c - k) % MOD
            else:
                p = (c + k) % MOD
            result.append(p)
        
        return np.array(result)

# Global for interrupted key cipher
PRIME_SET = set(PRIMES[:500])

# =============================================================================
# CIPHER REGISTRY
# =============================================================================

CIPHER_REGISTRY: Dict[str, BaseCipher] = {
    'SUBSTITUTION': SubstitutionCipher(),
    'CAESAR': CaesarCipher(),
    'ATBASH': AtbashCipher(),
    'AFFINE': AffineCipher(),
    'HILL': HillCipher(),
    'RAILFENCE': RailFenceCipher(),
    'AUTOKEY': AutokeyCipher(),
    'COLUMNAR': ColumnarCipher(),
    'PORTA': PortaCipher(),
    'GRONSFELD': GronsfeldCipher(),
    'BIFID': BifidCipher(),
    'SKIP': SkipCipher(),
    'PROGRESSIVE': ProgressiveKeyCipher(),
    'INTERRUPTED': InterruptedKeyCipher(),
    'RUNNING_KEY': RunningKeyCipher(),
}

# =============================================================================
# MULTI-LAYER CIPHER CHAINS
# =============================================================================

@dataclass
class CipherChain:
    """Represents a chain of ciphers to apply in sequence."""
    name: str
    steps: List[Tuple[str, Any, str]]  # (cipher_name, key/params, mode)

def create_cipher_chains() -> List[CipherChain]:
    """Generate multi-layer cipher chains to test."""
    chains = []
    
    # Caesar + Vigenère combinations
    for shift in range(1, 29):
        for keyword in ['DIVINITY', 'PRIMES', 'TOTIENT', 'CICADA']:
            key = text_to_key(keyword)
            chains.append(CipherChain(
                name=f"CAESAR_{shift}+VIG_{keyword}",
                steps=[
                    ('CAESAR', shift, 'SHIFT'),
                    ('SUBSTITUTION', key, 'SUB')
                ]
            ))
    
    # Atbash + Vigenère
    for keyword in ['DIVINITY', 'PRIMES', 'WISDOM', 'CICADA', 'LIBER']:
        key = text_to_key(keyword)
        chains.append(CipherChain(
            name=f"ATBASH+VIG_{keyword}",
            steps=[
                ('ATBASH', None, 'MIRROR'),
                ('SUBSTITUTION', key, 'SUB')
            ]
        ))
    
    # Vigenère + Atbash
    for keyword in ['DIVINITY', 'PRIMES', 'WISDOM']:
        key = text_to_key(keyword)
        chains.append(CipherChain(
            name=f"VIG_{keyword}+ATBASH",
            steps=[
                ('SUBSTITUTION', key, 'SUB'),
                ('ATBASH', None, 'MIRROR')
            ]
        ))
        
    # Porta Chains
    for keyword in ['ABYSS', 'CICADA', 'TYRANT', 'DESTINY']:
        key = text_to_key(keyword)
        chains.append(CipherChain(
            name=f"PORTA_{keyword}",
            steps=[('PORTA', key, 'PORTA')]
        ))
        # Porta + Caesar
        for shift in [3, 11, 19]:
            chains.append(CipherChain(
                name=f"PORTA_{keyword}+CAESAR_{shift}",
                steps=[
                    ('PORTA', key, 'PORTA'),
                    ('CAESAR', shift, 'SHIFT')
                ]
            ))

    # Gronsfeld Chains using Primes/Phi
    prime_digits = list(map(int, list("2357111317192329313741434753596167717379838997")))
    phi_digits_list = list(map(int, list("16180339887498948482045868343656381177203091798057")))
    
    chains.append(CipherChain(name="GRONSFELD_PRIMES", steps=[('GRONSFELD', prime_digits, 'SUB')]))
    chains.append(CipherChain(name="GRONSFELD_PHI", steps=[('GRONSFELD', phi_digits_list, 'SUB')]))
    
    # Bifid Chains
    for period in [5, 7, 9]:
        chains.append(CipherChain(name=f"BIFID_P{period}", steps=[('BIFID', period, f'PERIOD_{period}')]))
    
    # Double Vigenère with different keys
    key_pairs = [
        ('DIVINITY', 'CIRCUMFERENCE'),
        ('PRIMES', 'TOTIENT'),
        ('CICADA', 'LIBER'),
        ('WISDOM', 'KNOWLEDGE'),
    ]
    for k1, k2 in key_pairs:
        chains.append(CipherChain(
            name=f"VIG_{k1}+VIG_{k2}",
            steps=[
                ('SUBSTITUTION', text_to_key(k1), 'SUB'),
                ('SUBSTITUTION', text_to_key(k2), 'SUB')
            ]
        ))
    
    # Reverse + Caesar + Vigenère (triple layer)
    for shift in [3, 7, 11, 13]:
        for keyword in ['DIVINITY', 'PRIMES']:
            chains.append(CipherChain(
                name=f"REV+CAESAR_{shift}+VIG_{keyword}",
                steps=[
                    ('REVERSE', None, 'REVERSE'),
                    ('CAESAR', shift, 'SHIFT'),
                    ('SUBSTITUTION', text_to_key(keyword), 'SUB')
                ]
            ))
    
    # Rail fence + Vigenère
    for rails in [2, 3, 4, 5]:
        for keyword in ['DIVINITY', 'CICADA']:
            chains.append(CipherChain(
                name=f"RAIL_{rails}+VIG_{keyword}",
                steps=[
                    ('RAILFENCE', rails, 'RAILS'),
                    ('SUBSTITUTION', text_to_key(keyword), 'SUB')
                ]
            ))
    
    return chains

# =============================================================================
# KEY GENERATION
# =============================================================================

CICADA_KEYWORDS = [
    'DIVINITY', 'CIRCUMFERENCE', 'CONSUMPTION', 'PRESERVATION', 'ENLIGHTENMENT',
    'EMERGENCE', 'INTERCONNECTEDNESS', 'TOTIENT', 'PRIMES', 'SACRED', 'WISDOM',
    'KOAN', 'PARABLE', 'INSTRUCTION', 'WARNING', 'WELCOME', 'PILGRIM', 'JOURNEY',
    'INSTAR', 'INTUS', 'CICADA', 'LIBER', 'PRIMUS', 'FAITH', 'TRUTH', 'BELIEF',
    'EMERSON', 'SELFRELIANCE', 'CONSCIOUSNESS', 'AWARENESS', 'KNOWLEDGE',
    'GEMATRIA', 'RUNES', 'CIPHER', 'CODE', 'KEY', 'FIBONACCI', 'LUCAS',
    'PRIME', 'VOID', 'CHAOS', 'ORDER', 'BALANCE', 'HARMONY',
]

def text_to_key(text: str) -> List[int]:
    """Convert text to key values."""
    text = text.upper().replace(' ', '')
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_INDEX:
                result.append(LATIN_TO_INDEX[digraph])
                i += 2
                continue
        if text[i] in LATIN_TO_INDEX:
            result.append(LATIN_TO_INDEX[text[i]])
        i += 1
    return result

def generate_master_keys(max_len: int = 200) -> Dict[str, List[int]]:
    """Generate comprehensive key dictionary."""
    keys = {}
    
    # Caesar shifts
    for shift in range(29):
        keys[f'CAESAR_{shift}'] = [shift]
    
    # Prime sequences
    for start in range(0, 200, 10):
        for length in [20, 50, 100]:
            seq = [p % MOD for p in PRIMES[start:start+length]]
            if seq:
                keys[f'PRIMES_S{start}_L{length}'] = seq
                keys[f'PRIMES_S{start}_L{length}_REVERSED'] = seq[::-1]
    
    # Totient sequences
    for start in range(0, 200, 10):
        seq = [t % MOD for t in TOTIENTS[start:start+100] if start+100 <= len(TOTIENTS)]
        if seq:
            keys[f'TOTIENT_S{start}'] = seq
    
    # Fibonacci
    seq = [f % MOD for f in FIBONACCI[:100]]
    keys['FIBONACCI'] = seq
    keys['FIBONACCI_REVERSED'] = seq[::-1]
    
    # Lucas
    seq = [l % MOD for l in LUCAS[:100]]
    keys['LUCAS'] = seq
    keys['LUCAS_REVERSED'] = seq[::-1]
    
    # Tribonacci
    seq = [t % MOD for t in TRIBONACCI[:100]]
    keys['TRIBONACCI'] = seq
    
    # Pell
    seq = [p % MOD for p in PELL[:100]]
    keys['PELL'] = seq
    
    # Mathematical constants
    keys['PI'] = [d % MOD for d in PI_DIGITS]
    keys['E'] = [d % MOD for d in E_DIGITS]
    keys['PHI'] = [d % MOD for d in PHI_DIGITS]
    keys['SQRT2'] = [d % MOD for d in SQRT2_DIGITS]
    
    # PHI as prime indices (the key that partially solved Page 55!)
    # We expand this since it was successful
    for start in range(0, 50, 5):
        length = 50
        indices = PHI_DIGITS[start:start+length]
        if len(indices) == length:
            key_seq = []
            valid = True
            for d in indices:
                if d < len(PRIMES):
                    key_seq.append(PRIMES[d] % MOD)
                else:
                    valid = False
                    break
            if valid:
                keys[f'PHI_PRIME_S{start}'] = key_seq
                keys[f'PHI_PRIME_S{start}_REVERSED'] = key_seq[::-1]

    # Similar logic for PI and E with prime indices
    for const_name, digits in [('PI', PI_DIGITS), ('E', E_DIGITS)]:
        for start in range(0, 50, 10):
            indices = digits[start:start+50]
            if len(indices) == 50:
                key_seq = [PRIMES[d] % MOD for d in indices if d < len(PRIMES)]
                if len(key_seq) == 50: # Only if all valid
                    keys[f'{const_name}_PRIME_S{start}'] = key_seq

    # Gematria primes
    gematria_primes = [v[2] for v in GEMATRIA.values()]
    keys['GEMATRIA_PRIMES'] = [p % MOD for p in gematria_primes]
    keys['GEMATRIA_PRIMES_REVERSED'] = [p % MOD for p in gematria_primes[::-1]]
    
    # Cicada keywords
    for word in CICADA_KEYWORDS:
        key = text_to_key(word)
        if key:
            keys[f'WORD_{word}'] = key
            keys[f'WORD_{word}_REVERSED'] = key[::-1]
            # Shifted versions
            for shift in [1, 2, 3, 7, 11, 13, 17, 19, 23]:
                keys[f'WORD_{word}+{shift}'] = [(k + shift) % MOD for k in key]
                keys[f'WORD_{word}+{shift}_REVERSED'] = [(k + shift) % MOD for k in key[::-1]]
    
    # Emerson Self-Reliance Running Key
    try:
        emerson_path = os.path.join(os.path.dirname(__file__), 'emerson_self_reliance.txt')
        if os.path.exists(emerson_path):
            with open(emerson_path, 'r', encoding='utf-8') as f:
                emerson_text = f.read()
            emerson_key = text_to_key(emerson_text)
            if emerson_key:
                # Store full key, and also chunks
                keys['EMERSON_FULL'] = emerson_key
                # Create chunks of length 100
                for i in range(0, min(len(emerson_key), 1000), 100):
                    keys[f'EMERSON_CHUNK_{i}'] = emerson_key[i:i+100]
    except Exception as e:
        print(f"Warning: Could not load Emerson key: {e}")

    # Affine parameters (a, b) where gcd(a, 29) = 1
    valid_a = [a for a in range(1, 29) if math.gcd(a, 29) == 1]
    for a in valid_a:
        for b in range(29):
            keys[f'AFFINE_{a}_{b}'] = [a, b]
            keys[f'AFFINE_{a}_{b}_REVERSED'] = [a, (29 - b) % 29]
    
    # Random exploration
    np.random.seed(3301)  # Deterministic
    for i in range(100):
        keys[f'RANDOM_{i}'] = list(np.random.randint(0, 29, size=50))
        keys[f'RANDOM_{i}_REVERSED'] = list(np.random.randint(0, 29, size=50))[::-1]
    
    return keys

# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

# English bigram frequencies (log probabilities)
ENGLISH_BIGRAMS = {
    'TH': 15, 'HE': 12, 'IN': 11, 'ER': 10, 'AN': 10, 'RE': 9, 'ON': 9,
    'AT': 8, 'EN': 8, 'ND': 8, 'TI': 8, 'ES': 8, 'OR': 8, 'TE': 7,
    'OF': 7, 'ED': 7, 'IS': 7, 'IT': 7, 'AL': 7, 'AR': 7, 'ST': 7,
    'TO': 7, 'NT': 7, 'NG': 6, 'SE': 6, 'HA': 6, 'AS': 6, 'OU': 6,
    'IO': 6, 'LE': 6, 'VE': 6, 'CO': 6, 'ME': 6, 'DE': 5, 'HI': 5,
    'RI': 5, 'RO': 5, 'IC': 5, 'NE': 5, 'EA': 5, 'RA': 5, 'CE': 5,
}

ENGLISH_TRIGRAMS = {
    'THE': 20, 'AND': 15, 'ING': 12, 'ION': 10, 'TIO': 10, 'ENT': 9,
    'ERE': 8, 'HER': 8, 'ATE': 8, 'VER': 7, 'TER': 7, 'THA': 7,
    'ATI': 7, 'FOR': 7, 'HAT': 7, 'ERS': 6, 'HIS': 6, 'RES': 6,
    'ILL': 6, 'ARE': 6, 'CON': 6, 'NCE': 6, 'ALL': 6, 'EVE': 6,
    'ITH': 6, 'TED': 5, 'AIN': 5, 'EST': 5, 'MAN': 5, 'RED': 5,
}

COMMON_WORDS = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAS', 'HIS', 'HIM', 'HOW', 'ITS',
    'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'DID', 'GET', 'LET',
    'SAY', 'SHE', 'TOO', 'USE', 'THAT', 'WITH', 'HAVE', 'THIS', 'WILL',
    'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'EACH', 'FIND', 'LONG', 'DOWN',
    'INTO', 'JUST', 'KNOW', 'MADE', 'MAKE', 'OVER', 'SUCH', 'TIME', 'VERY',
    'WHEN', 'WHAT', 'WHICH', 'THEIR', 'ABOUT', 'COULD', 'OTHER', 'THERE',
    'WOULD', 'FIRST', 'THESE', 'THINK', 'BEING', 'EVERY', 'WHERE',
}

CICADA_PHRASES = [
    'AN END', 'WITHIN THE', 'DEEP WEB', 'THERE EXISTS', 'A PAGE',
    'BELIEVE NOTHING', 'A WARNING', 'SOME WISDOM', 'THE PRIMES',
    'DIVINITY', 'CIRCUMFERENCE', 'CONSUMPTION', 'PRESERVATION',
    'LOSS OF DIVINITY', 'PILGRIM', 'WELCOME', 'THE FIRST',
    'INSTRUCTION', 'PARABLE', 'KOAN', 'SACRED', 'TRUTH',
]

def indices_to_text(indices: np.ndarray) -> str:
    """Convert index array to Latin text."""
    return ''.join(INDEX_TO_LATIN.get(int(i), '?') for i in indices)

def score_plaintext(text: str) -> float:
    """Score plaintext for English-likeness."""
    if not text:
        return 0.0
    
    text = text.upper()
    score = 0.0
    
    # Bigram scoring
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in ENGLISH_BIGRAMS:
            score += ENGLISH_BIGRAMS[bigram]
    
    # Trigram scoring
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in ENGLISH_TRIGRAMS:
            score += ENGLISH_TRIGRAMS[trigram] * 1.5
    
    # Word matching
    for word in COMMON_WORDS:
        if word in text:
            score += len(word) * 3
    
    # Cicada phrase matching (high bonus)
    for phrase in CICADA_PHRASES:
        if phrase.replace(' ', '') in text:
            score += 50
    
    # Vowel ratio
    vowels = sum(1 for c in text if c in 'AEIOU')
    ratio = vowels / max(len(text), 1)
    if 0.25 <= ratio <= 0.45:
        score += 20
    
    # Penalize long consonant clusters
    consonant_run = 0
    max_consonant = 0
    for c in text:
        if c not in 'AEIOU':
            consonant_run += 1
            max_consonant = max(max_consonant, consonant_run)
        else:
            consonant_run = 0
    if max_consonant > 5:
        score -= max_consonant * 2
    
    return score

# =============================================================================
# GPU WORKER CLASS
# =============================================================================

class GPUWorker:
    """Worker process for a single GPU."""
    
    def __init__(self, gpu_id: int, keys: Dict[str, List[int]], chains: List[CipherChain]):
        self.gpu_id = gpu_id
        self.keys = keys
        self.chains = chains
        self.substitution = SubstitutionCipher()
        self.caesar = CaesarCipher()
        self.atbash = AtbashCipher()
        self.affine = AffineCipher()
    
    def set_gpu(self):
        """Set this process to use specific GPU."""
        cuda.Device(self.gpu_id).use()
    
    def attack_page(self, rune_indices: np.ndarray, page_num: int) -> List[CipherResult]:
        """Run all attacks on a single page."""
        self.set_gpu()
        results = []
        
        # Convert to CuPy array
        ct_gpu = cp.array(rune_indices)
        
        # === PHASE 1: Single-layer attacks ===
        
        # Caesar shifts
        for shift in range(29):
            pt_gpu = (ct_gpu - shift) % MOD
            pt = cp.asnumpy(pt_gpu)
            text = indices_to_text(pt)
            score = score_plaintext(text)
            if score > 500:
                results.append(CipherResult(text[:100], score, 'CAESAR', f'SHIFT_{shift}', 'SHIFT'))
        
        # Atbash
        pt_gpu = (MOD - 1 - ct_gpu) % MOD
        pt = cp.asnumpy(pt_gpu)
        text = indices_to_text(pt)
        score = score_plaintext(text)
        if score > 500:
            results.append(CipherResult(text[:100], score, 'ATBASH', 'MIRROR', 'MIRROR'))
        
        # Vigenère with all keys
        for key_name, key in self.keys.items():
            if key_name.startswith('AFFINE_'):
                continue  # Handle separately
            
            key_gpu = cp.array(key)
            n = len(ct_gpu)
            key_len = len(key_gpu)
            ext_key = cp.array([key[i % key_len] for i in range(n)])
            
            for mode in ['SUB', 'ADD', 'SUB_REV', 'ADD_REV', 'BEAUFORT', 'XOR']:
                if mode == 'SUB':
                    pt_gpu = (ct_gpu - ext_key) % MOD
                elif mode == 'ADD':
                    pt_gpu = (ct_gpu + ext_key) % MOD
                elif mode == 'SUB_REV':
                    pt_gpu = (ext_key - ct_gpu) % MOD
                elif mode == 'ADD_REV':
                    pt_gpu = (MOD - ct_gpu - ext_key) % MOD
                elif mode == 'BEAUFORT':
                    pt_gpu = (ext_key - ct_gpu) % MOD
                elif mode == 'XOR':
                    pt_gpu = ct_gpu ^ ext_key
                
                pt = cp.asnumpy(pt_gpu)
                text = indices_to_text(pt)
                score = score_plaintext(text)
                if score > 500:
                    results.append(CipherResult(text[:100], score, 'VIGENERE', key_name, mode))
        
        # Affine cipher
        valid_a = [a for a in range(1, 29) if math.gcd(a, 29) == 1]
        for a in valid_a:
            a_inv = pow(a, -1, MOD)
            for b in range(29):
                pt_gpu = (a_inv * (ct_gpu - b)) % MOD
                pt = cp.asnumpy(pt_gpu)
                text = indices_to_text(pt)
                score = score_plaintext(text)
                if score > 500:
                    results.append(CipherResult(text[:100], score, 'AFFINE', f'a={a},b={b}', 'AFFINE'))
        
        # === PHASE 2: Multi-layer attacks ===
        for chain in self.chains:
            current = ct_gpu.copy()
            
            try:
                for cipher_name, params, mode in chain.steps:
                    if cipher_name == 'CAESAR':
                        current = (current - params) % MOD
                    elif cipher_name == 'ATBASH':
                        current = (MOD - 1 - current) % MOD
                    elif cipher_name == 'REVERSE':
                        current = current[::-1]
                    elif cipher_name == 'SUBSTITUTION':
                        key_gpu = cp.array(params)
                        n = len(current)
                        key_len = len(key_gpu)
                        ext_key = cp.array([params[i % key_len] for i in range(n)])
                        if mode == 'SUB':
                            current = (current - ext_key) % MOD
                        elif mode == 'ADD':
                            current = (current + ext_key) % MOD
                    elif cipher_name == 'RAILFENCE':
                        # Handle on CPU for complexity
                        current_np = cp.asnumpy(current)
                        rf = RailFenceCipher()
                        current_np = rf.decrypt(current_np, params, 'RAILS')
                        current = cp.array(current_np)
                    elif cipher_name in CIPHER_REGISTRY:
                        # Fallback for other ciphers (PORTA, GRONSFELD, BIFID, etc)
                        # We use CPU implementation via CIPHER_REGISTRY
                        current_np = cp.asnumpy(current)
                        cipher_obj = CIPHER_REGISTRY[cipher_name]
                        current_np = cipher_obj.decrypt(current_np, params, mode)
                        current = cp.array(current_np)
                
                pt = cp.asnumpy(current)
                text = indices_to_text(pt)
                score = score_plaintext(text)
                if score > 500:
                    results.append(CipherResult(text[:100], score, 'CHAIN', chain.name, 'MULTI'))
            
            except Exception as e:
                continue  # Skip failed chains
        
        # === PHASE 3: Reversed ciphertext ===
        ct_rev = ct_gpu[::-1]
        
        # Caesar on reversed
        for shift in range(29):
            pt_gpu = (ct_rev - shift) % MOD
            pt = cp.asnumpy(pt_gpu)
            text = indices_to_text(pt)
            score = score_plaintext(text)
            if score > 500:
                results.append(CipherResult(text[:100], score, 'CAESAR_REV', f'SHIFT_{shift}', 'REV'))
        
        # Top keys on reversed
        for key_name in ['PHI_PRIME_S0', 'WORD_DIVINITY', 'PRIMES_S0_L50']:
            if key_name in self.keys:
                key = self.keys[key_name]
                key_gpu = cp.array(key)
                n = len(ct_rev)
                key_len = len(key_gpu)
                ext_key = cp.array([key[i % key_len] for i in range(n)])
                
                for mode in ['SUB', 'ADD']:
                    if mode == 'SUB':
                        pt_gpu = (ct_rev - ext_key) % MOD
                    else:
                        pt_gpu = (ct_rev + ext_key) % MOD
                    
                    pt = cp.asnumpy(pt_gpu)
                    text = indices_to_text(pt)
                    score = score_plaintext(text)
                    if score > 500:
                        results.append(CipherResult(text[:100], score, 'VIGENERE_REV', key_name, f'{mode}_REV'))
        
        return sorted(results, key=lambda x: -x.score)[:10]

# =============================================================================
# WORK QUEUE SYSTEM
# =============================================================================

def gpu_worker_process(gpu_id: int, page_queue: Queue, result_queue: Queue, 
                       keys: Dict, chains: List[CipherChain], pages_dir: Path):
    """Worker process for GPU."""
    worker = GPUWorker(gpu_id, keys, chains)
    worker.set_gpu()
    
    while True:
        try:
            page_num = page_queue.get(timeout=1)
            if page_num is None:  # Poison pill
                break
            
            # Load page
            page_dir = pages_dir / f"page_{page_num:02d}"
            runes_file = page_dir / "runes.txt"
            
            if not runes_file.exists():
                result_queue.put((page_num, []))
                continue
            
            with open(runes_file, 'r', encoding='utf-8') as f:
                runes = f.read().strip()
            
            rune_indices = np.array([RUNE_TO_INDEX.get(r, 0) for r in runes if r in RUNE_TO_INDEX])
            
            if len(rune_indices) < 5:
                result_queue.put((page_num, []))
                continue
            
            # Attack
            start = time.time()
            results = worker.attack_page(rune_indices, page_num)
            elapsed = time.time() - start
            
            print(f"[GPU {gpu_id}] Page {page_num:02d}: {len(results)} results in {elapsed:.1f}s")
            result_queue.put((page_num, results))
            
        except queue.Empty:
            continue
        except Exception as e:
            print(f"[GPU {gpu_id}] Error: {e}")
            continue

# =============================================================================
# MAIN ATTACK ORCHESTRATOR
# =============================================================================

class MasterCipherAttack:
    """Orchestrates the full attack across multiple GPUs."""
    
    def __init__(self, pages_dir: Path, output_file: Path):
        self.pages_dir = pages_dir
        self.output_file = output_file
        self.keys = generate_master_keys()
        self.chains = create_cipher_chains()
        self.results = {}
        
        print(f"[KEYGEN] Generated {len(self.keys)} keys")
        print(f"[CHAINS] Generated {len(self.chains)} multi-layer chains")
    
    def get_pages_to_attack(self, page_spec: str) -> List[int]:
        """Parse page specification."""
        if page_spec == 'all':
            return list(range(0, 75))
        elif page_spec == 'unsolved':
            # Pages known to be unsolved
            unsolved = [2] + list(range(17, 55)) + [55, 58, 60, 61, 62, 65, 66, 67, 69, 70, 71, 72]
            return [p for p in unsolved if (self.pages_dir / f"page_{p:02d}" / "runes.txt").exists()]
        else:
            return [int(p) for p in page_spec.split(',')]
    
    def run_attack(self, pages: List[int], num_gpus: int = None):
        """Run attack with GPU work queue."""
        if num_gpus is None:
            num_gpus = min(GPU_COUNT, 2)
        
        print(f"\n{'='*70}")
        print(f"MASTER CIPHER ATTACK - {len(pages)} pages on {num_gpus} GPU(s)")
        print(f"{'='*70}")
        print(f"Keys: {len(self.keys)}")
        print(f"Chains: {len(self.chains)}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        # Create queues
        page_queue = Queue()
        result_queue = Queue()
        
        # Add pages to queue
        for page in pages:
            page_queue.put(page)
        
        # Add poison pills
        for _ in range(num_gpus):
            page_queue.put(None)
        
        # Start worker processes
        workers = []
        for gpu_id in range(num_gpus):
            p = Process(target=gpu_worker_process, args=(
                gpu_id, page_queue, result_queue, self.keys, self.chains, self.pages_dir
            ))
            p.start()
            workers.append(p)
        
        # Collect results
        results_collected = 0
        while results_collected < len(pages):
            try:
                page_num, page_results = result_queue.get(timeout=300)
                self.results[page_num] = page_results
                results_collected += 1
                print(f"[PROGRESS] {results_collected}/{len(pages)} pages complete")
            except queue.Empty:
                print("[WARNING] Timeout waiting for results")
                break
        
        # Wait for workers
        for p in workers:
            p.join(timeout=10)
        
        elapsed = time.time() - start_time
        print(f"\n[COMPLETE] Attack finished in {elapsed:.1f}s ({elapsed/60:.1f} min)")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save results to markdown and JSON."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("# MASTER CIPHER ATTACK RESULTS\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**GPUs:** {GPU_COUNT}\n")
            f.write(f"**Keys:** {len(self.keys)}\n")
            f.write(f"**Chains:** {len(self.chains)}\n\n")
            
            f.write("---\n\n## Summary\n\n")
            f.write("| Page | Score | Cipher | Key | Mode | Preview |\n")
            f.write("|------|-------|--------|-----|------|--------|\n")
            
            for page_num in sorted(self.results.keys()):
                results = self.results[page_num]
                if results:
                    best = results[0]
                    preview = best.plaintext[:50].replace('|', '\\|')
                    f.write(f"| {page_num:02d} | {best.score:.1f} | {best.cipher_name} | `{best.key_name}` | {best.mode} | {preview}... |\n")
                else:
                    f.write(f"| {page_num:02d} | - | - | - | - | No results |\n")
            
            f.write("\n---\n\n## Details\n\n")
            
            for page_num in sorted(self.results.keys()):
                results = self.results[page_num]
                f.write(f"### Page {page_num:02d}\n\n")
                
                if not results:
                    f.write("No results above threshold.\n\n")
                    continue
                
                for i, r in enumerate(results[:5], 1):
                    f.write(f"**{i}. Score: {r.score:.1f}** | Cipher: `{r.cipher_name}` | Key: `{r.key_name}` | Mode: {r.mode}\n")
                    f.write(f"```\n{r.plaintext}\n```\n\n")
        
        # JSON output
        json_file = self.output_file.with_suffix('.json')
        json_data = {}
        for page_num, results in self.results.items():
            json_data[str(page_num)] = [
                {
                    'plaintext': r.plaintext,
                    'score': r.score,
                    'cipher': r.cipher_name,
                    'key': r.key_name,
                    'mode': r.mode
                }
                for r in results
            ]
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"[SAVED] {self.output_file}")
        print(f"[SAVED] {json_file}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Master Cipher Attack')
    parser.add_argument('--pages', type=str, default='unsolved',
                        help='Pages to attack: all, unsolved, or comma-separated list')
    parser.add_argument('--gpus', type=int, default=None,
                        help='Number of GPUs to use')
    parser.add_argument('--output', type=str, default='MASTER_RESULTS.md',
                        help='Output file')
    
    args = parser.parse_args()
    
    pages_dir = Path(__file__).parent.parent / 'pages'
    output_file = Path(__file__).parent / args.output
    
    attack = MasterCipherAttack(pages_dir, output_file)
    pages = attack.get_pages_to_attack(args.pages)
    
    print(f"[PAGES] Attacking: {pages}")
    attack.run_attack(pages, args.gpus)

if __name__ == '__main__':
    main()

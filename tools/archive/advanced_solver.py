# -*- coding: utf-8 -*-
"""
Advanced Liber Primus Solver
Tests multiple cipher methods with intelligent scoring
"""

import itertools as it
from collections import Counter
import re

# =============================================================================
# GEMATRIA PRIMUS
# =============================================================================

GEMATRIA = (
    ('ᚠ', 'f', 2), ('ᚢ', 'u', 3), ('ᚦ', 'th', 5), ('ᚩ', 'o', 7),
    ('ᚱ', 'r', 11), ('ᚳ', 'c', 13), ('ᚷ', 'g', 17), ('ᚹ', 'w', 19),
    ('ᚻ', 'h', 23), ('ᚾ', 'n', 29), ('ᛁ', 'i', 31), ('ᛂ', 'j', 37),
    ('ᛇ', 'eo', 41), ('ᛈ', 'p', 43), ('ᛉ', 'x', 47), ('ᛋ', 's', 53),
    ('ᛏ', 't', 59), ('ᛒ', 'b', 61), ('ᛖ', 'e', 67), ('ᛗ', 'm', 71),
    ('ᛚ', 'l', 73), ('ᛝ', 'ing', 79), ('ᛟ', 'oe', 83), ('ᛞ', 'd', 89),
    ('ᚪ', 'a', 97), ('ᚫ', 'ae', 101), ('ᚣ', 'y', 103), ('ᛡ', 'io', 107),
    ('ᛠ', 'ea', 109)
)

RUNES = [x[0] for x in GEMATRIA]
LETTERS = [x[1] for x in GEMATRIA]
PRIMES = [x[2] for x in GEMATRIA]
ALPHABET_SIZE = 29

# =============================================================================
# PRIME UTILITIES
# =============================================================================

def prime_generator():
    D = {}
    yield 2
    for q in it.islice(it.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D:
                x += 2*p
            D[x] = p

def get_first_n_primes(n):
    gen = prime_generator()
    return [next(gen) for _ in range(n)]

# Pre-generate first 1000 primes
FIRST_1000_PRIMES = get_first_n_primes(1000)

# Fibonacci sequence
def fibonacci(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:n]

FIRST_1000_FIBS = fibonacci(1000)

# =============================================================================
# BASIC OPERATIONS
# =============================================================================

def shift(idx, amount):
    return (idx + amount) % ALPHABET_SIZE

def transliterate(text):
    result = ''
    for c in text:
        if c == '•':
            result += ' '
        elif c in RUNES:
            result += LETTERS[RUNES.index(c)]
        else:
            result += c
    return result

def runes_only(text):
    return [c for c in text if c in RUNES]

# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

# Common English words weighted by frequency
COMMON_WORDS = {
    'the': 5, 'and': 4, 'of': 4, 'to': 3, 'a': 2, 'in': 3, 'is': 3,
    'it': 2, 'that': 3, 'was': 2, 'for': 2, 'on': 2, 'are': 2, 'with': 2,
    'as': 2, 'be': 2, 'at': 2, 'this': 2, 'have': 2, 'from': 2,
    'or': 1, 'one': 1, 'by': 1, 'but': 1, 'not': 1, 'what': 1, 'all': 1,
    'were': 1, 'we': 2, 'when': 1, 'your': 1, 'can': 1, 'an': 2,
    # Cicada specific
    'within': 3, 'instar': 4, 'emerge': 3, 'divinity': 3, 'wisdom': 3,
    'truth': 3, 'prime': 3, 'cicada': 4, 'seek': 2, 'find': 2, 'path': 2,
    'deep': 2, 'web': 2, 'page': 2, 'instruction': 3, 'command': 2,
    'you': 2, 'must': 2, 'our': 2, 'who': 2, 'are': 2
}

# Bad patterns that indicate failed decryption
BAD_PATTERNS = ['xxx', 'qqq', 'zzz', 'jjj', 'xeo', 'eox', 'inginging']

# English bigram frequencies (normalized)
COMMON_BIGRAMS = {'th', 'he', 'in', 'er', 'an', 'en', 'on', 'at', 're', 'ed',
                  'nd', 'to', 'or', 'ea', 'ti', 'es', 'ng', 'of', 'al', 'de',
                  'se', 'le', 'sa', 'si', 'ar', 'te', 'is', 'ou', 'me', 'ne'}

def score_english(text):
    """Score how English-like a text appears. Higher = better."""
    text_lower = text.lower()
    score = 0
    
    # Word matching
    words = re.findall(r'[a-z]+', text_lower)
    for word in words:
        if word in COMMON_WORDS:
            score += COMMON_WORDS[word] * 10
    
    # Bigram analysis
    for i in range(len(text_lower) - 1):
        bigram = text_lower[i:i+2]
        if bigram.isalpha() and bigram in COMMON_BIGRAMS:
            score += 1
    
    # Penalize bad patterns
    for pattern in BAD_PATTERNS:
        if pattern in text_lower:
            score -= 20
    
    # Reward spaces followed by common word starters
    space_positions = [i for i, c in enumerate(text_lower) if c == ' ']
    for pos in space_positions:
        if pos + 1 < len(text_lower):
            next_char = text_lower[pos + 1]
            if next_char in 'taoiswbhfm':  # Common word starters
                score += 2
    
    return score

# =============================================================================
# DECRYPTION METHODS
# =============================================================================

def decrypt_caesar(text, shift_val):
    """Simple Caesar shift"""
    result = []
    for c in text:
        if c in RUNES:
            idx = RUNES.index(c)
            result.append(LETTERS[shift(idx, -shift_val)])
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

def decrypt_prime_shift(text, offset=0, direction=-1, start_prime_idx=0):
    """
    Shift by -(prime_n + offset) for each rune
    This is the Page 56 method when offset=57
    """
    result = []
    prime_idx = start_prime_idx
    
    for c in text:
        if c in RUNES:
            idx = RUNES.index(c)
            prime = FIRST_1000_PRIMES[prime_idx] if prime_idx < 1000 else prime_idx * 2
            new_idx = shift(idx, direction * (prime + offset))
            result.append(LETTERS[new_idx])
            prime_idx += 1
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

def decrypt_vigenere(text, key):
    """Vigenère cipher with numeric key"""
    result = []
    key_len = len(key)
    rune_count = 0
    
    for c in text:
        if c in RUNES:
            idx = RUNES.index(c)
            shift_val = key[rune_count % key_len]
            result.append(LETTERS[shift(idx, -shift_val)])
            rune_count += 1
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

def decrypt_autokey(text, primer):
    """Autokey cipher variant"""
    result = []
    key = list(primer)
    rune_count = 0
    
    for c in text:
        if c in RUNES:
            idx = RUNES.index(c)
            if rune_count < len(key):
                shift_val = key[rune_count]
            else:
                shift_val = idx  # Use plaintext as key
            new_idx = shift(idx, -shift_val)
            result.append(LETTERS[new_idx])
            key.append(new_idx)
            rune_count += 1
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

def decrypt_totient_shift(text, offset=0, direction=-1):
    """
    Shift by Euler's totient function values
    """
    def totient(n):
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result
    
    result = []
    n = 1
    
    for c in text:
        if c in RUNES:
            idx = RUNES.index(c)
            t = totient(n)
            new_idx = shift(idx, direction * (t + offset))
            result.append(LETTERS[new_idx])
            n += 1
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

def decrypt_fibonacci_shift(text, offset=0, direction=-1):
    """Shift by Fibonacci sequence"""
    result = []
    fib_idx = 0
    
    for c in text:
        if c in RUNES:
            idx = RUNES.index(c)
            fib = FIRST_1000_FIBS[fib_idx] if fib_idx < 1000 else fib_idx
            new_idx = shift(idx, direction * (fib + offset))
            result.append(LETTERS[new_idx])
            fib_idx += 1
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

def decrypt_running_key(text, key_text):
    """Running key cipher using another text as key"""
    key_runes = runes_only(key_text)
    result = []
    key_idx = 0
    
    for c in text:
        if c in RUNES:
            if key_idx >= len(key_runes):
                key_idx = 0  # Wrap around
            idx = RUNES.index(c)
            key_idx_val = RUNES.index(key_runes[key_idx])
            result.append(LETTERS[shift(idx, -key_idx_val)])
            key_idx += 1
        elif c == '•':
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)

# =============================================================================
# KNOWN PLAINTEXT ATTACK
# =============================================================================

def known_plaintext_attack(ciphertext, known_phrase, max_position=100):
    """
    Try to find where known plaintext might appear
    and derive potential keys
    """
    cipher_runes = runes_only(ciphertext)
    known_lower = known_phrase.lower().replace(' ', '')
    
    results = []
    
    for pos in range(min(max_position, len(cipher_runes) - len(known_lower))):
        key = []
        valid = True
        
        for i, char in enumerate(known_lower):
            # Find the rune index for this English character
            plain_idx = None
            for idx, letter in enumerate(LETTERS):
                if letter == char or (len(letter) > 1 and letter[0] == char):
                    plain_idx = idx
                    break
            
            if plain_idx is None:
                valid = False
                break
            
            cipher_idx = RUNES.index(cipher_runes[pos + i])
            key_val = (cipher_idx - plain_idx) % ALPHABET_SIZE
            key.append(key_val)
        
        if valid:
            results.append({
                'position': pos,
                'key': key,
                'key_pattern': analyze_key_pattern(key)
            })
    
    return results

def analyze_key_pattern(key):
    """Analyze if a key follows a mathematical pattern"""
    if len(key) < 3:
        return "too short"
    
    # Check for constant key (Caesar)
    if len(set(key)) == 1:
        return f"Caesar shift: {key[0]}"
    
    # Check for arithmetic sequence
    diffs = [key[i+1] - key[i] for i in range(len(key)-1)]
    if len(set(diffs)) == 1:
        return f"Arithmetic: start={key[0]}, step={diffs[0]}"
    
    # Check if key matches prime sequence
    for offset in range(-30, 30):
        matches = sum(1 for i, k in enumerate(key) if (FIRST_1000_PRIMES[i] + offset) % 29 == k)
        if matches == len(key):
            return f"Prime+{offset} shift"
    
    return "Unknown pattern"

# =============================================================================
# MAIN SOLVER
# =============================================================================

def solve_page(text, page_name="Unknown"):
    """
    Try multiple decryption methods on a page
    Returns list of (method, params, score, preview) tuples
    """
    results = []
    
    print(f"\n{'='*70}")
    print(f"Solving: {page_name}")
    print(f"{'='*70}")
    print(f"Input: {text[:60]}...")
    
    # Method 1: Caesar shifts
    print("\n[1] Testing Caesar shifts...")
    for shift_val in range(ALPHABET_SIZE):
        decrypted = decrypt_caesar(text, shift_val)
        score = score_english(decrypted)
        if score > 10:
            results.append(('Caesar', shift_val, score, decrypted[:100]))
    
    # Method 2: Prime shifts with different offsets
    print("[2] Testing Prime shifts...")
    for offset in range(0, 120, 1):
        for direction in [-1, 1]:
            decrypted = decrypt_prime_shift(text, offset, direction)
            score = score_english(decrypted)
            if score > 15:
                results.append((f'Prime{direction:+d}', offset, score, decrypted[:100]))
    
    # Method 3: Fibonacci shifts
    print("[3] Testing Fibonacci shifts...")
    for offset in range(-30, 30):
        for direction in [-1, 1]:
            decrypted = decrypt_fibonacci_shift(text, offset, direction)
            score = score_english(decrypted)
            if score > 15:
                results.append((f'Fib{direction:+d}', offset, score, decrypted[:100]))
    
    # Method 4: Simple Vigenère with short keys
    print("[4] Testing Vigenère with short keys...")
    for key_len in range(2, 8):
        # Try keys based on prime sequence
        for start in range(10):
            key = [(FIRST_1000_PRIMES[i + start]) % 29 for i in range(key_len)]
            decrypted = decrypt_vigenere(text, key)
            score = score_english(decrypted)
            if score > 15:
                results.append(('Vigenere-Prime', f"len={key_len},start={start}", score, decrypted[:100]))
    
    # Method 5: Known plaintext attack with Cicada-specific words
    print("[5] Testing known plaintext attack...")
    for phrase in ['instar', 'cicada', 'emerge', 'within', 'wisdom', 'truth', 'parable']:
        kpa_results = known_plaintext_attack(text, phrase)
        for kpa in kpa_results[:3]:  # Top 3 positions
            if 'Prime' in kpa['key_pattern'] or 'Arithmetic' in kpa['key_pattern']:
                results.append(('KPA', f"{phrase}@{kpa['position']}", 20, kpa['key_pattern']))
    
    # Sort by score
    results.sort(key=lambda x: x[2], reverse=True)
    
    # Show top results
    print(f"\n--- Top Results for {page_name} ---")
    if results:
        for method, params, score, preview in results[:5]:
            print(f"\n[Score: {score}] {method} (params: {params})")
            print(f"  {preview}...")
    else:
        print("No promising decryptions found.")
    
    return results

# =============================================================================
# TEST PAGES
# =============================================================================

if __name__ == "__main__":
    # Page 56 (known solution for comparison)
    PAGE_56 = "ᚫᛂ•ᛟᛋᚱ:ᛗᚣᛚᚩᚻ•ᚩᚫ•ᚳᚦᚷᚹ•ᚹᛚᚫ,ᛉᚩᚪᛈ•ᛗᛞᛞᚢᚷᚹ•ᛚ•ᛞᚾᚣᛂ•ᚳᚠᛡ•ᚫᛏᛈᛇᚪᚦ•ᚳᚫ:ᚳᛞ•ᚠᚾ•ᛡᛖ•ᚠᚾᚳᛝ•ᚱᚠ•ᚫᛁᚱᛞᛖ•ᛋᚣᛂᛠᚢᛝᚹ•ᛉᚩ•ᛗᛠᚹᚠ•ᚱᚷᛡ•ᛝᚱᛒ•ᚫᚾᚢᛋ:"
    
    # Some early pages to test
    PAGE_0_SAMPLE = "ᛋᚻᛖᚩᚷᛗᛡᚠ•ᛋᚣᛖᛝᚳ•ᚦᛂᚷᚫ•ᚠᛂᛟ•ᚩᚾᚦ•ᚾᛖᚹᛒᚪᛋᛟᛇᛁᛝᚢ•ᚾᚫᚷᛁᚦ•ᚻᛒᚾᛡ"
    
    # Test Page 56 first (known solution)
    print("\n" + "#" * 70)
    print("# VERIFYING KNOWN SOLUTION - PAGE 56")
    print("#" * 70)
    solve_page(PAGE_56, "Page 56")
    
    # Test an unsolved page
    print("\n" + "#" * 70)
    print("# ATTEMPTING UNKNOWN PAGE")
    print("#" * 70)
    solve_page(PAGE_0_SAMPLE, "Page 0 Sample")
    
    # Load and test first page from file
    try:
        with open('2014/Liber Primus/runes in text format.txt', 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        # Get first substantial page
        lines = full_text.split('\n')
        first_page = ''.join(line.replace('/', '') for line in lines[:12] if line.strip() not in ['%', '&', '$'])
        
        print("\n" + "#" * 70)
        print("# ATTEMPTING FIRST PAGE FROM FILE")
        print("#" * 70)
        solve_page(first_page, "First Page")
        
    except FileNotFoundError:
        print("Could not load Liber Primus file")

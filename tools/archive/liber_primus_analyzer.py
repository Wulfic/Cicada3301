# -*- coding: utf-8 -*-
"""
Liber Primus Analysis Toolkit
Comprehensive tools for analyzing and attempting to decrypt the Liber Primus

Author: Cicada Solver
Date: 2026-01-04
"""

import itertools as it
from collections import Counter, namedtuple
from pathlib import Path
import math
import re

# =============================================================================
# GEMATRIA PRIMUS - The Core Alphabet
# =============================================================================

Rune = namedtuple("Rune", ["icon", "english", "gematria", "index"])

GEMATRIA_PRIMUS = (
    Rune('ᚠ', 'f', 2, 0),
    Rune('ᚢ', 'u', 3, 1),
    Rune('ᚦ', 'th', 5, 2),
    Rune('ᚩ', 'o', 7, 3),
    Rune('ᚱ', 'r', 11, 4),
    Rune('ᚳ', 'c', 13, 5),
    Rune('ᚷ', 'g', 17, 6),
    Rune('ᚹ', 'w', 19, 7),
    Rune('ᚻ', 'h', 23, 8),
    Rune('ᚾ', 'n', 29, 9),
    Rune('ᛁ', 'i', 31, 10),
    Rune('ᛂ', 'j', 37, 11),
    Rune('ᛇ', 'eo', 41, 12),
    Rune('ᛈ', 'p', 43, 13),
    Rune('ᛉ', 'x', 47, 14),
    Rune('ᛋ', 's', 53, 15),
    Rune('ᛏ', 't', 59, 16),
    Rune('ᛒ', 'b', 61, 17),
    Rune('ᛖ', 'e', 67, 18),
    Rune('ᛗ', 'm', 71, 19),
    Rune('ᛚ', 'l', 73, 20),
    Rune('ᛝ', 'ing', 79, 21),
    Rune('ᛟ', 'oe', 83, 22),
    Rune('ᛞ', 'd', 89, 23),
    Rune('ᚪ', 'a', 97, 24),
    Rune('ᚫ', 'ae', 101, 25),
    Rune('ᚣ', 'y', 103, 26),
    Rune('ᛡ', 'io', 107, 27),
    Rune('ᛠ', 'ea', 109, 28),
)

RUNES = [r.icon for r in GEMATRIA_PRIMUS]
LETTERS = [r.english for r in GEMATRIA_PRIMUS]
PRIMES = [r.gematria for r in GEMATRIA_PRIMUS]
ALPHABET_SIZE = len(GEMATRIA_PRIMUS)

# Special characters
WORD_SEP = '•'
LINE_SEP = '%'
SECTION_SEP = '&'
PAGE_SEP = '$'
SPECIAL_CHARS = {WORD_SEP, LINE_SEP, SECTION_SEP, PAGE_SEP, '-', ':', '.', '\n', '/'}

# =============================================================================
# PRIME NUMBER UTILITIES
# =============================================================================

def prime_generator():
    """Infinite generator of prime numbers using Sieve of Eratosthenes variant"""
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

def get_primes(n):
    """Get first n prime numbers"""
    gen = prime_generator()
    return [next(gen) for _ in range(n)]

# =============================================================================
# RUNE CONVERSION UTILITIES
# =============================================================================

def rune_to_index(rune):
    """Convert rune to its index (0-28)"""
    try:
        return RUNES.index(rune)
    except ValueError:
        return None

def index_to_rune(index):
    """Convert index (0-28) to rune"""
    return RUNES[index % ALPHABET_SIZE]

def index_to_letter(index):
    """Convert index (0-28) to English letter(s)"""
    return LETTERS[index % ALPHABET_SIZE]

def rune_to_letter(rune):
    """Convert rune directly to English"""
    idx = rune_to_index(rune)
    return LETTERS[idx] if idx is not None else rune

def rune_to_gematria(rune):
    """Convert rune to its prime gematria value"""
    idx = rune_to_index(rune)
    return PRIMES[idx] if idx is not None else 0

def text_to_indices(text):
    """Convert runic text to list of indices, ignoring non-runes"""
    return [rune_to_index(c) for c in text if c in RUNES]

def text_to_runes_only(text):
    """Extract only rune characters from text"""
    return [c for c in text if c in RUNES]

def transliterate(text):
    """Convert runic text to English transliteration"""
    result = []
    for c in text:
        if c in RUNES:
            result.append(rune_to_letter(c))
        elif c == WORD_SEP:
            result.append(' ')
        elif c in SPECIAL_CHARS:
            result.append(c)
        else:
            result.append(c)
    return ''.join(result)

# =============================================================================
# CIPHER OPERATIONS
# =============================================================================

def shift_rune(rune, shift_amount):
    """Shift a rune by shift_amount positions (mod 29)"""
    idx = rune_to_index(rune)
    if idx is None:
        return rune
    new_idx = (idx + shift_amount) % ALPHABET_SIZE
    return index_to_rune(new_idx)

def caesar_decrypt(text, shift):
    """Apply Caesar cipher with given shift"""
    result = []
    for c in text:
        if c in RUNES:
            result.append(shift_rune(c, -shift))
        else:
            result.append(c)
    return ''.join(result)

def vigenere_decrypt(text, key_indices):
    """Decrypt using Vigenère cipher with list of key indices"""
    result = []
    key_len = len(key_indices)
    rune_count = 0
    
    for c in text:
        if c in RUNES:
            shift = key_indices[rune_count % key_len]
            result.append(shift_rune(c, -shift))
            rune_count += 1
        else:
            result.append(c)
    return ''.join(result)

def prime_shift_decrypt(text, offset=57, direction=-1):
    """
    Page 56 style decryption: shift each rune by -(prime_n + offset)
    
    Args:
        text: Runic ciphertext
        offset: Constant added to prime (57 for Page 56)
        direction: 1 or -1 for shift direction
    """
    result = []
    pg = prime_generator()
    
    for c in text:
        if c in RUNES:
            prime = next(pg)
            shift = direction * (prime + offset)
            result.append(shift_rune(c, shift))
        else:
            result.append(c)
    return ''.join(result)

def stream_decrypt(text, stream):
    """Decrypt using a custom stream of shift values"""
    result = []
    stream_iter = iter(stream)
    
    for c in text:
        if c in RUNES:
            try:
                shift = next(stream_iter)
                result.append(shift_rune(c, -shift))
            except StopIteration:
                result.append(c)
        else:
            result.append(c)
    return ''.join(result)

# =============================================================================
# FREQUENCY ANALYSIS
# =============================================================================

def count_runes(text):
    """Count frequency of each rune in text"""
    runes_only = text_to_runes_only(text)
    return Counter(runes_only)

def frequency_analysis(text):
    """
    Perform frequency analysis on runic text
    Returns sorted list of (rune, count, percentage, english)
    """
    counts = count_runes(text)
    total = sum(counts.values())
    
    results = []
    for rune, count in counts.most_common():
        idx = rune_to_index(rune)
        pct = (count / total * 100) if total > 0 else 0
        results.append({
            'rune': rune,
            'english': LETTERS[idx],
            'count': count,
            'percentage': pct,
            'gematria': PRIMES[idx]
        })
    return results

def print_frequency_analysis(text, title="Frequency Analysis"):
    """Pretty print frequency analysis"""
    results = frequency_analysis(text)
    total = sum(r['count'] for r in results)
    
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Total runes: {total}")
    print(f"\n{'Rune':<6} {'Eng':<5} {'Count':<8} {'%':<8} {'Gematria':<10}")
    print("-" * 45)
    
    for r in results:
        print(f"{r['rune']:<6} {r['english']:<5} {r['count']:<8} {r['percentage']:<8.2f} {r['gematria']:<10}")

# Expected English letter frequencies (approximate)
ENGLISH_FREQ = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}

# =============================================================================
# INDEX OF COINCIDENCE
# =============================================================================

def index_of_coincidence(text):
    """
    Calculate the Index of Coincidence (IoC) for runic text
    
    English text typically has IoC around 0.067 (1.73 normalized)
    Random text has IoC around 0.0385 (1.0 normalized)
    """
    runes_only = text_to_runes_only(text)
    n = len(runes_only)
    
    if n <= 1:
        return 0
    
    counts = Counter(runes_only)
    sum_freq = sum(f * (f - 1) for f in counts.values())
    ioc = sum_freq / (n * (n - 1))
    
    # Normalized IoC (multiply by alphabet size)
    normalized = ioc * ALPHABET_SIZE
    
    return {
        'ioc': ioc,
        'normalized': normalized,
        'total_runes': n,
        'unique_runes': len(counts)
    }

def kappa_test(text, max_period=30):
    """
    Kappa test to estimate key length for polyalphabetic cipher
    Returns list of (period, ioc) tuples
    """
    runes_only = text_to_runes_only(text)
    n = len(runes_only)
    results = []
    
    for period in range(1, min(max_period + 1, n // 2)):
        # Split text into columns by period
        columns = [[] for _ in range(period)]
        for i, rune in enumerate(runes_only):
            columns[i % period].append(rune)
        
        # Calculate average IoC across columns
        iocs = []
        for col in columns:
            if len(col) > 1:
                counts = Counter(col)
                m = len(col)
                sum_freq = sum(f * (f - 1) for f in counts.values())
                ioc = sum_freq / (m * (m - 1)) if m > 1 else 0
                iocs.append(ioc)
        
        avg_ioc = sum(iocs) / len(iocs) if iocs else 0
        results.append((period, avg_ioc * ALPHABET_SIZE))
    
    return results

# =============================================================================
# N-GRAM ANALYSIS
# =============================================================================

def find_ngrams(text, n=2):
    """Find all n-grams in runic text"""
    runes_only = text_to_runes_only(text)
    ngrams = []
    for i in range(len(runes_only) - n + 1):
        ngram = ''.join(runes_only[i:i+n])
        ngrams.append(ngram)
    return Counter(ngrams)

def find_repeated_sequences(text, min_length=3, max_length=10):
    """Find repeated sequences and their positions"""
    runes_only = ''.join(text_to_runes_only(text))
    sequences = {}
    
    for length in range(min_length, max_length + 1):
        for i in range(len(runes_only) - length + 1):
            seq = runes_only[i:i+length]
            if seq not in sequences:
                sequences[seq] = []
            sequences[seq].append(i)
    
    # Filter to only repeated sequences
    repeated = {seq: positions for seq, positions in sequences.items() 
                if len(positions) > 1}
    
    return repeated

def kasiski_examination(text, min_length=3):
    """
    Kasiski examination to find possible key lengths
    Looks at spacings between repeated sequences
    """
    repeated = find_repeated_sequences(text, min_length=min_length)
    spacings = []
    
    for seq, positions in repeated.items():
        for i in range(len(positions) - 1):
            for j in range(i + 1, len(positions)):
                spacing = positions[j] - positions[i]
                spacings.append(spacing)
    
    if not spacings:
        return []
    
    # Find common factors
    factor_counts = Counter()
    for spacing in spacings:
        for factor in range(2, min(spacing + 1, 50)):
            if spacing % factor == 0:
                factor_counts[factor] += 1
    
    return factor_counts.most_common(10)

# =============================================================================
# GEMATRIA CALCULATIONS
# =============================================================================

def calculate_gematria_sum(text):
    """Calculate total gematria value of runic text"""
    return sum(rune_to_gematria(c) for c in text if c in RUNES)

def calculate_word_gematria(text):
    """Calculate gematria for each word in text"""
    words = text.split(WORD_SEP)
    results = []
    for word in words:
        if any(c in RUNES for c in word):
            value = calculate_gematria_sum(word)
            results.append({
                'word': word,
                'transliteration': transliterate(word),
                'gematria': value
            })
    return results

# =============================================================================
# PAGE PARSING
# =============================================================================

def parse_pages(text):
    """
    Parse full Liber Primus text into individual pages
    Uses % for line breaks and & or $ for page breaks
    """
    # Split by page markers
    pages = re.split(r'[&$]+', text)
    return [p.strip() for p in pages if p.strip()]

def load_liber_primus(filepath):
    """Load Liber Primus from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# =============================================================================
# ENGLISH SCORING
# =============================================================================

# Common English words for scoring
COMMON_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'is', 'are', 'was', 'were', 'been', 'being', 'who', 'which', 'when', 'where',
    'why', 'how', 'each', 'some', 'into', 'could', 'than', 'other', 'so', 'if',
    # Cicada-specific words
    'instar', 'cicada', 'emergence', 'divinity', 'within', 'parable', 'wisdom',
    'knowledge', 'truth', 'seek', 'find', 'prime', 'self', 'path', 'journey'
}

def score_english(text):
    """
    Score how "English-like" a decrypted text appears
    Higher score = more likely to be correct English
    """
    text_lower = text.lower()
    words = re.findall(r'[a-z]+', text_lower)
    
    if not words:
        return 0
    
    # Count recognized words
    recognized = sum(1 for w in words if w in COMMON_WORDS)
    word_score = recognized / len(words) * 100
    
    # Check for common English patterns
    pattern_score = 0
    if ' the ' in text_lower:
        pattern_score += 10
    if ' and ' in text_lower:
        pattern_score += 10
    if ' of ' in text_lower:
        pattern_score += 10
    
    return word_score + pattern_score

# =============================================================================
# MAIN ANALYSIS FUNCTIONS
# =============================================================================

def analyze_text(text, title="Analysis"):
    """Comprehensive analysis of runic text"""
    print(f"\n{'#'*70}")
    print(f"# {title}")
    print(f"{'#'*70}")
    
    # Basic stats
    runes_only = text_to_runes_only(text)
    print(f"\nBasic Statistics:")
    print(f"  Total characters: {len(text)}")
    print(f"  Total runes: {len(runes_only)}")
    print(f"  Unique runes: {len(set(runes_only))}")
    print(f"  Gematria sum: {calculate_gematria_sum(text)}")
    
    # Index of Coincidence
    ioc_result = index_of_coincidence(text)
    print(f"\nIndex of Coincidence:")
    print(f"  Raw IoC: {ioc_result['ioc']:.6f}")
    print(f"  Normalized IoC: {ioc_result['normalized']:.4f}")
    print(f"  (English ≈ 1.73, Random ≈ 1.0)")
    
    # Frequency analysis
    print_frequency_analysis(text, "Rune Frequency Distribution")
    
    # Kappa test for key length
    print(f"\nKappa Test (Key Length Estimation):")
    kappa_results = kappa_test(text, max_period=15)
    print(f"  {'Period':<10} {'Norm. IoC':<12} {'Interpretation'}")
    print(f"  {'-'*40}")
    for period, ioc in kappa_results[:10]:
        interp = "HIGH" if ioc > 1.5 else "low"
        print(f"  {period:<10} {ioc:<12.4f} {interp}")
    
    # Kasiski examination
    print(f"\nKasiski Examination (Likely Key Lengths):")
    kasiski_results = kasiski_examination(text)
    for factor, count in kasiski_results[:5]:
        print(f"  Factor {factor}: {count} occurrences")
    
    return {
        'ioc': ioc_result,
        'kappa': kappa_results,
        'kasiski': kasiski_results
    }

def try_decryptions(text, title="Decryption Attempts"):
    """Try various decryption methods and score results"""
    print(f"\n{'#'*70}")
    print(f"# {title}")
    print(f"{'#'*70}")
    
    results = []
    
    # Try Caesar shifts
    print("\n--- Caesar Shifts ---")
    for shift in range(ALPHABET_SIZE):
        decrypted = caesar_decrypt(text, shift)
        translit = transliterate(decrypted)
        score = score_english(translit)
        if score > 5:  # Only show promising results
            results.append(('Caesar', shift, translit[:100], score))
    
    # Try Page 56 method with different offsets
    print("\n--- Prime Shift (Page 56 style) ---")
    for offset in range(50, 65):
        decrypted = prime_shift_decrypt(text, offset=offset, direction=-1)
        translit = transliterate(decrypted)
        score = score_english(translit)
        if score > 5:
            results.append(('Prime-shift', offset, translit[:100], score))
    
    # Sort by score
    results.sort(key=lambda x: x[3], reverse=True)
    
    print("\nTop Results:")
    for method, param, text_preview, score in results[:10]:
        print(f"\n{method} (param={param}, score={score:.1f}):")
        print(f"  {text_preview}...")
    
    return results

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Load and analyze
    lp_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    if lp_path.exists():
        print(f"Loading Liber Primus from: {lp_path}")
        text = load_liber_primus(lp_path)
        
        # Get pages
        pages = parse_pages(text)
        print(f"\nFound {len(pages)} pages/sections")
        
        # Analyze full text
        analyze_text(text, "Full Liber Primus Analysis")
        
        # Test Page 57 (The Parable - should be plaintext)
        page_57 = "ᛈᚪᚱᚪᛒᛚᛖ:ᛚᛁᚳᛖ•ᚦᛖ•ᛁᚾᛋᛏᚪᚱ•ᛏᚢᚾᚾᛖᛚᛝ•ᛏᚩ•ᚦᛖ•ᛋᚢᚱᚠᚪᚳᛖ.ᚹᛖ•ᛗᚢᛋᛏ•ᛋᚻᛖᛞ•ᚩᚢᚱ•ᚩᚹᚾ•ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ.ᚠᛁᚾᛞ•ᚦᛖ•ᛞᛁᚢᛁᚾᛁᛏᚣ•ᚹᛁᚦᛁᚾ•ᚪᚾᛞ•ᛖᛗᛖᚱᚷᛖ::"
        print("\n" + "="*70)
        print("PAGE 57 (THE PARABLE) - Should be plaintext:")
        print("="*70)
        print(transliterate(page_57))
        
    else:
        print(f"File not found: {lp_path}")
        print("Please run from the Cicada3301 repository root")

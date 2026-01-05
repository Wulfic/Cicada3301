#!/usr/bin/env python3
"""
Deep pattern analysis - looking for structural patterns that might reveal the key.

Key observations from previous analysis:
1. Gematria+ gives IoC ~1.79 with 127 "THE" appearances
2. Offset -200 (≡3 mod 29) improves all pages to IoC 1.4-1.57
3. Page 18 is already decrypted ("PARABLE...")

New approaches:
1. Look at word boundary patterns
2. Analyze repeated sequences (possible cribs)
3. Try using the solved "PARABLE" text as a running key
4. Look for acrostics or other structural patterns
"""

import sys
sys.path.insert(0, 'C:/Users/tyler/Repos/Cicada3301')

from collections import Counter, defaultdict
import re

# Rune alphabet and mappings
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'EA', 'IO']

GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 
            73, 79, 83, 89, 97, 101, 107, 113, 127, 149]  # Consecutive primes (first 29)

# Actually use the correct primes from the community data
GEMATRIA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 
            71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
RUNE_TO_GEM = {r: GEMATRIA[i] for i, r in enumerate(RUNES)}

def tokenize_runes(text):
    """Convert text to list of rune tokens."""
    tokens = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Try digraphs first
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph in RUNE_TO_IDX:
                tokens.append(digraph)
                i += 2
                continue
        if text[i] in RUNE_TO_IDX:
            tokens.append(text[i])
            i += 1
        else:
            # Non-rune character (delimiter)
            tokens.append(text[i])
            i += 1
    return tokens

def is_rune(token):
    return token in RUNE_TO_IDX

def shift_rune(rune, shift):
    """Shift a rune by amount (mod 29)."""
    idx = RUNE_TO_IDX[rune]
    new_idx = (idx + shift) % 29
    return RUNES[new_idx]

def gematria_shift_add(rune):
    """Shift rune by its gematria value (ADD direction)."""
    gem = RUNE_TO_GEM[rune]
    idx = RUNE_TO_IDX[rune]
    new_idx = (idx + gem) % 29
    return RUNES[new_idx]

def gematria_shift_sub(rune):
    """Shift rune by negative gematria value (SUB direction)."""
    gem = RUNE_TO_GEM[rune]
    idx = RUNE_TO_IDX[rune]
    new_idx = (idx - gem) % 29
    return RUNES[new_idx]

def load_pages():
    """Load the pages from the wiki data."""
    wiki_path = "C:/Users/tyler/Repos/Cicada3301/EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py"
    
    with open(wiki_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract individual Page variables (Page0, Page1, etc.)
    pages = []
    for i in range(58):
        pattern = rf'Page{i}\s*=\s*"([^"]*)"'
        match = re.search(pattern, content)
        if match:
            pages.append(match.group(1))
        else:
            pages.append("")  # Empty page
    
    return pages

def analyze_word_patterns(pages):
    """Analyze word patterns across all pages."""
    print("\n" + "="*70)
    print("WORD PATTERN ANALYSIS")
    print("="*70)
    
    all_words = []
    for page in pages:
        words = page.replace('.', ' ').replace('-', ' ').split()
        all_words.extend(words)
    
    word_freq = Counter(all_words)
    print(f"\nTotal words: {len(all_words)}")
    print(f"Unique words: {len(word_freq)}")
    print(f"\nTop 30 most common words:")
    for word, count in word_freq.most_common(30):
        print(f"  {word}: {count}")
    
    # Look at word lengths
    word_lengths = Counter(len(w) for w in all_words)
    print(f"\nWord length distribution:")
    for length in sorted(word_lengths.keys()):
        print(f"  Length {length}: {word_lengths[length]} words")
    
    return all_words

def analyze_repeated_sequences(text_runes, min_len=4, max_len=10):
    """Find repeated sequences (possible cribs or cipher artifacts)."""
    print("\n" + "="*70)
    print("REPEATED SEQUENCE ANALYSIS")
    print("="*70)
    
    # Only rune characters
    runes_only = [r for r in text_runes if is_rune(r)]
    rune_str = ''.join(runes_only)
    
    for seq_len in range(min_len, max_len + 1):
        sequences = Counter()
        positions = defaultdict(list)
        
        for i in range(len(rune_str) - seq_len + 1):
            seq = rune_str[i:i+seq_len]
            sequences[seq] += 1
            positions[seq].append(i)
        
        repeated = [(seq, count, positions[seq]) for seq, count in sequences.items() if count >= 2]
        repeated.sort(key=lambda x: -x[1])
        
        if repeated:
            print(f"\nLength {seq_len} repeated sequences (top 10):")
            for seq, count, pos in repeated[:10]:
                # Calculate distances between occurrences
                dists = [pos[i+1] - pos[i] for i in range(len(pos)-1)]
                print(f"  {seq}: {count} times, distances: {dists[:5]}...")

def try_running_key_with_parable(encrypted_page, parable_text):
    """Try using the solved PARABLE text as a running key."""
    print("\n" + "="*70)
    print("RUNNING KEY WITH PARABLE TEXT")
    print("="*70)
    
    # Get runes from both texts
    enc_tokens = tokenize_runes(encrypted_page)
    enc_runes = [t for t in enc_tokens if is_rune(t)]
    
    key_tokens = tokenize_runes(parable_text.replace('.', '').replace(' ', ''))
    key_runes = [t for t in key_tokens if is_rune(t)]
    
    print(f"Encrypted runes: {len(enc_runes)}")
    print(f"Key runes from PARABLE: {len(key_runes)}")
    
    # Extend key by repeating
    extended_key = (key_runes * ((len(enc_runes) // len(key_runes)) + 2))[:len(enc_runes)]
    
    # Try ADD and SUB with key
    for direction, op in [("ADD", 1), ("SUB", -1)]:
        result = []
        for enc_rune, key_rune in zip(enc_runes, extended_key):
            key_idx = RUNE_TO_IDX[key_rune]
            enc_idx = RUNE_TO_IDX[enc_rune]
            new_idx = (enc_idx + op * key_idx) % 29
            result.append(RUNES[new_idx])
        
        result_str = ''.join(result)
        
        # Calculate IoC
        freq = Counter(result)
        n = len(result)
        ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) * 29 if n > 1 else 0
        
        # Check for common patterns
        the_count = result_str.count('THE')
        and_count = result_str.count('AND')
        
        print(f"\n{direction} with PARABLE key:")
        print(f"  IoC: {ioc:.4f}")
        print(f"  THE count: {the_count}, AND count: {and_count}")
        print(f"  First 100 chars: {result_str[:100]}")

def try_fibonacci_gematria(encrypted_runes):
    """Try Fibonacci-based gematria shifts."""
    print("\n" + "="*70)
    print("FIBONACCI-BASED GEMATRIA SHIFT")
    print("="*70)
    
    runes = [r for r in tokenize_runes(encrypted_runes) if is_rune(r)]
    
    # Generate Fibonacci sequence
    fib = [1, 1]
    while len(fib) < len(runes):
        fib.append(fib[-1] + fib[-2])
    
    for direction, op in [("ADD", 1), ("SUB", -1)]:
        result = []
        for i, rune in enumerate(runes):
            shift = fib[i] % 29
            idx = RUNE_TO_IDX[rune]
            new_idx = (idx + op * shift) % 29
            result.append(RUNES[new_idx])
        
        result_str = ''.join(result)
        freq = Counter(result)
        n = len(result)
        ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) * 29 if n > 1 else 0
        
        print(f"\nFibonacci {direction}:")
        print(f"  IoC: {ioc:.4f}")
        print(f"  First 100 chars: {result_str[:100]}")

def try_totient_based_shift(encrypted_runes):
    """Try Euler's totient function based shifts."""
    print("\n" + "="*70)
    print("EULER TOTIENT BASED SHIFT")
    print("="*70)
    
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
    
    runes = [r for r in tokenize_runes(encrypted_runes) if is_rune(r)]
    
    for direction, op in [("ADD", 1), ("SUB", -1)]:
        result = []
        for i, rune in enumerate(runes):
            gem = RUNE_TO_GEM[rune]
            tot = totient(gem) % 29
            idx = RUNE_TO_IDX[rune]
            new_idx = (idx + op * tot) % 29
            result.append(RUNES[new_idx])
        
        result_str = ''.join(result)
        freq = Counter(result)
        n = len(result)
        ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) * 29 if n > 1 else 0
        
        print(f"\nTotient {direction}:")
        print(f"  IoC: {ioc:.4f}")
        print(f"  First 100 chars: {result_str[:100]}")

def try_prime_index_gematria(encrypted_runes):
    """
    Key insight: Page 56 formula uses -(prime + 57) mod 29
    What if instead of gematria value, we use the INDEX in the prime sequence?
    """
    print("\n" + "="*70)
    print("PRIME INDEX GEMATRIA (Page 56 variant)")
    print("="*70)
    
    # Prime indices: F=0 (2 is 0th prime), U=1 (3 is 1st), etc.
    PRIME_INDEX = {r: i for i, r in enumerate(RUNES)}
    
    runes = [r for r in tokenize_runes(encrypted_runes) if is_rune(r)]
    
    # Try various constants similar to 57 in Page 56 formula
    for const in [0, 13, 29, 47, 56, 57, 58, 59, 83, 101]:
        for direction, op in [("SUB", -1), ("ADD", 1)]:
            result = []
            for i, rune in enumerate(runes):
                prime_idx = PRIME_INDEX[rune]
                # Formula: -(prime_index + constant) mod 29
                shift = op * (prime_idx + const)
                idx = RUNE_TO_IDX[rune]
                new_idx = (idx + shift) % 29
                result.append(RUNES[new_idx])
            
            result_str = ''.join(result)
            freq = Counter(result)
            n = len(result)
            ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) * 29 if n > 1 else 0
            
            if ioc > 1.4:  # Only show promising results
                print(f"const={const}, {direction}: IoC={ioc:.4f}, first 60: {result_str[:60]}")

def try_cumulative_gematria(encrypted_runes):
    """
    Try shifting each rune by the cumulative sum of previous gematria values.
    This creates a running key effect.
    """
    print("\n" + "="*70)
    print("CUMULATIVE GEMATRIA SHIFT")
    print("="*70)
    
    runes = [r for r in tokenize_runes(encrypted_runes) if is_rune(r)]
    
    for direction, op in [("ADD", 1), ("SUB", -1)]:
        result = []
        cum_sum = 0
        for rune in runes:
            gem = RUNE_TO_GEM[rune]
            shift = cum_sum % 29
            idx = RUNE_TO_IDX[rune]
            new_idx = (idx + op * shift) % 29
            result.append(RUNES[new_idx])
            cum_sum += gem
        
        result_str = ''.join(result)
        freq = Counter(result)
        n = len(result)
        ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) * 29 if n > 1 else 0
        
        print(f"\nCumulative gematria {direction}:")
        print(f"  IoC: {ioc:.4f}")
        print(f"  First 100 chars: {result_str[:100]}")

def try_differential_analysis(encrypted_runes):
    """
    Look at differences between consecutive runes - might reveal plaintext patterns.
    """
    print("\n" + "="*70)
    print("DIFFERENTIAL ANALYSIS")
    print("="*70)
    
    runes = [r for r in tokenize_runes(encrypted_runes) if is_rune(r)]
    
    # Calculate differences
    diffs = []
    for i in range(1, len(runes)):
        idx1 = RUNE_TO_IDX[runes[i-1]]
        idx2 = RUNE_TO_IDX[runes[i]]
        diff = (idx2 - idx1) % 29
        diffs.append(diff)
    
    diff_freq = Counter(diffs)
    print("Difference frequencies (should be skewed for English):")
    for diff in sorted(diff_freq.keys()):
        print(f"  {diff:2d}: {'#' * (diff_freq[diff] // 5)} {diff_freq[diff]}")
    
    # In English, common transitions: E->S, T->H, A->N, etc.
    # If encrypted, differences should be uniform; if close to plaintext, should be skewed

def try_interleaved_pages(pages, page_indices):
    """
    Try treating multiple pages as interleaved single message.
    """
    print("\n" + "="*70)
    print("INTERLEAVED PAGE ANALYSIS")
    print("="*70)
    
    # Combine pages
    combined = []
    for idx in page_indices:
        if idx < len(pages):
            runes = [r for r in tokenize_runes(pages[idx]) if is_rune(r)]
            combined.extend(runes)
    
    print(f"Combined {len(page_indices)} pages: {len(combined)} runes")
    
    # Try gematria shift on combined
    result = []
    for rune in combined:
        result.append(gematria_shift_add(rune))
    
    result_str = ''.join(result)
    freq = Counter(result)
    n = len(result)
    ioc = sum(f * (f-1) for f in freq.values()) / (n * (n-1)) * 29 if n > 1 else 0
    
    print(f"Gematria+ on combined: IoC={ioc:.4f}")
    print(f"First 100 chars: {result_str[:100]}")

def analyze_acrostic(pages):
    """Look for acrostic patterns (first letter of each word/line)."""
    print("\n" + "="*70)
    print("ACROSTIC ANALYSIS")
    print("="*70)
    
    for i, page in enumerate(pages[:5]):  # First 5 pages
        words = page.replace('.', ' ').replace('-', ' ').split()
        if words:
            first_letters = []
            for word in words:
                tokens = tokenize_runes(word)
                if tokens and is_rune(tokens[0]):
                    first_letters.append(tokens[0])
            
            acrostic = ''.join(first_letters)
            print(f"Page {i} word acrostic: {acrostic[:50]}...")

def main():
    print("="*70)
    print("DEEP PATTERN ANALYSIS")
    print("="*70)
    
    pages = load_pages()
    print(f"Loaded {len(pages)} pages")
    
    # Page 18 is decrypted (PARABLE text)
    parable_text = pages[18] if len(pages) > 18 else ""
    print(f"\nDecrypted Page 18 (first 100 chars): {parable_text[:100]}")
    
    # Use Page 0 as test
    test_page = pages[0]
    print(f"\nTest Page 0 (first 100 chars): {test_page[:100]}")
    
    # Run analyses
    analyze_word_patterns(pages[:18])  # Only encrypted pages
    
    analyze_repeated_sequences(''.join(pages[:18]))
    
    try_running_key_with_parable(test_page, parable_text)
    
    try_prime_index_gematria(test_page)
    
    try_cumulative_gematria(test_page)
    
    try_differential_analysis(test_page)
    
    analyze_acrostic(pages)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

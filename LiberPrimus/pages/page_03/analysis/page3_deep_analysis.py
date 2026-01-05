#!/usr/bin/env python3
"""
DEEP ANALYSIS OF PAGE 3 - LIBER PRIMUS

This script investigates multiple approaches to properly decode Page 3:
1. Master key with different offsets
2. Word boundary analysis
3. Known plaintext attacks
4. Second layer detection
"""

import sys
from pathlib import Path
from collections import Counter

# ============================================================================
# CONSTANTS
# ============================================================================

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# The 95-length master key from community research
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def indices_to_text(indices):
    """Convert indices to text"""
    return "".join(LETTERS[i] for i in indices)

def text_to_indices(text):
    """Convert text to indices"""
    result = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph in LETTERS:
                result.append(LETTERS.index(digraph))
                i += 2
                continue
        # Single letter
        if text[i] in LETTERS:
            result.append(LETTERS.index(text[i]))
        i += 1
    return result

def decrypt_sub(cipher, key, offset=0):
    """SUB decryption: plaintext = (cipher - key) mod 29"""
    plaintext = []
    for i, c in enumerate(cipher):
        k = key[(i + offset) % len(key)]
        plaintext.append((c - k) % 29)
    return plaintext

def encrypt_sub(plaintext, key, offset=0):
    """ADD encryption: cipher = (plaintext + key) mod 29"""
    cipher = []
    for i, p in enumerate(plaintext):
        k = key[(i + offset) % len(key)]
        cipher.append((p + k) % 29)
    return cipher

def score_english(text):
    """Score text for English-likeness"""
    text = text.upper()
    score = 0.0
    
    # Trigrams
    trigrams = {
        'THE': 50, 'AND': 30, 'ING': 25, 'ION': 20, 'ENT': 15,
        'FOR': 15, 'TIO': 15, 'ERE': 15, 'HER': 15, 'ATE': 15,
        'VER': 12, 'TER': 12, 'THA': 12, 'ATI': 12, 'HAT': 12,
        'ITH': 12, 'WIT': 12, 'HIS': 12, 'OUR': 12, 'ALL': 12,
        'NOT': 12, 'ARE': 12, 'WAS': 12, 'HAS': 12, 'ONE': 12,
    }
    
    for i in range(len(text) - 2):
        tg = text[i:i+3]
        if tg in trigrams:
            score += trigrams[tg]
    
    # Bigrams
    bigrams = {
        'TH': 20, 'HE': 18, 'IN': 15, 'ER': 14, 'AN': 13,
        'RE': 12, 'ON': 11, 'AT': 11, 'EN': 10, 'ND': 10,
        'TI': 10, 'ES': 10, 'OR': 10, 'TE': 10, 'OF': 10,
    }
    
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        if bg in bigrams:
            score += bigrams[bg]
    
    # Cicada-specific keywords
    keywords = {
        'WISDOM': 100, 'TRUTH': 100, 'DIVINE': 100, 'EMERGE': 100,
        'INSTAR': 120, 'CIRCUMFERENCE': 150, 'KNOWLEDGE': 100,
        'PARABLE': 100, 'CICADA': 120, 'PRIMES': 100, 'SACRED': 100,
        'WITHIN': 80, 'PILGRIM': 100, 'JOURNEY': 80, 'SHADOW': 80,
        'INSTRUCTION': 100, 'COMMAND': 80, 'BELIEVE': 80,
    }
    
    for kw, bonus in keywords.items():
        score += text.count(kw) * bonus
    
    return score

# ============================================================================
# LOAD PAGE 3
# ============================================================================

def load_page3():
    """Load Page 3 from the transcription file"""
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by page separator
    pages = content.split('%')
    
    # Page 3 is the 3rd segment (0-indexed: 2)
    if len(pages) > 2:
        page3_raw = pages[2]
        indices = [RUNE_TO_INDEX[c] for c in page3_raw if c in RUNE_TO_INDEX]
        
        # Also get word boundaries
        words = []
        current_word = []
        for c in page3_raw:
            if c in RUNE_TO_INDEX:
                current_word.append(RUNE_TO_INDEX[c])
            elif c == '-' and current_word:
                words.append(current_word)
                current_word = []
        if current_word:
            words.append(current_word)
        
        return {
            'indices': indices,
            'words': words,
            'raw': page3_raw,
            'length': len(indices)
        }
    
    raise ValueError("Page 3 not found")

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def try_master_key_offsets(cipher):
    """Try the master key with different offsets"""
    print("\n" + "=" * 80)
    print("TEST 1: MASTER KEY WITH DIFFERENT OFFSETS")
    print("=" * 80)
    
    results = []
    for offset in range(95):
        plaintext = decrypt_sub(cipher, MASTER_KEY, offset)
        text = indices_to_text(plaintext)
        score = score_english(text)
        results.append((offset, score, text))
    
    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop 10 offsets:")
    for offset, score, text in results[:10]:
        print(f"  Offset {offset:2d}: Score {score:6.1f} | {text[:80]}...")
    
    return results[0]

def try_known_plaintexts(cipher):
    """Try known Liber Primus opening phrases as known-plaintext attacks"""
    print("\n" + "=" * 80)
    print("TEST 2: KNOWN PLAINTEXT ATTACKS")
    print("=" * 80)
    
    # Known openings from solved pages
    known_starts = [
        "SOMEWISDOM",
        "APARABLE",
        "AKOAN",
        "ANINSTRUCTION",
        "WELCOMEPILGRIM",
        "ITISTHROUGH",
        "THEPRIMES",
        "LIKETHE",
        "DIVINITYWITHIN",
        "WEMUST",
        "COMMANDYOUR",
        "JOURNEY",
    ]
    
    results = []
    for known in known_starts:
        known_indices = text_to_indices(known)
        if len(known_indices) < 5:
            continue
        
        # Derive key from known plaintext: key = (cipher - plaintext) mod 29
        key_fragment = []
        for i in range(min(len(known_indices), len(cipher))):
            k = (cipher[i] - known_indices[i]) % 29
            key_fragment.append(k)
        
        # Try extending this key
        # If key length is prime, test common primes
        for key_len in [71, 73, 79, 83, 89, 97, 101, 103, 107, 109]:
            if len(key_fragment) > key_len:
                continue
            
            # Build a test key by repeating the fragment
            test_key = (key_fragment * ((key_len // len(key_fragment)) + 1))[:key_len]
            
            plaintext = decrypt_sub(cipher, test_key)
            text = indices_to_text(plaintext)
            score = score_english(text)
            
            results.append((known, key_len, score, text))
    
    results.sort(key=lambda x: x[2], reverse=True)
    
    print("\nTop 10 known-plaintext attempts:")
    for known, klen, score, text in results[:10]:
        print(f"  '{known}' klen={klen}: Score {score:6.1f} | {text[:60]}...")
    
    return results[0] if results else None

def analyze_word_boundaries(page_data):
    """Analyze the word structure of Page 3"""
    print("\n" + "=" * 80)
    print("TEST 3: WORD BOUNDARY ANALYSIS")
    print("=" * 80)
    
    words = page_data['words']
    print(f"\nTotal words: {len(words)}")
    print(f"Total runes: {page_data['length']}")
    
    # Word length distribution
    lengths = [len(w) for w in words]
    print(f"\nWord length distribution:")
    for length in sorted(set(lengths)):
        count = lengths.count(length)
        print(f"  {length} runes: {count} words")
    
    # First few words
    print(f"\nFirst 10 words (as rune indices):")
    for i, word in enumerate(words[:10], 1):
        text = indices_to_text(word)
        print(f"  Word {i}: {word} -> {text}")
    
    return words

def try_prime_key_lengths(cipher):
    """Try various prime key lengths with IoC optimization"""
    print("\n" + "=" * 80)
    print("TEST 4: PRIME KEY LENGTHS WITH IOC ANALYSIS")
    print("=" * 80)
    
    from collections import Counter
    
    def compute_ioc(indices, key_length):
        if key_length < 1 or key_length >= len(indices):
            return 0.0
        
        cosets = [[] for _ in range(key_length)]
        for i, idx in enumerate(indices):
            cosets[i % key_length].append(idx)
        
        ioc_sum = 0.0
        valid = 0
        for coset in cosets:
            n = len(coset)
            if n < 2:
                continue
            freqs = Counter(coset)
            ioc = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
            ioc_sum += ioc
            valid += 1
        
        return ioc_sum / valid if valid > 0 else 0.0
    
    # Test primes from 31 to 127
    primes = [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
    
    print("\nIoC for prime key lengths:")
    results = []
    for p in primes:
        if p < len(cipher):
            ioc = compute_ioc(cipher, p)
            results.append((p, ioc))
            print(f"  Key={p:3d}: IoC={ioc:.6f}")
    
    return results

def search_second_layer(plaintext_indices):
    """Search for a second cipher layer in the plaintext"""
    print("\n" + "=" * 80)
    print("TEST 5: SECOND LAYER DETECTION")
    print("=" * 80)
    
    text = indices_to_text(plaintext_indices)
    
    # Caesar shift analysis
    print("\nCaesar shifts:")
    for shift in range(29):
        shifted = [(p + shift) % 29 for p in plaintext_indices]
        shifted_text = indices_to_text(shifted)
        score = score_english(shifted_text)
        if score > 500:
            print(f"  Shift {shift:2d}: Score {score:6.1f} | {shifted_text[:60]}...")
    
    # Reverse the text
    reversed_text = indices_to_text(plaintext_indices[::-1])
    rev_score = score_english(reversed_text)
    print(f"\nReversed text: Score {rev_score:.1f} | {reversed_text[:60]}...")
    
    # Every-Nth extraction (interleaving)
    print("\nInterleaving analysis:")
    for n in range(2, 6):
        for offset in range(n):
            stream = plaintext_indices[offset::n]
            if len(stream) > 20:
                stream_text = indices_to_text(stream)
                score = score_english(stream_text)
                if score > 200:
                    print(f"  Every {n}th from offset {offset}: Score {score:6.1f} | {stream_text[:50]}...")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("DEEP ANALYSIS: LIBER PRIMUS PAGE 3")
    print("=" * 80)
    
    # Load Page 3
    page3 = load_page3()
    cipher = page3['indices']
    
    print(f"\nPage 3 loaded: {len(cipher)} runes")
    
    # Run analyses
    try_master_key_offsets(cipher)
    try_known_plaintexts(cipher)
    analyze_word_boundaries(page3)
    try_prime_key_lengths(cipher)
    
    # Use the known-best key (83) and analyze second layer
    print("\n" + "=" * 80)
    print("ANALYZING BEST KEY (LENGTH 83)")
    print("=" * 80)
    
    # Generate key via frequency method
    key83 = []
    for i in range(83):
        coset = [cipher[j] for j in range(i, len(cipher), 83)]
        if coset:
            most_common = Counter(coset).most_common(1)[0][0]
            key83.append((most_common - 18) % 29)  # Assume E is most common
        else:
            key83.append(0)
    
    plaintext83 = decrypt_sub(cipher, key83)
    text83 = indices_to_text(plaintext83)
    score83 = score_english(text83)
    
    print(f"\nKey length 83:")
    print(f"  Score: {score83:.1f}")
    print(f"  Text: {text83}")
    
    search_second_layer(plaintext83)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

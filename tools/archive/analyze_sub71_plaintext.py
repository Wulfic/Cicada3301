#!/usr/bin/env python3
"""
Analyze the SUB-71 plaintext for secondary patterns
Tests: acrostic, every-Nth-character, positional encoding, gematria
"""

import sys
from pathlib import Path

# Simple inline implementations
ALPHABET = "FVÐOEAISGYHTLRMPNBKWJXZQC"

def text_to_indices(text):
    return [ALPHABET.index(c) if c in ALPHABET else -1 for c in text.upper()]

def indices_to_text(indices):
    return ''.join(ALPHABET[i] if 0 <= i < len(ALPHABET) else '?' for i in indices)

def compute_trigram_score(text):
    """Simple trigram scoring based on common English patterns"""
    if len(text) < 3:
        return 0.0
    
    # Common English trigrams with weights
    common_trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8,
        'ERS': 7, 'HIS': 7, 'RES': 7, 'ILL': 7, 'ARE': 7,
        'CON': 6, 'NCE': 6, 'THI': 6, 'WIT': 6, 'YOU': 6
    }
    
    # Common bigrams
    common_bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TI': 6, 'ES': 6, 'OR': 6, 'TE': 6, 'OF': 6
    }
    
    score = 0.0
    
    # Score trigrams
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in common_trigrams:
            score += common_trigrams[trigram]
    
    # Score bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in common_bigrams:
            score += common_bigrams[bigram]
    
    return score

# The SUB-71 decrypted plaintext
PLAINTEXT = "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTHMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN"

def test_acrostic(text, step=1):
    """Extract every-Nth-character starting from position 0"""
    result = text[::step]
    score = compute_trigram_score(result)
    return result, score

def test_positional_patterns(text):
    """Test various positional extraction patterns"""
    results = []
    
    # Every Nth character, all starting positions
    for n in range(2, 21):
        for offset in range(n):
            extracted = text[offset::n]
            if len(extracted) < 10:
                continue
            score = compute_trigram_score(extracted)
            results.append({
                'pattern': f'every-{n}th from offset {offset}',
                'length': len(extracted),
                'score': score,
                'text': extracted[:100],
                'full_text': extracted
            })
    
    # First/Last N characters
    for n in [3, 5, 7, 10, 15]:
        first_n = text[:n]
        last_n = text[-n:]
        results.append({
            'pattern': f'first {n} chars',
            'length': len(first_n),
            'score': 0,  # Too short to score meaningfully
            'text': first_n,
            'full_text': first_n
        })
        results.append({
            'pattern': f'last {n} chars',
            'length': len(last_n),
            'score': 0,
            'text': last_n,
            'full_text': last_n
        })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def test_word_extraction(text):
    """Try to identify word boundaries based on patterns"""
    # Look for capitalization patterns (if any)
    # Look for repeated short sequences
    words = []
    current = ""
    
    # Simple strategy: extract sequences that look like words
    # This is a heuristic for fragmented text
    for char in text:
        current += char
        # Common word endings
        if current.endswith(('THE', 'ING', 'AND', 'WITH', 'THAT', 'FROM')):
            if len(current) >= 3:
                words.append(current)
            current = ""
    
    if current:
        words.append(current)
    
    return words

def analyze_gematria(text):
    """Check if indices form numeric patterns"""
    indices = text_to_indices(text)
    
    # Sum of all indices
    total = sum(indices)
    
    # Look for patterns in cumulative sums
    cumsum = []
    running = 0
    for idx in indices:
        running += idx
        cumsum.append(running)
    
    # Check for multiples of special numbers (29, 71, 95, 137, etc.)
    special_nums = [29, 71, 95, 137, 255, 314]
    modulos = {num: [i for i, val in enumerate(cumsum) if val % num == 0] 
               for num in special_nums}
    
    return {
        'total_sum': total,
        'mean_index': total / len(indices),
        'cumsum_last': cumsum[-1],
        'special_positions': modulos
    }

def main():
    print("=" * 80)
    print("SUB-71 PLAINTEXT ANALYSIS")
    print("=" * 80)
    print(f"\nPlaintext length: {len(PLAINTEXT)}")
    print(f"First 100 chars: {PLAINTEXT[:100]}")
    print(f"Last 50 chars: {PLAINTEXT[-50:]}")
    
    # 1. Test acrostic patterns
    print("\n" + "=" * 80)
    print("1. ACROSTIC PATTERNS (every-Nth-character)")
    print("=" * 80)
    
    for n in [2, 3, 4, 5, 7, 10, 71]:
        result, score = test_acrostic(PLAINTEXT, n)
        print(f"\nEvery {n}th char: (score: {score:.2f}, length: {len(result)})")
        print(f"  {result[:80]}")
        if score > 100:
            print(f"  ** HIGH SCORE - Full text: {result}")
    
    # 2. Comprehensive positional analysis
    print("\n" + "=" * 80)
    print("2. POSITIONAL EXTRACTION (Top 15 by score)")
    print("=" * 80)
    
    patterns = test_positional_patterns(PLAINTEXT)
    for i, p in enumerate(patterns[:15], 1):
        print(f"\n#{i}: {p['pattern']}")
        print(f"  Score: {p['score']:.2f}, Length: {p['length']}")
        print(f"  Text: {p['text']}")
        if p['score'] > 150:
            print(f"  ** VERY HIGH SCORE - Full: {p['full_text']}")
    
    # 3. Word extraction attempt
    print("\n" + "=" * 80)
    print("3. WORD EXTRACTION (common endings)")
    print("=" * 80)
    
    words = test_word_extraction(PLAINTEXT)
    print(f"Found {len(words)} potential words:")
    for word in words[:20]:
        print(f"  {word}")
    
    # 4. Gematria analysis
    print("\n" + "=" * 80)
    print("4. GEMATRIA PATTERNS")
    print("=" * 80)
    
    gem = analyze_gematria(PLAINTEXT)
    print(f"Total sum of indices: {gem['total_sum']}")
    print(f"Mean index value: {gem['mean_index']:.2f}")
    print(f"Cumulative sum at end: {gem['cumsum_last']}")
    
    print("\nPositions where cumsum is divisible by special numbers:")
    for num, positions in gem['special_positions'].items():
        if positions:
            print(f"  Divisible by {num}: {len(positions)} positions")
            if len(positions) <= 10:
                print(f"    Positions: {positions}")
    
    # 5. Repeating pattern analysis
    print("\n" + "=" * 80)
    print("5. REPEATING PATTERNS")
    print("=" * 80)
    
    # Look for repeated n-grams
    for n in [3, 4, 5]:
        ngrams = {}
        for i in range(len(PLAINTEXT) - n + 1):
            ngram = PLAINTEXT[i:i+n]
            if ngram in ngrams:
                ngrams[ngram].append(i)
            else:
                ngrams[ngram] = [i]
        
        repeated = {k: v for k, v in ngrams.items() if len(v) > 1}
        if repeated:
            print(f"\nRepeated {n}-grams (appearing 2+ times):")
            sorted_repeated = sorted(repeated.items(), key=lambda x: len(x[1]), reverse=True)
            for ngram, positions in sorted_repeated[:10]:
                print(f"  '{ngram}': {len(positions)} times at {positions}")
    
    # 6. Check for embedded keywords
    print("\n" + "=" * 80)
    print("6. EMBEDDED KEYWORDS FROM PARABLE")
    print("=" * 80)
    
    keywords = [
        'WISDOM', 'KNOWLEDGE', 'TRUTH', 'PATH', 'SEEK', 'FIND',
        'HIDDEN', 'SECRET', 'DIVINE', 'ETERNAL', 'LIGHT', 'DARK',
        'GOOD', 'EVIL', 'VIRTUE', 'CICADA', 'PRIMUS', 'RUNE'
    ]
    
    found_keywords = []
    for keyword in keywords:
        if keyword in PLAINTEXT:
            positions = [i for i in range(len(PLAINTEXT)) if PLAINTEXT.startswith(keyword, i)]
            found_keywords.append((keyword, positions))
            print(f"  '{keyword}' found at positions: {positions}")
    
    if not found_keywords:
        print("  No Parable keywords found embedded directly")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nKey findings:")
    print("1. Check acrostic patterns with high scores (>100)")
    print("2. Check positional extractions with very high scores (>150)")
    print("3. Review repeated patterns for structure clues")
    print("4. Consider if gematria sums have significance")

if __name__ == '__main__':
    main()

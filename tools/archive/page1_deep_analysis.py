#!/usr/bin/env python3
"""
Deep analysis of Page 1 SUB-71 output to extract readable English
The current output has too many E's and fragments - needs further processing
"""

import os
from collections import Counter
from pathlib import Path

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_page1():
    """Load Page 1"""
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_runes = segments[0]
    page1_indices = [RUNE_TO_INDEX[c] for c in page1_runes if c in RUNE_TO_INDEX]
    
    return page1_indices

def decrypt_sub(cipher_indices, key_indices):
    """Decrypt with SUB"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert indices to text"""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """Score English-likeness"""
    text = text.upper()
    
    common_trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8
    }
    
    common_bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7
    }
    
    score = 0.0
    
    for i in range(len(text) - 2):
        if text[i:i+3] in common_trigrams:
            score += common_trigrams[text[i:i+3]]
    
    for i in range(len(text) - 1):
        if text[i:i+2] in common_bigrams:
            score += common_bigrams[text[i:i+2]]
    
    return score

# Best key from previous optimization
BEST_KEY_71 = [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7]

def test_all_extractions(plaintext_indices):
    """Test every possible extraction pattern"""
    plaintext_text = indices_to_text(plaintext_indices)
    
    results = []
    
    # Test every-Nth with all offsets
    for n in range(2, 30):
        for offset in range(n):
            if offset >= len(plaintext_indices):
                continue
            extracted_indices = plaintext_indices[offset::n]
            if len(extracted_indices) < 20:
                continue
            extracted_text = indices_to_text(extracted_indices)
            score = score_english(extracted_text)
            
            results.append({
                'pattern': f'every-{n}th from offset {offset}',
                'n': n,
                'offset': offset,
                'length': len(extracted_text),
                'score': score,
                'text': extracted_text,
                'indices': extracted_indices
            })
    
    # Test reading backwards
    reversed_text = plaintext_text[::-1]
    reversed_indices = plaintext_indices[::-1]
    results.append({
        'pattern': 'reversed',
        'n': 1,
        'offset': 0,
        'length': len(reversed_text),
        'score': score_english(reversed_text),
        'text': reversed_text,
        'indices': reversed_indices
    })
    
    # Test removing all E's
    no_e_indices = [idx for idx in plaintext_indices if idx != 18]  # 18 = E
    no_e_text = indices_to_text(no_e_indices)
    results.append({
        'pattern': 'removed all E',
        'n': 1,
        'offset': 0,
        'length': len(no_e_text),
        'score': score_english(no_e_text),
        'text': no_e_text,
        'indices': no_e_indices
    })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def test_secondary_transformations(plaintext_indices):
    """Test if plaintext needs secondary transformation"""
    results = []
    
    # Test Caesar shifts on plaintext
    for shift in range(1, 29):
        shifted = [(idx + shift) % 29 for idx in plaintext_indices]
        text = indices_to_text(shifted)
        score = score_english(text)
        if score > 200:
            results.append({
                'type': f'Caesar shift +{shift}',
                'score': score,
                'text': text
            })
    
    # Test Atbash (reverse alphabet)
    atbash = [28 - idx for idx in plaintext_indices]
    text = indices_to_text(atbash)
    score = score_english(text)
    results.append({
        'type': 'Atbash (reverse alphabet)',
        'score': score,
        'text': text
    })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def analyze_character_frequency(plaintext_indices):
    """Analyze what's wrong with the frequency distribution"""
    freq = Counter(plaintext_indices)
    
    print("\nCharacter frequency (top 10):")
    for idx, count in freq.most_common(10):
        letter = LETTERS[idx]
        pct = 100 * count / len(plaintext_indices)
        print(f"  {letter:5s} (index {idx:2d}): {count:3d} times ({pct:5.1f}%)")
    
    # Expected English frequencies
    expected = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
        'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3
    }
    
    print("\nExpected English frequencies:")
    for letter, pct in list(expected.items())[:5]:
        print(f"  {letter}: {pct}%")

def main():
    print("=" * 80)
    print("PAGE 1 - DEEP ANALYSIS FOR READABLE ENGLISH")
    print("=" * 80)
    
    cipher_indices = load_page1()
    plaintext_indices = decrypt_sub(cipher_indices, BEST_KEY_71)
    plaintext_text = indices_to_text(plaintext_indices)
    
    print(f"\nCurrent SUB-71 output (length {len(plaintext_text)}):")
    print(plaintext_text)
    
    base_score = score_english(plaintext_text)
    print(f"\nBase score: {base_score:.2f}")
    
    # Analyze frequency
    print("\n" + "=" * 80)
    print("CHARACTER FREQUENCY ANALYSIS")
    print("=" * 80)
    analyze_character_frequency(plaintext_indices)
    
    # Test all extractions
    print("\n" + "=" * 80)
    print("TESTING ALL EXTRACTION PATTERNS")
    print("=" * 80)
    
    extraction_results = test_all_extractions(plaintext_indices)
    
    print(f"\nTop 30 patterns by score:")
    print(f"{'Rank':<6} {'Pattern':<35} {'Score':<10} {'Length':<8} {'Preview'}")
    print("-" * 100)
    
    for i, r in enumerate(extraction_results[:30], 1):
        preview = r['text'][:60].replace('\n', ' ')
        print(f"{i:<6} {r['pattern']:<35} {r['score']:<10.2f} {r['length']:<8} {preview}")
    
    # Show best result in detail
    if extraction_results:
        best = extraction_results[0]
        print("\n" + "=" * 80)
        print(f"BEST PATTERN: {best['pattern']}")
        print("=" * 80)
        print(f"Score: {best['score']:.2f} (vs base {base_score:.2f})")
        print(f"Length: {best['length']}")
        print(f"\nFull text:")
        print(best['text'])
    
    # Test secondary transformations
    print("\n" + "=" * 80)
    print("TESTING SECONDARY TRANSFORMATIONS")
    print("=" * 80)
    
    transform_results = test_secondary_transformations(plaintext_indices)
    
    if transform_results:
        print(f"\nTop 10 transformations:")
        for i, r in enumerate(transform_results[:10], 1):
            print(f"\n{i}. {r['type']}")
            print(f"   Score: {r['score']:.2f}")
            print(f"   Preview: {r['text'][:80]}")
    
    # Look for repeated sequences that might be noise
    print("\n" + "=" * 80)
    print("PATTERN DETECTION")
    print("=" * 80)
    
    # Find runs of E's
    e_runs = []
    current_run = 0
    for idx in plaintext_indices:
        if idx == 18:  # E
            current_run += 1
        else:
            if current_run > 0:
                e_runs.append(current_run)
            current_run = 0
    
    if e_runs:
        print(f"\nRuns of E's found: {len(e_runs)}")
        print(f"Longest run: {max(e_runs)} E's")
        print(f"Average run: {sum(e_runs)/len(e_runs):.1f} E's")
        print(f"Total E's in runs: {sum(e_runs)} out of {len(plaintext_indices)} chars ({100*sum(e_runs)/len(plaintext_indices):.1f}%)")
    
    # Test removing consecutive E's (keep only first)
    dedupe_indices = []
    prev_idx = -1
    for idx in plaintext_indices:
        if idx == 18 and prev_idx == 18:  # Skip consecutive E's
            continue
        dedupe_indices.append(idx)
        prev_idx = idx
    
    dedupe_text = indices_to_text(dedupe_indices)
    dedupe_score = score_english(dedupe_text)
    
    print(f"\n" + "=" * 80)
    print("DEDUPED TEXT (removed consecutive E's)")
    print("=" * 80)
    print(f"Original length: {len(plaintext_text)}")
    print(f"Deduped length: {len(dedupe_text)}")
    print(f"Removed: {len(plaintext_text) - len(dedupe_text)} characters")
    print(f"Score: {dedupe_score:.2f} (vs base {base_score:.2f})")
    print(f"\nText:\n{dedupe_text}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    best_overall = max(
        [{'name': 'Base', 'score': base_score, 'text': plaintext_text}] +
        [{'name': r['pattern'], 'score': r['score'], 'text': r['text']} for r in extraction_results[:5]] +
        [{'name': 'Deduped', 'score': dedupe_score, 'text': dedupe_text}],
        key=lambda x: x['score']
    )
    
    print(f"\nBest result: {best_overall['name']}")
    print(f"Score: {best_overall['score']:.2f}")
    print(f"\nText:\n{best_overall['text']}")
    
    # Check if this looks like readable English
    words_found = []
    for word in ['THE', 'AND', 'OF', 'TO', 'IN', 'A', 'IS', 'THAT', 'FOR', 'IT', 'WITH', 'AS', 'WAS']:
        if word in best_overall['text']:
            count = best_overall['text'].count(word)
            words_found.append(f"{word}({count})")
    
    if words_found:
        print(f"\nCommon English words found: {', '.join(words_found)}")
    else:
        print(f"\n⚠️ WARNING: No common English words found")
        print("This suggests the plaintext may need:")
        print("  - A different key or key length")
        print("  - Additional transformation layer")
        print("  - Non-standard plaintext (cipher-speak, Latin, etc.)")

if __name__ == '__main__':
    main()

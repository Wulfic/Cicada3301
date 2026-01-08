#!/usr/bin/env python3
"""
Prime Number Section Decryption Test
=====================================
Based on the discovery that pages contain numbered sections (1-5, 7),
and the Cicada clue "THE PRIMES ARE SACRED", test if:

1. The section number N indicates to use the Nth prime as a key
2. The section number itself relates to the Gematria prime value
3. Combined sections form a readable message when properly decrypted

Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...
  Section 1 -> 2 (1st prime)
  Section 2 -> 3 (2nd prime)
  Section 3 -> 5 (3rd prime)
  Section 4 -> 7 (4th prime)
  Section 5 -> 11 (5th prime)
  Section 6 -> 13 (6th prime) [MISSING!]
  Section 7 -> 17 (7th prime)
"""

import os
import re
from collections import Counter

# Gematria Primus
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N',
                   'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                   'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# First 20 primes
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

def runes_to_indices(rune_text):
    """Convert rune text to indices."""
    return [RUNE_TO_INDEX[c] for c in rune_text if c in RUNE_TO_INDEX]

def indices_to_text(indices):
    """Convert indices to readable text."""
    return ''.join(INDEX_TO_LETTER[i] for i in indices)

def load_page_runes(page_num):
    """Load runes from a page file."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if os.path.exists(rune_path):
        with open(rune_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def extract_section_content(content, section_num):
    """Extract full content of a numbered section."""
    pattern = rf'{section_num}[-–](.+?)(?:(?:\d[-–])|(?:\n&)|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def score_english(text):
    """Score text for English-likeness."""
    text = text.upper()
    score = 0
    
    # Bigrams
    bigrams = {'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10, 'RE': 9, 'ON': 8}
    for bg, val in bigrams.items():
        score += text.count(bg) * val
    
    # Trigrams
    trigrams = {'THE': 30, 'AND': 20, 'ING': 18}
    for tg, val in trigrams.items():
        score += text.count(tg) * val
    
    return score

def test_prime_decryption():
    """Test using Nth prime as key for section N."""
    print("=" * 70)
    print("PRIME-BASED SECTION DECRYPTION TEST")
    print("=" * 70)
    print("\nHypothesis: Section N uses the Nth prime as decryption key")
    print("Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...")
    print()
    
    sections = {}
    
    # Extract sections
    content_36 = load_page_runes(36)
    content_37 = load_page_runes(37)
    content_38 = load_page_runes(38)
    content_10 = load_page_runes(10)
    
    if content_36:
        sec = extract_section_content(content_36, 1)
        if sec:
            sections[1] = runes_to_indices(sec)
    
    if content_37:
        for n in [2, 3, 4]:
            sec = extract_section_content(content_37, n)
            if sec:
                sections[n] = runes_to_indices(sec)
    
    if content_38:
        sec = extract_section_content(content_38, 5)
        if sec:
            sections[5] = runes_to_indices(sec)
    
    if content_10:
        # Section 7 is special - find content after "7-"
        match = re.search(r'7[-–]([ᚠ-ᛠ\-\.]+)', content_10)
        if match:
            sections[7] = runes_to_indices(match.group(1))
    
    # Test each section with its corresponding prime
    results = {}
    print("\nSECTION-BY-SECTION DECRYPTION:")
    print("-" * 70)
    
    for section_num in sorted(sections.keys()):
        indices = sections[section_num]
        prime = PRIMES[section_num - 1]  # 0-indexed
        prime_mod = prime % 29
        
        print(f"\nSection {section_num}: {len(indices)} runes, using {section_num}th prime = {prime} (mod 29 = {prime_mod})")
        
        # Method 1: Subtract prime mod 29
        dec1 = [(i - prime_mod) % 29 for i in indices]
        text1 = indices_to_text(dec1)
        score1 = score_english(text1)
        
        # Method 2: Subtract section number directly
        dec2 = [(i - section_num) % 29 for i in indices]
        text2 = indices_to_text(dec2)
        score2 = score_english(text2)
        
        # Method 3: Add prime (inverse operation)
        dec3 = [(i + prime_mod) % 29 for i in indices]
        text3 = indices_to_text(dec3)
        score3 = score_english(text3)
        
        # Method 4: Raw (no decryption)
        text0 = indices_to_text(indices)
        score0 = score_english(text0)
        
        print(f"  Raw:              {text0[:40]}... (score: {score0})")
        print(f"  SUB prime({prime}):  {text1[:40]}... (score: {score1})")
        print(f"  SUB section({section_num}):  {text2[:40]}... (score: {score2})")
        print(f"  ADD prime({prime}):  {text3[:40]}... (score: {score3})")
        
        # Find best
        best = max([(score0, 'raw', text0), (score1, f'sub_p{prime}', text1), 
                   (score2, f'sub_s{section_num}', text2), (score3, f'add_p{prime}', text3)])
        results[section_num] = {'text': best[2], 'method': best[1], 'score': best[0]}
    
    # Try combining best results
    print("\n" + "=" * 70)
    print("COMBINED RESULTS (Best method per section)")
    print("=" * 70)
    
    combined = ""
    for section_num in sorted(results.keys()):
        r = results[section_num]
        print(f"Section {section_num} ({r['method']}): {r['text'][:50]}...")
        combined += r['text'] + " | "
    
    print(f"\nCombined text (sections 1-5):")
    combined_15 = ""
    for n in range(1, 6):
        if n in results:
            combined_15 += results[n]['text']
    
    print(f"  {combined_15[:200]}...")
    
    # Check for TH patterns
    th_count = combined_15.count('TH')
    the_count = combined_15.count('THE')
    print(f"\n  TH count: {th_count}")
    print(f"  THE count: {the_count}")
    
    return results

def test_totient_decryption():
    """Test using totient function φ(prime) = prime - 1 as key."""
    print("\n" + "=" * 70)
    print("TOTIENT-BASED SECTION DECRYPTION TEST")
    print("=" * 70)
    print("\nHypothesis: Section N uses φ(Nth prime) = (Nth prime - 1) as key")
    print("Since primes are sacred, and totient is sacred...")
    print()
    
    sections = {}
    
    content_36 = load_page_runes(36)
    content_37 = load_page_runes(37)
    content_38 = load_page_runes(38)
    
    if content_36:
        sec = extract_section_content(content_36, 1)
        if sec:
            sections[1] = runes_to_indices(sec)
    
    if content_37:
        for n in [2, 3, 4]:
            sec = extract_section_content(content_37, n)
            if sec:
                sections[n] = runes_to_indices(sec)
    
    if content_38:
        sec = extract_section_content(content_38, 5)
        if sec:
            sections[5] = runes_to_indices(sec)
    
    print("RESULTS:")
    combined = ""
    for section_num in sorted(sections.keys()):
        indices = sections[section_num]
        prime = PRIMES[section_num - 1]
        totient = prime - 1  # φ(p) = p - 1 for prime p
        totient_mod = totient % 29
        
        # Decrypt with totient
        dec = [(i - totient_mod) % 29 for i in indices]
        text = indices_to_text(dec)
        score = score_english(text)
        
        print(f"\nSection {section_num}: prime={prime}, φ({prime})={totient}, mod29={totient_mod}")
        print(f"  Result: {text[:60]}... (score: {score})")
        combined += text
    
    print(f"\nCombined (sections 1-5):")
    print(f"  {combined[:200]}...")
    print(f"  TH count: {combined.count('TH')}")
    print(f"  THE count: {combined.count('THE')}")

def test_sequential_prime_key():
    """Test using sequential primes as a running key across all sections."""
    print("\n" + "=" * 70)
    print("SEQUENTIAL PRIME RUNNING KEY TEST")
    print("=" * 70)
    print("\nHypothesis: Use first N primes as running key, cycling if needed")
    
    # Collect all section content in order
    all_indices = []
    
    content_36 = load_page_runes(36)
    content_37 = load_page_runes(37)
    content_38 = load_page_runes(38)
    
    if content_36:
        sec = extract_section_content(content_36, 1)
        if sec:
            all_indices.extend(runes_to_indices(sec))
    
    if content_37:
        for n in [2, 3, 4]:
            sec = extract_section_content(content_37, n)
            if sec:
                all_indices.extend(runes_to_indices(sec))
    
    if content_38:
        sec = extract_section_content(content_38, 5)
        if sec:
            all_indices.extend(runes_to_indices(sec))
    
    print(f"\nTotal runes across sections 1-5: {len(all_indices)}")
    
    # Try different running key approaches
    tests = [
        ("First 5 primes cycling", [p % 29 for p in PRIMES[:5]]),
        ("First 7 primes cycling", [p % 29 for p in PRIMES[:7]]),
        ("First 11 primes cycling", [p % 29 for p in PRIMES[:11]]),
        ("Prime indices 0-4", list(range(5))),
        ("Fibonacci mod 29", [0, 1, 1, 2, 3, 5, 8, 13, 21, 5, 26, 2, 28]),
    ]
    
    for name, key in tests:
        decrypted = []
        for i, c in enumerate(all_indices):
            k = key[i % len(key)]
            decrypted.append((c - k) % 29)
        
        text = indices_to_text(decrypted)
        score = score_english(text)
        th = text.count('TH')
        the = text.count('THE')
        
        print(f"\n{name}: (score={score}, TH={th}, THE={the})")
        print(f"  {text[:80]}...")

def main():
    test_prime_decryption()
    test_totient_decryption()
    test_sequential_prime_key()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
KEY FINDINGS:
1. Numbered sections are a UNIQUE feature in Liber Primus
2. The section numbers may indicate:
   - Which prime to use as key (1st prime = 2, 2nd = 3, etc.)
   - Reading order across non-consecutive pages
   - Reference markers for cross-page decryption
3. Missing section 6 suggests intentional gap or hidden content
4. Pages 58-74 need transcription to search for section 6

NEXT STEPS:
1. Transcribe pages 58-74 to find missing section 6
2. Test combinations of section content with prime-based keys
3. Look for visual clues in the page images themselves
4. Consider that sections 1-5 and section 7 may be two different puzzles
""")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Test if Page 6 is the Missing Section 6
========================================
Hypothesis: Since sections 1-5 are on pages 36-38 and section 7 is on page 10,
maybe PAGE 6 represents SECTION 6 (the missing section).

This would mean:
- Section 6 content = all of page 6
- Section 6 key = 6th prime = 13

Let's test this theory and see if page 6 decrypts meaningfully with prime 13.
"""

import os
import sys

# Add tools dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def runes_to_indices(text):
    return [RUNE_TO_INDEX[c] for c in text if c in RUNE_TO_INDEX]

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER[i] for i in indices)

def score_english(text):
    score = 0
    text = text.upper()
    
    bigrams = {'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10}
    for bg, val in bigrams.items():
        score += text.count(bg) * val
    
    trigrams = {'THE': 30, 'AND': 20, 'ING': 18}
    for tg, val in trigrams.items():
        score += text.count(tg) * val
    
    return score

def load_page(page_num):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def main():
    print("=" * 70)
    print("TESTING: IS PAGE 6 THE MISSING SECTION 6?")
    print("=" * 70)
    
    # Load page 6
    content = load_page(6)
    if not content:
        print("ERROR: Could not load page 6")
        return
    
    indices = runes_to_indices(content)
    print(f"\nPage 6 has {len(indices)} runes")
    
    # Raw transliteration
    raw = indices_to_text(indices)
    raw_score = score_english(raw)
    print(f"\nRaw transliteration (score={raw_score}):")
    print(f"  {raw[:80]}...")
    
    # Test with 6th prime = 13
    sixth_prime = 13
    sixth_prime_mod = 13 % 29
    
    dec_p6 = [(i - sixth_prime_mod) % 29 for i in indices]
    text_p6 = indices_to_text(dec_p6)
    score_p6 = score_english(text_p6)
    
    print(f"\nWith 6th prime (13) as key, SUB mod 29 (score={score_p6}):")
    print(f"  {text_p6[:80]}...")
    print(f"  TH count: {text_p6.count('TH')}, THE count: {text_p6.count('THE')}")
    
    # Test with totient of 6th prime = 12
    totient_6 = 12
    dec_t6 = [(i - totient_6) % 29 for i in indices]
    text_t6 = indices_to_text(dec_t6)
    score_t6 = score_english(text_t6)
    
    print(f"\nWith φ(13)=12 as key (score={score_t6}):")
    print(f"  {text_t6[:80]}...")
    print(f"  TH count: {text_t6.count('TH')}, THE count: {text_t6.count('THE')}")
    
    # Test with just 6 as key
    dec_6 = [(i - 6) % 29 for i in indices]
    text_6 = indices_to_text(dec_6)
    score_6 = score_english(text_6)
    
    print(f"\nWith just 6 as key (score={score_6}):")
    print(f"  {text_6[:80]}...")
    print(f"  TH count: {text_6.count('TH')}, THE count: {text_6.count('THE')}")
    
    # Compare with what we found for other sections
    print("\n" + "=" * 70)
    print("COMPARISON WITH OTHER SECTIONS")
    print("=" * 70)
    
    # Section 1 (page 36) with 1st prime = 2
    content_36 = load_page(36)
    if content_36:
        # Find section after "1-"
        import re
        match = re.search(r'1[-–](.+?)(?:\n&|$)', content_36, re.DOTALL)
        if match:
            sec1_indices = runes_to_indices(match.group(1))
            dec1 = [(i - 2) % 29 for i in sec1_indices]  # 1st prime = 2
            text1 = indices_to_text(dec1)
            print(f"\nSection 1 (prime 2): {text1[:50]}... (TH={text1.count('TH')})")
    
    # Section 5 (page 38) with 5th prime = 11
    content_38 = load_page(38)
    if content_38:
        match = re.search(r'5[-–](.+?)(?:\n&|$)', content_38, re.DOTALL)
        if match:
            sec5_indices = runes_to_indices(match.group(1))
            dec5 = [(i - 11) % 29 for i in sec5_indices]  # 5th prime = 11
            text5 = indices_to_text(dec5)
            print(f"Section 5 (prime 11): {text5[:50]}... (TH={text5.count('TH')})")
    
    # Section 7 (page 10) with 7th prime = 17
    content_10 = load_page(10)
    if content_10:
        match = re.search(r'7[-–]([ᚠ-ᛠ\-\.]+)', content_10)
        if match:
            sec7_indices = runes_to_indices(match.group(1))
            dec7 = [(i - 17) % 29 for i in sec7_indices]  # 7th prime = 17
            text7 = indices_to_text(dec7)
            print(f"Section 7 (prime 17): {text7[:50]}... (TH={text7.count('TH')})")
    
    # Now test page 6 with same approach
    print(f"\nPage 6 as Section 6 (prime 13): {text_p6[:50]}... (TH={text_p6.count('TH')})")
    
    # Final verdict
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    
    if score_p6 > raw_score:
        print("✓ Decrypting with 6th prime (13) IMPROVES the score!")
        print("  This supports the hypothesis that page 6 = section 6")
    else:
        print("✗ Decrypting with 6th prime (13) does NOT improve the score")
        print("  Page 6 may not be section 6, or uses a different method")
    
    print(f"""
NOTES:
- Page 6 has {len(indices)} runes
- Sections 1-5 have roughly 20-140 runes each
- Page 6 is longer than typical numbered sections
- The missing '6-' marker suggests page 6 is NOT formatted like sections 1-5
- ALTERNATIVE: Section 6 might be on untranscribed pages 58-74
- ALTERNATIVE: "6" might reference prime index 6 = 13, used elsewhere
""")

if __name__ == '__main__':
    main()

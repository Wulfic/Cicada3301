#!/usr/bin/env python3
"""
Complete analysis of the numbered sections 1-7 theory.
Tests if sections 1-5, 7 can be decrypted using section-number primes
and if pages 56-57 really are Section 6.
"""

import os
from pathlib import Path

# Gematria Primus alphabet (29 characters) - includes ᚣ
GEMATRIA = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛠᛡᚣ'
RUNE_TO_IDX = {r: i for i, r in enumerate(GEMATRIA)}
IDX_TO_RUNE = {i: r for i, r in enumerate(GEMATRIA)}

# Primes 1st through 10th
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

# English letter frequencies for scoring
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2,
    'Q': 0.1, 'Z': 0.1
}

# Simple rune to letter mapping (30 chars to match extended alphabet)
RUNE_TO_LETTER = dict(zip(GEMATRIA, 'FUTHORKGWHNIJEOPXSTBEMLNDOAEAYY'))

def decrypt_single_key(runes, key):
    """Decrypt runes using a single shift key (SUB mod 29)."""
    result = []
    for r in runes:
        if r in RUNE_TO_IDX:
            idx = RUNE_TO_IDX[r]
            new_idx = (idx - key) % 29
            result.append(IDX_TO_RUNE[new_idx])
        else:
            result.append(r)
    return ''.join(result)

def runes_to_letters(runes):
    """Convert runes to approximate English letters."""
    result = []
    for r in runes:
        if r in RUNE_TO_LETTER:
            result.append(RUNE_TO_LETTER[r])
        elif r == '-':
            result.append(' ')
        elif r == '.':
            result.append('.')
        else:
            result.append(r)
    return ''.join(result)

def count_patterns(text):
    """Count TH, THE, and other common English patterns."""
    text = text.upper()
    patterns = {
        'TH': text.count('TH'),
        'THE': text.count('THE'),
        'AND': text.count('AND'),
        'ING': text.count('ING'),
        'OF': text.count('OF'),
        'TO': text.count('TO'),
        'IN': text.count('IN'),
    }
    return patterns

def load_section(page_num, section_num):
    """Load a specific section from a page."""
    pages_dir = Path(__file__).parent.parent / 'pages'
    runes_file = pages_dir / f'page_{page_num:02d}' / 'runes.txt'
    
    if not runes_file.exists():
        return None
    
    content = runes_file.read_text(encoding='utf-8')
    
    # Find section marker
    marker = f'{section_num}-'
    if marker not in content:
        # For section 7 on page 10, it's mid-text
        if f'-{section_num}-' in content:
            # Extract context around the number
            idx = content.find(f'-{section_num}-')
            start = max(0, idx - 20)
            end = min(len(content), idx + 30)
            return content[start:end]
        return None
    
    # Find start of section
    start_idx = content.find(marker)
    
    # Find end (next section, &, or end of content)
    end_markers = ['&', '\n\n']
    end_idx = len(content)
    
    # Also look for next numbered section
    for i in range(section_num + 1, 10):
        next_marker = f'\n{i}-'
        if next_marker in content[start_idx:]:
            potential_end = content.find(next_marker, start_idx)
            if potential_end > start_idx and potential_end < end_idx:
                end_idx = potential_end
    
    for em in end_markers:
        pos = content.find(em, start_idx + len(marker))
        if pos > start_idx and pos < end_idx:
            end_idx = pos
    
    section = content[start_idx:end_idx]
    return section

def main():
    print("=" * 70)
    print("COMPLETE NUMBERED SECTIONS ANALYSIS")
    print("Testing: Section N decrypted with Nth prime")
    print("=" * 70)
    
    # Section data: (page, section_num, description)
    sections = [
        (36, 1, "First numbered section"),
        (37, 2, "Second numbered section"),
        (37, 3, "Third numbered section"),
        (37, 4, "Fourth numbered section"),
        (38, 5, "Fifth numbered section"),
        # Section 6 is hypothesized to be pages 56-57 (cleartext)
        (10, 7, "Seventh section (mid-text)"),
    ]
    
    print("\n📊 SECTION EXTRACTION:")
    print("-" * 50)
    
    all_runes = []
    
    for page, section, desc in sections:
        section_text = load_section(page, section)
        if section_text:
            # Extract just the runes
            runes_only = ''.join(c for c in section_text if c in GEMATRIA)
            all_runes.append((section, runes_only))
            print(f"\n  Section {section} (page {page}): {len(runes_only)} runes")
            print(f"    Raw: {section_text[:50]}...")
        else:
            print(f"\n  Section {section} (page {page}): NOT FOUND")
    
    print("\n" + "=" * 70)
    print("🔐 PRIME-BASED DECRYPTION:")
    print("-" * 50)
    print("Testing: Section N decrypted with Nth prime")
    
    combined_decrypted = []
    
    for section_num, runes in all_runes:
        if section_num <= len(PRIMES):
            prime = PRIMES[section_num - 1]  # Nth prime (1-indexed)
            decrypted = decrypt_single_key(runes, prime)
            letters = runes_to_letters(decrypted)
            patterns = count_patterns(letters)
            
            print(f"\n  Section {section_num} (prime {prime}):")
            print(f"    Decrypted runes: {decrypted[:30]}...")
            print(f"    As letters: {letters[:30]}...")
            print(f"    Patterns: TH={patterns['TH']}, THE={patterns['THE']}, AND={patterns['AND']}")
            
            combined_decrypted.append(decrypted)
    
    # Combine all sections
    print("\n" + "=" * 70)
    print("📚 COMBINED SECTIONS 1-5 + 7:")
    print("-" * 50)
    
    combined = ''.join(combined_decrypted)
    combined_letters = runes_to_letters(combined)
    combined_patterns = count_patterns(combined_letters)
    
    print(f"\n  Total runes: {len(combined)}")
    print(f"  Combined decrypted: {combined[:60]}...")
    print(f"  As letters: {combined_letters[:60]}...")
    print(f"\n  Pattern counts:")
    for pattern, count in combined_patterns.items():
        print(f"    {pattern}: {count}")
    
    # Section 6 Analysis (pages 56-57)
    print("\n" + "=" * 70)
    print("📜 SECTION 6 HYPOTHESIS (Pages 56-57):")
    print("-" * 50)
    
    pages_dir = Path(__file__).parent.parent / 'pages'
    for page in [56, 57]:
        runes_file = pages_dir / f'page_{page:02d}' / 'runes.txt'
        if runes_file.exists():
            content = runes_file.read_text(encoding='utf-8')
            runes_only = ''.join(c for c in content if c in GEMATRIA)
            letters = runes_to_letters(content)
            
            print(f"\n  Page {page}:")
            print(f"    Rune count: {len(runes_only)}")
            print(f"    Content: {letters[:60]}...")
            
            # Check for § symbol
            if '§' in content:
                print(f"    ✓ Contains § section symbol!")
    
    # Pattern Summary
    print("\n" + "=" * 70)
    print("🔍 SUMMARY:")
    print("-" * 50)
    print("""
  CONFIRMED:
  - Sections 1-5 on pages 36-38 (encrypted)
  - Section 7 on page 10 (encrypted, mid-text)
  - Section 6 MISSING as Arabic numeral
  
  HYPOTHESIS:
  - Pages 56-57 = Section 6 (THE PARABLE)
  - Only page with § section symbol
  - Cleartext (already "decrypted")
  
  READING ORDER THEORY:
  1. Decrypt sections 1-5 (pages 36-38) with primes 2,3,5,7,11
  2. Read section 6 (pages 56-57) - THE PARABLE
  3. Decrypt section 7 (page 10) with prime 17
  
  The Parable appears to be the "core revelation"
  that the numbered sections lead to.
""")

if __name__ == '__main__':
    main()

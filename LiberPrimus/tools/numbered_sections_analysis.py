#!/usr/bin/env python3
"""
Numbered Sections Analysis
==========================
DISCOVERY: Pages 36-38 and 10 contain Arabic numerals (1, 2, 3, 4, 5, 7) embedded in rune text!
This is highly unusual in a purely runic text and likely contains important hints.

Pattern:
- Page 36: Contains "1-" starting a section
- Page 37: Contains "2-", "3-", "4-" starting sections
- Page 38: Contains "5-" starting a section  
- Page 10: Contains "7-" in the middle of text

MISSING: Number 6 is not found in any page!

This script:
1. Extracts all numbered sections
2. Analyzes them as separate cipher units
3. Tests if numbers indicate key values
4. Searches for missing number 6
"""

import os
import re
from collections import Counter, defaultdict

# Gematria Primus mapping
RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N',
                   'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
                   'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def runes_to_indices(rune_text):
    """Convert rune text to indices, skipping non-rune characters."""
    indices = []
    for char in rune_text:
        if char in RUNE_TO_INDEX:
            indices.append(RUNE_TO_INDEX[char])
    return indices

def indices_to_text(indices):
    """Convert indices to readable text."""
    return ''.join(INDEX_TO_LETTER[i] for i in indices)

def decrypt_sub(cipher_indices, key):
    """Decrypt using SUB mod 29: plaintext = (cipher - key) mod 29"""
    return [(c - k) % 29 for c, k in zip(cipher_indices, key * (len(cipher_indices) // len(key) + 1))]

def load_page_runes(page_num):
    """Load runes from a page file."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    if os.path.exists(rune_path):
        with open(rune_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def find_numbered_sections():
    """Find all numbered sections across all pages."""
    print("=" * 70)
    print("NUMBERED SECTIONS DISCOVERY")
    print("=" * 70)
    
    numbered_pages = {}
    
    for page_num in range(75):
        content = load_page_runes(page_num)
        if content is None:
            continue
        
        # Find any Arabic numerals
        numbers_found = re.findall(r'(\d+)[-\s]', content)
        if numbers_found:
            numbered_pages[page_num] = numbers_found
            print(f"\nPage {page_num:02d} contains numbers: {numbers_found}")
            
            # Extract section content
            for num in numbers_found:
                # Find the section starting with this number
                pattern = rf'{num}[-–]([ᚠ-ᛠ\-\.]+)'
                matches = re.findall(pattern, content)
                for match in matches:
                    rune_count = len([c for c in match if c in RUNE_TO_INDEX])
                    print(f"  Section {num}: {rune_count} runes")
                    print(f"    Preview: {match[:50]}...")
    
    return numbered_pages

def analyze_numbered_sequence():
    """Analyze the numbered sequence pattern."""
    print("\n" + "=" * 70)
    print("SEQUENCE ANALYSIS")
    print("=" * 70)
    
    # Known numbers: 1, 2, 3, 4, 5, 7
    # Missing: 6
    
    print("""
FOUND NUMBERS:
  Page 36: 1
  Page 37: 2, 3, 4
  Page 38: 5
  Page 10: 7

MISSING: 6

HYPOTHESIS 1: Pages 36-38 form a consecutive sequence (sections 1-5)
HYPOTHESIS 2: Page 10's "7" is part of a different sequence (where is 6?)
HYPOTHESIS 3: The numbers might be KEYS (use number N as key shift)
HYPOTHESIS 4: The numbers indicate reading ORDER across pages

NOTE: Number 6 might be:
  - On a page without transcription (pages 58-74)
  - Encoded differently (as runes for "six"?)
  - Intentionally missing (puzzle clue)
""")

def test_number_as_key():
    """Test if the number before each section is the decryption key."""
    print("\n" + "=" * 70)
    print("TESTING NUMBERS AS KEYS")
    print("=" * 70)
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    test_cases = [
        (36, '1', "ᛚᚦᛇᛟ-ᚪᚫᛠ-ᛗᛉᚻᚳᛉᚪᛏᚦ-ᚫᛉ-ᚩᛋᚳᛞ"),
        (37, '2', "ᚾᚣᛖᛉ-ᚾᚢᛉᛁ-ᛝᛏᛈᚹᛋᚣ-ᛏᛠᛈᛉ-ᚪᛁ"),
        (37, '3', "ᛞᚢᛈ-ᚹᚾᛖᚪ-ᚱᛚᛁᚹ-ᚫᛉ-ᛝᚠᛞᚪᚠ-ᛒᛄᛉ-ᛞ"),
        (37, '4', "ᛝᛄᛋᛄᛗᚱᛗ-ᚾᛒᛋᛗᛉᛞᚻᛉᛁ-ᚣᛡᚻᚣ"),
        (38, '5', "ᚻᚫᛉᚦᛒᛟ-ᛏᛟᚹᛄ-ᚫᛠᛗᚠᚫᚳᚷ-ᛇ-ᚻᚹᛗ"),
        (10, '7', "ᚷ-ᛚᛄᛖᚫ"),  # Content after 7
    ]
    
    for page, num_str, section_runes in test_cases:
        num = int(num_str)
        indices = runes_to_indices(section_runes)
        
        if not indices:
            continue
            
        # Test with number as simple shift key
        decrypted_simple = [(i - num) % 29 for i in indices]
        text_simple = indices_to_text(decrypted_simple)
        
        # Test with Gematria prime value of number
        # Number 1 is not a prime, 2 is first prime (index 0 = F)
        # Let's map: 1->2, 2->3, 3->5, 4->7, 5->11, 6->13, 7->17
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        prime_key = primes[num-1] if num <= len(primes) else num
        decrypted_prime = [(i - prime_key) % 29 for i in indices]
        text_prime = indices_to_text(decrypted_prime)
        
        # Also test with number as key length
        key = [num] * len(indices)
        decrypted_key = decrypt_sub(indices, [num])
        text_key = indices_to_text(decrypted_key)
        
        print(f"\nPage {page}, Section {num}:")
        print(f"  Original runes: {len(indices)} characters")
        print(f"  Direct (shift {num}): {text_simple[:50]}")
        print(f"  Prime (shift {prime_key}): {text_prime[:50]}")
        
        # Check for English patterns
        for text, method in [(text_simple, 'simple'), (text_prime, 'prime')]:
            th_count = text.count('TH')
            the_count = text.count('THE')
            if th_count > 0 or the_count > 0:
                print(f"  * {method}: TH={th_count}, THE={the_count}")

def extract_full_sections():
    """Extract full content of each numbered section."""
    print("\n" + "=" * 70)
    print("FULL SECTION EXTRACTION")
    print("=" * 70)
    
    sections = {}
    
    # Page 36 - Section 1
    content_36 = load_page_runes(36)
    if content_36:
        # Find everything after "1-" until end of content or next section marker
        match = re.search(r'1[-–](.+?)(?:\n&|$)', content_36, re.DOTALL)
        if match:
            section = match.group(1).strip()
            rune_indices = runes_to_indices(section)
            sections['1'] = {
                'page': 36,
                'indices': rune_indices,
                'rune_count': len(rune_indices),
                'text': section[:100]
            }
    
    # Page 37 - Sections 2, 3, 4
    content_37 = load_page_runes(37)
    if content_37:
        for num in ['2', '3', '4']:
            # Find section from number to next number or end
            next_num = str(int(num) + 1) if int(num) < 4 else None
            if next_num:
                pattern = rf'{num}[-–](.+?)(?:{next_num}[-–])'
            else:
                pattern = rf'{num}[-–](.+?)$'
            match = re.search(pattern, content_37, re.DOTALL)
            if match:
                section = match.group(1).strip()
                rune_indices = runes_to_indices(section)
                sections[num] = {
                    'page': 37,
                    'indices': rune_indices,
                    'rune_count': len(rune_indices),
                    'text': section[:100]
                }
    
    # Page 38 - Section 5
    content_38 = load_page_runes(38)
    if content_38:
        match = re.search(r'5[-–](.+?)(?:\n&|$)', content_38, re.DOTALL)
        if match:
            section = match.group(1).strip()
            rune_indices = runes_to_indices(section)
            sections['5'] = {
                'page': 38,
                'indices': rune_indices,
                'rune_count': len(rune_indices),
                'text': section[:100]
            }
    
    # Page 10 - Section 7
    content_10 = load_page_runes(10)
    if content_10:
        match = re.search(r'7[-–](.+?)(?:\n|$)', content_10, re.DOTALL)
        if match:
            section = match.group(1).strip()
            rune_indices = runes_to_indices(section)
            sections['7'] = {
                'page': 10,
                'indices': rune_indices,
                'rune_count': len(rune_indices),
                'text': section[:100]
            }
    
    # Print summary
    print("\nEXTRACTED SECTIONS:")
    for num in sorted(sections.keys(), key=int):
        s = sections[num]
        print(f"  Section {num} (Page {s['page']}): {s['rune_count']} runes")
        transliterated = indices_to_text(s['indices'][:30])
        print(f"    Raw: {transliterated}...")
    
    # Analyze combined
    print("\n\nCOMBINED ANALYSIS:")
    total_runes = sum(s['rune_count'] for s in sections.values())
    print(f"  Total runes in numbered sections: {total_runes}")
    
    # Frequency analysis of combined sections
    all_indices = []
    for num in ['1', '2', '3', '4', '5']:  # Just the consecutive ones
        if num in sections:
            all_indices.extend(sections[num]['indices'])
    
    if all_indices:
        freq = Counter(all_indices)
        print(f"\n  Frequency distribution (sections 1-5):")
        for idx, count in freq.most_common(10):
            pct = count / len(all_indices) * 100
            print(f"    {INDEX_TO_LETTER[idx]:3}: {count:3} ({pct:.1f}%)")
    
    return sections

def search_for_six():
    """Search for where number 6 might be hiding."""
    print("\n" + "=" * 70)
    print("SEARCHING FOR MISSING NUMBER 6")
    print("=" * 70)
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check pages around the pattern
    for page_num in range(35, 42):
        content = load_page_runes(page_num)
        if content:
            # Check for '6' directly
            if '6' in content:
                print(f"Page {page_num}: Found '6'!")
            
            # Check for rune spelling of "six" - would be S-I-X = ᛋᛁᛉ
            if 'ᛋᛁᛉ' in content:
                print(f"Page {page_num}: Found 'SIX' (ᛋᛁᛉ) in runes!")
    
    # Check if any pages 58-74 have transcriptions (they might have 6)
    print("\nPages 58-74 (untranscribed) might contain number 6")
    for page_num in range(58, 75):
        rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
        if os.path.exists(rune_path):
            with open(rune_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    print(f"  Page {page_num} has transcription: {len(content)} chars")
                    if '6' in content:
                        print(f"    *** FOUND '6' ON PAGE {page_num}! ***")

def main():
    print("=" * 70)
    print("NUMBERED SECTIONS ANALYSIS - LIBER PRIMUS")
    print("A Major Discovery in the Cicada 3301 Puzzle")
    print("=" * 70)
    
    # Find all numbered sections
    numbered_pages = find_numbered_sections()
    
    # Analyze the sequence pattern
    analyze_numbered_sequence()
    
    # Extract full sections
    sections = extract_full_sections()
    
    # Test numbers as keys
    test_number_as_key()
    
    # Search for missing 6
    search_for_six()
    
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
1. Pages 36-38 contain a NUMBERED SEQUENCE (1-5) of text sections
2. Page 10 has section 7, suggesting a DIFFERENT sequence
3. Number 6 is MISSING - this is likely intentional
4. The numbers may serve as:
   - Section identifiers for reading order
   - Decryption keys (shift values)
   - Cross-reference markers
   - Pointers to prime numbers (1st, 2nd, 3rd prime...)

RECOMMENDATION: 
- Decode sections 1-5 as a single unit with special attention
- Find where section 6 is hidden (possibly pages 58-74 or encoded as runes)
- Test if sections should be read in numeric order across pages
- Try using the section number as the decryption key
""")

if __name__ == '__main__':
    main()

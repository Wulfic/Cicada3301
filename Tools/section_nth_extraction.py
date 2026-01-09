#!/usr/bin/env python3
"""
Extract the Nth rune from section N to see if it forms a message.
Also try other extraction patterns.
"""

import os
from pathlib import Path

# Gematria Primus alphabet
GEMATRIA = 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛠᛡᚣ'
RUNE_TO_LETTER = dict(zip(GEMATRIA, 'FUTHORKGWHNIJEOPXSTBEMLNDOAEAYY'))

def extract_section_text(page_num, section_num):
    """Extract text from a numbered section."""
    pages_dir = Path(__file__).parent.parent / 'pages'
    runes_file = pages_dir / f'page_{page_num:02d}' / 'runes.txt'
    
    if not runes_file.exists():
        return None
    
    content = runes_file.read_text(encoding='utf-8')
    
    # For section 7, it's mid-text
    if section_num == 7:
        idx = content.find('-7-')
        if idx >= 0:
            # Get surrounding context
            start = max(0, idx - 10)
            end = min(len(content), idx + 15)
            return content[start:end]
        return None
    
    # For sections 1-5, find "N-" pattern
    # Check if file starts with the section marker
    if content.startswith(f'{section_num}-'):
        start_idx = 0
    else:
        # Look for section at start of line
        marker = f'\n{section_num}-'
        start_idx = content.find(marker)
        if start_idx >= 0:
            start_idx += 1  # Skip the newline
        else:
            return None
    
    # Find end of section
    end_idx = len(content)
    for next_sec in range(section_num + 1, 10):
        next_marker = f'\n{next_sec}-'
        pos = content.find(next_marker, start_idx)
        if pos > start_idx and pos < end_idx:
            end_idx = pos
    
    # Also check for & or double newline
    for em in ['&', '\n\n']:
        pos = content.find(em, start_idx + 2)
        if pos > start_idx and pos < end_idx:
            end_idx = pos
    
    return content[start_idx:end_idx]

def main():
    print("=" * 70)
    print("SECTION-NUMBER EXTRACTION ANALYSIS")
    print("=" * 70)
    
    sections = [
        (36, 1),
        (37, 2),
        (37, 3),
        (37, 4),
        (38, 5),
        # Section 6 = Pages 56-57 (The Parable)
        (10, 7),
    ]
    
    print("\n📊 RAW SECTION CONTENT:")
    print("-" * 50)
    
    section_runes = {}
    
    for page, sec in sections:
        text = extract_section_text(page, sec)
        if text:
            # Extract just runes (no numbers, hyphens, spaces)
            runes_only = [c for c in text if c in GEMATRIA]
            section_runes[sec] = runes_only
            print(f"\n  Section {sec} (page {page}):")
            print(f"    Raw: {text[:60]}")
            print(f"    Rune count: {len(runes_only)}")
            print(f"    First 10 runes: {''.join(runes_only[:10])}")
    
    print("\n" + "=" * 70)
    print("🔤 NTH RUNE FROM SECTION N:")
    print("-" * 50)
    print("  (Taking the Nth rune from section N)")
    
    extracted = []
    for sec in [1, 2, 3, 4, 5, 7]:
        if sec in section_runes and len(section_runes[sec]) >= sec:
            rune = section_runes[sec][sec - 1]  # 0-indexed
            letter = RUNE_TO_LETTER.get(rune, '?')
            extracted.append((sec, rune, letter))
            print(f"    Section {sec}, rune {sec}: {rune} = {letter}")
        else:
            extracted.append((sec, '?', '?'))
            print(f"    Section {sec}: insufficient runes")
    
    message = ''.join(e[2] for e in extracted)
    print(f"\n  Extracted message: {message}")
    
    print("\n" + "=" * 70)
    print("🔤 FIRST RUNE FROM EACH SECTION:")
    print("-" * 50)
    
    first_runes = []
    for sec in [1, 2, 3, 4, 5, 7]:
        if sec in section_runes and section_runes[sec]:
            rune = section_runes[sec][0]
            letter = RUNE_TO_LETTER.get(rune, '?')
            first_runes.append(letter)
            print(f"    Section {sec}: {rune} = {letter}")
    
    print(f"\n  First runes message: {''.join(first_runes)}")
    
    print("\n" + "=" * 70)
    print("🔤 LAST RUNE FROM EACH SECTION:")
    print("-" * 50)
    
    last_runes = []
    for sec in [1, 2, 3, 4, 5, 7]:
        if sec in section_runes and section_runes[sec]:
            rune = section_runes[sec][-1]
            letter = RUNE_TO_LETTER.get(rune, '?')
            last_runes.append(letter)
            print(f"    Section {sec}: {rune} = {letter}")
    
    print(f"\n  Last runes message: {''.join(last_runes)}")
    
    # Try section 6 as The Parable
    print("\n" + "=" * 70)
    print("📜 SECTION 6 = THE PARABLE:")
    print("-" * 50)
    
    pages_dir = Path(__file__).parent.parent / 'pages'
    parable_file = pages_dir / 'page_56' / 'runes.txt'
    if parable_file.exists():
        content = parable_file.read_text(encoding='utf-8')
        runes = [c for c in content if c in GEMATRIA]
        print(f"    Rune count: {len(runes)}")
        if len(runes) >= 6:
            sixth_rune = runes[5]  # 0-indexed, so 6th rune
            print(f"    6th rune: {sixth_rune} = {RUNE_TO_LETTER.get(sixth_rune, '?')}")
        print(f"    First rune: {runes[0]} = {RUNE_TO_LETTER.get(runes[0], '?')}")
        print(f"    Last rune: {runes[-1]} = {RUNE_TO_LETTER.get(runes[-1], '?')}")
    
    # Complete message including section 6
    print("\n" + "=" * 70)
    print("🔍 COMPLETE NTH-RUNE MESSAGE (with section 6):")
    print("-" * 50)
    
    if parable_file.exists():
        content = parable_file.read_text(encoding='utf-8')
        runes = [c for c in content if c in GEMATRIA]
        if len(runes) >= 6:
            sixth_rune = runes[5]
            sixth_letter = RUNE_TO_LETTER.get(sixth_rune, '?')
            
            full_extracted = []
            for sec in [1, 2, 3, 4, 5]:
                if sec in section_runes and len(section_runes[sec]) >= sec:
                    rune = section_runes[sec][sec - 1]
                    letter = RUNE_TO_LETTER.get(rune, '?')
                    full_extracted.append(letter)
            
            full_extracted.append(sixth_letter)  # Section 6
            
            if 7 in section_runes and len(section_runes[7]) >= 7:
                rune = section_runes[7][6]  # 7th rune, 0-indexed
                letter = RUNE_TO_LETTER.get(rune, '?')
                full_extracted.append(letter)
            elif 7 in section_runes:
                # Section 7 is short, just use what we have
                print(f"    Note: Section 7 only has {len(section_runes[7])} runes")
            
            print(f"\n  Complete message: {''.join(full_extracted)}")

if __name__ == '__main__':
    main()

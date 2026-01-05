#!/usr/bin/env python3
"""
Convert Page 1 SUB-71 output to actual letters (expanding TH, NG, etc.)
to see if it becomes readable English
"""

import os
from pathlib import Path

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

# Gematria Primus - some are digraphs
LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# Convert to single letters for readability
LETTERS_EXPANDED = [
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

def indices_to_text_with_spaces(indices):
    """Convert indices to text, treating words"""
    result = []
    for idx in indices:
        result.append(LETTERS[idx])
    return " ".join(result)

def indices_to_text(indices):
    """Convert indices to text"""
    return "".join(LETTERS[idx] for idx in indices)

# Best key from previous optimization
BEST_KEY_71 = [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7]

def main():
    print("=" * 80)
    print("PAGE 1 - ANALYZING AS ACTUAL ENGLISH TEXT")
    print("=" * 80)
    
    cipher_indices = load_page1()
    plaintext_indices = decrypt_sub(cipher_indices, BEST_KEY_71)
    plaintext_text = indices_to_text(plaintext_indices)
    
    print("\nOriginal output:")
    print(plaintext_text)
    
    print("\n" + "=" * 80)
    print("WORD ANALYSIS")
    print("=" * 80)
    
    # Split by potential word breaks
    # Look for "THE" as word marker
    words = plaintext_text.split("THE")
    print(f"\nSplitting by 'THE' creates {len(words)} segments:")
    for i, word in enumerate(words[:20], 1):
        if word:
            print(f"  {i}. {word}")
    
    # Count digraphs
    print("\n" + "=" * 80)
    print("DIGRAPH FREQUENCY")
    print("=" * 80)
    
    digraph_count = 0
    for idx in plaintext_indices:
        letter = LETTERS[idx]
        if len(letter) > 1:
            digraph_count += 1
    
    print(f"\nTotal characters: {len(plaintext_indices)}")
    print(f"Digraphs (TH, NG, EO, etc.): {digraph_count} ({100*digraph_count/len(plaintext_indices):.1f}%)")
    
    # Look for common patterns
    print("\n" + "=" * 80)
    print("COMMON PATTERNS")
    print("=" * 80)
    
    patterns = {
        'THE': plaintext_text.count('THE'),
        'EATH': plaintext_text.count('EATH'),
        'ATH': plaintext_text.count('ATH'),
        'REATH': plaintext_text.count('REATH'),
        'ING': plaintext_text.count('ING'),
        'OF': plaintext_text.count('OF'),
        'WITH': plaintext_text.count('WITH'),
        'THAT': plaintext_text.count('THAT')
    }
    
    print("\nPattern occurrences:")
    for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {pattern}: {count} times")
    
    # Try to parse as continuous text
    print("\n" + "=" * 80)
    print("ATTEMPTING TO READ AS CONTINUOUS TEXT")
    print("=" * 80)
    
    # Insert spaces after likely word endings
    text_with_spaces = plaintext_text
    
    # Replace common patterns with spaces
    for word in [' THE ', ' OF ', ' TO ', ' AND ', ' A ', ' IN ', ' THAT ', ' WITH ']:
        text_with_spaces = text_with_spaces.replace(word.strip(), word)
    
    print("\nWith spaces added after common words:")
    print(text_with_spaces)
    
    # Try reading just the parts with "THE"
    print("\n" + "=" * 80)
    print("EXTRACTING 'THE' CONTEXTS (5 chars before/after)")
    print("=" * 80)
    
    the_positions = []
    pos = 0
    while True:
        pos = plaintext_text.find('THE', pos)
        if pos == -1:
            break
        the_positions.append(pos)
        pos += 1
    
    print(f"\nFound 'THE' at {len(the_positions)} positions:")
    for i, pos in enumerate(the_positions[:15], 1):
        start = max(0, pos - 5)
        end = min(len(plaintext_text), pos + 8)
        context = plaintext_text[start:end]
        print(f"  {i}. ...{context}...")
    
    # Check if removing repeated patterns helps
    print("\n" + "=" * 80)
    print("HYPOTHESIS: Repeated patterns might be padding/noise")
    print("=" * 80)
    
    # Remove repeated ATH/EATH patterns
    cleaned = plaintext_text
    for pattern in ['EATH', 'ATH', 'THE']:
        # Only keep first occurrence of repeated pattern
        while pattern + pattern in cleaned:
            cleaned = cleaned.replace(pattern + pattern, pattern)
    
    print(f"\nAfter removing immediate repeats:")
    print(f"Original length: {len(plaintext_text)}")
    print(f"Cleaned length: {len(cleaned)}")
    print(f"\nCleaned text:")
    print(cleaned)
    
    # Look for acrostic (first letter of each segment)
    print("\n" + "=" * 80)
    print("TESTING ACROSTIC HYPOTHESIS")
    print("=" * 80)
    
    segments = [w for w in plaintext_text.split('THE') if w]
    acrostic = ''.join([seg[0] if seg else '' for seg in segments])
    print(f"\nFirst letter of each THE-segment:")
    print(acrostic)
    
    # Try every-Nth on just the consonants
    print("\n" + "=" * 80)
    print("SUGGESTION")
    print("=" * 80)
    print("""
The text contains recognizable English patterns:
  - "THE" appears 26 times
  - "OF" appears 4 times  
  - Common fragments: "EATH", "ATH", "REATH", "ING"

However, it's not standard readable English prose. Possibilities:

1. FRAGMENTED MESSAGE: The text is intentionally broken/encoded
   - May require reassembly or parsing rules
   - Could be an acrostic or positional encoding

2. WORD LIST: Not prose, but a list of words/fragments
   - Similar to cryptographic word lists
   - Each fragment might be significant

3. NEEDS ADDITIONAL LAYER: There may be another transformation
   - Transposition cipher on top of SUB
   - Column/row reading
   - Specific extraction pattern

4. TRANSCRIPTION ERRORS: Some runes may be misread
   - Would explain fragments that almost make sense
   - Need to verify against original images

Next steps:
- Test columnar transposition
- Try reading in different directions/patterns
- Verify original rune transcription
- Compare with known solved pages for format clues
""")

if __name__ == '__main__':
    main()

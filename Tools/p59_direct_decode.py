#!/usr/bin/env python3
"""
Direct rune-to-English decoder using Page 59's substitution table.
Works directly with rune characters, not runeglish conversion.
"""

# Rune to Gematria Latin mapping
RUNE_TO_LATIN = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R',
    'ᚳ': 'C', 'ᚷ': 'G', 'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N',
    'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P', 'ᛉ': 'X',
    'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M',
    'ᛚ': 'L', 'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A',
    'ᚫ': 'AE', 'ᛡ': 'IA', 'ᛣ': 'C', 'ᛠ': 'EA', 'ᚸ': 'G',
    'ᚣ': 'Y'
}

# Page 59 Cipher Table (Gematria Latin -> English)
PAGE59_CIPHER = {
    'R': 'A',
    'NG': 'W',
    'A': 'R',
    'M': 'N',
    'J': 'B',
    'I': 'E',
    'H': 'L',
    'E': 'I',
    'IA': 'V',
    'AE': 'O',
    'D': 'K',
    'OE': 'G',
    'C': 'D',
    'EO': 'T',
    'N': 'M',
    'P': 'S',
    'S': 'P',
    'X': 'X',
    'EA': 'F',
    'Y': 'TH',
    'TH': 'Y',
    # Missing mappings - derive from reciprocal pattern
    'F': 'EA',  # F -> EA (since EA -> F)
    'U': 'U',   # Identity (center-ish)
    'O': 'IA',  # O -> IA? Let's try...
    'G': 'OE',  # G -> OE (since OE -> G)
    'W': 'NG',  # W -> NG (since NG -> W)
    'L': 'H',   # L -> H (since H -> L)
    'B': 'J',   # B -> J (since J -> B)
    'T': 'EO',  # T -> EO (since EO -> T)
}

def decode_runes(rune_text: str) -> str:
    """Decode runes using Page 59 substitution."""
    result = []
    
    for char in rune_text:
        if char == '•':
            result.append(' ')
        elif char in ['-', '.', '\n', ' ', '%', '&', '$', '§']:
            result.append(char)
        elif char in RUNE_TO_LATIN:
            latin = RUNE_TO_LATIN[char]
            if latin in PAGE59_CIPHER:
                result.append(PAGE59_CIPHER[latin])
            else:
                result.append(f'[{latin}]')
        else:
            result.append(f'?{char}?')
    
    return ''.join(result)

def main():
    import os
    
    # Page 59 runes (from terminal output)
    page59_runes = """ᚱ•ᛝᚱᚪᛗᚹ
ᛄᛁᚻᛖᛁᛡᛁ•ᛗᚫᚣᚹ•ᛠᚪᚫᚾ•ᚣᛖᛈ•ᛄᚫᚫᛞ
ᛁᛉᛞᛁᛋᛇ•ᛝᛚᚱᛇ•ᚦᚫᛡ•ᛞᛗᚫᛝ•ᛇᚫ•ᛄᛁ•ᛇᚪᛡᛁ
ᛇᛁᛈᛇ•ᚣᛁ•ᛞᛗᚫᛝᚻᛁᚳᛟᛁ
ᛠᛖᛗᚳ•ᚦᚫᛡᚪ•ᛇᚪᛡᚣ
ᛁᛉᛋᛁᚪᛖᛁᛗᛞᛁ•ᚦᚫᛡᚪ•ᚳᚠᚣ
ᚳᚫ•ᛗᚫᛇ•ᛁᚳᛖᛇ•ᚫᚪ•ᛞᛚᚱᚹᛁ•ᚣᛖᛈ•ᛄᚫᚫᛞ
ᚫᚪ•ᚣᛁ•ᚾᛁᛈᛈᚱᛟᛁ•ᛞᚫᛗᛇᚱᛖᛗᛁᚳ•ᛝᛖᚣᛖᛗ
ᛁᛖᚣᛁᚪ•ᚣᛁ•ᛝᚫᚪᚳᛈ•ᚫᚪ•ᚣᛁᛖᚪ•ᛗᛡᚾᛄᛁᚪᛈ
ᛠᚫᚪ•ᚱᚻᚻ•ᛖᛈ•ᛈᚱᛞᚪᛁᚳ"""

    print("=" * 60)
    print("PAGE 59 VERIFICATION")
    print("=" * 60)
    print("\nRaw runes:")
    print(page59_runes)
    print("\nDecoded with Page 59 table:")
    decoded = decode_runes(page59_runes)
    print(decoded)
    
    # Expected: A WARNING, BELIEVE NOTHING FROM THIS BOOK, etc.
    
    # Now try on some unsolved pages
    pages_dir = os.path.join(os.path.dirname(__file__), "..", "pages")
    
    for page_num in [18, 19, 20, 21, 65, 69, 70, 71]:
        runes_file = os.path.join(pages_dir, f"page_{page_num:02d}", "runes.txt")
        if os.path.exists(runes_file):
            print(f"\n{'='*60}")
            print(f"PAGE {page_num}")
            print("=" * 60)
            with open(runes_file, 'r', encoding='utf-8') as f:
                runes = f.read()
            decoded = decode_runes(runes)
            print(f"First 300 chars:\n{decoded[:300]}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
RUNNING KEY FROM SOLVED TEXT

Hypothesis: Unsolved pages might be encrypted using text from solved pages as the running key.

For example:
- Use "PARABLE LIKE THE INSTAR..." (Page 56) as running key for Page 8
- Or use text from earlier solved onion pages
"""

import os
from pathlib import Path

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

ENGLISH_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 
    'WE', 'THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 
    'WAS', 'ONE', 'OUR', 'OUT', 'ARE', 'HAS', 'HIS', 'HOW', 'ITS', 'MAY',
    'NEW', 'NOW', 'OLD', 'SAY', 'SHE', 'TOO', 'TWO', 'WAY', 'WHO', 'YET',
    'THY', 'YEA', 'NAY', 'FIND', 'PATH', 'SEEK', 'TRUTH', 'LIGHT', 'WITHIN',
    'DIVINITY', 'EMERGE', 'SURFACE', 'PARABLE', 'INSTAR', 'CIRCUMFERENCE',
    'MUST', 'SHED', 'WITH', 'THIS', 'THAT', 'FROM', 'HAVE', 'BEEN', 'WILL'
}

# Known solved texts as potential running keys
SOLVED_TEXTS = {
    'PARABLE': 'PARABLELIKETHEINSTARTUNNELINGTOTHESURFACEWEMUSTSSHEDOUROWNC'
               'IRCUMFERENCESFINDTHEDIVINITYWITHINANDEMERGE',
    
    'WARNING': 'AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETR'
               'UETESTTHEKNOWLEDGEFINDYOURTRUTHEXPERIENCEYOURDEATH',
    
    'WELCOME': 'WELCOMEWELCOMEPILGRIMTOTHEGREATJOURNEYTOWDARDTHEENDOF'
               'ALLTHINGSITISNOTANEASYTRIPBUTFORTHOSEWHOFINDTHEIRWAY',
    
    'WISDOM': 'SOMEWISDOMTHEPRIMESARESACREDTHETOTIENTFUNCTIONISSACRED'
              'ALLTHINGSSHOULDBEENCRYPTEDKNOWTHIS',
              
    'DIVINITY': 'DIVINITYDIVINITYDIVINITYDIVINITYDIVINITYDIVINITYDIVINIT'
                'YDIVINITYDIVINITYDIVINITYDIVINITYDIVINITYDIVINITYDIVINI',
    
    'CICADA': 'CICADACICADACICADACICADACICADACICADACICADACICADACICADA'
              'CICADACICADACICADACICADACICADACICADACICADACICADACICADA'
}

def load_runes(page_num):
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    if not runes_file.exists():
        return None
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_rune_stream(rune_text):
    return [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]

def parse_words(rune_text):
    words = []
    current = []
    for c in rune_text:
        if c in RUNE_MAP:
            current.append(RUNE_MAP[c])
        elif c in '-. \n\r':
            if current:
                words.append(current)
                current = []
    if current:
        words.append(current)
    return words

def text_to_indices(text):
    result = []
    i = 0
    text = text.upper()
    while i < len(text):
        # Try digraphs first
        matched = False
        for digraph in ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO']:
            if text[i:i+len(digraph)] == digraph:
                result.append(LETTER_TO_IDX[digraph])
                i += len(digraph)
                matched = True
                break
        if not matched:
            if text[i] in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[text[i]])
            i += 1
    return result

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def decrypt_with_running_key(cipher, key_indices):
    """Decrypt cipher using running key."""
    plain = []
    for i in range(len(cipher)):
        key = key_indices[i % len(key_indices)]
        plain.append((cipher[i] - key) % 29)
    return plain

def score_words(plain_indices, words):
    """Score by counting English words."""
    score = 0
    found = []
    pos = 0
    
    for word_cipher in words:
        wlen = len(word_cipher)
        if pos + wlen > len(plain_indices):
            break
        word_text = indices_to_text(plain_indices[pos:pos+wlen])
        
        if word_text.upper() in ENGLISH_WORDS:
            score += len(word_text) * 100
            found.append(word_text)
        
        pos += wlen
    
    return score, found

def test_running_keys(page_num):
    """Test all solved texts as running keys."""
    
    print(f"\n{'='*70}")
    print(f"RUNNING KEY TEST: PAGE {page_num}")
    print("=" * 70)
    
    rune_text = load_runes(page_num)
    if not rune_text:
        print("Could not load page")
        return
    
    cipher = parse_rune_stream(rune_text)
    words = parse_words(rune_text)
    
    print(f"Cipher length: {len(cipher)}")
    
    results = []
    
    for name, text in SOLVED_TEXTS.items():
        key_indices = text_to_indices(text)
        if not key_indices:
            continue
        
        plain = decrypt_with_running_key(cipher, key_indices)
        score, found = score_words(plain, words)
        
        results.append({
            'key_name': name,
            'score': score,
            'words': found,
            'preview': indices_to_text(plain[:60])
        })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\nResults (sorted by score):")
    for r in results:
        print(f"\n{r['key_name']}:")
        print(f"  Score: {r['score']}")
        print(f"  Words: {', '.join(r['words'][:10])}")
        print(f"  Preview: {r['preview']}")

def main():
    for page_num in [8, 9, 10, 43, 51]:
        test_running_keys(page_num)

if __name__ == '__main__':
    main()

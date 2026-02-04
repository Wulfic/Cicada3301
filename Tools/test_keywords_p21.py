"""
Test all Page 63 keywords on Page 21 to find correct one
"""

import os

GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21,
    'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19,
    'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

GP_INDEX_TO_LATIN = {v: k for k, v in LATIN_TO_INDEX.items()}

# Keywords mapping to their indices (from Page 63)
KEYWORDS = {
    'CABAL': 'C A B A L',
    'DIVINITY': 'D I V I N I T Y',
    'ENCRYPTION': 'E N C R Y P T I O N',
    'OBSCURA': 'O B S C U R A',
    'ENCRYPT': 'E N C R Y P T',
    'SHADOWS': 'S H A D O W S',
    'DEOR': 'D E O R',
    'TOTIENT': 'T O T I E N T',
    'MOURNFUL': 'M O U R N F U L',
    'PRIMES': 'P R I M E S',
    'NUMBERS': 'N U M B E R S',
}

def keyword_to_indices(keyword_str):
    """Convert keyword string to indices"""
    words = keyword_str.split()
    indices = []
    for word in words:
        if word in LATIN_TO_INDEX:
            indices.append(LATIN_TO_INDEX[word])
        else:
            # Try single letters
            if len(word) == 1:
                if word in LATIN_TO_INDEX:
                    indices.append(LATIN_TO_INDEX[word])
    return indices

def indices_to_text(indices):
    """Convert indices to Latin text"""
    result = []
    for idx in indices:
        result.append(GP_INDEX_TO_LATIN.get(idx, '?'))
    return ''.join(result)

def count_readable_words(text):
    """Basic check for readable text"""
    vowels = 'AEIOUAEOY'
    vowel_count = sum(1 for c in text if c in vowels)
    if len(text) == 0:
        return 0
    return vowel_count / len(text)

# Load Page 21
page_file = 'LiberPrimus/pages/page_21/runes.txt'
with open(page_file, 'r', encoding='utf-8') as f:
    text = f.read().strip()

indices = []
for char in text:
    if char in GP_RUNE_TO_INDEX:
        indices.append(GP_RUNE_TO_INDEX[char])

print(f"Page 21 has {len(indices)} runes")
print()
print("Testing keywords with SUB mode (subtract):")
print("-" * 80)

results = []
for keyword_name, keyword_str in KEYWORDS.items():
    keyword_indices = keyword_to_indices(keyword_str)
    
    if len(keyword_indices) == 0:
        continue
    
    # SUB mode: subtract keyword
    decrypted = []
    for i, idx in enumerate(indices):
        decrypted.append((idx - keyword_indices[i % len(keyword_indices)]) % 29)
    
    # Convert to text
    result_text = indices_to_text(decrypted)
    
    # Check if it contains known words
    the_count = result_text.upper().count('THE')
    and_count = result_text.upper().count('AND')
    
    readable = count_readable_words(result_text)
    
    results.append({
        'name': keyword_name,
        'text': result_text[:100],
        'the_count': the_count,
        'and_count': and_count,
        'readable': readable
    })
    
    print(f"{keyword_name:15} THE:{the_count} AND:{and_count} Vowels:{readable:.2f}")
    print(f"  Preview: {result_text[:80]}")
    print()

# Sort by THE count
results.sort(key=lambda x: (x['the_count'] + x['and_count']), reverse=True)

print()
print("=" * 80)
print("TOP RESULT")
print("=" * 80)
best = results[0]
print(f"{best['name']}: {best['text']}")

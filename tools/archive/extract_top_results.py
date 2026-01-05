#!/usr/bin/env python3
"""
Extract and display the full decrypted text from top-scoring results.
Focus on the highest-scoring interleaved key combinations.
"""

import sys
sys.path.insert(0, 'c:/Users/tyler/Repos/Cicada3301/tools')

# =============================================================================
# GEMATRIA PRIMUS - 29 Anglo-Saxon Futhorc runes
# =============================================================================
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
         'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
NUM_RUNES = 29

# Master key from Page 0 - Page 57 analysis
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# =============================================================================
# PAGE DATA - Unsolved pages
# =============================================================================
UNSOLVED_PAGES = {
    27: "ᚫᛄᚣᛋᛗᛇᚣᛚᛝᚫᚫᚠᚳᛄᛞᛇᛒᚣᚦᛋᛡᚹᛠᛡᚾᚫᛈᛁᚢᚣᚱᛞᛇᛞᛝᛁᚢᚫᛠᚫᚱᛈᚳᚪᚣᛈᚹᛠᛞᛁᚢᚠᛞᚫᚷᛗᚣᛏᚾᛡᛠᛖᛠᛡᛒᚫᛟᛈᛗᚣᚣᛚᛇᛗᛞᚣᛈᛝᚣᛋᛝᛖᛝᛇᛁᚢᚣᛋᛏᛈᛝᛞᚦᛁᛄᛁᚠᚠᛚᚾᚣᚣᛒᛖᚱᛋ",
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    29: "ᚫᛠᚫᛇᛋᚷᚪᚱᚫᛄᛝᛗᚠᛇᚷᛒᚣᛏᛞᛞᛠᚾᛗᛇᚱᛗᛋᛄᛁᛄᚢᛏᛖᚷᚫᛇᚹᛈᛚᛠᛄᚫᛇᛠᛖᛄᚠᚠᚪᚷᛇᚪᛏᛗᛗᛒᚣᛡᛄᛖᛠᛁᚣᚫᚫᛗᛟᛇᛡᛝᛗᚢᛏᚱᚦᛈᛄᚪᛄᛋᛁᛡᚣᚣᚹᚠᛚᚱᛁᛟᚦᚫᛇᛒᛟᛄᚣᛈᚣᛇᛋᛄ",
    30: "ᛞᚪᛁᚣᛚᛄᛖᚦᛡᚣᛇᛚᛁᛈᛏᛋᛞᛁᛗᛄᛝᚠᛄᛈᛇᛁᛏᚣᛗᚢᚣᚱᛖᛡᚣᛁᛟᛄᚹᛇᛄᛄᚾᛁᚫᚣᛡᛁᛈᛋᚣᛠᛞᚳᛖᛞᛏᛈᚳᚣᛖᛞᚠᚫᛠᛒᚾᛏᚣᚾᚢᚠᛁᛏᚠᛖᚫᛄᛟᛈᛋᛄᚢᛏᛞᛈᚫᛟᛠᛇᚢᚷᛏᛠᛗᛡᛡ",
    31: "ᚫᛏᛈᛁᚫᚣᚹᛡᚠᛡᛚᛁᚣᛚᛗᛞᚾᛏᚷᛗᛠᛡᛇᛗᛝᚠᛟᚱᚷᛠᚦᛄᛖᚱᚪᛁᛟᛡᛄᛚᚪᛟᛇᛡᚣᛄᚷᛏᛗᚣᚣᛟᛁᛈᚢᛄᛋᛏᛠᛄᛠᚢᛡᚱᛟᛏᛠᚠᛇᛁᚦᚷᛁᛟᚫᚠᛄᛈᛞᛝᛚᛄᛒᛖᛏᛖᛞᛄᛄᚢᚣᛒᛈᛟᛠᛁᛟ",
    40: "ᛖᚹᛋᛄᚣᚾᚾᛝᛡᛋᛋᛄᛒᚠᛒᚣᛏᛡᛋᚳᛗᛠᛠᚢᚪᛄᛗᛡᚱᚳᛗᛄᚠᚢᚱᛝᛠᛡᛖᛒᛡᛠᛚᚫᛄᛡᛡᛁᚱᛈᛇᛁᛈᛝᚾᛒᛋᛠᛖᛒᚾᛇᛏᛟᛖᛝᚱᛗᛁᛇᛄᛈᛋᛒᛞᛇᛝᛇᛖᛏᛇᛁᚾᚾᛗ",
    41: "ᚱᚪᛗᛠᚢᛖᛋᛁᛝᛠᛟᚣᛈᛠᛗᛋᚫᛟᛁᚱᛄᛝᛡᚾᚢᚫᛗᛠᛈᛡᛇᛚᛄᚣᛚᚪᛄᛟᚷᛝᛠᛗᛁᛇᛁᛗᚫᛚᛇᛞᛖᛗᚣᛈᛋᛄᛝᛟᛠᛟᚱᛡᛝᛇᛁᛁᛏᛠᚾᛒᛡᛡᛄᚹᛡᚢᛝᛠᚦᛈᛄᛈᛠᚾᛟᛝᛇᚾᛁᛇ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    45: "ᛟᛟᛠᛒᚾᚫᛄᛁᛖᛄᛖᛗᛁᛖᛠᛈᛡᚢᛗᛟᛡᛝᛖᛚᚱᛁᚢᛝᛟᛖᛁᚪᛄᛇᛠᚫᛡᚣᛖᛞᛠᚣᛠᛒᚳᛝᛝᛡᛞᛏᛡᛈᛝᛁᛁᛄᛟᚾᚣᚷᚣᛄᛒᚢᛡᛠᛇᛚᛚᛁᛖᛄᚾᛋᛁᛡᚣᛏᛇᚱᛡᛝᚾᚣᛞᛇᛁᚫ",
    46: "ᚣᚾᚫᚾᚾᛞᛇᚳᛈᛚᛁᛚᛈᛟᛏᚫᛈᛏᚪᛖᛇᚢᛚᚪᚾᚪᚫᛠᚹᚪᛁᛄᛝᛠᛇᛖᛄᚣᛖᚢᛠᛈᚫᛁᚢᛁᚪᛠᛁᛠᛚᛄᛄᛚᛠᚢᛖᚢᚾᛒᚠᛚᛟᛁᛠᛝᚷᚣᛟᛈᛝᛈᚷᚳᚳᚢᛠᛏᛄᛖᛈᛇᚹᛠᛈᛝᛏᛏᛖ",
    47: "ᛈᛋᛇᛖᚳᛝᚷᛋᛇᛒᚹᛇᛁᚢᛟᛒᛁᚹᛁᛁᛁᛠᛝᛠᚷᚪᚳᚳᛠᚾᚪᛖᛏᛟᛗᛡᛁᚪᛄᛁᛚᚪᛈᛇᚷᚳᛁᛠᛝᛇᚱᛟᚾᛗᛈᛄᛄᛁᛒᛄᚾᛄᛋᚫᛄᛠᛝᛠᛏᚫᛄᛠᛁᛁᛁᛒᛁᚷᚳᛡᛠᛄᛈᛁᛒᚪᛡᚪᛝᛡ",
    48: "ᚫᚾᛇᛠᛖᛗᛞᛠᛖᚾᛄᛋᛠᛖᛄᚷᛒᛗᛗᛖᚱᚾᚹᚪᛇᛠᛖᛈᚢᛝᚾᛞᛖᛁᚳᚾᚳᛈᛝᛗᛚᛡᛡᛈᛋᛚᛝᛁᛟᛡᛗᛡᛚᛒᛄᛖᛗᛠᛁᚢᚳᚪᛞᛖᛁᚫᛡᚱᚹᛏᛝᛈᚹᛋᚾᛇᚾᛄᛞᛖᛚᚫᚾᚳᛟᚷᛞᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

# Rune Unicode to ASCII mapping
RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA', 'ᛣ': 'C', 'ᛤ': 'C', 'ᛥ': 'ST'
}

def unicode_to_runes(text):
    """Convert Unicode runes to ASCII rune names."""
    result = []
    for char in text:
        if char in RUNE_UNICODE:
            result.append(RUNE_UNICODE[char])
        elif char.isspace():
            result.append(' ')
    return result

def decrypt_sub(indices, key, rotation=0, offset=0):
    """Decrypt using subtraction: plaintext = (ciphertext - key) mod 29"""
    result = []
    key_len = len(key)
    for i, idx in enumerate(indices):
        key_val = key[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_xor(indices, key, rotation=0, offset=0):
    """Decrypt using XOR: plaintext = ciphertext XOR key"""
    result = []
    key_len = len(key)
    for i, idx in enumerate(indices):
        key_val = key[(i + rotation) % key_len]
        plain_idx = ((idx - offset) ^ key_val) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_interleaved(indices, key, rot1, rot2, offset=0):
    """Decrypt using two alternating rotations of the key."""
    result = []
    key_len = len(key)
    for i, idx in enumerate(indices):
        rotation = rot1 if i % 2 == 0 else rot2
        key_val = key[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(RUNES[i] for i in indices)

def score_text(text):
    """Enhanced scoring for English/Latin text."""
    score = 0
    
    # Common English words (3+ letters)
    english_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                     'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY',
                     'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW',
                     'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY', 'DID', 'MAN',
                     'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN',
                     'WILL', 'WHAT', 'WHEN', 'YOUR', 'SOME', 'THEM', 'INTO',
                     'WHICH', 'THERE', 'THEIR', 'OTHER', 'ABOUT', 'THESE',
                     'TRUTH', 'BEING', 'LIGHT', 'WISDOM', 'KNOWLEDGE']
    
    # Latin words
    latin_words = ['ET', 'AD', 'DE', 'IN', 'AB', 'EX', 'UT', 'NE', 'SI', 'AC',
                   'DEO', 'SOL', 'LUX', 'AER', 'EST', 'SUB', 'PER', 'PRO',
                   'HAEC', 'HOC', 'HIC', 'DUM', 'SUM', 'DUO', 'VIA', 'VERITAS',
                   'VITA', 'AMOR', 'MORS', 'DEUS', 'TERRA', 'CAELUM']
    
    # Score English words
    for word in english_words:
        if word in text:
            score += len(word) * 3
    
    # Score Latin words
    for word in latin_words:
        if word in text:
            score += len(word) * 2
    
    # Common digraphs
    digraphs = ['TH', 'HE', 'AN', 'IN', 'ER', 'ON', 'RE', 'ED', 'ND', 'HA',
                'AT', 'EN', 'ES', 'OF', 'OR', 'NT', 'EA', 'TI', 'TO', 'IT',
                'ST', 'IO', 'LE', 'IS', 'OU', 'AR', 'AS', 'DE', 'RT', 'VE']
    for dg in digraphs:
        score += text.count(dg) * 0.5
    
    return score

# =============================================================================
# MAIN - Extract and display top results
# =============================================================================

print("=" * 80)
print("🏆 TOP DECRYPTION RESULTS - FULL TEXT EXTRACTION")
print("=" * 80)

top_results = [
    # (page, method, params, description)
    (29, 'interleaved', (60, 45, 0), "HIGHEST SCORE: 115.0"),
    (47, 'interleaved', (45, 0, 0), "Score: 112.5"),
    (47, 'interleaved', (45, 90, 0), "Score: 111.5"),
    (52, 'interleaved', (15, 75, 0), "Score: 111.0"),
    (52, 'interleaved', (15, 30, 0), "Score: 109.5"),
    (48, 'interleaved', (90, 30, 0), "Score: 107.0"),
    (52, 'interleaved', (0, 75, 0), "Score: 107.0"),
    (30, 'interleaved', (30, 30, 0), "Score: 105.5"),
    (45, 'sub', (14, 1), "Score 105.5 - page mod 31, page mod 11"),
    (47, 'sub', (82, 18), "Score 105.0 - 311*page formula"),
    (28, 'sub', (93, 22), "Score 106.0 - 311-page formula"),
]

for page, method, params, desc in top_results:
    print(f"\n{'='*80}")
    print(f"📖 PAGE {page} - {desc}")
    print(f"{'='*80}")
    
    # Get the page data
    if page not in UNSOLVED_PAGES:
        print(f"Page {page} not found in data")
        continue
    
    runes = unicode_to_runes(UNSOLVED_PAGES[page])
    indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
    
    if method == 'interleaved':
        rot1, rot2, offset = params
        decrypted_indices = decrypt_interleaved(indices, MASTER_KEY, rot1, rot2, offset)
        print(f"Method: Interleaved key (rot1={rot1}, rot2={rot2}, offset={offset})")
    elif method == 'sub':
        rot, offset = params
        decrypted_indices = decrypt_sub(indices, MASTER_KEY, rot, offset)
        print(f"Method: Subtraction (rotation={rot}, offset={offset})")
    elif method == 'xor':
        rot, offset = params
        decrypted_indices = decrypt_xor(indices, MASTER_KEY, rot, offset)
        print(f"Method: XOR (rotation={rot}, offset={offset})")
    
    # Convert to text
    text = indices_to_text(decrypted_indices)
    score = score_text(text)
    
    print(f"Score: {score}")
    print(f"\nFull decrypted text ({len(text)} characters):")
    print("-" * 60)
    
    # Print in chunks of 60 characters for readability
    for i in range(0, len(text), 60):
        chunk = text[i:i+60]
        print(chunk)
    
    print("-" * 60)
    
    # Look for word patterns
    words_found = []
    all_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 
                 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY',
                 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN',
                 'WILL', 'WHAT', 'WHEN', 'YOUR', 'SOME', 'THEM', 'INTO',
                 'ET', 'AD', 'DE', 'IN', 'AB', 'EX', 'UT', 'NE', 'SI', 'AC',
                 'DEO', 'SOL', 'LUX', 'AER', 'EST', 'SUB', 'TRUTH', 'BEING',
                 'LIGHT', 'WISDOM', 'KNOWLEDGE', 'SEEK', 'FIND', 'PATH',
                 'HAEC', 'HOC', 'HIC', 'DUM', 'SUM', 'VERITAS', 'VIA']
    
    for word in all_words:
        if word in text:
            # Find all positions
            pos = 0
            while True:
                pos = text.find(word, pos)
                if pos == -1:
                    break
                words_found.append((word, pos))
                pos += 1
    
    if words_found:
        print(f"Words found: {[w[0] for w in words_found]}")
    
    # Look for repeating patterns
    print("\nPattern analysis:")
    for plen in [3, 4, 5]:
        patterns = {}
        for i in range(len(text) - plen + 1):
            pat = text[i:i+plen]
            if pat not in patterns:
                patterns[pat] = 0
            patterns[pat] += 1
        
        repeated = [(p, c) for p, c in patterns.items() if c >= 2]
        repeated.sort(key=lambda x: -x[1])
        if repeated[:5]:
            print(f"  {plen}-char patterns: {repeated[:5]}")

# =============================================================================
# Try additional experiments
# =============================================================================

print("\n" + "=" * 80)
print("🔬 ADDITIONAL EXPERIMENTS")
print("=" * 80)

# Try combining multiple pages with same parameters
print("\n📊 Testing if multiple pages use same key parameters...")

for rot, off in [(60, 45), (45, 0), (45, 90), (15, 75)]:
    print(f"\n--- Testing rot1={rot}, rot2={off if off != 0 else 'same'} across all pages ---")
    for page in sorted(UNSOLVED_PAGES.keys()):
        runes = unicode_to_runes(UNSOLVED_PAGES[page])
        indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]
        
        # Interleaved
        decrypted = decrypt_interleaved(indices, MASTER_KEY, rot, off, 0)
        text = indices_to_text(decrypted)
        score = score_text(text)
        
        if score >= 90:
            print(f"  Page {page}: Score {score:.1f} - {text[:50]}...")

# Try variations around the best parameters
print("\n" + "=" * 80)
print("🎯 FINE-TUNING BEST PARAMETERS (Page 29, rot1=60, rot2=45)")
print("=" * 80)

page = 29
runes = unicode_to_runes(UNSOLVED_PAGES[page])
indices = [RUNE_TO_IDX.get(r) for r in runes if r in RUNE_TO_IDX]

best_score = 0
best_params = None

for rot1 in range(55, 66):
    for rot2 in range(40, 51):
        for off in range(0, 29):
            decrypted = decrypt_interleaved(indices, MASTER_KEY, rot1, rot2, off)
            text = indices_to_text(decrypted)
            score = score_text(text)
            
            if score > best_score:
                best_score = score
                best_params = (rot1, rot2, off)
                print(f"New best: rot1={rot1}, rot2={rot2}, off={off} -> Score {score:.1f}")
                print(f"  Text: {text[:60]}...")

if best_params:
    print(f"\n🏆 BEST RESULT for Page 29: {best_params} with score {best_score:.1f}")
    decrypted = decrypt_interleaved(indices, MASTER_KEY, *best_params)
    text = indices_to_text(decrypted)
    print(f"\nFull text:\n{text}")

print("\n" + "=" * 80)
print("✅ EXTRACTION COMPLETE")
print("=" * 80)

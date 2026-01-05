#!/usr/bin/env python3
"""
Try to align word boundaries by testing different starting positions.
Also try multiple simultaneous key rotations (different rot for different positions).
"""

# Gematria Primus - 29 runes
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

# Unicode to rune mapping
RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

UNSOLVED_PAGES = {
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
}

COMMON_WORDS_SHORT = ['THE', 'AND', 'FOR', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAS', 
                      'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'ARE', 'HIS', 'NOW', 'WHO',
                      'HOW', 'NEW', 'OLD', 'SEE', 'WAY', 'TWO', 'HIM', 'ITS', 'MAY',
                      'SAY', 'SHE', 'DAY', 'GET', 'GOT', 'HAS', 'LET', 'OWN', 'TOO',
                      'USE', 'MAN', 'MEN']

COMMON_WORDS_LONG = ['THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'WILL',
                     'WHAT', 'WHEN', 'YOUR', 'SOME', 'THEM', 'INTO', 'TIME', 'VERY',
                     'JUST', 'KNOW', 'TAKE', 'COME', 'MADE', 'FIND', 'MAKE', 'MORE',
                     'EACH', 'THEN', 'THAN', 'DOES', 'GIVE', 'MOST', 'SUCH', 'EVEN',
                     'ONLY', 'ALSO', 'BACK', 'AFTER', 'BEING', 'THEIR', 'WHICH', 'THERE',
                     'WOULD', 'ABOUT', 'COULD', 'OTHER', 'THESE', 'FIRST', 'THING',
                     'TRUTH', 'LIGHT', 'WISDOM', 'DIVINE', 'SACRED']

ALL_WORDS = set(COMMON_WORDS_SHORT + COMMON_WORDS_LONG)

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i % 29] for i in indices)

def score_text(text):
    score = 0
    text_upper = text.upper()
    for word in ALL_WORDS:
        count = text_upper.count(word)
        score += count * len(word) * 1.5  # Increased weight
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 
               'NG', 'OF', 'OR', 'TO', 'IT', 'IS', 'OU', 'AR', 'AS', 'AL',
               'TE', 'SE', 'EA', 'TI', 'VE', 'HA', 'WI', 'HI', 'ES', 'ST']
    for bg in bigrams:
        score += text_upper.count(bg) * 0.5
    return score

def find_words_with_positions(text):
    """Find all words and their positions."""
    words_found = []
    text_upper = text.upper()
    for word in sorted(ALL_WORDS, key=len, reverse=True):
        start = 0
        while True:
            pos = text_upper.find(word, start)
            if pos == -1:
                break
            words_found.append((pos, pos + len(word), word))
            start = pos + 1
    return words_found

# Best result from previous analysis
BEST_PARAMS = {
    52: {'method': 'double_xor', 'rot1': 75, 'off1': 26, 'rot2': 75, 'off2': 1},
    28: {'method': 'xor_sub', 'rot1': 30, 'off1': 27, 'rot2': 55, 'off2': 18},
    44: {'method': 'double_xor', 'rot1': 24, 'off1': 12, 'rot2': 6, 'off2': 10}
}

print("=" * 80)
print("🔍 WORD BOUNDARY ALIGNMENT ANALYSIS")
print("=" * 80)

for page_num, params in BEST_PARAMS.items():
    indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
    n = len(indices)
    
    print(f"\n{'='*60}")
    print(f"📄 PAGE {page_num}")
    print(f"{'='*60}")
    
    # Apply best decryption
    decrypted = []
    for i, idx in enumerate(indices):
        k1 = MASTER_KEY[(i + params['off1']) % len(MASTER_KEY)]
        if params['method'] == 'double_xor':
            k2 = MASTER_KEY[(i + params['off2']) % len(MASTER_KEY)]
            dec = ((idx ^ k1 ^ params['rot1']) ^ k2 ^ params['rot2']) % 29
        else:  # xor_sub
            k2 = MASTER_KEY[(i + params['off2']) % len(MASTER_KEY)]
            dec = (((idx ^ k1 ^ params['rot1']) - k2 - params['rot2']) % 29)
        decrypted.append(dec)
    
    text = indices_to_text(decrypted)
    print(f"Original: {text[:100]}...")
    
    # Find word positions
    words = find_words_with_positions(text)
    word_positions = sorted(set([w[0] for w in words]))
    
    print(f"\nWord start positions: {word_positions[:20]}...")
    
    # Try shifting the text to different alignments
    print("\n🔄 Testing text shifts for word alignment:")
    for shift in range(1, 10):
        shifted_text = text[shift:] + text[:shift]
        score = score_text(shifted_text)
        words = find_words_with_positions(shifted_text)
        if score > score_text(text) * 0.8:  # At least 80% of original score
            print(f"  Shift {shift}: Score {score:.1f}, Words found: {len(words)}")
            if shift <= 3:
                print(f"    Text: {shifted_text[:60]}...")
    
    # Try removing first N characters
    print("\n🔪 Testing prefix removal:")
    for remove in range(1, 10):
        trimmed = text[remove:]
        score = score_text(trimmed)
        words = find_words_with_positions(trimmed)
        if score > 50:
            print(f"  Remove {remove}: Score {score:.1f}")
            if remove <= 3:
                print(f"    Text: {trimmed[:60]}...")

print("\n" + "=" * 80)
print("🧪 TESTING VARIABLE ROTATION PER SEGMENT")
print("=" * 80)
print("(Different rotation for different parts of the text)")

results = []

for page_num in [28, 44, 52]:
    indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
    n = len(indices)
    
    print(f"\n📄 Page {page_num}:")
    
    # Split text into segments and try different rotations for each
    segment_size = n // 4  # 4 segments
    
    for rot1 in range(0, 29, 4):
        for rot2 in range(0, 29, 4):
            for rot3 in range(0, 29, 4):
                for rot4 in range(0, 29, 4):
                    for offset in range(0, len(MASTER_KEY), 15):
                        decrypted = []
                        for i, idx in enumerate(indices):
                            # Choose rotation based on segment
                            if i < segment_size:
                                rotation = rot1
                            elif i < 2 * segment_size:
                                rotation = rot2
                            elif i < 3 * segment_size:
                                rotation = rot3
                            else:
                                rotation = rot4
                            
                            key_val = MASTER_KEY[(i + offset) % len(MASTER_KEY)]
                            dec = (idx ^ key_val ^ rotation) % 29
                            decrypted.append(dec)
                        
                        text = indices_to_text(decrypted)
                        score = score_text(text)
                        if score > 130:
                            results.append({
                                'page': page_num,
                                'rots': (rot1, rot2, rot3, rot4),
                                'offset': offset,
                                'score': score,
                                'text': text[:80]
                            })

if results:
    results.sort(key=lambda x: x['score'], reverse=True)
    print("\n📊 TOP VARIABLE ROTATION RESULTS:")
    for i, r in enumerate(results[:10]):
        print(f"\n{i+1}. Page {r['page']} | rots={r['rots']} off={r['offset']} | Score: {r['score']:.1f}")
        print(f"   {r['text']}")
else:
    print("\nNo results above threshold.")

print("\n" + "=" * 80)
print("🔍 EXAMINING CHARACTER PATTERNS")
print("=" * 80)

# Analyze which runes appear most frequently in our best decryptions
for page_num, params in BEST_PARAMS.items():
    indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
    
    decrypted = []
    for i, idx in enumerate(indices):
        k1 = MASTER_KEY[(i + params['off1']) % len(MASTER_KEY)]
        if params['method'] == 'double_xor':
            k2 = MASTER_KEY[(i + params['off2']) % len(MASTER_KEY)]
            dec = ((idx ^ k1 ^ params['rot1']) ^ k2 ^ params['rot2']) % 29
        else:
            k2 = MASTER_KEY[(i + params['off2']) % len(MASTER_KEY)]
            dec = (((idx ^ k1 ^ params['rot1']) - k2 - params['rot2']) % 29)
        decrypted.append(dec)
    
    text = indices_to_text(decrypted)
    
    # Count each rune
    from collections import Counter
    counts = Counter(decrypted)
    
    print(f"\n📄 Page {page_num} rune frequency:")
    most_common = counts.most_common(10)
    for idx, count in most_common:
        pct = count / len(decrypted) * 100
        print(f"  {RUNES[idx]:3s} ({idx:2d}): {count:3d} ({pct:5.1f}%) - expected in English: E, T, A, O, I, N...")

print("\n✅ Analysis complete!")

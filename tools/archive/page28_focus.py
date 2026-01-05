#!/usr/bin/env python3
"""
Focus on Page 28 which shows the best single-layer result.
Do extremely fine-grained search around the best parameters.
"""

RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

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

PAGE28 = "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ"

COMMON_WORDS = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAS',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HIM', 'HIS', 'HOW',
    'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'BOY', 'DID',
    'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'WILL', 'WHAT',
    'WHEN', 'YOUR', 'SOME', 'THEM', 'INTO', 'WHICH', 'THERE', 'THEIR', 'ABOUT',
    'WOULD', 'COULD', 'OTHER', 'THESE', 'FIRST', 'BEING', 'THING', 'THOSE',
    'TRUTH', 'LIGHT', 'WISDOM', 'DIVINE', 'SACRED', 'WITHIN', 'KNOWLEDGE',
    'IS', 'IT', 'AS', 'AT', 'BE', 'WE', 'OR', 'AN', 'NO', 'SO', 'IF', 'MY',
    'UP', 'TO', 'GO', 'ME', 'HE', 'BY', 'IN', 'ON', 'OF', 'DO'
}

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
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word) * 2
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 
               'NG', 'OF', 'OR', 'TO', 'IT', 'IS', 'OU', 'AR', 'AS', 'AL',
               'TE', 'SE', 'EA', 'TI', 'VE', 'HA', 'WI', 'HI', 'ES', 'ST']
    for bg in bigrams:
        score += text_upper.count(bg) * 0.5
    return score

print("=" * 80)
print("🔍 PAGE 28 DEEP ANALYSIS")
print("=" * 80)

indices = unicode_to_indices(PAGE28)
print(f"Page 28 has {len(indices)} runes")

# Best result: xor r=2 o=59
print("\n📊 Best single-layer result: XOR rot=2, off=59")
decrypted = []
for i, idx in enumerate(indices):
    key_val = MASTER_KEY[(i + 59) % len(MASTER_KEY)]
    dec = (idx ^ key_val ^ 2) % 29
    decrypted.append(dec)
text = indices_to_text(decrypted)
print(f"Text: {text}")
print(f"Score: {score_text(text):.1f}")

# Find all words
print("\n📖 Finding words in the text:")
text_upper = text.upper()
words_found = []
for word in sorted(COMMON_WORDS, key=len, reverse=True):
    start = 0
    while True:
        pos = text_upper.find(word, start)
        if pos == -1:
            break
        words_found.append((pos, word))
        start = pos + 1

words_found.sort()
print(f"Words found at positions: {words_found}")

# Manual segmentation attempt
print("\n📝 Attempting to read the text:")
print(f"Full text: {text}")
print()

# Highlight words
highlighted = text_upper
for pos, word in sorted(words_found, reverse=True):
    highlighted = highlighted[:pos] + f"[{word}]" + highlighted[pos+len(word):]
print(f"Highlighted: {highlighted}")

# Now test more combinations around this best result
print("\n" + "=" * 80)
print("🔬 FINE SEARCH AROUND BEST PARAMETERS")
print("=" * 80)

best_results = []

# Test nearby rotations and offsets
for rot in range(29):  # All rotations
    for off in range(len(MASTER_KEY)):  # All offsets
        decrypted = []
        for i, idx in enumerate(indices):
            key_val = MASTER_KEY[(i + off) % len(MASTER_KEY)]
            dec = (idx ^ key_val ^ rot) % 29
            decrypted.append(dec)
        text = indices_to_text(decrypted)
        score = score_text(text)
        
        # Count specific patterns
        text_upper = text.upper()
        the_count = text_upper.count('THE')
        th_count = text_upper.count('TH')
        
        if score > 110 or the_count >= 3:
            best_results.append({
                'rot': rot,
                'off': off,
                'score': score,
                'the_count': the_count,
                'th_count': th_count,
                'text': text
            })

best_results.sort(key=lambda x: (x['the_count'], x['score']), reverse=True)
print(f"\nTop results by 'THE' count:")
for i, r in enumerate(best_results[:15]):
    print(f"{i+1}. rot={r['rot']:2d} off={r['off']:2d} THE={r['the_count']} TH={r['th_count']:2d} score={r['score']:.1f}")
    print(f"   {r['text'][:70]}...")

# Check if any result starts with a known word
print("\n" + "=" * 80)
print("🔎 RESULTS STARTING WITH KNOWN WORDS")
print("=" * 80)

starting_words = ['THE', 'AND', 'FOR', 'BUT', 'NOW', 'ALL', 'ONE', 'IT', 'IN', 'TO', 
                  'BE', 'WE', 'IS', 'AS', 'AT', 'IF', 'SO', 'DO', 'OR', 'AN', 'NO',
                  'THIS', 'THAT', 'WHEN', 'THEY', 'WHAT', 'WITH', 'FROM', 'HAVE',
                  'THERE', 'WHICH', 'THEIR', 'THESE', 'THOSE', 'FIRST', 'WITHIN']

for rot in range(29):
    for off in range(len(MASTER_KEY)):
        decrypted = []
        for i, idx in enumerate(indices):
            key_val = MASTER_KEY[(i + off) % len(MASTER_KEY)]
            dec = (idx ^ key_val ^ rot) % 29
            decrypted.append(dec)
        text = indices_to_text(decrypted)
        text_upper = text.upper()
        
        for word in starting_words:
            if text_upper.startswith(word):
                score = score_text(text)
                print(f"Starts with '{word}': rot={rot} off={off} score={score:.1f}")
                print(f"  {text[:70]}...")
                break

# Also try subtraction
print("\n" + "=" * 80)
print("🔎 SUBTRACTION - RESULTS STARTING WITH KNOWN WORDS")
print("=" * 80)

for rot in range(29):
    for off in range(len(MASTER_KEY)):
        decrypted = []
        for i, idx in enumerate(indices):
            key_val = MASTER_KEY[(i + off) % len(MASTER_KEY)]
            dec = (idx - key_val - rot) % 29
            decrypted.append(dec)
        text = indices_to_text(decrypted)
        text_upper = text.upper()
        
        for word in starting_words:
            if text_upper.startswith(word):
                score = score_text(text)
                if score > 90:
                    print(f"Starts with '{word}': rot={rot} off={off} score={score:.1f}")
                    print(f"  {text[:70]}...")
                break

print("\n✅ Analysis complete!")

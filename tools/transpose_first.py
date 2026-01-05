#!/usr/bin/env python3
"""
Transpose BEFORE decryption approach.
The cipher may be: Transpose -> Encrypt
So we need: Decrypt -> Untranspose (or Untranspose -> Decrypt)

Try columnar untransposition BEFORE applying decryption.
"""

# Gematria Primus - 29 runes
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

# Master key from Page 0 - Page 57
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

# Unicode to rune mapping
RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

# Unsolved pages data
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

UNSOLVED = [27, 28, 29, 30, 31, 40, 41, 44, 45, 46, 47, 48, 52]

def unicode_to_indices(text):
    """Convert Unicode runes to indices."""
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

# English words for scoring
COMMON_WORDS = {
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'IT',
    'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT', 'THIS',
    'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE', 'OR',
    'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
    'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH', 'GO', 'ME',
    'WHEN', 'MAKE', 'CAN', 'LIKE', 'TIME', 'NO', 'JUST', 'HIM', 'KNOW',
    'IS', 'I', 'ARE', 'WAS', 'WERE', 'NOW', 'THEN', 'HERE', 'HOW', 'THAN',
    'THEM', 'WAY', 'THESE', 'INTO', 'THOSE', 'SOME', 'ONLY', 'MAY', 'MUST',
    'BEING', 'THING', 'DIVINE', 'WISDOM', 'TRUTH', 'LIGHT', 'SEEK', 'FIND',
    'PATH', 'SELF', 'MIND', 'EYE', 'SEE', 'HEAR', 'FEEL', 'THINK', 'KNOW',
    'WITHIN', 'WITHOUT', 'ABOVE', 'BELOW', 'THROUGH', 'BEYOND', 'BEFORE',
    'AFTER', 'SACRED', 'PRIMES', 'CICADA', 'SECRET', 'HIDDEN', 'REVEAL',
    'OUR', 'US', 'YOUR', 'LOVE', 'LIFE', 'DEATH', 'MANY', 'EACH', 'EVERY',
    'OTHER', 'WORLD', 'OVER', 'UNDER', 'SUCH', 'VERY', 'EVEN', 'NEW', 'OLD',
    'FIRST', 'LAST', 'LONG', 'GREAT', 'LITTLE', 'OWN', 'SAME', 'MAN', 'WOMAN',
    'ANY', 'WORK', 'PART', 'TAKE', 'COME', 'COULD', 'GOOD', 'BAD', 'GIVE'
}

def get_page_indices(page_num):
    """Get rune indices for a page."""
    if page_num not in UNSOLVED_PAGES:
        return None
    return unicode_to_indices(UNSOLVED_PAGES[page_num])

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(RUNES[i] for i in indices)

def columnar_untranspose(indices, width):
    """Undo columnar transposition - read by rows, write by columns."""
    n = len(indices)
    height = (n + width - 1) // width
    full_cols = n % width if n % width != 0 else width
    
    # Create grid
    result = []
    pos = 0
    grid = [[] for _ in range(height)]
    
    for col in range(width):
        col_height = height if col < full_cols else height - 1
        for row in range(col_height):
            if pos < n:
                grid[row].append(indices[pos])
                pos += 1
    
    # Read by rows
    return [item for row in grid for item in row]

def columnar_transpose(indices, width):
    """Apply columnar transposition - read by columns, write by rows."""
    n = len(indices)
    height = (n + width - 1) // width
    
    # Fill grid row by row
    grid = []
    pos = 0
    for row in range(height):
        grid.append([])
        for col in range(width):
            if pos < n:
                grid[row].append(indices[pos])
                pos += 1
    
    # Read by columns
    result = []
    for col in range(width):
        for row in range(height):
            if col < len(grid[row]):
                result.append(grid[row][col])
    
    return result

def decrypt_sub(indices, key_indices, rotation=0, offset=0):
    """Decrypt using subtraction."""
    result = []
    key_len = len(key_indices)
    for i, idx in enumerate(indices):
        key_val = key_indices[(i + offset) % key_len]
        decrypted = (idx - key_val - rotation) % 29
        result.append(decrypted)
    return result

def decrypt_xor(indices, key_indices, rotation=0, offset=0):
    """Decrypt using XOR."""
    result = []
    key_len = len(key_indices)
    for i, idx in enumerate(indices):
        key_val = key_indices[(i + offset) % key_len]
        decrypted = (idx ^ key_val ^ rotation) % 29
        result.append(decrypted)
    return result

def decrypt_add(indices, key_indices, rotation=0, offset=0):
    """Decrypt using addition."""
    result = []
    key_len = len(key_indices)
    for i, idx in enumerate(indices):
        key_val = key_indices[(i + offset) % key_len]
        decrypted = (idx + key_val + rotation) % 29
        result.append(decrypted)
    return result

def score_text(text):
    """Score based on English word patterns."""
    score = 0
    text_upper = text.upper()
    
    for word in COMMON_WORDS:
        count = text_upper.count(word)
        score += count * len(word)
    
    # Bonus for common bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 
               'NG', 'OF', 'OR', 'TO', 'IT', 'IS', 'OU', 'AR', 'AS', 'AL',
               'TE', 'SE', 'EA', 'TI', 'VE', 'HA', 'WI', 'HI', 'ES', 'ST']
    for bg in bigrams:
        score += text_upper.count(bg) * 0.5
    
    return score

def count_words(text):
    """Count how many common words appear."""
    text_upper = text.upper()
    count = 0
    for word in COMMON_WORDS:
        if word in text_upper:
            count += text_upper.count(word)
    return count

print("=" * 80)
print("🔄 TRANSPOSE-FIRST APPROACH")
print("=" * 80)
print("\nTesting: Columnar Untranspose BEFORE decryption")
print()

best_results = []

for page_num in UNSOLVED:
    indices = get_page_indices(page_num)
    if not indices:
        continue
    
    page_best = []
    
    # Test different column widths
    for width in range(2, 20):
        # Try untransposing first
        untransposed = columnar_untranspose(indices, width)
        
        # Then decrypt with different methods and parameters
        for rotation in range(0, 29, 2):  # Step by 2 for speed
            for offset in range(0, min(95, len(indices)), 5):  # Step by 5
                
                # Subtraction
                decrypted = decrypt_sub(untransposed, MASTER_KEY, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score > 120:
                    page_best.append({
                        'page': page_num,
                        'method': 'untranspose_sub',
                        'width': width,
                        'rotation': rotation,
                        'offset': offset,
                        'score': score,
                        'text': text[:100]
                    })
                
                # XOR
                decrypted = decrypt_xor(untransposed, MASTER_KEY, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score > 120:
                    page_best.append({
                        'page': page_num,
                        'method': 'untranspose_xor',
                        'width': width,
                        'rotation': rotation,
                        'offset': offset,
                        'score': score,
                        'text': text[:100]
                    })
                
                # Addition
                decrypted = decrypt_add(untransposed, MASTER_KEY, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score > 120:
                    page_best.append({
                        'page': page_num,
                        'method': 'untranspose_add',
                        'width': width,
                        'rotation': rotation,
                        'offset': offset,
                        'score': score,
                        'text': text[:100]
                    })
    
    # Also try transposing (not untransposing) first
    for width in range(2, 20):
        transposed = columnar_transpose(indices, width)
        
        for rotation in range(0, 29, 2):
            for offset in range(0, min(95, len(indices)), 5):
                
                decrypted = decrypt_sub(transposed, MASTER_KEY, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score > 120:
                    page_best.append({
                        'page': page_num,
                        'method': 'transpose_sub',
                        'width': width,
                        'rotation': rotation,
                        'offset': offset,
                        'score': score,
                        'text': text[:100]
                    })
                
                decrypted = decrypt_xor(transposed, MASTER_KEY, rotation, offset)
                text = indices_to_text(decrypted)
                score = score_text(text)
                if score > 120:
                    page_best.append({
                        'page': page_num,
                        'method': 'transpose_xor',
                        'width': width,
                        'rotation': rotation,
                        'offset': offset,
                        'score': score,
                        'text': text[:100]
                    })
    
    if page_best:
        # Sort and keep top results
        page_best.sort(key=lambda x: x['score'], reverse=True)
        best_results.extend(page_best[:5])  # Top 5 per page
        
        print(f"\n📄 Page {page_num}: Found {len(page_best)} results above threshold")
        for r in page_best[:3]:
            print(f"   {r['method']} w={r['width']} r={r['rotation']} o={r['offset']}: {r['score']:.1f}")
            print(f"   Text: {r['text'][:60]}...")
    else:
        print(f"\n📄 Page {page_num}: No results above 120")

print("\n" + "=" * 80)
print("📊 TOP RESULTS WITH TRANSPOSE-FIRST")
print("=" * 80)

if best_results:
    best_results.sort(key=lambda x: x['score'], reverse=True)
    for i, r in enumerate(best_results[:20]):
        print(f"\n{i+1}. Page {r['page']} | {r['method']} w={r['width']} r={r['rotation']} o={r['offset']} | Score: {r['score']:.1f}")
        print(f"   {r['text']}")
else:
    print("\nNo high-scoring results found with transpose-first approach.")

# Also test: different transposition schemes
print("\n" + "=" * 80)
print("🔄 TESTING SKIP CIPHER BEFORE DECRYPTION")
print("=" * 80)

def skip_reorder(indices, skip):
    """Reorder by reading every nth character."""
    n = len(indices)
    result = []
    visited = [False] * n
    pos = 0
    while len(result) < n:
        if not visited[pos]:
            result.append(indices[pos])
            visited[pos] = True
        pos = (pos + skip) % n
        # Safety: if we're stuck, find next unvisited
        if visited[pos]:
            for i in range(n):
                if not visited[i]:
                    pos = i
                    break
            else:
                break
    return result

skip_results = []

for page_num in [28, 44, 52]:  # Focus on best pages
    indices = get_page_indices(page_num)
    if not indices:
        continue
    
    for skip in range(2, 20):
        try:
            reordered = skip_reorder(indices, skip)
            
            for rotation in range(0, 29, 2):
                for offset in range(0, min(95, len(indices)), 5):
                    
                    decrypted = decrypt_xor(reordered, MASTER_KEY, rotation, offset)
                    text = indices_to_text(decrypted)
                    score = score_text(text)
                    if score > 130:
                        skip_results.append({
                            'page': page_num,
                            'skip': skip,
                            'rotation': rotation,
                            'offset': offset,
                            'score': score,
                            'text': text[:100]
                        })
        except:
            continue

if skip_results:
    skip_results.sort(key=lambda x: x['score'], reverse=True)
    print("\nTop skip cipher results:")
    for r in skip_results[:10]:
        print(f"  Page {r['page']} skip={r['skip']} r={r['rotation']} o={r['offset']}: {r['score']:.1f}")
        print(f"  {r['text'][:60]}...")
else:
    print("\nNo high-scoring skip cipher results.")

print("\n✅ Analysis complete!")

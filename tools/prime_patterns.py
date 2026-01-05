#!/usr/bin/env python3
"""
Investigate prime-based patterns and the significance of 1331 = 11³
The master key sum is 11³, which suggests 11 is important.
Try grouping by 11, modular arithmetic with 11, etc.
"""

# Gematria Primus - 29 runes with prime values
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
         'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
          73, 79, 83, 89, 97, 101, 103, 107, 109]

RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
IDX_TO_PRIME = {i: p for i, p in enumerate(PRIMES)}

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

# Common English words for scoring
COMMON_WORDS = {
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'IT',
    'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT', 'THIS',
    'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE', 'OR',
    'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
    'SO', 'UP', 'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH', 'GO', 'ME',
    'WHEN', 'MAKE', 'CAN', 'LIKE', 'TIME', 'NO', 'JUST', 'HIM', 'KNOW',
    'IS', 'I', 'ARE', 'WAS', 'WERE', 'NOW', 'THEN', 'HERE', 'HOW', 'THAN',
    'THEM', 'WAY', 'THESE', 'INTO', 'THOSE', 'SOME', 'ONLY', 'MAY', 'MUST',
    'BEING', 'THING', 'DIVINE', 'WISDOM', 'TRUTH', 'LIGHT', 'SEEK', 'FIND'
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
        score += count * len(word)
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 
               'NG', 'OF', 'OR', 'TO', 'IT', 'IS', 'OU', 'AR', 'AS', 'AL']
    for bg in bigrams:
        score += text_upper.count(bg) * 0.5
    return score

print("=" * 80)
print("🔢 PRIME PATTERN ANALYSIS")
print("=" * 80)

print("\n📊 Analyzing key structure:")
print(f"Key length: {len(MASTER_KEY)}")
print(f"Key sum: {sum(MASTER_KEY)} = 11³ = 1331")
print(f"Average key value: {sum(MASTER_KEY)/len(MASTER_KEY):.2f}")

# Group key by 11s
print("\n🔢 Key grouped by 11s:")
for i in range(0, len(MASTER_KEY), 11):
    chunk = MASTER_KEY[i:i+11]
    print(f"  [{i:2d}-{min(i+10, len(MASTER_KEY)-1):2d}]: {chunk} → sum = {sum(chunk)}")

# Check if each group of 11 has special properties
print("\n🔍 Properties of each group of 11:")
for i in range(0, len(MASTER_KEY), 11):
    chunk = MASTER_KEY[i:i+11]
    chunk_sum = sum(chunk)
    print(f"  Group {i//11}: sum={chunk_sum}, mod11={chunk_sum % 11}, mod29={chunk_sum % 29}")

# Convert key to prime values
print("\n🔢 Key as prime values:")
prime_key = [PRIMES[k] for k in MASTER_KEY]
print(f"Sum of primes: {sum(prime_key)}")
print(f"Product would be: (too large to compute)")

# Test different decryption approaches based on 11
print("\n" + "=" * 80)
print("🧪 TESTING 11-BASED APPROACHES")
print("=" * 80)

results = []

for page_num in [28, 44, 52]:  # Focus on best pages
    indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
    n = len(indices)
    
    print(f"\n📄 Page {page_num} (length {n}):")
    
    # Approach 1: Divide text into 11 sections, process each differently
    section_size = n // 11
    
    # Approach 2: Use key[i mod 11] instead of full key
    print("  Testing mod 11 key indexing...")
    for rotation in range(29):
        for offset in range(11):  # Only 11 offsets matter now
            decrypted = []
            for i, idx in enumerate(indices):
                key_idx = (i + offset) % 11  # Cycle through first 11 key values
                key_val = MASTER_KEY[key_idx]
                dec = (idx - key_val - rotation) % 29
                decrypted.append(dec)
            text = indices_to_text(decrypted)
            score = score_text(text)
            if score > 80:
                results.append({
                    'page': page_num,
                    'method': 'mod11_sub',
                    'rotation': rotation,
                    'offset': offset,
                    'score': score,
                    'text': text[:80]
                })
    
    # Approach 3: XOR with mod 11 key
    print("  Testing mod 11 XOR...")
    for rotation in range(29):
        for offset in range(11):
            decrypted = []
            for i, idx in enumerate(indices):
                key_idx = (i + offset) % 11
                key_val = MASTER_KEY[key_idx]
                dec = (idx ^ key_val ^ rotation) % 29
                decrypted.append(dec)
            text = indices_to_text(decrypted)
            score = score_text(text)
            if score > 80:
                results.append({
                    'page': page_num,
                    'method': 'mod11_xor',
                    'rotation': rotation,
                    'offset': offset,
                    'score': score,
                    'text': text[:80]
                })
    
    # Approach 4: Try groups based on position mod 11
    print("  Testing 11-interleaved decryption...")
    for rotation in range(29):
        for offset in range(min(11, len(indices))):
            decrypted = [0] * n
            for group in range(11):
                # Process every 11th character starting from offset
                for i, pos in enumerate(range(group, n, 11)):
                    key_val = MASTER_KEY[(i + offset) % len(MASTER_KEY)]
                    decrypted[pos] = (indices[pos] - key_val - rotation) % 29
            text = indices_to_text(decrypted)
            score = score_text(text)
            if score > 80:
                results.append({
                    'page': page_num,
                    'method': '11_interleaved',
                    'rotation': rotation,
                    'offset': offset,
                    'score': score,
                    'text': text[:80]
                })

# Sort and display results
if results:
    results.sort(key=lambda x: x['score'], reverse=True)
    print("\n" + "=" * 80)
    print("📊 TOP RESULTS WITH PRIME/11 PATTERNS")
    print("=" * 80)
    for i, r in enumerate(results[:20]):
        print(f"\n{i+1}. Page {r['page']} | {r['method']} r={r['rotation']} o={r['offset']} | Score: {r['score']:.1f}")
        print(f"   {r['text']}")
else:
    print("\nNo results above threshold with 11-based approaches.")

# Additional investigation: What if the cipher uses prime index values?
print("\n" + "=" * 80)
print("🔢 PRIME VALUE-BASED DECRYPTION")
print("=" * 80)

for page_num in [28, 44, 52]:
    indices = unicode_to_indices(UNSOLVED_PAGES[page_num])
    
    # Convert indices to prime values, then back
    prime_text = [IDX_TO_PRIME[idx] for idx in indices]
    prime_key = [PRIMES[k] for k in MASTER_KEY[:len(indices)]]
    
    # Subtract prime values
    decrypted_primes = [(p - k) % 113 for p, k in zip(prime_text, prime_key)]  # 113 is largest prime
    
    # Try to map back to rune indices
    PRIME_TO_IDX = {p: i for i, p in enumerate(PRIMES)}
    
    # See if any make sense
    valid_count = sum(1 for p in decrypted_primes if p in PRIME_TO_IDX)
    print(f"Page {page_num}: {valid_count}/{len(decrypted_primes)} map to valid primes")

print("\n✅ Analysis complete!")

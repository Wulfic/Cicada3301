#!/usr/bin/env python3
"""
Analyze the discovered SUB keys for patterns.
All pages use SUB mod 29 with prime-length keys.

Looking for:
1. Common sequences between keys
2. Keys that spell something in Gematria
3. Mathematical relationships
4. Keys that match Cicada content
"""

# Gematria Primus - 29 characters
GEMATRIA = ['F', 'U', 'TH', 'O', 'R', 'C/K', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S/Z', 'T', 'B', 'E', 'M',
            'L', 'ING', 'OE', 'D', 'A', 'AE', 'Y', 'IA/IO', 'EA']

PRIME_VALUES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                73, 79, 83, 89, 97, 101, 103, 107, 109]

# Discovered keys
KEYS = {
    0: [19, 6, 23, 16, 10, 22, 9, 27, 26, 11, 16, 3, 19, 0, 12, 7, 23, 17, 7, 1, 1, 5, 28, 7, 20, 21, 15, 1, 17, 20, 23, 8, 22, 9, 20, 16, 7, 8, 13, 22, 15, 10, 2, 11, 22, 22, 4, 9, 19, 24, 1, 8, 12, 18, 21, 11, 21, 22, 21, 12, 7, 6, 13, 1, 14, 12, 26, 11, 11, 5, 27, 21, 25, 8, 22, 15, 20, 4, 20, 4, 19, 26, 0, 19, 1, 6, 2, 3, 22, 26, 24, 1, 19, 22, 12, 0, 21, 18, 20, 5, 17, 4, 24, 10, 19, 14, 19, 7, 12, 12, 14, 16, 2],  # len 113
    1: [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7],  # len 71
    2: [4, 23, 28, 26, 20, 28, 4, 15, 21, 18, 25, 2, 10, 4, 5, 6, 3, 27, 5, 24, 27, 15, 15, 12, 10, 15, 0, 14, 5, 11, 11, 8, 25, 21, 28, 16, 20, 11, 2, 14, 10, 10, 15, 14, 4, 0, 19, 1, 8, 26, 19, 7, 19, 20, 14, 10, 7, 4, 26, 2, 20, 18, 7, 8, 3, 16, 27, 1, 2, 1, 3, 6, 10, 19, 10, 12, 14, 28, 4, 8, 16, 10, 16],  # len 83
    3: [6, 0, 11, 19, 27, 27, 22, 2, 4, 16, 28, 1, 11, 14, 1, 19, 21, 0, 2, 17, 23, 5, 3, 18, 23, 9, 18, 14, 19, 3, 11, 21, 22, 15, 20, 19, 12, 13, 18, 8, 20, 26, 28, 17, 24, 12, 3, 10, 11, 20, 21, 0, 5, 9, 2, 16, 5, 0, 9, 4, 1, 21, 11, 27, 5, 21, 13, 14, 2, 26, 0, 23, 14, 17, 28, 27, 4, 13, 6, 20, 16, 8, 9],  # len 83
    4: [1, 23, 19, 6, 17, 13, 0, 7, 27, 25, 20, 27, 11, 5, 27, 23, 14, 18, 8, 20, 6, 19, 23, 4, 21, 18, 11, 8, 22, 28, 9, 9, 23, 21, 8, 6, 25, 0, 28, 11, 9, 10, 20, 13, 28, 15, 19, 1, 9, 15, 2, 3, 0, 27, 18, 19, 19, 1, 10, 4, 28, 3, 15, 8, 8, 17, 3, 24, 27, 1, 25, 4, 23, 0, 8, 19, 10, 21, 2, 26, 21, 19, 16, 10, 24, 1, 24, 2, 10, 26, 12, 11, 5, 8, 13, 28, 9, 16, 1, 14, 9, 1, 0]  # len 103
}

def indices_to_text(indices):
    """Convert indices to text"""
    result = []
    for idx in indices:
        idx = idx % 29
        glyph = GEMATRIA[idx]
        if '/' in glyph:
            glyph = glyph.split('/')[0]
        result.append(glyph)
    return ''.join(result)

print("=" * 60)
print("KEY ANALYSIS FOR PAGES 0-4")
print("=" * 60)
print()

# Basic statistics
print("-" * 60)
print("BASIC KEY STATISTICS")
print("-" * 60)

for page, key in KEYS.items():
    key_text = indices_to_text(key)
    key_sum = sum(key)
    key_avg = sum(key) / len(key)
    key_mod29 = key_sum % 29
    
    # Frequency of each index
    freq = {}
    for k in key:
        freq[k] = freq.get(k, 0) + 1
    most_common = sorted(freq.items(), key=lambda x: -x[1])[:5]
    
    print(f"Page {page}: length={len(key)}")
    print(f"  Sum={key_sum}, Avg={key_avg:.2f}, Sum mod 29={key_mod29} ({GEMATRIA[key_mod29]})")
    print(f"  Most common: {most_common}")
    print(f"  As text: {key_text[:60]}...")
    print()

# Look for common subsequences
print("-" * 60)
print("COMMON SUBSEQUENCES (length 3+)")
print("-" * 60)

def find_subsequences(key, min_len=3):
    """Find all subsequences of given minimum length"""
    subseqs = set()
    for length in range(min_len, min(10, len(key))):
        for i in range(len(key) - length + 1):
            subseqs.add(tuple(key[i:i+length]))
    return subseqs

all_subseqs = {page: find_subsequences(key) for page, key in KEYS.items()}

# Find common across pages
for i in range(5):
    for j in range(i+1, 5):
        common = all_subseqs[i] & all_subseqs[j]
        if common:
            longest = max(common, key=len)
            print(f"Pages {i} & {j}: {len(common)} common, longest: {list(longest)}")
            if len(longest) >= 4:
                print(f"  As text: {indices_to_text(list(longest))}")

print()

# Check if keys match known Cicada words
print("-" * 60)
print("MATCH AGAINST CICADA VOCABULARY")
print("-" * 60)

def text_to_indices(text):
    clean = ''.join(text.upper().split())
    indices = []
    i = 0
    while i < len(clean):
        found = False
        for length in [3, 2, 1]:
            if i + length <= len(clean):
                chunk = clean[i:i+length]
                for j, glyph in enumerate(GEMATRIA):
                    if glyph == chunk or (len(glyph) > 1 and chunk in glyph.split('/')):
                        indices.append(j)
                        i += length
                        found = True
                        break
                if found:
                    break
        if not found:
            for j, glyph in enumerate(GEMATRIA):
                if clean[i] in glyph.split('/')[0]:
                    indices.append(j)
                    break
            i += 1
    return indices

cicada_words = [
    "DIVINITY", "CIRCUMFERENCE", "INSTAR", "EMERGE", "PARABLE",
    "PRIMES", "SACRED", "TOTIENT", "CONSUMPTION", "PRESERVATION",
    "ADHERENCE", "WARNING", "WISDOM", "KOAN", "INSTRUCTION",
    "WELCOME", "PILGRIM", "JOURNEY", "TRUTH", "KNOWLEDGE"
]

for word in cicada_words:
    word_indices = text_to_indices(word)
    
    # Check if word appears in any key
    for page, key in KEYS.items():
        for start in range(len(key) - len(word_indices) + 1):
            if key[start:start+len(word_indices)] == word_indices:
                print(f"FOUND '{word}' in Page {page} key at position {start}")

# Check windowed matching
print("\nPartial matches (5+ char subsequences):")
for word in cicada_words:
    if len(word) >= 5:
        word_indices = text_to_indices(word)
        for page, key in KEYS.items():
            for win_len in range(5, min(8, len(word_indices))):
                for start in range(len(word_indices) - win_len + 1):
                    window = word_indices[start:start+win_len]
                    for key_start in range(len(key) - win_len + 1):
                        if key[key_start:key_start+win_len] == window:
                            print(f"  '{word}' fragment ({indices_to_text(window)}) in Page {page} at pos {key_start}")

print()

# Mathematical analysis
print("-" * 60)
print("MATHEMATICAL PATTERNS")
print("-" * 60)

# Check for arithmetic progressions
for page, key in KEYS.items():
    diffs = [key[i+1] - key[i] for i in range(len(key)-1)]
    
    # Look for repeating difference patterns
    for period in range(2, 20):
        matches = 0
        for i in range(len(diffs) - period):
            if diffs[i] == diffs[i + period]:
                matches += 1
        if matches > len(diffs) // 4:  # More than 25% match
            print(f"Page {page}: Period {period} has {matches} matching diffs")
    
    # Check if differences are special
    unique_diffs = set(diffs)
    if len(unique_diffs) < 15:
        print(f"Page {page}: Only {len(unique_diffs)} unique differences: {sorted(unique_diffs)[:10]}")

print()

# Compare keys as prime values
print("-" * 60)
print("PRIME VALUE ANALYSIS")
print("-" * 60)

for page, key in KEYS.items():
    prime_key = [PRIME_VALUES[k] for k in key]
    prime_sum = sum(prime_key)
    
    # Check if prime sum has special properties
    print(f"Page {page}: Prime value sum = {prime_sum}")
    
    # Difference from nearest prime
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                return False
        return True
    
    for offset in range(-10, 11):
        if is_prime(prime_sum + offset):
            print(f"  {prime_sum} + {offset} = {prime_sum + offset} (prime)")
            break

print()

# XOR and other operations between keys
print("-" * 60)
print("CROSS-KEY OPERATIONS")
print("-" * 60)

# Check if Pages 2 and 3 keys (both length 83) are related
key2 = KEYS[2]
key3 = KEYS[3]

print("Pages 2 & 3 (both length 83):")

# XOR
xor_result = [(key2[i] ^ key3[i]) for i in range(83)]
print(f"  XOR result: {xor_result[:20]}...")
print(f"  XOR as text: {indices_to_text([x % 29 for x in xor_result])[:40]}")

# Difference
diff_result = [(key2[i] - key3[i]) % 29 for i in range(83)]
print(f"  Diff mod 29: {diff_result[:20]}...")
print(f"  Diff as text: {indices_to_text(diff_result)[:40]}")

# Sum
sum_result = [(key2[i] + key3[i]) % 29 for i in range(83)]
print(f"  Sum mod 29: {sum_result[:20]}...")
print(f"  Sum as text: {indices_to_text(sum_result)[:40]}")

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

"""
Attempt first-layer decryption on pages with prime key lengths and high IoC.
Focus on pages with strongest signals.
"""

from collections import Counter
import os

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

IDX_TO_RUNE = {v: k for k, v in RUNE_TO_IDX.items()}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

# English frequency order (single letters in Gematria)
ENGLISH_FREQ_ORDER = [18, 16, 24, 3, 10, 9, 15, 8, 4, 20, 23, 5, 1, 19, 13, 26, 6, 17, 0, 7, 14, 11, 12, 21, 22, 25, 27, 28, 2]

def load_page(page_num):
    """Load runes from a page."""
    path = f"../pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return None, None
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Keep structure (words separated by hyphens)
    words = []
    rune_indices = []
    
    for part in content.replace('\n', ' ').split('-'):
        word_runes = [c for c in part if c in RUNE_TO_IDX]
        if word_runes:
            words.append(word_runes)
            rune_indices.extend([RUNE_TO_IDX[r] for r in word_runes])
    
    return rune_indices, words

def find_key_by_frequency(cipher_indices, key_length):
    """Find key by frequency analysis on each coset."""
    # Split into cosets
    cosets = [[] for _ in range(key_length)]
    for i, idx in enumerate(cipher_indices):
        cosets[i % key_length].append(idx)
    
    # For each coset, find shift that best matches English frequency
    key = []
    for coset in cosets:
        if not coset:
            key.append(0)
            continue
        
        # Count frequencies
        freq = Counter(coset)
        
        # Find most common rune in coset
        most_common = freq.most_common(1)[0][0]
        
        # Assume most common maps to E (index 18) in English
        # c - k = p, so k = c - p
        shift = (most_common - 18) % 29
        key.append(shift)
    
    return key

def decrypt_with_key(cipher_indices, key):
    """Decrypt using subtraction: p = c - k mod 29."""
    key_length = len(key)
    plain = []
    for i, c in enumerate(cipher_indices):
        k = key[i % key_length]
        p = (c - k) % 29
        plain.append(p)
    return plain

def indices_to_letters(indices):
    """Convert indices to letter string."""
    return ''.join(IDX_TO_LETTER[i] for i in indices)

def count_english_patterns(letters):
    """Count English-like patterns."""
    score = 0
    # Count THE, AND, FOR, etc.
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT']
    for word in common_words:
        score += letters.count(word) * len(word)
    
    # Count TH digraph
    score += letters.count('TH') * 2
    
    return score

def analyze_page(page_num, key_length):
    """Analyze a page with given key length."""
    cipher_indices, words = load_page(page_num)
    if not cipher_indices:
        print(f"Page {page_num}: No data")
        return None
    
    print(f"\n{'='*70}")
    print(f"PAGE {page_num} - Key Length {key_length}")
    print(f"{'='*70}")
    print(f"Total runes: {len(cipher_indices)}, Words: {len(words)}")
    
    # Find key by frequency analysis
    key = find_key_by_frequency(cipher_indices, key_length)
    print(f"\nDerived key (first 30): {key[:30]}...")
    
    # Decrypt
    plain_indices = decrypt_with_key(cipher_indices, key)
    
    # Convert to letters
    letters = indices_to_letters(plain_indices)
    print(f"\nFirst 200 chars of decryption:")
    print(letters[:200])
    
    # Score
    score = count_english_patterns(letters)
    print(f"\nEnglish pattern score: {score}")
    
    # Count specific digraphs/trigraphs
    th_count = letters.count('TH')
    the_count = letters.count('THE')
    and_count = letters.count('AND')
    ing_count = letters.count('ING')
    print(f"TH: {th_count}, THE: {the_count}, AND: {and_count}, ING: {ing_count}")
    
    # Check for EMB pattern (found in previous analysis)
    emb_count = letters.count('EMB')
    print(f"EMB (mystery pattern): {emb_count}")
    
    # Reconstructed with word boundaries
    print(f"\nWord-by-word reconstruction (first 20 words):")
    word_idx = 0
    for word_runes in words[:20]:
        word_cipher = [RUNE_TO_IDX[r] for r in word_runes]
        word_plain = []
        for i, c in enumerate(word_cipher):
            k = key[word_idx % key_length]
            p = (c - k) % 29
            word_plain.append(IDX_TO_LETTER[p])
            word_idx += 1
        print(f"  {''.join(word_plain)}", end=" ")
    print()
    
    return {
        'page': page_num,
        'key_length': key_length,
        'letters': letters,
        'score': score,
        'th_count': th_count,
        'the_count': the_count,
        'emb_count': emb_count
    }

def main():
    # Best candidate pages (prime key lengths, high IoC)
    candidates = [
        (8, 101),   # Prime, IoC 0.0726
        (46, 109),  # Prime, IoC 0.0948 (highest!)
        (13, 83),   # Prime, IoC 0.0763
        (43, 71),   # Prime, IoC 0.0681
        (17, 107),  # Prime, IoC 0.0623
        (21, 107),  # Prime, IoC 0.0810
    ]
    
    results = []
    for page, kl in candidates:
        result = analyze_page(page, kl)
        if result:
            results.append(result)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY - Best Decryption Candidates")
    print("="*70)
    print(f"{'Page':>4} | {'Key Len':>7} | {'Score':>5} | {'TH':>4} | {'THE':>4} | {'EMB':>4}")
    print("-" * 45)
    for r in results:
        print(f"{r['page']:4d} | {r['key_length']:7d} | {r['score']:5d} | {r['th_count']:4d} | {r['the_count']:4d} | {r['emb_count']:4d}")

if __name__ == '__main__':
    main()

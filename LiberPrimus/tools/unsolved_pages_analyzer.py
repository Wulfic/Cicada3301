"""
Comprehensive analyzer for truly UNSOLVED pages (segments 0.7-0.12)
These correspond to our pages 8-54 in the workspace.
"""

import os
from collections import Counter

# Gematria Primus mapping
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

def load_runes(page_num):
    """Load runes from a page file."""
    path = f"../pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return None
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract only runes
    runes = [c for c in content if c in RUNE_TO_IDX]
    return runes

def compute_ioc(indices, key_length):
    """Compute average IoC for a given key length."""
    if len(indices) < key_length * 2:
        return 0.0
    
    cosets = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        cosets[i % key_length].append(idx)
    
    ioc_sum = 0.0
    valid_cosets = 0
    for coset in cosets:
        if len(coset) < 2:
            continue
        freqs = Counter(coset)
        n = len(coset)
        ioc = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
        ioc_sum += ioc
        valid_cosets += 1
    
    if valid_cosets == 0:
        return 0.0
    return ioc_sum / valid_cosets

def find_best_key_lengths(indices, max_length=150, top_n=5):
    """Find the best key lengths by IoC analysis."""
    results = []
    for kl in range(2, min(max_length, len(indices) // 2)):
        ioc = compute_ioc(indices, kl)
        results.append((kl, ioc))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]

def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def analyze_page(page_num):
    """Analyze a single page."""
    runes = load_runes(page_num)
    if not runes:
        return None
    
    indices = [RUNE_TO_IDX[r] for r in runes]
    
    # Find best key lengths
    best_kls = find_best_key_lengths(indices)
    
    # Find word count (hyphen-separated)
    path = f"../pages/page_{page_num:02d}/runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    words = [w for w in content.replace('\n', ' ').split('-') if any(c in RUNE_TO_IDX for c in w)]
    
    return {
        'page': page_num,
        'rune_count': len(runes),
        'word_count': len(words),
        'best_key_lengths': best_kls,
        'top_key_length': best_kls[0][0] if best_kls else None,
        'top_ioc': best_kls[0][1] if best_kls else 0.0,
        'is_prime': is_prime(best_kls[0][0]) if best_kls else False
    }

def main():
    print("=" * 80)
    print("UNSOLVED PAGES ANALYSIS (Segments 0.7-0.12 = Our Pages 8-54)")
    print("=" * 80)
    print()
    
    results = []
    
    # Analyze pages 6-55 (segments 0.6-0.12 plus some margin)
    for page_num in range(6, 56):
        result = analyze_page(page_num)
        if result:
            results.append(result)
    
    if not results:
        print("No pages found!")
        return
    
    # Summary table
    print(f"{'Page':>4} | {'Runes':>6} | {'Words':>5} | {'Top Key':>8} | {'IoC':>6} | {'Prime?':>6} | Top 5 Key Lengths")
    print("-" * 90)
    
    for r in results:
        top_kls_str = ', '.join([f"{kl}({ioc:.4f})" for kl, ioc in r['best_key_lengths']])
        prime_mark = "✓" if r['is_prime'] else ""
        print(f"{r['page']:4d} | {r['rune_count']:6d} | {r['word_count']:5d} | {r['top_key_length']:8d} | {r['top_ioc']:.4f} | {prime_mark:^6} | {top_kls_str}")
    
    print()
    print("=" * 80)
    print("KEY LENGTH FREQUENCY ACROSS PAGES")
    print("=" * 80)
    
    # Count key length occurrences
    kl_counter = Counter()
    for r in results:
        for kl, ioc in r['best_key_lengths'][:3]:  # Top 3
            kl_counter[kl] += 1
    
    print("\nMost common key lengths (in top 3 for each page):")
    for kl, count in kl_counter.most_common(15):
        prime_mark = "PRIME" if is_prime(kl) else ""
        print(f"  Key length {kl}: appears in {count} pages {prime_mark}")
    
    # Group pages by similar key lengths
    print()
    print("=" * 80)
    print("PAGES GROUPED BY TOP KEY LENGTH")
    print("=" * 80)
    
    kl_groups = {}
    for r in results:
        kl = r['top_key_length']
        if kl not in kl_groups:
            kl_groups[kl] = []
        kl_groups[kl].append(r['page'])
    
    for kl in sorted(kl_groups.keys()):
        pages = kl_groups[kl]
        prime_mark = "PRIME" if is_prime(kl) else ""
        print(f"  Key length {kl} {prime_mark}: pages {pages}")

if __name__ == '__main__':
    main()

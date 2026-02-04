"""
Pages 21-30 Systematic Attack
=============================
Page 63 contains wisdom hints and keywords. Let's use these as keys.
Cicada loves self-referential puzzles and keyword reuse.
"""

import os
from collections import Counter
from pathlib import Path

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def to_str(nums):
    return "".join(RUNEGLISH[n % 29] for n in nums)

def calc_ioc(text):
    """Calculate Index of Coincidence"""
    if len(text) < 2:
        return 0
    counts = Counter(text)
    n = len(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def string_to_key(s):
    """Convert string to key indices using Gematria"""
    gematria_map = {runeglish: i for i, runeglish in enumerate(RUNEGLISH)}
    key = []
    i = 0
    s = s.upper()
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in gematria_map:
            key.append(gematria_map[s[i:i+2]])
            i += 2
        elif s[i] in gematria_map:
            key.append(gematria_map[s[i]])
            i += 1
        else:
            i += 1
    return key

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Keywords from Page 63 wisdom grid
PAGE63_KEYWORDS = [
    'VOID',
    'AETHEREAL',
    'CARNAL',
    'ANALOG',
    'MOURNFUL',
    'SHADOWS',
    'BUFFERS',
    'MOBIUS',
    'OBSCURA',
    'SUOID',  # mysterious term
    'CABAL',
    'FORM',
    # Also common cipher keywords
    'DIVINITY',  # used in multiple pages
    'CONSUMPTION',  # Page 68
    'DEOR',  # from Page 20 hint
    'PRIMES',
    'TOTIENT',
    'SACRED',
    'ENCRYPT',
    'ENCRYPTION',
    'WISDOM',
]

# Load runes from pages 21-30
print("[*] Loading runes from pages 21-30...")
page_runes = {}
page_counts = {}

for page_num in range(21, 31):
    rune_path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if Path(rune_path).exists():
        try:
            runes = load_runes(rune_path)
            page_runes[page_num] = runes
            page_counts[page_num] = len(runes)
            print(f"    Page {page_num}: {len(runes)} runes")
        except Exception as e:
            print(f"    Page {page_num}: ERROR - {e}")
    else:
        print(f"    Page {page_num}: File not found")

print(f"\n[*] Loaded {len(page_runes)} pages")

# Attack each page with each keyword
print("\n" + "="*80)
print("ATTACKING PAGES 21-30 WITH PAGE 63 KEYWORDS")
print("="*80)

results = {}

for page_num, runes in sorted(page_runes.items()):
    print(f"\n{'='*80}")
    print(f"PAGE {page_num} ({len(runes)} runes)")
    print(f"{'='*80}")
    
    best_results = []
    
    for keyword in PAGE63_KEYWORDS:
        key = string_to_key(keyword)
        if not key or len(key) == 0:
            continue
        
        # Try multiple modes
        for mode_name, mode_func in [
            ('SUB', lambda c, k: (c - k) % 29),
            ('ADD', lambda c, k: (c + k) % 29),
            ('BEAUFORT', lambda c, k: (k - c) % 29),
            ('SUB_REV', lambda c, k: (c - k) % 29),  # Reverse key
        ]:
            # Apply cipher
            decrypted = []
            key_cycle = 0
            for cipher_val in runes:
                key_val = key[key_cycle % len(key)]
                if mode_name == 'SUB_REV':
                    plain_val = (cipher_val - key_val) % 29
                else:
                    plain_val = mode_func(cipher_val, key_val)
                decrypted.append(plain_val)
                key_cycle += 1
            
            decrypted_text = to_str(decrypted)
            ioc = calc_ioc(decrypted_text)
            
            # Look for common words
            common_words = ['THE', 'AND', 'BUT', 'FOR', 'ARE', 'NOT', 'YOU', 'ALL', 'ONE', 'HER',
                           'THAT', 'THIS', 'WITH', 'HAVE', 'THEY', 'BEEN', 'BEEN', 'KNOW']
            found_words = [w for w in common_words if w in decrypted_text]
            
            # Store if promising
            if ioc > 1.5 or len(found_words) >= 2:
                score = ioc + len(found_words) * 0.2
                best_results.append({
                    'keyword': keyword,
                    'mode': mode_name,
                    'ioc': ioc,
                    'words': found_words,
                    'score': score,
                    'text': decrypted_text[:100]
                })
    
    # Sort by score
    best_results.sort(key=lambda x: -x['score'])
    
    # Show top 5 results
    if best_results:
        print(f"\n[+] Top 5 Results:")
        for i, result in enumerate(best_results[:5], 1):
            print(f"\n{i}. Keyword: {result['keyword']:15} Mode: {result['mode']:8}")
            print(f"   IoC: {result['ioc']:.4f}, Words: {result['words']}")
            print(f"   Preview: {result['text']}")
        
        # Save the top result
        top = best_results[0]
        results[page_num] = top
        
        # Mark if text is readable
        if top['ioc'] > 1.7 or len(top['words']) >= 5:
            print(f"\n[!!!] POSSIBLY READABLE - Check this one!")
    else:
        print("\n[-] No promising results")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

readable_pages = []
for page_num, result in sorted(results.items()):
    if result['ioc'] > 1.65 or len(result['words']) >= 4:
        readable_pages.append((page_num, result))
        print(f"Page {page_num}: {result['keyword']:15} ({result['mode']:8}) IoC={result['ioc']:.4f}")

if readable_pages:
    print(f"\n[+] Found {len(readable_pages)} pages with promising results!")
else:
    print("\n[-] No highly promising results yet")

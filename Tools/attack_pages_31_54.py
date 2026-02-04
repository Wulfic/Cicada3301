"""
Pages 31-54 Systematic Attack
Test all known keywords from Page 63 and solved pages
"""

import os
import sys

# Gematria Primus mappings
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21,
    'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_INDEX_TO_LATIN = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N',
    'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
    'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

GP_LATIN_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5,
    'G': 6, 'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11,
    'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17,
    'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23,
    'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}

# Keywords from Page 63 and solved pages
KEYWORDS = [
    # Page 63 grid keywords
    'VOID', 'AETHEREAL', 'CARNAL', 'ANALOG', 'MOURNFUL', 'SHADOWS',
    'BUFFERS', 'MOBIUS', 'OBSCURA', 'CABAL', 'FORM',
    # Known successful keywords
    'DIVINITY', 'DEOR', 'PRIMES', 'TOTIENT', 'SACRED', 'ENCRYPTION', 
    'ENCRYPT', 'CONSUMPTION', 'WISDOM', 'TRUTH', 'FAITH', 'PATH',
    'SEEK', 'FIND', 'KNOW', 'SPIRIT', 'SOUL', 'LIGHT', 'DEATH',
    # From solved pages
    'CIRCUMFERENCE', 'KOAN', 'CICADA', 'FIRFUMFERENFE', 'WARNING',
    'BELIEVE', 'NOTHING', 'INSTRUCTION', 'UNREASONABLE', 'WEALTH',
    'PARABLE', 'INSTAR', 'JOURNEY', 'PILGRIM', 'EPILOGUE'
]

def load_runes(page_num):
    """Load runes from page file"""
    page_dir = f"LiberPrimus/pages/page_{page_num:02d}"
    rune_file = os.path.join(page_dir, "runes.txt")
    
    if not os.path.exists(rune_file):
        return None
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    # Extract only runes
    runes = []
    for char in text:
        if char in GP_RUNE_TO_INDEX:
            runes.append(char)
    
    return runes

def runes_to_indices(runes):
    """Convert runes to indices"""
    return [GP_RUNE_TO_INDEX[r] for r in runes]

def word_to_indices(word):
    """Convert a word to cipher indices"""
    indices = []
    i = 0
    word = word.upper()
    
    while i < len(word):
        # Try two-letter combos first
        if i < len(word) - 1:
            two_char = word[i:i+2]
            if two_char in GP_LATIN_TO_INDEX:
                indices.append(GP_LATIN_TO_INDEX[two_char])
                i += 2
                continue
        
        # Single character
        one_char = word[i]
        if one_char in GP_LATIN_TO_INDEX:
            indices.append(GP_LATIN_TO_INDEX[one_char])
        i += 1
    
    return indices

def vigenere_decrypt(cipher, key, mode='SUB'):
    """Vigenere decrypt with SUB, ADD, or Beaufort"""
    result = []
    key_idx = 0
    
    for c in cipher:
        if mode == 'SUB':
            # Standard Vigenere: P = (C - K) mod 29
            p = (c - key[key_idx % len(key)]) % 29
        elif mode == 'ADD':
            # Reverse Vigenere: P = (C + K) mod 29
            p = (c + key[key_idx % len(key)]) % 29
        elif mode == 'BEAUFORT':
            # Beaufort: P = (K - C) mod 29
            p = (key[key_idx % len(key)] - c) % 29
        
        result.append(p)
        key_idx += 1
    
    return result

def indices_to_text(indices):
    """Convert indices to readable text"""
    return ''.join(GP_INDEX_TO_LATIN[i] for i in indices)

def calculate_ioc(indices):
    """Calculate Index of Coincidence"""
    freq = [0] * 29
    for idx in indices:
        freq[idx] += 1
    
    n = len(indices)
    if n <= 1:
        return 0
    
    ioc = sum(f * (f - 1) for f in freq) / (n * (n - 1))
    return ioc * 29

def score_english(text):
    """Score text for English-like properties"""
    text = text.upper()
    
    # Common words
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE',
        'FROM', 'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN',
        'THAN', 'MORE', 'WHEN', 'WHICH', 'TIME', 'INTO', 'SOME', 'COULD'
    ]
    
    score = sum(text.count(word) for word in common_words)
    
    # Common bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
    score += sum(text.count(bg) * 0.5 for bg in bigrams)
    
    return score

def main():
    print("=" * 80)
    print("PAGES 31-54 SYSTEMATIC KEYWORD ATTACK")
    print("=" * 80)
    print()
    
    results = []
    
    for page_num in range(31, 55):
        print(f"Testing Page {page_num}...")
        
        runes = load_runes(page_num)
        if not runes:
            print(f"  ⚠️  Could not load Page {page_num}")
            continue
        
        cipher = runes_to_indices(runes)
        
        if len(cipher) < 50:
            print(f"  ⚠️  Page {page_num} too short ({len(cipher)} runes)")
            continue
        
        page_results = []
        
        for keyword in KEYWORDS:
            key = word_to_indices(keyword)
            if not key:
                continue
            
            for mode in ['SUB', 'ADD', 'BEAUFORT']:
                plaintext = vigenere_decrypt(cipher, key, mode)
                ioc = calculate_ioc(plaintext)
                
                # Only record high IoC results
                if ioc > 1.65:
                    text = indices_to_text(plaintext)
                    eng_score = score_english(text)
                    
                    page_results.append({
                        'page': page_num,
                        'keyword': keyword,
                        'mode': mode,
                        'ioc': ioc,
                        'score': eng_score,
                        'text': text
                    })
        
        if page_results:
            # Sort by IoC
            page_results.sort(key=lambda x: x['ioc'], reverse=True)
            best = page_results[0]
            
            print(f"  ✅ Page {page_num}: {best['keyword']} ({best['mode']}) → IoC {best['ioc']:.4f}, Score {best['score']:.1f}")
            print(f"     Preview: {best['text'][:80]}")
            
            results.extend(page_results)
        else:
            print(f"  ❌ Page {page_num}: No high IoC results")
    
    print()
    print("=" * 80)
    print("SUMMARY OF HIGH-IOC RESULTS")
    print("=" * 80)
    print()
    
    # Sort all results by IoC
    results.sort(key=lambda x: x['ioc'], reverse=True)
    
    print(f"{'Page':<6} {'Keyword':<15} {'Mode':<10} {'IoC':<8} {'Score':<7} Preview")
    print("-" * 80)
    
    for r in results[:50]:  # Top 50
        preview = r['text'][:50].replace('\n', ' ')
        print(f"{r['page']:<6} {r['keyword']:<15} {r['mode']:<10} {r['ioc']:<8.4f} {r['score']:<7.1f} {preview}")
    
    # Save full results
    print()
    print("Saving detailed results...")
    
    with open("pages_31_54_attack_results.txt", 'w', encoding='utf-8') as f:
        f.write("PAGES 31-54 SYSTEMATIC KEYWORD ATTACK\n")
        f.write("=" * 80 + "\n\n")
        
        for r in results:
            f.write(f"Page {r['page']}: {r['keyword']} ({r['mode']})\n")
            f.write(f"IoC: {r['ioc']:.4f}, English Score: {r['score']:.1f}\n")
            f.write("=" * 80 + "\n")
            f.write(r['text'][:500])
            f.write("\n\n" + "=" * 80 + "\n\n")
    
    print("✅ Saved: pages_31_54_attack_results.txt")
    
    # Group by page
    by_page = {}
    for r in results:
        if r['page'] not in by_page:
            by_page[r['page']] = []
        by_page[r['page']].append(r)
    
    print()
    print("Pages with HIGH IoC results:")
    for page_num in sorted(by_page.keys()):
        best = max(by_page[page_num], key=lambda x: x['ioc'])
        print(f"  Page {page_num}: {best['keyword']} ({best['mode']}) → IoC {best['ioc']:.4f}")

if __name__ == "__main__":
    main()

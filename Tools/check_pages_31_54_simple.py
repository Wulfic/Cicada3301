"""
Check Pages 31-54 for Simple Ciphers
- Test if any are already plaintext
- Test Caesar shifts
- Test φ(prime) cipher like Pages 55-74
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

def generate_primes(n):
    """Generate first n primes"""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

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
            runes.append(GP_RUNE_TO_INDEX[char])
    
    return runes

def caesar_decrypt(cipher, shift):
    """Caesar shift decryption"""
    return [(c - shift) % 29 for c in cipher]

def totient_decrypt(cipher):
    """φ(prime) decryption like Pages 55-74"""
    primes = generate_primes(len(cipher) + 100)
    result = []
    key_idx = 0
    
    for i, c in enumerate(cipher):
        # Check for literal F (cipher[i] == 0)
        if c == 0:
            result.append(0)
            # Don't increment key for literal F
        else:
            phi = primes[key_idx] - 1  # φ(prime) = prime - 1
            p = (c - phi) % 29
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
    
    # Common words (expand list)
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE',
        'FROM', 'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN',
        'WARNING', 'WISDOM', 'TRUTH', 'SACRED', 'PRIMES', 'KOAN', 'PATH'
    ]
    
    score = sum(text.count(word) * 2 for word in common_words)
    
    # Common bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'EA']
    score += sum(text.count(bg) for bg in bigrams)
    
    return score

def main():
    print("=" * 80)
    print("PAGES 31-54 SIMPLE CIPHER CHECK")
    print("=" * 80)
    print()
    
    all_results = []
    
    for page_num in range(31, 55):
        cipher = load_runes(page_num)
        if not cipher:
            print(f"Page {page_num}: Could not load")
            continue
        
        if len(cipher) < 50:
            print(f"Page {page_num}: Too short ({len(cipher)} runes)")
            continue
        
        page_results = []
        
        # Test no shift (plaintext)
        plaintext = indices_to_text(cipher)
        ioc = calculate_ioc(cipher)
        score = score_english(plaintext)
        page_results.append(('PLAINTEXT', ioc, score, plaintext))
        
        # Test Caesar shifts
        for shift in range(1, 29):
            decrypted = caesar_decrypt(cipher, shift)
            text = indices_to_text(decrypted)
            ioc = calculate_ioc(decrypted)
            score = score_english(text)
            
            if ioc > 1.5 or score > 10:
                page_results.append((f'CAESAR_{shift}', ioc, score, text))
        
        # Test φ(prime) cipher
        decrypted = totient_decrypt(cipher)
        text = indices_to_text(decrypted)
        ioc = calculate_ioc(decrypted)
        score = score_english(text)
        
        if ioc > 1.5 or score > 10:
            page_results.append(('PHI_PRIME', ioc, score, text))
        
        # Find best result
        if page_results:
            best = max(page_results, key=lambda x: x[2])  # Sort by score
            
            if best[2] > 5 or best[1] > 1.5:
                print(f"Page {page_num}: {best[0]:<15} IoC {best[1]:.4f}, Score {best[2]:>5.1f}")
                print(f"  Preview: {best[3][:80]}")
                print()
                
                all_results.append({
                    'page': page_num,
                    'method': best[0],
                    'ioc': best[1],
                    'score': best[2],
                    'text': best[3]
                })
            else:
                print(f"Page {page_num}: No readable results (best score: {best[2]:.1f})")
    
    print()
    print("=" * 80)
    print("SUMMARY - HIGH SCORING RESULTS")
    print("=" * 80)
    
    if all_results:
        all_results.sort(key=lambda x: x['score'], reverse=True)
        
        for r in all_results:
            print(f"Page {r['page']}: {r['method']} → IoC {r['ioc']:.4f}, Score {r['score']:.1f}")
            print(f"  {r['text'][:100]}")
            print()
        
        # Save detailed results
        with open("pages_31_54_simple_results.txt", 'w', encoding='utf-8') as f:
            f.write("PAGES 31-54 SIMPLE CIPHER RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            for r in all_results:
                f.write(f"PAGE {r['page']} - {r['method']}\n")
                f.write(f"IoC: {r['ioc']:.4f}, Score: {r['score']:.1f}\n")
                f.write("=" * 80 + "\n")
                f.write(r['text'])
                f.write("\n\n" + "=" * 80 + "\n\n")
        
        print("✅ Saved: pages_31_54_simple_results.txt")
    else:
        print("❌ No pages showed high scores with simple ciphers")
        print()
        print("This suggests Pages 31-54 use:")
        print("  - Running key cipher (previous page as key)")
        print("  - Autokey cipher")
        print("  - Transposition + substitution")
        print("  - Complex multi-stage encryption")

if __name__ == "__main__":
    main()

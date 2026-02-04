"""
Multi-Pass Cipher Test - Page 21
Test if scrambled text needs SECOND Vigenère pass
"""

import os

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

KEYWORDS = [
    'DIVINITY', 'PRIMES', 'WISDOM', 'TOTIENT', 'SACRED', 'TRUTH',
    'DEOR', 'VOID', 'AETHEREAL', 'CARNAL', 'ANALOG', 'SHADOWS',
    'OBSCURA', 'CABAL', 'ENCRYPTION', 'CONSUMPTION', 'WARNING',
    'PILGRIM', 'JOURNEY', 'PATH', 'CIRCUMFERENCE', 'KOAN'
]

def load_page_21():
    """Load and do first-pass decryption of Page 21"""
    rune_file = "LiberPrimus/pages/page_21/runes.txt"
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    # Extract runes
    runes = []
    for char in text:
        if char in GP_RUNE_TO_INDEX:
            runes.append(GP_RUNE_TO_INDEX[char])
    
    return runes

def word_to_indices(word):
    """Convert word to indices"""
    indices = []
    i = 0
    word = word.upper()
    
    while i < len(word):
        if i < len(word) - 1:
            two_char = word[i:i+2]
            if two_char in GP_LATIN_TO_INDEX:
                indices.append(GP_LATIN_TO_INDEX[two_char])
                i += 2
                continue
        
        one_char = word[i]
        if one_char in GP_LATIN_TO_INDEX:
            indices.append(GP_LATIN_TO_INDEX[one_char])
        i += 1
    
    return indices

def vigenere_decrypt(cipher, key, mode='SUB'):
    """Vigenere decrypt"""
    result = []
    key_idx = 0
    
    for c in cipher:
        if mode == 'SUB':
            p = (c - key[key_idx % len(key)]) % 29
        elif mode == 'ADD':
            p = (c + key[key_idx % len(key)]) % 29
        elif mode == 'BEAUFORT':
            p = (key[key_idx % len(key)] - c) % 29
        
        result.append(p)
        key_idx += 1
    
    return result

def indices_to_text(indices):
    """Convert indices to text"""
    return ''.join(GP_INDEX_TO_LATIN[i] for i in indices)

def calculate_ioc(indices):
    """Calculate IoC"""
    freq = [0] * 29
    for idx in indices:
        freq[idx] += 1
    
    n = len(indices)
    if n <= 1:
        return 0
    
    ioc = sum(f * (f - 1) for f in freq) / (n * (n - 1))
    return ioc * 29

def score_english(text):
    """Score English readability"""
    text = text.upper()
    
    common_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE',
        'KNOW', 'TRUTH', 'WISDOM', 'PATH', 'PRIMES', 'SACRED', 'WILL',
        'SEEK', 'FIND', 'WAY', 'END', 'BEGIN', 'JOURNEY'
    ]
    
    score = sum(text.count(word) * 3 for word in common_words)
    
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND']
    score += sum(text.count(bg) for bg in bigrams)
    
    return score

def main():
    print("=" * 80)
    print("MULTI-PASS CIPHER TEST - PAGE 21")
    print("=" * 80)
    print()
    
    # Load Page 21
    cipher = load_page_21()
    print(f"Page 21: {len(cipher)} runes")
    print()
    
    # First pass: CABAL/Beaufort (known to give IoC 1.9728)
    print("FIRST PASS: CABAL/Beaufort")
    key1 = word_to_indices('CABAL')
    first_pass = vigenere_decrypt(cipher, key1, 'BEAUFORT')
    text1 = indices_to_text(first_pass)
    ioc1 = calculate_ioc(first_pass)
    score1 = score_english(text1)
    
    print(f"IoC: {ioc1:.4f}, Score: {score1:.1f}")
    print(f"Preview: {text1[:100]}")
    print()
    
    # Second pass: Try all keywords
    print("SECOND PASS: Testing all keywords...")
    print("=" * 80)
    print()
    
    results = []
    
    for keyword in KEYWORDS:
        key2 = word_to_indices(keyword)
        if not key2:
            continue
        
        for mode in ['SUB', 'ADD', 'BEAUFORT']:
            second_pass = vigenere_decrypt(first_pass, key2, mode)
            text2 = indices_to_text(second_pass)
            ioc2 = calculate_ioc(second_pass)
            score2 = score_english(text2)
            
            # Only report if improvement
            if score2 > score1 + 20 or ioc2 > ioc1 + 0.2:
                results.append({
                    'keyword': keyword,
                    'mode': mode,
                    'ioc': ioc2,
                    'score': score2,
                    'text': text2
                })
    
    if results:
        results.sort(key=lambda x: x['score'], reverse=True)
        
        print("IMPROVEMENTS FOUND:\n")
        for i, r in enumerate(results[:10], 1):
            print(f"{i}. {r['keyword']} ({r['mode']})")
            print(f"   IoC: {r['ioc']:.4f}, Score: {r['score']:.1f}")
            print(f"   {r['text'][:100]}")
            print()
        
        # Save best
        best = results[0]
        with open("page_21_multipass_best.txt", 'w', encoding='utf-8') as f:
            f.write(f"PAGE 21 - MULTI-PASS CIPHER\n")
            f.write(f"Pass 1: CABAL/Beaufort → IoC {ioc1:.4f}\n")
            f.write(f"Pass 2: {best['keyword']}/{best['mode']} → IoC {best['ioc']:.4f}, Score {best['score']:.1f}\n")
            f.write("=" * 80 + "\n\n")
            f.write(best['text'])
        
        print(f"✅ Saved: page_21_multipass_best.txt")
    else:
        print("❌ No improvements found with second pass")
        print()
        print("This suggests multi-pass cipher is NOT the solution.")
        print("Try other hypotheses:")
        print("  - Word-level anagram")
        print("  - Running key from Page 20")
        print("  - Page-dependent transformations")

if __name__ == "__main__":
    main()

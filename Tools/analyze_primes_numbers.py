"""
PRIMES NUMBERS Anagram Analysis
================================
The P19 hint says "PRIMES NUMBERS" instead of "PRIME NUMBERS".
This grammatical oddity may be intentional. Analyze possible anagrams.
"""

from itertools import permutations
from collections import Counter

def get_anagrams(text, min_word_len=3):
    """Find dictionary words that can be made from letters."""
    letters = Counter(text.upper().replace(' ', ''))
    
    # Common English words to check
    common_words = [
        'PRIMES', 'NUMBERS', 'PRIME', 'NUMBER', 'SUM', 'SUMS', 'RUN', 'RUNS',
        'BURN', 'BURNS', 'PRISM', 'PRISMS', 'UMBER', 'RUMBS', 'RUBS', 'NUBS',
        'PINES', 'SPINE', 'MINES', 'MINER', 'MINERS', 'BRINE', 'BRINES',
        'SIMPER', 'SIMPLE', 'NIMBUS', 'NIMBLE', 'SERMON', 'SERUMS', 'SERUM',
        'SUPER', 'SUPERS', 'RUNE', 'RUNES', 'MUSE', 'MUSES', 'PERM', 'PERMS',
        'NURSE', 'NURSES', 'PURSE', 'PURSES', 'SIREN', 'SIRENS', 'RISEN',
        'RESIN', 'RESINS', 'RINSE', 'INSURE', 'SNIPER', 'SNIPERS', 'MISER',
        # Cicada-related
        'CIPHER', 'HIDDEN', 'SECRET', 'PATH', 'PATHS', 'SPIRAL', 'PRIME',
        'DEOR', 'RUNE', 'RUNIC', 'GEMATRIA', 'PILGRIM', 'INSTAR',
        # Two-word combos
        'PERMISSIBLE', 'IMPRESSION', 'SUBMISSION', 'PERMISSION',
        # Latin/archaic
        'NIMBUS', 'PRIMUS', 'REBUS',
    ]
    
    # More specific patterns
    words_found = []
    
    for word in common_words:
        word_letters = Counter(word)
        if all(word_letters[c] <= letters[c] for c in word_letters):
            words_found.append(word)
    
    return words_found

def analyze_primesnumbers():
    """Analyze 'PRIMES NUMBERS' for hidden meaning."""
    print("="*60)
    print("PRIMES NUMBERS ANAGRAM ANALYSIS")
    print("="*60)
    
    text = "PRIMESNUMBERS"
    print(f"\nOriginal: PRIMES NUMBERS")
    print(f"Letters: {text} ({len(text)} chars)")
    print(f"Letter counts: {dict(Counter(text))}")
    
    # Check for simple anagrams
    print("\n--- Dictionary Words Possible ---")
    words = get_anagrams(text)
    print(f"Words found: {sorted(set(words))}")
    
    # Check for two-word combinations that use all letters
    print("\n--- Two-Word Combinations (all 13 letters) ---")
    
    # Some interesting potential combinations:
    combos = [
        ("PRIMES", "BURN"),
        ("NUMBERS", "IP"),
        ("NIMBUS", "PERMS"),
        ("PRIME", "BURNS"),
        ("PRISM", "BURN"),
        ("RUNE", "PRISM"),
        ("SUPER", "RIM"),
        ("SUM", "PRISM"),
        ("SNIPER", "BUM"),
        ("PRUNE", "SIMB"),
        ("UMBER", "SPIN"),
        ("RIMBUS", "PEN"),
    ]
    
    for w1, w2 in combos:
        combined = w1 + w2
        if sorted(combined) == sorted(text):
            print(f"  ✓ {w1} + {w2} = uses all letters!")
        else:
            remaining = list(text)
            for c in w1 + w2:
                if c in remaining:
                    remaining.remove(c)
            if remaining:
                print(f"  {w1} + {w2} -- remaining: {''.join(remaining)}")
    
    # Check if it's an intentional grammatical error pointing to something
    print("\n--- Grammatical Analysis ---")
    print("'PRIMES NUMBERS' vs 'PRIME NUMBERS'")
    print("Extra S in PRIMES could mean:")
    print("  - PRIME'S NUMBERS (possessive)")
    print("  - Multiple primes")
    print("  - S = 15 in Gematria (index of S rune)")
    print("  - S is the 15th letter of alphabet (1-indexed)")
    
    # Gematria analysis
    print("\n--- Gematria Analysis ---")
    
    GEMATRIA = {
        'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
        'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23,
        'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }
    
    GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                       53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    # Convert "PRIMES NUMBERS" to Gematria indices
    phrase = "PRIMESNUMBERS"
    indices = []
    for c in phrase:
        if c in GEMATRIA:
            indices.append(GEMATRIA[c])
    
    print(f"Gematria indices: {indices}")
    print(f"Sum of indices: {sum(indices)}")
    
    # Sum of corresponding Gematria primes
    prime_values = [GEMATRIA_PRIMES[i] for i in indices]
    print(f"Gematria prime values: {prime_values}")
    print(f"Sum of primes: {sum(prime_values)}")
    
    # Check modular properties
    print(f"Sum of indices mod 29: {sum(indices) % 29}")
    print(f"Sum of primes mod 29: {sum(prime_values) % 29}")
    
    # Could the indices themselves be a key?
    print(f"\nAs key: {indices}")
    print(f"Key length: {len(indices)}")
    
    # 812 / 13 = 62.46... not exact
    # But 812 mod 13 = 6
    print(f"812 mod {len(indices)}: {812 % len(indices)}")
    
    # What if we rearrange the letters to find a meaningful phrase?
    print("\n--- Possible Meaningful Rearrangements ---")
    
    # Manual analysis of interesting rearrangements
    rearrangements = [
        "PRIME SUM BERNS",
        "RUNE PRISM BS",
        "BURN PRIMES",
        "PRISM BURN ES",
        "SNIPER BRUMS",
        "RUB SPINE MRS",
        "SUM BRINE PRS",
        "SPIN UMBER RS",
        "NIMBUS REPS",
        "PRUNE SIMBS",
    ]
    
    for r in rearrangements:
        clean = r.replace(' ', '')
        if sorted(clean) == sorted(text):
            print(f"  ✓ {r}")
        else:
            print(f"  ? {r}")

def check_as_key():
    """Check if PRIMESNUMBERS or variants work as a key for Page 20."""
    print("\n" + "="*60)
    print("TESTING AS DECRYPTION KEY")
    print("="*60)
    
    import collections
    
    RUNE_TO_IDX = {
        'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
        'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
        'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
        'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
    }
    
    IDX_TO_LATIN = {
        0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
        8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
        16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
        24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
    }
    
    ENGLISH_TO_IDX = {
        'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
        'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
        'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
        'Y': 26, 'Z': 15
    }
    
    def load_runes():
        with open(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt", 'r', encoding='utf-8') as f:
            content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
        return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]
    
    def calculate_ioc(indices):
        if len(indices) < 2: return 0
        counts = collections.Counter(indices)
        numerator = sum(n * (n - 1) for n in counts.values())
        denominator = len(indices) * (len(indices) - 1)
        return numerator / denominator * 29.0
    
    def runes_to_latin(indices):
        return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)
    
    runes = load_runes()
    
    # Keys to try
    keys = [
        "PRIMESNUMBERS",
        "NUMBERSPRIME",
        "PRIMESBURNS",
        "SNUMBERPRIMES",
        "PRIMESS",  # Just the extra S
    ]
    
    for key_str in keys:
        key = [ENGLISH_TO_IDX.get(c, 0) for c in key_str]
        
        # Try subtract mode
        result = [(runes[i] - key[i % len(key)]) % 29 for i in range(len(runes))]
        ioc = calculate_ioc(result)
        print(f"\nKey: {key_str}")
        print(f"  C - key: IoC={ioc:.4f}")
        if ioc > 1.1:
            print(f"  Text: {runes_to_latin(result[:80])}")
        
        # Try add mode
        result = [(runes[i] + key[i % len(key)]) % 29 for i in range(len(runes))]
        ioc = calculate_ioc(result)
        print(f"  C + key: IoC={ioc:.4f}")
        if ioc > 1.1:
            print(f"  Text: {runes_to_latin(result[:80])}")

if __name__ == "__main__":
    analyze_primesnumbers()
    check_as_key()

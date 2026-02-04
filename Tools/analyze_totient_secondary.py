"""
Test combining Totient cipher with additional decryption layers.
Pages 21-30 show very high IoC after Totient shift, but output is still gibberish.
Need to find the secondary cipher layer.
"""

import os
from collections import Counter

# Gematria Primus
GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
             31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
             73, 79, 83, 89, 97, 101, 103, 107, 109]

def rune_to_index(rune):
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

def totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def load_page(page_num):
    page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    subdir = f"page_{page_num:02d}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            runes = [c for c in content if c in GP_RUNES]
            return runes
    return []

def apply_totient_cipher(runes, operation='sub'):
    result = []
    for rune in runes:
        idx = rune_to_index(rune)
        if idx is not None:
            prime_val = GP_PRIMES[idx]
            phi = totient(prime_val)
            shift = phi % 29
            if operation == 'sub':
                new_idx = (idx - shift) % 29
            else:
                new_idx = (idx + shift) % 29
            result.append(new_idx)
    return result

def apply_vigenere_sub(indices, key_indices):
    """Apply Vigenère subtraction with a running key"""
    result = []
    key_len = len(key_indices)
    for i, idx in enumerate(indices):
        key_shift = key_indices[i % key_len]
        new_idx = (idx - key_shift) % 29
        result.append(new_idx)
    return result

def apply_autokey(indices):
    """Autokey cipher - each decrypted letter becomes the next key"""
    result = []
    # First letter has no key, use it as-is or try to guess
    for start_guess in range(29):
        result = [start_guess]
        for i in range(1, len(indices)):
            # P[i] = C[i] - P[i-1] mod 29
            p_prev = result[-1]
            p_curr = (indices[i] - p_prev) % 29
            result.append(p_curr)
        # Check IoC
        ioc = calculate_ioc(result)
        if ioc > 1.5:
            yield result, ioc, start_guess

def apply_beaufort(indices, key_indices):
    """Beaufort cipher: P = K - C mod 29"""
    result = []
    key_len = len(key_indices)
    for i, idx in enumerate(indices):
        key_shift = key_indices[i % key_len]
        new_idx = (key_shift - idx) % 29
        result.append(new_idx)
    return result

def indices_to_latin(indices):
    return ''.join(index_to_latin(i) for i in indices)

def calculate_ioc(indices):
    n = len(indices)
    if n <= 1:
        return 0
    counts = Counter(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29

def find_english_words(text, min_len=3):
    english_words = [
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS',
        'HOW', 'ITS', 'LET', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO',
        'BOY', 'DID', 'SAY', 'SHE', 'TOO', 'USE', 'ODE', 'MET', 'BID', 'ALT',
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
        'CALL', 'DEAD', 'EACH', 'FIND', 'GIVE', 'GOOD', 'JUST', 'KNOW', 'LIKE',
        'LONG', 'MADE', 'MAKE', 'MORE', 'MUST', 'NAME', 'ONLY', 'OVER', 'PATH',
        'SELF', 'SUCH', 'TAKE', 'THAN', 'THEM', 'THEN', 'TRUE', 'UNTO', 'UPON',
        'VERY', 'WANT', 'WELL', 'WERE', 'WHEN', 'WORD', 'WORK', 'YEAR', 'ALSO',
        'BEING', 'LIGHT', 'TRUTH', 'WITHIN', 'DIVINE', 'SACRED', 'SECRET',
        'THERE', 'THEIR', 'WHICH', 'WOULD', 'OTHER', 'THESE', 'FIRST', 'COULD',
        'AFTER', 'WHERE', 'THOSE', 'GREAT', 'THROUGH', 'BETWEEN',
        'LONE', 'EODE', 'SEFA', 'REAPER', 'AEON', 'PRIME', 'PILGRIM', 'ADEPT',
        'WISDOM', 'KNOWLEDGE', 'UNDERSTAND', 'PRIMES', 'TOTIENT', 'SEEK', 'FIND',
    ]
    english_words = sorted(set(english_words), key=len, reverse=True)
    found = []
    text_upper = text.upper()
    for word in english_words:
        if len(word) >= min_len:
            pos = 0
            while True:
                pos = text_upper.find(word, pos)
                if pos == -1:
                    break
                found.append((word, pos))
                pos += 1
    found_sorted = sorted(found, key=lambda x: (-len(x[0]), x[1]))
    result = []
    covered = set()
    for word, pos in found_sorted:
        word_range = set(range(pos, pos + len(word)))
        if not word_range & covered:
            result.append((word, pos))
            covered |= word_range
    return sorted(result, key=lambda x: x[1])

def try_interleave(indices):
    """Like P20's interleave operation"""
    n = len(indices)
    if n % 2 != 0:
        # Pad or truncate
        n = n - 1
    half = n // 2
    first_half = indices[:half]
    second_half = indices[half:2*half]
    interleaved = []
    for i in range(half):
        interleaved.append(first_half[i])
        interleaved.append(second_half[i])
    return interleaved

def main():
    print("="*60)
    print("TOTIENT + SECONDARY CIPHER ANALYSIS")
    print("="*60)
    
    # Best pages by IoC after totient:
    # Page 21 ADD: 2.0218
    # Page 22 SUB: 2.0215
    # Page 24 ADD: 1.9076
    # Page 26 SUB: 1.9015
    
    best_pages = [
        (21, 'add'),
        (22, 'sub'),
        (24, 'add'),
        (26, 'sub'),
        (23, 'add'),
        (25, 'add'),
    ]
    
    for page_num, op in best_pages:
        print(f"\n{'='*60}")
        print(f"PAGE {page_num} (Totient {op.upper()})")
        print(f"{'='*60}")
        
        runes = load_page(page_num)
        if not runes:
            continue
            
        # Apply totient
        totient_result = apply_totient_cipher(runes, op)
        base_latin = indices_to_latin(totient_result)
        base_ioc = calculate_ioc(totient_result)
        base_words = find_english_words(base_latin)
        
        print(f"Totient {op.upper()} IoC: {base_ioc:.4f}")
        print(f"First 80: {base_latin[:80]}")
        print(f"Words: {base_words[:5]}")
        
        # Try interleave after totient
        print(f"\n--- After Interleave ---")
        interleaved = try_interleave(totient_result)
        int_latin = indices_to_latin(interleaved)
        int_ioc = calculate_ioc(interleaved)
        int_words = find_english_words(int_latin)
        print(f"IoC: {int_ioc:.4f}")
        print(f"First 80: {int_latin[:80]}")
        print(f"Words: {int_words[:5]}")
        
        # Try autokey after totient
        print(f"\n--- Autokey on Totient Result ---")
        best_autokey = None
        best_autokey_ioc = 0
        for result, ioc, start in apply_autokey(totient_result):
            if ioc > best_autokey_ioc:
                best_autokey_ioc = ioc
                best_autokey = result
        if best_autokey and best_autokey_ioc > base_ioc:
            ak_latin = indices_to_latin(best_autokey)
            ak_words = find_english_words(ak_latin)
            print(f"Best Autokey IoC: {best_autokey_ioc:.4f}")
            print(f"First 80: {ak_latin[:80]}")
            print(f"Words: {ak_words[:5]}")
        else:
            print(f"Autokey doesn't improve IoC")
        
        # Try Vigenère with simple keys
        print(f"\n--- Vigenère with simple keys ---")
        for key_name, key in [
            ("DIVINITY", [23, 10, 16, 10, 9, 10, 16, 27]),  # D-I-V-I-N-I-T-Y
            ("PRIMES", [13, 4, 10, 19, 18, 15]),  # P-R-I-M-E-S
            ("TOTIENT", [16, 3, 16, 10, 18, 9, 16]),  # T-O-T-I-E-N-T
            ("SACRED", [15, 24, 5, 4, 18, 23]),  # S-A-C-R-E-D
        ]:
            vig_result = apply_vigenere_sub(totient_result, key)
            vig_latin = indices_to_latin(vig_result)
            vig_ioc = calculate_ioc(vig_result)
            vig_words = find_english_words(vig_latin)
            if vig_words or vig_ioc > base_ioc:
                print(f"  Key '{key_name}': IoC={vig_ioc:.4f}, Words={vig_words[:3]}")

if __name__ == "__main__":
    main()

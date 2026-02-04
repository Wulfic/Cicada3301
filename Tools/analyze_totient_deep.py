"""
Deep analysis of Totient-shifted pages - especially Page 22 with IoC 1.8766!
This confirms P63's hint: "THE TOTIENT FUNCTION IS SACRED"
"""

import os
import re
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
    """Convert rune to index"""
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    """Convert index to latin"""
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

def totient(n):
    """Euler's totient function"""
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
    """Load page runes"""
    page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    # Pages are in subdirectories like page_21/runes.txt
    subdir = f"page_{page_num:02d}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            runes = [c for c in content if c in GP_RUNES]
            return runes, f"page_{page_num:02d}/runes.txt"
    # Try without leading zero
    subdir = f"page_{page_num}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            runes = [c for c in content if c in GP_RUNES]
            return runes, f"page_{page_num}/runes.txt"
    return [], ""

def apply_totient_cipher(runes, operation='sub'):
    """Apply totient cipher: P = (C - φ(GP_PRIME[C])) mod 29 or ADD"""
    result = []
    for rune in runes:
        idx = rune_to_index(rune)
        if idx is not None:
            prime_val = GP_PRIMES[idx]
            phi = totient(prime_val)  # For primes, φ(p) = p - 1
            shift = phi % 29
            if operation == 'sub':
                new_idx = (idx - shift) % 29
            else:  # add
                new_idx = (idx + shift) % 29
            result.append(new_idx)
    return result

def indices_to_latin(indices):
    """Convert indices to latin string"""
    return ''.join(index_to_latin(i) for i in indices)

def calculate_ioc(indices):
    """Calculate Index of Coincidence"""
    n = len(indices)
    if n <= 1:
        return 0
    counts = Counter(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29  # Normalized for 29-letter alphabet

def find_english_words(text, min_len=3):
    """Find English words in text"""
    # Common English words that could appear
    english_words = [
        # 3-letter
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD',
        'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS',
        'HOW', 'ITS', 'LET', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO',
        'BOY', 'DID', 'SAY', 'SHE', 'TOO', 'USE', 'THE', 'ODE', 'MET', 'BID',
        # 4-letter
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
        'CALL', 'DEAD', 'EACH', 'FIND', 'GIVE', 'GOOD', 'JUST', 'KNOW', 'LIKE',
        'LONG', 'MADE', 'MAKE', 'MORE', 'MUST', 'NAME', 'ONLY', 'OVER', 'PATH',
        'SELF', 'SUCH', 'TAKE', 'THAN', 'THEM', 'THEN', 'TRUE', 'UNTO', 'UPON',
        'VERY', 'WANT', 'WELL', 'WERE', 'WHEN', 'WORD', 'WORK', 'YEAR', 'ALSO',
        'BACK', 'COME', 'COULD', 'FIRST', 'GREAT', 'HAND', 'HIGH', 'JUST',
        'KEEP', 'LAST', 'LEFT', 'LIFE', 'LINE', 'LOOK', 'LOVE', 'MIND', 'MOST',
        'NEED', 'NEXT', 'OPEN', 'PART', 'PLACE', 'RIGHT', 'SAME', 'SEEK',
        'SOME', 'SOUL', 'STILL', 'THING', 'THINK', 'THREE', 'TIME', 'TURN',
        'UNDER', 'WHAT', 'WHERE', 'WHICH', 'WHILE', 'WORLD', 'WOULD', 'YEARS',
        'BEING', 'LIGHT', 'TRUTH', 'WITHIN', 'DIVINE', 'SACRED', 'SECRET',
        # 5+ letter
        'THERE', 'THEIR', 'WHICH', 'WOULD', 'OTHER', 'THESE', 'FIRST', 'COULD',
        'AFTER', 'WHERE', 'THOSE', 'BEING', 'GREAT', 'THROUGH', 'BETWEEN',
        'ANOTHER', 'WITHIN', 'WITHOUT', 'BEFORE', 'BECAUSE',
        # Old English / Cicada-related
        'LONE', 'EODE', 'SEFA', 'REAPER', 'AEON', 'PRIME', 'PILGRIM', 'ADEPT',
        'INITIATE', 'WISDOM', 'KNOWLEDGE', 'UNDERSTAND', 'PRIMES', 'TOTIENT',
        'CIPHER', 'HIDDEN', 'REVEAL', 'JOURNEY', 'SEEK', 'FIND', 'TRUTH',
    ]
    
    # Remove duplicates and sort by length
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
    
    # Remove overlapping shorter words
    found_sorted = sorted(found, key=lambda x: (-len(x[0]), x[1]))
    result = []
    covered = set()
    for word, pos in found_sorted:
        word_range = set(range(pos, pos + len(word)))
        if not word_range & covered:
            result.append((word, pos))
            covered |= word_range
    
    return sorted(result, key=lambda x: x[1])

def try_transpositions(indices, text):
    """Try various transpositions on the text"""
    results = []
    n = len(indices)
    
    # 1. Interleaved (like P20)
    if n % 2 == 0:
        half = n // 2
        first_half = indices[:half]
        second_half = indices[half:]
        interleaved = []
        for i in range(half):
            interleaved.append(first_half[i])
            interleaved.append(second_half[i])
        ioc = calculate_ioc(interleaved)
        latin = indices_to_latin(interleaved)
        words = find_english_words(latin)
        results.append(('INTERLEAVED', ioc, latin[:80], words))
    
    # 2. Reverse interleave
    if n % 2 == 0:
        half = n // 2
        first_half = indices[:half]
        second_half = indices[half:][::-1]  # Reverse second half
        interleaved = []
        for i in range(half):
            interleaved.append(first_half[i])
            interleaved.append(second_half[i])
        ioc = calculate_ioc(interleaved)
        latin = indices_to_latin(interleaved)
        words = find_english_words(latin)
        results.append(('INTERLEAVED-REV', ioc, latin[:80], words))
    
    # 3. Column transposition (try various widths)
    for cols in [5, 6, 7, 8, 9, 10, 11, 12]:
        rows = n // cols
        if rows * cols <= n:
            grid = []
            for r in range(rows):
                row_data = indices[r*cols : (r+1)*cols]
                grid.append(row_data)
            # Read by columns
            by_cols = []
            for c in range(cols):
                for r in range(rows):
                    by_cols.append(grid[r][c])
            ioc = calculate_ioc(by_cols)
            latin = indices_to_latin(by_cols)
            words = find_english_words(latin)
            if words:
                results.append((f'COLS-{cols}', ioc, latin[:80], words))
    
    # 4. Spiral reading
    # Skip for now, try simple approaches first
    
    return results

def analyze_page(page_num, verbose=True):
    """Analyze a single page with totient cipher"""
    runes, filename = load_page(page_num)
    if not runes:
        return None
    
    print(f"\n{'='*60}")
    print(f"PAGE {page_num}: {filename}")
    print(f"{'='*60}")
    print(f"Rune count: {len(runes)}")
    
    # Apply totient cipher (SUB)
    result_sub = apply_totient_cipher(runes, 'sub')
    latin_sub = indices_to_latin(result_sub)
    ioc_sub = calculate_ioc(result_sub)
    words_sub = find_english_words(latin_sub)
    
    print(f"\n--- TOTIENT SUB: IoC = {ioc_sub:.4f} ---")
    print(f"First 100 chars: {latin_sub[:100]}")
    print(f"Words found: {words_sub}")
    
    # Apply totient cipher (ADD)
    result_add = apply_totient_cipher(runes, 'add')
    latin_add = indices_to_latin(result_add)
    ioc_add = calculate_ioc(result_add)
    words_add = find_english_words(latin_add)
    
    print(f"\n--- TOTIENT ADD: IoC = {ioc_add:.4f} ---")
    print(f"First 100 chars: {latin_add[:100]}")
    print(f"Words found: {words_add}")
    
    # Try transpositions on the best one
    if ioc_sub > 1.4:
        print(f"\n--- TRANSPOSITIONS ON SUB (IoC {ioc_sub:.4f}) ---")
        trans_results = try_transpositions(result_sub, latin_sub)
        for name, ioc, text, words in trans_results:
            if words:
                print(f"  {name}: IoC={ioc:.4f}, words={words}")
                print(f"    Text: {text}")
    
    if ioc_add > 1.4:
        print(f"\n--- TRANSPOSITIONS ON ADD (IoC {ioc_add:.4f}) ---")
        trans_results = try_transpositions(result_add, latin_add)
        for name, ioc, text, words in trans_results:
            if words:
                print(f"  {name}: IoC={ioc:.4f}, words={words}")
                print(f"    Text: {text}")
    
    return {
        'page': page_num,
        'rune_count': len(runes),
        'ioc_sub': ioc_sub,
        'ioc_add': ioc_add,
        'latin_sub': latin_sub,
        'latin_add': latin_add,
        'words_sub': words_sub,
        'words_add': words_add
    }

def main():
    print("="*60)
    print("DEEP TOTIENT CIPHER ANALYSIS")
    print("P63 says: 'THE TOTIENT FUNCTION IS SACRED'")
    print("="*60)
    
    # Analyze pages 21-30 with elevated IoC
    results = []
    for page_num in range(21, 31):
        result = analyze_page(page_num)
        if result:
            results.append(result)
    
    # Summary sorted by IoC
    print("\n" + "="*60)
    print("SUMMARY - Sorted by IoC (SUB)")
    print("="*60)
    for r in sorted(results, key=lambda x: x['ioc_sub'], reverse=True):
        print(f"Page {r['page']}: IoC_SUB={r['ioc_sub']:.4f}, IoC_ADD={r['ioc_add']:.4f}, "
              f"Runes={r['rune_count']}, Words_SUB={len(r['words_sub'])}, Words_ADD={len(r['words_add'])}")

if __name__ == "__main__":
    main()

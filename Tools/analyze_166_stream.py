"""
Page 20 - Analyze the 166-rune Deor Stream
============================================
The stream "HOEEDOEBDMEATH..." was extracted by:
  (Deor at prime positions) - (P20 at prime positions) = Stream

This contains plaintext fragments: DEATH, THE, RATIO, LENGTH, NTH
It needs transposition decryption.

166 = 2 × 83 (83 is prime)
"""

import collections
import itertools

STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

GP = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
val_map = {r: i for i, r in enumerate(GP)}
inv_map = {i: r for i, r in enumerate(GP)}

def to_ints(text):
    """Convert single chars only (ignore digraphs to maintain 166)"""
    single_gp = {k: v for k, v in val_map.items() if len(k) == 1}
    return [single_gp[c] for c in text if c in single_gp]

def to_str(ints):
    return "".join(inv_map[i] for i in ints)

def calculate_ioc(values):
    counts = collections.Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def get_primes(n):
    return [i for i in range(2, n) if is_prime(i)]

def main():
    print("="*60)
    print("ANALYZING THE 166-RUNE DEOR STREAM")
    print("="*60)
    
    stream_ints = to_ints(STREAM)
    n = len(stream_ints)
    
    print(f"Stream length: {n}")
    print(f"Stream: {STREAM[:80]}...")
    print(f"IoC: {calculate_ioc(stream_ints):.4f}")
    
    # Factorizations
    print(f"\n166 = 2 × 83 (83 is prime)")
    print(f"Also: 166 = 166 × 1")
    
    # Try various transposition widths
    print("\n--- Transposition Analysis ---")
    
    best_results = []
    
    for width in [2, 83, 7, 11, 13, 17, 19, 23]:
        if n % width == 0:
            height = n // width
            print(f"\n{width} × {height} grid:")
            
            # Row-major to column-major
            col_major = []
            for c in range(width):
                for r in range(height):
                    col_major.append(stream_ints[r * width + c])
            
            ioc = calculate_ioc(col_major)
            text = to_str(col_major)
            print(f"  Column-major read: IoC={ioc:.4f}")
            print(f"  Text: {text[:60]}")
            
            # Look for words
            words = []
            for word in ['THE', 'AND', 'DEATH', 'PATH', 'RATIO', 'LENGTH', 'WHO', 'THAT', 'THIS']:
                if word in text:
                    words.append(word)
            if words:
                print(f"  ⚠️ Words found: {words}")
            
            # Reverse columns
            rev_col = []
            for c in range(width-1, -1, -1):
                for r in range(height):
                    rev_col.append(stream_ints[r * width + c])
            text2 = to_str(rev_col)
            print(f"  Reversed columns: {text2[:60]}")
    
    # Try 83 columns, read 2 rows
    print("\n--- 83 × 2 Grid (83 columns, 2 rows) ---")
    width = 83
    height = 2
    
    # Build grid
    grid = []
    for r in range(height):
        row = []
        for c in range(width):
            row.append(stream_ints[r * width + c])
        grid.append(row)
    
    # Column major read
    col_read = []
    for c in range(width):
        for r in range(height):
            col_read.append(grid[r][c])
    
    print(f"Column read: {to_str(col_read)[:60]}")
    
    # Interleave pairs
    interleaved = []
    for c in range(width):
        interleaved.append(grid[0][c])
        interleaved.append(grid[1][c])
    
    print(f"Interleaved: {to_str(interleaved)[:60]}")
    
    # What if we pair-compress (sum pairs mod 29)?
    print("\n--- Pair Compression (sum mod 29) ---")
    compressed = []
    for i in range(0, n, 2):
        if i + 1 < n:
            compressed.append((stream_ints[i] + stream_ints[i+1]) % 29)
    
    print(f"Compressed length: {len(compressed)}")
    print(f"IoC: {calculate_ioc(compressed):.4f}")
    print(f"Text: {to_str(compressed)}")
    
    # Subtract pairs
    print("\n--- Pair Difference ---")
    diff = []
    for i in range(0, n, 2):
        if i + 1 < n:
            diff.append((stream_ints[i] - stream_ints[i+1]) % 29)
    
    print(f"IoC: {calculate_ioc(diff):.4f}")
    print(f"Text: {to_str(diff)}")
    
    # XOR-like (first × inverse of second?)
    print("\n--- Spiral Read ---")
    # Create 2D approximation
    # 166 is not a perfect square, but close to 13×13=169
    # Try 14×12=168 (close)
    
    # Actually, let's try reading at prime positions
    print("\n--- Prime Position Read ---")
    primes = get_primes(n)
    prime_read = [stream_ints[p] for p in primes if p < n]
    print(f"Primes in 0-{n-1}: {len(prime_read)} values")
    print(f"IoC: {calculate_ioc(prime_read):.4f}")
    print(f"Text: {to_str(prime_read)}")
    
    # Try the Page 24 key mentioned earlier
    print("\n--- With Page 24 Key (83 ints) ---")
    key_p24 = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 
               15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 
               11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 
               22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 
               15, 13, 15]
    
    # Apply key with pair sum
    result = []
    for k in range(len(key_p24)):
        idx = k * 2
        if idx + 1 >= n:
            break
        pair_sum = (stream_ints[idx] + stream_ints[idx+1]) % 29
        decrypted = (pair_sum - key_p24[k]) % 29
        result.append(decrypted)
    
    print(f"Pair sum - key: {to_str(result)}")
    print(f"IoC: {calculate_ioc(result):.4f}")
    
    # Word search in all results
    print("\n--- Looking for English words ---")
    for r in [compressed, diff, prime_read, result]:
        text = to_str(r)
        words_found = []
        for w in ['THE', 'AND', 'DEATH', 'PATH', 'WAY', 'RATIO', 'LENGTH', 'PRIME', 'NUMBER', 
                  'DEOR', 'SONG', 'POEM', 'KEY', 'FIND', 'THIS', 'THAT', 'WHO', 'WHAT']:
            if w in text:
                words_found.append(w)
        if words_found:
            print(f"  Found: {words_found} in: {text[:40]}...")

if __name__ == "__main__":
    main()

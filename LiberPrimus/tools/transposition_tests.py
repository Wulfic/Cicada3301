"""
Test transposition ciphers on the rune sequence
Key length is 113 (prime) - could this be used for transposition?
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

def parse_to_runes(text):
    """Convert text to rune list"""
    text = text.upper().replace('/', '').replace(' ', '')
    runes = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in DIGRAPHS:
                runes.append(digraph)
                i += 2
                continue
        if text[i].isalpha():
            runes.append(text[i])
        i += 1
    return runes

def score_text(runes):
    """Score text based on English-like patterns"""
    text = ''.join(runes)
    
    # Good patterns
    score = 0
    good_patterns = ['THE', 'AND', 'ING', 'ETH', 'THAT', 'DOETH', 'GOETH', 'HATH',
                     'THOU', 'THEE', 'THY', 'THERE', 'THING', 'EARTH', 'HEART',
                     'TRUTH', 'WISDOM', 'DIVINE']
    for p in good_patterns:
        score += text.count(p) * len(p) * 5
    
    # Count TH - too many TH is suspicious
    th_count = runes.count('TH')
    if th_count > len(runes) * 0.15:  # More than 15% TH is bad
        score -= (th_count - len(runes) * 0.15) * 10
    
    return score

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)
N = len(runes)
print(f"Total runes: {N}")

original_score = score_text(runes)
print(f"Original score: {original_score}")

print("\n" + "="*70)
print("TEST: COLUMNAR TRANSPOSITION (read by columns)")
print("="*70)

# Key length 113 - read in columns of width 113?
# But 259 / 113 = 2.3 rows, too short

# Try various column widths
best_score = original_score
best_width = 0
best_result = None

for width in range(2, 50):
    # Read by columns
    num_rows = (N + width - 1) // width
    
    # Pad to fill grid
    padded = runes + ['F'] * (num_rows * width - N)
    
    # Create grid and read by columns
    result = []
    for col in range(width):
        for row in range(num_rows):
            idx = row * width + col
            if idx < N:
                result.append(runes[idx])
    
    score = score_text(result)
    if score > best_score:
        best_score = score
        best_width = width
        best_result = result
        print(f"Width {width}: Score {score} (better!)")

if best_result:
    print(f"\nBest columnar: width={best_width}, score={best_score}")
    print(f"Text: {''.join(best_result[:80])}...")
else:
    print("No columnar improvement found")

print("\n" + "="*70)
print("TEST: RAIL FENCE CIPHER")
print("="*70)

for rails in range(2, 10):
    # Read in zigzag pattern
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for r in runes:
        fence[rail].append(r)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    result = []
    for row in fence:
        result.extend(row)
    
    score = score_text(result)
    if score > original_score:
        print(f"Rails {rails}: Score {score} (better!)")
        print(f"Text: {''.join(result[:80])}...")

print("\n" + "="*70)
print("TEST: REVERSE COLUMNAR (undo transposition)")
print("="*70)

# What if the original text was transposed? Try to undo it.
for width in range(2, 50):
    num_rows = (N + width - 1) // width
    
    # Assuming text was written by columns, read by rows
    # We reverse: read by columns to get original row order
    result = []
    for row in range(num_rows):
        for col in range(width):
            idx = col * num_rows + row
            if idx < N:
                result.append(runes[idx])
    
    score = score_text(result)
    if score > original_score:
        print(f"Reverse width {width}: Score {score} (better!)")
        print(f"Text: {''.join(result[:80])}...")

print("\n" + "="*70)
print("TEST: SKIP CIPHER (read every Nth rune)")
print("="*70)

for skip in range(2, 20):
    for offset in range(skip):
        # Read every Nth rune starting at offset
        result = [runes[i] for i in range(offset, N, skip)]
        
        score = score_text(result)
        if score > 50:  # Show any reasonable result
            text = ''.join(result)
            if 'THAT' in text or 'DOETH' in text or 'GOETH' in text:
                print(f"Skip {skip}, offset {offset}: Score {score}")
                print(f"Text: {text[:60]}...")

print("\n" + "="*70)
print("TEST: KEY-BASED TRANSPOSITION")
print("="*70)

# Use key derived from primes or key sum patterns
def keyed_transpose(runes, key):
    """Transpose runes using a numeric key"""
    n = len(key)
    result = []
    
    # Sort key to get column order
    sorted_key = sorted(enumerate(key), key=lambda x: x[1])
    
    # Number of full rows
    num_rows = (len(runes) + n - 1) // n
    
    # Pad
    padded = list(runes) + ['F'] * (num_rows * n - len(runes))
    
    # Create grid (rows x cols)
    grid = []
    for row in range(num_rows):
        grid.append(padded[row * n:(row + 1) * n])
    
    # Read columns in key order
    for orig_pos, _ in sorted_key:
        for row in range(num_rows):
            if row * n + orig_pos < len(runes):
                result.append(grid[row][orig_pos])
    
    return result[:len(runes)]

# Test with simple numeric keys
test_keys = [
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],  # Pi digits
    [1, 1, 2, 3, 5, 8, 13, 21],  # Fibonacci
    [2, 3, 5, 7, 11, 13, 17],  # Primes
]

for key in test_keys:
    result = keyed_transpose(runes, key)
    score = score_text(result)
    if score > original_score:
        print(f"Key {key[:5]}...: Score {score}")
        print(f"Text: {''.join(result[:60])}...")

print("\n" + "="*70)
print("TEST: PRIME INDEX READING")  
print("="*70)

# Read only runes at prime positions
def get_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(limit + 1) if sieve[i]]

primes = get_primes(N)
prime_runes = [runes[p] for p in primes if p < N]
print(f"Prime positions ({len(prime_runes)} runes): {''.join(prime_runes)}")

# Non-prime positions
non_prime_runes = [runes[i] for i in range(N) if i not in primes]
print(f"Non-prime positions ({len(non_prime_runes)} runes): {''.join(non_prime_runes[:80])}...")

print("\n" + "="*70)
print("TEST: INTERLEAVED STREAMS")
print("="*70)

# What if text is interleaved from 2 or 3 messages?
for streams in range(2, 6):
    print(f"\n{streams} interleaved streams:")
    for s in range(streams):
        stream_runes = [runes[i] for i in range(s, N, streams)]
        score = score_text(stream_runes)
        text = ''.join(stream_runes)
        
        # Look for meaningful words
        words_found = []
        for word in ['THAT', 'THE', 'DOETH', 'GOETH', 'HATH', 'THOU', 'THEE']:
            if word in text:
                words_found.append(word)
        
        print(f"  Stream {s}: {text[:50]}...")
        if words_found:
            print(f"    Words found: {words_found}")

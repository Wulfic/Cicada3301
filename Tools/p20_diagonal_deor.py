"""
Page 20 - Advanced Attack: Diagonal + Deor Key
================================================
The hint says "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"
And the decoded artifact ends with "DIAG" (diagonal).

Strategy: 
1. Read P20 diagonally
2. Apply Deor poem as running key
"""

import os
from collections import Counter

# Gematria Primus
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

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

def to_int(text):
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in GP_MAP:
            result.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            result.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return result

def to_str(nums):
    return "".join(INV_MAP[n % 29] for n in nums)

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Load P20
p20 = load_runes("LiberPrimus/pages/page_20/runes.txt")
print(f"P20: {len(p20)} runes, IoC: {calc_ioc(p20):.4f}")

# Load Deor poem (if available)
deor_path = "LiberPrimus/reference/deor.txt"
try:
    deor = load_runes(deor_path)
    print(f"Deor: {len(deor)} runes, IoC: {calc_ioc(deor):.4f}")
except:
    # Deor poem in runeglish
    DEOR_TEXT = """
    WELUND HIM BE WURMAN WRÆCES CUNNADE
    ANHYDIG EORL EARFOÞA DREAG
    HÆFDE HIM TO GESIÞÞE SORGE OND LONGAÞ
    WINTERCEALDE WRÆCE WEAN OFT ONFOND
    SIÞÞAN HINE NIÐHAD ON NEDE LEGDE
    SWONCRE SEONOBENDE ON SYLLAN MONN
    ÞÆS OFEREODE ÞISSES SWA MÆG
    """
    deor = to_int(DEOR_TEXT.upper().replace('\n', ' '))
    print(f"Deor (text): {len(deor)} runes")

# Create 28x29 grid
ROWS = 28
COLS = 29
if ROWS * COLS != len(p20):
    print(f"Warning: grid size mismatch, padding")
    p20 = p20 + [0] * (ROWS * COLS - len(p20))

grid = [p20[r*COLS:(r+1)*COLS] for r in range(ROWS)]

print(f"\nGrid: {ROWS}x{COLS}")

# Diagonal reading patterns
print("\n=== DIAGONAL READING + DEOR KEY ===")

def read_diagonal(grid, step_r=1, step_c=1):
    """Read diagonally with wrap-around"""
    result = []
    visited = set()
    
    for start_c in range(len(grid[0])):
        r, c = 0, start_c
        while len(result) < len(grid) * len(grid[0]):
            if (r, c) not in visited and 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                result.append(grid[r][c])
                visited.add((r, c))
            r += step_r
            c = (c + step_c) % len(grid[0])
            if r >= len(grid):
                break
    
    return result

def word_score(text):
    """Score by common English words"""
    words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
             'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'SAID',
             'DEATH', 'DEAD', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'KNOW',
             'LONE', 'ALONE', 'SELF', 'MEAN', 'PRIME', 'SACRED', 'WISDOM',
             'DEOR', 'SONG', 'REAPER', 'AEON']
    return sum(len(w)**2 for w in words if w in text)

best_result = None
best_score = 0

# Try all diagonal step patterns
for step_c in range(1, 29):
    diag_read = read_diagonal(grid, 1, step_c)
    
    if len(diag_read) < 100:
        continue
    
    # Apply Deor as key (running key cipher)
    key = deor * (len(diag_read) // len(deor) + 1)
    key = key[:len(diag_read)]
    
    for op_name, op in [('sub', lambda c, k: (c-k)%29), 
                        ('add', lambda c, k: (c+k)%29),
                        ('beaufort', lambda c, k: (k-c)%29)]:
        decrypted = [op(c, k) for c, k in zip(diag_read, key)]
        ioc = calc_ioc(decrypted)
        text = to_str(decrypted)
        wscore = word_score(text)
        
        total_score = ioc * 100 + wscore
        
        if total_score > best_score:
            best_score = total_score
            best_result = (step_c, op_name, ioc, wscore, text[:80])
        
        if ioc > 1.3 or wscore > 50:
            print(f"Diag step={step_c}, {op_name}: IoC={ioc:.4f}, Words={wscore}")
            print(f"  {text[:60]}...")

if best_result:
    step_c, op_name, ioc, wscore, text = best_result
    print(f"\nBest: step={step_c}, {op_name}")
    print(f"  IoC={ioc:.4f}, Words={wscore}")
    print(f"  {text}")

# Try prime-sorted diagonal
print("\n=== PRIME-SORTED DIAGONAL ===")

primes = [i for i in range(COLS) if is_prime(i)]
non_primes = [i for i in range(COLS) if not is_prime(i)]

# Rearrange columns by prime status
for arrangement in [primes + non_primes, non_primes + primes, sorted(range(COLS), key=lambda x: (not is_prime(x), x))]:
    rearranged = []
    for r in range(ROWS):
        for c in arrangement:
            rearranged.append(grid[r][c])
    
    # Apply Deor key
    key = deor * (len(rearranged) // len(deor) + 1)
    key = key[:len(rearranged)]
    
    decrypted = [(c - k) % 29 for c, k in zip(rearranged, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    wscore = word_score(text)
    
    if ioc > 1.2 or wscore > 30:
        print(f"Arrangement {arrangement[:5]}...: IoC={ioc:.4f}, Words={wscore}")
        print(f"  {text[:60]}...")

# The hint says "REARRANGING THE PRIMES NUMBERS"
# What if we sort the runes themselves by their prime values?
print("\n=== REARRANGING BY PRIME VALUE ===")

prime_values = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

# Group P20 runes by whether their GP index is prime
prime_runes = [(i, p20[i]) for i in range(len(p20)) if is_prime(p20[i])]
non_prime_runes = [(i, p20[i]) for i in range(len(p20)) if not is_prime(p20[i])]

print(f"Prime-valued runes: {len(prime_runes)}")
print(f"Non-prime-valued runes: {len(non_prime_runes)}")

# Rearrange: primes first, then non-primes
rearranged = [r for _, r in prime_runes] + [r for _, r in non_prime_runes]

# Apply Deor key
key = deor * (len(rearranged) // len(deor) + 1)
key = key[:len(rearranged)]

for op_name, op in [('sub', lambda c, k: (c-k)%29), ('beaufort', lambda c, k: (k-c)%29)]:
    decrypted = [op(c, k) for c, k in zip(rearranged, key)]
    ioc = calc_ioc(decrypted)
    text = to_str(decrypted)
    wscore = word_score(text)
    print(f"Prime-first + Deor ({op_name}): IoC={ioc:.4f}, Words={wscore}")
    print(f"  {text[:60]}...")

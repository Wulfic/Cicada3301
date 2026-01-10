"""
Page 20 Solution Verification Script
=====================================
Validates the "solution candidate" and performs fresh analysis.
"""

import collections
import sys

# Gematria Primus mapping
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
    23: 'D', 24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def analyze_solution_candidate():
    """Analyze the claimed 'solution' from page_20_solution_candidate.txt"""
    print("=" * 60)
    print("ANALYZING SOLUTION CANDIDATE")
    print("=" * 60)
    
    # The claimed plaintext
    claimed = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIRSIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"
    
    print(f"Claimed plaintext: {claimed}")
    print(f"Length: {len(claimed)}")
    
    # Convert to indices for IoC
    latin_to_idx = {}
    for idx, latin in IDX_TO_LATIN.items():
        if latin not in latin_to_idx:
            latin_to_idx[latin] = idx
    
    # Try to parse
    indices = []
    i = 0
    while i < len(claimed):
        if i + 2 <= len(claimed) and claimed[i:i+2] in ['TH', 'EO', 'NG', 'OE', 'AE', 'EA', 'IA']:
            indices.append(latin_to_idx.get(claimed[i:i+2], 0))
            i += 2
        else:
            indices.append(latin_to_idx.get(claimed[i], 0))
            i += 1
    
    ioc = calculate_ioc(indices)
    print(f"IoC of claimed solution: {ioc:.4f}")
    print(f"Expected IoC for English: ~1.7")
    print(f"Random IoC: ~1.0")
    print()
    
    # Check for English words
    english_words = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'THAT', 'IS', 'WAS', 'HE', 'FOR', 'IT', 'WITH', 'AS', 'HIS', 'ON', 'BE', 'AT', 'BY', 'I', 'NOT', 'OR', 'HAVE', 'FROM', 'THEY', 'THIS', 'WERE', 'SHE', 'ALL', 'THEIR', 'WHICH', 'WHAT', 'SO', 'DEAD', 'DEATH', 'MEAN', 'PATH', 'SONG', 'WHO', 'REAPER']
    
    found = []
    for word in english_words:
        if word in claimed:
            found.append(word)
    
    print(f"English words found: {found}")
    print(f"Number of words: {len(found)}")
    
    # Calculate expected random matches
    # For a random 83-char string from 26 letters, probability of 'THE' appearing is roughly (1/26)^3 * 81 ≈ 0.5%
    print(f"\nNote: With 83 characters, finding 2-3 common words is expected by chance.")
    print()
    
    return ioc

def analyze_raw_page20():
    """Fresh analysis of Page 20 raw runes"""
    print("=" * 60)
    print("FRESH ANALYSIS OF PAGE 20")
    print("=" * 60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    
    print(f"Total runes: {len(runes)}")
    print(f"Grid dimensions: 29 x 28 = {29*28} (actual: {len(runes)})")
    print()
    
    # Overall IoC
    ioc = calculate_ioc(runes)
    print(f"Overall IoC: {ioc:.4f}")
    
    # Frequency distribution
    counts = collections.Counter(runes)
    print(f"\nFrequency distribution (top 10):")
    for idx, cnt in counts.most_common(10):
        print(f"  {IDX_TO_LATIN[idx]:3s} (idx {idx:2d}): {cnt:3d} ({cnt/len(runes)*100:.1f}%)")
    
    # Expected uniform distribution
    expected = len(runes) / 29
    print(f"\nExpected uniform: {expected:.1f} per rune")
    
    # Chi-squared test
    chi_sq = sum((cnt - expected)**2 / expected for cnt in counts.values())
    print(f"Chi-squared: {chi_sq:.2f} (df=28, critical 95%=41.3)")
    
    return runes

def test_prime_extractions(runes):
    """Test various prime-based extractions"""
    print("\n" + "=" * 60)
    print("PRIME-BASED EXTRACTIONS")
    print("=" * 60)
    
    # 1. Extract runes at prime positions (0-indexed)
    primes = [i for i in range(len(runes)) if is_prime(i)]
    prime_runes = [runes[i] for i in primes if i < len(runes)]
    print(f"\n1. Runes at PRIME POSITIONS (0-indexed):")
    print(f"   Count: {len(prime_runes)}")
    print(f"   IoC: {calculate_ioc(prime_runes):.4f}")
    print(f"   Text: {runes_to_latin(prime_runes[:50])}...")
    
    # 2. Extract runes with prime VALUES
    prime_values = [2, 3, 5, 7, 11, 13]  # First few primes are in the low indices
    prime_idx_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}  # Indices 0-13 have prime values
    prime_val_runes = [r for r in runes if r in prime_idx_set]
    print(f"\n2. Runes with PRIME VALUES (idx 0-13):")
    print(f"   Count: {len(prime_val_runes)}")
    print(f"   IoC: {calculate_ioc(prime_val_runes):.4f}")
    
    # 3. Non-prime positions
    non_prime_runes = [runes[i] for i in range(len(runes)) if not is_prime(i)]
    print(f"\n3. Runes at NON-PRIME POSITIONS:")
    print(f"   Count: {len(non_prime_runes)}")
    print(f"   IoC: {calculate_ioc(non_prime_runes):.4f}")
    
    return prime_runes, non_prime_runes

def test_deor_running_key(runes):
    """Test Deor poem as running key"""
    print("\n" + "=" * 60)
    print("DEOR RUNNING KEY TEST")
    print("=" * 60)
    
    # Load Deor poem and convert to indices
    deor_path = r"c:\Users\tyler\Repos\Cicada3301\Analysis\Reference_Docs\deor_poem.txt"
    try:
        with open(deor_path, 'r', encoding='utf-8') as f:
            deor_text = f.read().upper()
    except:
        print("Could not load Deor poem file")
        return
    
    # Convert to simple indices (A=0, B=1, etc.) for English text
    latin_to_idx = {
        'F': 0, 'U': 1, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'P': 13, 'X': 14, 'S': 15,
        'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'D': 23,
        'A': 24, 'Y': 26
    }
    
    # Extract letters only
    deor_indices = []
    for c in deor_text:
        if c in latin_to_idx:
            deor_indices.append(latin_to_idx[c])
    
    print(f"Deor poem length (letters): {len(deor_indices)}")
    
    if len(deor_indices) < len(runes):
        print("Deor poem too short for full running key")
        return
    
    # Test Vigenère subtract
    result = [(runes[i] - deor_indices[i]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(result)
    print(f"\nC - Deor (standard running key):")
    print(f"   IoC: {ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")
    
    # Test Vigenère add
    result = [(runes[i] + deor_indices[i]) % 29 for i in range(len(runes))]
    ioc = calculate_ioc(result)
    print(f"\nC + Deor (Beaufort variant):")
    print(f"   IoC: {ioc:.4f}")
    print(f"   Preview: {runes_to_latin(result[:80])}")

def test_grid_transpositions(runes):
    """Test grid-based transpositions"""
    print("\n" + "=" * 60)
    print("GRID TRANSPOSITION TESTS")
    print("=" * 60)
    
    # Create 29x28 grid
    rows = 28
    cols = 29
    
    if len(runes) != rows * cols:
        print(f"Warning: Rune count {len(runes)} != {rows}x{cols}={rows*cols}")
    
    grid = []
    for r in range(rows):
        row = runes[r*cols:(r+1)*cols]
        grid.append(row)
    
    # Test 1: Read by columns
    col_read = []
    for c in range(cols):
        for r in range(rows):
            if c < len(grid[r]):
                col_read.append(grid[r][c])
    
    print(f"\n1. Read by COLUMNS:")
    print(f"   IoC: {calculate_ioc(col_read):.4f}")
    
    # Test 2: Read prime columns only
    prime_cols = [c for c in range(cols) if is_prime(c)]
    prime_col_read = []
    for c in prime_cols:
        for r in range(rows):
            if c < len(grid[r]):
                prime_col_read.append(grid[r][c])
    
    print(f"\n2. Read PRIME COLUMNS only ({prime_cols}):")
    print(f"   Count: {len(prime_col_read)}")
    print(f"   IoC: {calculate_ioc(prime_col_read):.4f}")
    
    # Test 3: Spiral read
    spiral = []
    top, bottom, left, right = 0, rows-1, 0, cols-1
    while top <= bottom and left <= right:
        for c in range(left, right+1):
            if top < len(grid) and c < len(grid[top]):
                spiral.append(grid[top][c])
        top += 1
        for r in range(top, bottom+1):
            if r < len(grid) and right < len(grid[r]):
                spiral.append(grid[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left-1, -1):
                if bottom < len(grid) and c < len(grid[bottom]):
                    spiral.append(grid[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top-1, -1):
                if r < len(grid) and left < len(grid[r]):
                    spiral.append(grid[r][left])
            left += 1
    
    print(f"\n3. SPIRAL read:")
    print(f"   Count: {len(spiral)}")
    print(f"   IoC: {calculate_ioc(spiral):.4f}")
    
    # Test 4: Diagonal read
    diag = []
    for d in range(rows + cols - 1):
        for r in range(rows):
            c = d - r
            if 0 <= c < cols and r < len(grid) and c < len(grid[r]):
                diag.append(grid[r][c])
    
    print(f"\n4. DIAGONAL read:")
    print(f"   Count: {len(diag)}")
    print(f"   IoC: {calculate_ioc(diag):.4f}")

def main():
    print("PAGE 20 SOLUTION VERIFICATION")
    print("=" * 60)
    print()
    
    # Check claimed solution
    ioc_claimed = analyze_solution_candidate()
    
    # Fresh analysis
    runes = analyze_raw_page20()
    
    # Test prime extractions
    prime_runes, non_prime = test_prime_extractions(runes)
    
    # Test Deor running key
    test_deor_running_key(runes)
    
    # Test grid transpositions
    test_grid_transpositions(runes)
    
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    print("""
The "solution candidate" in page_20_solution_candidate.txt is NOT verified:
1. IoC is too low for English (~1.0 vs expected ~1.7)
2. The methodology (Pair Sum + Page 24 Key) is arbitrary
3. Words found ("DEAD", "THE") are expected by random chance
4. No clear English message emerges

Page 20 Status: UNSOLVED

The hint "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"
has not been successfully applied. Further investigation needed.
""")

if __name__ == "__main__":
    main()

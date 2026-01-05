"""
Calculate Index of Coincidence (IoC) for Page 1 at various key lengths.

If Page 1 uses a polyalphabetic cipher, the IoC will spike at the true key length
when we partition the ciphertext into co-sets.
"""

import os
from collections import Counter

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

def load_page1():
    """Load Page 1 from transcription file."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1 = segments[0]
    
    # Extract rune indices only
    rune_indices = [RUNE_TO_INDEX[c] for c in page1 if c in RUNE_TO_INDEX]
    return rune_indices

def calculate_ioc(text_indices):
    """Calculate Index of Coincidence for a text (as list of indices 0-28)."""
    n = len(text_indices)
    if n <= 1:
        return 0.0
    
    freq = Counter(text_indices)
    
    # IoC = sum(f_i * (f_i - 1)) / (n * (n - 1))
    numerator = sum(count * (count - 1) for count in freq.values())
    denominator = n * (n - 1)
    
    return numerator / denominator if denominator > 0 else 0.0

def calculate_ioc_for_period(text_indices, period):
    """Calculate average IoC when text is split into co-sets of given period."""
    if period < 1:
        return 0.0
    
    # Split into co-sets
    cosets = [[] for _ in range(period)]
    for i, idx in enumerate(text_indices):
        cosets[i % period].append(idx)
    
    # Calculate IoC for each co-set and average
    iocs = []
    for coset in cosets:
        if len(coset) > 1:
            iocs.append(calculate_ioc(coset))
    
    return sum(iocs) / len(iocs) if iocs else 0.0

def main():
    print("=" * 80)
    print("Index of Coincidence Analysis - Page 1")
    print("=" * 80)
    
    page1_indices = load_page1()
    print(f"\nPage 1 length: {len(page1_indices)} runes")
    
    # Calculate IoC for the full text (no period assumption)
    full_ioc = calculate_ioc(page1_indices)
    print(f"Full text IoC: {full_ioc:.4f}")
    
    # Expected IoC values:
    # - Random text (29 symbols): ~1/29 ≈ 0.0345
    # - English-like text: ~0.065-0.070 (higher due to letter frequency variation)
    # - Polyalphabetic cipher: closer to random (~0.035-0.040)
    
    print(f"\nExpected values:")
    print(f"  Random (29 symbols): ~0.0345")
    print(f"  English-like: ~0.065-0.070")
    print(f"  Polyalphabetic: ~0.035-0.040")
    
    # Test key lengths from 1 to 150
    print("\n" + "=" * 80)
    print("IoC by Key Length (testing for periodicity)")
    print("=" * 80)
    print(f"\n{'Length':<8} {'IoC':<10} {'vs Full':<10} {'Notes'}")
    print("-" * 80)
    
    results = []
    for period in range(1, 151):
        ioc = calculate_ioc_for_period(page1_indices, period)
        diff = ioc - full_ioc
        results.append((period, ioc, diff))
    
    # Sort by IoC (descending) to find peaks
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    
    # Show top 20 periods by IoC
    print("\nTop 20 periods by IoC:")
    for period, ioc, diff in sorted_results[:20]:
        note = ""
        if period == 95:
            note = "← MASTER KEY LENGTH"
        elif period in [1, 2, 3, 5, 7, 11, 13]:
            note = f"← small factor"
        elif period % 95 == 0 or 95 % period == 0:
            note = f"← factor/multiple of 95"
        
        print(f"{period:<8} {ioc:<10.4f} {diff:+10.4f} {note}")
    
    # Also show specific interesting lengths
    print("\n" + "=" * 80)
    print("Specific key lengths of interest:")
    print("=" * 80)
    print(f"\n{'Length':<8} {'IoC':<10} {'Notes'}")
    print("-" * 80)
    
    interesting = [1, 5, 11, 19, 29, 47, 53, 95, 190, 254]
    for period in interesting:
        if period <= len(page1_indices):
            ioc = calculate_ioc_for_period(page1_indices, period)
            note = ""
            if period == 95:
                note = "Master key length"
            elif period == 254:
                note = "Page 1 length"
            elif period == 29:
                note = "Alphabet size"
            elif period in [5, 11, 19, 47, 53]:
                note = "Prime from gematria"
            
            print(f"{period:<8} {ioc:<10.4f} {note}")

if __name__ == "__main__":
    main()

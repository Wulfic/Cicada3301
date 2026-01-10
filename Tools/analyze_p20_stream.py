import os
import sys

# The stream we extracted from P20 Primes - Deor Primes + Shift 5
# IoC 1.1459
STREAM = "YEOTJEOBJSGOXAEOUIWEEOHSHCHELTFFXENGMHETHEAAEWTHFJIAHEAJYFCN"

def get_gem_map():
    # GP Gematria
    return {
        'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
        'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
        'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }

def get_inv_gem_map():
    gem = get_gem_map()
    return {v: k for k, v in gem.items()}

def to_int(text):
    gem = get_gem_map()
    # Determine splitting (greedy)
    res = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text) and text[i:i+2] in gem:
            res.append(gem[text[i:i+2]])
            i += 2
        elif text[i] in gem:
            res.append(gem[text[i]])
            i += 1
        else:
            # Skip unknown
            i += 1
    return res

def to_str(nums):
    inv = get_inv_gem_map()
    return "".join([inv.get(n, "?") for n in nums])

def atbash(text):
    gem = get_gem_map()
    inv = get_inv_gem_map()
    nums = to_int(text)
    atbashed = [28 - n for n in nums]
    return to_str(atbashed)

def analyze_frequency(text):
    counts = {}
    total = 0
    # Treat as single letters for approximate frequency
    # Ideally should use runic parsing
    nums = to_int(text)
    for n in nums:
        counts[n] = counts.get(n, 0) + 1
        total += 1
    
    inv = get_inv_gem_map()
    print(f"Length (Runes): {total}")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("Top Frequencies:")
    for num, count in sorted_counts[:5]:
        rune = inv[num]
        print(f"  {rune}: {count} ({count/total*100:.1f}%)")

def find_substrings(text, min_len=3):
    print(f"\nChecking for common English substrings in: {text}")
    common = ["THE", "AND", "ING", "ENT", "ION", "HER", "FOR", "THA", "NTH", "INT", "ERE", "TIO", "TER", "EST", "ERS", "ATI", "HAT", "ATE", "ALL", "ETH", "HES", "VER", "HIS", "OFT", "ITH", "FTH", "STH", "OTH", "RES", "ONT", "ENG", "ISH", "KEY", "DEOR", "PATH"]
    
    found = []
    for s in common:
        if s in text:
            found.append(s)
    
    if found:
        print(f"Found: {', '.join(found)}")
    else:
        print("None found.")

def main():
    print("--- Analysis of P20 Prime Stream ---")
    print(f"Stream: {STREAM}")
    analyze_frequency(STREAM)
    find_substrings(STREAM)
    
    reversed_stream = STREAM[::-1] # Naive reverse (might break digraphs)
    # Better reverse:
    nums = to_int(STREAM)
    reversed_str = to_str(nums[::-1])
    
    print("\n--- Reversed ---")
    print(f"Rev: {reversed_str}")
    find_substrings(reversed_str)
    
    print("\n--- Atbash ---")
    atb = atbash(STREAM)
    print(f"Atbash: {atb}")
    find_substrings(atb)
    
    print("\n--- Atbash Reversed ---")
    atb_rev = atbash(reversed_str)
    print(f"AtbRev: {atb_rev}")
    find_substrings(atb_rev)

    # Check for "Words" using a dictionary if possible (later)

if __name__ == "__main__":
    main()

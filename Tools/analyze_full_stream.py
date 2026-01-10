import sys

def get_gp_map():
    return {
        'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
        'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
        'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }

def get_inv_map():
    return {v: k for k, v in get_gp_map().items()}

def to_int(text):
    gem = get_gp_map()
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
            i += 1
    return res

def to_str(nums):
    inv = get_inv_map()
    return "".join([inv.get(n, "?") for n in nums])

def atbash(nums):
    return [28 - n for n in nums]

def analyze(text, label=""):
    print(f"\n[{label}] Length: {len(text)} Runes")
    
    # Substrings
    common = ["THE", "AND", "ING", "ENT", "ION", "HER", "FOR", "THA", "NTH", "INT", "ERE", "TIO", "TER", "EST", "ERS", "ATI", "HAT", "ATE", "ALL", "ETH", "HES", "VER", "HIS", "OFT", "ITH", "FTH", "STH", "OTH", "RES", "ONT", "ENG", "ISH", "KEY", "DEOR", "PATH", "IAM", "JOY", "ICY", "BE", "DEATH", "LIFE", "WARN", "NO", "YES"]
    
    found = []
    for s in common:
        if s in text:
            found.append(s)
    if found:
        print(f"Substrings: {', '.join(sorted(found))}")
        
    # Frequencies
    counts = {}
    for n in to_int(text):
        counts[n] = counts.get(n, 0) + 1
    total = len(to_int(text))
    inv = get_inv_map()
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("Top 5 Freqs:")
    for num, c in sorted_counts[:5]:
        print(f"  {inv[num]}: {c} ({c/total*100:.1f}%)")
        
    print(f"Preview: {text[:80]}...")

def main():
    path = "Analysis/Outputs/p20_prime_stream_full.txt"
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except:
        print("File not found.")
        return

    # Extract clean stream lines (skip headers)
    stream1 = ""
    stream2 = ""
    
    current = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith("--- Method 1"):
            current = 1
            continue
        if line.startswith("--- Method 2"):
            current = 2
            continue
            
        if current == 1:
            stream1 += line
        elif current == 2:
            stream2 += line
            
    # Analyze Method 1
    nums1 = to_int(stream1)
    analyze(stream1, "Method 1 (C-K+5)")
    
    atb1_nums = atbash(nums1)
    atb1_str = to_str(atb1_nums)
    analyze(atb1_str, "Method 1 Atbash")

    rev1_str = to_str(nums1[::-1])
    analyze(rev1_str, "Method 1 Reversed")
    
    atb_rev1_str = to_str(atb1_nums[::-1])
    analyze(atb_rev1_str, "Method 1 Atbash Reversed")

    # Analyze Method 2
    nums2 = to_int(stream2)
    analyze(stream2, "Method 2 (Beaufort)")
    
    atb2_nums = atbash(nums2)
    atb2_str = to_str(atb2_nums)
    analyze(atb2_str, "Method 2 Atbash")

if __name__ == "__main__":
    main()

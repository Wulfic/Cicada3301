#!/usr/bin/env python3
"""
Test if SUB operation with optimized key length works on Page 2
This validates whether the SUB-71 breakthrough on Page 1 extends to other pages
"""

import json
from pathlib import Path
from collections import Counter

# Rune alphabet (29 runes)
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

# Gematria Primus alphabet (for reference, 24 letters but we work with indices 0-28)
LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def text_to_indices(text):
    """Convert Gematria Primus text to indices - for already converted text, just return indices"""
    # Text is actually already a string of letter names, we need to work with rune indices
    # This function is not used for loading, but for reference
    return [i for i in range(len(text))]

def indices_to_text(indices):
    """Convert indices to Gematria Primus text"""
    return ''.join(LETTERS[i] if 0 <= i < len(LETTERS) else '?' for i in indices)

def compute_ioc(indices, key_length):
    """Compute Index of Coincidence for a given key length"""
    cosets = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        cosets[i % key_length].append(idx)
    
    ioc_sum = 0.0
    for coset in cosets:
        if len(coset) < 2:
            continue
        freqs = Counter(coset)
        n = len(coset)
        ioc = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1)) if n > 1 else 0
        ioc_sum += ioc
    
    return ioc_sum / key_length if key_length > 0 else 0

def load_page2():
    """Load Page 2 ciphertext from the transcription file"""
    trans_path = Path(__file__).parent.parent / "2014" / "Liber Primus" / "runes in text format.txt"
    
    if not trans_path.exists():
        print(f"ERROR: Transcription file not found at {trans_path}")
        return None
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by % to get pages
    segments = content.split('%')
    if len(segments) < 2:
        print("ERROR: Could not find Page 2 (not enough segments)")
        return None
    
    # Page 2 is the second segment (index 1)
    page2_runes = segments[1]
    
    # Convert runes to indices (0-28)
    page2_indices = [RUNE_TO_INDEX[c] for c in page2_runes if c in RUNE_TO_INDEX]
    
    return page2_indices

def main():
    print("=" * 80)
    print("PAGE 2 - IOC ANALYSIS TO FIND KEY LENGTH")
    print("=" * 80)
    
    page2 = load_page2()
    if not page2:
        print("\nERROR: Could not load Page 2")
        print("Expected location: 2014/Liber Primus/runes in text format.txt")
        return
    
    indices = page2  # Already in index format
    
    print(f"\nPage 2 Statistics:")
    print(f"  Length: {len(indices)} runes")
    print(f"  First 20 indices: {indices[:20]}")
    print(f"  Preview: {indices_to_text(indices[:50])}")
    
    # Test key lengths from 1 to 150
    print("\n" + "=" * 80)
    print("IOC ANALYSIS (testing key lengths 1-150)")
    print("=" * 80)
    
    results = []
    for klen in range(1, 151):
        ioc = compute_ioc(indices, klen)
        results.append((klen, ioc))
    
    # Sort by IoC score
    results_sorted = sorted(results, key=lambda x: x[1], reverse=True)
    
    print("\nTop 20 key lengths by IoC:")
    print(f"{'Rank':<6} {'Key Length':<12} {'IoC Score':<15} {'Notes'}")
    print("-" * 80)
    
    for i, (klen, ioc) in enumerate(results_sorted[:20], 1):
        notes = []
        if klen == 71:
            notes.append("** SAME AS PAGE 1 **")
        if klen == 95:
            notes.append("(master key length)")
        if klen in [29, 58, 87, 116, 145]:
            notes.append("(multiple of 29)")
        if klen in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
            notes.append("(prime)")
        
        note_str = " ".join(notes) if notes else ""
        print(f"{i:<6} {klen:<12} {ioc:<15.6f} {note_str}")
    
    # Highlight key findings
    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    
    top_key_length, top_ioc = results_sorted[0]
    print(f"\nHighest IoC: key length {top_key_length} with IoC {top_ioc:.6f}")
    
    # Check if 71 is in top ranks
    klen_71_ioc = next((ioc for klen, ioc in results if klen == 71), None)
    klen_71_rank = next((i for i, (klen, ioc) in enumerate(results_sorted, 1) if klen == 71), None)
    
    if klen_71_rank:
        print(f"\nKey length 71 (same as Page 1):")
        print(f"  Rank: #{klen_71_rank}")
        print(f"  IoC: {klen_71_ioc:.6f}")
        
        if klen_71_rank <= 5:
            print("  ✅ Page 2 likely uses same key length as Page 1!")
        elif klen_71_rank <= 20:
            print("  ⚠️  Key length 71 is plausible but not top-ranked")
        else:
            print("  ❌ Key length 71 does not work well for Page 2")
    
    # Check master key length
    klen_95_ioc = next((ioc for klen, ioc in results if klen == 95), None)
    klen_95_rank = next((i for i, (klen, ioc) in enumerate(results_sorted, 1) if klen == 95), None)
    
    if klen_95_rank:
        print(f"\nMaster key length 95:")
        print(f"  Rank: #{klen_95_rank}")
        print(f"  IoC: {klen_95_ioc:.6f}")
    
    # Save results to file
    output_path = Path(__file__).parent / "PAGE2_IOC_RESULTS.txt"
    with open(output_path, 'w') as f:
        f.write("PAGE 2 - IOC ANALYSIS RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Page 2 length: {len(indices)} runes\n\n")
        f.write("Top 50 key lengths by IoC:\n")
        f.write(f"{'Rank':<6} {'Key Length':<12} {'IoC Score':<15}\n")
        f.write("-" * 80 + "\n")
        for i, (klen, ioc) in enumerate(results_sorted[:50], 1):
            f.write(f"{i:<6} {klen:<12} {ioc:<15.6f}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("FULL RESULTS (all key lengths 1-150)\n")
        f.write("=" * 80 + "\n")
        for klen, ioc in results:
            f.write(f"{klen:<6} {ioc:.6f}\n")
    
    print(f"\nFull results saved to: {output_path}")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print(f"""
1. If key length {top_key_length} ranks highest:
   - Create tool: page2_sub{top_key_length}_attack.py
   - Use SUB operation (not XOR) based on Page 1 findings
   - Verify perfect reversibility

2. Compare Page 1 and Page 2 key lengths:
   - If same (71): Pages may share key or methodology
   - If different: Each page has unique key length

3. Test SUB operation systematically:
   - Frequency-based key initialization
   - Hill-climbing optimization
   - Check reversibility (must be 100%)
""")

if __name__ == '__main__':
    main()

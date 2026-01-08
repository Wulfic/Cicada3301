#!/usr/bin/env python3
"""
Attempt to parse first-layer output as Old English with THE as word boundary.
Given: AETHATAEYETHESTHESTHEAEATHEORNG...
Theory: Text might be compressed Old English with spaces removed.

Approach: Use THE as potential word boundary and analyze resulting words.
"""

PAGES = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYCKTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGTHEESTHENGTTHEATHEATHTHEAHENGTHETHTHRAAINGTHETHEATETHWAETHEAINGWHIATTHETHATHENGRHEATHEATHETHISOFRAETHOFITHEAEMTHEINGENGTHEHETHEATHFMHTHENGWNGETHEHETHEBDEHEADTHEINGTHEINGTHEAOINGETHIINGITNGTTHWEOTHEHENGTHEATHTHENGNGATHESTWTHETHTHEATHNGETHEIREOENGNG",
    2: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHEAHNGOOEOHISRAEOITHLEAAONGAAAHREINGOFOTHTBTHENREINGTHEAYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHEKSINGTHBCFAJITHATHEUINTHEMTHETHEOREAOEINGOMTHEEEATHEOEHEJSOHENGIINGHINGINGEAITHEIAHEOYNGTHEAISHNRFEOIAHEFANEIAHEOEHEOEHENGTHETHEORNG",
    3: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBITHETHETHATHENGEHEITHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSO",
    4: "EMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBEMBTHETHETOSOTHETHEOTHIHTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATHETHIHETHENGTHENGEOINGEOINGEITHTBTBETHEOTHETHINGHEETHHEINGHENGATHETHETSOTSOTHEOHEOTHETHENGTHETHEITHEOFEATHTHETHTHETOITSATTHETHETHENG"
}

def split_on_the(text):
    """Split text on THE occurrences"""
    parts = text.split('THE')
    return [p for p in parts if p]  # Remove empty strings

def analyze_splits(parts, name):
    """Analyze the parts created by splitting on THE"""
    print(f"\n{'='*60}")
    print(f"{name} - Split on 'THE'")
    print(f"{'='*60}")
    print(f"Original parts ({len(parts)} segments):")
    
    # Show first 20 parts
    for i, p in enumerate(parts[:20]):
        if len(p) >= 2:
            print(f"  [{i}] {p}")
    print(f"  ...")
    
    # Look for patterns in the parts
    # Common Old English suffixes
    suffixes = ['ETH', 'EST', 'ED', 'ING', 'LY', 'ER', 'EN', 'TH', 'ST', 'RE']
    prefixes = ['UN', 'BE', 'FOR', 'OUT', 'OVER', 'UNDER', 'WITH']
    
    print(f"\nParts ending with common suffixes:")
    for suffix in suffixes:
        matching = [p for p in parts if p.endswith(suffix)]
        if matching:
            print(f"  -{suffix}: {matching[:5]}")
    
    print(f"\nParts starting with common prefixes:")
    for prefix in prefixes:
        matching = [p for p in parts if p.startswith(prefix)]
        if matching:
            print(f"  {prefix}-: {matching[:5]}")

def reconstruct_with_the(text):
    """
    Try to reconstruct readable text by treating THE as a word separator.
    Format: [part1] THE [part2] THE [part3]...
    """
    parts = text.split('THE')
    
    # Try different interpretations
    reconstructions = []
    
    # 1. THE as "the" (article)
    words = []
    for i, part in enumerate(parts):
        if part:
            words.append(part)
        if i < len(parts) - 1:
            words.append('THE')
    reconstructions.append(('THE as word', ' '.join(words)))
    
    # 2. THE attached to following word
    words = []
    for i, part in enumerate(parts):
        if i == 0 and part:
            words.append(part)
        elif part:
            words.append('THE' + part)
    reconstructions.append(('THE+next', ' '.join(words)))
    
    # 3. THE attached to previous word
    words = []
    for i, part in enumerate(parts):
        if part:
            if i < len(parts) - 1:
                words.append(part + 'THE')
            else:
                words.append(part)
    reconstructions.append(('prev+THE', ' '.join(words)))
    
    return reconstructions

# Main analysis
print("=" * 70)
print("THE-BOUNDARY WORD RECONSTRUCTION ANALYSIS")
print("=" * 70)

for pnum, text in sorted(PAGES.items()):
    # Strip EMB for pages 2-4
    if pnum >= 2:
        while text.startswith('EMB'):
            text = text[3:]
    
    parts = split_on_the(text)
    analyze_splits(parts, f"Page {pnum}")
    
    # Show reconstructions
    print(f"\nReconstructions (first 100 chars):")
    for name, recon in reconstruct_with_the(text):
        print(f"  {name}: {recon[:100]}...")

# Look for pattern: A ETH AT A EYE THE S THE S THE A EA THE OR NG
print("\n" + "=" * 70)
print("MANUAL WORD BOUNDARY ATTEMPT - Page 0 Opening")
print("=" * 70)

opening = PAGES[0][:100]
print(f"Raw: {opening}")
print()

# Try to find meaningful word boundaries
# AETHATAEYETHESTHESTHEAEATHEORNG...
# Could be: AE THAT A EYE THES THES THEA EA THE ORNG...
# Or: A ETH AT A EYE THE S THE S THE A EA THE ORNG...

manual_parses = [
    "AE THAT A EYE THES THES THE A EA THE ORNG",
    "A ETH AT A EYE THE S THE S THE A EA THE OR NG",
    "AETH AT AE YE THE S THES THE AEA THE ORNG",
    "AE THAT AE YE THES THES THE AEEA THE ORNG THRO",
]

print("Possible manual parses of opening:")
for parse in manual_parses:
    print(f"  {parse}")

# Check if "AE" is a valid Old English word (yes - "ever, always")
# Check if "ETH" is valid (yes - verb suffix)
# "THAT" is valid
# "EYE" is valid
# "THES" - could be genitive "THESE"

print("\n" + "=" * 70)
print("FREQUENCY ANALYSIS OF SPLIT SEGMENTS")
print("=" * 70)

from collections import Counter

for pnum, text in sorted(PAGES.items()):
    if pnum >= 2:
        while text.startswith('EMB'):
            text = text[3:]
    
    parts = split_on_the(text)
    part_counts = Counter(parts)
    
    print(f"\nPage {pnum} - Most common segments:")
    for segment, count in part_counts.most_common(15):
        if len(segment) >= 2:
            print(f"  {segment}: {count}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

"""
Diagnostic script to verify Page 1 transcription quality.

Checks:
- Rune statistics (length, frequency distribution)
- Comparison with Page 57 (Parable) distribution as baseline
- Detection of anomalies (repeated sequences, unusual patterns)
- Word boundary markers
"""

import os
from collections import Counter

# Rune alphabet (index 0..28)
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

def load_transcription_pages():
    """Load pages from the transcription file (split on %)."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    return segments

def analyze_page(page_text, page_name):
    """Analyze a page and return diagnostic info."""
    # Extract only runes
    runes_only = ''.join(c for c in page_text if c in RUNES)
    
    # Count all characters
    total_chars = len(page_text)
    rune_count = len(runes_only)
    
    # Special markers
    word_sep = page_text.count('•')
    hyphen = page_text.count('-')
    percent = page_text.count('%')
    ampersand = page_text.count('&')
    dollar = page_text.count('$')
    colon = page_text.count(':')
    
    # Rune frequency
    rune_freq = Counter(runes_only)
    
    # Convert to indices for stats
    indices = [RUNE_TO_INDEX[r] for r in runes_only]
    
    # Look for repeated sequences (potential transcription errors)
    repeated_3 = []
    for i in range(len(runes_only) - 2):
        trigram = runes_only[i:i+3]
        if runes_only.count(trigram) > 5:  # Appears more than 5 times
            repeated_3.append((trigram, runes_only.count(trigram)))
    
    repeated_3 = list(set(repeated_3))  # Remove duplicates
    repeated_3.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'name': page_name,
        'total_chars': total_chars,
        'rune_count': rune_count,
        'markers': {
            'word_sep': word_sep,
            'hyphen': hyphen,
            'percent': percent,
            'ampersand': ampersand,
            'dollar': dollar,
            'colon': colon
        },
        'rune_freq': rune_freq,
        'indices': indices,
        'repeated_trigrams': repeated_3[:10]  # Top 10
    }

def compare_distributions(page1_stats, page57_stats):
    """Compare rune distributions between Page 1 and Page 57 (Parable)."""
    print("\n=== Rune Frequency Comparison (Page 1 vs Page 57) ===")
    
    # Normalize to percentages
    p1_total = sum(page1_stats['rune_freq'].values())
    p57_total = sum(page57_stats['rune_freq'].values())
    
    print(f"\n{'Rune':<6} {'Index':<6} {'Page1%':<10} {'Page57%':<10} {'Diff':<10}")
    print("-" * 50)
    
    for i, rune in enumerate(RUNES):
        p1_pct = (page1_stats['rune_freq'][rune] / p1_total * 100) if p1_total > 0 else 0
        p57_pct = (page57_stats['rune_freq'][rune] / p57_total * 100) if p57_total > 0 else 0
        diff = abs(p1_pct - p57_pct)
        
        # Flag unusual differences (>3%)
        flag = "  ⚠️" if diff > 3.0 else ""
        print(f"{rune:<6} {i:<6} {p1_pct:<10.2f} {p57_pct:<10.2f} {diff:<10.2f}{flag}")

def main():
    print("=" * 70)
    print("Page 1 Transcription Verification")
    print("=" * 70)
    
    # Load pages
    segments = load_transcription_pages()
    
    print(f"\nTotal segments in transcription file: {len(segments)}")
    
    # Analyze Page 1 (segment 0)
    if len(segments) < 1:
        print("ERROR: No segments found!")
        return
    
    print("\n" + "=" * 70)
    print("Analyzing Page 1 (segment 0)")
    print("=" * 70)
    
    page1_stats = analyze_page(segments[0], "Page 1")
    
    print(f"\nTotal characters: {page1_stats['total_chars']}")
    print(f"Rune count: {page1_stats['rune_count']}")
    print(f"\nMarkers:")
    for marker, count in page1_stats['markers'].items():
        print(f"  {marker}: {count}")
    
    print(f"\nTop 10 most frequent runes:")
    for rune, count in page1_stats['rune_freq'].most_common(10):
        idx = RUNE_TO_INDEX[rune]
        pct = count / page1_stats['rune_count'] * 100
        print(f"  {rune} (index {idx:2d}): {count:4d} ({pct:5.2f}%)")
    
    if page1_stats['repeated_trigrams']:
        print(f"\nRepeated trigrams (appear >5 times):")
        for trigram, count in page1_stats['repeated_trigrams']:
            print(f"  {trigram}: {count} times")
    
    # Analyze Page 57 (Parable) for comparison
    if len(segments) >= 57:
        print("\n" + "=" * 70)
        print("Analyzing Page 57 (Parable) for comparison")
        print("=" * 70)
        
        page57_stats = analyze_page(segments[56], "Page 57")
        
        print(f"\nTotal characters: {page57_stats['total_chars']}")
        print(f"Rune count: {page57_stats['rune_count']}")
        
        # Compare distributions
        compare_distributions(page1_stats, page57_stats)
    
    # Look for potential transcription issues
    print("\n" + "=" * 70)
    print("Potential Issues Check")
    print("=" * 70)
    
    issues = []
    
    # Check for unusual length (Page 1 should be substantial)
    if page1_stats['rune_count'] < 50:
        issues.append(f"⚠️  Page 1 seems very short ({page1_stats['rune_count']} runes)")
    
    # Check for missing word separators
    if page1_stats['markers']['word_sep'] == 0 and page1_stats['rune_count'] > 50:
        issues.append("⚠️  No word separators (•) found - might indicate formatting issue")
    
    # Check for extremely unbalanced rune distribution
    most_common = page1_stats['rune_freq'].most_common(1)[0][1]
    if most_common > page1_stats['rune_count'] * 0.15:
        issues.append(f"⚠️  One rune appears unusually often ({most_common}/{page1_stats['rune_count']} = {most_common/page1_stats['rune_count']*100:.1f}%)")
    
    if issues:
        print("\nPotential issues found:")
        for issue in issues:
            print(issue)
    else:
        print("\n✓ No obvious transcription issues detected")
    
    print("\n" + "=" * 70)
    print(f"Page 1 preview (first 100 chars):")
    print("=" * 70)
    print(segments[0][:100])
    
    print("\n" + "=" * 70)
    print(f"Page 1 runes only (first 50):")
    print("=" * 70)
    runes_only = ''.join(c for c in segments[0] if c in RUNES)
    print(runes_only[:50])

if __name__ == "__main__":
    main()

"""
Check word separator (•) usage across all pages in the transcription.
"""

import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    
    print("=" * 80)
    print("Word Separator (•) Usage Across All Pages")
    print("=" * 80)
    print(f"\n{'Page':<6} {'Runes':<8} {'•':<8} {'Hyphens':<10} {'Ratio':<10}")
    print("-" * 80)
    
    for i, seg in enumerate(segments[:20]):  # First 20 pages
        if not seg.strip():
            continue
        
        runes_only = ''.join(c for c in seg if c in RUNES)
        word_sep = seg.count('•')
        hyphens = seg.count('-')
        ratio = word_sep / len(runes_only) if len(runes_only) > 0 else 0
        
        print(f"{i:<6} {len(runes_only):<8} {word_sep:<8} {hyphens:<10} {ratio:<10.3f}")

if __name__ == "__main__":
    main()

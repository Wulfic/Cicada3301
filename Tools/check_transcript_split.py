
import os

def analyze_runes_full():
    path = "LiberPrimus/reference/transcripts/runes_full.txt"
    if not os.path.exists(path):
        print("File not found")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by % which seems to be the page separator
    # Note: Some files might use % as a separator, checking if it's consistent.
    # Page 0 is known.
    
    sections = content.split('%')
    print(f"Total sections found: {len(sections)}")
    
    for i, section in enumerate(sections):
        # Clean up whitespace
        clean_section = section.strip()
        if not clean_section:
            # Maybe a trailing %
            print(f"Section {i}: EMPTY")
            continue
            
        lines = clean_section.split('\n')
        # Filter out comments/tags if any (like &)
        rune_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith('&') and not l.strip().startswith('$')]
        
        rune_count = sum(len(l) for l in rune_lines)
        print(f"Section {i} (Page {i}): {rune_count} chars")
        if rune_lines:
            print(f"  Start: {rune_lines[0][:20]}")

if __name__ == "__main__":
    analyze_runes_full()

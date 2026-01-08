
import re
import os

SOURCE_FILE = 'LiberPrimus/reference/transcripts/github_liber_primus.md'
OUTPUT_DIR = 'LiberPrimus/pages'

def is_rune_line(line):
    # Check if line contains rune characters (U+16A0 to U+16F0)
    # allow some noise, but mostly runes.
    runes = [c for c in line if '\u16a0' <= c <= '\u16f0']
    if not runes:
        return False
    # Heuristic: if a line has runes, it's a rune line.
    # Ignore lines that are just one rune markers or mixed heavily with text?
    # Actually, the transcript has "English:" text too.
    # We want lines that are *predominantly* runes or part of the rune block.
    # But usually rune lines are clean or have bullets.
    return len(runes) > 0

def extract_content():
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by headers like "## ... XX.jpg"
    # Regex lookahead to split but keep delimiter? No, split captures group.
    # We'll validly finding all headers positions.
    
    # Pattern to find headers and the page number
    # Examples: 
    # ## Liber Primus - 00.jpg
    # ## Runes - 01.jpg
    # ## 03.jpg
    # ## 74.jpg - 57.jpg
    
    pattern = re.compile(r'^##\s+(?:.*?)(\d{2})\.jpg', re.MULTILINE)
    
    last_pos = 0
    matches = list(pattern.finditer(content))
    
    print(f"Found {len(matches)} sections.")
    
    for i, match in enumerate(matches):
        page_num_str = match.group(1)
        page_num = int(page_num_str)
        
        start_pos = match.end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        section_content = content[start_pos:end_pos]
        
        # Extract Runes
        # Strategy: Look for lines with runes.
        lines = section_content.split('\n')
        rune_lines = []
        for line in lines:
            # Clean line
            clean = line.strip()
            if is_rune_line(clean):
                # Remove common non-rune chars like bullets if needed
                # But keep it raw if possible, just stripped
                rune_lines.append(clean)
        
        if rune_lines:
            target_dir = os.path.join(OUTPUT_DIR, f"page_{page_num:02d}")
            os.makedirs(target_dir, exist_ok=True)
            target_file = os.path.join(target_dir, "runes.txt")
            
            # Filter out lines that look like explanations "Runes:" is not a rune line.
            # is_rune_line handles that because "Runes:" has no runes.
            
            # Post-processing: remove bullets '•' if they are separators?
            # User wants runes.
            # Example: ᚱ•ᛝᚱᚪᛗᚹ
            # Keep bullets, they might be separators.
            
            final_text = "\n".join(rune_lines)
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(final_text)
                
            print(f"Page {page_num:02d}: Extracted {len(rune_lines)} lines of runes.")
        else:
            print(f"Page {page_num:02d}: No runes found.")

if __name__ == "__main__":
    extract_content()

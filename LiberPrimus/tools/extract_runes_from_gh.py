
import re
import os

SOURCE_FILE = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\reference\transcripts\github_liber_primus.md"
PAGES_DIR = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"

def extract():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: {SOURCE_FILE} not found.")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into sections based on H1 (#) or H2 (##)
    # The file has "# LP1", "# LP2" and "## XX.jpg"
    # We want to split by "## " mainly.
    
    sections = re.split(r'\n## ', content)
    
    print(f"Found {len(sections)} sections.")
    
    for section in sections:
        # Extract page number from the first line (header)
        header_line = section.split('\n')[0]
        
        # Look for pattern like "00.jpg", "57.jpg"
        # Prioritize the FIRST number found before ".jpg"
        match = re.search(r'(\d+)\.jpg', header_line)
        if not match:
            continue
            
        page_num_str = match.group(1)
        page_num = int(page_num_str)
        
        # Check for Runes:
        runes_match = re.search(r'Runes:\s*\n(.*?)(?:\n\n|\n[A-Za-z]+:)', section, re.DOTALL)
        if not runes_match:
            # Check for "The runes were not encrypted, and they read:"
            runes_match = re.search(r'read:\s*\n(.*?)(?:\n\n|\n[A-Za-z]+:)', section, re.DOTALL)
            
        if runes_match:
            raw_runes = runes_match.group(1)
            # Clean up indentation
            cleaned_lines = []
            for line in raw_runes.split('\n'):
                line = line.strip()
                if line:
                    cleaned_lines.append(line)
            
            cleaned_runes = '\n'.join(cleaned_lines)
            
            # Skip if it looks like English translation (e.g. "SOME WISDOM")
            # But the "Runes:" block usually contains runes OR transliterated text.
            # If it contains standard ASCII letters, it might be transliterated.
            # Convert transliterated to Runes? Or leave as is?
            # User wants "Runes". 
            # If the source has "SOME WISDOM", that's English.
            # Let's check for Runes characters.
            
            has_runes = any(ord(c) > 0x16A0 and ord(c) < 0x16F0 for c in cleaned_runes)
            
            target_dir = os.path.join(PAGES_DIR, f"page_{page_num:02d}")
            target_file = os.path.join(target_dir, "runes.txt")
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            # Write it
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_runes)
            
            print(f"Extracted runes for Page {page_num:02d}")
            
        else:
            # print(f"No runes found for Page {page_num:02d}")
            pass

if __name__ == "__main__":
    extract()

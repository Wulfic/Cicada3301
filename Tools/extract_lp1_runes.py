import re

def extract_runes():
    with open('temp_liber_primus.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract LP1 section
    lp1_match = re.search(r'# LP1\n(.*?)# LP2', content, re.DOTALL)
    if not lp1_match:
        print("LP1 section not found")
        return

    lp1_content = lp1_match.group(1)
    
    # Split by pages
    # Pages are marked by ## .. - XX.jpg or ## XX.jpg
    pages = re.split(r'## .*?(\d+)\.jpg', lp1_content)
    
    # pages[0] is intro text
    # pages[1] is page number, pages[2] is content, pages[3] is page number...
    
    page_data = {}
    
    for i in range(1, len(pages), 2):
        page_num = pages[i] # string "00", "01" etc
        page_content = pages[i+1]
        
        # Extract Runes block
        runes_match = re.search(r'Runes:\s*\n\s*((?:[^\n]+\n)+)', page_content)
        if runes_match:
            runes_text = runes_match.group(1).strip()
            # Clean up indentation
            lines = [line.strip() for line in runes_text.split('\n')]
            runes_clean = '\n'.join(lines)
            page_data[page_num] = runes_clean
        else:
            # Check for cleartext or other indicators
            if "**Key:** - (Written in cleartext.)" in page_content:
                 page_data[page_num] = "(Cleartext page - no runes)"
            elif "Decoding the runes on the page" in page_content:
                 page_data[page_num] = "(Runes present but not transcribed in source)"
            else:
                 page_data[page_num] = "(No runes found in source)"

    for num in sorted(page_data.keys()):
        print(f"--- Page {num} ---")
        print(page_data[num])
        print("------------------")

if __name__ == "__main__":
    extract_runes()

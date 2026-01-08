import re

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by level 2 headers (pages)
    sections = re.split(r'(^## .*)', content, flags=re.MULTILINE)
    
    pages = []
    
    current_page = None
    
    for section in sections:
        if section.startswith('## '):
            # This is a header
            header = section.strip()
            # Try to extract page number/name
            # Format usually "## Title - ##.jpg" or "## ##.jpg"
            match = re.search(r'(\d+)\.jpg', header)
            if match:
                current_page = {'number': match.group(1), 'header': header, 'content': ''}
                pages.append(current_page)
            else:
                current_page = None # Skip non-page sections like "## Introduction"
        elif current_page:
            current_page['content'] += section

    solved_pages = []

    for page in pages:
        content = page['content']
        
        # Look for "Key:"
        key_match = re.search(r'\*\*Key:\*\*(.*?)(?=\n)', content, re.IGNORECASE)
        key = key_match.group(1).strip() if key_match else "Unknown"
        
        # Look for English plaintext. 
        # It's often in a code block or just text.
        # Common markers in this repo: "Decrypted:", "Clartext:", "Translation:", or just English text after runes.
        # But we need to avoid extracting the Runes themselves.
        
        # Simple heuristic: Look for blocks that don't look like runes and OutGuess signatures.
        # Also, check if the Key says "Unsolved".
        
        if "unsolved" in key.lower():
            continue

        # Extracting likely english text is tricky without a specific format.
        # Let's dump the whole content for the user to see, or try to be smart.
        # I'll output the page number and a snippet of the content to helping me decide.
        
        solved_pages.append({
            'number': page['number'],
            'key': key,
            'excerpt': content[:500].replace('\n', ' ')
        })

    return solved_pages

results = analyze_file('people_liber_primus.md')
for res in results:
    print(f"Page {res['number']}: Key='{res['key']}'")
    print(f"Excerpt: {res['excerpt']}")
    print("-" * 20)

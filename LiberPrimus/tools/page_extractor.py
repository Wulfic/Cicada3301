"""
Liber Primus Page Extractor
Parses the runes text file and extracts content for each page.
"""

import os
import re
import shutil

# Path configuration
BASE_PATH = r"c:\Users\tyler\Repos\Cicada3301"
SOURCE_RUNES = os.path.join(BASE_PATH, "2014", "Liber Primus", "runes in text format.txt")
SOURCE_IMAGES = os.path.join(BASE_PATH, "2014", "Liber Primus", "liber primus images full")
OUTPUT_PATH = os.path.join(BASE_PATH, "LiberPrimus", "pages")

# Read the source file
with open(SOURCE_RUNES, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by page separator (%)
# Note: The text uses / for line breaks within pages
raw_pages = content.split('%')

# Clean up pages
pages = []
for i, page in enumerate(raw_pages):
    # Strip whitespace but preserve internal structure
    page = page.strip()
    if page:  # Skip empty pages
        pages.append({
            'number': i,
            'raw': page,
            'lines': [l for l in page.split('/') if l.strip()],
            'has_section_marker': '&' in page,
            'has_chapter_marker': '$' in page
        })

print(f"Found {len(pages)} pages")

# Analyze each page
for i, page in enumerate(pages):
    # Count runes (exclude formatting characters)
    rune_count = sum(1 for c in page['raw'] if c not in '-./&$%\n\r\t ')
    page['rune_count'] = rune_count
    
    # Check if it appears to be plaintext (readable without decryption)
    # Page 57 (The Parable) is known plaintext
    sample = page['raw'][:50].replace('-', ' ').replace('/', ' ')
    
    print(f"Page {page['number']:2d}: {rune_count:4d} runes, {len(page['lines']):2d} lines")

# Output page data
print("\n--- Page Details ---\n")
for page in pages[:10]:  # First 10 pages
    print(f"=== PAGE {page['number']} ===")
    print(f"Runes: {page['rune_count']}")
    print(f"Section markers: {page['has_section_marker']}")
    print(f"Chapter markers: {page['has_chapter_marker']}")
    print(f"Content preview: {page['raw'][:100]}...")
    print()

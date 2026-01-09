
import os

with open('LiberPrimus/reference/transcripts/runes_full.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# Pages seem to be separated by % or &
# Let's inspect potential separators
pages = content.split('%')
print(f"Number of sections split by '%': {len(pages)}")

# Let's preview the start of each section to identify them
for i, page in enumerate(pages):
    clean_page = page.strip().split('\n')[0][:50]
    print(f"Section {i}: {clean_page}")

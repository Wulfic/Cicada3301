
import os

path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_71\runes.txt"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize
parts = text.replace('\n', '•').replace(' ', '').split('•')
parts = [p for p in parts if p] # Remove empty

print(f"Total words: {len(parts)}")

w14_pos = 0
w60_pos = 0

current_pos = 0
for i, w in enumerate(parts):
    if i == 14:
        w14_pos = current_pos
    if i == 60:
        w60_pos = current_pos
    
    current_pos += len(w)

print(f"Word 14 starts at char index: {w14_pos}")
print(f"Word 60 starts at char index: {w60_pos}")
print(f"Distance: {w60_pos - w14_pos}")

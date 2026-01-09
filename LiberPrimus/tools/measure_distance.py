
import os

path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_71\runes.txt"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize
# Based on solve_page_71_patterns, we replaced \n with dot
parts = text.replace('\n', ' ').split(' ')
parts = [p for p in parts if p] # Remove empty

idx = 0
print(f"Total words: {len(parts)}")

w14_rune = ""
w60_rune = ""
w14_pos = 0
w60_pos = 0

current_pos = 0
for i, w in enumerate(parts):
    if i == 14:
        w14_pos = current_pos
        w14_rune = w
    if i == 60:
        w60_pos = current_pos
        w60_rune = w
    
    current_pos += len(w) # Note: We are ignoring space length in the count if the key skips spaces.
                           # If the key includes spaces, we need to count them.
                           # Cicada running keys usually skip spaces in the ciphertext but the key text might not?
                           # Usually Vigenere is done on the letters only.

print(f"Word 14 ({w14_rune}) starts at char index (ignoring spaces): {w14_pos}")
print(f"Word 60 ({w60_rune}) starts at char index (ignoring spaces): {w60_pos}")
print(f"Distance: {w60_pos - w14_pos}")


import os
from collections import Counter

# Page 0 Decrypted Runes (Indices)
# We need the indices, not the string, to be precise, or the string 'fleþ...'
# I will use the string representation I know.
PAGE_0_TEXT = """
welcuman-wylc-he-be-þas-word-uile-sec-an-heo-waron-hie-
fleþ-eall-uile-dœþ-scal-tyr-e-al-uile-warn-f-s-uile-fi-
sod-ic-eom-uile-uyd-nu-haþen-a-ic-
warn-f-s-uile-fi-sod-ic-eom-uile-uyd-nu-haþen-a-ic-
"""

# Mapping standard letters back to indices for the script if needed, 
# but for bigrams we can just use the characters if the hill climber uses characters.
# The hill climber decrypts to INDICES, then converts to LETTERS.
# So I should generate bigrams of INDICES or LETTERS.
# The current hill climber converts to LETTERS 'TH', 'F' etc.
# My PAGE_0_TEXT uses 'þ', 'œ' etc.
# I need to align them.
# The hill climber uses `IDX_TO_LETTER` = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

# I should map 'þ' -> 'TH', 'œ' -> 'OE', 'ea' -> 'EA', 'eo' -> 'EO', 'ia' -> 'IO'? No, 'ia' is 'IO' in that list?
# Let's check `IDX_TO_LETTER` again in hill_climb_decrypt.py
# 27: 'IO', 28: 'EA'.
# My TRANS_MAP in apply_mined_keys.py: 27: 'ia', 28: 'ea'.
# So 'ia' in my text is 'IO' in Hill Climber.

RUNE_MAP_REV = {
    'f': 0, 'u': 1, 'þ': 2, 'o': 3, 'r': 4, 'c': 5, 'g': 6, 'w': 7,
    'h': 8, 'n': 9, 'i': 10, 'j': 11, 'eo': 12, 'p': 13, 'x': 14, 's': 15,
    't': 16, 'b': 17, 'e': 18, 'm': 19, 'l': 20, 'ŋ': 21, 'œ': 22, 'd': 23,
    'a': 24, 'æ': 25, 'y': 26, 'ia': 27, 'ea': 28
}

IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

def generate_profile():
    # Parse Page 0 text into indices
    indices = []
    i = 0
    clean_text = PAGE_0_TEXT.replace('\n', '').replace(' ', '')
    # Need to handle multi-char runes 'eo', 'ea', 'ia', 'oe' (œ is single char in python string usually but input might vary)
    # My text uses 'eo', 'ea', 'œ'.
    # I'll tokenize carefully.
    
    # Simple tokenizer
    tokens = []
    cur = 0
    while cur < len(clean_text):
        if clean_text[cur] == '-':
            cur += 1
            continue
            
        # Try 2-char runes first
        if cur + 2 <= len(clean_text) and clean_text[cur:cur+2] in RUNE_MAP_REV:
            tokens.append(RUNE_MAP_REV[clean_text[cur:cur+2]])
            cur += 2
        elif clean_text[cur] in RUNE_MAP_REV:
            tokens.append(RUNE_MAP_REV[clean_text[cur]])
            cur += 1
        else:
            # Skip unknown or spaces
            cur += 1
            
    # Convert to letters used by Hill Climber
    letters = [IDX_TO_LETTER[x] for x in tokens]
    
    # Generate Bigrams
    bigrams = []
    for j in range(len(letters)-1):
        bigrams.append(letters[j] + letters[j+1]) # Concatenate e.g. "THEA" or "FEO"?
        # NO, the hill climber uses bigrams of the LETTERS.
        # But 'TH' is one letter in the climber.
        # So "TH" + "E" = "THE".
        # I should just use the list of symbols.
    
    # Actually the Hill Climber joins them?
    # No, BIGRAM_SCORES keys are like 'TH', 'HE'.
    # 'TH' in bigrams usually means T followed by H.
    # But here 'TH' is a single symbol.
    # So valid bigrams are pairs of SYMBOLS.
    # E.g. (TH, E) -> "THE". (F, L) -> "FL".
    
    # Wait, the current hill climber uses `letters` string?
    # Let's check the code: `letters = "".join([IDX_TO_LETTER[x] for x in plain])`
    # `IDX_TO_LETTER` entries are STRINGS.
    # So `[2, 18]` -> `['TH', 'E']` -> `"THE"`.
    # Then it does `counts = Counter(letters[i:i+2] for i in range(len(letters)-1))`
    # So it counts CHARACTERS bigrams in the expanded string.
    # So 'THE' becomes 'TH', 'HE'.
    # This is fine for 'TH' symbol becoming 'T'+'H'.
    # But wait, 'TH' symbol is ONE RUNE.
    # If I score 'T'+'H', I am scoring the *transliteration*.
    # That is what the script does.
    
    # So I just need to generate the bigram frequencies of the EXPANDED STRING of Page 0.
    
    expanded_text = "".join(letters)
    bigram_counts = Counter(expanded_text[k:k+2] for k in range(len(expanded_text)-1))
    
    print("NEW_BIGRAM_SCORES = {")
    total = sum(bigram_counts.values())
    for bg, count in bigram_counts.most_common(50):
        # Normalize to 0-100 or similar
        score = int((count / total) * 1000)
        print(f"    '{bg}': {score},")
    print("}")

if __name__ == "__main__":
    generate_profile()

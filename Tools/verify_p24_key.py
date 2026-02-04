"""
Verify how P24_KEY was derived from Page 24 runes
"""

# Rune to index mapping (Gematria Primus order)
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

# P24_KEY from p20_comprehensive_attack.py
P24_KEY = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 
           15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 
           11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 
           22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 
           15, 13, 15]

print(f"P24_KEY has {len(P24_KEY)} values")

# Load Page 24 runes
with open("LiberPrimus/pages/page_24/runes.txt", 'r', encoding='utf-8') as f:
    p24_raw = f.read()

# Extract just the runes (no punctuation, spaces, newlines)
p24_runes = [c for c in p24_raw if c in RUNE_TO_IDX]
p24_indices = [RUNE_TO_IDX[c] for c in p24_runes]

print(f"Page 24 has {len(p24_runes)} runes")
print(f"\nFirst 83 runes of P24 converted to indices:")
print(p24_indices[:83])

print(f"\nP24_KEY:")
print(P24_KEY)

print(f"\nDo they match? {p24_indices[:83] == P24_KEY}")

# Check if there's any transformation
print("\n--- Checking possible transformations ---")

# Direct match?
matches = sum(1 for a, b in zip(p24_indices[:83], P24_KEY) if a == b)
print(f"Direct matches: {matches}/83")

# Reversed?
matches_rev = sum(1 for a, b in zip(p24_indices[:83], P24_KEY[::-1]) if a == b)
print(f"Reversed matches: {matches_rev}/83")

# Offset?
for offset in range(29):
    transformed = [(i + offset) % 29 for i in p24_indices[:83]]
    matches = sum(1 for a, b in zip(transformed, P24_KEY) if a == b)
    if matches > 10:
        print(f"Offset {offset}: {matches}/83 matches")

# Maybe P24_KEY is from a different source?
print("\n--- Checking if P24_KEY comes from the 166 stream ---")

STREAM_166 = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Single char to index
GP_MAP = {'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9, 
          'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 
          'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28}

single_gp = {k: v for k, v in GP_MAP.items() if len(k) == 1}
stream_indices = [single_gp[c] for c in STREAM_166 if c in single_gp]
print(f"166 stream has {len(stream_indices)} single-char indices")

# Check pair sums
pair_sums = [(stream_indices[i] + stream_indices[i+1]) % 29 for i in range(0, 166, 2)]
print(f"\nPair sums (first 83 positions):")
print(pair_sums[:30])

# Is P24_KEY used to decrypt pair_sums?
decrypted = [(p - k) % 29 for p, k in zip(pair_sums, P24_KEY)]
print(f"\nPair-sum - P24_KEY:")
print(decrypted[:30])

# Convert to runeglish
INV_MAP = {v: k for k, v in GP_MAP.items()}
result_text = "".join(INV_MAP[n] for n in decrypted)
print(f"\nDecrypted text: {result_text}")

# Check what words appear
import re
print("\n--- Word finding ---")
for word in ['DEAD', 'REAPER', 'AEON', 'DIAG', 'MEAN', 'SIX', 'THE']:
    if word in result_text:
        idx = result_text.find(word)
        print(f"Found '{word}' at position {idx}")

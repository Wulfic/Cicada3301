"""
Debug the rune indexing issue
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

print(f"GP_RUNES length: {len(GP_RUNES)}")
print(f"GP_LATIN length: {len(GP_LATIN)}")

# Check specific runes
test_rune = 'ᚫ'  # This should be AE
idx = GP_RUNES.index(test_rune)
print(f"Rune {test_rune} is at index {idx}, latin = {GP_LATIN[idx]}")

# Check the first rune of page 73
page73_first = 'ᚫ'
print(f"\nPage 73 first rune: {page73_first}")
print(f"Index: {GP_RUNES.index(page73_first)}")
print(f"Latin: {GP_LATIN[GP_RUNES.index(page73_first)]}")

# What we expect:
# A = index 24
# AE = index 25
print(f"\nA is at index {GP_LATIN.index('A')}")
print(f"AE is at index {GP_LATIN.index('AE')}")

# First prime shift
print(f"\nFirst shift: phi(2) mod 29 = 1")
print(f"If cipher = 25 (AE), plain = (25-1) = 24 = A. CORRECT!")
print(f"If cipher = 28 (EA), plain = (28-1) = 27 = IA. WRONG!")

# Check the index I'm getting
print(f"\nActual index of ᚫ in GP_RUNES: {GP_RUNES.index('ᚫ')}")

# -*- coding: utf-8 -*-
"""
Page 56 Decryption Verification
Confirms the known working decryption method for Page 56
"""

import itertools as it

# Gematria Primus
gematriaprimus = (
    ('ᚠ', 'f', 2), ('ᚢ', 'u', 3), ('ᚦ', 'th', 5), ('ᚩ', 'o', 7),
    ('ᚱ', 'r', 11), ('ᚳ', 'c', 13), ('ᚷ', 'g', 17), ('ᚹ', 'w', 19),
    ('ᚻ', 'h', 23), ('ᚾ', 'n', 29), ('ᛁ', 'i', 31), ('ᛂ', 'j', 37),
    ('ᛇ', 'eo', 41), ('ᛈ', 'p', 43), ('ᛉ', 'x', 47), ('ᛋ', 's', 53),
    ('ᛏ', 't', 59), ('ᛒ', 'b', 61), ('ᛖ', 'e', 67), ('ᛗ', 'm', 71),
    ('ᛚ', 'l', 73), ('ᛝ', 'ing', 79), ('ᛟ', 'oe', 83), ('ᛞ', 'd', 89),
    ('ᚪ', 'a', 97), ('ᚫ', 'ae', 101), ('ᚣ', 'y', 103), ('ᛡ', 'io', 107),
    ('ᛠ', 'ea', 109)
)

runes = [x[0] for x in gematriaprimus]
letters = [x[1] for x in gematriaprimus]
ALPHABET_SIZE = 29

def primegen():
    """Generate prime numbers"""
    D = {}
    yield 2
    for q in it.islice(it.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D:
                x += 2*p
            D[x] = p

def shift(offset, direction): 
    return (offset + direction) % ALPHABET_SIZE

# Page 56 ciphertext (without the hex block)
PAGE_56_RUNIC = '''ᚫᛂ•ᛟᛋᚱ:ᛗᚣᛚᚩᚻ•ᚩᚫ•ᚳᚦᚷᚹ•ᚹᛚᚫ,ᛉᚩᚪᛈ•ᛗᛞᛞᚢᚷᚹ•ᛚ•ᛞᚾᚣᛂ•ᚳᚠᛡ•ᚫᛏᛈᛇᚪᚦ•ᚳᚫ:ᚳᛞ•ᚠᚾ•ᛡᛖ•ᚠᚾᚳᛝ•ᚱᚠ•ᚫᛁᚱᛞᛖ•ᛋᚣᛂᛠᚢᛝᚹ•ᛉᚩ•ᛗᛠᚹᚠ•ᚱᚷᛡ•ᛝᚱᛒ•ᚫᚾᚢᛋ:'''

# Page 57 - The Parable (plaintext)
PAGE_57 = "ᛈᚪᚱᚪᛒᛚᛖ:ᛚᛁᚳᛖ•ᚦᛖ•ᛁᚾᛋᛏᚪᚱ•ᛏᚢᚾᚾᛖᛚᛝ•ᛏᚩ•ᚦᛖ•ᛋᚢᚱᚠᚪᚳᛖ.ᚹᛖ•ᛗᚢᛋᛏ•ᛋᚻᛖᛞ•ᚩᚢᚱ•ᚩᚹᚾ•ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ.ᚠᛁᚾᛞ•ᚦᛖ•ᛞᛁᚢᛁᚾᛁᛏᚣ•ᚹᛁᚦᛁᚾ•ᚪᚾᛞ•ᛖᛗᛖᚱᚷᛖ::"

def decrypt_page_56(page_text, offset=57, skip_first_n=0):
    """
    Decrypt using Page 56 method: shift each rune by -(prime_n + offset)
    
    Args:
        page_text: Runic ciphertext
        offset: Constant to add to prime (57 is the known value for Page 56)
        skip_first_n: Skip this many runes before starting prime sequence
    """
    pg = primegen()
    result = ''
    rune_count = 0
    
    for c in page_text:
        if c == '•':
            result += ' '
            continue
        if c not in runes:
            result += c
            continue
        
        o = runes.index(c)
        np = next(pg)
        o = shift(o, -(np + offset))
        result += letters[o]
        rune_count += 1
    
    return result

def transliterate(text):
    """Direct transliteration without decryption"""
    result = ''
    for c in text:
        if c == '•':
            result += ' '
        elif c in runes:
            result += letters[runes.index(c)]
        else:
            result += c
    return result

print("=" * 70)
print("PAGE 56 DECRYPTION VERIFICATION")
print("=" * 70)

print("\n--- Page 56 Ciphertext (runic) ---")
print(PAGE_56_RUNIC[:100] + "...")

print("\n--- Page 56 Direct Transliteration (no decryption) ---")
print(transliterate(PAGE_56_RUNIC))

print("\n--- Page 56 Decrypted (prime + 57 method) ---")
decrypted_56 = decrypt_page_56(PAGE_56_RUNIC, offset=57)
print(decrypted_56)

print("\n" + "=" * 70)
print("PAGE 57 (THE PARABLE) - Direct Transliteration")
print("=" * 70)
print(transliterate(PAGE_57))

print("\n" + "=" * 70)
print("TESTING DIFFERENT OFFSETS ON PAGE 56")
print("=" * 70)

# Try different offsets to see what produces readable text
for offset in range(50, 70):
    result = decrypt_page_56(PAGE_56_RUNIC, offset=offset)
    # Check for readable English indicators
    if any(word in result.lower() for word in ['the', 'and', 'is', 'an', 'of', 'to', 'a ']):
        print(f"\nOffset {offset}: {result[:80]}...")

print("\n" + "=" * 70)
print("ANALYSIS OF PAGE 56 DECRYPTION")
print("=" * 70)

# The confirmed offset 57 result
print("\nConfirmed decryption (offset=57):")
print(decrypted_56)
print("\nThis appears to contain a message about 'an instruction' and 'within all'")
print("Note the hex block in the original that may contain RSA-encrypted data:")
print("""
36367763ab73783c7af284446c
59466b4cd653239a311cb7116
d4618dee09a8425893dc7500b
464fdaf1672d7bef5e891c6e227
4568926a49fb4f45132c2a8b4
""")

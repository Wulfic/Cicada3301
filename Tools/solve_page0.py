
import collections

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
# Inverse map
IDX_TO_RUNE = {v: k for k, v in RUNE_MAP.items()}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

LETTER_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

RUNES = """
ᛋᚻᛖᚩᚷᛗᛡᚠ-ᛋᚣᛖᛝᚳ.ᚦᛄᚷᚫ-ᚠᛄᛟ-

ᚩᚾᚦ-ᚾᛖᚹᛒᚪᛋᛟᛇᛁᛝᚢ-ᚾᚫᚷᛁᚦ-ᚻᛒᚾᛡ-

ᛈᛒᚾ-ᛇᛄᚦ-ᚪᛝᚣᛉ-ᛒᛞᛈ-ᛖᛡᚠᛉᚷᚠ-

ᛋᛈᛏᚠᛈᚢᛝᚣᛝᛉᛡ-ᚣᚻ-ᛒᚢ-ᚷᚩᛈ-ᛝᚫᚦ-ᛁ

ᚫᚻᛉᚦᛈᚷ-ᚣᚠᛝᚳᛄ-ᚦᚪᛗᛁᛝᛁᛡᚣ-ᚻᛇ-ᛏᚻᚫ

ᛡ-ᛉᚣ-ᛖᚢᛝ-ᚳᚠᚾ-ᛇᚦᛄᛁᚦ-ᚦᛈ-ᚣᛝᛠ-ᚣᚾ

ᛖᚣ-ᛞᛉᛝᚹ-ᛒᚳᛉᛞᛒᚠ-ᛗᛏᚾᛖ-ᛠᛄᚾᛚᚷ

ᛒ-ᛉᚷᚦ.ᚣᛁᛞᚪ-ᛝᚷᛗᛄᚱᚩᛚᛇ-ᚣᛏᛈᛁᚦᛞᛄ-

ᛟᚻᛚ-ᛠ-ᚠᛉᚫᛈᚷᛉ-ᚠᛚᚹᛇᛏᚫ-ᚠᚷᚾ-ᛗᛇᛚᚾ-

ᛝᛗᚠᚱᛡ-ᚪᛋ-ᛠᛗᛝᛉᛉᛇᛞᛒ-ᛟᛞᛗᚩ-ᛠ

ᛇᚻ-ᛞᛝᚷ-ᛟᛝᛚᚢᚱᚾᛏ-ᚫᛋᚣᚢᚻᚱᛏ-ᚻᚳ-ᛋᛟ

ᛏᛟᛝᚢᚱ-ᛋ-ᚠᚩᛖᚹᛠᛟᛚᚠᚫ-ᛗᚱᛝ-ᛞᚪᛗᚱ-ᚹ
"""

def parse_runes(text):
    return [RUNE_MAP[c] for c in text if c in RUNE_MAP]

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def autokey_decrypt(cipher_indices, primer_indices):
    plain = []
    
    for i in range(len(cipher_indices)):
        if i < len(primer_indices):
            key = primer_indices[i]
        else:
            key = plain[i - len(primer_indices)]
        
        plain_char = (cipher_indices[i] - key) % 29
        plain.append(plain_char)
    return plain

def vigenere_decrypt(cipher_indices, key_indices):
    plain = []
    key_len = len(key_indices)
    for i in range(len(cipher_indices)):
        key = key_indices[i % key_len]
        plain_char = (cipher_indices[i] - key) % 29
        plain.append(plain_char)
    return plain

def score_text(text):
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'ANY', 'CAN', 'HAD', 'HAS', 'HIM', 'HIS', 'HOW', 'INK', 'MAN', 'MAY', 'NEW', 'NOW', 'OLD', 'ONE', 'OUT', 'PUT', 'RUN', 'SAY', 'SEE', 'SHE', 'SIT', 'SON', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'WHY', 'YES', 'YET']
    score = 0
    upper_text = text.upper()
    for word in common_words:
        score += upper_text.count(word) * len(word)
    return score

def main():
    cipher = parse_runes(RUNES)
    print(f"Loaded {len(cipher)} runes.")

    primers = {
        "IP (Indices 10,13)": [10, 13],
        "PI (Indices 13,10)": [13, 10],
        "PI Digits (3,1,4,1,5)": [3, 1, 4, 1, 5],
        "THE": [16, 8, 18],     # T,H,E letters are indices 16, 18? No. 
                                # T=16, H=8, E=18. Wait. T is 16. H is 8. E is 18.
                                # But "TH" is a rune (2). So, is the primer runes or letters?
                                # Usually primer is Runes. 
                                # If primer is "THE", is it Rune(TH) Rune(E)? -> [2, 18]
                                # Or Rune(T) Rune(H) Rune(E)? -> [16, 8, 18]
        "TH-E (Runes 2,18)": [2, 18],
        "Key 113 (First 5)": [19, 6, 23, 16, 10]
    }

    print("\n--- Autokey Decryption Attempts ---")
    for name, primer in primers.items():
        decrypted = autokey_decrypt(cipher, primer)
        text = indices_to_text(decrypted)
        sc = score_text(text)
        print(f"Primer: {name}")
        print(f"Score: {sc}")
        print(f"Preview: {text[:60]}")
        print("-" * 40)
        
    print("\n--- Interleave Analysis of Runes ---")
    # Check every Nth char
    for n in range(2, 6):
        extracted = cipher[::n]
        text = indices_to_text(extracted)
        print(f"Skip {n}: {text[:60]}")

if __name__ == "__main__":
    main()

import os
import sys

# P20 extracted key (IoC 1.14 stream)
# Length 49
KEY_ORIGINAL = "YEOTJEOBJSGOXAEOUIWEEOHSHCHELTFFXENGMHETHEAAEWTHFJIAHEAJYFCN"
KEY_ATBASH   = "THTEOBTJBPOEAEXOAEIAENGITLPLDLIHEOEAEAXIWNLIYFONGYEABULFBTHEADM"

def get_rune_map():
    return {
        'ᚠ':0, 'ᚢ':1, 'ᚦ':2, 'ᚩ':3, 'ᚱ':4, 'ᚳ':5, 'ᚷ':6, 'ᚹ':7, 'ᚻ':8, 'ᚾ':9, 'ᛁ':10, 'ᛄ':11, 'ᛇ':12,
        'ᛈ':13, 'ᛉ':14, 'ᛋ':15, 'ᛏ':16, 'ᛒ':17, 'ᛖ':18, 'ᛗ':19, 'ᛚ':20, 'ᛝ':21, 'ᛟ':22, 'ᛞ':23, 'ᚪ':24,
        'ᚫ':25, 'ᚣ':26, 'ᛡ':27, 'ᛠ':28
    }

def get_ascii_map():
    return {
        'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
        'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
        'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }

def get_inv_map():
    return {v: k for k, v in get_ascii_map().items()}

def to_int(text):
    gem = get_ascii_map()
    res = []
    i = 0
    while i < len(text):
        if i + 2 <= len(text) and text[i:i+2] in gem:
            res.append(gem[text[i:i+2]])
            i += 2
        elif text[i] in gem:
            res.append(gem[text[i]])
            i += 1
        else:
            i += 1
    return res

def to_str(nums):
    inv = get_inv_map()
    return "".join([inv.get(n, "?") for n in nums])

def get_p18_runes():
    path = "LiberPrimus/pages/page_18/runes.txt"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    gem = get_rune_map()
    res = []
    for char in content:
        if char in gem:
            res.append(gem[char])
    return res

def calc_ioc(nums):
    if not nums: return 0
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    num = 0.0
    for k in counts:
        num += counts[k] * (counts[k] - 1)
    den = len(nums) * (len(nums) - 1)
    if den == 0: return 0
    return num / den * 29.0

def decrypt_vigenere(cipher, key, mode=0):
    res = []
    L = len(key)
    for i, c in enumerate(cipher):
        k = key[i % L]
        if mode == 0: # C - K
            p = (c - k) % 29
        elif mode == 1: # C + K
            p = (c + k) % 29
        elif mode == 2: # K - C
            p = (k - c) % 29
        res.append(p)
    return res

def main():
    p18 = get_p18_runes()
    print(f"P18 Total Runes: {len(p18)}")
    
    p18_part2 = p18[53:]
    print(f"P18 Part 2 (Runes 53 onwards): {len(p18_part2)}")
    
    keys = {
        "ORIGINAL": to_int(KEY_ORIGINAL),
        "ATBASH": to_int(KEY_ATBASH)
    }
    
    # Generate Columnar versions (7x7)
    def to_cols(k_nums):
        if len(k_nums) != 49: return k_nums
        grid = []
        for r in range(7):
            grid.append(k_nums[r*7 : (r+1)*7])
        cols = []
        for c in range(7):
            for r in range(7):
                cols.append(grid[r][c])
        return cols

    keys["ORIGINAL_COLS"] = to_cols(keys["ORIGINAL"])
    keys["ATBASH_COLS"] = to_cols(keys["ATBASH"])
    
    modes = ["C - K", "C + K", "K - C"]
    
    print("\n--- Trying to decrypt P18 Part 2 ---")
    
    for k_name, k_nums in keys.items():
        print(f"\nKey: {k_name}")
        for m_idx, m_name in enumerate(modes):
            dec = decrypt_vigenere(p18_part2, k_nums, m_idx)
            ioc = calc_ioc(dec)
            print(f"  Mode {m_name}: IoC {ioc:.4f}")
            if ioc > 1.1:
                print(f"  --> HIGH IoC! Text: {to_str(dec[:50])}")

    print("\n--- Reversed Keys ---")
    for k_name, k_nums in keys.items():
        k_rev = k_nums[::-1]
        print(f"\nKey: {k_name} (REV)")
        for m_idx, m_name in enumerate(modes):
            dec = decrypt_vigenere(p18_part2, k_rev, m_idx)
            ioc = calc_ioc(dec)
            print(f"  Mode {m_name}: IoC {ioc:.4f}")
            if ioc > 1.1:
                print(f"  --> HIGH IoC! Text: {to_str(dec[:50])}")

if __name__ == "__main__":
    main()

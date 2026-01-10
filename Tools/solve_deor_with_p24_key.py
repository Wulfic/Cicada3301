
import sys

# Deor Stream (166 runes)
STREAM_STR = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Page 24 Key (83 ints)
KEY_83 = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 15, 13, 15]

# GP Map
GP = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
    'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
    'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}
GP_INV = {v: k for k, v in GP.items()}

def to_ints(text):
    res = []
    # Treat each char as individual rune if possible.
    # Note: GP has DIGRAPHS which might conflict.
    # We want 'T' and 'H', not 'TH'.
    # GP keys are varying length.
    single_gp = {k: v for k, v in GP.items() if len(k) == 1}
    
    for char in text:
        if char in single_gp:
            res.append(single_gp[char])
        else:
            # Handle unknown? Skip?
            # Or assume text has English letters that are not in GP single?
            # 'Q', 'V', 'K'?
            # GP has 'K'->5? 'V'->1?
            # Let's use a broader map if needed or just skip.
            pass
            
    return res

def to_str(nums):
    return "".join([GP_INV[n] for n in nums])

def main():
    stream_nums = to_ints(STREAM_STR)
    print(f"Stream Nums Length: {len(stream_nums)}")
    
    # Extend Key to match stream
    key_extended = KEY_83 * (len(stream_nums) // len(KEY_83) + 1)
    key = key_extended[:len(stream_nums)]
    
    print("\n--- Attempt 1: Stream - Key ---")
    dec1 = [(s - k) % 29 for s, k in zip(stream_nums, key)]
    print(to_str(dec1))
    
    print("\n--- Attempt 2: Key - Stream (Beaufort) ---")
    dec2 = [(k - s) % 29 for s, k in zip(stream_nums, key)]
    print(to_str(dec2))
    
    print("\n--- Attempt 3: Stream + Key ---")
    dec3 = [(s + k) % 29 for s, k in zip(stream_nums, key)]
    print(to_str(dec3))
    
    print("\n--- Attempt 4: Reverse Key ---")
    key_rev = GP_INV
    # No, reverse the key array
    key_r = KEY_83[::-1]
    key_r_ext = key_r * 2
    key_r = key_r_ext[:len(stream_nums)]
    
    dec4 = [(s - k) % 29 for s, k in zip(stream_nums, key_r)]
    print(to_str(dec4))

if __name__ == "__main__":
    main()

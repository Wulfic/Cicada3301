
import sys

STREAM_STR = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# Page 24 Key (83 ints)
KEY_83 = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 15, 13, 15]

GP = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
    'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
    'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}
GP_INV = {v: k for k, v in GP.items()}

def to_ints(text):
    single_gp = {k: v for k, v in GP.items() if len(k) == 1}
    res = []
    for char in text:
        if char in single_gp:
            res.append(single_gp[char])
        else:
            # Handle unknown
            pass
    return res

def to_str(nums):
    return "".join([GP_INV[n] for n in nums])

def main():
    nums = to_ints(STREAM_STR)
    print(f"Original Length: {len(nums)}")
    
    # Compress Pairs
    pairs = []
    for i in range(0, len(nums), 2):
        if i+1 < len(nums):
            # Sum mod 29
            val = (nums[i] + nums[i+1]) % 29
            pairs.append(val)
            
    print(f"Compressed Length: {len(pairs)}")
    print(f"Pair Preview: {to_str(pairs)[:50]}")
    
    # Try Applying Key to Pairs
    # Cipher = Pairs? Key = KEY_83?
    
    print("\n--- Pairs - Key ---")
    dec1 = [(p - k) % 29 for p, k in zip(pairs, KEY_83)]
    print(to_str(dec1))
    
    print("\n--- Key - Pairs (Beaufort) ---")
    dec2 = [(k - p) % 29 for p, k in zip(pairs, KEY_83)]
    print(to_str(dec2))
    
    print("\n--- Pairs + Key ---")
    dec3 = [(p + k) % 29 for p, k in zip(pairs, KEY_83)]
    print(to_str(dec3))
    
    # Try Diff
    pair_diff = []
    for i in range(0, len(nums), 2):
        if i+1 < len(nums):
            val = (nums[i] - nums[i+1]) % 29
            pair_diff.append(val)
            
    print("\n--- Diff Pairs - Key ---")
    dec4 = [(p - k) % 29 for p, k in zip(pair_diff, KEY_83)]
    print(to_str(dec4))
    
    print("\n--- Key - Diff Pairs (Beaufort) ---")
    dec5 = [(k - p) % 29 for p, k in zip(pair_diff, KEY_83)]
    print(to_str(dec5))

if __name__ == "__main__":
    main()

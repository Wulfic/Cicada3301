import os
import sys

# Add . to path
sys.path.append(".")

# Key candidates derived from P20 Primes
KEY_ORIGINAL = "YEOTJEOBJSGOXAEOUIWEEOHSHCHELTFFXENGMHETHEAAEWTHFJIAHEAJYFCN"
# Atbash of Key
KEY_ATBASH   = "THTEOBTJBPOEAEXOAEIAENGITLPLDLIHEOEAEAXIWNLIYFONGYEABULFBTHEADM"

def get_gp_map():
    return {
        'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
        'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
        'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21,
        'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
    }

def get_inv_map():
    return {v: k for k, v in get_gp_map().items()}

def to_int(text):
    gem = get_gp_map()
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

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def get_p20_runes():
    # Load from file if possible, or hardcode/reference
    # Using existing tool style: load from LiberPrimus/pages/page_20/runes.txt if exists
    path = "LiberPrimus/pages/page_20/runes.txt"
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse character by character for runes
    gem = {
        'ᚠ':0, 'ᚢ':1, 'ᚦ':2, 'ᚩ':3, 'ᚱ':4, 'ᚳ':5, 'ᚷ':6, 'ᚹ':7, 'ᚻ':8, 'ᚾ':9, 'ᛁ':10, 'ᛄ':11, 'ᛇ':12,
        'ᛈ':13, 'ᛉ':14, 'ᛋ':15, 'ᛏ':16, 'ᛒ':17, 'ᛖ':18, 'ᛗ':19, 'ᛚ':20, 'ᛝ':21, 'ᛟ':22, 'ᛞ':23, 'ᚪ':24,
        'ᚫ':25, 'ᚣ':26, 'ᛡ':27, 'ᛠ':28
    }
    
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
    return num / den * 29.0 # Normalized for 29

def decrypt(cipher_nums, key_nums):
    res = []
    for i, c in enumerate(cipher_nums):
        k = key_nums[i % len(key_nums)]
        p = (c - k) % 29
        res.append(p)
    return res

def main():
    p20_full = get_p20_runes()
    print(f"P20 Total Runes: {len(p20_full)}")
    
    # Extract Composites (Indices that are NOT prime)
    # Using 0-based index? Or 1-based?
    # Usual Cicada prime index is 2, 3, 5, 7... so based on 0,1,2,3...
    # Let's assume 0-based for now.
    
    composites = []
    for i in range(len(p20_full)):
        if not is_prime(i):
            composites.append(p20_full[i])
            
    print(f"P20 Composite Runes: {len(composites)}")
    
    keys = {
        "ORIGINAL": to_int(KEY_ORIGINAL),
        "ATBASH": to_int(KEY_ATBASH)
    }
    
    print("\n--- Testing P20 Composites Decryption ---")
    
    for name, k_nums in keys.items():
        print(f"\nKey: {name} (Len {len(k_nums)})")
        
        # Plain Decrypt
        dec = decrypt(composites, k_nums)
        ioc = calc_ioc(dec)
        print(f"  Standard Decrypt IoC: {ioc:.4f}")
        if ioc > 1.1:
            print(f"  High IoC! Preview: {to_str(dec[:50])}")
            
        # Reversed Key
        dec_rev = decrypt(composites, k_nums[::-1])
        ioc_rev = calc_ioc(dec_rev)
        print(f"  Reversed Key IoC: {ioc_rev:.4f}")
        
    print("\n--- Testing P20 FULL Decryption (Just in case) ---")
    for name, k_nums in keys.items():
        dec = decrypt(p20_full, k_nums)
        ioc = calc_ioc(dec)
        print(f"Key: {name} -> P20 Full IoC: {ioc:.4f}")

if __name__ == "__main__":
    main()

import sys
import os

# 166 Runes from Deor
stream_runes = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# The Working Key from solve_deor_pairs.py (P24 Dots Key?)
key_p24 = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 15, 13, 15]


# GP Mapping
GP = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
val_map = {r: i for i, r in enumerate(GP)}
inv_map = {i: r for i, r in enumerate(GP)}

# Force Single Char Parsing (ignore digraphs in input stream to maintain 166 count)
def to_ints_force_single(text):
    single_gp = {k: v for k, v in val_map.items() if len(k) == 1}
    res = []
    for char in text:
        if char in single_gp:
            res.append(single_gp[char])
        else:
            # If char not in single_gp (e.g. 'Z' or 'V' if they were there), skip or map closest?
            # Our stream is clean "HOE..."
            pass
    return res

stream_ints = to_ints_force_single(stream_runes)
print(f"Stream Ints Length: {len(stream_ints)}")

def solve(op_name, op_func):
    res_str = ""
    res_ints = []
    
    # Process pairs
    # We step by 2: (0,1), (2,3), ...
    for k in range(len(key_p24)):
        idx = k * 2
        if idx+1 >= len(stream_ints): break
        
        a = stream_ints[idx]
        b = stream_ints[idx+1]
        
        # Operation on Pair
        val_pair = op_func(a, b)
        
        # Apply Key (Subtract Key is standard Vigenere/Beaufort logic)
        final = (val_pair - key_p24[k]) % 29
        res_ints.append(final)
        res_str += inv_map[final] # Note: inv_map can return digraphs like 'TH', 'EO'
        
    print(f"[{op_name}] (len {len(res_ints)}): {res_str}")
    return res_str

print("-" * 40)
solve("Sum(A+B) - Key", lambda a, b: (a + b))
solve("Diff(A-B) - Key", lambda a, b: (a - b))
solve("Diff(B-A) - Key", lambda a, b: (b - a))
print("-" * 40)


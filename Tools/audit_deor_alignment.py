import sys

# Stream and Key
stream_runes = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"
key_p24 = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 15, 13, 15]

GP = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
val_map = {r: i for i, r in enumerate(GP)}
inv_map = {i: r for i, r in enumerate(GP)}

def to_ints_force_single(text):
    single_gp = {k: v for k, v in val_map.items() if len(k) == 1}
    res = []
    for char in text:
        if char in single_gp:
            res.append(single_gp[char])
    return res

stream_ints = to_ints_force_single(stream_runes)

def get_pairs(offset=0):
    # Try different pairing alignments? 
    # Usually (0,1), (2,3).
    # What if we skip 1 char? (0), (1,2), (3,4)...
    # What if we skip 1 pair?
    ps = []
    i = offset
    while i < len(stream_ints) - 1:
        val = (stream_ints[i] + stream_ints[i+1]) % 29
        ps.append(val)
        i += 2
    return ps

def decrypt(pairs, key_shift=0, key_subset=None):
    # slide the key against the pairs
    res = ""
    k_len = len(key_p24)
    for i, p in enumerate(pairs):
        k_idx = (i + key_shift)
        if k_idx < 0 or k_idx >= k_len:
            res += "?"
            continue
        
        k = key_p24[k_idx]
        val = (p - k) % 29
        res += inv_map[val]
    return res

print(f"Original Length: {len(stream_ints)}")
raw_pairs = get_pairs(0)

print("\n--- Sliding Key Check (Desync detection) ---")
# If the text DEASIX... is correct at start, key_shift 0 is correct at start.
# If text turns into garbage at index X, maybe key needs to shift?

base_dec = decrypt(raw_pairs, 0)
print(f"Base: {base_dec}")

# Let's try to detect if a shift +1 or -1 makes sense LATER in the string
# We break the string into chunks and try shifts for each chunk
chunk_size = 10
for i in range(0, len(raw_pairs), chunk_size):
    chunk = raw_pairs[i:i+chunk_size]
    print(f"\nChunk {i}-{i+chunk_size}:")
    
    # Try offsets -2 to +2 relative to the base 'i'
    for delta in range(-2, 3):
        # We want key index to be i + delta
        # So we pass key_shift = delta relative to the chunk start logic?
        # No, decrypt takes global index.
        # We want to use key_p24[i + delta], key_p24[i+1 + delta]...
        
        # Manually decode chunk
        dec_chunk = ""
        for j, p in enumerate(chunk):
            real_idx = i + j
            k_idx = real_idx + delta
            if 0 <= k_idx < len(key_p24):
                val = (p - key_p24[k_idx]) % 29
                dec_chunk += inv_map[val]
            else:
                dec_chunk += "."
        
        validity = " "
        # Heuristic: count vowels?
        # vowels = set(['A','E','I','O','U','AE','EA','EO','OE','IA'])
        # cnt = sum(1 for x in dec_chunk if x in vowels) # rough
        
        print(f"  Shift {delta:+d}: {dec_chunk}")


print("\n--- Sliding Window on Input (Odd Index Pairing?) ---")
# Maybe (0), (1,2), (3,4)...
raw_pairs_off1 = get_pairs(1)
dec_off1 = decrypt(raw_pairs_off1, 0) # Key aligned to start of pairs
print(f"Offset 1 Pair: {dec_off1}")

print("\n--- Reverse Key? ---")
rev_key = list(reversed(key_p24))
res_rev = ""
for i, p in enumerate(raw_pairs):
    if i < len(rev_key):
        val = (p - rev_key[i]) % 29
        res_rev += inv_map[val]
print(f"RevKey: {res_rev}")

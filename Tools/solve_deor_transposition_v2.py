
import sys

STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

def rail_fence(text, num_rails):
    # This is decrypting Rail Fence (assuming text is ciphertext)
    # But usually creating rail fence splits plaintext.
    # To decrypt, we need to reconstruct the fence.
    rng = range(len(text))
    pos = sorted(rng, key=lambda i: (i % (2 * (num_rails - 1)), i))
    # Wait, simple rail fence pattern is 0, 1, 2... k-1, k-2... 1, 0, 1...
    
    fence = [[] for _ in range(num_rails)]
    rail = 0
    change = 1
    
    # Calculate lengths of each rail
    rails_len = [0] * num_rails
    for i in range(len(text)):
        rails_len[rail] += 1
        rail += change
        if rail == num_rails - 1 or rail == 0:
            change = -change
            
    # Distrib chars
    it = iter(text)
    grid = [[] for _ in range(num_rails)]
    for r in range(num_rails):
        for _ in range(rails_len[r]):
            grid[r].append(next(it))
            
    # Read off zig-zag
    res = []
    rail = 0
    change = 1
    processed_rails = [0] * num_rails
    
    for i in range(len(text)):
        res.append(grid[rail][processed_rails[rail]])
        processed_rails[rail] += 1
        rail += change
        if rail == num_rails - 1 or rail == 0:
            change = -change
            
    return "".join(res)

def skip_decode(text, n):
    # Read every nth character
    return text[::n]

def main():
    print(f"Stream: {STREAM[:50]}...")
    
    print("\n--- Rail Fence Decrypt ---")
    for r in range(2, 6):
        dec = rail_fence(STREAM, r)
        print(f"Rails {r}: {dec[:60]}")
        
    print("\n--- Skip Patterns ---")
    for n in range(2, 10):
        sk = skip_decode(STREAM, n)
        print(f"Skip {n}: {sk[:60]}")
        
    # Also check offsets
    print("\n--- Skip with Offsets (Period 2, 3) ---")
    for n in [2, 3]:
        for start in range(n):
            sk = STREAM[start::n]
            print(f"Skip {n} Offset {start}: {sk[:60]}")

if __name__ == "__main__":
    main()

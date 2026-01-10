
import sys
import os

# Create absolute path to Tools
sys.path.append(os.path.join(os.getcwd(), 'Tools'))

# We need to import the functions from attack_p20_deor_prime_key
# But that file is a script. We might need to copy the functions or import as module.
# Let's try importing.

try:
    import attack_p20_deor_prime_key as attack
except ImportError:
    print("Could not import attack tool.")
    sys.exit(1)

def main():
    # Re-run the extraction logic
    p20_runes = attack.get_p20_runes() # Using function from the module
    deor_runes = attack.get_deor_runes()
    
    p20_primes = attack.extract_primes(p20_runes)
    deor_primes = attack.extract_primes(deor_runes)
    
    # Ensure lengths match
    length = min(len(p20_primes), len(deor_primes))
    p20_primes = p20_primes[:length]
    deor_primes = deor_primes[:length]
    
    # Method 3: Deor - P20 (Beaufort)
    # The output log showed this had IoC 1.1459 and text like "HOEEDOE..."
    
    decoded = []
    gp = attack.GP  # Gematria Primus mapping
    gp_inv = {v: k for k, v in gp.items()}
    
    # Access rune values directly?
    # attack.GP is likely a dict {'F': 0, ...}
    # Let's assume we have lists of integers in p20_primes ? NO, extract_primes returns Runes (chars/strings).
    # We need to convert to numbers.
    
    def to_nums(runes):
        return [gp[r] for r in runes]
        
    p20_nums = to_nums(p20_primes)
    deor_nums = to_nums(deor_primes)
    
    res_nums = []
    for k, c in zip(deor_nums, p20_nums):
        # K - C
        val = (k - c) % 29
        res_nums.append(val)
        
    # Convert back to Runes
    # Need number to rune map
    # check if attack has it.
    
    # Invert GP manually if needed
    num_to_rune = {v: k for k, v in gp.items()}
    
    res_runes = [num_to_rune[n] for n in res_nums]
    res_str = "".join(res_runes)
    
    print(f"Extracted Stream ({length} runes):")
    print(res_str)
    
    # Save to file
    out_path = os.path.join(os.getcwd(), 'Analysis', 'Outputs', 'deor_stream_beaufort.txt')
    with open(out_path, 'w') as f:
        f.write(res_str)
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    main()

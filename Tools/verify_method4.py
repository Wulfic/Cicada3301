"""
Verify Method 4 - Check for collisions
"""

GEMATRIA_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                   53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

print("Monoalphabetic substitution table for Method 4:")
print("Input -> Output")

outputs = {}
for c in range(29):
    prime_val = GEMATRIA_PRIMES[c]
    phi_val = prime_val - 1
    out = (c - (phi_val % 29)) % 29
    outputs[c] = out
    print(f"  {c:2d} ({IDX_TO_LATIN[c]:3s}) -> {out:2d} ({IDX_TO_LATIN[out]:3s})   [φ={phi_val}, φ%29={phi_val % 29}]")

unique_outputs = set(outputs.values())
print(f"\nUnique outputs: {len(unique_outputs)} out of 29")

if len(unique_outputs) < 29:
    print("COLLISION DETECTED - artificially high IoC!")
    
    # Count collisions
    from collections import Counter
    out_counts = Counter(outputs.values())
    print("\nOutputs with multiple inputs:")
    for out, count in out_counts.items():
        if count > 1:
            inputs = [c for c in range(29) if outputs[c] == out]
            print(f"  {out} ({IDX_TO_LATIN[out]}) <- {[(i, IDX_TO_LATIN[i]) for i in inputs]}")

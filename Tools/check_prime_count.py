def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

count = 0
primes = []
for i in range(0, 1060): # Check up to 1060
    if is_prime(i):
        count += 1
        primes.append(i)

print(f"Primes up to 812: {len([p for p in primes if p < 812])}")
print(f"Primes up to 1047 (Deor len): {len([p for p in primes if p < 1047])}")

# What range gives 179 primes?
for n in range(0, 2000):
    c = 0
    for i in range(n):
        if is_prime(i): c+=1
    if c == 179:
        print(f"Range {n} has 179 primes.")

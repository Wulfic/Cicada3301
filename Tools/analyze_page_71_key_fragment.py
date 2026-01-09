
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def phi(n):
    result = 1
    for i in range(2, n):
        if gcd(i, n) == 1:
            result += 1
    return result

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_primes(limit):
    primes = []
    for x in range(2, limit):
        if is_prime(x):
            primes.append(x)
    return primes

def get_totients(limit):
    return [phi(x) for x in range(1, limit)]

KEY_FRAGMENT = [0, 18, 3, 13, 24, 16, 8, 24, 8, 21]
KEY_STRING = "FEOPATHAHNG"

# Letters count
from collections import Counter
key_counter = Counter(KEY_STRING)

def check_anagram(phrase, key_counter):
    phrase_counter = Counter(phrase.replace(" ", "").upper())
    # check if phrase can be formed from key (subset)
    # or if key is anagram of phrase (exact match)
    
    # Check if phrase is sub-anagram of Key
    is_sub = True
    for char, count in phrase_counter.items():
        if key_counter[char] < count:
            is_sub = False
            break
    
    if is_sub:
        leftover = []
        for char, count in key_counter.items():
            if count > phrase_counter[char]:
                leftover.append(char * (count - phrase_counter[char]))
        return "".join(sorted(leftover))
    return None

print(f"Key Fragment: {KEY_FRAGMENT}")
print(f"Key String:   {KEY_STRING}")

# 1. Search in Primes
print("\n--- Searching Primes (mod 29) ---")
primes = get_primes(10000)
primes_mod = [p % 29 for p in primes]

for i in range(len(primes_mod) - len(KEY_FRAGMENT) + 1):
    if primes_mod[i:i+len(KEY_FRAGMENT)] == KEY_FRAGMENT:
        print(f"MATCH FOUND in Primes at index {i} (Prime value: {primes[i]})")
        print(f"Context: {primes[i:i+len(KEY_FRAGMENT)]}")

# 2. Search in Totients
print("\n--- Searching Totients (mod 29) ---")
totients = get_totients(10000)
totients_mod = [t % 29 for t in totients]

for i in range(len(totients_mod) - len(KEY_FRAGMENT) + 1):
    if totients_mod[i:i+len(KEY_FRAGMENT)] == KEY_FRAGMENT:
        print(f"MATCH FOUND in Totients at index {i} (n={i+1}, phi={totients[i]})")
        print(f"Context: {totients[i:i+len(KEY_FRAGMENT)]}")

# 3. Anagram search
print("\n--- Anagram Search ---")
candidates = [
    "THE PATH OF",
    "THE PATH",
    "A PATH",
    "ONE PATH",
    "PATH OF",
    "DEATH",
    "LIFE",
    "GOD",
    "INTUS",
    "CICADA",
    "PRIMES",
]

for cand in candidates:
    rem = check_anagram(cand, key_counter)
    if rem is not None:
        print(f"'{cand}' is a valid sub-anagram. Remaining: {rem}")

# Check provided file corpus if exists
corpus_path = "LiberPrimus/key_search_corpus.txt"
import os
if os.path.exists(corpus_path):
    print(f"\n--- Searching {corpus_path} ---")
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().upper()
                if "FEOPATHAHNG" in line:
                    print(f"Found literal match in line: {line}")
    except:
        pass

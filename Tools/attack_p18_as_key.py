#!/usr/bin/env python3
"""
Test using Page 18's plaintext as key for Page 20 and other pages.

Page 18 plaintext: "BEING OF ALL I WILL ASC THE OATH IS SWORN TO THE ONE WITHIN THE ABOVE THE WAY"

Maybe this is the running key for subsequent pages?
"""

from collections import Counter
import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛞᛟᚪᚫᛡᛠᚣ"
RUNEGLISH = "FUÞORCGWHNIJEOPZSTBEMLNGDOÆYIA"
GP_MAP = {'F':0,'U':1,'V':1,'TH':2,'P':2,'Þ':2,'O':3,'R':4,'C':5,'K':5,'G':6,'W':7,
          'H':8,'N':9,'I':10,'J':11,'EO':12,'Z':14,'X':14,'S':15,'T':16,'B':17,
          'E':18,'M':19,'L':20,'NG':21,'OE':22,'D':23,'A':24,'AE':25,'Æ':25,'Y':26,
          'IA':27,'IO':27,'EA':28}

def text_to_indices(text):
    """Convert English text to Gematria Primus indices"""
    text = text.upper().replace(' ', '')
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in GP_MAP:
            result.append(GP_MAP[text[i:i+2]])
            i += 2
        elif text[i] in GP_MAP:
            result.append(GP_MAP[text[i]])
            i += 1
        else:
            i += 1
    return result

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [c for c in text if c in RUNES]

def rune_to_idx(r):
    return RUNES.index(r) if r in RUNES else -1

def idx_to_text(indices):
    return ''.join(RUNEGLISH[i % 29] for i in indices)

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1) / 29) if n > 1 else 0

def main():
    print("=" * 70)
    print("USING PAGE 18 PLAINTEXT AS KEY")
    print("=" * 70)
    
    # Page 18 plaintext
    p18_plaintext = "BEING OF ALL I WILL ASC THE OATH IS SWORN TO THE ONE WITHIN THE ABOVE THE WAY"
    p18_key = text_to_indices(p18_plaintext)
    
    print(f"Page 18 plaintext: {p18_plaintext}")
    print(f"As indices ({len(p18_key)} chars): {p18_key[:20]}...")
    print(f"Key length: {len(p18_key)} (53 is prime)")
    
    # Load Page 20
    p20 = load_runes('c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_20/runes.txt')
    p20_idx = [rune_to_idx(r) for r in p20]
    
    print(f"\nPage 20: {len(p20)} runes")
    
    # Try Page 18 plaintext as key
    print("\n" + "=" * 70)
    print("PAGE 18 PLAINTEXT AS KEY FOR PAGE 20")
    print("=" * 70)
    
    for name, op in [("SUB (C-K)", lambda c,k: (c-k)%29), 
                     ("Beaufort (K-C)", lambda c,k: (k-c)%29),
                     ("ADD (C+K)", lambda c,k: (c+k)%29)]:
        decrypted = [op(c, p18_key[i % len(p18_key)]) for i, c in enumerate(p20_idx)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:80])
        print(f"{name}: IoC = {ioc:.2f}")
        print(f"  {text}")
    
    # Also try Page 19's hint as key
    print("\n" + "=" * 70)
    print("PAGE 19 HINT AS KEY")
    print("=" * 70)
    
    p19_hint = "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR"
    p19_key = text_to_indices(p19_hint)
    print(f"Page 19 hint: {p19_hint}")
    print(f"Key length: {len(p19_key)}")
    
    for name, op in [("SUB", lambda c,k: (c-k)%29), ("Beaufort", lambda c,k: (k-c)%29)]:
        decrypted = [op(c, p19_key[i % len(p19_key)]) for i, c in enumerate(p20_idx)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:80])
        print(f"{name}: IoC = {ioc:.2f} | {text[:60]}")
    
    # Try combining P18 and P19 as alternating keys
    print("\n" + "=" * 70)
    print("COMBINED KEYS")
    print("=" * 70)
    
    # Concatenate P18 + P19 as key
    combined_key = p18_key + p19_key
    print(f"Combined key length: {len(combined_key)}")
    
    for name, op in [("SUB", lambda c,k: (c-k)%29), ("Beaufort", lambda c,k: (k-c)%29)]:
        decrypted = [op(c, combined_key[i % len(combined_key)]) for i, c in enumerate(p20_idx)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:80])
        print(f"{name}: IoC = {ioc:.2f} | {text[:60]}")
    
    # What if P18 plaintext is key for P19 (not P20)?
    print("\n" + "=" * 70)
    print("PAGE 18 AS KEY FOR PAGE 19")
    print("=" * 70)
    
    p19_path = 'c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_19/runes.txt'
    p19 = load_runes(p19_path)
    p19_idx = [rune_to_idx(r) for r in p19]
    print(f"Page 19: {len(p19)} runes")
    
    for name, op in [("SUB", lambda c,k: (c-k)%29), ("Beaufort", lambda c,k: (k-c)%29)]:
        decrypted = [op(c, p18_key[i % len(p18_key)]) for i, c in enumerate(p19_idx)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:60])
        print(f"{name}: IoC = {ioc:.2f} | {text}")
    
    # What about using P18 for just composite positions of P20?
    print("\n" + "=" * 70)
    print("P18 KEY FOR COMPOSITE POSITIONS ONLY")
    print("=" * 70)
    
    def is_prime(n):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5)+1, 2):
            if n % i == 0: return False
        return True
    
    # Get composite position runes
    composite_indices = [p20_idx[i] for i in range(len(p20)) if not is_prime(i)]
    print(f"Composite positions: {len(composite_indices)} runes")
    
    for name, op in [("SUB", lambda c,k: (c-k)%29), ("Beaufort", lambda c,k: (k-c)%29)]:
        decrypted = [op(c, p18_key[i % len(p18_key)]) for i, c in enumerate(composite_indices)]
        ioc = calc_ioc(decrypted)
        text = idx_to_text(decrypted[:80])
        print(f"{name}: IoC = {ioc:.2f} | {text[:60]}")

if __name__ == '__main__':
    main()

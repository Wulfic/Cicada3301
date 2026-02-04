#!/usr/bin/env python3
"""
Attack Page 20: Use Prime-numbered Stanzas from Deor

The Deor poem has 7 stanzas. The primes among 1-7 are: 2, 3, 5, 7
What if "REARRANGING THE PRIMES NUMBERS" means using stanzas 2, 3, 5, 7?

Stanza structure of Deor:
1. Wayland the Smith (lines 1-7)
2. Beadohild (lines 8-13)
3. Maethhild (lines 14-17)
4. Theodric (lines 18-20)
5. Eormanric (lines 21-27)
6. General suffering (lines 28-34)
7. Deor himself (lines 35-42)

Each stanza ends with the refrain: "Þæs ofereode, þisses swā mæg"
"""

import os
from collections import Counter

# Gematria Primus
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X',
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

CHAR_MAP = {
    'a': 24, 'b': 17, 'c': 5, 'd': 23, 'e': 18, 'f': 0, 'g': 6, 'h': 8, 'i': 10,
    'j': 11, 'l': 20, 'm': 19, 'n': 9, 'o': 3, 'p': 13, 'r': 4, 's': 15, 't': 16,
    'u': 1, 'w': 7, 'x': 14, 'y': 26, 'æ': 25, 'þ': 2, 'ð': 2, 'k': 5, 'v': 1
}

def load_runes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def text_to_indices(text):
    """Convert text to Gematria indices."""
    indices = []
    for c in text.lower():
        if c in CHAR_MAP:
            indices.append(CHAR_MAP[c])
    return indices

def calc_ioc(indices):
    if len(indices) < 2:
        return 0
    counts = Counter(indices)
    n = len(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29 if denominator > 0 else 0

def indices_to_latin(indices):
    return ''.join(LATIN_TABLE[i] for i in indices)

def vigenere_decrypt(cipher, key, mode='sub'):
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        elif mode == 'add':
            result.append((c + k) % 29)
        elif mode == 'beaufort':
            result.append((k - c) % 29)
    return result

# Deor stanza definitions (Old English text)
# Each stanza from the Deor poem
DEOR_STANZAS = {
    1: """Welund him be wurman wræces cunnade,
anhydig eorl earfoþa dreag,
hæfde him to gesiþþe sorge ond longaþ,
wintercealde wræce; wean oft onfond,
siþþan hine Niðhad on nede legde,
swoncre seonobende on syllan monn.
Þæs ofereode, þisses swa mæg.""",
    
    2: """Beadohilde ne wæs hyre broþra deaþ
on sefan swa sar swa hyre sylfre þing,
þæt heo gearolice ongieten hæfde
þæt heo eacen wæs; æfre ne meahte
þriste geþencan, hu ymb þæt sceolde.
Þæs ofereode, þisses swa mæg.""",
    
    3: """We þæt Mæðhilde monge gefrugnon
wurdon grundlease Geates frige,
þæt hi seið-sorga slæp ealle binom.
Þæs ofereode, þisses swa mæg.""",
    
    4: """Ðeodric ahte þritig wintra
Mæringa burg; þæt wæs monegum cuþ.
Þæs ofereode, þisses swa mæg.""",
    
    5: """We geascodan Eormanrices
wylfenne geþoht; ahte wide folc
Gotena rices. Þæt wæs grim cyning.
Sæt secg monig sorgum gebunden,
wean on wenan, wyscte geneahhe
þæt þæs cynerices ofercumen wære.
Þæs ofereode, þisses swa mæg.""",
    
    6: """Siteð sorgcearig, sælum bidæled,
on sefan sweorceð, sylfum þinceð
þæt sy endeleas earfoða dæl.
Mæg þonne geþencan, þæt geond þas woruld
witig Dryhten wendeþ geneahhe,
eorle monegum are gesceawað,
wislicne blæd, sumum weana dæl.""",
    
    7: """Þæt ic bi me sylfum secgan wille,
þæt ic hwile wæs Heodeninga scop,
dryhtne dyre. Me wæs Deor noma.
Ahte ic fela wintra folgað tilne,
holdne hlaford, oþþæt Heorrenda nu,
leoðcræftig monn londryht geþah,
þæt me eorla hleo ær gesealde.
Þæs ofereode, þisses swa mæg."""
}

# Just the refrain
DEOR_REFRAIN = "Þæs ofereode, þisses swa mæg"

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    cipher = load_runes(p20_path)
    print(f"Loaded {len(cipher)} runes from Page 20")
    
    # Prime stanzas: 2, 3, 5, 7
    prime_stanzas = [2, 3, 5, 7]
    
    print("\n" + "="*60)
    print("APPROACH 1: Concatenate prime stanzas (2, 3, 5, 7)")
    print("="*60)
    
    prime_text = ""
    for s in prime_stanzas:
        prime_text += DEOR_STANZAS[s]
    
    prime_key = text_to_indices(prime_text)
    print(f"Prime stanzas key length: {len(prime_key)}")
    print(f"Key preview: {indices_to_latin(prime_key[:50])}")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, prime_key, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    print("\n" + "="*60)
    print("APPROACH 2: Rearrange stanzas by prime order")
    print("="*60)
    
    # Original: 1,2,3,4,5,6,7
    # Rearranged putting primes first: 2,3,5,7,1,4,6
    rearranged_order = [2, 3, 5, 7, 1, 4, 6]
    rearranged_text = ""
    for s in rearranged_order:
        rearranged_text += DEOR_STANZAS[s]
    
    rearranged_key = text_to_indices(rearranged_text)
    print(f"Rearranged stanzas key length: {len(rearranged_key)}")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, rearranged_key, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    print("\n" + "="*60)
    print("APPROACH 3: Use only the refrain repeated")
    print("="*60)
    
    refrain_key = text_to_indices(DEOR_REFRAIN)
    print(f"Refrain key: {indices_to_latin(refrain_key)} ({len(refrain_key)} chars)")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, refrain_key, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    print("\n" + "="*60)
    print("APPROACH 4: Stanza 7 only (contains 'DEOR')")
    print("="*60)
    
    stanza7_key = text_to_indices(DEOR_STANZAS[7])
    print(f"Stanza 7 key length: {len(stanza7_key)}")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, stanza7_key, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    print("\n" + "="*60)
    print("APPROACH 5: Extract lines at prime positions from full Deor")
    print("="*60)
    
    # Get all lines
    all_lines = []
    for s in range(1, 8):
        lines = DEOR_STANZAS[s].strip().split('\n')
        all_lines.extend(lines)
    
    print(f"Total lines: {len(all_lines)}")
    
    # Extract prime-numbered lines (2, 3, 5, 7, 11, 13, ...)
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    
    prime_lines = [all_lines[i-1] for i in range(1, len(all_lines)+1) if is_prime(i) and i <= len(all_lines)]
    print(f"Prime-numbered lines: {len(prime_lines)}")
    
    prime_lines_text = " ".join(prime_lines)
    prime_lines_key = text_to_indices(prime_lines_text)
    print(f"Prime lines key length: {len(prime_lines_key)}")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, prime_lines_key, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    print("\n" + "="*60)
    print("APPROACH 6: Word 'DEOR' as simple key")
    print("="*60)
    
    deor_simple = text_to_indices("DEOR")
    print(f"DEOR key: {deor_simple}")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, deor_simple, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")
    
    print("\n" + "="*60)
    print("APPROACH 7: The phrase 'THE LONE' from partial solution")
    print("="*60)
    
    the_lone = text_to_indices("THELONE")  # Without space
    print(f"THELONE key: {the_lone}")
    
    for mode in ['sub', 'add', 'beaufort']:
        result = vigenere_decrypt(cipher, the_lone, mode)
        ioc = calc_ioc(result)
        latin = indices_to_latin(result)
        print(f"\n[{mode.upper()}] IoC: {ioc:.4f}")
        print(f"  Preview: {latin[:80]}")

if __name__ == '__main__':
    main()

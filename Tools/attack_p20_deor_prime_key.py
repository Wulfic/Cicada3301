
import os
from collections import Counter

# --- Text Data ---
DEOR_TEXT_OLD_ENGLISH = """
Welund him be wurman wræces cunnade,
anhydig eorl earfoþa dreag,
hæfde him to gesiþþe sorge ond longaþ,
wintercealde wræce; wean oft onfond,
siþþan hine Niðhad on nede legde,
swoncre seonobende on syllan monn.
Þæs ofereode, þisses swa mæg.

Beadohilde ne wæs hyre broþra deaþ
on sefan swa sar swa hyre sylfre þing,
þæt heo gearolice ongieten hæfde
þæt heo eacen wæs; æfre ne meahte
þriste geþencan, hu ymb þæt sceolde.
Þæs ofereode, þisses swa mæg.

We þæt Mæðhilde monge gefrugnon
wurdon grundlease Geates frige,
þæt hi seo sorglufu slæp ealle binom.
Þæs ofereode, þisses swa mæg.

Ðeodric ahte þritig wintra
Mæringa burg; þæt wæs monegum cuþ.
Þæs ofereode, þisses swa mæg.

We geascodan Eormanrices
wylfenne geþoht; ahte wide folc
Gotena rices. Þæt wæs grim cyning.
Sæt secg monig sorgum gebunden,
wean on wenan, wyscte geneahhe
þæt þæs cynerices ofercumen wære.
Þæs ofereode, þisses swa mæg.

Siteð sorgcearig, sælum bedæled,
on sefan sweorceð, sylfum þinceð
þæt sy endeleas earfoða dæl.
Mæg þonne geþencan, þæt geond þas woruld
witig Dryhten wendeþ geneahhe,
eorle monegum are gesceawað,
wislicne blæd, sumum weana dæl.

Þæt ic bi me sylfum secgan wille,
þæt ic hwile wæs Heodeninga scop,
dryhtne dyre. Me wæs Deor noma.
Ahte ic fela wintra folgað tilne,
holdne hlaford, oþþæt Heorrenda nu,
leoðcræftig monn londryht geþah,
þæt me eorla hleo ær gesealde.
Þæs ofereode, þisses swa mæg.
"""

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
LATIN_TO_VAL = {
    'F': 0, 'U': 1, 'V': 1, 'TH': 2, 'P': 2, 'Þ': 2, 'Ð': 2, 
    'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9, 
    'I': 10, 'J': 11, 'EO': 12, 'Z': 14, 'S': 15, 'T': 16, 'B': 17, 
    'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 
    'A': 24, 'AE': 25, 'Æ': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}
LATIN_TABLE = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace('-', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def tokenize_oe(text):
    text = text.upper().replace(' ', '').replace('\n', '').replace(',', '').replace('.', '').replace(';', '')
    values = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in LATIN_TO_VAL:
            values.append(LATIN_TO_VAL[text[i:i+2]])
            i += 2
        elif text[i] in LATIN_TO_VAL:
            values.append(LATIN_TO_VAL[text[i]])
            i += 1
        else:
            i += 1
    return values

def to_letters(values):
    return "".join([LATIN_TABLE[v] for v in values])

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    # 1. Get Deor Runes
    deor_runes = tokenize_oe(DEOR_TEXT_OLD_ENGLISH)
    print(f"Deor Poem Length: {len(deor_runes)}")
    
    # 2. Extract Prime Indices from Deor
    deor_primes = [deor_runes[i] for i in range(len(deor_runes)) if is_prime(i)]
    print(f"Extracted {len(deor_primes)} runes from Deor at Prime Indices.")
    print(f"Key Preview: {to_letters(deor_primes)[:50]}")
    
    # 3. Decrypt Page 20 with Deor-Prime Key (Running)
    dec1 = [(c - k) % 29 for c, k in zip(cipher, deor_primes * (len(cipher)//len(deor_primes) + 1))]
    print(f"Deor-Prime Key IoC: {calculate_ioc(dec1):.4f}")
    print(f"Preview: {to_letters(dec1)[:50]}")
    
    # 4. Try Decrypting Prime Indices of Page 20 with Deor-Prime Key
    p20_primes = [cipher[i] for i in range(len(cipher)) if is_prime(i)]
    dec2 = [(c - k) % 29 for c, k in zip(p20_primes, deor_primes[:len(p20_primes)])]
    print(f"P20-Primes decrypted by Deor-Primes IoC: {calculate_ioc(dec2):.4f}")
    print(f"Preview: {to_letters(dec2)[:50]}")
    
    # DEBUG
    print("\n--- DEBUG ---")
    print(f"P20 Primes (First 10): {[to_letters([x]) for x in p20_primes[:10]]}")
    print(f"Deor Primes (First 10): {[to_letters([x]) for x in deor_primes[:10]]}")
    print(f"Result (First 10): {[to_letters([x]) for x in dec2[:10]]}")
    
    # Try Variant: P = C + K
    dec3 = [(c + k) % 29 for c, k in zip(p20_primes, deor_primes[:len(p20_primes)])]
    print(f"\nVariant (C+K) IoC: {calculate_ioc(dec3):.4f}")
    print(f"Preview: {to_letters(dec3)[:50]}")
    
    # Try Variant: Beaufort (K - C)
    dec5 = [(k - c) % 29 for c, k in zip(p20_primes, deor_primes[:len(p20_primes)])]
    print(f"\nVariant (K-C, Beaufort) IoC: {calculate_ioc(dec5):.4f}")
    print(f"Preview: {to_letters(dec5)[:50]}")
    
    # Try Variant: Beaufort + Shift (K - C + S)
    # Loop shifts
    best_ioc = 0
    best_shift = 0
    for s in range(29):
        shifted = [(x + s) % 29 for x in dec5]
        ioc = calculate_ioc(shifted)
        if ioc > best_ioc:
            best_ioc = ioc
            best_shift = s
    
    print(f"Best Beaufort Shift: {best_shift} (IoC: {best_ioc:.4f})")
    print(f"Preview: {to_letters([(x + best_shift) % 29 for x in dec5])[:60]}")

    # Output to File
    out_path = "Analysis/Outputs/p20_prime_stream_full.txt"
    ck_shift_5 = [(x + 5) % 29 for x in dec2] # YEOT...
    kc_shift_0 = dec5
    
    with open(out_path, "w") as f:
        f.write("--- Method 1: (P20_Prime - Deor_Prime + 5) ---\n")
        f.write(to_letters(ck_shift_5) + "\n\n")
        
        f.write("--- Method 2: (Deor_Prime - P20_Prime) (Beaufort) ---\n")
        f.write(to_letters(kc_shift_0) + "\n\n")
        
    print(f"\nSaved full streams to {out_path}")


if __name__ == "__main__":
    main()

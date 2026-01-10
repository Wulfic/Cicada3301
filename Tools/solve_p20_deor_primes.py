
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

# --- Rune Mapping ---
# Standard Cicada Gematria
RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
INV_RUNE_MAP = {v: k for k, v in RUNE_MAP.items()}

# Latin to Rune Value Mapping (Approximate for OE)
LATIN_TO_VAL = {
    'F': 0, 'U': 1, 'V': 1, 'TH': 2, 'P': 2, 'Þ': 2, 'Ð': 2, 
    'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9, 
    'I': 10, 'J': 11, 'EO': 12, 'Z': 14, 'S': 15, 'T': 16, 'B': 17, 
    'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 
    'A': 24, 'AE': 25, 'Æ': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace('-', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def tokenize_oe(text):
    """Converts OE text to rune values."""
    text = text.upper().replace(' ', '').replace('\n', '').replace(',', '').replace('.', '').replace(';', '')
    values = []
    i = 0
    while i < len(text):
        # Check double chars first
        if i + 1 < len(text) and text[i:i+2] in LATIN_TO_VAL:
            values.append(LATIN_TO_VAL[text[i:i+2]])
            i += 2
        elif text[i] in LATIN_TO_VAL:
            values.append(LATIN_TO_VAL[text[i]])
            i += 1
        else:
            i += 1 # Skip unknown
    return values

def decrypt_vigenere(cipher, key):
    res = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        val = (c - k) % 29
        res.append(val)
    return res

def to_letters(values):
    # Reverse map for display (Approx)
    # Using the standard Latin Table from other tools
    LATIN_TABLE = [
        "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", 
        "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
    ]
    return "".join([LATIN_TABLE[v] for v in values])

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29  # Normalized for N=29

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    
    if not os.path.exists(p20_path):
        print(f"Error: {p20_path} not found.")
        return

    cipher = load_runes(p20_path)
    print(f"Loaded {len(cipher)} runes from Page 20.")
    print(f"Cipher IoC: {calculate_ioc(cipher):.4f}")

    # 1. Deor Running Key
    deor_key = tokenize_oe(DEOR_TEXT_OLD_ENGLISH)
    print(f"Generated Deor Key (Running): {len(deor_key)} runes.")
    
    decrypted_deor = decrypt_vigenere(cipher, deor_key)
    ioc_deor = calculate_ioc(decrypted_deor)
    print(f"Deor Running Key IoC: {ioc_deor:.4f}")
    print(f"Preview: {to_letters(decrypted_deor)[:50]}")

    # 2. Deor Repeating Key (Refrain)
    refrain = "Þæs ofereode, þisses swa mæg"
    refrain_key = tokenize_oe(refrain)
    print(f"Refrain Key: {to_letters(refrain_key)}")
    decrypted_refrain = decrypt_vigenere(cipher, refrain_key)
    print(f"Refrain Key IoC: {calculate_ioc(decrypted_refrain):.4f}")

    # 3. Prime Indices Extraction
    primes = [i for i in range(len(cipher)) if  
              all(i % p != 0 for p in range(2, int(i**0.5) + 1)) and i > 1]
    
    prime_runes = [cipher[i] for i in primes if i < len(cipher)]
    print(f"Extracted {len(prime_runes)} runes at Prime Indices.")
    print(f"Prime Runes IoC: {calculate_ioc(prime_runes):.4f}")
    print(f"Prime Runes Text: {to_letters(prime_runes)[:50]}")

    # 4. Prime Value Extraction (Runes that are Prime Numbers)
    prime_vals = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    # Note: 29 is modulus, not a value usually (0-28)
    
    val_primes = [c for c in cipher if c in prime_vals]
    print(f"Extracted {len(val_primes)} runes with Prime Values.")
    print(f"Prime Values IoC: {calculate_ioc(val_primes):.4f}")
    print(f"Prime Values Text: {to_letters(val_primes)}")
    
    # 5. Reverse Vigenere (P = C + K => C = P - K => K = C - P? No. P = C - K)
    # Maybe key is reversed?
    reversed_deor = deor_key[::-1]
    decrypted_rev_deor = decrypt_vigenere(cipher, reversed_deor)
    print(f"Reversed Deor Key IoC: {calculate_ioc(decrypted_rev_deor):.4f}")

if __name__ == "__main__":
    main()


import os
from collections import Counter

# --- Definitions ---
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

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def calculate_ioc(values):
    counts = Counter(values)
    n = len(values)
    if n < 2: return 0
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1)) * 29

def main():
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    p20_path = os.path.join(repo, "LiberPrimus", "pages", "page_20", "runes.txt")
    cipher = load_runes(p20_path)
    
    deor_runes = tokenize_oe(DEOR_TEXT_OLD_ENGLISH)
    deor_primes = [deor_runes[i] for i in range(len(deor_runes)) if is_prime(i)]
    
    p20_primes = [cipher[i] for i in range(len(cipher)) if is_prime(i)]
    
    # Target Cipher for further analysis
    target_cipher = [(c - k) % 29 for c, k in zip(p20_primes, deor_primes[:len(p20_primes)])]
    
    print(f"Target Cipher IoC: {calculate_ioc(target_cipher):.4f}")
    
    # 1. Caesar Shift Bruteforce
    print("\n--- Caesar Shift ---")
    for shift in range(29):
        shifted = [(c + shift) % 29 for c in target_cipher]
        print(f"Shift {shift}: {to_letters(shifted)[:60]}")
        
    # 2. Vigenere with common keys
    keys = ["DIVINITY", "FIRFUMFERENFE", "INSTAR", "CICADA"] 
    # (FIRFUMFERENFE is CIRCUMFERENCE with C=F?)
    # Just standard keys
    
    # 3. Frequency Analysis
    print("\n--- Frequency ---")
    counts = Counter(target_cipher)
    sorted_counts = counts.most_common()
    print("Top 5 Runes:")
    for val, count in sorted_counts[:5]:
        print(f"{LATIN_TABLE[val]} ({val}): {count}")
    
    # 4. Save to file
    out_path = os.path.join(repo, "Analysis", "Outputs", "p20_prime_stream_candidate.txt")
    with open(out_path, "w") as f:
        f.write(to_letters(target_cipher))
    print(f"\nSaved full candidate to {out_path}")

if __name__ == "__main__":
    main()

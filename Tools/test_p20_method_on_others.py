"""
Test the P20 method (prime positions + Deor Beaufort + interleave) on Pages 21-30
"""

import os
from collections import Counter

os.chdir(r"c:\Users\tyler\Repos\Cicada3301")

# Gematria Primus
RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
GP_MAP = {r: i for i, r in enumerate(RUNEGLISH)}
INV_MAP = {i: r for i, r in enumerate(RUNEGLISH)}

RUNE_TO_IDX = {
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

DEOR_TEXT = """
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

def tokenize_oe(text):
    text = text.upper().replace(' ', '').replace('\n', '')
    text = ''.join(c for c in text if c.isalpha() or c in 'ÞÐÆ')
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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def calc_ioc(values):
    if len(values) < 2:
        return 0
    counts = Counter(values)
    n = len(values)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1) / 29)

def to_str(indices):
    return "".join(INV_MAP[i % 29] for i in indices)

def load_page(page_num):
    path = f"LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def find_words(text, words):
    found = []
    for word in words:
        if word in text:
            found.append(word)
    return found

# Convert Deor to GP values
deor_values = tokenize_oe(DEOR_TEXT)
print(f"Deor poem: {len(deor_values)} values")

# Common words to look for
WORDS = ['THE', 'LONE', 'HER', 'ONE', 'ALT', 'MET', 'ODE', 'AM', 'BID', 'SAY', 'OF',
         'DEATH', 'PATH', 'SELF', 'EODE', 'SEFA', 'AND', 'FOR', 'YOU', 'ALL', 'ARE',
         'THIS', 'THAT', 'WITH', 'HAVE', 'WILL', 'FROM', 'THEY', 'BEEN', 'WITHIN']

print("="*80)
print("TESTING P20 METHOD ON PAGES 21-35")
print("="*80)

results = []

for page_num in range(20, 36):
    page_runes = load_page(page_num)
    if page_runes is None:
        continue
    
    # Extract prime positions (matching length with Deor)
    max_len = min(len(page_runes), len(deor_values))
    page_primes = [page_runes[i] for i in range(max_len) if is_prime(i)]
    deor_primes = [deor_values[i] for i in range(max_len) if is_prime(i)]
    
    # Ensure same length
    length = min(len(page_primes), len(deor_primes))
    page_primes = page_primes[:length]
    deor_primes = deor_primes[:length]
    
    # Beaufort cipher: K - C
    stream = [(deor_primes[i] - page_primes[i]) % 29 for i in range(length)]
    
    # Interleave if length is even
    if len(stream) % 2 == 0:
        half = len(stream) // 2
        interleaved_indices = []
        for i in range(half):
            interleaved_indices.append(stream[i])
            interleaved_indices.append(stream[half + i])
        interleaved_text = to_str(interleaved_indices)
    else:
        interleaved_text = to_str(stream)
    
    # Calculate IoC
    stream_ioc = calc_ioc(stream)
    
    # Find words
    words_found = find_words(interleaved_text, WORDS)
    
    print(f"\nPage {page_num}:")
    print(f"  Runes: {len(page_runes)}, Primes: {length}, IoC: {stream_ioc:.4f}")
    print(f"  Words found: {words_found}")
    print(f"  Text (first 60): {interleaved_text[:60]}...")
    
    results.append((page_num, length, stream_ioc, len(words_found), interleaved_text[:80]))

print("\n" + "="*80)
print("SUMMARY: PAGES RANKED BY WORD COUNT")
print("="*80)

results.sort(key=lambda x: (-x[3], -x[2]))
for page_num, length, ioc, word_count, text in results[:10]:
    print(f"Page {page_num}: {word_count} words, IoC={ioc:.4f}, len={length}")
    print(f"  '{text[:60]}...'")

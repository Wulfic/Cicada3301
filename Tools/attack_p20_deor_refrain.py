"""
Page 20 - Deor Refrain Attack
=============================
The refrain "Þæs ofereode, þisses swa mæg" appears 7 times.
Try using just the refrain as the key.
"""

import collections

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

IDX_TO_LATIN = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# English to Gematria index mapping
ENGLISH_TO_IDX = {
    'A': 24, 'B': 17, 'C': 5, 'D': 23, 'E': 18, 'F': 0, 'G': 6, 'H': 8,
    'I': 10, 'J': 11, 'K': 5, 'L': 20, 'M': 19, 'N': 9, 'O': 3, 'P': 13,
    'Q': 5, 'R': 4, 'S': 15, 'T': 16, 'U': 1, 'V': 1, 'W': 7, 'X': 14,
    'Y': 26, 'Z': 15
}

def load_runes(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '').replace('•', '').replace("'", '')
    return [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]

def runes_to_latin(indices):
    return ''.join(IDX_TO_LATIN.get(i, '?') for i in indices)

def calculate_ioc(text):
    if len(text) < 2: return 0
    counts = collections.Counter(text)
    numerator = sum(n * (n - 1) for n in counts.values())
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator * 29.0

def decrypt_vigenere(cipher, key, mode='sub'):
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'sub':
            result.append((c - k) % 29)
        else:
            result.append((c + k) % 29)
    return result

def main():
    print("="*60)
    print("PAGE 20 - DEOR REFRAIN ATTACK")
    print("="*60)
    
    runes = load_runes(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt")
    rows, cols = 28, 29
    
    # The refrain in Old English: "Þæs ofereode, þisses swa mæg"
    # Transliterations to try:
    refrains = [
        "THAESOFEREODETHISSESSWAMAEG",      # Direct transliteration
        "THAESOFEREODETISSESWAMAEG",        # þisses -> tisses (no th in middle)
        "THASOFEREODETHISSESWAMAEG",        # æ -> a
        "THAESOFEREODETHISESSWAMAEG",       # Single s
        "OFEREODETHISSESSWAMAEG",           # Without "Þæs"
        "THATOVERTHISTHISSOMAYTHIS",        # Modern translation-ish
        "THATPASSEDAWAYSOMAYETHIS",         # Modern English meaning
        "THAESOFEREODETHISSESWAMAEGK",      # With trailing K (DEOR K hint)
    ]
    
    print(f"\nTotal runes: {len(runes)}")
    print(f"Grid: {rows} × {cols}")
    
    for refrain in refrains:
        key = [ENGLISH_TO_IDX.get(c, 0) for c in refrain if c in ENGLISH_TO_IDX]
        print(f"\n--- Refrain: {refrain} (len={len(key)}) ---")
        
        # Try direct decryption
        result = decrypt_vigenere(runes, key, 'sub')
        ioc = calculate_ioc(result)
        print(f"C - refrain: IoC={ioc:.4f}")
        if ioc > 1.1:
            print(f"Text: {runes_to_latin(result[:80])}")
        
        # Try add mode
        result = decrypt_vigenere(runes, key, 'add')
        ioc = calculate_ioc(result)
        print(f"C + refrain: IoC={ioc:.4f}")
        if ioc > 1.1:
            print(f"Text: {runes_to_latin(result[:80])}")
    
    # What if each of the 7 strophes uses the refrain differently?
    print("\n--- 7 strophe structure: each 4-row block uses refrain offset by strophe number ---")
    
    refrain = "THAESOFEREODETHISSESSWAMAEG"
    key = [ENGLISH_TO_IDX.get(c, 0) for c in refrain if c in ENGLISH_TO_IDX]
    grid = [[runes[r*cols + c] for c in range(cols)] for r in range(rows)]
    
    result = []
    for r in range(rows):
        strophe = r // 4  # Which strophe (0-6)
        for c in range(cols):
            pos = c  # Position within row
            # Offset key by strophe number
            key_pos = (pos + strophe) % len(key)
            result.append((grid[r][c] - key[key_pos]) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Strophe-offset refrain: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # What if the refrain is used as a row transposition key?
    print("\n--- Refrain as row reordering key ---")
    
    # Sort rows by refrain values (use first 28 chars)
    refrain28 = refrain[:28] if len(refrain) >= 28 else refrain * 2
    refrain28 = refrain28[:28]
    
    row_keys = [(ENGLISH_TO_IDX.get(c, 0), i) for i, c in enumerate(refrain28)]
    sorted_rows = [i for _, i in sorted(row_keys)]
    
    print(f"Row order: {sorted_rows}")
    
    reordered = []
    for new_pos, old_pos in enumerate(sorted_rows):
        for c in range(cols):
            reordered.append(grid[old_pos][c])
    
    ioc = calculate_ioc(reordered)
    print(f"Transposed (no decrypt): IoC={ioc:.4f}")
    
    # Now decrypt the transposed grid
    full_key = key * (len(reordered) // len(key) + 1)
    full_key = full_key[:len(reordered)]
    result = decrypt_vigenere(reordered, full_key, 'sub')
    ioc = calculate_ioc(result)
    print(f"Transposed + refrain decrypt: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")
    
    # What if each row is decrypted with a DIFFERENT strophe from Deor?
    print("\n--- Each 4-row block decrypted with different Deor strophe ---")
    
    # Get the 7 strophes (excluding refrain)
    strophe1 = "WELUNDHIMBEWURMANWRAESCUNNADEANHYDIGEORLEARFOTHADREAGHAEFDEHIMTOGESITHTHESORGEONDONGATWINTERCEALDEWAECEWEANOFTONFONDSITHTHANHINENITHADONNEDELEGDESWONCRESEONOBENDEONSELLANMONN"
    strophe2 = "BEADOHILDENEWASHYREBROTHRADEATONSEFANSWAARSWAHERESELFRETHINGTHATHEOGEAROLICEONGIETHENHAEFDETHATHEEOEACENWAESAEFRENEEMAHTETHRISTEGETHENCANHUYMBTHAETSCOLDE"
    strophe3 = "WETHATMAETTHILDEMONGEGEFRUGNONWURDONGUNDLEASEGEATSFRIGETHATHISEITSORGESLAEPEALLEBINOM"
    strophe4 = "THEODRICAHTETRITIGWINTRAMARENGABURGTHAETWASMONEGUMCUTH"
    strophe5 = "WEGEASCODANEORMANRICESWYLFENNEGETOHAHTEWIDFOLCGOTENARICESTHAETWASGEMCYNINGSAETSECGMONIGSORGUMEGEBUNDENWEAONWENANWYSCTEGENEAHHETHAETHTHAESCYNERICESOFERCUMENWERE"
    strophe6 = "SITETHSORGCEARIGSELUMIDELEDONSEAFSWEORCETHSEOFUMTHINCATHTHATSEYENDELEASEARFOTHADAELMAGETHONNEGETHENCANTHEGEONDTHASWORULD"
    strophe7 = "WITIGDRYHTENWNDETHENEAHHEEORLEMONEGUMAREGESCEWATWISLICNEBLAEDSUUMWEANADAELTHATICBIMESELFUMSECGANWILLTHATICWHILEWASHEODENENGASCOPLORYHTNEDFYREMEWASDORNOMAAHTEICELAWENTRAFOLGAETILNEHOLDENHLAFFORDOTHATTHEORRENNDUNULEODCREFTIGMONNONLONDRITHGETAHTHEATMEEORLEAHEOAERGESEALDE"
    
    strophes_text = [strophe1, strophe2, strophe3, strophe4, strophe5, strophe6, strophe7]
    strophes_keys = [[ENGLISH_TO_IDX.get(c, 0) for c in s if c in ENGLISH_TO_IDX] for s in strophes_text]
    
    result = []
    for r in range(rows):
        strophe_idx = r // 4  # 0-6
        strophe_key = strophes_keys[strophe_idx]
        for c in range(cols):
            key_val = strophe_key[c % len(strophe_key)]
            result.append((grid[r][c] - key_val) % 29)
    
    ioc = calculate_ioc(result)
    print(f"Per-strophe key decryption: IoC={ioc:.4f}")
    print(f"Text: {runes_to_latin(result[:80])}")

if __name__ == "__main__":
    main()

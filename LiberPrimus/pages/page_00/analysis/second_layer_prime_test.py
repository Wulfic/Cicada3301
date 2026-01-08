#!/usr/bin/env python3
"""
Test the Page 56 method (prime-1 subtraction) on our FIRST LAYER OUTPUT.
This tests if prime-1 is a second layer cipher on top of our SUB mod 29 result.
"""

# Gematria Primus
LETTER_TO_IDX = {
    'F': 0, 'V': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23,
    'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'EA': 28
}
IDX_TO_LETTER = ['F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
                 'A', 'AE', 'Y', 'IA', 'EA']

# First 300 primes
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
          157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 
          239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 
          331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 
          421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
          509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
          613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
          709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
          821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
          919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019,
          1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097,
          1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
          1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291,
          1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409,
          1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487,
          1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579,
          1583, 1597, 1601, 1607, 1609, 1613, 1619]

# English frequency scoring
ENGLISH_FREQ = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 
                'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
                'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0,
                'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.1, 'Z': 0.07}
ENGLISH_BIGRAMS = {'TH': 15.2, 'HE': 12.8, 'IN': 9.8, 'ER': 9.4, 'AN': 8.2, 'RE': 6.8, 
                   'ON': 6.5, 'AT': 6.2, 'EN': 5.6, 'ND': 5.6, 'TI': 5.4, 'ES': 5.2,
                   'OR': 5.0, 'TE': 4.6, 'OF': 4.0, 'ED': 4.0, 'IS': 4.0, 'IT': 4.0,
                   'AL': 3.8, 'AR': 3.6, 'ST': 3.6, 'TO': 3.2, 'NT': 3.2, 'NG': 3.0}

# First layer outputs from our SUB mod 29 attack
FIRST_LAYER_OUTPUTS = {
    0: "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL",
    1: "THEREATHHOGTHENGTHEATHTHWTIAEEATHEATHENGRENGHEATHATHTHRWTHEATHOFGTTHREATHETHEOTHEATHTMITHOTHTHWRHEOFEETHEHMAIATTHEATHYTHETHEAEHTHNBPCWATHXONGAEMUAERUYTHEREODENGGEATHTHJATHEANITHMPTHIATHERTHENREATHTHTEATHMOENTHWTOITHLTHTITATPREATHEATHTHOINGWREOFTHEAIXDFWGEREOWIDHTHECEOGEATCTHEOFREOJTHTHJXIJITHETHAEREIATHEANTHGYFIANGTHTHEREIATRTTHIATHEONGLBYREONGGAJUDEAETHEDSRIAN",
    2: "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYJJUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE",
    3: "TMMEEMMEMNGEEBMTMTBTEEEBEEEAEESBSBEMEEEMEEBEEEEEEEEEEEEMBEBEEEEEEEEEMEEEEEEEEMEEEEEENTHEOTHTHOEAERREMTHEATHHANGTIALIESJOETEDIATHENGTHCINYWTEOTTHAPEAFAEREOTTEAYEDESTIAXNPTHAEPAEDOEWIEOBJMETHETHEOJEATEONGBRCIATHEPETHPCITDHEAGGSOEIAANGNGE",
    4: "MEESBETEEEBEMBBMMBEEETEBBEEETEMEMBEEMMETMBMMEEMMMEEBEMEMEEMEEEETMEMBEEEMEMEEEEBBEMEEEEEEMEBMEMBEMLEEBOEJOEREANDNGLTHEETHERENDBFEAHEATEHENTHEAWHEOFSANGTIATESTHNGFATHEANGNGTENGGISAEANGIPTIATHOETHEAFPEONGTHEAIANJHXGEORETHCFMYWGTHEANGIATHTHEOTHAERNITHAEOEL"
}

def text_to_indices(text):
    """Convert Gematria text to indices, handling digraphs."""
    indices = []
    i = 0
    text = text.upper().replace('K', 'C').replace('U', 'V')  # Normalize
    
    while i < len(text):
        # Check for digraphs first
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_IDX:
                indices.append(LETTER_TO_IDX[digraph])
                i += 2
                continue
        
        # Single letter
        if text[i] in LETTER_TO_IDX:
            indices.append(LETTER_TO_IDX[text[i]])
            i += 1
        else:
            # Skip non-Gematria characters
            i += 1
    
    return indices

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(IDX_TO_LETTER[i] for i in indices)

def score_text(text):
    """Score text based on English letter and bigram frequency."""
    text = text.upper()
    score = 0
    
    for char in text:
        if char in ENGLISH_FREQ:
            score += ENGLISH_FREQ[char]
    
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in ENGLISH_BIGRAMS:
            score += ENGLISH_BIGRAMS[bigram] * 2
    
    return score

def method_prime_minus_1(indices):
    """Page 56 method: subtract (prime[i] - 1) from each position."""
    result = []
    for i, c in enumerate(indices):
        if i < len(PRIMES):
            shift = (PRIMES[i] - 1) % 29
            result.append((c - shift) % 29)
        else:
            result.append(c)
    return result

def method_prime_only(indices):
    """Subtract prime[i] directly."""
    result = []
    for i, c in enumerate(indices):
        if i < len(PRIMES):
            shift = PRIMES[i] % 29
            result.append((c - shift) % 29)
        else:
            result.append(c)
    return result

def method_add_prime_minus_1(indices):
    """ADD (prime[i] - 1) instead of subtract."""
    result = []
    for i, c in enumerate(indices):
        if i < len(PRIMES):
            shift = (PRIMES[i] - 1) % 29
            result.append((c + shift) % 29)
        else:
            result.append(c)
    return result

def method_add_prime(indices):
    """ADD prime[i] directly."""
    result = []
    for i, c in enumerate(indices):
        if i < len(PRIMES):
            shift = PRIMES[i] % 29
            result.append((c + shift) % 29)
        else:
            result.append(c)
    return result

def method_constant_shift(indices, k):
    """Constant shift."""
    return [(c + k) % 29 for c in indices]

def test_page(page_num, first_layer_text):
    """Test all methods on a page's first layer output."""
    print(f"\n{'='*60}")
    print(f"PAGE {page_num}")
    print(f"{'='*60}")
    
    indices = text_to_indices(first_layer_text)
    print(f"First layer: {len(indices)} indices from {len(first_layer_text)} chars")
    
    original_score = score_text(first_layer_text)
    print(f"Original first-layer score: {original_score:.1f}")
    
    # Test various methods
    methods = [
        ("Prime - 1 (Page 56)", method_prime_minus_1(indices)),
        ("Prime only", method_prime_only(indices)),
        ("ADD Prime - 1", method_add_prime_minus_1(indices)),
        ("ADD Prime", method_add_prime(indices)),
    ]
    
    # Also test some constant shifts
    for k in [3, 19, 24]:
        methods.append((f"Shift({k})", method_constant_shift(indices, k)))
    
    results = []
    for name, result_indices in methods:
        text = indices_to_text(result_indices)
        score = score_text(text)
        results.append((name, score, text[:60]))
    
    # Sort by score
    results.sort(key=lambda x: -x[1])
    
    print(f"\nResults (sorted by score, original = {original_score:.1f}):")
    print("-" * 60)
    for name, score, text in results:
        diff = score - original_score
        marker = "✓" if score > original_score else " "
        print(f"{marker} {name}: Score = {score:.1f} ({diff:+.1f})")
        print(f"   {text}...")
    
    return results

def main():
    print("Testing Second Layer Methods on First-Layer Outputs")
    print("=" * 70)
    print("\nHypothesis: After SUB mod 29, apply prime-based shift as second layer")
    
    for page_num in range(5):
        if page_num in FIRST_LAYER_OUTPUTS:
            test_page(page_num, FIRST_LAYER_OUTPUTS[page_num])
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("\nIf any method scores higher than original, it may be the second layer.")
    print("If original scores best, the text may already be correct (just needs parsing).")

if __name__ == "__main__":
    main()

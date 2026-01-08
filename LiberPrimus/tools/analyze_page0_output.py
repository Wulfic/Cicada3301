
import collections

# First-Layer Output from Page 00 README
TEXT = "AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC" \
       "KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHE" \
       "AGOETHNTHEOCKLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWI" \
       "ASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEO" \
       "OTIXWTHEATHPHNGTHEAXATHPIASTHIPL"

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']
LETTER_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

def text_to_indices(text):
    result = []
    i = 0
    while i < len(text):
        for digraph in ['TH', 'NG', 'OE', 'AE', 'IO', 'EA', 'EO']:
            if text[i:i+len(digraph)] == digraph:
                result.append(LETTER_TO_IDX[digraph])
                i += len(digraph)
                break
        else:
            if text[i] in LETTER_TO_IDX:
                result.append(LETTER_TO_IDX[text[i]])
            i += 1
    return result

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def calculate_ioc(indices):
    counts = collections.Counter(indices)
    numerator = sum(n * (n - 1) for n in counts.values())
    N = len(indices)
    return numerator / (N * (N - 1)) if N > 1 else 0

def try_shifts(indices):
    print("\n--- Shift Cipher Analysis ---")
    for shift in range(29):
        shifted = [(x - shift) % 29 for x in indices]
        res_text = indices_to_text(shifted)
        # Simple heuristic: Look for common words like "THE"
        # Wait, the input has "THE" (TH-E is 2-18 or T-H-E 16-8-18)?
        # The runes have a 'TH' rune. The text representation uses 'TH' for rune 2.
        # So "THE" in the text representation is Rune 2 + Rune 18.
        # If I shift, characters change.
        # Let's just print first 50 chars for each shift
        print(f"Shift {shift:2d}: {res_text[:60]}")

def main():
    print(f"Analyzing text of length {len(TEXT)}")
    indices = text_to_indices(TEXT)
    print(f"Parsed into {len(indices)} runes")
    
    ioc = calculate_ioc(indices)
    print(f"IoC: {ioc:.4f}")
    
    # Frequency analysis
    counts = collections.Counter(indices)
    total = len(indices)
    print("\nTop 5 Runes:")
    for idx, count in counts.most_common(5):
        print(f"  {LETTERS[idx]}: {count} ({count/total*100:.1f}%)")

    try_shifts(indices)

if __name__ == "__main__":
    main()

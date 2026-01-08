
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

def main():
    indices = text_to_indices(TEXT)
    print(f"Loaded {len(indices)} runes from First Layer Output.")
    
    # Interleave Analysis
    print("\n--- Interleave Analysis ---")
    for n in range(2, 6):
        extracted = indices[::n]
        text = indices_to_text(extracted)
        print(f"Skip {n}: {text[:60]}")
    
    print("\n--- Reverse/Complement Analysis ---")
    functions = {
        "x -> (29 - x) % 29": lambda x: (29 - x) % 29, # Regular Atbash? No, Atbash is max - x.
        # Runes are 0-28. 28 maps to 0? 29-x -> 0->0, 1->28.
        # Let's try (28 - x)
        "x -> 28 - x": lambda x: 28 - x,
        "x -> (x + 14) % 29 (ROT13-like)": lambda x: (x + 14) % 29,
        "x -> (x * 3) % 29": lambda x: (x * 3) % 29,
    }
    
    for name, func in functions.items():
        try:
            transformed = [func(x) for x in indices]
            text = indices_to_text(transformed)
            print(f"{name}: {text[:60]}")
        except:
            pass
            
    # Check for "Words between hyphens" equivalent?
    # The output has no hyphens.
    
    # Check "Old English" dictionary match?
    # Simple check for "DOETH"
    print("\n--- Word Search ---")
    d_indices = text_to_indices("DOETH")
    print(f"Indices for DOETH: {d_indices}")

    if "DOETH" in TEXT:
        print("Found DOETH")
    if "GOETH" in TEXT:
        print("Found GOETH")

if __name__ == "__main__":
    main()


import os
import re

def main():
    with open(r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\key_search_corpus.txt", 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize to Uppercase Alpha only
    clean = re.sub(r'[^A-Z]', '', content.upper())
    
    # Target pattern: E O P A T H
    # indices: E(18), O(3), P(13), A(24), T(16), H(8)
    # Characters: E O P A T H
    
    target = "EOPATH"
    
    print(f"Searching for '{target}' in {len(clean)} chars...")
    
    matches = [m.start() for m in re.finditer(target, clean)]
    for m in matches:
        start = max(0, m - 10)
        end = min(len(clean), m + 20)
        context = clean[start:end]
        print(f"Match at {m}: ...{context}...")
        
    # Also search for 'FEOPATH'
    target2 = "FEOPATH"
    matches2 = [m.start() for m in re.finditer(target2, clean)]
    if matches2:
        print("FOUND FEOPATH!")
        for m in matches2:
            print(clean[m-10:m+20])
            
    # Search for WARNING key fragment: NG D G Y R Y N
    # NGDGYRYN
    target3 = "NGDGYRYN"
    print(f"Searching for '{target3}'...")
    matches3 = [m.start() for m in re.finditer(target3, clean)]
    for m in matches3:
        print(f"Match WARNING Key at {m}: {clean[m-10:m+20]}")

    # Search for relaxed WARNING key (G Y R Y)
    target4 = "GYRY" # G(6) Y(26) R(4) Y(26)
    print(f"Searching for '{target4}'...")
    matches4 = [m.start() for m in re.finditer(target4, clean)]
    for m in matches4:
         print(f"Match GYRY at {m}: {clean[m-10:m+20]}")

if __name__ == "__main__":
    main()

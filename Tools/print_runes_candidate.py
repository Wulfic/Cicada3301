
candidate = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIRSIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"
GP = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()

print(f"Length: {len(candidate)}") 
# Note: candidate string has digraphs `AE`, `EO`, `EA`, `TH`, `NG`, `OE`, `IA`.
# I need to parse it back to logical Runes.

def parse_to_runes(text):
    runes_out = []
    i = 0
    while i < len(text):
        # Check 3 chars (IA? No, IA is 2)
        # Check 2 chars
        if i + 1 < len(text):
            chunk2 = text[i:i+2]
            if chunk2 in GP:
                runes_out.append(chunk2)
                i += 2
                continue
        # Check 1 char
        chunk1 = text[i]
        if chunk1 in GP:
            runes_out.append(chunk1)
            i += 1
            continue
        # Fallback if char not in GP (e.g. V, K, Z -> mapped to U, C, S usually, but here string comes from GP chars)
        runes_out.append(chunk1)
        i += 1
    return runes_out

runes = parse_to_runes(candidate)
print(f"Parsed Runes Count: {len(runes)}")

print("Idx | Rune | Val | Analysis")
print("----|------|-----|---------")
for idx, r in enumerate(runes):
    try:
        val = GP.index(r)
    except:
        val = -1
    print(f"{idx:3} | {r:4} | {val:3} |")

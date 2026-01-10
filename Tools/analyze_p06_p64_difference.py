
import os

# Gematria Primus Mapping
gp_map = [
    ('ᚠ', 'F'), ('ᚢ', 'U'), ('ᚦ', 'TH'), ('ᚩ', 'O'), ('ᚱ', 'R'), ('ᚳ', 'C'), 
    ('ᚷ', 'G'), ('ᚹ', 'W'), ('ᚻ', 'H'), ('ᚾ', 'N'), ('ᛁ', 'I'), ('ᛂ', 'J'), 
    ('ᛇ', 'EO'), ('ᛈ', 'P'), ('ᛉ', 'X'), ('ᛋ', 'S'), ('ᛏ', 'T'), ('ᛒ', 'B'), 
    ('ᛖ', 'E'), ('ᛗ', 'M'), ('ᛚ', 'L'), ('ᛝ', 'NG'), ('ᛟ', 'OE'), ('ᛞ', 'D'), 
    ('ᚪ', 'A'), ('ᚫ', 'AE'), ('ᚣ', 'Y'), ('ᛡ', 'IA'), ('ᛠ', 'EA')
]

rune_to_index = {r: i for i, (r, _) in enumerate(gp_map)}
index_to_latin = {i: l for i, (_, l) in enumerate(gp_map)}

COMMON_WORDS = ["THE", "AND", "YOU", "ARE", "WHO", "FOR", "NOT", "BUT", "ALL", "THAT", "WITH", "THIS", "HAVE", "FROM"]

def clean_runes(text):
    return [c for c in text if c in rune_to_index]

def main():
    with open('LiberPrimus/pages/page_06/runes.txt', 'r', encoding='utf-8') as f:
        p6_text = f.read()
    with open('LiberPrimus/pages/page_64/runes.txt', 'r', encoding='utf-8') as f:
        p64_text = f.read()
    
    p6_runes = clean_runes(p6_text)
    p64_runes = clean_runes(p64_text)
    
    length = min(len(p6_runes), len(p64_runes))
    print(f"Comparing first {length} runes.")
    
    # Calculate difference
    diff_stream = []
    for i in range(length):
        r6 = rune_to_index[p6_runes[i]]
        r64 = rune_to_index[p64_runes[i]]
        
        # Try P64 - P6
        diff = (r64 - r6) % 29
        diff_stream.append(diff)
        
    # Analyze difference
    diff_text = "".join([index_to_latin[x] for x in diff_stream])
    print(f"Difference Stream (P64 - P06) Preview: {diff_text[:100]}...")
    
    # Check simple translation
    print("\nChecking Caesar Shifts on Difference Stream...")
    for shift in range(29):
        shifted = "".join([index_to_latin[(x + shift) % 29] for x in diff_stream])
        score = 0
        for w in COMMON_WORDS:
            if w in shifted:
                score += 1
        if score > 0:
            print(f"Shift {shift} Score {score}: {shifted[:50]}...")

    # Check Deor Keys on Difference Stream
    # Or just "IMPERIAL" / "DIAGONAL" on Difference Stream

if __name__ == "__main__":
    main()

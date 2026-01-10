
from collections import Counter

STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

TARGET_WORDS = [
    "CICADA", "INSTAR", "PRIMES", "EMERGE", "DEATH", "LIFE", "GOOD", "LUCK", "PATH", "DEOR", "KEY",
    "WHO", "DO", "WE", "BE", "LENGTH", "RATIO", "ENEMY", "FRIEND", "FOE", "COMMAND", "SYSTEM",
    "ONE", "TWO", "THREE", "THIRTY", "THREE", "ZERO", "ONE",  # 3301
    "LIBER", "PRIMUS", "ALGORITHM", "CIPHER", "SOLVE", "MAGI", "US", "THE"
]

def check_anagrams():
    stream_counts = Counter(STREAM)
    print(f"Stream Length: {len(STREAM)}")
    print(f"Counts: {stream_counts}")
    
    print("\n--- Anagram Check ---")
    for word in TARGET_WORDS:
        # Rune mapping approximation (Latin chars)
        # Note: STREAM contains 'OE', 'EO', 'TH', 'NG' represented as single runes in Runeglish but encoded as multigraphs in my string?
        # IMPORTANT: The STREAM string I have uses 'EO', 'AE' etc as DIGRAPHS (2 chars). 
        # But 'E' and 'O' are also single runes.
        # My Counter will count 'E', 'O' separately.
        # If the stream was generated from `to_letters`, it converted runes to Latin strings.
        # So 'EO' rune became "EO" string.
        # So counting letters is APPROXIMATELY correct, but 'TH' rune is 'T','H'.
        
        # Check if word can be formed
        w_counts = Counter(word)
        can_form = True
        for char, count in w_counts.items():
            if stream_counts[char] < count:
                can_form = False
                break
        
        if can_form:
            print(f"[YES] {word}")
        else:
            print(f"[NO ] {word} (Missing: {[c for c, n in w_counts.items() if stream_counts[c] < n]})")

if __name__ == "__main__":
    check_anagrams()

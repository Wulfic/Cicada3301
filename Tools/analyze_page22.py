"""
Deep analysis of Page 22 - unusual IoC 3.47!
"""
import os
from collections import Counter

GP_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
GP_LATIN = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 
            'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
            'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

def rune_to_index(rune):
    if rune in GP_RUNES:
        return GP_RUNES.index(rune)
    return None

def index_to_latin(idx):
    if 0 <= idx < 29:
        return GP_LATIN[idx]
    return '?'

def load_page(page_num):
    page_dir = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    subdir = f"page_{page_num:02d}"
    runes_path = os.path.join(page_dir, subdir, "runes.txt")
    if os.path.exists(runes_path):
        with open(runes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            rune_lines = [l for l in lines if not l.startswith('Note:')]
            runes = [c for c in ''.join(rune_lines) if c in GP_RUNES]
            return runes
    return []

def calculate_ioc(indices):
    n = len(indices)
    if n <= 1:
        return 0
    counts = Counter(indices)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return (numerator / denominator) * 29

def indices_to_latin(indices):
    return ''.join(index_to_latin(i) for i in indices)

def apply_vigenere(cipher_indices, key_indices, mode='sub'):
    result = []
    key_len = len(key_indices)
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]
        if mode == 'sub':
            p = (c - k) % 29
        else:
            p = (c + k) % 29
        result.append(p)
    return result

def main():
    print("="*60)
    print("PAGE 22 DEEP ANALYSIS")
    print("="*60)
    
    runes = load_page(22)
    cipher_indices = [rune_to_index(r) for r in runes if rune_to_index(r) is not None]
    
    print(f"Rune count: {len(cipher_indices)}")
    print(f"Raw IoC: {calculate_ioc(cipher_indices):.4f}")
    
    # Frequency analysis
    print("\n--- CIPHER FREQUENCY ---")
    counts = Counter(cipher_indices)
    for idx, count in sorted(counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {GP_LATIN[idx]:3} ({idx:2}): {count:2} = {count/len(cipher_indices)*100:.1f}%")
    
    # Try the best key from hill-climbing
    best_key = [25, 17, 0, 4, 18, 6, 15, 27, 16, 24, 26, 0, 21, 10, 15, 16, 12, 4, 13, 1, 2, 28, 5, 7, 21, 18, 17, 15, 0, 17, 13, 17, 15, 7, 25, 21, 9, 26, 5, 7, 12]
    
    plain = apply_vigenere(cipher_indices, best_key, 'sub')
    print(f"\n--- DECRYPTION WITH KEY LENGTH 41 (SUB) ---")
    print(f"IoC: {calculate_ioc(plain):.4f}")
    print(f"Full text:")
    print(indices_to_latin(plain))
    
    # Check for patterns
    text = indices_to_latin(plain)
    print(f"\n--- PATTERN ANALYSIS ---")
    
    # Look for repeated segments
    for length in [3, 4, 5, 6]:
        segments = {}
        for i in range(len(text) - length + 1):
            seg = text[i:i+length]
            if seg not in segments:
                segments[seg] = []
            segments[seg].append(i)
        
        repeats = {k: v for k, v in segments.items() if len(v) > 1}
        if repeats:
            print(f"Repeated {length}-grams:")
            for seg, positions in sorted(repeats.items(), key=lambda x: -len(x[1]))[:3]:
                print(f"  '{seg}' at positions {positions}")
    
    # Try shorter key lengths
    print("\n--- TRYING SHORTER KEY LENGTHS ---")
    for kl in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        for mode in ['sub', 'add']:
            # Try with simple repeating pattern
            for start in range(29):
                key = [(start + i) % 29 for i in range(kl)]
                plain = apply_vigenere(cipher_indices, key, mode)
                ioc = calculate_ioc(plain)
                if ioc > 1.5:
                    text = indices_to_latin(plain)
                    if 'THE' in text:
                        print(f"KL={kl}, Mode={mode}, Start={start}: IoC={ioc:.2f}, '{text[:40]}'")

if __name__ == "__main__":
    main()

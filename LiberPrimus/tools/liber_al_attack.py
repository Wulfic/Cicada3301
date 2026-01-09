#!/usr/bin/env python3
"""
Liber AL vel Legis Running Key Attack on Liber Primus
=====================================================
Tests Liber AL (The Book of the Law by Crowley) as a running key source.
Also tests self-referential approaches using solved LP pages.

The 2012 Cicada puzzle used Liber AL as a book code source!
"""

import os
import re
from collections import Counter

# Gematria Primus mapping
GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8,
    'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16,
    'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24,
    'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_INDEX_TO_RUNE = {v: k for k, v in GP_RUNE_TO_INDEX.items()}

# Runeglish to index mapping for key text
LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8,
    'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15, 'Z': 15, 'T': 16,
    'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'OE': 22, 'D': 23, 'A': 24,
    'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28, 'Q': 5
}

INDEX_TO_RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                       'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

# English word list for scoring
COMMON_WORDS = set([
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I', 'IT', 'FOR',
    'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT', 'THIS', 'BUT', 'HIS',
    'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE', 'OR', 'AN', 'WILL', 'MY',
    'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'SO', 'UP', 'OUT', 'IF',
    'ABOUT', 'WHO', 'GET', 'WHICH', 'GO', 'ME', 'WHEN', 'MAKE', 'CAN', 'LIKE',
    'TIME', 'NO', 'JUST', 'HIM', 'KNOW', 'TAKE', 'PEOPLE', 'INTO', 'YEAR', 'YOUR',
    'GOOD', 'SOME', 'COULD', 'THEM', 'SEE', 'OTHER', 'THAN', 'THEN', 'NOW', 'LOOK',
    'ONLY', 'COME', 'ITS', 'OVER', 'THINK', 'ALSO', 'BACK', 'AFTER', 'USE', 'TWO',
    'HOW', 'OUR', 'WORK', 'FIRST', 'WELL', 'WAY', 'EVEN', 'NEW', 'WANT', 'BECAUSE',
    'ANY', 'THESE', 'GIVE', 'DAY', 'MOST', 'US', 'IS', 'ARE', 'WAS', 'WERE', 'BEEN',
    # Cicada/mystical themed words
    'TRUTH', 'LIGHT', 'DARK', 'WISDOM', 'PRIMES', 'SACRED', 'DIVINE', 'KEY', 'SECRET',
    'KNOWLEDGE', 'HIDDEN', 'REVEAL', 'UNVEIL', 'PATH', 'SEEK', 'FIND', 'BELIEVE',
    'NOTHING', 'EVERYTHING', 'WORLD', 'SPIRIT', 'MIND', 'BODY', 'SOUL', 'DEATH',
    'LIFE', 'LOVE', 'LAW', 'WILL', 'STAR', 'SUN', 'MOON', 'GOD', 'GODS',
    # From Liber AL
    'NUIT', 'HADIT', 'HORUS', 'THELEMA', 'KHABS', 'KHU', 'AIWASS', 'NU'
])

def read_runes(filepath):
    """Read runes from a file, extracting only valid rune characters."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    runes = [c for c in content if c in GP_RUNE_TO_INDEX]
    return runes

def text_to_key_indices(text):
    """Convert English text to Gematria Primus indices for use as running key."""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        # Try two-character digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        # Try single character
        char = text[i]
        if char in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[char])
        i += 1
    return indices

def decrypt_sub(cipher_indices, key_indices):
    """Decrypt using SUB: plaintext = (cipher - key) mod 29"""
    result = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (c - k) % 29
        result.append(p)
    return result

def decrypt_add(cipher_indices, key_indices):
    """Decrypt using ADD: plaintext = (cipher + key) mod 29"""
    result = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        p = (c + k) % 29
        result.append(p)
    return result

def indices_to_runeglish(indices):
    """Convert Gematria indices to runeglish string."""
    return ''.join(INDEX_TO_RUNEGLISH[i] for i in indices)

def score_output(runeglish):
    """Score output based on English word matches."""
    score = 0
    text = runeglish.upper()
    
    # Check for word matches
    for word in COMMON_WORDS:
        if len(word) >= 3:
            count = text.count(word)
            score += count * len(word) * 10
    
    # Bonus for repeated patterns that could be words
    for length in range(3, 8):
        for i in range(len(text) - length):
            pattern = text[i:i+length]
            if text.count(pattern) > 2:
                score += length * 5
    
    return score

def calculate_ioc(indices):
    """Calculate Index of Coincidence."""
    if len(indices) < 2:
        return 0
    counter = Counter(indices)
    n = len(indices)
    numerator = sum(count * (count - 1) for count in counter.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator > 0 else 0

def load_liber_al(filepath):
    """Load Liber AL vel Legis text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_solved_pages():
    """Load all solved pages' plaintext for self-referential attack."""
    solved_pages = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                   55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68, 72, 73, 74]
    
    combined_text = ""
    base_dir = "c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages"
    
    for page_num in solved_pages:
        page_dir = os.path.join(base_dir, f"page_{page_num:02d}")
        readme_path = os.path.join(page_dir, "README.md")
        
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract plaintext sections
                if "SOLVED" in content or "Plaintext" in content or "Translation" in content:
                    combined_text += content + "\n"
    
    return combined_text

def run_liber_al_attack():
    """Main attack using Liber AL as running key."""
    print("="*70)
    print("LIBER AL VEL LEGIS RUNNING KEY ATTACK")
    print("="*70)
    
    # Load Liber AL
    liber_al_path = "c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/research/liber_al_vel_legis.txt"
    liber_al = load_liber_al(liber_al_path)
    
    # Convert to key indices
    key_indices = text_to_key_indices(liber_al)
    print(f"Liber AL key length: {len(key_indices)} indices")
    
    # Test pages to attack
    unsolved_pages = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    results = []
    
    for page_num in unsolved_pages:
        rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt"
        runes = read_runes(rune_path)
        
        if not runes:
            continue
        
        cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]
        
        # Test with different starting offsets in Liber AL
        best_score = 0
        best_result = None
        
        for offset in range(0, min(len(key_indices), 1000), 100):  # Try every 100 positions
            key_segment = key_indices[offset:]
            
            # SUB mode
            plain_sub = decrypt_sub(cipher_indices, key_segment)
            runeglish_sub = indices_to_runeglish(plain_sub)
            score_sub = score_output(runeglish_sub)
            
            if score_sub > best_score:
                best_score = score_sub
                best_result = ('SUB', offset, runeglish_sub[:100], plain_sub)
            
            # ADD mode  
            plain_add = decrypt_add(cipher_indices, key_segment)
            runeglish_add = indices_to_runeglish(plain_add)
            score_add = score_output(runeglish_add)
            
            if score_add > best_score:
                best_score = score_add
                best_result = ('ADD', offset, runeglish_add[:100], plain_add)
        
        if best_result:
            mode, offset, preview, indices = best_result
            ioc = calculate_ioc(indices)
            results.append((page_num, best_score, mode, offset, preview, ioc))
            
        print(f"Page {page_num:02d}: Best Score = {best_score}, Mode = {best_result[0] if best_result else 'N/A'}")
    
    print("\n" + "="*70)
    print("TOP RESULTS:")
    print("="*70)
    
    for page_num, score, mode, offset, preview, ioc in sorted(results, key=lambda x: -x[1])[:10]:
        print(f"\nPage {page_num:02d} | Score: {score} | Mode: {mode} | Offset: {offset} | IoC: {ioc:.4f}")
        print(f"Preview: {preview}")
    
    return results

def run_self_referential_attack():
    """Attack using solved LP pages' text as the running key."""
    print("\n" + "="*70)
    print("SELF-REFERENTIAL ATTACK (Solved Pages as Key)")
    print("="*70)
    
    # Load all solved page content
    solved_text = load_solved_pages()
    key_indices = text_to_key_indices(solved_text)
    print(f"Solved pages key length: {len(key_indices)} indices")
    
    if len(key_indices) < 100:
        print("Not enough solved text for attack")
        return []
    
    # Attack first few unsolved pages
    unsolved_pages = [18, 19, 20, 21, 22, 23]
    
    results = []
    
    for page_num in unsolved_pages:
        rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt"
        runes = read_runes(rune_path)
        
        if not runes:
            continue
        
        cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]
        
        # Test with different starting offsets
        best_score = 0
        best_result = None
        
        for offset in range(0, min(len(key_indices), 500), 50):
            key_segment = key_indices[offset:]
            
            plain_sub = decrypt_sub(cipher_indices, key_segment)
            runeglish_sub = indices_to_runeglish(plain_sub)
            score_sub = score_output(runeglish_sub)
            
            if score_sub > best_score:
                best_score = score_sub
                best_result = ('SUB', offset, runeglish_sub[:100], plain_sub)
            
            plain_add = decrypt_add(cipher_indices, key_segment)
            runeglish_add = indices_to_runeglish(plain_add)
            score_add = score_output(runeglish_add)
            
            if score_add > best_score:
                best_score = score_add
                best_result = ('ADD', offset, runeglish_add[:100], plain_add)
        
        if best_result:
            mode, offset, preview, indices = best_result
            ioc = calculate_ioc(indices)
            results.append((page_num, best_score, mode, offset, preview, ioc))
        
        print(f"Page {page_num:02d}: Best Score = {best_score}")
    
    return results

def run_chapter_specific_attack():
    """Test specific chapters of Liber AL on specific pages."""
    print("\n" + "="*70)
    print("CHAPTER-SPECIFIC ATTACK")
    print("="*70)
    
    liber_al_path = "c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/research/liber_al_vel_legis.txt"
    liber_al = load_liber_al(liber_al_path)
    
    # Split into chapters
    chapters = re.split(r'Chapter [IVX]+', liber_al)
    
    print(f"Found {len(chapters)-1} chapters")
    
    # Test each chapter against first unsolved page
    page_num = 18
    rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    runes = read_runes(rune_path)
    
    if not runes:
        print("Could not read page 18")
        return
    
    cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]
    
    for chap_num, chapter in enumerate(chapters[1:], 1):
        key_indices = text_to_key_indices(chapter)
        
        if len(key_indices) < 50:
            continue
        
        plain_sub = decrypt_sub(cipher_indices, key_indices)
        runeglish_sub = indices_to_runeglish(plain_sub)
        score_sub = score_output(runeglish_sub)
        
        plain_add = decrypt_add(cipher_indices, key_indices)
        runeglish_add = indices_to_runeglish(plain_add)
        score_add = score_output(runeglish_add)
        
        print(f"Chapter {chap_num}: SUB={score_sub}, ADD={score_add}")
        print(f"  SUB preview: {runeglish_sub[:60]}")
        print(f"  ADD preview: {runeglish_add[:60]}")

def test_sacred_number_offsets():
    """Test offsets based on sacred/significant numbers from Cicada."""
    print("\n" + "="*70)
    print("SACRED NUMBER OFFSET ATTACK")
    print("="*70)
    
    # Sacred numbers from Cicada/Thelema
    sacred_offsets = [
        11,    # 11 is sacred in Thelema
        13,    # Prime
        17,    # Prime  
        29,    # Prime, GP alphabet size
        31,    # Prime
        37,    # Prime
        41,    # Prime
        47,    # Prime
        53,    # Prime
        59,    # Prime
        61,    # 61 = "Nothing" in Hebrew gematria
        93,    # 93 = Thelema, Agape
        111,   # 111 = Aleph spelled out
        156,   # 156 = BABALON
        220,   # 220 = Liber AL number (CCXX)
        333,   # Choronzon
        418,   # Great Work number
        666,   # Number of the Beast
    ]
    
    liber_al_path = "c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/research/liber_al_vel_legis.txt"
    liber_al = load_liber_al(liber_al_path)
    key_indices = text_to_key_indices(liber_al)
    
    page_num = 18
    rune_path = f"c:/Users/tyler/Repos/Cicada3301/LiberPrimus/pages/page_{page_num:02d}/runes.txt"
    runes = read_runes(rune_path)
    
    if not runes:
        return
    
    cipher_indices = [GP_RUNE_TO_INDEX[r] for r in runes]
    
    print(f"Testing sacred number offsets on Page 18 ({len(runes)} runes)")
    
    for offset in sacred_offsets:
        if offset >= len(key_indices):
            continue
        
        key_segment = key_indices[offset:]
        
        plain_sub = decrypt_sub(cipher_indices, key_segment)
        runeglish_sub = indices_to_runeglish(plain_sub)
        score_sub = score_output(runeglish_sub)
        
        plain_add = decrypt_add(cipher_indices, key_segment)
        runeglish_add = indices_to_runeglish(plain_add)
        score_add = score_output(runeglish_add)
        
        best_mode = 'SUB' if score_sub >= score_add else 'ADD'
        best_score = max(score_sub, score_add)
        best_preview = runeglish_sub if score_sub >= score_add else runeglish_add
        
        if best_score > 100:  # Only show interesting results
            print(f"Offset {offset}: Score={best_score} ({best_mode})")
            print(f"  {best_preview[:80]}")

if __name__ == "__main__":
    # Run all attacks
    run_liber_al_attack()
    run_self_referential_attack()
    run_chapter_specific_attack()
    test_sacred_number_offsets()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

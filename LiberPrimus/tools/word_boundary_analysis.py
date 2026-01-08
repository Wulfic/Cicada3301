#!/usr/bin/env python3
"""
Word Boundary Analysis Tool
===========================

Apply first-layer decryption while preserving word boundaries (hyphens).
This allows us to analyze the decrypted output word-by-word.

Key insight: Word boundaries are preserved through encryption!
A 3-rune encrypted word MUST decrypt to a 3-rune plaintext word.
"""

from pathlib import Path
from collections import Counter

# Gematria Primus mappings
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
RUNE_TO_INDEX.setdefault("ᛄ", 11)  # Alternate J rune
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# Key lengths (best performing for each page)
BEST_KEYS = {
    0: 113, 1: 71, 2: 83, 3: 83, 4: 103, 5: 71,
    6: 83, 7: 83, 8: 71, 9: 71, 10: 137, 11: 83
}

def get_liber_primus_root():
    return Path(__file__).resolve().parent.parent

def load_page_raw(page_num: int) -> str:
    """Load raw rune text with word boundaries preserved."""
    pages_root = get_liber_primus_root() / "pages"
    rune_path = pages_root / f"page_{page_num:02d}" / "runes.txt"
    if not rune_path.exists():
        raise ValueError(f"Page {page_num} not found at {rune_path}")
    return rune_path.read_text(encoding="utf-8")

def parse_with_boundaries(raw_text: str) -> list:
    """
    Parse rune text preserving word boundaries.
    Returns list of words, where each word is a list of rune indices.
    """
    words = []
    current_word = []
    
    for char in raw_text:
        if char in RUNE_TO_INDEX:
            current_word.append(RUNE_TO_INDEX[char])
        elif char == '-' or char == ' ' or char == '\n':
            if current_word:
                words.append(current_word)
                current_word = []
        elif char in '.&%$§:/':  # Punctuation - also word boundary
            if current_word:
                words.append(current_word)
                current_word = []
    
    if current_word:
        words.append(current_word)
    
    return words

def compute_ioc(indices, key_length):
    """Compute Index of Coincidence for a key length."""
    if key_length < 1 or key_length >= len(indices):
        return 0.0
    
    cosets = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        cosets[i % key_length].append(idx)
    
    ioc_sum = 0.0
    valid_cosets = 0
    
    for coset in cosets:
        n = len(coset)
        if n < 2:
            continue
        freqs = Counter(coset)
        ioc = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
        ioc_sum += ioc
        valid_cosets += 1
    
    return ioc_sum / valid_cosets if valid_cosets > 0 else 0.0

def generate_frequency_key(cipher_indices, key_length):
    """Generate key assuming most common symbol decrypts to E (index 18)."""
    key = []
    for i in range(key_length):
        coset = [cipher_indices[j] for j in range(i, len(cipher_indices), key_length)]
        if not coset:
            key.append(0)
            continue
        most_common = Counter(coset).most_common(1)[0][0]
        key.append((most_common - 18) % 29)  # Assume most common -> E
    return key

def decrypt_sub(cipher_indices, key):
    """Decrypt using SUB: plaintext = (cipher - key) mod 29"""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key[i % len(key)]
        plaintext.append((c - k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert indices to letter representation."""
    return ''.join(LETTERS[i] for i in indices)

def decrypt_words(words, key):
    """
    Decrypt each word separately, maintaining word boundaries.
    Key position is tracked continuously across words.
    """
    decrypted_words = []
    key_pos = 0
    
    for word in words:
        decrypted_word = []
        for idx in word:
            k = key[key_pos % len(key)]
            decrypted_word.append((idx - k) % 29)
            key_pos += 1
        decrypted_words.append(decrypted_word)
    
    return decrypted_words

def analyze_page(page_num: int, key_length: int = None):
    """Analyze a page with word boundaries preserved."""
    print(f"\n{'='*70}")
    print(f"WORD BOUNDARY ANALYSIS - PAGE {page_num}")
    print(f"{'='*70}\n")
    
    raw_text = load_page_raw(page_num)
    words = parse_with_boundaries(raw_text)
    
    # Flatten for key generation
    all_indices = [idx for word in words for idx in word]
    
    if key_length is None:
        key_length = BEST_KEYS.get(page_num, 71)
    
    print(f"Total runes: {len(all_indices)}")
    print(f"Total words: {len(words)}")
    print(f"Word lengths: {[len(w) for w in words[:30]]}...")
    print(f"Key length: {key_length}")
    
    # Generate and decrypt
    key = generate_frequency_key(all_indices, key_length)
    decrypted_words = decrypt_words(words, key)
    
    # Convert to text with word boundaries
    word_texts = [indices_to_text(w) for w in decrypted_words]
    
    print(f"\nDecrypted words (first 50):")
    print("-" * 70)
    for i, word in enumerate(word_texts[:50]):
        print(f"{i+1:3}: {word}")
    
    # Word length statistics
    length_freq = Counter(len(w) for w in word_texts)
    print(f"\nWord length distribution:")
    for length in sorted(length_freq.keys()):
        count = length_freq[length]
        print(f"  Length {length}: {count} words")
    
    # Look for common English patterns
    print(f"\nLooking for common patterns:")
    
    # Single-character words (should be A, I, O or digraphs)
    single_chars = [w for w in word_texts if len(w) <= 2]
    print(f"  Single-char/digraph words: {single_chars[:20]}")
    
    # Two-rune words (could be: TO, IN, OF, IS, IT, BE, WE, etc.)
    two_rune = [w for w in word_texts if len(w) in [2, 3, 4]]  # 2-4 letters
    print(f"  Short words (2-4 letters): {two_rune[:20]}")
    
    # Words ending in TH (common in Old English)
    th_words = [w for w in word_texts if w.endswith('TH')]
    print(f"  Words ending in TH: {th_words[:15]}")
    
    # Words containing THE
    the_words = [w for w in word_texts if 'THE' in w]
    print(f"  Words containing THE: {the_words[:15]}")
    
    # Words with -ING/-NG endings
    ing_words = [w for w in word_texts if w.endswith('NG') or w.endswith('ING')]
    print(f"  Words ending in NG/ING: {ing_words[:15]}")
    
    # Words with -ETH endings (Old English)
    eth_words = [w for w in word_texts if w.endswith('ETH')]
    print(f"  Words ending in ETH: {eth_words[:15]}")
    
    return word_texts, decrypted_words

def compare_word_structures(page1: int, page2: int):
    """Compare word length patterns between two pages."""
    print(f"\n{'='*70}")
    print(f"COMPARING WORD STRUCTURES: Page {page1} vs Page {page2}")
    print(f"{'='*70}\n")
    
    words1 = parse_with_boundaries(load_page_raw(page1))
    words2 = parse_with_boundaries(load_page_raw(page2))
    
    lengths1 = [len(w) for w in words1]
    lengths2 = [len(w) for w in words2]
    
    print(f"Page {page1}: {len(words1)} words, lengths: {lengths1[:30]}...")
    print(f"Page {page2}: {len(words2)} words, lengths: {lengths2[:30]}...")
    
    # Find matching patterns
    matches = 0
    for i in range(min(len(lengths1), len(lengths2))):
        if lengths1[i] == lengths2[i]:
            matches += 1
    
    print(f"\nMatching word lengths at same position: {matches}/{min(len(lengths1), len(lengths2))}")
    
    # Look for identical word length sequences
    for seq_len in range(5, 15):
        for i in range(len(lengths1) - seq_len):
            seq1 = lengths1[i:i+seq_len]
            for j in range(len(lengths2) - seq_len):
                seq2 = lengths2[j:j+seq_len]
                if seq1 == seq2:
                    print(f"  Found matching sequence of {seq_len} at positions {i}, {j}: {seq1}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        page_num = int(sys.argv[1])
        key_length = int(sys.argv[2]) if len(sys.argv) > 2 else None
        analyze_page(page_num, key_length)
    else:
        # Default: analyze first few pages
        for page in [0, 1, 2]:
            analyze_page(page)
        
        # Compare Page 0 with solved Page 56
        print("\n\n" + "="*70)
        print("COMPARING WITH SOLVED PAGE 56")
        print("="*70)
        compare_word_structures(0, 56)

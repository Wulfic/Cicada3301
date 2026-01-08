#!/usr/bin/env python3
"""
Word-Boundary Aware Solver
Uses the fact that hyphens/dots mark word boundaries in the Liber Primus.
Decrypts preserving word structure and scores based on word validity.
"""

import os
import sys
from pathlib import Path
from collections import Counter
import random

# Gematria Primus mappings
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

# Common short English words that might appear
COMMON_WORDS = {
    'A', 'I', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN',
    'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US',
    'WE', 'ALL', 'AND', 'ARE', 'BUT', 'CAN', 'FOR', 'HAS', 'HIM', 'HIS',
    'HOW', 'ITS', 'MAY', 'NEW', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT',
    'OWN', 'SAY', 'SHE', 'THE', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'YOU',
    'FIND', 'FROM', 'HAVE', 'INTO', 'JUST', 'KNOW', 'LIKE', 'MAKE', 'MANY',
    'MORE', 'MUST', 'ONLY', 'OVER', 'SELF', 'SOME', 'SUCH', 'TAKE', 'THAN',
    'THAT', 'THEM', 'THEN', 'THIS', 'THUS', 'UNTO', 'UPON', 'WHAT', 'WHEN',
    'WILL', 'WITH', 'YOUR', 'BEING', 'THEIR', 'THERE', 'THESE', 'THING',
    'THOSE', 'TRUTH', 'WHICH', 'WITHIN', 'DIVINITY', 'EMERGE', 'CIRCUMFERENCE',
    # Old English words
    'THEE', 'THOU', 'THINE', 'HATH', 'DOTH', 'DOETH', 'SHALT', 'WILT', 'ART',
    'THY', 'YE', 'UNTO', 'WHEREIN', 'THEREOF', 'WHEREOF', 'HEREBY', 'THEREBY',
    # Thematic words
    'SHED', 'SURFACE', 'INSTAR', 'PRIMUS', 'LIBER', 'WISDOM', 'LIGHT',
    'KNOWLEDGE', 'PATH', 'SEEK', 'FOUND', 'BECOME', 'WORLD', 'MIND',
}

def load_runes(page_num):
    """Load runes from a page file."""
    page_dir = Path(__file__).parent.parent / "pages" / f"page_{page_num:02d}"
    runes_file = page_dir / "runes.txt"
    
    if not runes_file.exists():
        return None
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        return f.read()

def parse_words(rune_text):
    """Parse rune text into words, extracting word boundaries."""
    words = []
    current_word = []
    
    for char in rune_text:
        if char in RUNE_MAP:
            current_word.append(RUNE_MAP[char])
        elif char in '-.' or char == ' ':
            if current_word:
                words.append(current_word)
                current_word = []
        elif char in '\n\r':
            if current_word:
                words.append(current_word)
                current_word = []
        elif char == '•':  # Alternate word separator
            if current_word:
                words.append(current_word)
                current_word = []
    
    if current_word:
        words.append(current_word)
    
    return words

def decrypt_word(word_indices, key, key_offset):
    """Decrypt a single word using part of the key."""
    result = []
    for i, c in enumerate(word_indices):
        k = key[(key_offset + i) % len(key)]
        p = (c - k) % 29
        result.append(p)
    return result

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(LETTERS[i] for i in indices)

def score_word(word_text):
    """Score a decrypted word for English likelihood."""
    # Flatten digraphs for matching
    flat = word_text
    for digraph in ['TH', 'NG', 'IO', 'EO', 'EA', 'AE', 'OE']:
        flat = flat.replace(digraph, '@')
    
    score = 0
    
    # Exact match with common word
    if word_text in COMMON_WORDS:
        score += 100 * len(word_text)
    
    # Partial matches
    for common in COMMON_WORDS:
        if common in word_text and len(common) >= 3:
            score += 20
    
    # English letter frequency approximation
    vowel_count = sum(1 for c in word_text if c in 'AEIOU')
    letter_count = len(flat)
    
    if letter_count > 0:
        vowel_ratio = vowel_count / letter_count
        # English has ~38% vowels
        if 0.25 < vowel_ratio < 0.55:
            score += 10
        else:
            score -= 10
    
    # Penalize unlikely patterns
    if 'XX' in word_text or 'QQ' in word_text:
        score -= 20
    
    # Bonus for common letter patterns
    for pattern in ['TH', 'HE', 'AN', 'IN', 'ER', 'ND', 'RE', 'ED', 'ES', 'EN']:
        score += word_text.count(pattern) * 5
    
    return score

def hill_climb_word(word_indices, key_length, iterations=500):
    """Find the best key portion for a single word."""
    best_key = [random.randint(0, 28) for _ in range(min(key_length, len(word_indices)))]
    best_decrypted = decrypt_word(word_indices, best_key, 0)
    best_text = indices_to_text(best_decrypted)
    best_score = score_word(best_text)
    
    for _ in range(iterations):
        new_key = best_key.copy()
        pos = random.randint(0, len(new_key) - 1)
        new_key[pos] = random.randint(0, 28)
        
        new_decrypted = decrypt_word(word_indices, new_key, 0)
        new_text = indices_to_text(new_decrypted)
        new_score = score_word(new_text)
        
        if new_score > best_score:
            best_key = new_key
            best_text = new_text
            best_score = new_score
    
    return best_key, best_text, best_score

def analyze_page_with_words(page_num):
    """Analyze a page using word boundary information."""
    rune_text = load_runes(page_num)
    if not rune_text:
        print(f"Could not load page {page_num}")
        return
    
    print(f"\n{'='*70}")
    print(f"WORD-AWARE ANALYSIS: Page {page_num}")
    print(f"{'='*70}")
    
    # Parse into words
    words = parse_words(rune_text)
    print(f"Found {len(words)} words")
    
    # Show word length distribution
    word_lengths = [len(w) for w in words]
    length_counts = Counter(word_lengths)
    print(f"Word length distribution: {dict(sorted(length_counts.items()))}")
    
    # Total rune count
    total_runes = sum(len(w) for w in words)
    print(f"Total runes: {total_runes}")
    
    # Try to decrypt each word independently
    print("\n--- Word-by-word decryption attempts ---")
    
    decoded_words = []
    for i, word in enumerate(words[:20]):  # First 20 words
        # Try all possible single-value keys (0-28)
        best_text = None
        best_score = -1000
        best_key = None
        
        for k in range(29):
            decrypted = [(c - k) % 29 for c in word]
            text = indices_to_text(decrypted)
            s = score_word(text)
            if s > best_score:
                best_score = s
                best_text = text
                best_key = k
        
        decoded_words.append((best_text, best_score, best_key))
        
        # Show if it looks like a valid word
        is_match = best_text in COMMON_WORDS
        marker = "✓" if is_match else " "
        print(f"  Word {i+1} (len={len(word)}): {best_text:15} score={best_score:4} key={best_key:2} {marker}")
    
    # Try common key patterns
    print("\n--- Testing common key values ---")
    
    for test_key in [0, 1, 2, 7, 11, 13, 17, 19, 23, 29 % 29]:
        decoded = []
        for word in words[:10]:
            decrypted = [(c - test_key) % 29 for c in word]
            decoded.append(indices_to_text(decrypted))
        print(f"Key={test_key:2}: {' '.join(decoded[:8])}")
    
    return words

def find_word_matches(page_num, target_word):
    """Find positions where a target word could be in the ciphertext."""
    rune_text = load_runes(page_num)
    if not rune_text:
        return []
    
    words = parse_words(rune_text)
    
    # Convert target word to indices
    target_indices = []
    i = 0
    while i < len(target_word):
        # Check for digraphs
        found = False
        for j, letter in enumerate(LETTERS):
            if target_word[i:].startswith(letter):
                target_indices.append(j)
                i += len(letter)
                found = True
                break
        if not found:
            i += 1
    
    target_len = len(target_indices)
    matches = []
    
    for word_idx, word in enumerate(words):
        if len(word) == target_len:
            # Calculate what key would decrypt this word to target
            key = [(word[i] - target_indices[i]) % 29 for i in range(target_len)]
            matches.append({
                'word_idx': word_idx,
                'cipher_word': word,
                'key': key,
                'target': target_word
            })
    
    return matches

def main():
    print("=" * 70)
    print("WORD-BOUNDARY AWARE SOLVER")
    print("=" * 70)
    
    # Analyze pages with word structure
    for page in [8, 13, 43, 46]:
        analyze_page_with_words(page)
    
    # Search for "THE" pattern
    print("\n" + "=" * 70)
    print("SEARCHING FOR 'THE' IN WORD POSITIONS")
    print("=" * 70)
    
    for page in [8, 13, 43, 46]:
        matches = find_word_matches(page, "THE")
        print(f"\nPage {page}: Found {len(matches)} words with length 2 (could be THE)")
        for m in matches[:5]:
            key_str = ','.join(map(str, m['key']))
            print(f"  Word {m['word_idx']}: cipher={m['cipher_word']} -> key=[{key_str}]")

if __name__ == "__main__":
    main()

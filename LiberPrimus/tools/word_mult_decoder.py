#!/usr/bin/env python3
"""
COMPREHENSIVE WORD-MULTIPLIER DECODER

Applies the optimal (multiplier, offset) for each page using word-index based keys.
Key formula: key = (word_index × multiplier + offset) mod 29

This tool:
1. Finds optimal parameters for each page
2. Decodes with those parameters
3. Marks recognized English words
4. Saves results to files
"""

import os
from pathlib import Path
from collections import Counter
import json

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

# Comprehensive English word list
COMMON_WORDS = {
    # One letter
    'A', 'I',
    # Two letters
    'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 
    'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
    # Three letters  
    'ALL', 'AND', 'ARE', 'BUT', 'CAN', 'FOR', 'HAS', 'HIM', 'HIS', 'HOW', 
    'ITS', 'MAY', 'NEW', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT', 'OWN', 
    'SAY', 'SHE', 'THE', 'TOO', 'TWO', 'USE', 'WAY', 'WHO', 'YOU', 'YET',
    'THY', 'YEA', 'NAY', 'ANY', 'OWE', 'OWN',
    # Four letters
    'FIND', 'FROM', 'HAVE', 'INTO', 'JUST', 'KNOW', 'LIKE', 'MAKE', 'MANY',
    'MORE', 'MUST', 'ONLY', 'OVER', 'PATH', 'SELF', 'SOME', 'SUCH', 'TAKE', 
    'THAN', 'THAT', 'THEM', 'THEN', 'THIS', 'THUS', 'UNTO', 'UPON', 'WHAT', 
    'WHEN', 'WILL', 'WITH', 'YOUR', 'SEEK', 'THOU', 'THEE', 'HATH', 'DOTH',
    'THEY', 'ALSO', 'BEEN', 'EACH', 'WERE', 'SAID', 'MADE', 'BOTH',
    # Five+ letters
    'BEING', 'THEIR', 'THERE', 'THESE', 'THING', 'THOSE', 'TRUTH', 'WHICH', 
    'THINE', 'SHALT', 'SHALL', 'WORLD', 'LIGHT', 'WISDOM', 'PRIME', 'PRIMES',
    'WITHIN', 'DIVINITY', 'EMERGE', 'KNOWLEDGE', 'BECOME', 'CIRCUMFERENCE',
    'CONSUMPTION', 'INSTRUCTION', 'ADMONITION', 'INSTAR', 'SURFACE',
    'PILGRIM', 'JOURNEY', 'SACRED', 'SECRET', 'HIDDEN', 'AWAKEN'
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
    """Parse rune text into word index lists."""
    words = []
    current_word = []
    
    for char in rune_text:
        if char in RUNE_MAP:
            current_word.append(RUNE_MAP[char])
        elif char in '-. \n\r':
            if current_word:
                words.append(current_word)
                current_word = []
    
    if current_word:
        words.append(current_word)
    
    return words

def decrypt_word(indices, key):
    """Decrypt a word with given key."""
    return [(c - key) % 29 for c in indices]

def indices_to_text(indices):
    """Convert indices to text."""
    return ''.join(LETTERS[i] for i in indices)

def score_word(text):
    """Score a word. Higher if it's a known English word."""
    if text.upper() in COMMON_WORDS:
        return len(text) * 100
    return 0

def find_optimal_params(words):
    """Find optimal (mult, offset) for a page."""
    best_mult = 1
    best_offset = 0
    best_score = 0
    best_words_found = []
    
    for mult in range(1, 29):
        for offset in range(29):
            total_score = 0
            found_words = []
            
            for word_idx, word in enumerate(words):
                key = (word_idx * mult + offset) % 29
                decrypted = decrypt_word(word, key)
                text = indices_to_text(decrypted)
                score = score_word(text)
                total_score += score
                
                if score > 0:
                    found_words.append((word_idx, text, key))
            
            if total_score > best_score:
                best_score = total_score
                best_mult = mult
                best_offset = offset
                best_words_found = found_words
    
    return best_mult, best_offset, best_score, best_words_found

def decode_page(words, mult, offset):
    """Decode all words with given parameters."""
    decoded_words = []
    word_info = []
    
    for word_idx, word in enumerate(words):
        key = (word_idx * mult + offset) % 29
        decrypted = decrypt_word(word, key)
        text = indices_to_text(decrypted)
        is_english = text.upper() in COMMON_WORDS
        
        decoded_words.append({
            'index': word_idx,
            'cipher': [LETTERS[i] for i in word],
            'plaintext': text,
            'key': key,
            'is_english': is_english
        })
    
    return decoded_words

def format_output(decoded_words, mark_english=True):
    """Format decoded words for display."""
    result = []
    
    for i, w in enumerate(decoded_words):
        text = w['plaintext']
        if mark_english and w['is_english']:
            text = f"[{text}]"
        result.append(text)
    
    # Format into lines of ~60 chars
    lines = []
    current_line = []
    current_len = 0
    
    for word in result:
        word_len = len(word) + 1  # +1 for space
        if current_len + word_len > 60 and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_len = word_len
        else:
            current_line.append(word)
            current_len += word_len
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def analyze_all_pages():
    """Analyze all unsolved pages and save results."""
    
    print("=" * 70)
    print("COMPREHENSIVE WORD-MULTIPLIER DECODING")
    print("=" * 70)
    
    results = {}
    
    for page_num in range(8, 57):
        rune_text = load_runes(page_num)
        if not rune_text:
            continue
        
        words = parse_words(rune_text)
        if len(words) < 10:
            continue
        
        mult, offset, score, found_words = find_optimal_params(words)
        decoded = decode_page(words, mult, offset)
        
        results[page_num] = {
            'multiplier': mult,
            'offset': offset,
            'score': score,
            'word_count': len(words),
            'english_words': [w['plaintext'] for w in decoded if w['is_english']],
            'decoded_words': decoded
        }
        
        # Print summary
        eng_words = ', '.join(results[page_num]['english_words'][:8])
        print(f"Page {page_num:2d}: mult={mult:2d}, offset={offset:2d}, "
              f"score={score:4d}, words={len(words):2d}")
        if eng_words:
            print(f"         English: {eng_words}")
    
    return results

def save_decoded_pages(results):
    """Save decoded pages to files."""
    
    output_dir = Path(__file__).parent / "results" / "word_mult_decode"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save summary
    summary_file = output_dir / "summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("WORD-MULTIPLIER DECODING SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write("Key formula: key = (word_index × multiplier + offset) mod 29\n\n")
        
        for page_num in sorted(results.keys()):
            r = results[page_num]
            f.write(f"Page {page_num:2d}: mult={r['multiplier']:2d}, "
                   f"offset={r['offset']:2d}, score={r['score']:4d}\n")
            f.write(f"  English words: {', '.join(r['english_words'])}\n\n")
    
    # Save individual page decodes
    for page_num, r in results.items():
        page_file = output_dir / f"page_{page_num:02d}_decoded.txt"
        
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(f"PAGE {page_num} DECODED\n")
            f.write(f"Multiplier: {r['multiplier']}\n")
            f.write(f"Offset: {r['offset']}\n")
            f.write(f"Score: {r['score']}\n")
            f.write(f"English words found: {', '.join(r['english_words'])}\n")
            f.write("=" * 70 + "\n\n")
            
            # Format decoded text
            decoded = r['decoded_words']
            f.write(format_output(decoded, mark_english=True))
            f.write("\n\n")
            
            # Detailed word-by-word
            f.write("=" * 70 + "\n")
            f.write("WORD-BY-WORD DETAIL\n")
            f.write("=" * 70 + "\n")
            for w in decoded:
                cipher_str = ''.join(w['cipher'])
                marker = "✓" if w['is_english'] else " "
                f.write(f"{w['index']:3d}: {cipher_str:15} -> {w['plaintext']:15} "
                       f"(key={w['key']:2d}) {marker}\n")
    
    print(f"\nResults saved to: {output_dir}")
    
    # Save JSON for programmatic use
    json_file = output_dir / "all_results.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        # Convert to serializable format
        json_data = {}
        for page_num, r in results.items():
            json_data[str(page_num)] = {
                'multiplier': r['multiplier'],
                'offset': r['offset'],
                'score': r['score'],
                'word_count': r['word_count'],
                'english_words': r['english_words']
            }
        json.dump(json_data, f, indent=2)

def show_best_pages(results, top_n=10):
    """Show the best scoring pages in detail."""
    
    print("\n" + "=" * 70)
    print(f"TOP {top_n} BEST-SCORING PAGES")
    print("=" * 70)
    
    sorted_pages = sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)
    
    for page_num, r in sorted_pages[:top_n]:
        print(f"\n{'='*70}")
        print(f"PAGE {page_num} - mult={r['multiplier']}, offset={r['offset']}, "
              f"score={r['score']}")
        print(f"{'='*70}")
        print(f"English words: {', '.join(r['english_words'])}")
        print("\nDecoded text:")
        print(format_output(r['decoded_words']))

if __name__ == '__main__':
    results = analyze_all_pages()
    save_decoded_pages(results)
    show_best_pages(results, top_n=5)

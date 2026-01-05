#!/usr/bin/env python3
"""
Extract all recognizable English words from Page 1 SUB-71 output
Maybe the message is sparse/fragmented but the words are there
"""

from pathlib import Path
import re

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

# Common English words to search for
DICTIONARY = set([
    # Articles, pronouns
    'THE', 'A', 'AN', 'THIS', 'THAT', 'THESE', 'THOSE', 'I', 'YOU', 'HE', 'SHE', 'IT', 'WE', 'THEY',
    'ME', 'HIM', 'HER', 'US', 'THEM', 'MY', 'YOUR', 'HIS', 'ITS', 'OUR', 'THEIR',
    # Verbs
    'IS', 'ARE', 'WAS', 'WERE', 'BE', 'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'DO', 'DOES', 'DID',
    'WILL', 'WOULD', 'SHALL', 'SHOULD', 'MAY', 'MIGHT', 'MUST', 'CAN', 'COULD',
    'GO', 'COME', 'SEE', 'KNOW', 'THINK', 'TAKE', 'MAKE', 'GET', 'GIVE', 'FIND', 'TELL', 'ASK',
    # Prepositions
    'IN', 'ON', 'AT', 'TO', 'FOR', 'WITH', 'FROM', 'BY', 'ABOUT', 'OF', 'THROUGH', 'OVER', 'UNDER',
    'BETWEEN', 'AMONG', 'WITHIN', 'WITHOUT',
    # Conjunctions
    'AND', 'OR', 'BUT', 'SO', 'YET', 'FOR', 'NOR', 'AS', 'IF', 'WHEN', 'WHERE', 'WHILE', 'THOUGH',
    # Cicada-related words
    'WISDOM', 'KNOWLEDGE', 'TRUTH', 'DIVINE', 'SACRED', 'SECRET', 'HIDDEN', 'PATH', 'WAY',
    'SEEK', 'FIND', 'UNDERSTAND', 'LEARN', 'TEACH', 'GUIDE', 'LEAD', 'FOLLOW',
    'LIGHT', 'DARK', 'SHADOW', 'VOID', 'CHAOS', 'ORDER', 'HARMONY', 'BALANCE',
    'RUNE', 'GLYPH', 'SYMBOL', 'SIGN', 'MARK', 'CODE', 'CIPHER', 'KEY',
    'PRIMUS', 'LIBER', 'BOOK', 'TEXT', 'WORD', 'LETTER', 'NUMBER',
    'QUESTION', 'ANSWER', 'RIDDLE', 'PUZZLE', 'MYSTERY', 'ENIGMA',
    # Common words
    'ALL', 'SOME', 'NONE', 'MANY', 'FEW', 'MUCH', 'LITTLE', 'MORE', 'LESS', 'MOST', 'LEAST',
    'GOOD', 'BAD', 'RIGHT', 'WRONG', 'TRUE', 'FALSE', 'NEW', 'OLD', 'GREAT', 'SMALL',
    'MAN', 'MEN', 'WOMAN', 'WOMEN', 'PEOPLE', 'PERSON', 'THING', 'TIME', 'LIFE', 'DEATH',
    'WORLD', 'EARTH', 'SKY', 'SEA', 'FIRE', 'WATER', 'AIR', 'WIND',
    'BEGINNING', 'END', 'START', 'FINISH', 'FIRST', 'LAST', 'BEFORE', 'AFTER', 'NOW', 'THEN',
    'HERE', 'THERE', 'EVERYWHERE', 'NOWHERE', 'SOMEWHERE',
    'WHO', 'WHAT', 'WHEN', 'WHERE', 'WHY', 'HOW', 'WHICH',
    'NOT', 'NO', 'YES', 'NEVER', 'ALWAYS', 'SOMETIMES', 'OFTEN', 'RARELY',
    'POWER', 'FORCE', 'ENERGY', 'STRENGTH', 'WEAK', 'STRONG',
    'MIND', 'BODY', 'SOUL', 'SPIRIT', 'HEART', 'THOUGHT', 'FEELING', 'SENSE',
    'ABOVE', 'BELOW', 'INSIDE', 'OUTSIDE', 'NEAR', 'FAR', 'LEFT', 'RIGHT',
    'SAME', 'DIFFERENT', 'ALIKE', 'UNLIKE', 'SIMILAR', 'OPPOSITE',
    'WELCOME', 'FAREWELL', 'GREETINGS', 'HELLO', 'GOODBYE',
])

def load_page1():
    repo_root = Path(__file__).parent.parent
    trans_path = repo_root / "2014" / "Liber Primus" / "runes in text format.txt"
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_runes = segments[0]
    page1_indices = [RUNE_TO_INDEX[c] for c in page1_runes if c in RUNE_TO_INDEX]
    
    return page1_indices

def decrypt_sub(cipher_indices, key_indices):
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def indices_to_text(indices):
    return "".join(LETTERS[idx] for idx in indices)

BEST_KEY_71 = [13, 19, 14, 4, 4, 11, 24, 23, 13, 8, 26, 19, 6, 0, 4, 18, 13, 24, 14, 10, 0, 10, 16, 18, 25, 20, 26, 1, 4, 11, 19, 6, 7, 23, 2, 3, 0, 9, 15, 6, 27, 7, 1, 7, 8, 3, 22, 3, 24, 2, 15, 24, 11, 16, 8, 19, 12, 3, 27, 13, 6, 12, 21, 1, 1, 3, 8, 19, 25, 19, 7]

def extract_words(text):
    """Find all dictionary words in the text"""
    text = text.upper()
    found_words = []
    
    for word in DICTIONARY:
        count = text.count(word)
        if count > 0:
            found_words.append((word, count))
    
    return found_words

def find_word_positions(text, word):
    """Find all positions of a word in text"""
    positions = []
    start = 0
    while True:
        pos = text.find(word, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions

def extract_context(text, pos, word_len, context_len=10):
    """Extract context around a position"""
    start = max(0, pos - context_len)
    end = min(len(text), pos + context_len + word_len)
    before = text[start:pos]
    match = text[pos:pos+word_len]
    after = text[pos+word_len:end]
    return before + "[" + match + "]" + after

def main():
    print("=" * 80)
    print("PAGE 1 - EXTRACTING RECOGNIZABLE ENGLISH WORDS")
    print("=" * 80)
    
    cipher_indices = load_page1()
    plaintext_indices = decrypt_sub(cipher_indices, BEST_KEY_71)
    plaintext_text = indices_to_text(plaintext_indices)
    
    print(f"\nFull SUB-71 output ({len(plaintext_text)} chars):")
    print(plaintext_text)
    
    # Find all dictionary words
    found_words = extract_words(plaintext_text)
    found_words_sorted = sorted(found_words, key=lambda x: x[1], reverse=True)
    
    print("\n" + "=" * 80)
    print("DICTIONARY WORDS FOUND")
    print("=" * 80)
    
    print(f"\nTotal unique words found: {len(found_words_sorted)}")
    print(f"\nAll found words (sorted by frequency):")
    print(f"{'Word':<20} {'Count':<8} {'% of text'}")
    print("-" * 50)
    
    for word, count in found_words_sorted:
        percent = (count * len(word) / len(plaintext_text)) * 100
        print(f"{word:<20} {count:<8} {percent:>5.1f}%")
    
    # Show context for most common words
    print("\n" + "=" * 80)
    print("WORD CONTEXTS (top 10 most frequent words)")
    print("=" * 80)
    
    for word, count in found_words_sorted[:10]:
        print(f"\n'{word}' appears {count} times:")
        positions = find_word_positions(plaintext_text, word)
        
        # Show first 5 contexts
        for i, pos in enumerate(positions[:5]):
            context = extract_context(plaintext_text, pos, len(word), 15)
            print(f"  {i+1}. ...{context}...")
        
        if len(positions) > 5:
            print(f"  ... and {len(positions) - 5} more occurrences")
    
    # Try to reconstruct sentences
    print("\n" + "=" * 80)
    print("POTENTIAL SENTENCES (segments with 3+ words)")
    print("=" * 80)
    
    # Split by potential word boundaries
    segments = []
    for i in range(len(plaintext_text) - 20):
        segment = plaintext_text[i:i+20]
        words_in_segment = [w for w, c in found_words if w in segment]
        if len(words_in_segment) >= 3:
            segments.append((i, segment, words_in_segment))
    
    # Deduplicate overlapping segments
    unique_segments = []
    last_pos = -100
    for pos, seg, words in segments:
        if pos > last_pos + 10:
            unique_segments.append((pos, seg, words))
            last_pos = pos
    
    if unique_segments:
        print(f"\nFound {len(unique_segments)} potential sentence segments:")
        for i, (pos, seg, words) in enumerate(unique_segments[:20], 1):
            print(f"\n{i}. Position {pos}: '{seg}'")
            print(f"   Words: {', '.join(words)}")
    else:
        print("\nNo clear sentence segments found with 3+ dictionary words.")
    
    # Character distribution
    print("\n" + "=" * 80)
    print("CHARACTER ANALYSIS")
    print("=" * 80)
    
    from collections import Counter
    char_counts = Counter(plaintext_text)
    total_chars = len(plaintext_text)
    
    print(f"\nTop 15 most frequent characters/bigraphs:")
    print(f"{'Char':<10} {'Count':<8} {'%'}")
    print("-" * 30)
    
    for char, count in char_counts.most_common(15):
        percent = (count / total_chars) * 100
        print(f"{char:<10} {count:<8} {percent:>5.1f}%")
    
    # Summary
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    total_word_coverage = sum(count * len(word) for word, count in found_words_sorted)
    coverage_percent = (total_word_coverage / len(plaintext_text)) * 100
    
    print(f"\nDictionary word coverage: {coverage_percent:.1f}% of text")
    print(f"Most common words: {', '.join(w for w, c in found_words_sorted[:5])}")
    
    if len(found_words_sorted) < 10:
        print("\n⚠ Very few dictionary words found - suggests:")
        print("  1. Plaintext is not standard English")
        print("  2. Additional transformation needed")
        print("  3. Key/cipher still not correct")
    elif coverage_percent < 30:
        print("\n⚠ Low word coverage - suggests:")
        print("  1. Text is heavily fragmented")
        print("  2. Non-standard vocabulary or spelling")
        print("  3. Mixed with non-word content")
    else:
        print("\n✓ Reasonable word coverage - suggests:")
        print("  1. Decryption is on the right track")
        print("  2. May need to parse/interpret the fragments")
        print("  3. Could be intentional cipher-speak or compressed text")

if __name__ == '__main__':
    main()

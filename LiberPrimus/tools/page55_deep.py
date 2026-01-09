#!/usr/bin/env python3
"""
PAGE 55 DEEP ANALYSIS - Test key reset variations

First part decrypts to: "AN END. WITHIN THE DEEP WEB. THERE EXISTS A PAGE THAT HASHES TO. IT IS THE DUTY"
Then it breaks. Let's test different key reset strategies.
"""

from pathlib import Path

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

def euler_totient(n):
    return n - 1 if n >= 2 else 0

def load_page_55():
    script_dir = Path(__file__).parent
    page_dir = script_dir.parent / "pages" / "page_55"
    runes_file = page_dir / "runes.txt"
    
    with open(runes_file, 'r', encoding='utf-8') as f:
        rune_text = f.read()
    
    return rune_text

def decrypt_char(cipher_idx, key_idx, offset=0):
    """Decrypt single character using phi(prime) + offset."""
    k = (euler_totient(PRIMES[key_idx % len(PRIMES)]) + offset) % 29
    return (cipher_idx - k) % 29

def parse_words_and_sentences(rune_text):
    """Parse rune text into words and sentences."""
    words = []
    sentences = []
    
    current_word = []
    current_sentence = []
    
    for c in rune_text:
        if c in RUNE_MAP:
            current_word.append(RUNE_MAP[c])
        elif c == '-':  # Word separator
            if current_word:
                current_sentence.append(current_word)
                current_word = []
        elif c == '.':  # Sentence separator
            if current_word:
                current_sentence.append(current_word)
                current_word = []
            if current_sentence:
                sentences.append(current_sentence)
                current_sentence = []
    
    # Don't forget trailing content
    if current_word:
        current_sentence.append(current_word)
    if current_sentence:
        sentences.append(current_sentence)
    
    return sentences

def indices_to_text(indices):
    return ''.join(LETTERS[i] for i in indices)

def test_method_1_global_key(rune_text):
    """Method 1: Global prime counter (current method)."""
    print("\n=== Method 1: Global prime counter ===")
    cipher = [RUNE_MAP[c] for c in rune_text if c in RUNE_MAP]
    plain = []
    for i, c in enumerate(cipher):
        k = euler_totient(PRIMES[i % len(PRIMES)]) % 29
        plain.append((c - k) % 29)
    
    # Format with word breaks
    result = []
    idx = 0
    for c in rune_text:
        if c in RUNE_MAP:
            result.append(LETTERS[plain[idx]])
            idx += 1
        elif c == '-':
            result.append(' ')
        elif c == '.':
            result.append('. ')
    
    print(''.join(result))

def test_method_2_sentence_reset(rune_text):
    """Method 2: Reset prime counter at each sentence (.)."""
    print("\n=== Method 2: Reset key at each sentence (.) ===")
    sentences = parse_words_and_sentences(rune_text)
    
    output = []
    for sent in sentences:
        prime_idx = 0
        sent_text = []
        for word in sent:
            word_text = []
            for c in word:
                k = euler_totient(PRIMES[prime_idx % len(PRIMES)]) % 29
                p = (c - k) % 29
                word_text.append(LETTERS[p])
                prime_idx += 1
            sent_text.append(''.join(word_text))
        output.append(' '.join(sent_text))
    
    print('. '.join(output) + '.')

def test_method_3_word_reset(rune_text):
    """Method 3: Reset prime counter at each word (-)."""
    print("\n=== Method 3: Reset key at each word (-) ===")
    sentences = parse_words_and_sentences(rune_text)
    
    output = []
    for sent in sentences:
        sent_text = []
        for word in sent:
            word_text = []
            for i, c in enumerate(word):
                k = euler_totient(PRIMES[i % len(PRIMES)]) % 29
                p = (c - k) % 29
                word_text.append(LETTERS[p])
            sent_text.append(''.join(word_text))
        output.append(' '.join(sent_text))
    
    print('. '.join(output) + '.')

def test_method_4_hybrid(rune_text):
    """Method 4: Hybrid - global key but try different offsets for later sentences."""
    print("\n=== Method 4: Try different sentence offsets ===")
    sentences = parse_words_and_sentences(rune_text)
    
    # First, count characters in first few sentences
    total = 0
    for i, sent in enumerate(sentences):
        chars = sum(len(w) for w in sent)
        print(f"  Sentence {i}: {chars} chars (total so far: {total})")
        total += chars
    
    # Test different offsets for sentence 4 onwards
    for offset in range(0, 29):
        output = []
        global_idx = 0
        for si, sent in enumerate(sentences):
            sent_text = []
            for word in sent:
                word_text = []
                for c in word:
                    if si >= 4:  # After "IT IS THE DUTY"
                        k = (euler_totient(PRIMES[(global_idx + offset) % len(PRIMES)])) % 29
                    else:
                        k = euler_totient(PRIMES[global_idx % len(PRIMES)]) % 29
                    p = (c - k) % 29
                    word_text.append(LETTERS[p])
                    global_idx += 1
                sent_text.append(''.join(word_text))
            output.append(' '.join(sent_text))
        
        result = '. '.join(output) + '.'
        # Check if last part contains common words
        last_part = output[-2] if len(output) > 1 else output[-1]
        if 'THE' in last_part.upper() or 'OF' in last_part.upper() or 'AND' in last_part.upper():
            print(f"  Offset {offset}: {result[-80:]}")

def test_method_5_check_symbols(rune_text):
    """Check what the & and $ symbols at the end might mean."""
    print("\n=== Method 5: Check special symbols ===")
    print("Raw rune text:")
    print(repr(rune_text))
    print("\nSymbols found: & and $ at end - these may be significant!")

def test_method_6_reverse_prime(rune_text):
    """Method 6: Try reversing prime sequence or using different prime sets."""
    print("\n=== Method 6: Alternative prime sequences ===")
    sentences = parse_words_and_sentences(rune_text)
    
    # Try primes starting from different indices
    for start_prime in [0, 5, 10, 15]:
        output = []
        global_idx = start_prime
        for sent in sentences:
            sent_text = []
            for word in sent:
                word_text = []
                for c in word:
                    k = euler_totient(PRIMES[global_idx % len(PRIMES)]) % 29
                    p = (c - k) % 29
                    word_text.append(LETTERS[p])
                    global_idx += 1
                sent_text.append(''.join(word_text))
            output.append(' '.join(sent_text))
        
        result = '. '.join(output) + '.'
        words_found = sum(1 for w in ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'THAT', 'FOR', 'WITH', 'AN', 'END'] 
                        if w in result.upper())
        if words_found > 4:
            print(f"  Starting at prime[{start_prime}] ({PRIMES[start_prime]}): {words_found} common words")
            print(f"    {result}")

def main():
    print("PAGE 55 DEEP ANALYSIS")
    print("=" * 70)
    
    rune_text = load_page_55()
    print(f"Rune text length: {len(rune_text)}")
    print(f"Rune count: {sum(1 for c in rune_text if c in RUNE_MAP)}")
    
    test_method_1_global_key(rune_text)
    test_method_2_sentence_reset(rune_text)
    test_method_3_word_reset(rune_text)
    test_method_4_hybrid(rune_text)
    test_method_5_check_symbols(rune_text)
    test_method_6_reverse_prime(rune_text)

if __name__ == '__main__':
    main()

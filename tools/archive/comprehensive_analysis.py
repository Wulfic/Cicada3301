# -*- coding: utf-8 -*-
"""
Comprehensive Liber Primus Analysis Suite
Tackles all major solving approaches:
1. Running Key Cipher with reference texts
2. RSA Hex Block Analysis
3. Gematria Pattern Analysis
4. Steganography Detection
"""

import itertools as it
from collections import Counter
from pathlib import Path
import math
import re
import os

# =============================================================================
# GEMATRIA PRIMUS
# =============================================================================

GEMATRIA = (
    ('ᚠ', 'f', 2), ('ᚢ', 'u', 3), ('ᚦ', 'th', 5), ('ᚩ', 'o', 7),
    ('ᚱ', 'r', 11), ('ᚳ', 'c', 13), ('ᚷ', 'g', 17), ('ᚹ', 'w', 19),
    ('ᚻ', 'h', 23), ('ᚾ', 'n', 29), ('ᛁ', 'i', 31), ('ᛂ', 'j', 37),
    ('ᛇ', 'eo', 41), ('ᛈ', 'p', 43), ('ᛉ', 'x', 47), ('ᛋ', 's', 53),
    ('ᛏ', 't', 59), ('ᛒ', 'b', 61), ('ᛖ', 'e', 67), ('ᛗ', 'm', 71),
    ('ᛚ', 'l', 73), ('ᛝ', 'ing', 79), ('ᛟ', 'oe', 83), ('ᛞ', 'd', 89),
    ('ᚪ', 'a', 97), ('ᚫ', 'ae', 101), ('ᚣ', 'y', 103), ('ᛡ', 'io', 107),
    ('ᛠ', 'ea', 109)
)

RUNES = [x[0] for x in GEMATRIA]
LETTERS = [x[1] for x in GEMATRIA]
PRIMES = [x[2] for x in GEMATRIA]
ALPHABET_SIZE = 29

# English to rune index mapping
ENGLISH_TO_IDX = {}
for idx, (rune, eng, prime) in enumerate(GEMATRIA):
    ENGLISH_TO_IDX[eng] = idx
    if len(eng) == 1:
        ENGLISH_TO_IDX[eng.upper()] = idx

# =============================================================================
# UTILITIES
# =============================================================================

def shift(idx, amount):
    return (idx + amount) % ALPHABET_SIZE

def transliterate(text):
    result = ''
    for c in text:
        if c == '•':
            result += ' '
        elif c in RUNES:
            result += LETTERS[RUNES.index(c)]
        else:
            result += c
    return result

def runes_only(text):
    return [c for c in text if c in RUNES]

def text_to_indices(text):
    """Convert runic text to indices"""
    return [RUNES.index(c) for c in text if c in RUNES]

def english_to_indices(text):
    """Convert English text to rune indices (best effort)"""
    indices = []
    text = text.lower()
    i = 0
    while i < len(text):
        # Try digraphs first
        if i + 2 <= len(text):
            digraph = text[i:i+2]
            if digraph == 'th':
                indices.append(2)
                i += 2
                continue
            elif digraph == 'ng':
                indices.append(21)
                i += 2
                continue
            elif digraph == 'eo':
                indices.append(12)
                i += 2
                continue
            elif digraph == 'ae':
                indices.append(25)
                i += 2
                continue
            elif digraph == 'ea':
                indices.append(28)
                i += 2
                continue
            elif digraph == 'io':
                indices.append(27)
                i += 2
                continue
            elif digraph == 'oe':
                indices.append(22)
                i += 2
                continue
        
        # Single character
        char = text[i]
        if char in ENGLISH_TO_IDX:
            indices.append(ENGLISH_TO_IDX[char])
        elif char == 'k':  # k -> c
            indices.append(5)
        elif char == 'v':  # v -> u
            indices.append(1)
        elif char == 'q':  # q -> c
            indices.append(5)
        elif char == 'z':  # z -> s
            indices.append(15)
        # Skip non-letters
        i += 1
    
    return indices

def score_english(text):
    """Score how English-like a text appears"""
    common_words = {'the', 'and', 'of', 'to', 'a', 'in', 'is', 'it', 'that', 'was',
                    'for', 'on', 'are', 'with', 'as', 'be', 'at', 'this', 'have',
                    'from', 'or', 'one', 'by', 'but', 'not', 'what', 'all', 'we',
                    'within', 'instar', 'emerge', 'divinity', 'wisdom', 'truth',
                    'you', 'must', 'our', 'who', 'find', 'seek', 'path'}
    
    text_lower = text.lower()
    words = re.findall(r'[a-z]+', text_lower)
    
    score = sum(10 for w in words if w in common_words)
    
    # Bigram bonus
    common_bigrams = {'th', 'he', 'in', 'er', 'an', 'en', 'on', 'at', 're', 'ed'}
    for i in range(len(text_lower) - 1):
        if text_lower[i:i+2] in common_bigrams:
            score += 1
    
    return score

# =============================================================================
# PART 1: RUNNING KEY CIPHER
# =============================================================================

def running_key_decrypt(ciphertext, keytext):
    """
    Running key cipher: C - K = P (mod alphabet_size)
    Uses another text as the key
    """
    cipher_indices = text_to_indices(ciphertext)
    key_indices = english_to_indices(keytext)
    
    if len(key_indices) < len(cipher_indices):
        # Repeat key if needed
        key_indices = (key_indices * (len(cipher_indices) // len(key_indices) + 1))[:len(cipher_indices)]
    
    result = []
    for i, c_idx in enumerate(cipher_indices):
        k_idx = key_indices[i] if i < len(key_indices) else 0
        p_idx = (c_idx - k_idx) % ALPHABET_SIZE
        result.append(LETTERS[p_idx])
    
    # Reconstruct with spaces
    output = []
    idx = 0
    for c in ciphertext:
        if c in RUNES:
            output.append(result[idx])
            idx += 1
        elif c == '•':
            output.append(' ')
        else:
            output.append(c)
    
    return ''.join(output)

def test_running_key_ciphers(ciphertext):
    """Test running key cipher with various key texts"""
    print("\n" + "=" * 70)
    print("RUNNING KEY CIPHER ANALYSIS")
    print("=" * 70)
    
    # Reference texts to try as keys
    key_texts = {
        "Self-Reliance Opening": """
            I read the other day some verses written by an eminent painter which were original 
            and not conventional. The soul always hears an admonition in such lines, let the 
            subject be what it may. The sentiment they instil is of more value than any thought 
            they may contain. To believe your own thought, to believe that what is true for you 
            in your private heart is true for all men, that is genius.
        """,
        
        "Self-Reliance - Trust thyself": """
            Trust thyself every heart vibrates to that iron string Accept the place the 
            divine providence has found for you the society of your contemporaries the 
            connection of events Great men have always done so and confided themselves 
            childlike to the genius of their age betraying their perception that the 
            absolutely trustworthy was seated at their heart working through their hands
        """,
        
        "Book of the Law Ch1": """
            Had! The manifestation of Nuit. The unveiling of the company of heaven.
            Every man and every woman is a star. Every number is infinite; there is no 
            difference. Help me, o warrior lord of Thebes, in my unveiling before the 
            Children of men!
        """,
        
        "Book of the Law - Do what thou wilt": """
            Do what thou wilt shall be the whole of the Law. The word of the Law is 
            Thelema. Who calls us Thelemites will do no wrong, if he look but close 
            into the word. For there are therein Three Grades, the Hermit, and the Lover, 
            and the man of Earth. Do what thou wilt shall be the whole of the Law.
        """,
        
        "Cicada Parable": """
            parable like the instar tunneling to the surface we must shed our own 
            circumferences find the divinity within and emerge
        """,
        
        "Prime Numbers": "".join([chr(ord('a') + (p % 26)) for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]*10]),
        
        "Fibonacci Sequence": "".join([chr(ord('a') + (f % 26)) for f in [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610]*10]),
    }
    
    results = []
    
    for key_name, key_text in key_texts.items():
        decrypted = running_key_decrypt(ciphertext, key_text)
        score = score_english(decrypted)
        results.append((key_name, score, decrypted[:100]))
        
        if score > 30:
            print(f"\n*** PROMISING: {key_name} (score={score}) ***")
            print(f"  {decrypted[:120]}...")
    
    # Also test with different starting positions in key
    print("\n--- Testing with offset key positions ---")
    best_key = "Self-Reliance Opening"
    for offset in range(0, 500, 50):
        key_text = key_texts[best_key][offset:] + key_texts[best_key][:offset]
        decrypted = running_key_decrypt(ciphertext, key_text)
        score = score_english(decrypted)
        if score > 40:
            print(f"  Offset {offset}: score={score}")
            print(f"    {decrypted[:80]}...")
    
    # Sort and show best
    results.sort(key=lambda x: x[1], reverse=True)
    print("\n--- Top Results ---")
    for key_name, score, preview in results[:5]:
        print(f"  [{score}] {key_name}: {preview[:60]}...")
    
    return results

# =============================================================================
# PART 2: RSA HEX BLOCK ANALYSIS
# =============================================================================

def analyze_rsa_block():
    """Analyze the hex block from Page 56"""
    print("\n" + "=" * 70)
    print("RSA HEX BLOCK ANALYSIS")
    print("=" * 70)
    
    # The hex block from Page 56
    hex_block = """36367763ab73783c7af284446c
59466b4cd653239a311cb7116
d4618dee09a8425893dc7500b
464fdaf1672d7bef5e891c6e227
4568926a49fb4f45132c2a8b4"""
    
    # Clean and concatenate
    hex_clean = hex_block.replace('\n', '').replace(' ', '')
    print(f"\nHex block (cleaned): {hex_clean}")
    print(f"Length: {len(hex_clean)} hex chars = {len(hex_clean)*4} bits")
    
    # Convert to integer
    try:
        n = int(hex_clean, 16)
        print(f"\nAs integer: {n}")
        print(f"Bit length: {n.bit_length()}")
    except ValueError as e:
        print(f"Error parsing hex: {e}")
        return
    
    # Check if it's a reasonable RSA modulus size
    print(f"\n--- RSA Analysis ---")
    if n.bit_length() < 512:
        print(f"WARNING: {n.bit_length()} bits is too small for RSA modulus")
        print("This might be:")
        print("  - An RSA ciphertext (encrypted message)")
        print("  - A hash value")
        print("  - Part of a larger key")
    
    # Try to factor (small factors first)
    print("\n--- Factorization Attempt ---")
    factors = []
    temp_n = n
    
    # Test small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                   53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    for p in small_primes:
        while temp_n % p == 0:
            factors.append(p)
            temp_n //= p
    
    if factors:
        print(f"Small factors found: {factors}")
        print(f"Remaining: {temp_n}")
    else:
        print("No small prime factors found")
    
    # Check if it might be a hash
    print("\n--- Hash Analysis ---")
    hash_sizes = {128: "MD5", 160: "SHA-1", 256: "SHA-256", 384: "SHA-384", 512: "SHA-512"}
    bit_len = n.bit_length()
    for size, name in hash_sizes.items():
        if abs(bit_len - size) < 8:
            print(f"Could be {name} hash ({size} bits)")
    
    # Check for ASCII interpretation
    print("\n--- ASCII Interpretation ---")
    try:
        # Pad to even length
        hex_padded = hex_clean if len(hex_clean) % 2 == 0 else '0' + hex_clean
        ascii_bytes = bytes.fromhex(hex_padded)
        ascii_text = ascii_bytes.decode('ascii', errors='replace')
        printable = ''.join(c if 32 <= ord(c) < 127 else '.' for c in ascii_text)
        print(f"As ASCII: {printable[:80]}")
    except Exception as e:
        print(f"ASCII decode error: {e}")
    
    # Look for known RSA public keys from Cicada
    print("\n--- Known Cicada RSA Keys ---")
    print("Cicada 3301 has used RSA keys in previous puzzles.")
    print("The public key fingerprints are available on MIT key servers.")
    print("This hex block might be encrypted with one of those keys.")
    
    # Check the number's properties
    print("\n--- Mathematical Properties ---")
    
    # Is it prime?
    def is_probably_prime(n, k=10):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        for _ in range(k):
            a = 2 + (hash(str(_)) % (n - 4))
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    print(f"Is probably prime: {is_probably_prime(n)}")
    print(f"n mod 29: {n % 29} (alphabet size)")
    print(f"n mod 3301: {n % 3301} (Cicada number)")
    
    # Gematria primes sum
    gematria_sum = sum(PRIMES)
    print(f"n mod {gematria_sum} (gematria sum): {n % gematria_sum}")
    
    return n

# =============================================================================
# PART 3: GEMATRIA PATTERN ANALYSIS  
# =============================================================================

def analyze_gematria_patterns(text):
    """Analyze gematria values for patterns"""
    print("\n" + "=" * 70)
    print("GEMATRIA PATTERN ANALYSIS")
    print("=" * 70)
    
    # Load full text
    runes = runes_only(text)
    print(f"\nTotal runes: {len(runes)}")
    
    # Calculate gematria values
    gematria_values = [PRIMES[RUNES.index(r)] for r in runes]
    total = sum(gematria_values)
    
    print(f"Total gematria sum: {total}")
    print(f"Average gematria value: {total / len(runes):.2f}")
    
    # Factor analysis
    print("\n--- Factor Analysis of Total ---")
    
    def prime_factors(n):
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    factors = prime_factors(total)
    print(f"Prime factors of {total}: {factors}")
    print(f"Unique factors: {set(factors)}")
    
    # Check for significant numbers
    print("\n--- Significant Number Check ---")
    significant = {
        29: "Alphabet size",
        3301: "Cicada number",
        1033: "Part of 3301",
        1595277641: "Parable gematria product",
    }
    
    for num, desc in significant.items():
        if total % num == 0:
            print(f"  Divisible by {num} ({desc}): {total // num}")
        print(f"  {total} mod {num} = {total % num}")
    
    # Word-by-word gematria
    print("\n--- Word Gematria Analysis ---")
    words = text.split('•')
    word_values = []
    
    for word in words[:20]:  # First 20 words
        word_runes = runes_only(word)
        if word_runes:
            value = sum(PRIMES[RUNES.index(r)] for r in word_runes)
            word_values.append(value)
            translit = transliterate(word)
            print(f"  {translit[:15]:<15} = {value}")
    
    # Look for patterns in word values
    if len(word_values) > 2:
        diffs = [word_values[i+1] - word_values[i] for i in range(len(word_values)-1)]
        print(f"\n  Differences between word values: {diffs[:10]}")
    
    # Page-by-page analysis
    print("\n--- Page Gematria Sums ---")
    pages = text.split('&')
    page_sums = []
    
    for i, page in enumerate(pages[:10]):
        page_runes = runes_only(page)
        if page_runes:
            page_sum = sum(PRIMES[RUNES.index(r)] for r in page_runes)
            page_sums.append(page_sum)
            factors_pg = prime_factors(page_sum)
            print(f"  Page {i}: sum={page_sum}, factors={factors_pg[:5]}{'...' if len(factors_pg) > 5 else ''}")
    
    # Look for relationships between page sums
    if len(page_sums) > 1:
        print("\n  Page sum relationships:")
        for i in range(len(page_sums) - 1):
            gcd = math.gcd(page_sums[i], page_sums[i+1])
            print(f"    GCD(Page{i}, Page{i+1}) = {gcd}")
    
    return total, word_values, page_sums

# =============================================================================
# PART 4: IMAGE STEGANOGRAPHY DETECTION
# =============================================================================

def check_steganography_indicators():
    """Check for steganography in LP images"""
    print("\n" + "=" * 70)
    print("STEGANOGRAPHY ANALYSIS")
    print("=" * 70)
    
    image_dir = Path("2014/Liber Primus/liber primus images full")
    
    if not image_dir.exists():
        print(f"Image directory not found: {image_dir}")
        return
    
    # List images
    images = sorted(image_dir.glob("*.jpg"))
    print(f"\nFound {len(images)} images")
    
    # Check file sizes for anomalies
    print("\n--- File Size Analysis ---")
    sizes = []
    for img in images:
        size = img.stat().st_size
        sizes.append((img.name, size))
    
    avg_size = sum(s[1] for s in sizes) / len(sizes)
    print(f"Average file size: {avg_size:.0f} bytes")
    
    # Flag unusually large files (might contain hidden data)
    print("\nUnusually large files (>150% of average):")
    for name, size in sizes:
        if size > avg_size * 1.5:
            print(f"  {name}: {size} bytes ({size/avg_size*100:.0f}% of avg)")
    
    print("\nUnusually small files (<50% of average):")
    for name, size in sizes:
        if size < avg_size * 0.5:
            print(f"  {name}: {size} bytes ({size/avg_size*100:.0f}% of avg)")
    
    # Check for Outguess signatures
    print("\n--- Outguess Detection ---")
    print("Outguess was used in 2012 and 2013 Cicada puzzles.")
    print("To extract hidden data, run: outguess -r image.jpg output.txt")
    
    # Check first few bytes of each file
    print("\n--- JPEG Header Analysis ---")
    print("Checking for valid JPEG signatures and anomalies...")
    
    anomalies = []
    for img in images[:10]:  # Check first 10
        with open(img, 'rb') as f:
            header = f.read(20)
            
            # Valid JPEG starts with FFD8FF
            if header[:3] != b'\xff\xd8\xff':
                anomalies.append(f"{img.name}: Invalid JPEG header")
            
            # Check for EXIF or JFIF
            if b'Exif' in header:
                print(f"  {img.name}: Contains EXIF data")
            if b'JFIF' in header:
                print(f"  {img.name}: JFIF format")
    
    if anomalies:
        print("\nAnomalies found:")
        for a in anomalies:
            print(f"  {a}")
    
    # Provide extraction commands
    print("\n--- Recommended Extraction Commands ---")
    print("""
To check for hidden data using various tools:

1. Outguess (most likely for Cicada):
   outguess -r image.jpg output.txt

2. Steghide:
   steghide extract -sf image.jpg

3. Strings (simple text extraction):
   strings image.jpg | grep -i cicada

4. ExifTool (metadata):
   exiftool image.jpg

5. Binwalk (embedded files):
   binwalk -e image.jpg
""")
    
    return images

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Load Liber Primus
    lp_path = Path("2014/Liber Primus/runes in text format.txt")
    
    if lp_path.exists():
        with open(lp_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
        
        # Get first substantial section for running key test
        first_section = full_text[:2000]
        
        print("#" * 70)
        print("# COMPREHENSIVE LIBER PRIMUS ANALYSIS")
        print("#" * 70)
        
        # 1. Running Key Cipher Analysis
        test_running_key_ciphers(first_section)
        
        # 2. RSA Hex Block Analysis
        analyze_rsa_block()
        
        # 3. Gematria Pattern Analysis
        analyze_gematria_patterns(full_text)
        
        # 4. Steganography Detection
        check_steganography_indicators()
        
        print("\n" + "#" * 70)
        print("# ANALYSIS COMPLETE")
        print("#" * 70)
        
    else:
        print(f"Liber Primus not found at {lp_path}")

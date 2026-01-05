"""
Test if the XOR-71 output is itself a key or needs further transformation.

Hypotheses to test:
1. XOR-71 output indices are pointers to Parable positions
2. XOR-71 output needs a second XOR/SUB with Parable as running key
3. XOR-71 output indices map to a different alphabet/gematria scheme
"""

import os

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

OPTIMIZED_KEY_71 = [16, 4, 13, 27, 4, 15, 25, 27, 16, 8, 5, 10, 22, 0, 1, 6, 24, 9, 15, 10, 0, 0, 6, 3, 10, 22, 14, 5, 16, 3, 15, 20, 27, 1, 4, 24, 0, 20, 19, 21, 4, 21, 14, 14, 6, 0, 10, 17, 24, 17, 3, 8, 17, 16, 6, 2, 12, 25, 24, 13, 7, 18, 21, 15, 19, 10, 6, 10, 27, 3, 5]

def load_page1():
    """Load Page 1."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_indices = [RUNE_TO_INDEX[c] for c in segments[0] if c in RUNE_TO_INDEX]
    return page1_indices

def load_parable():
    """Load Parable (Page 57) as indices."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    parable_indices = [RUNE_TO_INDEX[c] for c in segments[56] if c in RUNE_TO_INDEX]
    return parable_indices

def decrypt_xor(cipher_indices, key_indices):
    """XOR decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c ^ k) % 29)
    return plaintext

def decrypt_sub(cipher_indices, key_indices):
    """SUB decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c - k) % 29)
    return plaintext

def decrypt_add(cipher_indices, key_indices):
    """ADD decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c + k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert to text."""
    return "".join(LETTERS[i] for i in indices)

def score_text(text):
    """Simple English scoring."""
    text_upper = text.upper()
    
    common_words = [
        "THE", "OF", "AND", "TO", "IN", "IS", "THAT", "IT", "WITH", "FOR",
        "AS", "WAS", "ON", "BE", "AT", "BY", "THIS", "FROM", "OR", "AN",
        "DIVINE", "EMERGE", "INSTAR", "CIRCUMFERENCE", "WITHIN", "TRUTH"
    ]
    
    score = 0.0
    for word in common_words:
        import re
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = len(re.findall(pattern, text_upper))
        score += matches * len(word) * 2
    
    # Bigrams
    for bg in ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN"]:
        score += text_upper.count(bg) * 1.5
    
    return score

def main():
    print("="*80)
    print("Testing Alternative Transformations of XOR-71 Output")
    print("="*80)
    
    # Get XOR-71 output
    cipher_indices = load_page1()
    xor71_output = decrypt_xor(cipher_indices, OPTIMIZED_KEY_71)
    
    print(f"\nXOR-71 output: {indices_to_text(xor71_output)[:100]}...")
    print(f"Length: {len(xor71_output)}")
    
    # Load Parable
    parable = load_parable()
    print(f"\nParable length: {len(parable)}")
    print(f"Parable text: {indices_to_text(parable)}")
    
    # Test 1: XOR-71 output with Parable as running key
    print("\n" + "="*80)
    print("Test 1: Apply Parable as running key to XOR-71 output")
    print("="*80)
    
    for op_name, op_func in [("SUB", decrypt_sub), ("ADD", decrypt_add), ("XOR", decrypt_xor)]:
        result = op_func(xor71_output, parable)
        text = indices_to_text(result)
        score = score_text(text)
        
        print(f"\n{op_name} with Parable:")
        print(f"  Score: {score:.2f}")
        print(f"  Preview: {text[:150]}")
    
    # Test 2: Use XOR-71 indices modulo Parable length as pointers
    print("\n" + "="*80)
    print("Test 2: XOR-71 indices as pointers into Parable")
    print("="*80)
    
    parable_len = len(parable)
    pointer_result = [parable[idx % parable_len] for idx in xor71_output]
    text = indices_to_text(pointer_result)
    score = score_text(text)
    
    print(f"Score: {score:.2f}")
    print(f"Preview: {text[:150]}")
    
    # Test 3: XOR-71 output + Parable (position-based)
    print("\n" + "="*80)
    print("Test 3: Combine XOR-71 with Parable position-wise")
    print("="*80)
    
    for op_name in ["ADD", "SUB", "XOR"]:
        result = []
        for i in range(min(len(xor71_output), len(parable))):
            if op_name == "ADD":
                result.append((xor71_output[i] + parable[i]) % 29)
            elif op_name == "SUB":
                result.append((xor71_output[i] - parable[i]) % 29)
            elif op_name == "XOR":
                result.append((xor71_output[i] ^ parable[i]) % 29)
        
        text = indices_to_text(result)
        score = score_text(text)
        
        print(f"\n{op_name} (position-wise with Parable):")
        print(f"  Score: {score:.2f}")
        print(f"  Preview: {text[:150]}")
    
    # Test 4: Reverse operations - what if we need to ADD back the key?
    print("\n" + "="*80)
    print("Test 4: Re-encrypt XOR-71 with key-71 (reverse direction)")
    print("="*80)
    
    # Try XOR-71 output XOR key-71 again (should give original cipher)
    reversed_xor = []
    for i, val in enumerate(xor71_output):
        k = OPTIMIZED_KEY_71[i % len(OPTIMIZED_KEY_71)]
        reversed_xor.append((val ^ k) % 29)
    
    # Check if this matches original
    matches = sum(1 for i in range(len(cipher_indices)) if reversed_xor[i] == cipher_indices[i])
    print(f"Matches with original cipher: {matches}/{len(cipher_indices)}")
    
    if matches == len(cipher_indices):
        print("✓ XOR-71 decrypt is correctly reversible")
    else:
        print("⚠️ XOR-71 decrypt not fully reversible - possible issue")
    
    # Test 5: What if the "TH" patterns are intentional - look at TH positions
    print("\n" + "="*80)
    print("Test 5: Analyze 'TH' (index 2) positions in XOR-71 output")
    print("="*80)
    
    th_positions = [i for i, val in enumerate(xor71_output) if val == 2]  # TH = index 2
    print(f"'TH' appears at {len(th_positions)} positions out of {len(xor71_output)}")
    print(f"Positions: {th_positions[:30]}...")
    
    # Check if positions have a pattern
    if len(th_positions) > 1:
        gaps = [th_positions[i+1] - th_positions[i] for i in range(len(th_positions)-1)]
        from collections import Counter
        gap_freq = Counter(gaps)
        print(f"Most common gaps: {gap_freq.most_common(10)}")
    
    # Extract non-TH characters
    non_th = [LETTERS[val] for val in xor71_output if val != 2]
    print(f"\nText without 'TH': {''.join(non_th)[:150]}")

if __name__ == "__main__":
    main()

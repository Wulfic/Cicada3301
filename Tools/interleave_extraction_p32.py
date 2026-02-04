"""
Interleaving Hypothesis - Extract Words at Regular Intervals
Page 32 plaintext may be interleaved at specific positions
"""

import os
from collections import defaultdict

GP_RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14,
    'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21,
    'ᛟ': 22, 'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

GP_INDEX_TO_LATIN = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N',
    'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M',
    'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

WORD_DICT = {
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
    'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM',
    'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN', 'HIM', 'HIS',
    'HOW', 'WHO', 'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'TWO', 'WAY', 'WHY',
    'TRY', 'ASK', 'END', 'EVEN', 'FIND', 'FIRST', 'GET', 'GIVE', 'GOOD',
    'HAND', 'HELP', 'HERE', 'HIGH', 'JUST', 'KEEP', 'KNOW', 'LAST',
    'LIFE', 'LIKE', 'LITTLE', 'LONG', 'LOOK', 'MAKE', 'MAN', 'MAY',
    'MEANS', 'MORE', 'MOST', 'MUCH', 'MUST', 'NAME', 'NEED', 'NEVER',
    'NEW', 'NEXT', 'NO', 'NOW', 'NUMBER', 'OF', 'OLD', 'ON', 'ONLY',
    'OR', 'OTHER', 'OVER', 'OWN', 'PART', 'PATH', 'PEOPLE', 'PLACE',
    'RIGHT', 'SAME', 'SAY', 'SEE', 'SEEM', 'SHOULD', 'SHOW', 'SIDE',
    'SOME', 'SOMETHING', 'STILL', 'SUCH', 'TAKE', 'TELL', 'THAN', 'THAT',
    'THEM', 'THEN', 'THESE', 'THEY', 'THING', 'THINK', 'THIS', 'THOSE',
    'TIME', 'TO', 'TOO', 'TOOK', 'TOP', 'TOWN', 'TRY', 'TURN', 'TWO',
    'UNDER', 'UP', 'US', 'USED', 'VERY', 'WAY', 'WEEK', 'WERE',
    'WHICH', 'WHILE', 'WILL', 'WITH', 'WORD', 'WORK', 'WORLD', 'WOULD',
    'YEAR', 'YES', 'YOU', 'YOUR',
    # Cicada themes
    'PRIMES', 'SACRED', 'TRUTH', 'WISDOM', 'JOURNEY', 'PATH', 'SEEK', 'FIND',
    'KNOW', 'ENCRYPT', 'KEY', 'RUNE', 'ANCIENT', 'MYSTERY', 'VOID', 'LIGHT',
}

def load_caesar_11_text():
    """Load Page 32 after Caesar 11"""
    page_dir = "LiberPrimus/pages/page_32"
    rune_file = os.path.join(page_dir, "runes.txt")
    
    with open(rune_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    indices = []
    for char in text:
        if char in GP_RUNE_TO_INDEX:
            indices.append(GP_RUNE_TO_INDEX[char])
    
    # Caesar 11
    caesar = [(i - 11) % 29 for i in indices]
    
    # Convert to text
    result = []
    for idx in caesar:
        result.append(GP_INDEX_TO_LATIN[idx])
    
    return ''.join(result)

def extract_at_intervals(text, start=0, step=1, length=None):
    """Extract characters at regular intervals"""
    if length is None:
        return text[start::step]
    else:
        return "".join(text[i:i+2] if i+1 < len(text) else text[i] 
                      for i in range(start, length, step))

def score_text_quality(text):
    """Score extracted text for English content"""
    # Count known words
    words_found = 0
    chars_in_words = 0
    
    i = 0
    while i < len(text) - 1:
        # Try two-character combos
        two_char = text[i:i+2]
        for length in [4, 3, 2, 1]:
            substring = text[i:i+length].upper()
            if substring in WORD_DICT:
                words_found += 1
                chars_in_words += length
                i += length
                break
        else:
            i += 1
    
    # Percentage of text in known words
    if len(text) > 0:
        word_percentage = (chars_in_words / len(text)) * 100
    else:
        word_percentage = 0
    
    return words_found, word_percentage

def find_best_extraction(text):
    """Test various extraction parameters"""
    best_score = 0
    best_config = None
    results = []
    
    print("Testing extraction patterns...")
    print("=" * 80)
    
    # Test different starting positions and steps
    for start in range(min(20, len(text))):
        for step in range(1, min(50, len(text) // 10)):
            extracted = extract_at_intervals(text, start, step)
            
            if len(extracted) < 20:  # Skip too-short extractions
                continue
            
            words, percentage = score_text_quality(extracted)
            
            if percentage > best_score:
                best_score = percentage
                best_config = (start, step)
                results.append((percentage, words, start, step, extracted[:100]))
    
    results.sort(reverse=True)
    
    print(f"\nTop 15 Extraction Results:\n")
    print(f"{'%Words':<10} {'Count':<8} {'Start':<8} {'Step':<8} {'Preview'}")
    print("-" * 80)
    
    for percentage, count, start, step, preview in results[:15]:
        print(f"{percentage:>7.1f}%  {count:>5}   {start:>5}   {step:>5}   {preview[:50]}")
    
    if best_config:
        print(f"\n✅ Best configuration: Start={best_config[0]}, Step={best_config[1]}")
        best_extraction = extract_at_intervals(text, best_config[0], best_config[1])
        return best_extraction
    
    return None

def main():
    print("=" * 80)
    print("INTERLEAVING EXTRACTION - PAGE 32")
    print("=" * 80)
    print()
    
    text = load_caesar_11_text()
    print(f"Text length: {len(text)}")
    print(f"First 200 chars: {text[:200]}")
    print()
    
    # Find best extraction
    best = find_best_extraction(text)
    
    if best:
        print()
        print("=" * 80)
        print("BEST EXTRACTED TEXT")
        print("=" * 80)
        print()
        print(best[:500])
        
        # Save result
        with open("page_32_interleave_extracted.txt", 'w', encoding='utf-8') as f:
            f.write(best)
        print("\n✅ Saved to: page_32_interleave_extracted.txt")

if __name__ == "__main__":
    main()

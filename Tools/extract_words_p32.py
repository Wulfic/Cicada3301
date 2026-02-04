"""
Extract Coherent Words from Scrambled Text - Page 32
Uses dynamic programming and known word dictionary
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

# Extended dictionary
WORD_DICT = {
    # Common English
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
    'UNDER', 'UP', 'US', 'USE', 'USED', 'VERY', 'WAY', 'WEEK', 'WERE',
    'WHAT', 'WHEN', 'WHERE', 'WHICH', 'WHILE', 'WHO', 'WHY', 'WILL',
    'WITH', 'WORD', 'WORK', 'WORLD', 'WOULD', 'YEAR', 'YES', 'YOU',
    # Cicada themes
    'PRIMES', 'SACRED', 'TRUTH', 'WISDOM', 'JOURNEY', 'PILGRIMAGE', 'PATH',
    'SEEK', 'FIND', 'KNOW', 'ENCRYPT', 'CIPHER', 'KEY', 'RUNE', 'ANCIENT',
    'MYSTERY', 'ENDLESS', 'VOID', 'LIGHT', 'DARK', 'DEATH', 'LIFE', 'WAY',
    'SELF', 'SOUL', 'SPIRIT', 'END', 'BEGIN', 'CYCLE', 'ETERNAL', 'SECRET',
    # Old English possibilities
    'EODE', 'SEFA', 'HAL', 'THANE', 'WYRD', 'AEON', 'DEOR', 'LONE',
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

def find_word_sequences(text, min_score=0.5):
    """Find word sequences in text using sliding window"""
    # Build sliding windows and check for known words
    findings = []
    
    for start in range(len(text) - 2):
        for end in range(start + 2, min(start + 15, len(text))):
            substring = text[start:end]
            if substring.upper() in WORD_DICT:
                findings.append({
                    'word': substring.upper(),
                    'start': start,
                    'end': end,
                    'length': len(substring)
                })
    
    return findings

def segment_text(text, max_iterations=50):
    """Try to segment text into known words (greedy approach)"""
    words = []
    pos = 0
    iteration = 0
    
    while pos < len(text) and iteration < max_iterations:
        found = False
        
        # Try to find longest word starting at current position
        for length in range(min(15, len(text) - pos), 1, -1):
            substring = text[pos:pos+length].upper()
            if substring in WORD_DICT:
                words.append(text[pos:pos+length])
                pos += length
                found = True
                break
        
        if not found:
            # Try single character
            words.append(text[pos])
            pos += 1
        
        iteration += 1
    
    return words, pos == len(text)  # Return words and whether we successfully segmented entire text

def main():
    print("=" * 80)
    print("WORD EXTRACTION FROM PAGE 32 (Caesar 11)")
    print("=" * 80)
    print()
    
    text = load_caesar_11_text()
    print(f"Text length: {len(text)}")
    print(f"First 300 chars: {text[:300]}")
    print()
    
    # Find all embedded words
    print("FINDING EMBEDDED KNOWN WORDS...")
    print("=" * 80)
    print()
    
    findings = find_word_sequences(text)
    print(f"Found {len(findings)} instances of known words\n")
    
    # Group by word
    by_word = defaultdict(list)
    for finding in findings:
        by_word[finding['word']].append(finding['start'])
    
    print("Words Found (with positions):\n")
    for word in sorted(by_word.keys()):
        positions = by_word[word]
        print(f"  {word:<15} appears {len(positions):>2}x at positions: {positions[:5]}")
    
    print()
    print("=" * 80)
    print("SEGMENTATION ATTEMPT (Greedy)")
    print("=" * 80)
    print()
    
    words, complete = segment_text(text)
    print(f"Successfully segmented entire text: {complete}")
    print(f"Word count: {len(words)}")
    print()
    
    print("Extracted words/segments:")
    print(" ".join(words[:100]))  # First 100 segments
    
    # Count how many are known words
    known_count = sum(1 for w in words if w.upper() in WORD_DICT)
    print(f"\nKnown words: {known_count} / {len(words)} ({100*known_count/len(words):.1f}%)")
    
    # Try different strategies
    print()
    print("=" * 80)
    print("ALTERNATIVE STRATEGIES")
    print("=" * 80)
    print()
    
    # Strategy: Extract every Nth character
    print("Strategy 1: Every 2nd character")
    every_2 = text[::2]
    findings_2 = find_word_sequences(every_2)
    print(f"  Found {len(findings_2)} known words")
    print(f"  Sample: {every_2[:150]}")
    print()
    
    # Strategy: Extract using only vowel-heavy runs
    print("Strategy 2: Text analysis")
    vowels = "AEIOUOEA"
    vowel_runs = []
    current_run = ""
    current_consonants = ""
    
    for i, char in enumerate(text):
        is_vowel = char in vowels
        if is_vowel:
            if current_consonants:
                vowel_runs.append(("C", current_consonants))
                current_consonants = ""
            current_run += char
        else:
            if current_run:
                vowel_runs.append(("V", current_run))
                current_run = ""
            current_consonants += char
    
    # Find pattern
    v_pattern = "".join(t for t, _ in vowel_runs[:50])
    print(f"  V/C pattern (first 50): {v_pattern}")
    print()
    
    # Check if word positions correlate with pattern
    print("Strategy 3: Find most common word at each position mod N")
    for mod in [3, 5, 7, 11]:
        position_words = defaultdict(lambda: defaultdict(int))
        for word, positions in by_word.items():
            for pos in positions:
                position_words[pos % mod][word] += 1
        
        print(f"  Position mod {mod}:")
        for pos_mod in range(mod):
            if position_words[pos_mod]:
                top_word = max(position_words[pos_mod].items(), key=lambda x: x[1])[0]
                print(f"    pos mod {pos_mod}: {top_word}")

if __name__ == "__main__":
    main()

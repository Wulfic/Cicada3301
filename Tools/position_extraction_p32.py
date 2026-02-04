"""
Position-based extraction test for Page 32
Test even/odd, primes, Fibonacci, etc.
"""

import os
import math

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

WORD_DICT = set([
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
    'WAS', 'ONE', 'OUR', 'OUT', 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM',
    'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'BEEN', 'HIM', 'HIS',
    'HOW', 'WHO', 'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'TWO', 'WAY', 'WHY',
    'TRY', 'ASK', 'END', 'EVEN', 'FIND', 'FIRST', 'GET', 'GIVE', 'GOOD',
    'HAND', 'HELP', 'HERE', 'HIGH', 'JUST', 'KEEP', 'KNOW', 'LAST', 'LIFE',
    'LIKE', 'LONG', 'LOOK', 'MAKE', 'MAN', 'MAY', 'MORE', 'MOST', 'MUST',
    'NAME', 'NEED', 'NEVER', 'NEW', 'NEXT', 'NO', 'NOW', 'OF', 'OLD', 'ON',
    'ONLY', 'OR', 'OTHER', 'OVER', 'OWN', 'PART', 'PATH', 'PEOPLE', 'PLACE',
    'RIGHT', 'SAME', 'SEE', 'SEEM', 'SHOULD', 'SHOW', 'SIDE', 'SOME', 'SUCH',
    'TAKE', 'TELL', 'THAN', 'THEM', 'THEN', 'THESE', 'THING', 'THINK', 'THIS',
    'THOSE', 'TIME', 'TO', 'TOO', 'TOOK', 'TOP', 'TOWN', 'TURN', 'TWO',
    'UNDER', 'UP', 'US', 'VERY', 'WAY', 'WEEK', 'WERE', 'WHICH', 'WHILE',
    'WILL', 'WITH', 'WORD', 'WORK', 'WORLD', 'YEAR', 'YES', 'YOU', 'YOUR',
])

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

def extract_positions(text, positions):
    """Extract characters at specified positions"""
    result = []
    for pos in positions:
        if pos < len(text):
            result.append(text[pos])
    return ''.join(result)

def score_english(text):
    """Count English words in text"""
    count = 0
    i = 0
    while i < len(text) - 2:
        for length in range(4, 1, -1):
            if i + length <= len(text):
                word = text[i:i+length].upper()
                if word in WORD_DICT:
                    count += 1
                    i += length
                    break
        else:
            i += 1
    
    return count

def is_prime(n):
    """Check if n is prime"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_primes(limit):
    """Get all primes up to limit"""
    return [i for i in range(2, limit) if is_prime(i)]

def get_fibonacci(limit):
    """Get Fibonacci numbers up to limit"""
    fibs = [1, 1]
    while fibs[-1] < limit:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:-1]

def main():
    print("=" * 80)
    print("POSITION-BASED EXTRACTION - PAGE 32")
    print("=" * 80)
    print()
    
    text = load_caesar_11_text()
    text_len = len(text)
    print(f"Text length: {text_len}")
    print()
    
    results = []
    
    # Test even positions
    even_pos = [i for i in range(text_len) if i % 2 == 0]
    extracted = extract_positions(text, even_pos)
    score = score_english(extracted)
    results.append({
        'name': 'Even positions',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Even positions: {score} words")
    
    # Test odd positions
    odd_pos = [i for i in range(text_len) if i % 2 == 1]
    extracted = extract_positions(text, odd_pos)
    score = score_english(extracted)
    results.append({
        'name': 'Odd positions',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Odd positions: {score} words")
    
    # Test prime positions
    primes = get_primes(text_len)
    extracted = extract_positions(text, primes)
    score = score_english(extracted)
    results.append({
        'name': 'Prime positions',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Prime positions: {score} words")
    
    # Test Fibonacci positions
    fibs = get_fibonacci(text_len)
    extracted = extract_positions(text, fibs)
    score = score_english(extracted)
    results.append({
        'name': 'Fibonacci positions',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Fibonacci positions: {score} words")
    
    # Test every 3rd position
    every_3rd = [i for i in range(text_len) if i % 3 == 0]
    extracted = extract_positions(text, every_3rd)
    score = score_english(extracted)
    results.append({
        'name': 'Every 3rd position',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Every 3rd position: {score} words")
    
    # Test every 5th position
    every_5th = [i for i in range(text_len) if i % 5 == 0]
    extracted = extract_positions(text, every_5th)
    score = score_english(extracted)
    results.append({
        'name': 'Every 5th position',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Every 5th position: {score} words")
    
    # Test composite (non-prime) positions
    composite_pos = [i for i in range(2, text_len) if not is_prime(i)]
    extracted = extract_positions(text, composite_pos)
    score = score_english(extracted)
    results.append({
        'name': 'Composite positions',
        'score': score,
        'sample': extracted[:100]
    })
    print(f"Composite positions: {score} words")
    
    # Results summary
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    results.sort(key=lambda x: x['score'], reverse=True)
    for r in results[:5]:
        print(f"\n{r['name']}: {r['score']} words")
        print(f"Sample: {r['sample']}")

if __name__ == "__main__":
    main()

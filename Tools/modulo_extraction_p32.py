"""
Test all modulo-based extractions for Page 32
"""

import os

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

def main():
    text = load_caesar_11_text()
    text_len = len(text)
    
    print("Testing modulo-based extractions...")
    print("=" * 60)
    
    results = []
    
    # Test mod N for N from 1 to 50, with all remainders 0 to N-1
    for mod in range(1, 51):
        for remainder in range(mod):
            extracted = []
            for i in range(text_len):
                if i % mod == remainder:
                    extracted.append(text[i])
            
            extracted_text = ''.join(extracted)
            score = score_english(extracted_text)
            
            if score >= 15:  # Only report good results
                results.append({
                    'mod': mod,
                    'remainder': remainder,
                    'score': score,
                    'sample': extracted_text[:100]
                })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\nTop 20 Results (score >= 15):")
    print(f"{'Mod':<6} {'Remainder':<12} {'Score':<8} {'Preview'}")
    print("-" * 60)
    
    for r in results[:20]:
        print(f"{r['mod']:<6} {r['remainder']:<12} {r['score']:<8} {r['sample'][:40]}")
    
    if results:
        print()
        print("=" * 60)
        print("BEST RESULT")
        print("=" * 60)
        best = results[0]
        print(f"\nMod: {best['mod']}, Remainder: {best['remainder']}, Score: {best['score']}")
        print()
        print(best['sample'][:500])

if __name__ == "__main__":
    main()

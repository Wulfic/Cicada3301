#!/usr/bin/env python3
"""
Analyze Page 2 SUB-83 plaintext for interleaving patterns (like Page 1)
"""

PLAINTEXT = "LTLEETEENEMEBEMMEBEEEMEMBEBEELEEEEBGMEEEMEEEEMEEIATEEEEEIAMEEEEBEEMEMMMMMMEBEMEEEEMETTHICOETHIWOEBBIACHLTESWHLNLPBGTHEHPJDHFYEAGIEOIAGEARTRTGEOLTHHXEOEODGFIATEYIIUTHERYIAPTHHENGTLEARETHRHEJUMGENDOESTHTHNGAEFEREAIATENGUXTHEAEEETHHESDLNREOEPTHNDDETSMENRETHEEAEARMYIAESTHDEPEOINIIBTHWGDXIMICBEFXTEAE"

def score_pattern(text):
    """Simple English scoring"""
    common_trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10
    }
    
    common_bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7
    }
    
    score = 0.0
    for i in range(len(text) - 2):
        if text[i:i+3] in common_trigrams:
            score += common_trigrams[text[i:i+3]]
    
    for i in range(len(text) - 1):
        if text[i:i+2] in common_bigrams:
            score += common_bigrams[text[i:i+2]]
    
    return score

print("=" * 80)
print("PAGE 2 SUB-83 PLAINTEXT ANALYSIS")
print("=" * 80)
print(f"\nLength: {len(PLAINTEXT)}")
print(f"Full text: {PLAINTEXT}\n")

# Test interleaving patterns
print("=" * 80)
print("INTERLEAVING ANALYSIS")
print("=" * 80)

results = []

# Every Nth character
for n in range(2, 11):
    for offset in range(n):
        extracted = PLAINTEXT[offset::n]
        if len(extracted) < 10:
            continue
        score = score_pattern(extracted)
        results.append({
            'pattern': f'every-{n}th from offset {offset}',
            'n': n,
            'offset': offset,
            'length': len(extracted),
            'score': score,
            'text': extracted
        })

# Sort by score
results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)

print("\nTop 20 patterns by score:")
print(f"{'Rank':<6} {'Pattern':<30} {'Score':<10} {'Length':<8} {'Preview'}")
print("-" * 90)

for i, r in enumerate(results_sorted[:20], 1):
    print(f"{i:<6} {r['pattern']:<30} {r['score']:<10.2f} {r['length']:<8} {r['text'][:50]}")

# Check if any extraction scores significantly higher
base_score = score_pattern(PLAINTEXT)
print(f"\n\nBase score (full text): {base_score:.2f}")
print(f"Best extraction score: {results_sorted[0]['score']:.2f}")
print(f"Ratio: {results_sorted[0]['score'] / base_score:.2f}x")

if results_sorted[0]['score'] > base_score * 1.1:
    print("\n✓ INTERLEAVING DETECTED - extraction scores higher than full text!")
    best = results_sorted[0]
    print(f"\nBest pattern: {best['pattern']}")
    print(f"Full extracted text:\n{best['text']}")
else:
    print("\n⚠ No strong interleaving pattern detected")
    print("Plaintext may be single-stream or different structure than Page 1")

# Check for repeated patterns
print("\n" + "=" * 80)
print("REPEATED PATTERNS")
print("=" * 80)

for n in [3, 4, 5]:
    ngrams = {}
    for i in range(len(PLAINTEXT) - n + 1):
        ngram = PLAINTEXT[i:i+n]
        if ngram in ngrams:
            ngrams[ngram].append(i)
        else:
            ngrams[ngram] = [i]
    
    repeated = {k: v for k, v in ngrams.items() if len(v) > 1}
    if repeated:
        print(f"\n{n}-grams appearing 2+ times:")
        sorted_repeated = sorted(repeated.items(), key=lambda x: len(x[1]), reverse=True)
        for ngram, positions in sorted_repeated[:10]:
            print(f"  '{ngram}': {len(positions)} times")

print("\n" + "=" * 80)
print("COMPARISON WITH PAGE 1")
print("=" * 80)
print("""
Page 1:
  - Base score: 223.50
  - Best extraction (every-2nd offset 1): 255.00
  - Ratio: 1.14x (14% improvement)
  - Strong interleaving detected

Page 2:
  - Base score: {:.2f}
  - Best extraction: {:.2f}
  - Ratio: {:.2f}x
""".format(base_score, results_sorted[0]['score'], results_sorted[0]['score'] / base_score))

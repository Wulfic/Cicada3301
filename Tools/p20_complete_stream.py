"""
Page 20 - Complete Stream Analysis
===================================
Building on findings:
- 166-rune stream (Deor@primes - P20@primes) has IoC 1.89
- 2x83 interleaved reading reveals: EODE, SEFA, THE LONE, HER
- Contains Old English words

Let's try to fully decode this.
"""

from collections import Counter
import itertools

# The 166-stream 
STREAM = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"

# 2x83 column reading (THE LONE appears here)
def read_2x83(text):
    rows, cols = 83, 2
    result = ""
    for c in range(cols):
        for r in range(rows):
            idx = r * cols + c
            if idx < len(text):
                result += text[idx]
    return result

INTERLEAVED = read_2x83(STREAM)

print("166-Stream Analysis")
print("=" * 60)
print(f"Original: {STREAM[:60]}...")
print(f"2x83 Int: {INTERLEAVED[:60]}...")
print()

# Count IoC
def calc_ioc(text):
    counts = Counter(text)
    n = len(text)
    if n < 2:
        return 0
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1)) * 26

print(f"Original IoC: {calc_ioc(STREAM):.4f}")
print(f"2x83 Interleaved IoC: {calc_ioc(INTERLEAVED):.4f}")

# Manual word detection
print("\n=== MANUAL WORD DETECTION ===")

words_3plus = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
               'SAY', 'MET', 'BID', 'FEE', 'ODE', 'EODE', 'SEFA', 'LONE', 'SELF', 'ALT', 'MOD',
               'DEATH', 'PATH', 'TRUTH', 'FIND', 'SEEK', 'DEAD', 'MEAN', 'AEON', 'REAPER', 'PRIME',
               'THATS', 'RATIO', 'LENGTH', 'MEAT', 'HEAT', 'SEAT', 'FEAT', 'NEAT', 'BEAT']

for word in words_3plus:
    for text_name, text in [('Original', STREAM), ('2x83', INTERLEAVED)]:
        idx = text.find(word)
        if idx >= 0:
            ctx = text[max(0, idx-5):min(len(text), idx+len(word)+5)]
            print(f"  {word:10s} in {text_name:10s} @ {idx:3d}: ...{ctx}...")

# The pattern suggests this is a TRANSPOSITION cipher
# Try all possible grid dimensions
print("\n=== GRID TRANSPOSITION SEARCH ===")

def word_score(text):
    words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'ALL', 'ONE', 'HER',
             'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'BEEN', 'LONE', 'SELF',
             'DEATH', 'PATH', 'TRUTH', 'DEAD', 'MEAN', 'AEON', 'MET', 'SAY',
             'EODE', 'SEFA', 'FEE', 'ODE', 'BID', 'ALT']
    return sum(len(w)**2 for w in words if w in text)

best_results = []

for rows in range(2, 84):
    for cols in range(2, 84):
        if rows * cols != len(STREAM):
            continue
        
        # Column-major read
        col_major = ""
        for c in range(cols):
            for r in range(rows):
                col_major += STREAM[r * cols + c]
        
        score = word_score(col_major)
        ioc = calc_ioc(col_major)
        
        if score >= 50 or 'THELONE' in col_major or 'DEATH' in col_major:
            best_results.append((score, ioc, rows, cols, col_major[:80]))

# Also try different reading patterns on the 2x83 result
# Spiral, zigzag, etc.
for result in sorted(best_results, reverse=True)[:10]:
    score, ioc, r, c, text = result
    print(f"Grid {r}x{c}: score={score}, IoC={ioc:.2f}")
    print(f"  {text}...")
    print()

# Now try assuming this IS the plaintext and look for word boundaries
print("\n=== WORD BOUNDARY ANALYSIS ===")

# The INTERLEAVED reading has readable phrases
text = INTERLEAVED

# Look for all 3+ letter words
found_words = []
for start in range(len(text)):
    for length in range(3, 12):
        if start + length > len(text):
            break
        word = text[start:start+length]
        if word in ['THE', 'LONE', 'HER', 'ONE', 'MET', 'BID', 'SAY', 'EODE', 'SEFA', 
                    'FEE', 'ODE', 'ALT', 'SELF', 'DEATH', 'PATH', 'DEAD', 'AEON',
                    'MEAT', 'HEAT', 'SEAT', 'FEAT', 'NEAT', 'BEAT', 'EAT', 'ATE',
                    'THY', 'WAY', 'DAY', 'SAY', 'MAY', 'LAY', 'PAY', 'HEY']:
            found_words.append((start, word))

print("Found words at positions:")
for pos, word in sorted(found_words):
    print(f"  {pos:3d}: {word}")

# Attempt: what if the text itself IS meaningful but we need to insert spaces correctly?
print("\n=== TRYING DIFFERENT INTERPRETATIONS ===")

# The phrase around THE LONE:
# SEFALTTHELONETNHER
# SEFA LT THE LONE T N HER
# SEFA (heart) + LT + THE LONE + TN + HER

# Could be Old English:
# "Sefa [heart/mind] ... the lone [one] ... her"

# Check what comes before SEFA
idx_sefa = INTERLEAVED.find('SEFA')
idx_thelone = INTERLEAVED.find('THELONE')
idx_her = INTERLEAVED.find('HER', idx_thelone)

print(f"Before SEFA: {INTERLEAVED[:idx_sefa]}")
print(f"SEFA to THELONE: {INTERLEAVED[idx_sefa:idx_thelone]}")
print(f"THELONE to HER: {INTERLEAVED[idx_thelone:idx_her+3]}")
print(f"After HER: {INTERLEAVED[idx_her+3:idx_her+30]}")

# Try interpreting the whole thing
print("\n=== FULL INTERPRETATION ATTEMPT ===")

# Parse character by character with possible word matches
def interpret_text(text):
    interpretation = []
    i = 0
    while i < len(text):
        # Try to match known words (longest first)
        matched = False
        for length in range(min(8, len(text)-i), 1, -1):
            candidate = text[i:i+length]
            known_words = ['THELONE', 'EODE', 'SEFA', 'DEATH', 'LONE', 'SELF', 'PATH', 
                           'AEON', 'DEAD', 'MEAN', 'MEAT', 'HEAT', 'FEAT', 'SEAT', 'NEAT',
                           'THE', 'HER', 'ONE', 'MET', 'BID', 'SAY', 'FEE', 'ODE', 'ALT',
                           'THY', 'WAY', 'DAY', 'MAY', 'LAY', 'PAY', 'HEY', 'EAT', 'ATE',
                           'OF', 'OR', 'ON', 'AT', 'TO', 'BY', 'IN', 'AM', 'AN', 'AS',
                           'ME', 'HE', 'WE', 'BE', 'SO', 'NO', 'GO', 'DO', 'HO', 'LO']
            if candidate in known_words:
                interpretation.append(f"[{candidate}]")
                i += length
                matched = True
                break
        if not matched:
            interpretation.append(text[i])
            i += 1
    return ''.join(interpretation)

result = interpret_text(INTERLEAVED)
print(f"Interpreted: {result[:200]}...")

# Count coverage
word_chars = sum(len(s)-2 for s in result.split('[') if ']' in s)
total_chars = len(INTERLEAVED)
print(f"\nWord coverage: {word_chars}/{total_chars} = {word_chars/total_chars*100:.1f}%")

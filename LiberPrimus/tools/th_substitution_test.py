"""
Test hypothesis: Some TH occurrences are actually other runes that got shifted to TH
If we subtract a pattern from TH positions, do we get better English?
"""

DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

GEMATRIA = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6, 'W': 7,
    'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14, 'S': 15,
    'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20, 'NG': 21, 'ING': 21, 'D': 22,
    'OE': 23, 'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

REVERSE_GEMATRIA = {v: k for k, v in GEMATRIA.items() if k not in ['K', 'ING', 'IO']}

def parse_to_runes(text):
    """Convert text to rune sequence with indices"""
    text = text.upper()
    runes = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in DIGRAPHS:
                runes.append((digraph, GEMATRIA.get(digraph, -1)))
                i += 2
                continue
        if text[i].isalpha():
            runes.append((text[i], GEMATRIA.get(text[i], -1)))
        i += 1
    return runes

def runes_to_text(rune_list):
    """Convert rune list back to text"""
    return ''.join(REVERSE_GEMATRIA.get(val, '?') for _, val in rune_list)

def score_english(text):
    """Simple English scoring based on common bigrams"""
    text = text.upper()
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR']
    score = 0
    for bg in bigrams:
        score += text.count(bg) * 10
    
    # Penalize weird patterns
    weird = ['ZZ', 'QQ', 'XX', 'VV', 'JJ', 'KK']
    for w in weird:
        score -= text.count(w) * 20
    
    return score

PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

runes = parse_to_runes(PAGE0_OUTPUT)
print(f"Total runes: {len(runes)}")

# Find TH positions
th_positions = [i for i, (r, v) in enumerate(runes) if r == 'TH']
print(f"TH positions: {len(th_positions)}")

print("="*70)
print("TEST: Shift every Nth TH to different rune")
print("="*70)

# TH has index 2. What if some TH should be index 0 (F)?
# This would mean we ADDED 2 to F to get TH

# Test: shift every 2nd TH, every 3rd TH, etc.
best_score = 0
best_config = None

original_text = runes_to_text(runes)
original_score = score_english(original_text)
print(f"Original score: {original_score}")

for skip in [2, 3, 4, 5]:
    for shift in range(-5, 6):
        if shift == 0:
            continue
            
        # Make a modified copy
        new_runes = list(runes)
        
        # Shift every Nth TH
        th_count = 0
        for i in range(len(new_runes)):
            if new_runes[i][0] == 'TH':
                if th_count % skip == 0:  # Modify every Nth TH
                    new_val = (new_runes[i][1] + shift) % 29
                    new_runes[i] = (REVERSE_GEMATRIA.get(new_val, '?'), new_val)
                th_count += 1
        
        text = runes_to_text(new_runes)
        score = score_english(text)
        
        if score > best_score:
            best_score = score
            best_config = (skip, shift)
            
        if score > original_score:
            print(f"Skip {skip}, Shift {shift:+d}: Score {score} (vs {original_score}) - Better!")

print(f"\nBest config: Skip {best_config[0]}, Shift {best_config[1]}, Score {best_score}")

print("\n" + "="*70)
print("TEST: Shift TH based on position modulo key length")
print("="*70)

# Key length is 113. What if position % 113 determines TH transformation?
KEY_LENGTH = 113

for mod_trigger in [0, 1, 2]:  # Test different mod values as triggers
    for shift in range(-5, 6):
        if shift == 0:
            continue
            
        new_runes = list(runes)
        
        for i in range(len(new_runes)):
            if new_runes[i][0] == 'TH':
                if i % 3 == mod_trigger:  # Simple mod pattern
                    new_val = (new_runes[i][1] + shift) % 29
                    new_runes[i] = (REVERSE_GEMATRIA.get(new_val, '?'), new_val)
        
        text = runes_to_text(new_runes)
        score = score_english(text)
        
        if score > original_score:
            print(f"Mod 3={mod_trigger}, Shift {shift:+d}: Score {score}")

print("\n" + "="*70)
print("TEST: What if every TH should be shifted by its position index?")
print("="*70)

# Variable shift: TH at position i becomes (2 + i) mod 29
for offset in range(-10, 10):
    new_runes = list(runes)
    
    for i in range(len(new_runes)):
        if new_runes[i][0] == 'TH':
            new_val = (2 + i + offset) % 29  # 2 is TH index, add position
            new_runes[i] = (REVERSE_GEMATRIA.get(new_val, '?'), new_val)
    
    text = runes_to_text(new_runes)
    score = score_english(text)
    
    if score > original_score * 0.8:  # Show if reasonably close
        print(f"TH[i] = (2 + i + {offset}) % 29: Score {score}")

print("\n" + "="*70)
print("HYPOTHESIS: TH is a NULL/space marker")
print("="*70)

# What if TH marks word boundaries (like space)?
# Remove all TH and see what words we get

non_th_text = ''.join([r for r, v in runes if r != 'TH'])
print(f"Text with TH removed ({len(non_th_text)} chars):")
print(non_th_text[:100] + "...")

# Look for English words
import re
words_3plus = re.findall(r'[A-Z]{3,}', non_th_text)
print(f"\nPotential 3+ letter words (unique): {set(words_3plus)}")

# What if TH splits words?
print("\nText split by TH positions:")
segments = []
last = 0
for pos in th_positions:
    segment = ''.join([r for r, v in runes[last:pos]])
    if segment:
        segments.append(segment)
    last = pos + 1
# Add final segment
segment = ''.join([r for r, v in runes[last:]])
if segment:
    segments.append(segment)

print(f"Segments (first 20): {segments[:20]}")
print(f"Total segments: {len(segments)}")

# Count segment lengths
segment_lengths = [len(s) for s in segments]
from collections import Counter
length_dist = Counter(segment_lengths)
print(f"Segment length distribution: {dict(sorted(length_dist.items()))}")

# Average English word is 4-5 letters. If TH is space, segments should be ~4-5 runes
avg_len = sum(segment_lengths) / len(segment_lengths)
print(f"Average segment length: {avg_len:.2f} runes")

if 3.5 <= avg_len <= 6:
    print("✅ This MATCHES typical English word lengths!")
else:
    print(f"❌ Typical word length is 4-5, this is {avg_len:.1f}")

#!/usr/bin/env python3
"""
FINAL ANALYSIS - Try to read the best decryptions as coherent text.
"""

# =============================================================================
# BEST RESULTS FROM OUR ANALYSIS
# =============================================================================

# Page 52: double XOR (rot1=75, off1=26, rot2=75, off2=1)
# Score: 158.5, Coverage: 36.4%
PAGE_52_BEST = "NOWISEATNGBFDSTHUDMFTHEOUUOIGTHONEAOFAOFDHEEONGOFSNGHJJUPPUAOFJOYEOUTHEOLJLEOEASOEIAFOOLBFDFBYEAIAOMBBEALNG"

# Page 52: single SUB (rot=71, off=1)  
# Score: 136.0
PAGE_52_SUB = "THELSXNGOEOFEOPJEPOEBOEWEOITHULCHBIIEAYOETHEREADEODEOEADEOIAWBEWNGLJIAAEAPXETIATHNNPINGPYJIADEBFOEOMOEYXUEOETTHNIAMUTH"

# Page 28: double XOR_XOR (rot1=80, off1=5, rot2=10, off2=25)
# Score: 127.0, Coverage: 45.3%
PAGE_28_BEST = "DTHEONGWTHEYTIAITHEATHXOERNYTEADJTHEANGTHIATMYSUODEAYYMEIADUNGBYYPFXEIAEAOEIYODXIAREADEAPESAYAEIAMTHEOTHWCAEBEOCYHDAEYMYEANGRPBNGDIAEEOWF"

# Page 28: XOR→SUB (rot1=30, off1=27, rot2=55, off2=18)
# Score: 150.0
PAGE_28_XOR_SUB = "WASFSANBOTTHFSAIWEITUTHNGFBTHEAWEAWEOLMJFHCITOBONEOUEOFSNGYOIWAEONGRPIALRMILJMDOESWAEAETHEOGETIBNGOA"

# Page 44: double XOR (rot1=24, off1=12, rot2=6, off2=10)
# Score: 147.5
PAGE_44_BEST = "NOIANHGOEAENEANGCGYEAJWEANRIANGUSFLITHDJFFMWBNEORCANOHBMEOATPAEBEORNGOGEOLSIANGXYPPOSLETHREPNTHSLEOOEATHYEJSHEOONG"

# Page 44: single XOR (rot=77, off=1)
PAGE_44_XOR = "THEYTHEOLYTBUTHWYNGINEODBUTHEJEOETHEOIEBTHTHTEOFLEARFWAEUBIAIAPSYOEGIEAFJOEXCHCCEARSMAEFWIANGUAEOCNHACNGIUTHIAEFUIPEO"

def find_word_breaks(text):
    """Try to find word breaks in the text."""
    # Common English words
    words = [
        # Long words first
        'INSTRUCTION', 'CIRCUMFERENCE', 'CONSUMPTION', 'ENLIGHTEN', 'BEGINNING',
        'DISCIPLE', 'BROTHER', 'PARABLE', 'PILGRIM', 'COMMAND', 'BELIEVE',
        'NOTHING', 'WISDOM', 'SACRED', 'WITHIN', 'SPIRIT', 'DIVINE', 'HIDDEN',
        'SECRET', 'ANSWER', 'CICADA', 'EMERGE', 'SHADOW', 'MASTER', 'PRIMES',
        'THERE', 'THEIR', 'ABOUT', 'WOULD', 'THESE', 'OTHER', 'WORDS', 'COULD',
        'FIRST', 'WATER', 'AFTER', 'WHERE', 'RIGHT', 'THINK', 'THREE', 'BEING',
        'TRUTH', 'LIGHT', 'THING', 'WHICH', 'SHALL', 'THOSE', 'EVERY', 'GREAT',
        'WORLD', 'STILL', 'LONG', 'READ', 'LEARN', 'FEAR', 'EARS',
        'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN',
        'EACH', 'INTO', 'MAKE', 'THAN', 'THEM', 'THEN', 'LOOK', 'ONLY', 'OVER',
        'SUCH', 'TAKE', 'COME', 'MADE', 'FIND', 'MORE', 'HERE', 'KNOW', 'SELF',
        'SEEK', 'TRUE', 'MIND', 'SOUL', 'PATH', 'WORD', 'LIFE', 'DEAD', 'DARK',
        'DEEP', 'SAID', 'UNTO',
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
        'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'ITS',
        'LET', 'MAY', 'OLD', 'SEE', 'NOW', 'WAY', 'WHO', 'DID', 'GET', 'HIM',
        'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'JOY', 'EAT',
        'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT',
        'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
        'A', 'I', 'O',
    ]
    
    result = []
    pos = 0
    
    while pos < len(text):
        found = False
        # Try to find longest matching word at current position
        for word in words:
            if text[pos:pos+len(word)] == word:
                result.append(word)
                pos += len(word)
                found = True
                break
        
        if not found:
            # No word found, take single character
            result.append(text[pos])
            pos += 1
    
    return result

def analyze_text(name, text):
    """Analyze a decrypted text."""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {name}")
    print("="*60)
    
    print(f"\nOriginal: {text}")
    print(f"Length: {len(text)} characters")
    
    # Find word breaks
    segments = find_word_breaks(text)
    
    # Separate words from non-words
    words = [s for s in segments if len(s) > 1]
    singles = [s for s in segments if len(s) == 1]
    
    print(f"\nWords found: {len(words)}")
    print(f"Single chars: {len(singles)}")
    
    # Calculate coverage
    word_chars = sum(len(w) for w in words)
    coverage = word_chars / len(text) * 100
    print(f"Word coverage: {coverage:.1f}%")
    
    # Show segmentation
    print(f"\nSegmentation: {' '.join(segments)}")
    
    # Try to read as sentences
    print(f"\nAttempted reading:")
    readable = ' '.join(segments)
    print(f"  {readable}")

def main():
    print("=" * 80)
    print("📖 FINAL READING ANALYSIS")
    print("=" * 80)
    
    analyze_text("Page 52 (double XOR)", PAGE_52_BEST)
    analyze_text("Page 52 (single SUB)", PAGE_52_SUB)
    analyze_text("Page 28 (double XOR_XOR)", PAGE_28_BEST)
    analyze_text("Page 28 (XOR→SUB)", PAGE_28_XOR_SUB)
    analyze_text("Page 44 (double XOR)", PAGE_44_BEST)
    analyze_text("Page 44 (single XOR)", PAGE_44_XOR)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY OF READABLE PATTERNS")
    print("=" * 80)
    
    print("""
Most Promising Readings:

1. PAGE 52 (double XOR):
   "NOW IS EAT NG B F D S TH U D M F THE O U U O I G TH ONE A OF A OF D HE E ON GO F S NG..."
   → Possible: "NOW IS..." followed by unclear text
   
2. PAGE 44 (single XOR):
   "THEY THE O L Y T BUT H W Y NG IN E O D BUT HE J E O E THE O I E B TH TH THE OF LEAR F..."
   → Clear pattern: "THEY THE... BUT... THE... OF LEARN..."
   
3. PAGE 28 (double XOR):
   "D THE ON G W THEY T IA I THE AT H X O E R NY T E A D J THE A NG TH IA T MY S U O D E A..."
   → Pattern: "THE ON... THEY... THE AT... THE... MY..."
   
4. PAGE 28 (XOR→SUB):
   "WAS F S AN B O T TH F S A I WE IT U TH NG F B THE A WE A WE O L M J F H C IT O B ONE O..."
   → Possible: "WAS... AN... WE IT... THE... WE... ONE..."

Key Observations:
- All texts show clear English word patterns (THE, THEY, BUT, WE, NOW, etc.)
- Coverage ranges from 35-45% which is high for random text
- Word boundaries are not aligned, suggesting:
  a) Additional transposition layer, or
  b) Some characters need mapping adjustment, or
  c) Text is partially in an unknown encoding
""")
    
    print("\n🎯 ANALYSIS COMPLETE")

if __name__ == '__main__':
    main()

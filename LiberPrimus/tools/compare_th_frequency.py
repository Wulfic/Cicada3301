"""
Compare TH rune frequency in our decrypted output vs known solved Cicada texts
"""

# Digraphs in Gematria Primus (each is a SINGLE rune)
DIGRAPHS = ['TH', 'NG', 'EA', 'AE', 'IA', 'EO', 'OE']

def parse_to_runes(text):
    """Convert text to rune sequence, treating digraphs as single runes"""
    text = text.upper()
    runes = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in DIGRAPHS:
                runes.append(digraph)
                i += 2
                continue
        if text[i].isalpha():
            runes.append(text[i])
        i += 1
    return runes

def count_rune_frequency(runes):
    """Count frequency of each rune"""
    counts = {}
    for rune in runes:
        counts[rune] = counts.get(rune, 0) + 1
    return counts

def analyze_text(name, text):
    """Analyze a text and report TH frequency"""
    runes = parse_to_runes(text)
    counts = count_rune_frequency(runes)
    total = len(runes)
    
    th_count = counts.get('TH', 0)
    th_pct = (th_count / total * 100) if total > 0 else 0
    
    # Count THE (TH + E)
    the_count = 0
    for i in range(len(runes) - 1):
        if runes[i] == 'TH' and runes[i+1] == 'E':
            the_count += 1
    
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"Total runes: {total}")
    print(f"TH count: {th_count} ({th_pct:.1f}%)")
    print(f"THE count (TH+E pairs): {the_count}")
    
    # Top 5 runes
    sorted_counts = sorted(counts.items(), key=lambda x: -x[1])[:10]
    print(f"Top 10 runes: {sorted_counts}")
    
    return th_pct, the_count, total

# Our Page 0 first-layer output
PAGE0_OUTPUT = """AETHATAEYETHESTHESTHEAEATHEORNGTHROTHIASTHDIATHETHEANGENEATHESTHEAAETHATHTHEOFLETHEATHTHYC/KHTHEADTHEOTHBTMINGDOETHESTHITHEONTHEATHLATHEOEALNTHEATHEOEATHOUMTOEDTHIAOETHEESTHEOTHEATHEAGOETHNTHEOC/KLYDTHEAXTHANTPLTHEIADTHTHEATHAESIGTHEREANUPTTHEOTHEATHINGNTHEOFHATHENTHEASTHWIASTHEATHANTHEAJRDINTHESOEDNTHEDTHATHERETHNGTHEOTHEATHETHEARTHENTHEAINGXTHMITHEATHEAGMYEEOOTIXWTHEATHPHNGTHEAXATHPIASTHIPL"""

# Solved Page 57 - The Parable (plaintext)
PAGE57_PARABLE = """PARABLELIKETHEINSTARTUNELINGTOTHESURFACEWEMUSTSHEDDOUROWNFIRMUMFERENCEFINDTHEDIVINITYWITHINDANDEMERGE"""

# Solved Page 56 - An End
PAGE56_ANEND = """WITHINTHADEEPWEBTHEREEXISTSAPAGETHATSHASHESTOANUMBERITISTHEDUTYOFEVERYPILGRIMTOSEEKOUTTHISPAGE"""

# A WARNING (from onion pages - Atbash solved)
A_WARNING = """AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETRUEESTTHEKNOWLEDGEFINDYOURTHUEXPERIENCEYOURDEATHDONOTEDITORCHANGETHISBOOKORTHEMESSAGECONTAINEDWITHINTEITHERTHEWORDSORTHERENUMBERSFORALLISSACRED"""

# WELCOME (from onion pages - Vigenere DIVINITY)
WELCOME = """WELCOMEWELCOMEPILGRIMTOTHEGREATJOURNEYTOWARDTHEENDOFALLTHINGSITISNOTANEASYTRIPBUTFORTHOSEWHOFINDTHEIRWAYHEREISANECESSARYONE"""

# SOME WISDOM (from onion pages - plaintext)
SOME_WISDOM = """SOMEWISDOMTHEPRIMESARESACREDTHETOTIENTFUNCTIONISSACREDALLTHINGSSHOULDBEENCRYPTEDKNOWTHIS"""

# Known sample of Old English for comparison
OLD_ENGLISH_SAMPLE = """THENWASSODTHEGODEWERODSMONDIHTHUISETHESECGSHEWORLDHISMONDRIHTENMETODMIHTIGWELLETEAHTEOFETHERTHANWETHEGMOTANDODUNDANEWOLDANTWEONODWEOROLDETOSOMNETHETODOLDE"""

print("="*60)
print("TH RUNE FREQUENCY COMPARISON")
print("="*60)

results = []
results.append(("Our Page 0 Decrypted", *analyze_text("Our Page 0 Decrypted", PAGE0_OUTPUT)))
results.append(("Page 57 Parable (solved)", *analyze_text("Page 57 Parable (solved)", PAGE57_PARABLE)))
results.append(("Page 56 An End (solved)", *analyze_text("Page 56 An End (solved)", PAGE56_ANEND)))
results.append(("A Warning (onion)", *analyze_text("A Warning (onion)", A_WARNING)))
results.append(("Welcome (onion)", *analyze_text("Welcome (onion)", WELCOME)))
results.append(("Some Wisdom (onion)", *analyze_text("Some Wisdom (onion)", SOME_WISDOM)))
results.append(("Old English Sample", *analyze_text("Old English Sample", OLD_ENGLISH_SAMPLE)))

print("\n" + "="*60)
print("SUMMARY COMPARISON")
print("="*60)
print(f"{'Text':<30} {'TH%':>8} {'THE pairs':>10} {'Total':>8}")
print("-"*60)
for name, th_pct, the_count, total in results:
    print(f"{name:<30} {th_pct:>7.1f}% {the_count:>10} {total:>8}")

# Calculate if our TH frequency is anomalous
avg_th_pct = sum(r[1] for r in results[1:]) / len(results[1:])  # Exclude our page
our_th_pct = results[0][1]

print(f"\n{'='*60}")
print("ANALYSIS")
print("="*60)
print(f"Our Page 0 TH: {our_th_pct:.1f}%")
print(f"Average of solved texts: {avg_th_pct:.1f}%")
print(f"Difference: {our_th_pct - avg_th_pct:+.1f} percentage points")

if our_th_pct > avg_th_pct * 1.5:
    print("\n⚠️  WARNING: Our TH frequency is >50% higher than solved texts!")
    print("   This may indicate:")
    print("   1. Another cipher layer affecting TH specifically")
    print("   2. Different content style")
    print("   3. Decryption issue")
elif our_th_pct > avg_th_pct * 1.2:
    print("\n⚠️  NOTICE: Our TH frequency is 20-50% higher than solved texts")
    print("   May need investigation but could be normal variation")
else:
    print("\n✅ TH frequency is within normal range for Cicada texts")

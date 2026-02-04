"""
Page 20 Non-Primes - Word Segmentation Analysis
================================================
The decrypted texts have high IoCs. Let's try to segment them into words.
"""

from collections import defaultdict

RUNEGLISH = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
             'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']

# Extended English word list including Old English variants
WORDS = set([
    # Common English
    'A', 'I', 'AM', 'AN', 'AS', 'AT', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'SO', 'TO', 'UP', 'US', 'WE',
    'ALL', 'AND', 'ANY', 'ARE', 'BUT', 'CAN', 'DID', 'FOR', 'GOT', 'HAD', 'HAS', 'HER', 'HIM', 'HIS', 'HOW', 'ITS', 'LET', 'MAY', 'MET', 'NOT', 'NOW', 'OLD', 'ONE', 'OUR', 'OUT', 'OWN', 'SAY', 'SEE', 'SHE', 'THE', 'TOO', 'TWO', 'WAY', 'WHO', 'WHY', 'YES', 'YOU',
    'THAT', 'THIS', 'WITH', 'HAVE', 'FROM', 'THEY', 'BEEN', 'SAID', 'EACH', 'WOULD', 'COULD', 'WHICH', 'THEIR', 'ABOUT', 'THERE', 'THESE', 'WHAT', 'WHEN', 'WHERE', 'WILL', 'JUST', 'ONLY', 'OVER', 'ALSO', 'SUCH', 'SOME', 'SAME', 'TIME', 'WORK', 'BACK', 'KNOW', 'GOOD', 'WELL', 'HIGH', 'MAKE', 'COME', 'MOST', 'YEAR', 'GIVE', 'FIND', 'TELL', 'THINK', 'FEEL', 'SHOW', 'TAKE', 'GET', 'PUT', 'KEEP', 'TURN',
    # Old English / Mystical / Cicada themed
    'DEATH', 'PATH', 'TRUTH', 'SEEK', 'SEEKER', 'WISDOM', 'SACRED', 'AEON', 'REAPER', 'LIFE', 'SOUL', 'MIND', 'SPIRIT', 'SELF', 'OTHER', 'WITHIN', 'BEYOND', 'LIGHT', 'DARK', 'SHADOW', 'VOID', 'KNOW', 'KNOWING', 'BEING', 'BECOMING',
    'THEE', 'THOU', 'THINE', 'HATH', 'DOTH', 'YET', 'LO', 'ART', 'WAS', 'ERE', 'NAY', 'NIGH', 'HEED', 'HEARKEN',
    'ODE', 'BID', 'ALT', 'EO', 'AE', 'EA', 'IA', 'NG', 'TH', 'OE', 'EW', 'AW', 'OW', 'OON',
    'SONG', 'TELL', 'TOLD', 'KNOW', 'KNEW', 'SEEN', 'CAME', 'COME', 'WENT', 'GONE',
    'HO', 'OH', 'AH', 'YE', 'MATH', 'EAT', 'ATE', 'MEAT', 'HEAT', 'SEAT', 'BEAT', 'FEAT', 'GREAT', 'LATE', 'FATE', 'RATE', 'GATE', 'MATE', 'DATE', 'HATE',
    'DEOR', 'WELA', 'MUND', 'HELM', 'WARD', 'WYRD', 'WEALD', 'MEOD', 'MEAD', 'LEAD', 'READ', 'DEAD', 'DREAD', 'SPREAD',
    'HEAL', 'HEED', 'FEED', 'NEED', 'DEED', 'SEED', 'WEED', 'FREED', 'BREED', 'GREED',
    'DOE', 'FOE', 'HOE', 'WOE', 'TOE', 'ROE', 'BOE', 'FLOE', 'SLOE',
    'OFT', 'SIN', 'WIN', 'TIN', 'FIN', 'BIN', 'DIN', 'KIN', 'PIN', 'THIN', 'CHIN', 'SPIN', 'GRIN',
    'THY', 'WHY', 'TRY', 'CRY', 'DRY', 'FRY', 'PRY', 'SHY', 'SKY', 'SPY', 'PLY', 'FLY', 'SLY',
    'LONG', 'SONG', 'WRONG', 'STRONG', 'ALONG', 'AMONG',
    'DARK', 'MARK', 'PARK', 'BARK', 'HARK', 'LARK', 'SPARK',
    'LATE', 'FATE', 'GATE', 'RATE', 'MATE', 'DATE', 'HATE', 'PLATE', 'STATE', 'CREATE',
    'RAIN', 'PAIN', 'GAIN', 'MAIN', 'VAIN', 'PLAIN', 'TRAIN', 'BRAIN', 'STRAIN',
    'EAR', 'DEAR', 'FEAR', 'GEAR', 'HEAR', 'NEAR', 'PEAR', 'REAR', 'SEAR', 'TEAR', 'WEAR', 'YEAR', 'CLEAR', 'SMEAR', 'SPEAR',
    'EYE', 'DYE', 'LYE', 'RYE', 'TYE', 'BYE',
    # Additional related words
    'PRAYER', 'PRAY', 'NIGHT', 'RIGHT', 'SIGHT', 'FIGHT', 'LIGHT', 'MIGHT', 'TIGHT', 'FRIGHT', 'FLIGHT', 'BLIGHT', 'PLIGHT', 'SLIGHT',
    'DOOR', 'FLOOR', 'POOR', 'MOOR', 'BOOK', 'LOOK', 'TOOK', 'GOOD', 'FOOD', 'WOOD', 'STOOD',
    'LOVE', 'MOVE', 'ABOVE', 'DOVE', 'COVE', 'ROVE', 'WOVE', 'DROVE', 'GROVE', 'PROVE', 'STOVE', 'SHOVE',
    'HAND', 'LAND', 'SAND', 'BAND', 'GRAND', 'BRAND', 'STRAND', 'STAND', 'COMMAND',
    'HEART', 'START', 'PART', 'ART', 'CART', 'DART', 'SMART', 'CHART',
    'REST', 'BEST', 'FEST', 'JEST', 'NEST', 'PEST', 'TEST', 'VEST', 'WEST', 'QUEST', 'GUEST', 'BLESSED', 'DRESSED', 'STRESSED',
])

def segment_dp(text, words_set, max_word_len=20):
    """Dynamic programming word segmentation"""
    n = len(text)
    dp = [None] * (n + 1)
    dp[0] = []
    
    for i in range(1, n + 1):
        for j in range(max(0, i - max_word_len), i):
            word = text[j:i]
            if word in words_set and dp[j] is not None:
                candidate = dp[j] + [word]
                if dp[i] is None:
                    dp[i] = candidate
    
    return dp[n] if dp[n] else []

# Load the results from file or recreate them
results = {
    'SUB_166stream': 'EOHOPTHHIALWOYNIUROCUOCEARJILFAEOEBTHDEEARSHBWOLLGTHLWYUMRSSILRXYAPUUMTHSATIILPMGUDFTHAYONYCAYOEEAFALYYPWYDNGNTHADMEAAEEAEOGNPETHTNTHWBRNGYFMLAEJAEOLEATHFDIAOCXEADDMWOEDTHJUGSLTHJCIXNIEASAEULTRATHCAEICIMYAHAELLUIDIAEEECEANBPOJORFSEANCWTSTIIATWRMAEHSYAEIALFXJIAOTUIOEITHYOEJPLEAXOENEAERAEIACNPDEOTHNEAJHIAAETHAEAEGTHNDUOEAEEOTYTYPENTHDTYTEUTHEATHHNGJEOTHUUYOAEXTHCWHBBEOAEIEAEMTAEUNGDGOUDWFEOTHIAJREOEOIAAAJAEGBFIARRRNMAEBBEITDMEOFCNOEGEOEARDSBMOEYSDOEEBJOEEOPCOYJLEELLEINTHAEGCCHAEOAERUOENGJFBSOLWXIYEOTHFXROWTTHWNXEARXJICNGEOYRTHYEOUAEOSIXSAEJPAEGTHNNAWWAENGNEEHNGHCCYNGNOHISEATHAIAAHNGTHXGAEEAYNGHAEDRSBAEFRBOEBHRAEDAEAEOEDIAIALNGEOOEMDWIACYHEAIBNEATXSIAUJXASUSPOEXYOONGYEONSEAUTHBIAXETOEFAEEAPMWTGAAXRGLAEHHFIAEAJOLCEOEHPWBYOLUELGHHRUOEOESEAGEOLCTSICGTHDIAIAAIHNRLIWTYEOEYXINTEATBUUNGYDMWGXJFWWCSIBEOSEAAEEDLIAYTHCTHOYNGIEAENJBCLTTUGAEEAIANG',
    'Shift_16': 'RACSNAFNGXGEABIOEHAECOELPOEEOJYOEIEAOUEODTUOEREOBRTHULOENGPUCBHJGAEFIAAEOINGEOREAOEEPYOYEOEASPGJSIEAEOUWAEDFGEOTHJOEFYWSAEWAENRJAEEOLOISXFBNGCRCEAOENEOEAEAIATNGLOTHOHPIENFSMDAEWJIANGNMEOCPFTBWEPIAEOUIAIMEAEAUEOTDYDATTHNGEONGRJIYIADOEDMOEJEYTBJNGOIACXOAEEOMCCERCXIAPGXMEOIAHLRXNWCNGBIHMDMNCAAEIAJOESUABLMRGMSAEPSEODMMIJJNREOIANTHOTHFGFEOEPEMSYDEAEICACOLEOEITGMOBOYJNGSGYIAABRBUHFIARFODLAGOOEBTHEAEFRGEAUIASHXAEIABMFAEDAUGIAMACEOBUOEXHCUYEAEOLNGTHNAEMNEAAEYOTHIAJLXTHDWYHMEAEWIJRBEXPAESIATHRXBIANGANORPCWDTEEAGTHIGXMWHTHEAMCIAWIAAEONGDSYIAIAEAECAECTHEOWBRAEFIAFIBAEYAEYTDRPAENHICPIPOERIAFOEEADTEXEOFMEHIAAESAIARGTHRYJTHLGOEHNGWAESAESASBEEOHXAYINEAEOFIWINPNGTGOGAMXJBJEDGAYUCISTNEOIAJTHRBWEOANEOMDNXHAHNGPWRDEOGITXUMCXCEAXEFWNYAUNGBDMNGILOAEOENWCAEACETHEOIAHIHXFEETAEGNFIAENGWAEIAUEONAEOHUTHLJRDJEAYRSHAJWBWGSBIAGLIWFMRNGLOBCPEBNUMYIWHBHIAGXD',
}

print("="*70)
print("WORD SEGMENTATION ANALYSIS")
print("="*70)

for name, text in results.items():
    print(f"\n{'='*70}")
    print(f"Method: {name}")
    print(f"{'='*70}")
    
    # Try basic word search (no segmentation)
    print("\n1. BASIC WORD SEARCH (greedy):")
    found_words = []
    for word in sorted(WORDS, key=len, reverse=True):
        if word in text:
            found_words.append(word)
    
    if found_words:
        print(f"   Found {len(found_words)} words: {sorted(found_words)}")
        for word in sorted(found_words):
            idx = text.find(word)
            print(f"     {word} at position {idx}")
    else:
        print("   No words found")
    
    # Try segmentation
    print("\n2. DYNAMIC PROGRAMMING SEGMENTATION:")
    segmented = segment_dp(text, WORDS)
    if segmented:
        print(f"   Segmented into {len(segmented)} words:")
        print(f"   {' '.join(segmented[:50])}")  # First 50 words
        if len(segmented) > 50:
            print(f"   ... ({len(segmented) - 50} more words)")
    else:
        print("   No segmentation found (check with looser constraints)")
    
    # Character frequency analysis
    print("\n3. CHARACTER FREQUENCY:")
    from collections import Counter
    freq = Counter(text)
    for char, count in freq.most_common(10):
        pct = count / len(text) * 100
        print(f"   {char}: {count} ({pct:.1f}%)")
    
    # Look for patterns
    print("\n4. PATTERN SEARCH:")
    patterns = ['THETHE', 'ANDAND', 'THEAND', 'THEBUT', 'THEAT', 'THEOR', 'THEOF', 'WITHTHE', 'FROMTHE']
    for pattern in patterns:
        if pattern in text:
            print(f"   Found pattern: {pattern}")

# Additional analysis: check if trigrams form words
print("\n" + "="*70)
print("TRIGRAM WORD PATTERNS")
print("="*70)

text = results['SUB_166stream']
trigrams = set()
for i in range(len(text)-2):
    trigram = text[i:i+3]
    if trigram in WORDS:
        trigrams.add(trigram)

print(f"\nTrigrams that match words: {sorted(trigrams)}")

# Try to find sentence patterns
print("\n" + "="*70)
print("LOOKING FOR SENTENCE-LIKE PATTERNS (A THE THE)")
print("="*70)

for i in range(len(text)-10):
    substr = text[i:i+9]
    # Check if this looks like a sentence starter
    if any(word in substr for word in ['THETHE', 'ATHEA', 'THEAT', 'ATHTHE']):
        print(f"Position {i}: {substr}")

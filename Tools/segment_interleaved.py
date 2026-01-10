"""
Page 20 - Dictionary-based word segmentation
=============================================
The interleaved 166-stream contains English words.
Use dynamic programming to find optimal word boundaries.
"""

# The interleaved stream
INTERLEAVED = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"

# Common English words (sorted by length for greedy matching)
DICTIONARY = {
    # Articles, pronouns, prepositions
    'A', 'I', 'O', 'OF', 'TO', 'IN', 'IT', 'IS', 'HE', 'WE', 'ME', 'MY', 'BY', 'SO', 'NO', 'OR', 'AT', 'AN', 'IF', 'AS', 'BE', 'DO', 'UP',
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HIS', 'HAS', 'HAD', 'WHO', 'WAY', 'MAY', 'SAY', 'DAY',
    'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'WERE', 'SAID', 'EACH', 'MAKE', 'LIKE', 'TIME', 'JUST', 'KNOW', 'TAKE', 'COME',
    'THEIR', 'WOULD', 'THERE', 'COULD', 'ABOUT', 'OTHER', 'WHICH', 'THESE', 'FIRST', 'AFTER', 'YEARS', 'THOSE',
    
    # Old English / Runeglish words
    'YE', 'YEA', 'NAY', 'THY', 'THEE', 'THOU', 'THINE', 'HATH', 'DOTH', 'THUS', 'HENCE', 'FORTH', 'UNTO',
    'ART', 'ERE', 'OFT', 'HITHER', 'THITHER', 'WHITHER', 'WHEREFORE',
    
    # Common content words
    'MAN', 'MEN', 'GOD', 'WAR', 'DAY', 'WAY', 'SEA', 'SUN', 'SON', 'LIFE', 'LOVE', 'WORD', 'WORK', 'WORLD', 'EARTH', 'HEART',
    'LONE', 'ALONE', 'STONE', 'BONE', 'TONE', 'ZONE', 'DONE', 'GONE', 'NONE', 'ONE',
    'DEATH', 'DEAD', 'DIE', 'DIED', 'PATH', 'TRUTH', 'FAITH', 'LIGHT', 'NIGHT', 'RIGHT', 'MIGHT',
    
    # Cicada themes
    'PRIME', 'PRIMES', 'SACRED', 'DIVINE', 'DIVINITY', 'WISDOM', 'PILGRIM', 'INSTAR', 'EMERGE', 'WITHIN', 'CIPHER',
    'CIRCUMFERENCE', 'TOTIENT', 'ENCRYPT', 'RUNE', 'RUNES', 'DEOR', 'SONG', 'POEM', 'VERSE', 'KEY',
    'REAPER', 'AEON', 'MEAN', 'RATIO', 'LENGTH', 'NUMBER', 'DIAGONAL', 'GRID', 'COLUMN',
    
    # Verbs
    'AM', 'IS', 'BE', 'GO', 'DO', 'SEE', 'KNOW', 'FIND', 'SEEK', 'HEAR', 'FEEL', 'TAKE', 'GIVE', 'COME', 'MAKE', 'THINK', 'LOOK',
    'MET', 'SET', 'GET', 'LET', 'BET', 'YET', 'NET', 'WET',
    
    # More words found in context
    'FALT', 'FAULT', 'ALT', 'HALT', 'SALT', 'MALT',  # FALT = OE for fault/sin
    'SELF', 'HELP', 'FELT', 'MELT', 'BELT', 'DEALT',
    'ODE', 'MODE', 'CODE', 'NODE', 'BODE', 'RODE',
    'EO', 'OE', 'AE', 'TH', 'NG', 'EA', 'IA',  # Runeglish digraphs as "words"
    
    # Single letters that might be valid
    'F', 'U', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'J', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'D', 'Y',
}

def segment_words(text, dictionary):
    """
    Use dynamic programming to find word segmentation that maximizes
    total word length (prefers longer words).
    
    Returns list of (score, segmentation) for top solutions.
    """
    n = len(text)
    
    # dp[i] = (best_score, best_segmentation) ending at position i
    dp = [(0, [])] * (n + 1)
    dp[0] = (0, [])
    
    for i in range(1, n + 1):
        best_score = -1
        best_seg = None
        
        # Try all possible word endings at position i
        for j in range(max(0, i - 15), i):  # Max word length 15
            word = text[j:i]
            if word in dictionary:
                prev_score, prev_seg = dp[j]
                # Score: word length squared (favor longer words)
                word_score = len(word) ** 2 if len(word) > 1 else 0.1
                new_score = prev_score + word_score
                
                if new_score > best_score:
                    best_score = new_score
                    best_seg = prev_seg + [word]
        
        if best_seg is not None:
            dp[i] = (best_score, best_seg)
        else:
            # No word found - try single character
            prev_score, prev_seg = dp[i-1]
            dp[i] = (prev_score - 0.5, prev_seg + [text[i-1]])  # Penalty for unmatched
    
    return dp[n]

def segment_greedy(text, dictionary):
    """Greedy longest-match segmentation"""
    result = []
    i = 0
    while i < len(text):
        # Try longest match first
        found = False
        for length in range(min(15, len(text) - i), 0, -1):
            word = text[i:i+length]
            if word in dictionary:
                result.append(word)
                i += length
                found = True
                break
        
        if not found:
            result.append(text[i])
            i += 1
    
    return result

print("="*60)
print("Word Segmentation Analysis")
print("="*60)

print(f"\nInterleaved stream ({len(INTERLEAVED)} chars):")
print(f"{INTERLEAVED[:80]}...")

# Try different portions
portions = [
    ("Full stream", INTERLEAVED),
    ("First half", INTERLEAVED[:83]),
    ("Second half", INTERLEAVED[83:]),
    ("Around THE LONE", INTERLEAVED[15:50]),
    ("Middle section", INTERLEAVED[40:100]),
]

for name, text in portions:
    print(f"\n--- {name} ---")
    print(f"Text: {text}")
    
    # DP segmentation
    score, words = segment_words(text, DICTIONARY)
    print(f"\nDP segmentation (score={score:.1f}):")
    print(f"  {' '.join(words)}")
    
    # Count recognized words
    recognized = [w for w in words if len(w) > 1 and w in DICTIONARY and w not in 'EAOIU']
    print(f"  Recognized words: {recognized}")

# Focus on the THE LONE region
print("\n" + "="*60)
print("Detailed analysis of THE LONE region")
print("="*60)

region = INTERLEAVED[10:60]
print(f"\nRegion: {region}")

# Try all possible word parses
print("\nManual parse attempts:")
parses = [
    "OME T BID AM SE FALT THE LONE TN HER A AU IO AE TIO AE A YO ME",
    "O MET BID AM SELF ALT THE LONE TN HER A A U IO AE TIO AE A YO ME",
    "O MET B I DAM SE FALT THE LONE T N HER A A U I O AE T I O AE A YO ME",
    "OME T BID AM S E FALT THE LONE TN HE RA AU IO AE TIO AE AYO ME",
]

for parse in parses:
    words = parse.split()
    # Score by recognized words
    recognized = [w for w in words if w in DICTIONARY and len(w) > 1]
    print(f"  Parse: {parse}")
    print(f"    Recognized: {recognized}")
    print()

# What about if we look for "THE LONE" as a key phrase?
print("="*60)
print("THE LONE as key phrase")
print("="*60)

print("\nIn Old English context:")
print("  'THE LONE' could mean 'the solitary one' or 'the lonely'")
print("  Related to 'alone' (all + one)")
print("  In Deor poem context: The poet is 'the lone' lamenter")

print("\nIn Cicada context:")
print("  'THE LONE' could refer to the solitary solver")
print("  'THE LONE PATH' - pilgrimage theme")
print("  'THE LONE PRIME' - mathematical theme?")

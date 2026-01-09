
import os
import multiprocessing
import itertools
from collections import Counter
import time

# --- CONSTANTS ---

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

RUNES_INV = {v: k for k, v in RUNE_MAP.items()}

# Mapping from rune index (0-28) to English output (simplified)
# Note: This is an approximation for scoring. 
# Runes map to sounds, but we map to nearest English letter for trigram analysis.
# We treat TH, EO, NG, AE as single tokens for scoring? 
# No, usually we expand them to score English text.
# 2: TH -> T, H ? 
# 21: NG -> N, G ?
# 25: AE -> A, E ?
# 12: EO -> E, O ?
# Let's map to single distinct chars for internal scoring to keep it simple, 
# OR expand them. Expanding is better for actual English trigrams.
RUNE_TO_TEXT_DECODE = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# Top English Trigrams (Frequency per 1000 roughly)
TRIGRAMS = {
    'THE': 18, 'AND': 7, 'ING': 7, 'HER': 3, 'THA': 6, 'ERE': 3,
    'FOR': 3, 'ENT': 4, 'ION': 4, 'TER': 2, 'WAS': 4, 'YOU': 3,
    'ITH': 3, 'VER': 2, 'ALL': 2, 'WIT': 2, 'THI': 3, 'TIO': 3
}

COMMON_WORDS = [
    "CICADA", "PRIMUS", "LIBER", "TOTIENT", "PRIME", "CIRCUMFERENCE", 
    "MESSAGE", "WARNING", "BELIEVE", "NOTHING", "BOOK", "TRUE", "KNOWLEDGE",
    "FIND", "TRUTH", "EXPERIENCE", "DEATH", "SACRED", "NUMBERS", "WORDS",
    "INTUS", "CHAPTER", "SECTION", "INSTAR", "EMERGENCE", "DIVINITY",
    "PILGRIM", "JOURNEY", "INSTRUCTION", "ENLIGHTENMENT", "CONSUMPTION",
    "PRESERVATION", "INTELLIGENCE", "SYSTEM", "WITHIN", "INTERCONNECTEDNESS",
    "SELFRELIANCE", "COMMAND"
]

# Large Dictionary imported from previous step
LARGE_DICT = [
    "THE", "OF", "TO", "AND", "A", "IN", "IS", "IT", "YOU", "THAT", "HE", "WAS", "FOR", "ON", "ARE", "WITH", "AS", "I", "HIS", "THEY", "BE", "AT", "ONE", "HAVE", "THIS", "FROM", "OR", "HAD", "BY", "NOT", "WORD", "BUT", "WHAT", "SOME", "WE", "CAN", "OUT", "OTHER", "WERE", "ALL", "THERE", "WHEN", "UP", "USE", "YOUR", "HOW", "SAID", "AN", "EACH", "SHE", "WHICH", "DO", "THEIR", "TIME", "IF", "WILL", "WAY", "ABOUT", "MANY", "THEN", "THEM", "WRITE", "WOULD", "LIKE", "SO", "THESE", "HER", "LONG", "MAKE", "THING", "SEE", "HIM", "TWO", "HAS", "LOOK", "MORE", "DAY", "COULD", "GO", "COME", "DID", "NUMBER", "SOUND", "NO", "MOST", "PEOPLE", "MY", "OVER", "KNOW", "WATER", "THAN", "CALL", "FIRST", "WHO", "MAY", "DOWN", "SIDE", "BEEN", "NOW", "FIND", "ANY", "NEW", "WORK", "PART", "TAKE", "GET", "PLACE", "MADE", "LIVE", "WHERE", "AFTER", "BACK", "LITTLE", "ONLY", "ROUND", "MAN", "YEAR", "CAME", "SHOW", "EVERY", "GOOD", "ME", "GIVE", "OUR", "UNDER", "NAME", "VERY", "THROUGH", "JUST", "FORM", "SENTENCE", "GREAT", "THINK", "SAY", "HELP", "LOW", "LINE", "DIFFER", "TURN", "CAUSE", "MUCH", "MEAN", "BEFORE", "MOVE", "RIGHT", "BOY", "OLD", "TOO", "SAME", "TELL", "DOES", "SET", "THREE", "WANT", "AIR", "WELL", "ALSO", "PLAY", "SMALL", "END", "PUT", "HOME", "READ", "HAND", "PORT", "LARGE", "SPELL", "ADD", "EVEN", "LAND", "HERE", "MUST", "BIG", "HIGH", "SUCH", "FOLLOW", "ACT", "WHY", "ASK", "MEN", "CHANGE", "WENT", "LIGHT", "KIND", "OFF", "NEED", "HOUSE", "PICTURE", "TRY", "US", "AGAIN", "ANIMAL", "POINT", "MOTHER", "WORLD", "NEAR", "BUILD", "SELF", "EARTH", "FATHER", "HEAD", "STAND", "OWN", "PAGE", "SHOULD", "COUNTRY", "FOUND", "ANSWER", "SCHOOL", "GROW", "STUDY", "STILL", "LEARN", "PLANT", "COVER", "FOOD", "SUN", "FOUR", "BETWEEN", "STATE", "KEEP", "EYE", "NEVER", "LAST", "LET", "THOUGHT", "CITY", "TREE", "CROSS", "FARM", "HARD", "START", "MIGHT", "STORY", "SAW", "FAR", "SEA", "DRAW", "LEFT", "LATE", "RUN", "DON'T", "WHILE", "PRESS", "CLOSE", "NIGHT", "REAL", "LIFE", "FEW", "NORTH", "OPEN", "SEEM", "TOGETHER", "NEXT", "WHITE", "CHILDREN", "BEGIN", "GOT", "WALK", "EXAMPLE", "EASE", "PAPER", "GROUP", "ALWAYS", "MUSIC", "THOSE", "BOTH", "MARK", "OFTEN", "LETTER", "UNTIL", "MILE", "RIVER", "CAR", "FEET", "CARE", "SECOND", "BOOK", "CARRY", "TOOK", "SCIENCE", "EAT", "ROOM", "FRIEND", "BEGAN", "IDEA", "FISH", "MOUNTAIN", "STOP", "ONCE", "BASE", "HEAR", "HORSE", "CUT", "SURE", "WATCH", "COLOR", "FACE", "WOOD", "MAIN", "ENOUGH", "PLAIN", "GIRL", "USUAL", "YOUNG", "READY", "ABOVE", "EVER", "RED", "LIST", "THOUGH", "FEEL", "TALK", "BIRD", "SOON", "BODY", "DOG", "FAMILY", "DIRECT", "POSE", "LEAVE", "SONG", "MEASURE", "DOOR", "PRODUCT", "BLACK", "SHORT", "NUMERAL", "CLASS", "WIND", "QUESTION", "HAPPEN", "COMPLETE", "SHIP", "AREA", "HALF", "ROCK", "ORDER", "FIRE", "SOUTH", "PROBLEM", "PIECE", "TOLD", "KNEW", "PASS", "SINCE", "TOP", "WHOLE", "KING", "SPACE", "HEARD", "BEST", "HOUR", "BETTER", "TRUE", "DURING", "HUNDRED", "FIVE", "REMEMBER", "STEP", "EARLY", "HOLD", "WEST", "GROUND", "INTEREST", "REACH", "FAST", "VERB", "SING", "LISTEN", "SIX", "TABLE", "TRAVEL", "LESS", "MORNING", "TEN", "SIMPLE", "SEVERAL", "VOWEL", "TOWARD", "WAR", "LAY", "AGAINST", "PATTERN", "SLOW", "CENTER", "LOVE", "PERSON", "MONEY", "SERVE", "APPEAR", "ROAD", "MAP", "RAIN", "RULE", "GOVERN", "PULL", "COLD", "NOTICE", "VOICE", "UNIT", "POWER", "TOWN", "FINE", "CERTAIN", "FLY", "FALL", "LEAD", "CRY", "DARK", "MACHINE", "NOTE", "WAIT", "PLAN", "FIGURE", "STAR", "BOX", "NOUN", "FIELD", "REST", "CORRECT", "ABLE", "POUND", "DONE", "BEAUTY", "DRIVE", "STOOD", "CONTAIN", "FRONT", "TEACH", "WEEK", "FINAL", "GAVE", "GREEN", "OH", "QUICK", "DEVELOP", "OCEAN", "WARM", "FREE", "MINUTE", "STRONG", "SPECIAL", "MIND", "BEHIND", "CLEAR", "TAIL", "PRODUCE", "FACT", "STREET", "INCH", "MULTIPLY", "NOTHING", "COURSE", "STAY", "WHEEL", "FULL", "FORCE", "BLUE", "OBJECT", "DECIDE", "SURFACE", "DEEP", "MOON", "ISLAND", "FOOT", "SYSTEM", "BUSY", "TEST", "RECORD", "BOAT", "COMMON", "GOLD", "POSSIBLE", "PLANE", "STEAD", "DRY", "WONDER", "LAUGH", "THOUSAND", "AGO", "RAN", "CHECK", "GAME", "SHAPE", "EQUATE", "HOT", "MISS", "BROUGHT", "HEAT", "SNOW", "TIRE", "BRING", "YES", "DISTANT", "FILL", "EAST", "PAINT", "LANGUAGE", "AMONG", "GRAND", "BALL", "YET", "WAVE", "DROP", "HEART", "AM", "PRESENT", "HEAVY", "DANCE", "ENGINE", "POSITION", "ARM", "WIDE", "SAIL", "MATERIAL", "SIZE", "VARY", "SETTLE", "SPEAK", "WEIGHT", "GENERAL", "ICE", "MATTER", "CIRCLE", "PAIR", "INCLUDE", "DIVIDE", "SYLLABLE", "FELT", "PERHAPS", "PICK", "SUDDEN", "COUNT", "SQUARE", "REASON", "LENGTH", "REPRESENT", "ART", "SUBJECT", "REGION", "ENERGY", "HUNT", "PROBABLE", "BED", "BROTHER", "EGG", "RIDE", "CELL", "BELIEVE", "FRACTION", "FOREST", "SIT", "RACE", "WINDOW", "STORE", "SUMMER", "TRAIN", "SLEEP", "PROVE", "LONE", "LEG", "EXERCISE", "WALL", "CATCH", "MOUNT", "WISH", "SKY", "BOARD", "JOY", "WINTER", "SAT", "WRITTEN", "WILD", "INSTRUMENT", "KEPT", "GLASS", "GRASS", "COW", "JOB", "EDGE", "SIGN", "VISIT", "PAST", "SOFT", "FUN", "BRIGHT", "GAS", "WEATHER", "MONTH", "MILLION", "BEAR", "FINISH", "HAPPY", "HOPE", "FLOWER", "CLOTHE", "STRANGE", "GONE", "JUMP", "BABY", "EIGHT", "VILLAGE", "MEET", "ROOT", "BUY", "RAISE", "SOLVE", "METAL", "WHETHER", "PUSH", "SEVEN", "PARAGRAPH", "THIRD", "SHALL", "HELD", "HAIR", "DESCRIBE", "COOK", "FLOOR", "EITHER", "RESULT", "BURN", "HILL", "SAFE", "CAT", "CENTURY", "CONSIDER", "TYPE", "LAW", "BIT", "COAST", "COPY", "PHRASE", "SILENT", "TALL", "SAND", "SOIL", "ROLL", "TEMPERATURE", "FINGER", "INDUSTRY", "VALUE", "FIGHT", "LIE", "BEAT", "EXCITE", "NATURAL", "VIEW", "SENSE", "EAR", "ELSE", "QUITE", "BROKE", "CASE", "MIDDLE", "KILL", "SON", "LAKE", "MOMENT", "SCALE", "LOUD", "SPRING", "OBSERVE", "CHILD", "STRAIGHT", "CONSONANT", "NATION", "DICTIONARY", "MILK", "SPEED", "METHOD", "ORGAN", "PAY", "AGE", "SECTION", "DRESS", "CLOUD", "SURPRISE", "QUIET", "STONE", "TINY", "CLIMB", "COOL", "DESIGN", "POOR", "LOT", "EXPERIMENT", "BOTTOM", "KEY", "IRON", "SINGLE", "STICK", "FLAT", "TWENTY", "SKIN", "SMILE", "CREASE", "HOLE", "TRADE", "MELODY", "TRIP", "OFFICE", "RECEIVE", "ROW", "MOUTH", "EXACT", "SYMBOL", "DIE", "LEAST", "TROUBLE", "SHOUT", "EXCEPT", "WROTE", "SEED", "TONE", "JOIN", "SUGGEST", "CLEAN", "BREAK", "LADY", "YARD", "RISE", "BAD", "BLOW", "OIL", "BLOOD", "TOUCH", "GREW", "CENT", "MIX", "TEAM", "WIRE", "COST", "LOST", "BROWN", "WEAR", "GARDEN", "EQUAL", "SENT", "CHOOSE", "FELL", "FIT", "FLOW", "FAIR", "BANK", "COLLECT", "SAVE", "CONTROL", "DECIMAL", "GENTLE", "WOMAN", "CAPTAIN", "PRACTICE", "SEPARATE", "DIFFICULT", "DOCTOR", "PLEASE", "PROTECT", "NOON", "WHOSE", "LOCATE", "RING", "CHARACTER", "INSECT", "CAUGHT", "PERIOD", "INDICATE", "RADIO", "SPOKE", "ATOM", "HUMAN", "HISTORY", "EFFECT", "ELECTRIC", "EXPECT", "CROP", "MODERN", "ELEMENT", "HIT", "STUDENT", "CORNER", "PARTY", "SUPPLY", "BONE", "RAIL", "IMAGINE", "PROVIDE", "AGREE", "THUS", "CAPITAL", "WON'T", "CHAIR", "DANGER", "FRUIT", "RICH", "THICK", "SOLDIER", "PROCESS", "OPERATE", "GUESS", "NECESSARY", "SHARP", "WING", "CREATE", "NEIGHBOR", "WASH", "BAT", "RATHER", "CROWD", "CORN", "COMPARE", "POEM", "STRING", "BELL", "DEPEND", "MEAT", "RUB", "TUBE", "FAMOUS", "DOLLAR", "STREAM", "FEAR", "SIGHT", "THIN", "TRIANGLE", "PLANET", "HURRY", "CHIEF", "COLONY", "CLOCK", "MINE", "TIE", "ENTER", "MAJOR", "FRESH", "SEARCH", "SEND", "YELLOW", "GUN", "ALLOW", "PRINT", "DEAD", "SPOT", "DESERT", "SUIT", "CURRENT", "LIFT", "ROSE", "CONTINUE", "BLOCK", "CHART", "HAT", "SELL", "SUCCESS", "COMPANY", "SUBTRACT", "EVENT", "PARTICULAR", "DEAL", "SWIM", "TERM", "OPPOSITE", "WIFE", "SHOE", "SHOULDER", "SPREAD", "ARRANGE", "CAMP", "INVENT", "COTTON", "BORN", "DETERMINE", "QUART", "NINE", "TRUCK", "NOISE", "LEVEL", "CHANCE", "GATHER", "SHOP", "STRETCH", "THROW", "SHINE", "PROPERTY", "COLUMN", "MOLECULE", "SELECT", "WRONG", "GRAY", "REPEAT", "REQUIRE", "BROAD", "PREPARE", "SALT", "NOSE", "PLURAL", "ANGER", "CLAIM", "CONTINENT", "OXYGEN", "SUGAR", "DEATH", "PRETTY", "SKILL", "WOMEN", "SEASON", "SOLUTION", "MAGNET", "SILVER", "THANK", "BRANCH", "MATCH", "SUFFIX", "ESPECIALLY", "FIG", "AFRAID", "HUGE", "SISTER", "STEEL", "DISCUSS", "FORWARD", "SIMILAR", "GUIDE", "EXPERIENCE", "SCORE", "APPLE", "BOUGHT", "LED", "PITCH", "COAT", "MASS", "CARD", "BAND", "ROPE", "SLIP", "WIN", "DREAM", "EVENING", "CONDITION", "FEED", "TOOL", "TOTAL", "BASIC", "SMELL", "VALLEY", "NOR", "DOUBLE", "SEAT", "ARRIVE", "MASTER", "TRACK", "PARENT", "SHORE", "DIVISION", "SHEET", "SUBSTANCE", "FAVOR", "CONNECT", "POST", "SPEND", "CHORD", "FAT", "GLAD", "ORIGINAL", "SHARE", "STATION", "DAD", "BREAD", "CHARGE", "PROPER", "BAR", "OFFER", "SEGMENT", "SLAVE", "DUCK", "INSTANT", "MARKET", "DEGREE", "POPULATE", "CHICK", "DEAR", "ENEMY", "REPLY", "DRINK", "OCCUR", "SUPPORT", "SPEECH", "NATURE", "RANGE", "STEAM", "MOTION", "PATH", "LIQUID", "LOG", "MEANT", "QUOTIENT", "TEETH", "SHELL", "NECK", "DIGEST"
]

# Page 59 Text (Running Key)
PAGE_59_TEXT = "AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETRUETESTTHEKNOWLEDGEFINDYOURTRUTHEXPERIENCEYOURDEATHDONOTEDITORCHANGETHISBOOKORTHEMESSAGECONTAINEDWITHINEITHERTHEWORDSORTHEIRNUMBERSFORALLISSACRED"

# --- FUNCTIONS ---

def get_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    indices = [RUNE_MAP[c] for c in runes if c in RUNE_MAP]
    return indices

def runes_to_string(indices):
    # Convert list of rune indices to English string (expanding bigrams)
    res = []
    for x in indices:
        txt = RUNE_TO_TEXT_DECODE.get(x, '')
        res.append(txt)
    return "".join(res)

def score_text(text):
    # Count trigrams
    score = 0
    l = len(text)
    if l < 3: return 0
    
    for i in range(l - 2):
        tri = text[i:i+3]
        if tri in TRIGRAMS:
            score += TRIGRAMS[tri]
    
    return score

def decrypt(ciphertext_indices, key_indices):
    # Vigenere Decrypt: (Cipher - Key) % 29
    # Note: 29 is rune alphabet size
    dec = []
    k_len = len(key_indices)
    for i, c in enumerate(ciphertext_indices):
        k = key_indices[i % k_len]
        p = (c - k) % 29
        dec.append(p)
    return dec

def worker_task(args):
    # Unpack
    ciphertext_indices, keys_text_list = args
    
    best_loc_score = -1
    best_loc_key = None
    best_loc_txt = ""
    
    for key_text in keys_text_list:
        # Convert key to indices
        k_ind = [RUNE_MAP[c] for c in key_text if c in RUNE_MAP]
        # Or if key is passed as English text, we need to convert it?
        # Assuming keys supplied are English words that we map back to Runes?
        # But we don't know the english-to-rune map perfectly (multiple runes map to letters?)
        # Let's assume the key is supplied as Runes or we map carefully.
        # Actually, for this brute force, let's assume keys are from the WORD LIST
        # and we map English -> Runes using a simple inverted map (lossy) or standard map.
        
        # Simplified English->Rune for key generation:
        # F->0, U->1, TH->2 ...
        pass
    
    return None

# --- REVISED WORKER ---
# Needs to be top level for pickling
TEXT_TO_RUNE_SIMPLE = {
    'F':0, 'U':1, 'TH':2, 'O':3, 'R':4, 'C':5, 'G':6, 'W':7,
    'H':8, 'N':9, 'I':10, 'J':11, 'EO':12, 'P':13, 'X':14, 'S':15,
    'T':16, 'B':17, 'E':18, 'M':19, 'L':20, 'NG':21, 'OE':22, 'D':23,
    'A':24, 'AE':25, 'Y':26, 'IA':27, 'EA':28,
    'K': 5, 'Q': 5, 'V': 1, 'Z': 5 # Rough mappings
}

def english_to_rune_indices(word):
    # Greedy parse
    word = word.upper()
    indices = []
    i = 0
    while i < len(word):
        # Check 2 chars
        if i < len(word)-1:
            two = word[i:i+2]
            if two in TEXT_TO_RUNE_SIMPLE:
                indices.append(TEXT_TO_RUNE_SIMPLE[two])
                i += 2
                continue
        # Check 1 char
        one = word[i]
        if one in TEXT_TO_RUNE_SIMPLE:
            indices.append(TEXT_TO_RUNE_SIMPLE[one])
            i+=1
        else:
            # Skip unknown or map to F
            i+=1
    return indices

def check_keys(args):
    cipher_indices, key_strings = args
    results = []
    
    for k_str in key_strings:
        k_ind = english_to_rune_indices(k_str)  
        if not k_ind: continue
        
        p_ind = decrypt(cipher_indices, k_ind)
        p_txt = runes_to_string(p_ind)
        sc = score_text(p_txt)
        
        if sc > 10: # Threshold to report
            results.append((k_str, sc, p_txt[:40]))
            
    return results

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python crack_parallel.py <page_num>")
        return
        
    pg = sys.argv[1]
    print(f"Loading Page {pg}...")
    try:
        cipher = get_runes(pg)
    except Exception as e:
        print(f"Error loading page: {e}")
        return
        
    print(f"Cipher length: {len(cipher)} runes.")
    
    # Generate Keys
    # 1. Page 59 Text (Running Key)
    # Note: We must try shifts of this text as well.
    keys = [PAGE_59_TEXT, PAGE_59_TEXT[:30], PAGE_59_TEXT[:50]]
    
    # 2. Large Dictionary
    keys.extend(LARGE_DICT)
    
    # 3. Pairs of LARGE_DICT would be too big (1300*1300 = 1.6M). 
    # Let's try pairs of COMMON_WORDS (Cicada specific)
    for a, b in itertools.permutations(COMMON_WORDS, 2):
        keys.append(a + b)
        
    print(f"Generated {len(keys)} keys to test.")
    
    # Chunking
    num_cpus = os.cpu_count() or 4
    chunk_size = len(keys) // num_cpus + 1
    chunks = [keys[i:i + chunk_size] for i in range(0, len(keys), chunk_size)]
    
    args = [(cipher, chunk) for chunk in chunks]
    
    print(f"Starting parallel processing on {num_cpus} CPUs...")
    
    start_time = time.time()
    with multiprocessing.Pool(processes=num_cpus) as pool:
        all_results = pool.map(check_keys, args)
        
    # Flatten
    flat_results = []
    for r in all_results:
        flat_results.extend(r)
        
    # Sort
    flat_results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Done in {time.time() - start_time:.2f}s")
    print("\n--- TOP RESULTS ---")
    for k, s, t in flat_results[:20]:
        print(f"KEY: {k:<20} | SCORE: {s:<4} | DECRYPT: {t}")

if __name__ == "__main__":
    main()

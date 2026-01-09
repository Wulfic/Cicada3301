
import os
from collections import Counter

RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28, 'ᛂ': 11
}

NUM_TO_RUNETEXT = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# Condensed word list for brevity in this script block
COMMON_WORDS = [
    "THE", "OF", "TO", "AND", "A", "IN", "IS", "IT", "YOU", "THAT", "HE", "WAS", "FOR", "ON", "ARE", "WITH", "AS", "I", "HIS", "THEY", "BE", "AT", "ONE", "HAVE", "THIS", "FROM", "OR", "HAD", "BY", "NOT", "WORD", "BUT", "WHAT", "SOME", "WE", "CAN", "OUT", "OTHER", "WERE", "ALL", "THERE", "WHEN", "UP", "USE", "YOUR", "HOW", "SAID", "AN", "EACH", "SHE", "WHICH", "DO", "THEIR", "TIME", "IF", "WILL", "WAY", "ABOUT", "MANY", "THEN", "THEM", "WRITE", "WOULD", "LIKE", "SO", "THESE", "HER", "LONG", "MAKE", "THING", "SEE", "HIM", "TWO", "HAS", "LOOK", "MORE", "DAY", "COULD", "GO", "COME", "DID", "NUMBER", "SOUND", "NO", "MOST", "PEOPLE", "MY", "OVER", "KNOW", "WATER", "THAN", "CALL", "FIRST", "WHO", "MAY", "DOWN", "SIDE", "BEEN", "NOW", "FIND", "ANY", "NEW", "WORK", "PART", "TAKE", "GET", "PLACE", "MADE", "LIVE", "WHERE", "AFTER", "BACK", "LITTLE", "ONLY", "ROUND", "MAN", "YEAR", "CAME", "SHOW", "EVERY", "GOOD", "ME", "GIVE", "OUR", "UNDER", "NAME", "VERY", "THROUGH", "JUST", "FORM", "SENTENCE", "GREAT", "THINK", "SAY", "HELP", "LOW", "LINE", "DIFFER", "TURN", "CAUSE", "MUCH", "MEAN", "BEFORE", "MOVE", "RIGHT", "BOY", "OLD", "TOO", "SAME", "TELL", "DOES", "SET", "THREE", "WANT", "AIR", "WELL", "ALSO", "PLAY", "SMALL", "END", "PUT", "HOME", "READ", "HAND", "PORT", "LARGE", "SPELL", "ADD", "EVEN", "LAND", "HERE", "MUST", "BIG", "HIGH", "SUCH", "FOLLOW", "ACT", "WHY", "ASK", "MEN", "CHANGE", "WENT", "LIGHT", "KIND", "OFF", "NEED", "HOUSE", "PICTURE", "TRY", "US", "AGAIN", "ANIMAL", "POINT", "MOTHER", "WORLD", "NEAR", "BUILD", "SELF", "EARTH", "FATHER", "HEAD", "STAND", "OWN", "PAGE", "SHOULD", "COUNTRY", "FOUND", "ANSWER", "SCHOOL", "GROW", "STUDY", "STILL", "LEARN", "PLANT", "COVER", "FOOD", "SUN", "FOUR", "BETWEEN", "STATE", "KEEP", "EYE", "NEVER", "LAST", "LET", "THOUGHT", "CITY", "TREE", "CROSS", "FARM", "HARD", "START", "MIGHT", "STORY", "SAW", "FAR", "SEA", "DRAW", "LEFT", "LATE", "RUN", "DON'T", "WHILE", "PRESS", "CLOSE", "NIGHT", "REAL", "LIFE", "FEW", "NORTH", "OPEN", "SEEM", "TOGETHER", "NEXT", "WHITE", "CHILDREN", "BEGIN", "GOT", "WALK", "EXAMPLE", "EASE", "PAPER", "GROUP", "ALWAYS", "MUSIC", "THOSE", "BOTH", "MARK", "OFTEN", "LETTER", "UNTIL", "MILE", "RIVER", "CAR", "FEET", "CARE", "SECOND", "BOOK", "CARRY", "TOOK", "SCIENCE", "EAT", "ROOM", "FRIEND", "BEGAN", "IDEA", "FISH", "MOUNTAIN", "STOP", "ONCE", "BASE", "HEAR", "HORSE", "CUT", "SURE", "WATCH", "COLOR", "FACE", "WOOD", "MAIN", "ENOUGH", "PLAIN", "GIRL", "USUAL", "YOUNG", "READY", "ABOVE", "EVER", "RED", "LIST", "THOUGH", "FEEL", "TALK", "BIRD", "SOON", "BODY", "DOG", "FAMILY", "DIRECT", "POSE", "LEAVE", "SONG", "MEASURE", "DOOR", "PRODUCT", "BLACK", "SHORT", "NUMERAL", "CLASS", "WIND", "QUESTION", "HAPPEN", "COMPLETE", "SHIP", "AREA", "HALF", "ROCK", "ORDER", "FIRE", "SOUTH", "PROBLEM", "PIECE", "TOLD", "KNEW", "PASS", "SINCE", "TOP", "WHOLE", "KING", "SPACE", "HEARD", "BEST", "HOUR", "BETTER", "TRUE", "DURING", "HUNDRED", "FIVE", "REMEMBER", "STEP", "EARLY", "HOLD", "WEST", "GROUND", "INTEREST", "REACH", "FAST", "VERB", "SING", "LISTEN", "SIX", "TABLE", "TRAVEL", "LESS", "MORNING", "TEN", "SIMPLE", "SEVERAL", "VOWEL", "TOWARD", "WAR", "LAY", "AGAINST", "PATTERN", "SLOW", "CENTER", "LOVE", "PERSON", "MONEY", "SERVE", "APPEAR", "ROAD", "MAP", "RAIN", "RULE", "GOVERN", "PULL", "COLD", "NOTICE", "VOICE", "UNIT", "POWER", "TOWN", "FINE", "CERTAIN", "FLY", "FALL", "LEAD", "CRY", "DARK", "MACHINE", "NOTE", "WAIT", "PLAN", "FIGURE", "STAR", "BOX", "NOUN", "FIELD", "REST", "CORRECT", "ABLE", "POUND", "DONE", "BEAUTY", "DRIVE", "STOOD", "CONTAIN", "FRONT", "TEACH", "WEEK", "FINAL", "GAVE", "GREEN", "OH", "QUICK", "DEVELOP", "OCEAN", "WARM", "FREE", "MINUTE", "STRONG", "SPECIAL", "MIND", "BEHIND", "CLEAR", "TAIL", "PRODUCE", "FACT", "STREET", "INCH", "MULTIPLY", "NOTHING", "COURSE", "STAY", "WHEEL", "FULL", "FORCE", "BLUE", "OBJECT", "DECIDE", "SURFACE", "DEEP", "MOON", "ISLAND", "FOOT", "SYSTEM", "BUSY", "TEST", "RECORD", "BOAT", "COMMON", "GOLD", "POSSIBLE", "PLANE", "STEAD", "DRY", "WONDER", "LAUGH", "THOUSAND", "AGO", "RAN", "CHECK", "GAME", "SHAPE", "EQUATE", "HOT", "MISS", "BROUGHT", "HEAT", "SNOW", "TIRE", "BRING", "YES", "DISTANT", "FILL", "EAST", "PAINT", "LANGUAGE", "AMONG", "GRAND", "BALL", "YET", "WAVE", "DROP", "HEART", "AM", "PRESENT", "HEAVY", "DANCE", "ENGINE", "POSITION", "ARM", "WIDE", "SAIL", "MATERIAL", "SIZE", "VARY", "SETTLE", "SPEAK", "WEIGHT", "GENERAL", "ICE", "MATTER", "CIRCLE", "PAIR", "INCLUDE", "DIVIDE", "SYLLABLE", "FELT", "PERHAPS", "PICK", "SUDDEN", "COUNT", "SQUARE", "REASON", "LENGTH", "REPRESENT", "ART", "SUBJECT", "REGION", "ENERGY", "HUNT", "PROBABLE", "BED", "BROTHER", "EGG", "RIDE", "CELL", "BELIEVE", "FRACTION", "FOREST", "SIT", "RACE", "WINDOW", "STORE", "SUMMER", "TRAIN", "SLEEP", "PROVE", "LONE", "LEG", "EXERCISE", "WALL", "CATCH", "MOUNT", "WISH", "SKY", "BOARD", "JOY", "WINTER", "SAT", "WRITTEN", "WILD", "INSTRUMENT", "KEPT", "GLASS", "GRASS", "COW", "JOB", "EDGE", "SIGN", "VISIT", "PAST", "SOFT", "FUN", "BRIGHT", "GAS", "WEATHER", "MONTH", "MILLION", "BEAR", "FINISH", "HAPPY", "HOPE", "FLOWER", "CLOTHE", "STRANGE", "GONE", "JUMP", "BABY", "EIGHT", "VILLAGE", "MEET", "ROOT", "BUY", "RAISE", "SOLVE", "METAL", "WHETHER", "PUSH", "SEVEN", "PARAGRAPH", "THIRD", "SHALL", "HELD", "HAIR", "DESCRIBE", "COOK", "FLOOR", "EITHER", "RESULT", "BURN", "HILL", "SAFE", "CAT", "CENTURY", "CONSIDER", "TYPE", "LAW", "BIT", "COAST", "COPY", "PHRASE", "SILENT", "TALL", "SAND", "SOIL", "ROLL", "TEMPERATURE", "FINGER", "INDUSTRY", "VALUE", "FIGHT", "LIE", "BEAT", "EXCITE", "NATURAL", "VIEW", "SENSE", "EAR", "ELSE", "QUITE", "BROKE", "CASE", "MIDDLE", "KILL", "SON", "LAKE", "MOMENT", "SCALE", "LOUD", "SPRING", "OBSERVE", "CHILD", "STRAIGHT", "CONSONANT", "NATION", "DICTIONARY", "MILK", "SPEED", "METHOD", "ORGAN", "PAY", "AGE", "SECTION", "DRESS", "CLOUD", "SURPRISE", "QUIET", "STONE", "TINY", "CLIMB", "COOL", "DESIGN", "POOR", "LOT", "EXPERIMENT", "BOTTOM", "KEY", "IRON", "SINGLE", "STICK", "FLAT", "TWENTY", "SKIN", "SMILE", "CREASE", "HOLE", "TRADE", "MELODY", "TRIP", "OFFICE", "RECEIVE", "ROW", "MOUTH", "EXACT", "SYMBOL", "DIE", "LEAST", "TROUBLE", "SHOUT", "EXCEPT", "WROTE", "SEED", "TONE", "JOIN", "SUGGEST", "CLEAN", "BREAK", "LADY", "YARD", "RISE", "BAD", "BLOW", "OIL", "BLOOD", "TOUCH", "GREW", "CENT", "MIX", "TEAM", "WIRE", "COST", "LOST", "BROWN", "WEAR", "GARDEN", "EQUAL", "SENT", "CHOOSE", "FELL", "FIT", "FLOW", "FAIR", "BANK", "COLLECT", "SAVE", "CONTROL", "DECIMAL", "GENTLE", "WOMAN", "CAPTAIN", "PRACTICE", "SEPARATE", "DIFFICULT", "DOCTOR", "PLEASE", "PROTECT", "NOON", "WHOSE", "LOCATE", "RING", "CHARACTER", "INSECT", "CAUGHT", "PERIOD", "INDICATE", "RADIO", "SPOKE", "ATOM", "HUMAN", "HISTORY", "EFFECT", "ELECTRIC", "EXPECT", "CROP", "MODERN", "ELEMENT", "HIT", "STUDENT", "CORNER", "PARTY", "SUPPLY", "BONE", "RAIL", "IMAGINE", "PROVIDE", "AGREE", "THUS", "CAPITAL", "WON'T", "CHAIR", "DANGER", "FRUIT", "RICH", "THICK", "SOLDIER", "PROCESS", "OPERATE", "GUESS", "NECESSARY", "SHARP", "WING", "CREATE", "NEIGHBOR", "WASH", "BAT", "RATHER", "CROWD", "CORN", "COMPARE", "POEM", "STRING", "BELL", "DEPEND", "MEAT", "RUB", "TUBE", "FAMOUS", "DOLLAR", "STREAM", "FEAR", "SIGHT", "THIN", "TRIANGLE", "PLANET", "HURRY", "CHIEF", "COLONY", "CLOCK", "MINE", "TIE", "ENTER", "MAJOR", "FRESH", "SEARCH", "SEND", "YELLOW", "GUN", "ALLOW", "PRINT", "DEAD", "SPOT", "DESERT", "SUIT", "CURRENT", "LIFT", "ROSE", "CONTINUE", "BLOCK", "CHART", "HAT", "SELL", "SUCCESS", "COMPANY", "SUBTRACT", "EVENT", "PARTICULAR", "DEAL", "SWIM", "TERM", "OPPOSITE", "WIFE", "SHOE", "SHOULDER", "SPREAD", "ARRANGE", "CAMP", "INVENT", "COTTON", "BORN", "DETERMINE", "QUART", "NINE", "TRUCK", "NOISE", "LEVEL", "CHANCE", "GATHER", "SHOP", "STRETCH", "THROW", "SHINE", "PROPERTY", "COLUMN", "MOLECULE", "SELECT", "WRONG", "GRAY", "REPEAT", "REQUIRE", "BROAD", "PREPARE", "SALT", "NOSE", "PLURAL", "ANGER", "CLAIM", "CONTINENT", "OXYGEN", "SUGAR", "DEATH", "PRETTY", "SKILL", "WOMEN", "SEASON", "SOLUTION", "MAGNET", "SILVER", "THANK", "BRANCH", "MATCH", "SUFFIX", "ESPECIALLY", "FIG", "AFRAID", "HUGE", "SISTER", "STEEL", "DISCUSS", "FORWARD", "SIMILAR", "GUIDE", "EXPERIENCE", "SCORE", "APPLE", "BOUGHT", "LED", "PITCH", "COAT", "MASS", "CARD", "BAND", "ROPE", "SLIP", "WIN", "DREAM", "EVENING", "CONDITION", "FEED", "TOOL", "TOTAL", "BASIC", "SMELL", "VALLEY", "NOR", "DOUBLE", "SEAT", "ARRIVE", "MASTER", "TRACK", "PARENT", "SHORE", "DIVISION", "SHEET", "SUBSTANCE", "FAVOR", "CONNECT", "POST", "SPEND", "CHORD", "FAT", "GLAD", "ORIGINAL", "SHARE", "STATION", "DAD", "BREAD", "CHARGE", "PROPER", "BAR", "OFFER", "SEGMENT", "SLAVE", "DUCK", "INSTANT", "MARKET", "DEGREE", "POPULATE", "CHICK", "DEAR", "ENEMY", "REPLY", "DRINK", "OCCUR", "SUPPORT", "SPEECH", "NATURE", "RANGE", "STEAM", "MOTION", "PATH", "LIQUID", "LOG", "MEANT", "QUOTIENT", "TEETH", "SHELL", "NECK", "DIGEST", "LIBER", "PRIMUS", "CICADA", "EMERGENCE", "INSTAR", "CIRCUMFERENCE", "DIVINITY", "PROGRAM", "WARNING", "INTELLIGENCE", "WISDOM", "COMMAND", "PRIZE", "ACHIEVE", "MESSAGE", "SYSTEM", "CIPHER", "CODE", "RUNES", "CHAPTER", "INTUS", "PRESERVE", "CONSUME", "ADHERE", "INSTRUCTION", "PRIMES", "TOTIENT", "NUMBERS", "SACRED", "PILGRIM", "JOURNEY", "AUTHOR", "SECRET", "HIDDEN", "TRUTH", "BELIEF", "SYSTEMS", "LOSS", "TRANSMISSION", "INCOMING", "WELCOME", "GOODBYE", "HELLO", "BEWARE", "KNOWLEDGE", "UNDERSTANDING", "BEGINNING", "PRESERVATION", "CONSUMPTION", "ADHERENCE", "DIFFICULTY", "HARDSHIP", "ORDEAL", "TESTING", "FILTER", "SCREEN", "PASSAGE", "GATE", "OPENING", "CLOSING", "VOID", "ABYSS", "LIGHT", "DARKNESS", "SHADOW", "ECLIPSE", "OSCILLATION", "WAVELENGTH", "FREQUENCY", "SIGNAL", "DECRYPTION", "ENCRYPTION", "KEY", "LOCK", "DOOR", "WAY", "PATH", "ROAD", "STREET", "AVENUE", "LANE", "PASSAGEWAY", "CORRIDOR", "HALL", "ROOM", "CHAMBER", "SANCTUARY", "TEMPLE", "SHRINE", "ALTAR", "SACRIFICE", "OFFERING", "GIFT", "REWARD", "PENALTY", "PUNISHMENT", "CONSEQUENCE", "RESULT", "OUTCOME", "EFFECT", "CAUSE", "REASON", "PURPOSE", "MEANING", "SIGNIFICANCE", "IMPORTANCE", "VALUE", "WORTH", "PRICE", "COST", "EXPENSE", "PAYMENT", "CHARGE", "FEE", "TAX", "TOLL", "DUES", "DEBT", "OWE", "OWN", "POSSESS", "HAVE", "HOLD", "KEEP", "MAINTAIN", "SUSTAIN", "SUPPORT", "UPHOLD", "DEFEND", "PROTECT", "GUARD", "WATCH", "OBSERVE", "SEE", "LOOK", "VIEW", "SIGHT", "VISION", "IMAGE", "PICTURE", "SCENE", "PANORAMA", "LANDSCAPE", "VISTA", "PROSPECT", "OUTLOOK", "PERSPECTIVE", "VIEWPOINT", "SANDPOINT", "ANGLE", "ASPECT", "PHASE", "STAGE", "STATE", "CONDITION", "SITUATION", "CIRCUMSTANCE", "POSITION", "STATUS", "RANK", "GRADE", "LEVEL", "DEGREE", "EXTENT", "SCOPE", "RANGE", "LIMIT", "BOUND", "BOUNDARY", "BORDER", "EDGE", "MARGIN", "FRINGE", "VERGE", "BRINK", "THRESHOLD", "DOORSTEP", "ENTRANCE", "ENTRY", "GATEWAY", "PORTAL", "ACCESS", "ADMISSION", "ADMITTANCE", "ENTRYWAY", "INGRESS", "INLET", "OPENING", "ORIFICE", "VENT", "EXIT", "EGRESS", "OUTLET", "WAY", "ROUTE", "COURSE", "PATH", "TRACK", "TRAIL", "TRACE", "PRINT", "MARK", "SIGN", "SYMBOL", "TOKEN", "EMBLEM", "BADGE", "INSIGNIA", "CREST", "SEAL", "STAMP", "BRAND", "LABEL", "TAG", "TICKET", "STUB", "COUPON", "VOUCHER", "PASS", "PERMIT", "LICENSE", "CERTIFICATE", "DIPLOMA", "DEGREE", "AWARD", "PRIZE", "TROPHY", "MEDAL", "RIBBON", "WREATH", "GARLAND", "CROWN", "DIADEM", "TIARA", "CORONET", "CHAPLET", "HEADBAND", "FILLET", "SNOOD", "HAIRNET", "NET", "WEB", "MESH", "LATTICE", "SCREEN", "SIEVE", "FILTER", "STRAINER", "SIFTER", "RIDDLE", "PUZZLE", "MYSTERY", "ENIGMA", "CONUNDRUM", "PROBLEM", "QUESTION", "ISSUE", "MATTER", "AFFAIR", "TOPIC", "SUBJECT", "THEME", "MOTIF", "TEXT", "SCRIPT", "LINES", "LYRICS", "WORDS", "VERSE", "POETRY", "POEM", "RHYME", "SONG", "BALLAD", "LAY", "ODE", "EPIC", "SAGA", "TALE", "STORY", "LEGEND", "MYTH", "FABLE", "PARABLE", "ALLEGORY", "APOLOGUE", "NARRATIVE", "ACCOUNT", "REPORT", "RECORD", "HISTORY", "CHRONICLE", "ANNAL", "ARCHIVE", "REGISTER", "ROLL", "LIST", "CATALOG", "INVENTORY", "INDEX", "TABLE", "CHART", "GRAPH", "DIAGRAM", "MAP", "PLAN", "PLAT", "PLOT", "SCHEME", "DESIGN", "PATTERN", "MODEL", "MOLD", "TEMPLATE"
]

def load_runes(pg):
    path = f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{pg}\\runes.txt"
    with open(path, 'r', encoding='utf-8') as f:
        runes = f.read()
    return runes

def get_pattern(text_or_indices):
    seen = {}
    res = []
    next_code = 0
    indices = []
    
    if isinstance(text_or_indices, str):
        # String case (Word)
        for c in text_or_indices:
            if c not in seen:
                seen[c] = next_code
                next_code += 1
            res.append(str(seen[c]))
    else:
        # Indices case
        for c in text_or_indices:
            if c not in seen:
                seen[c] = next_code
                next_code += 1
            res.append(str(seen[c]))
            
    return ".".join(res)

def main():
    runes = load_runes("59")
    # Clean and split
    text = runes.replace('\n', '•').replace(' ', '•')
    words_raw = [w for w in text.split('•') if w]

    # Pre-process dictionary patterns
    dict_patterns = {}
    for w in COMMON_WORDS:
        p = get_pattern(w)
        if p not in dict_patterns:
            dict_patterns[p] = []
        # Store as (Word, Length)
        dict_patterns[p].append(w)

    print(f"Loaded {len(COMMON_WORDS)} dict words.")
    
    print("\n--- MATCHING ---")
    
    # Priority words to output
    indices_of_interest = [0, 1, 2, 6, 20, 23, 24, 29, 32, 42]

    for i, w_rune in enumerate(words_raw):
        indices = [RUNE_MAP[c] for c in w_rune if c in RUNE_MAP]
        if not indices: continue
        
        pat = get_pattern(indices)
        word_len = len(indices)
        
        matches = [cand for cand in dict_patterns.get(pat, []) if len(cand) == word_len]
        
        rune_txt = "-".join([NUM_TO_RUNETEXT[x] for x in indices])
        
        if len(matches) > 0 and (len(matches) < 20 or i in indices_of_interest):
             print(f"Word {i} [{rune_txt}] ({word_len}): {matches[:10]}")

if __name__ == "__main__":
    main()

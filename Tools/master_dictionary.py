#!/usr/bin/env python3
"""
MASTER DICTIONARY FOR CICADA 3301 / LIBER PRIMUS DECRYPTION
============================================================

This module contains ALL relevant data for cryptanalysis:
- Gematria Primus alphabet (29 runes)
- Prime numbers, totient values, Fibonacci, Lucas sequences
- Known keys from solved pages
- Words extracted from Self-Reliance (Emerson)
- Words from solved page plaintexts
- Common English words and trigrams
- Cicada-specific terminology

Author: Wulfic
Date: January 2026
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from functools import lru_cache

# =============================================================================
# GEMATRIA PRIMUS ALPHABET (29 characters)
# =============================================================================

GEMATRIA = {
    'ᚠ': (0, 'F', 2),    'ᚢ': (1, 'U', 3),    'ᚦ': (2, 'TH', 5),
    'ᚩ': (3, 'O', 7),    'ᚱ': (4, 'R', 11),   'ᚳ': (5, 'C', 13),
    'ᚷ': (6, 'G', 17),   'ᚹ': (7, 'W', 19),   'ᚻ': (8, 'H', 23),
    'ᚾ': (9, 'N', 29),   'ᛁ': (10, 'I', 31),  'ᛂ': (11, 'J', 37),
    'ᛇ': (12, 'EO', 41), 'ᛈ': (13, 'P', 43),  'ᛉ': (14, 'X', 47),
    'ᛋ': (15, 'S', 53),  'ᛏ': (16, 'T', 59),  'ᛒ': (17, 'B', 61),
    'ᛖ': (18, 'E', 67),  'ᛗ': (19, 'M', 71),  'ᛚ': (20, 'L', 73),
    'ᛝ': (21, 'NG', 79), 'ᛟ': (22, 'OE', 83), 'ᛞ': (23, 'D', 89),
    'ᚪ': (24, 'A', 97),  'ᚫ': (25, 'AE', 101),'ᚣ': (26, 'Y', 103),
    'ᛡ': (27, 'IA', 107),'ᛠ': (28, 'EA', 109)
}

# Alternative J rune (sometimes seen)
GEMATRIA['ᛄ'] = (11, 'J', 37)

ALPHABET_SIZE = 29

# Rune to Index
RUNE_TO_INDEX: Dict[str, int] = {k: v[0] for k, v in GEMATRIA.items()}

# Index to Rune
INDEX_TO_RUNE: Dict[int, str] = {v[0]: k for k, v in GEMATRIA.items()}

# Index to Latin Letter(s)
INDEX_TO_LATIN: Dict[int, str] = {v[0]: v[1] for k, v in GEMATRIA.items()}

# Index to Prime Value
INDEX_TO_PRIME: Dict[int, int] = {v[0]: v[2] for k, v in GEMATRIA.items()}

# Latin to Index (for key conversion)
LATIN_TO_INDEX: Dict[str, int] = {}
for k, v in GEMATRIA.items():
    latin = v[1]
    idx = v[0]
    if latin not in LATIN_TO_INDEX:
        LATIN_TO_INDEX[latin] = idx
    # Handle single chars from digraphs too
    if len(latin) == 1:
        LATIN_TO_INDEX[latin] = idx

# Add single letter mappings for digraphs (for flexible key input)
LATIN_TO_INDEX['K'] = LATIN_TO_INDEX['C']  # K = C in Gematria Primus

# =============================================================================
# PRIME NUMBERS AND TOTIENT VALUES
# =============================================================================

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Generate all primes up to limit using Sieve of Eratosthenes."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# Generate primes up to 10000 (enough for most purposes)
PRIMES = sieve_of_eratosthenes(10000)
PRIME_SET = set(PRIMES)

# First 500 primes (commonly used)
FIRST_500_PRIMES = PRIMES[:500]

# Primes mod 29 (for direct use as key values)
PRIMES_MOD_29 = [p % ALPHABET_SIZE for p in PRIMES]

@lru_cache(maxsize=10000)
def totient(n: int) -> int:
    """Euler's totient function φ(n)."""
    if n == 1:
        return 1
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

# Precompute totients for first 1000 numbers
TOTIENTS = {i: totient(i) for i in range(1, 1001)}

# Totient of primes: φ(p) = p - 1
PRIME_TOTIENTS = [p - 1 for p in PRIMES]
PRIME_TOTIENTS_MOD_29 = [(p - 1) % ALPHABET_SIZE for p in PRIMES]

# =============================================================================
# FIBONACCI AND LUCAS SEQUENCES
# =============================================================================

def generate_fibonacci(n: int) -> List[int]:
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

def generate_lucas(n: int) -> List[int]:
    """Generate first n Lucas numbers."""
    if n <= 0:
        return []
    if n == 1:
        return [2]
    luc = [2, 1]
    for _ in range(2, n):
        luc.append(luc[-1] + luc[-2])
    return luc

FIBONACCI = generate_fibonacci(100)
LUCAS = generate_lucas(100)

FIBONACCI_MOD_29 = [f % ALPHABET_SIZE for f in FIBONACCI]
LUCAS_MOD_29 = [l % ALPHABET_SIZE for l in LUCAS]

# =============================================================================
# KNOWN KEYS FROM SOLVED PAGES
# =============================================================================

# Verified keys that successfully decoded pages
KNOWN_KEYS = {
    'DIVINITY': [23, 10, 28, 10, 29, 10, 16, 26],  # Pages 03, 04, 61
    'FIRFUMFERENFE': None,  # Pages 14, 15, 72 - Will compute
    'CONSUMPTION': None,  # Page 62
    'KOAN': None,  # Page 64
    'CICADA': None,  # Page 67
    'YAHEOOPYJ': None,  # Page 17
    'INSTAR': None,
    'INTUS': None,
    'CHAPTER': None,
    'SECTION': None,
    'PARABLE': None,
    'INSTRUCTION': None,
    'WARNING': None,
    'WELCOME': None,
    'PILGRIM': None,
    'JOURNEY': None,
    'SACRED': None,
    'WISDOM': None,
    'PRIMES': None,
    'TOTIENT': None,
    'CIRCUMFERENCE': None,
    'ENLIGHTENMENT': None,
    'PRESERVATION': None,
    'EMERGENCE': None,
    'INTERCONNECTEDNESS': None,
    'SELFRELIANCE': None,
    'COMMAND': None,
    'EMERSON': None,
    'DEEP': None,
    'WEB': None,
}

def text_to_key(text: str) -> List[int]:
    """Convert text to list of indices (key values)."""
    text = text.upper().replace(' ', '')
    result = []
    i = 0
    while i < len(text):
        # Try digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in LATIN_TO_INDEX:
                result.append(LATIN_TO_INDEX[digraph])
                i += 2
                continue
        # Single char
        char = text[i]
        if char in LATIN_TO_INDEX:
            result.append(LATIN_TO_INDEX[char])
        i += 1
    return result

# Compute all key indices
for key_name in KNOWN_KEYS:
    if KNOWN_KEYS[key_name] is None:
        KNOWN_KEYS[key_name] = text_to_key(key_name)

# =============================================================================
# CICADA-SPECIFIC TERMS
# =============================================================================

CICADA_TERMS = [
    # Core concepts
    "CICADA", "PRIMUS", "LIBER", "LIBERPRIMUS", "GEMATRIA", "RUNE", "RUNES",
    "INTUS", "INSTAR", "EMERGENCE", "DIVINITY", "TOTIENT", "PRIME", "PRIMES",
    "CIRCUMFERENCE", "ENLIGHTENMENT", "CONSCIOUSNESS", "PILGRIM", "JOURNEY",
    
    # Page titles and markers
    "CHAPTER", "SECTION", "PARABLE", "KOAN", "WARNING", "INSTRUCTION",
    "WELCOME", "WISDOM", "EPILOGUE", "END", "BEGINNING",
    
    # Philosophical terms
    "SACRED", "TRUTH", "KNOWLEDGE", "BELIEF", "EXPERIENCE", "REALITY",
    "ILLUSION", "SELF", "SOUL", "MIND", "SPIRIT", "BEING", "EXISTENCE",
    "NATURE", "UNIVERSE", "COSMOS", "INFINITY", "ETERNITY",
    
    # Actions from instructions
    "BELIEVE", "QUESTION", "SEEK", "FIND", "DISCOVER", "UNDERSTAND",
    "LEARN", "TEACH", "PRESERVE", "CONSUME", "CREATE", "DESTROY",
    
    # Deep web hints
    "DEEP", "WEB", "ONION", "TOR", "HIDDEN", "SECRET", "MYSTERY",
    "HASH", "PAGE", "PILGRIM", "DUTY",
    
    # Numbers as words
    "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
    "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "TWENTYNINE",
    
    # Latin phrases (transliterated)
    "CREDO", "VERITAS", "LUX", "FIAT", "VOX", "DEI", "DEUS",
    
    # 3301-specific
    "THREETHREEZEROONE", "THREEZERONEONE", "THREETHOUSANDTHREEHUNDREDONE",
]

CICADA_TERM_KEYS = {term: text_to_key(term) for term in CICADA_TERMS}

# =============================================================================
# SELF-RELIANCE EXTRACTION
# =============================================================================

def load_self_reliance() -> str:
    """Load Self-Reliance text if available."""
    paths = [
        Path(__file__).parent / "reference" / "research" / "Self-Reliance.txt",
        Path("c:/Users/tyler/Repos/Cicada3301/LiberPrimus/reference/research/Self-Reliance.txt"),
    ]
    for path in paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    return ""

SELF_RELIANCE_TEXT = load_self_reliance()

def extract_words_from_text(text: str) -> Set[str]:
    """Extract unique words from text, cleaned."""
    words = re.findall(r'[A-Za-z]+', text.upper())
    # Filter to reasonable length
    return {w for w in words if 2 <= len(w) <= 30}

SELF_RELIANCE_WORDS = extract_words_from_text(SELF_RELIANCE_TEXT)
SELF_RELIANCE_WORD_KEYS = {w: text_to_key(w) for w in SELF_RELIANCE_WORDS}

# Key phrases from Self-Reliance that might be used
SELF_RELIANCE_PHRASES = [
    "TRUST THYSELF",
    "ENVY IS IGNORANCE",
    "IMITATION IS SUICIDE",
    "NOTHING IS AT LAST SACRED",
    "WHOSO WOULD BE A MAN",
    "FOOLISH CONSISTENCY",
    "HOBGOBLIN OF LITTLE MINDS",
    "TO BE GREAT IS TO BE MISUNDERSTOOD",
    "SPEAK YOUR LATENT CONVICTION",
    "SHED CIRCUMFERENCES",
]

# =============================================================================
# SOLVED PAGE PLAINTEXTS (for running key analysis)
# =============================================================================

SOLVED_PLAINTEXTS = {
    1: "AWARNINGBELIEVENOTHINGFROMTHISBOOKEXCEPTWHATYOUKNOWTOBETRUETESTTHEKNOWLEDGEFINDYOURTRUTHEXPERIENCEYOURDEATHDONOTEDITORCHANGETHISBOOKORTHEMESSAGECONTAINEDWITHINEITHERTHEWORDSORTHEIRNUMBERSFORALLISSACRED",
    3: "WELCOMEPILGRIMTOTHEGREATJOURNEYTOWARDTHEENDOFALLTHINGSITISNOTANEASYTRIPBUTFORTHOSEWHOFINDTHEIRWAYHEREISANECESSARYONEALONGTHEWAYYOUWILLFINDANENDTOALLSTRUGGLEANDSUFFERINGYOURINNOCENCEYOURILLUSIONSYOURCERTAINTYANDYOURREALITYULTIMATELYYOUWILLDISCOVERANENDTOSELF",
    5: "SOMEWISDOMTHEPRIMESARESACREDTHETOTIENTFUNCTIONISSACREDALLDIVISIONSARENOTEQUALSOMEARETRUERANDTHESEARETHEDIVISIONSBETWEENZEROANDONE",
    9: "ANINSTRUCTIONDOFOURUNREASONABLETHINGSEACHDAY",
    55: "ANENDWITHINTHADEEPWEBTHEREEXISTSAPAGETHATHASESTOTHEIDYTWOFEUERYPILGRIMTOSEEKOUTTHISPAGE",
}

SOLVED_PLAINTEXT_WORDS = set()
for pt in SOLVED_PLAINTEXTS.values():
    SOLVED_PLAINTEXT_WORDS.update(extract_words_from_text(pt))

# =============================================================================
# COMMON ENGLISH WORDS
# =============================================================================

COMMON_ENGLISH_WORDS = [
    # Most common 500 English words
    "THE", "OF", "TO", "AND", "A", "IN", "IS", "IT", "YOU", "THAT", "HE", "WAS",
    "FOR", "ON", "ARE", "WITH", "AS", "I", "HIS", "THEY", "BE", "AT", "ONE",
    "HAVE", "THIS", "FROM", "OR", "HAD", "BY", "NOT", "WORD", "BUT", "WHAT",
    "SOME", "WE", "CAN", "OUT", "OTHER", "WERE", "ALL", "THERE", "WHEN", "UP",
    "USE", "YOUR", "HOW", "SAID", "AN", "EACH", "SHE", "WHICH", "DO", "THEIR",
    "TIME", "IF", "WILL", "WAY", "ABOUT", "MANY", "THEN", "THEM", "WRITE",
    "WOULD", "LIKE", "SO", "THESE", "HER", "LONG", "MAKE", "THING", "SEE",
    "HIM", "TWO", "HAS", "LOOK", "MORE", "DAY", "COULD", "GO", "COME", "DID",
    "NUMBER", "SOUND", "NO", "MOST", "PEOPLE", "MY", "OVER", "KNOW", "WATER",
    "THAN", "CALL", "FIRST", "WHO", "MAY", "DOWN", "SIDE", "BEEN", "NOW",
    "FIND", "ANY", "NEW", "WORK", "PART", "TAKE", "GET", "PLACE", "MADE",
    "LIVE", "WHERE", "AFTER", "BACK", "LITTLE", "ONLY", "ROUND", "MAN", "YEAR",
    "CAME", "SHOW", "EVERY", "GOOD", "ME", "GIVE", "OUR", "UNDER", "NAME",
    "VERY", "THROUGH", "JUST", "FORM", "SENTENCE", "GREAT", "THINK", "SAY",
    "HELP", "LOW", "LINE", "DIFFER", "TURN", "CAUSE", "MUCH", "MEAN", "BEFORE",
    "MOVE", "RIGHT", "BOY", "OLD", "TOO", "SAME", "TELL", "DOES", "SET",
    "THREE", "WANT", "AIR", "WELL", "ALSO", "PLAY", "SMALL", "END", "PUT",
    "HOME", "READ", "HAND", "PORT", "LARGE", "SPELL", "ADD", "EVEN", "LAND",
    "HERE", "MUST", "BIG", "HIGH", "SUCH", "FOLLOW", "ACT", "WHY", "ASK",
    "MEN", "CHANGE", "WENT", "LIGHT", "KIND", "OFF", "NEED", "HOUSE", "PICTURE",
    "TRY", "US", "AGAIN", "ANIMAL", "POINT", "MOTHER", "WORLD", "NEAR", "BUILD",
    "SELF", "EARTH", "FATHER", "HEAD", "STAND", "OWN", "PAGE", "SHOULD",
    "COUNTRY", "FOUND", "ANSWER", "SCHOOL", "GROW", "STUDY", "STILL", "LEARN",
    "PLANT", "COVER", "FOOD", "SUN", "FOUR", "BETWEEN", "STATE", "KEEP", "EYE",
    "NEVER", "LAST", "LET", "THOUGHT", "CITY", "TREE", "CROSS", "FARM", "HARD",
    "START", "MIGHT", "STORY", "SAW", "FAR", "SEA", "DRAW", "LEFT", "LATE",
    "RUN", "WHILE", "PRESS", "CLOSE", "NIGHT", "REAL", "LIFE", "FEW", "NORTH",
    "OPEN", "SEEM", "TOGETHER", "NEXT", "WHITE", "CHILDREN", "BEGIN", "GOT",
    "WALK", "EXAMPLE", "EASE", "PAPER", "GROUP", "ALWAYS", "MUSIC", "THOSE",
    "BOTH", "MARK", "OFTEN", "LETTER", "UNTIL", "MILE", "RIVER", "CAR", "FEET",
    "CARE", "SECOND", "BOOK", "CARRY", "TOOK", "SCIENCE", "EAT", "ROOM",
    "FRIEND", "BEGAN", "IDEA", "FISH", "MOUNTAIN", "STOP", "ONCE", "BASE",
    "HEAR", "HORSE", "CUT", "SURE", "WATCH", "COLOR", "FACE", "WOOD", "MAIN",
    # Additional philosophical/mystical terms
    "SPIRIT", "SOUL", "MIND", "BODY", "HEART", "LOVE", "TRUTH", "WISDOM",
    "KNOWLEDGE", "BELIEF", "FAITH", "HOPE", "FEAR", "DEATH", "LIFE", "LIGHT",
    "DARK", "DARKNESS", "SHADOW", "SECRET", "MYSTERY", "HIDDEN", "SACRED",
    "DIVINE", "GOD", "GODS", "HEAVEN", "HELL", "ANGEL", "DEMON", "SPIRIT",
]

COMMON_WORD_KEYS = {w: text_to_key(w) for w in COMMON_ENGLISH_WORDS}

# =============================================================================
# TRIGRAMS AND N-GRAMS FOR SCORING
# =============================================================================

# Top English trigrams with approximate frequency weights
TRIGRAMS = {
    'THE': 100, 'AND': 80, 'ING': 75, 'HER': 60, 'THA': 60, 'ERE': 50,
    'FOR': 50, 'ENT': 45, 'ION': 45, 'TER': 40, 'WAS': 40, 'YOU': 40,
    'ITH': 35, 'VER': 35, 'ALL': 35, 'WIT': 35, 'THI': 35, 'TIO': 35,
    'EVE': 30, 'OFT': 30, 'EST': 30, 'ATE': 30, 'HIS': 30, 'OUR': 30,
    'ERS': 28, 'INT': 28, 'TED': 28, 'ATI': 28, 'STA': 28, 'HAT': 28,
    'NOT': 25, 'BUT': 25, 'HAS': 25, 'REA': 25, 'OME': 25, 'COM': 25,
    'PRO': 22, 'WHO': 22, 'ONE': 22, 'OUT': 22, 'OWN': 22, 'MEN': 22,
    'CAN': 20, 'HAV': 20, 'WOR': 20, 'MAN': 20, 'ORT': 20, 'RES': 20,
    'NDE': 18, 'AVE': 18, 'NEW': 18, 'NOW': 18, 'OLD': 18, 'SEE': 18,
}

# Bigrams
BIGRAMS = {
    'TH': 50, 'HE': 45, 'IN': 40, 'ER': 38, 'AN': 36, 'RE': 35, 'ON': 34,
    'AT': 32, 'EN': 30, 'ND': 30, 'TI': 28, 'ES': 28, 'OR': 27, 'TE': 26,
    'OF': 25, 'ED': 25, 'IS': 24, 'IT': 24, 'AL': 23, 'AR': 22, 'ST': 22,
    'TO': 21, 'NT': 21, 'NG': 20, 'SE': 20, 'HA': 19, 'AS': 19, 'OU': 18,
    'IO': 18, 'LE': 17, 'VE': 17, 'CO': 16, 'ME': 16, 'DE': 15, 'HI': 15,
}

# Quadgrams for strong pattern matching
QUADGRAMS = {
    'TION': 100, 'THAT': 90, 'WITH': 85, 'THER': 80, 'THIS': 75, 'HAVE': 70,
    'FROM': 65, 'OULD': 60, 'IGHT': 55, 'HERE': 55, 'HING': 50, 'OULD': 50,
    'WHAT': 45, 'BEEN': 45, 'WERE': 40, 'THEY': 40, 'WILL': 40, 'YOUR': 38,
    'WHEN': 35, 'SOME': 35, 'MENT': 35, 'ABLE': 35, 'NESS': 32, 'INGS': 30,
    'JUST': 28, 'ONLY': 28, 'OVER': 28, 'SUCH': 28, 'ALSO': 25, 'BACK': 25,
    'KNOW': 25, 'TAKE': 25, 'COME': 25, 'MORE': 25, 'INTO': 22, 'YEAR': 22,
    'GOOD': 22, 'WELL': 22, 'MAKE': 22, 'CALL': 20, 'FIND': 20, 'LOOK': 20,
}

# =============================================================================
# SPECIAL NUMBER SEQUENCES
# =============================================================================

# 3301 related
NUMBER_3301 = 3301
NUMBER_3301_FACTORS = [1, 3301]  # 3301 is prime

# Key lengths from solved pages (many are prime)
KNOWN_KEY_LENGTHS = [7, 8, 9, 11, 13, 17, 29, 43, 53, 61, 71, 83, 89, 97]

# Prime key lengths to try
PRIME_KEY_LENGTHS = [p for p in PRIMES if p <= 200]

# Offset values to try (all possible for mod 29)
OFFSETS = list(range(ALPHABET_SIZE))

# =============================================================================
# COMBINED MASTER WORD LIST
# =============================================================================

def get_all_words() -> Set[str]:
    """Get combined set of all words from all sources."""
    all_words = set(CICADA_TERMS)
    all_words.update(COMMON_ENGLISH_WORDS)
    all_words.update(SELF_RELIANCE_WORDS)
    all_words.update(SOLVED_PLAINTEXT_WORDS)
    return all_words

def get_all_keys() -> Dict[str, List[int]]:
    """Get dictionary of all words mapped to their key indices."""
    all_keys = {}
    all_keys.update(CICADA_TERM_KEYS)
    all_keys.update(COMMON_WORD_KEYS)
    all_keys.update(SELF_RELIANCE_WORD_KEYS)
    all_keys.update(KNOWN_KEYS)
    return all_keys

ALL_WORDS = get_all_words()
ALL_KEYS = get_all_keys()

# =============================================================================
# UTILITY FUNCTIONS FOR KEY GENERATION
# =============================================================================

def generate_prime_sequence_key(length: int, start_prime_idx: int = 0, 
                                 use_totient: bool = False) -> List[int]:
    """Generate a key using sequential primes or their totients."""
    if use_totient:
        return [PRIME_TOTIENTS_MOD_29[start_prime_idx + i] for i in range(length)]
    else:
        return [PRIMES_MOD_29[start_prime_idx + i] for i in range(length)]

def generate_fibonacci_key(length: int, start_idx: int = 0) -> List[int]:
    """Generate a key using Fibonacci sequence."""
    return [FIBONACCI_MOD_29[start_idx + i] for i in range(length)]

def generate_lucas_key(length: int, start_idx: int = 0) -> List[int]:
    """Generate a key using Lucas sequence."""
    return [LUCAS_MOD_29[start_idx + i] for i in range(length)]

def generate_offset_variations(key: List[int], offsets: List[int] = None) -> List[Tuple[int, List[int]]]:
    """Generate all offset variations of a key."""
    if offsets is None:
        offsets = OFFSETS
    return [(o, [(k + o) % ALPHABET_SIZE for k in key]) for o in offsets]

def reverse_key(key: List[int]) -> List[int]:
    """Reverse a key."""
    return list(reversed(key))

def shift_key(key: List[int], shift: int) -> List[int]:
    """Shift all values in key by a constant."""
    return [(k + shift) % ALPHABET_SIZE for k in key]

def invert_key(key: List[int]) -> List[int]:
    """Invert key values (for decrypt/encrypt swap)."""
    return [(ALPHABET_SIZE - k) % ALPHABET_SIZE for k in key]

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

def print_dictionary_stats():
    """Print statistics about the dictionary."""
    print("=" * 60)
    print("MASTER DICTIONARY STATISTICS")
    print("=" * 60)
    print(f"Alphabet size: {ALPHABET_SIZE}")
    print(f"Total primes loaded: {len(PRIMES)}")
    print(f"Cicada-specific terms: {len(CICADA_TERMS)}")
    print(f"Self-Reliance words: {len(SELF_RELIANCE_WORDS)}")
    print(f"Common English words: {len(COMMON_ENGLISH_WORDS)}")
    print(f"Solved plaintext words: {len(SOLVED_PLAINTEXT_WORDS)}")
    print(f"Total unique words: {len(ALL_WORDS)}")
    print(f"Total keys available: {len(ALL_KEYS)}")
    print(f"Trigrams for scoring: {len(TRIGRAMS)}")
    print(f"Bigrams for scoring: {len(BIGRAMS)}")
    print(f"Quadgrams for scoring: {len(QUADGRAMS)}")
    print("=" * 60)

if __name__ == "__main__":
    print_dictionary_stats()
    
    # Test some conversions
    print("\nSample key conversions:")
    for word in ["DIVINITY", "CICADA", "PRIMUS", "TOTIENT", "CIRCUMFERENCE"]:
        key = text_to_key(word)
        print(f"  {word} -> {key}")

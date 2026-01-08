#!/usr/bin/env python3
"""
Prime Sum Attack - Test if decryption works via prime value sums

The insight: Each rune word's prime sum might need to match an English word's prime sum
after some transformation.

Key discovery: Many words share the same prime sum:
- WISDOM = SECRET = 270
- ALL = LIBER = 243
- TRUTH (would need to calculate) etc.
"""

import os
import re
from collections import defaultdict

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
PRIME_TO_LETTER = {p: l for p, l in zip(PRIMES, LETTERS)}
LETTER_TO_PRIME = {l: p for l, p in zip(LETTERS, PRIMES)}
LETTER_TO_INDEX = {l: i for i, l in enumerate(LETTERS)}
INDEX_TO_LETTER = {i: l for i, l in enumerate(LETTERS)}

def text_to_prime_sum(text):
    """Convert text to sum of prime values"""
    text = text.upper()
    total = 0
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'EA']:
                total += LETTER_TO_PRIME[digraph]
                i += 2
                continue
        if text[i] in LETTER_TO_PRIME:
            total += LETTER_TO_PRIME[text[i]]
        i += 1
    return total

def text_to_indices(text):
    """Convert text to list of indices"""
    text = text.upper()
    indices = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            digraph = text[i:i+2]
            if digraph in LETTER_TO_INDEX:
                indices.append(LETTER_TO_INDEX[digraph])
                i += 2
                continue
        if text[i] in LETTER_TO_INDEX:
            indices.append(LETTER_TO_INDEX[text[i]])
        else:
            indices.append(-1)  # Unknown character
        i += 1
    return indices

def indices_to_text(indices):
    """Convert indices back to text"""
    return ''.join(INDEX_TO_LETTER.get(i, '?') for i in indices)

def read_rune_words(page_num):
    """Read rune file and return list of words (hyphen-separated groups)"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Split by hyphens to get words
    words = re.split(r'-+', content)
    words = [w.strip() for w in words if w.strip()]
    return words

def load_english_words():
    """Load comprehensive English word list"""
    words = set()
    
    # Common words
    common = """
    A AN THE AND OR BUT IF OF TO IN ON AT BY FOR WITH AS IS IT HE SHE WE THEY
    BE AM ARE WAS WERE BEEN BEING HAVE HAS HAD HAVING DO DOES DID DOING
    WILL WOULD SHOULD COULD MAY MIGHT MUST CAN SHALL OUGHT NEED DARE
    I ME MY MINE MYSELF YOU YOUR YOURS YOURSELF HE HIM HIS HIMSELF
    SHE HER HERS HERSELF IT ITS ITSELF WE US OUR OURS OURSELVES
    THEY THEM THEIR THEIRS THEMSELVES WHO WHOM WHOSE WHAT WHICH THAT
    THIS THESE THOSE ONE SOME ANY ALL NO NONE EACH EVERY EITHER NEITHER
    MUCH MANY MORE MOST LITTLE LESS LEAST FEW FEWER FEWEST OTHER ANOTHER
    SUCH SAME DIFFERENT LIKE UNLIKE SIMILAR VARIOUS SEVERAL CERTAIN
    GO WENT GONE GOING COME CAME COMING GET GOT GETTING GIVE GAVE GIVEN
    TAKE TOOK TAKEN TAKING MAKE MADE MAKING SEE SAW SEEN SEEING KNOW KNEW
    THINK THOUGHT FEEL FELT WANT WANTED USE USED FIND FOUND TELL TOLD
    SAY SAID CALL CALLED BECOME BECAME TRY TRIED LEAVE LEFT PUT PUTTING
    MEAN MEANT KEEP KEPT LET BEGIN BEGAN SEEM SEEMED HELP HELPED SHOW
    HEAR HEARD PLAY PLAYED RUN RAN MOVE MOVED LIVE LIVED BELIEVE BELIEVED
    BRING BROUGHT HAPPEN HAPPENED WRITE WROTE SET SETTING SIT SAT STAND
    LOSE LOST PAY PAID MEET MET INCLUDE INCLUDED CONTINUE CONTINUED
    LEARN LEARNED CHANGE CHANGED LEAD LED UNDERSTAND UNDERSTOOD WATCH
    FOLLOW FOLLOWED STOP STOPPED CREATE CREATED SPEAK SPOKE ALLOW ALLOWED
    ADD ADDED SPEND SPENT GROW GREW OPEN OPENED WALK WALKED WIN WON OFFER
    REMEMBER REMEMBERED LOVE LOVED CONSIDER CONSIDERED APPEAR APPEARED
    BUY BOUGHT WAIT WAITED SERVE SERVED DIE DIED SEND SENT EXPECT EXPECTED
    BUILD BUILT STAY STAYED FALL FELL CUT CUTTING REACH REACHED KILL KILLED
    REMAIN REMAINED SUGGEST SUGGESTED RAISE RAISED PASS PASSED SELL SOLD
    REQUIRE REQUIRED REPORT REPORTED DECIDE DECIDED PULL PULLED
    TIME YEAR PEOPLE WAY DAY MAN WOMAN CHILD WORLD LIFE HAND PART PLACE
    CASE WEEK COMPANY SYSTEM GROUP PROBLEM FACT POINT GOVERNMENT STUDY
    AREA WATER MONEY STORY WORK JOB THING NIGHT HOME BOOK WORD FAMILY
    POWER STATE COUNTRY HEAD MOTHER FATHER QUESTION HOUSE SIDE DEVELOPMENT
    BODY IDEA FRIEND HOUR RATE FACE REASON RESULT SCHOOL CITY COMMUNITY
    PERSON ROOM MARKET PROGRAM CHANGE MEMBER INFORMATION RESEARCH STUDENT
    BUSINESS DOOR HEALTH OFFICE SERVICE PARTY LEVEL PLAN VALUE PRESIDENT
    HISTORY VOICE COURSE GROUP INTEREST SITUATION EXPERIENCE POSITION POLICY
    GAME ISSUE CENTER MEETING ACTION MOMENT PRACTICE TOWN NUMBER NAME
    WAR NATURE TRUTH WISDOM SPIRIT MIND SOUL HEART WILL POWER FORCE
    LOVE FEAR HOPE FAITH PEACE LIGHT DARK SHADOW VOID FORM MATTER ENERGY
    SPACE EARTH AIR FIRE WATER METAL STONE WOOD FLESH BLOOD BONE SPIRIT
    THOUGHT DREAM VISION WORD SPEECH SILENCE SOUND MUSIC DANCE SONG ART
    BEAUTY TRUTH GOOD EVIL LIFE DEATH BIRTH GROWTH DECAY END BEGINNING
    PAST PRESENT FUTURE ETERNITY MOMENT HOUR DAY NIGHT YEAR AGE ERA
    EAST WEST NORTH SOUTH UP DOWN LEFT RIGHT CENTER ABOVE BELOW
    WHOLE PART HALF DOUBLE TRIPLE SINGLE MANY FEW ALL NONE SOME ANY
    FIRST SECOND THIRD FOURTH FIFTH LAST NEXT PREVIOUS FINAL ONLY
    NEW OLD YOUNG ANCIENT MODERN ETERNAL MORTAL DIVINE SACRED PROFANE
    HIGH LOW DEEP SHALLOW WIDE NARROW LONG SHORT GREAT SMALL BIG LITTLE
    STRONG WEAK FAST SLOW BRIGHT DIM LOUD QUIET HARD SOFT ROUGH SMOOTH
    HOT COLD WARM COOL DRY WET CLEAN DIRTY PURE MIXED SIMPLE COMPLEX
    FULL EMPTY OPEN CLOSED FREE BOUND WILD TAME ALIVE DEAD REAL FAKE
    TRUE FALSE RIGHT WRONG GOOD BAD BEAUTIFUL UGLY RICH POOR WISE FOOLISH
    WELCOME PILGRIM JOURNEY TOWARD SEEKER FINDER KEEPER MAKER BREAKER
    CIPHER CYPHER CODE SECRET HIDDEN MYSTERY PUZZLE RIDDLE ENIGMA CLUE
    PRIMUS LIBER BOOK SCROLL TEXT WORD LETTER RUNE SYMBOL SIGN
    EMERGE INSTAR BECOME TRANSFORM CHANGE GROW EVOLVE ASCEND DESCEND
    COMMAND INSTRUCTION ORDER RULE LAW PRINCIPLE AXIOM THEOREM TRUTH
    CIRCUMFERENCE DIAMETER RADIUS CIRCLE SPHERE SQUARE TRIANGLE POINT LINE
    CARNAL AETHEREAL MATERIAL SPIRITUAL PHYSICAL MENTAL ETERNAL TEMPORAL
    TOTIENT PRIME FACTOR MULTIPLE DIVIDE MULTIPLY ADD SUBTRACT POWER ROOT
    ENCRYPT DECRYPT ENCODE DECODE CIPHER DECIPHER SOLVE UNSOLVED MYSTERY
    THOU THEE THY THINE HATH DOTH GOETH DOETH UNTO UPON WHILST AMONGST
    WHEREFORE THEREFORE HEREBY HEREIN THEREOF WHEREIN HEREBY HERETOFORE
    VERILY TRULY SURELY CERTAINLY INDEED FORSOOTH BEHOLD OBSERVE WITNESS
    SEEK SEEKETH FOUND FINDETH KNOCK KNOCKETH OPEN OPENETH ASK ASKETH
    KNOW KNOWETH WISDOM UNDERSTANDING KNOWLEDGE INSIGHT REVELATION
    SHALL SHALT WILL WILT WOULD WOULDST SHOULD SHOULDST COULD COULDST
    MAY MAYEST MIGHT MIGHTEST MUST OUGHT CAN CANST NEED NEEDEST
    INSTRUCTION COMMAND OBEY FOLLOW LEAD GUIDE TEACH LEARN MASTER STUDENT
    REALITY ILLUSION TRUTH LIE WISDOM FOLLY LIGHT DARKNESS LIFE DEATH
    OUTSIDE INSIDE ABOVE BELOW BEFORE AFTER WITHIN WITHOUT BEYOND
    THING THINGS BEING BEINGS ENTITY ENTITIES ESSENCE FORM SUBSTANCE
    SELF SELVES SOUL SOULS SPIRIT SPIRITS MIND MINDS BODY BODIES
    CONSUME CONSUMED CONSUMING DEVOUR DEVOURED DEVOURING ABSORB ABSORBED
    AN INSTRUCTION COMMAND YOUR OWN SELF DIVINITY
    """.split()
    words.update(w for w in common)
    
    return words

def build_prime_lookup(words):
    """Build mapping from prime sum to possible English words"""
    sum_to_words = defaultdict(list)
    for word in words:
        ps = text_to_prime_sum(word)
        sum_to_words[ps].append(word)
    return sum_to_words

def decrypt_word_with_key(rune_word, key_word, operation='sub'):
    """
    Decrypt a rune word using a key word's prime values
    - Cycles through key letters
    - Applies operation (sub/add) mod 29
    """
    rune_indices = text_to_indices(rune_word)
    key_indices = text_to_indices(key_word)
    
    if not key_indices:
        return rune_word
    
    decrypted = []
    for i, idx in enumerate(rune_indices):
        if idx == -1:
            continue
        key_idx = key_indices[i % len(key_indices)]
        if operation == 'sub':
            new_idx = (idx - key_idx) % 29
        else:
            new_idx = (idx + key_idx) % 29
        decrypted.append(new_idx)
    
    return indices_to_text(decrypted)

def test_prime_sum_matching(page_num, key, operation='sub'):
    """
    Test if decrypted words have prime sums matching English words
    """
    words = read_rune_words(page_num)
    english = load_english_words()
    prime_lookup = build_prime_lookup(english)
    
    print(f"\n=== Page {page_num} with key '{key}' ({operation}) ===")
    print(f"Total words: {len(words)}")
    
    matches = []
    for i, rune_word in enumerate(words[:20]):  # First 20 words
        decrypted = decrypt_word_with_key(rune_word, key, operation)
        prime_sum = text_to_prime_sum(decrypted)
        possible = prime_lookup.get(prime_sum, [])
        
        if possible:
            matches.append((i, rune_word, decrypted, prime_sum, possible))
            print(f"  Word {i}: {rune_word} -> {decrypted} (sum={prime_sum}) -> {possible}")
        else:
            print(f"  Word {i}: {rune_word} -> {decrypted} (sum={prime_sum}) -> no match")
    
    return matches

def test_word_length_preservation(page_num):
    """
    Check if rune word lengths could match English word lengths
    assuming hyphens are word boundaries
    """
    words = read_rune_words(page_num)
    
    print(f"\n=== Page {page_num} Word Length Analysis ===")
    
    # Count how many runes in each word
    for i, word in enumerate(words[:15]):
        indices = text_to_indices(word)
        rune_count = len([x for x in indices if x >= 0])
        print(f"  Word {i}: '{word}' -> {rune_count} runes")

def main():
    print("=" * 60)
    print("PRIME SUM ATTACK - Testing if cipher uses prime value sums")
    print("=" * 60)
    
    # Test word length preservation first
    test_word_length_preservation(0)
    test_word_length_preservation(2)
    
    # Test various keys with prime sum matching
    keys = ['DIVINITY', 'WISDOM', 'PILGRIM', 'WELCOME', 'SACRED', 'PRIMUS']
    
    for key in keys:
        for op in ['sub', 'add']:
            test_prime_sum_matching(2, key, op)
            print()

if __name__ == '__main__':
    main()

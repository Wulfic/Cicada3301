#!/usr/bin/env python3
"""
Vigenère Word Attack - Test if each word uses the same key pattern

Hypothesis: Each word is encrypted with a short repeating key that
resets at each word boundary.

We'll try common short keys like "DIVINITY", "WISDOM", "PILGRIM", etc.
and score based on how many words produce valid English.
"""

import os
import re
from collections import defaultdict, Counter

RUNE_TO_INDEX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

INDEX_TO_LETTER = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
                   'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 
                   'A', 'AE', 'Y', 'IA', 'EA']

LETTER_TO_INDEX = {
    'F': 0, 'U': 1, 'TH': 2, 'O': 3, 'R': 4, 'C': 5, 'K': 5, 'G': 6,
    'W': 7, 'H': 8, 'N': 9, 'I': 10, 'J': 11, 'EO': 12, 'P': 13,
    'X': 14, 'S': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19, 'L': 20,
    'NG': 21, 'OE': 22, 'D': 23, 'A': 24, 'AE': 25, 'Y': 26,
    'IA': 27, 'IO': 27, 'EA': 28, 'V': 1, 'Q': 5, 'Z': 15
}

def text_to_indices(text):
    """Convert English text to Gematria Primus indices"""
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
        i += 1
    return indices

def runes_to_indices(runes):
    return [RUNE_TO_INDEX[r] for r in runes if r in RUNE_TO_INDEX]

def indices_to_text(indices):
    return ''.join(INDEX_TO_LETTER[i] for i in indices if 0 <= i < 29)

def read_rune_words(page_num):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rune_path = os.path.join(base_path, 'pages', f'page_{page_num:02d}', 'runes.txt')
    
    with open(rune_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    words = re.split(r'[-\n]+', content)
    words = [w.strip() for w in words if w.strip()]
    return words

# English word dictionary
ENGLISH_WORDS = set("""
A AN THE AND OR BUT IF OF TO IN ON AT BY FOR WITH AS IS IT HE SHE WE THEY I
BE AM ARE WAS WERE BEEN BEING HAVE HAS HAD HAVING DO DOES DID DOING
WILL WOULD SHOULD COULD MAY MIGHT MUST CAN SHALL OUGHT NEED DARE
ME MY MINE MYSELF YOU YOUR YOURS YOURSELF HE HIM HIS HIMSELF
HER HERS HERSELF IT ITS ITSELF US OUR OURS OURSELVES
THEM THEIR THEIRS THEMSELVES WHO WHOM WHOSE WHAT WHICH THAT
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
TIME YEAR PEOPLE WAY DAY MAN WOMAN CHILD WORLD LIFE HAND PART PLACE
THING NIGHT HOME BOOK WORD FAMILY POWER STATE COUNTRY HEAD MOTHER FATHER
QUESTION HOUSE SIDE BODY IDEA FRIEND HOUR FACE REASON RESULT SCHOOL
PERSON ROOM MARKET PROGRAM MEMBER RESEARCH STUDENT BUSINESS DOOR HEALTH
WAR NATURE TRUTH WISDOM SPIRIT MIND SOUL HEART WILL FORCE LOVE FEAR HOPE
FAITH PEACE LIGHT DARK SHADOW VOID FORM MATTER ENERGY SPACE EARTH AIR
FIRE WATER THOUGHT DREAM VISION SPEECH SILENCE SOUND MUSIC ART BEAUTY
GOOD EVIL DEATH BIRTH GROWTH DECAY END BEGINNING PAST PRESENT FUTURE
EAST WEST NORTH SOUTH UP DOWN LEFT RIGHT CENTER ABOVE BELOW
WHOLE HALF DOUBLE TRIPLE SINGLE FIRST SECOND THIRD FOURTH FIFTH LAST NEXT
NEW OLD YOUNG ANCIENT MODERN ETERNAL MORTAL DIVINE SACRED PROFANE
HIGH LOW DEEP WIDE LONG SHORT GREAT SMALL BIG STRONG WEAK FAST SLOW
BRIGHT DIM LOUD QUIET HARD SOFT HOT COLD WARM COOL DRY WET CLEAN DIRTY
PURE SIMPLE COMPLEX FULL EMPTY OPEN CLOSED FREE BOUND WILD ALIVE DEAD REAL
TRUE FALSE RIGHT WRONG BEAUTIFUL UGLY RICH POOR WISE FOOLISH
WELCOME PILGRIM JOURNEY TOWARD SEEKER FINDER KEEPER MAKER BREAKER
CIPHER CODE SECRET HIDDEN MYSTERY PUZZLE RIDDLE ENIGMA CLUE
PRIMUS LIBER SCROLL TEXT LETTER RUNE SYMBOL SIGN
EMERGE INSTAR BECOME TRANSFORM GROW EVOLVE ASCEND DESCEND
COMMAND INSTRUCTION ORDER RULE LAW PRINCIPLE AXIOM THEOREM
CIRCUMFERENCE DIAMETER RADIUS CIRCLE SPHERE SQUARE TRIANGLE POINT LINE
CARNAL AETHEREAL MATERIAL SPIRITUAL PHYSICAL MENTAL ETERNAL TEMPORAL
TOTIENT PRIME FACTOR MULTIPLE DIVIDE MULTIPLY ADD SUBTRACT ROOT
ENCRYPT DECRYPT ENCODE DECODE DECIPHER SOLVE UNSOLVED
THOU THEE THY THINE HATH DOTH GOETH DOETH UNTO UPON WHILST AMONGST
WHEREFORE THEREFORE HEREBY HEREIN THEREOF WHEREIN HERETOFORE
VERILY TRULY SURELY CERTAINLY INDEED FORSOOTH BEHOLD OBSERVE WITNESS
SEEK SEEKETH KNOCK KNOCKETH ASK ASKETH
KNOWETH UNDERSTANDING KNOWLEDGE INSIGHT REVELATION
SHALT WILT WOULDST SHOULDST COULDST MAYEST MIGHTEST CANST NEEDEST
OBEY FOLLOW GUIDE TEACH MASTER SELF SELVES BEINGS ENTITY ESSENCE
CONSUME CONSUMED CONSUMING DEVOUR DEVOURED ABSORB ABSORBED
DIVINITY WITHIN REALITY OUTSIDE THINGS SHADOWS MOBIUS AETHEREAL
PARABLE SURFACE SHED CIRCUMFERENCES TUNNELING
""".upper().split())

def decrypt_word_with_key(rune_indices, key_indices, operation='sub'):
    """Decrypt a word using key with word-boundary reset"""
    decrypted = []
    for i, idx in enumerate(rune_indices):
        k = key_indices[i % len(key_indices)]
        if operation == 'sub':
            new_idx = (idx - k) % 29
        else:
            new_idx = (idx + k) % 29
        decrypted.append(new_idx)
    return decrypted

def score_decryption(decrypted_words, english_dict):
    """Score how many decrypted words are in the English dictionary"""
    matches = []
    for i, indices in enumerate(decrypted_words):
        text = indices_to_text(indices)
        if text in english_dict:
            matches.append((i, text))
    return len(matches), matches

def test_key(page_num, key_text, operation='sub'):
    """Test a key word on a page"""
    words = read_rune_words(page_num)
    key_indices = text_to_indices(key_text)
    
    decrypted_words = []
    for rune_word in words:
        rune_indices = runes_to_indices(rune_word)
        if not rune_indices:
            decrypted_words.append([])
            continue
        decrypted = decrypt_word_with_key(rune_indices, key_indices, operation)
        decrypted_words.append(decrypted)
    
    score, matches = score_decryption(decrypted_words, ENGLISH_WORDS)
    return score, matches, decrypted_words

def main():
    # Keys to try (Cicada-relevant words)
    keys = [
        'DIVINITY', 'WISDOM', 'PILGRIM', 'WELCOME', 'JOURNEY', 'SACRED', 'PRIMUS',
        'LIBER', 'CICADA', 'INSTAR', 'EMERGE', 'TRUTH', 'DIVINE', 'SPIRIT',
        'SHADOW', 'VOID', 'LIGHT', 'DARK', 'PATH', 'SEEK', 'FIND', 'KNOW',
        'SELF', 'MIND', 'SOUL', 'GOD', 'THE', 'AND', 'PARABLE', 'SURFACE',
        'CIRCUMFERENCE', 'TUNNELING', 'SHED', 'CARNAL', 'AETHEREAL', 'MOBIUS',
        'TOTIENT', 'PRIME', 'REALITY', 'OUTSIDE', 'WITHIN', 'COMMAND',
        'INSTRUCTION', 'CONSUME', 'BEHOLD', 'VERILY', 'UNTO', 'UPON',
        'IP', 'PI', 'EP', 'PE', 'IPEP', 'PEPI', 'FIBONACCI', 'EULER',
        'FU', 'TH', 'OR', 'CG', 'WH', 'NI', 'FP', 'XT', 'SB', 'EM', 'LNG',
    ]
    
    print("=" * 70)
    print("VIGENÈRE WORD ATTACK - Testing keys with word-boundary reset")
    print("=" * 70)
    
    for page_num in [0, 2, 3, 4]:
        print(f"\n{'='*70}")
        print(f"PAGE {page_num}")
        print(f"{'='*70}")
        
        results = []
        for key in keys:
            for op in ['sub', 'add']:
                score, matches, _ = test_key(page_num, key, op)
                if score > 2:
                    results.append((score, key, op, matches))
        
        # Sort by score
        results.sort(key=lambda x: -x[0])
        
        if results:
            print(f"\nTop keys for Page {page_num}:")
            for score, key, op, matches in results[:10]:
                match_words = ', '.join(f"{i}:{w}" for i, w in matches[:8])
                print(f"  {key:15s} ({op}): {score:2d} matches - {match_words}")
        else:
            print(f"\nNo keys found with >2 matches for Page {page_num}")
        
        # Show best decryption
        if results:
            best_score, best_key, best_op, _ = results[0]
            print(f"\nBest decryption (key={best_key}, op={best_op}):")
            _, _, decrypted_words = test_key(page_num, best_key, best_op)
            words = read_rune_words(page_num)
            
            output = []
            for i, indices in enumerate(decrypted_words):
                if indices:
                    text = indices_to_text(indices)
                    if text in ENGLISH_WORDS:
                        output.append(f"[{text}]")
                    else:
                        output.append(text)
                else:
                    output.append("?")
            
            print(' '.join(output[:40]) + "...")

if __name__ == '__main__':
    main()

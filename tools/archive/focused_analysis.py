#!/usr/bin/env python3
"""
FOCUSED ANALYSIS - Deep dive into the most promising results.
Page 28 double_xor_xor has 45.3% word coverage with clear patterns.
"""

import re
from collections import Counter

# =============================================================================
# CONSTANTS
# =============================================================================
RUNES = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 
         'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA']
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}
NUM_RUNES = 29

MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]

RUNE_UNICODE = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

UNSOLVED_PAGES = {
    28: "ᛡᚳᛏᛄᛝᛠᛠᛡᛗᚱᛡᛁᚢᛠᚣᚫᛟᛡᛒᛗᛁᚷᚦᛄᛝᚷᛝᚦᛋᛄᛟᛡᚱᛡᛗᛏᛠᚪᚫᛒᛁᛄᛞᛄᚾᛄᛝᛠᛞᛡᚱᛡᚪᛟᛇᛖᛄᛞᛄᛒᚢᛇᚾᛈᛇᚱᛄᛗᚳᚢᛄᛡᛄᛗᛡᚫᛋᛠᚣᛖᛟᛏᛟᛠᛟᛄᛗᛒᚱᛏᛡᛄᛇᛖᛏᛝᛠᛏᚫᛏ",
    52: "ᛇᛠᚣᛏᚳᛖᛟᛄᛋᛡᛝᚣᛟᛄᛇᛈᛒᛡᛝᛋᛇᛖᛠᚠᛚᛈᛠᛁᛁᚾᛗᛟᛠᛡᚳᚷᛏᛋᛄᚾᛡᚳᛗᛈᚾᛇᚣᛄᛏᛠᛟᛠᛗᚾᚫᚪᛏᛖᛖᚠᛁᛁᚾᛁᛏᛇᛟᚣᚱᛒᛡᚣᛠᛖᛋᛟᛈᛡᚱᛏᛖᚫᛠᛒᛋᚦᛁᛁᛗ",
    44: "ᚱᛟᛝᛖᛇᛡᚣᛄᚱᚣᛟᛝᛗᛖᚱᚣᛇᚢᚠᚣᛚᛋᚦᚣᛏᛈᛠᛟᛏᚣᛗᛇᚳᚣᛏᛟᚢᚣᛒᛇᛟᛇᚣᚦᛈᚣᛡᚪᛒᛚᛡᚣᛚᛚᛇᛏᛟᛝᛄᛇᛏᛚᛈᚣᛠᛖᛠᛁᚣᚪᛗᚣᛖᛇᛟᛄᛚᛇᛒᛁᛗᛄᛇᚣᛝᛠᛇᚫᚷ",
}

def unicode_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_UNICODE:
            rune = RUNE_UNICODE[char]
            if rune in RUNE_TO_IDX:
                indices.append(RUNE_TO_IDX[rune])
    return indices

def indices_to_text(indices):
    return ''.join(RUNES[i] for i in indices)

def decrypt_xor(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = ((idx - offset) ^ key_val) % NUM_RUNES
        result.append(plain_idx)
    return result

def decrypt_sub(indices, rotation, offset):
    result = []
    key_len = len(MASTER_KEY)
    for i, idx in enumerate(indices):
        key_val = MASTER_KEY[(i + rotation) % key_len]
        plain_idx = (idx - key_val - offset) % NUM_RUNES
        result.append(plain_idx)
    return result

# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_page_28():
    """Deep analysis of Page 28 with the best result."""
    print("=" * 80)
    print("🔬 DEEP ANALYSIS: PAGE 28")
    print("   Method: double_xor_xor (rot1=80, off1=5, rot2=10, off2=25)")
    print("=" * 80)
    
    indices = unicode_to_indices(UNSOLVED_PAGES[28])
    print(f"\nPage length: {len(indices)} runes")
    
    # Best parameters from previous analysis
    dec1 = decrypt_xor(indices, 80, 5)
    dec2 = decrypt_xor(dec1, 10, 25)
    text = indices_to_text(dec2)
    
    print(f"\nDecrypted text:\n{text}")
    print(f"\nLength: {len(text)} characters")
    
    # Manual word segmentation attempt
    print("\n" + "-" * 60)
    print("MANUAL SEGMENTATION ATTEMPT:")
    print("-" * 60)
    
    # The text is: DTHEONGWTHEYTIAITHEATHXOERNYTEADJTHEANGTHIATMYSUODEAYYMEIADUNGBYYPFXEIAEAOEIYODXIAREADEAPESAYAEIAMTHEOTHWCAEBEOCYHDAEYMYEANGRPBNGDIAEEOWF
    
    # Let me try to find word boundaries
    text_with_spaces = ""
    words_found = []
    
    # Known patterns I can see:
    patterns = [
        (0, 'D'),      # unclear
        (1, 'THE'),    # THE
        (4, 'ON'),     # ON (or LONG without L?)
        (6, 'G'),      # unclear
        (7, 'W'),      # unclear
        (8, 'THEY'),   # THEY
        (12, 'T'),     # unclear
        (13, 'IA'),    # IA (rune?)
        (15, 'I'),     # I
        (16, 'THE'),   # THE
        (19, 'AT'),    # AT (or A TH?)
        (21, 'H'),     # unclear
        (22, 'X'),     # unclear
        (23, 'O'),     # unclear
        (24, 'E'),     # unclear
        (25, 'R'),     # unclear
        (26, 'NY'),    # unclear
        (28, 'T'),     # unclear
        (29, 'E'),     # unclear
        (30, 'A'),     # A
        (31, 'D'),     # unclear
        (32, 'J'),     # unclear
        (33, 'THE'),   # THE
        (36, 'AN'),    # AN
        (38, 'G'),     # unclear (or GANG?)
        (39, 'TH'),    # TH
        (41, 'IA'),    # IA
        (43, 'T'),     # unclear
        (44, 'MY'),    # MY
        (46, 'S'),     # unclear
        (47, 'U'),     # unclear
        (48, 'O'),     # unclear
        (49, 'D'),     # unclear
        (50, 'E'),     # unclear
        (51, 'AYY'),   # unclear
        (54, 'ME'),    # ME
        (56, 'IA'),    # IA
        (58, 'D'),     # unclear
        (59, 'UN'),    # unclear (or DUNG?)
        (61, 'G'),     # unclear
        (62, 'BY'),    # BY
        (64, 'Y'),     # unclear
        (65, 'P'),     # unclear
        (66, 'F'),     # unclear
        (67, 'X'),     # unclear
        (68, 'E'),     # unclear
        (69, 'IA'),    # IA
        (71, 'E'),     # unclear
        (72, 'A'),     # A
        (73, 'O'),     # unclear
        (74, 'E'),     # unclear
        (75, 'I'),     # I
        (76, 'Y'),     # unclear
        (77, 'O'),     # unclear
        (78, 'D'),     # unclear
        (79, 'X'),     # unclear
        (80, 'IA'),    # IA
        (82, 'READ'), # READ (or ARE AD?)
        (86, 'EA'),    # EA
        (88, 'P'),     # unclear
        (89, 'E'),     # unclear
        (90, 'SAY'),   # SAY
        (93, 'A'),     # A
        (94, 'E'),     # unclear
        (95, 'IA'),    # IA
        (97, 'M'),     # unclear
        (98, 'THE'),   # THE
        (101, 'O'),    # unclear
        (102, 'TH'),   # unclear
        (104, 'W'),    # unclear
        (105, 'C'),    # unclear
        (106, 'A'),    # A
        (107, 'E'),    # unclear
        (108, 'BE'),   # BE
        (110, 'O'),    # unclear
        (111, 'C'),    # unclear
        (112, 'Y'),    # unclear
        (113, 'HD'),   # unclear
        (115, 'A'),    # A
        (116, 'E'),    # unclear
        (117, 'Y'),    # unclear
        (118, 'MY'),   # MY
        (120, 'E'),    # unclear
        (121, 'AN'),   # AN
        (123, 'G'),    # unclear
        (124, 'R'),    # unclear
        (125, 'P'),    # unclear
        (126, 'B'),    # unclear
        (127, 'NG'),   # NG (rune)
        (129, 'D'),    # unclear
        (130, 'IA'),   # IA
        (132, 'E'),    # unclear
        (133, 'E'),    # unclear
        (134, 'O'),    # unclear
        (135, 'W'),    # unclear
        (136, 'F'),    # unclear
    ]
    
    # Try to read it as: "D THE ON G W THEY T IA I THE AT H X O E R NY T E A D J THE AN G TH IA T MY..."
    # Or: "D THE LONG THEY ??? THE AT ??? THE AN ??? MY ..."
    
    # Let's try searching for finer parameters around the best result
    print("\n" + "-" * 60)
    print("FINE-TUNING PARAMETERS:")
    print("-" * 60)
    
    best_score = 0
    best_text = ""
    best_params = None
    
    for rot1 in range(75, 86):
        for off1 in range(10):
            for rot2 in range(5, 16):
                for off2 in range(20, 30):
                    dec1 = decrypt_xor(indices, rot1, off1)
                    dec2 = decrypt_xor(dec1, rot2, off2)
                    text = indices_to_text(dec2)
                    
                    # Score by counting THE, THEY, ARE, SAY occurrences
                    score = 0
                    for word in ['THE', 'THEY', 'ARE', 'SAY', 'MY', 'BE', 'AN', 'AT', 'ON', 'READ', 'DID']:
                        score += text.count(word) * len(word)
                    
                    if score > best_score:
                        best_score = score
                        best_text = text
                        best_params = (rot1, off1, rot2, off2)
    
    print(f"Best params: rot1={best_params[0]}, off1={best_params[1]}, rot2={best_params[2]}, off2={best_params[3]}")
    print(f"Best score: {best_score}")
    print(f"Best text: {best_text}")

def analyze_page_44():
    """Deep analysis of Page 44."""
    print("\n" + "=" * 80)
    print("🔬 DEEP ANALYSIS: PAGE 44")
    print("   Method: xor (rot=77, off=1)")
    print("=" * 80)
    
    indices = unicode_to_indices(UNSOLVED_PAGES[44])
    
    # The text shows: THEYTHEOLYTBUTHWYNGINEODBUTHEJEOETHEOIEBTHTHTEOFLEARFWAEUBIAIAPSYOEGIEAFJOEXCHCCEARSMAEFWIANGUAEOCNHACNGIUTHIAEFUIPEO
    # Clear patterns: THEY THE, BUT, THE, OF
    
    text = indices_to_text(decrypt_xor(indices, 77, 1))
    print(f"\nDecrypted text:\n{text}")
    
    # Try all nearby parameters
    print("\n" + "-" * 60)
    print("FINE-TUNING PARAMETERS:")
    print("-" * 60)
    
    best_score = 0
    best_text = ""
    best_params = None
    
    for rot in range(70, 85):
        for off in range(29):
            text = indices_to_text(decrypt_xor(indices, rot, off))
            
            score = 0
            for word in ['THE', 'THEY', 'BUT', 'OF', 'AND', 'LEARN', 'FEAR', 'EARS']:
                score += text.count(word) * len(word)
            
            if score > best_score:
                best_score = score
                best_text = text
                best_params = (rot, off)
    
    print(f"Best params: rot={best_params[0]}, off={best_params[1]}")
    print(f"Best score: {best_score}")
    print(f"Best text: {best_text}")
    
    # Also try double XOR
    print("\n" + "-" * 60)
    print("TRYING DOUBLE XOR:")
    print("-" * 60)
    
    best_score = 0
    best_text = ""
    best_params = None
    
    for rot1 in range(0, 95, 10):
        for off1 in range(0, 29, 5):
            dec1 = decrypt_xor(indices, rot1, off1)
            for rot2 in range(0, 95, 10):
                for off2 in range(0, 29, 5):
                    dec2 = decrypt_xor(dec1, rot2, off2)
                    text = indices_to_text(dec2)
                    
                    score = 0
                    for word in ['THE', 'THEY', 'BUT', 'OF', 'AND', 'LEARN', 'FEAR', 'EARS', 'THIS', 'THAT']:
                        score += text.count(word) * len(word) * 2
                    
                    if score > best_score:
                        best_score = score
                        best_text = text
                        best_params = (rot1, off1, rot2, off2)
    
    if best_params:
        print(f"Best params: rot1={best_params[0]}, off1={best_params[1]}, rot2={best_params[2]}, off2={best_params[3]}")
        print(f"Best score: {best_score}")
        print(f"Best text: {best_text}")

def exhaustive_page_52():
    """Exhaustive search for Page 52."""
    print("\n" + "=" * 80)
    print("🔬 EXHAUSTIVE SEARCH: PAGE 52")
    print("=" * 80)
    
    indices = unicode_to_indices(UNSOLVED_PAGES[52])
    
    best_results = []
    
    # Try all single-layer XOR and SUB
    for method_name, method in [('xor', decrypt_xor), ('sub', decrypt_sub)]:
        for rot in range(95):
            for off in range(29):
                text = indices_to_text(method(indices, rot, off))
                
                # Score
                score = 0
                for word in ['THE', 'THERE', 'THEY', 'THAT', 'THIS', 'WITH', 'AND', 'FOR', 'ARE', 'BUT', 
                             'FROM', 'HAVE', 'NOT', 'ALL', 'ONE', 'CAN', 'HER', 'WAS', 'OUR', 'OUT']:
                    count = text.count(word)
                    if count > 0:
                        score += count * len(word) * 3
                
                if score >= 40:
                    best_results.append({
                        'method': method_name,
                        'rot': rot,
                        'off': off,
                        'score': score,
                        'text': text[:80]
                    })
    
    # Sort and display
    best_results.sort(key=lambda x: -x['score'])
    
    print("\nTop 15 results:")
    for i, r in enumerate(best_results[:15]):
        print(f"\n#{i+1}: {r['method']} rot={r['rot']}, off={r['off']}, score={r['score']}")
        print(f"    {r['text']}")

def main():
    analyze_page_28()
    analyze_page_44()
    exhaustive_page_52()
    
    print("\n" + "=" * 80)
    print("🎯 FOCUSED ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

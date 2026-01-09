import os

# Copy definitions
RUNE_MAP = {
    'ᚠ': 0,  'ᚢ': 1,  'ᚦ': 2,  'ᚩ': 3,  'ᚱ': 4,  'ᚳ': 5,  'ᚷ': 6,  'ᚹ': 7,
    'ᚻ': 8,  'ᚾ': 9,  'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

def runes_to_indices(text):
    indices = []
    for char in text:
        if char in RUNE_MAP:
            indices.append(RUNE_MAP[char])
    return indices

def indices_to_eng(indices):
    return "".join([LETTERS[i] for i in indices])

# Candidate key from BATCH_RESULTS.md (Page 02)
KEY = [23, 9, 14, 21, 14, 18, 22, 21, 8, 6, 26, 3, 12, 17, 22, 18, 9, 15, 20, 1, 6, 21, 20, 25, 21, 11, 16, 22, 15, 16, 16, 0, 0, 2, 15, 4, 2, 0, 9, 22, 26, 22, 15]

# Page 02 Content
PAGE_PATH = r'c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_02\runes.txt'
with open(PAGE_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# We need to map text characters to key indices
# Only Runes consume a key index. Punctuation does not.

rune_indices = [] # List of (char_index_in_text, rune_val)
stream_index = 0
for i, char in enumerate(text):
    if char in RUNE_MAP:
        rune_indices.append((i, RUNE_MAP[char]))

print(f"Total runes: {len(rune_indices)}")

# "EAMEASTHLT" is at checking output:
# EAI-T.TTH-EAMEASTHLT
# E(0), A(1), I(2). T(3). T(4), T(5), H(6). E(7), A(8), M(9), E(10), A(11), S(12), TH(13), L(14), T(15).
# So "EAMEASTHLT" corresponds to rune stream indices 7 to 16.
# Let's extract them.

segment_indices = [x[1] for x in rune_indices[7:17]]
orig_segment_eng = indices_to_eng(segment_indices)
print(f"Cipher Segment: {orig_segment_eng}")

# Decrypt with current key
key_len = len(KEY)
current_dec = []
for i in range(7, 17):
    c = rune_indices[i][1]
    k = KEY[i % key_len]
    p = (c - k) % 29
    current_dec.append(p)

print(f"Current Decryption: {indices_to_eng(current_dec)}")
# Should match EAMEASTHLT

# Target: SAME AS THAT
TARGET_STR = "SAMEASTHAT"
# S, A, M, E, A, S, TH, A, T. (Wait 9 letters?)
# EAMEASTHLT is 10 chars?
# E(18) A(24) M(19) E(18) A(24) S(15) TH(2) L(20) T(16). (9 runes).
# S(15) A(24) M(19) E(18) A(24) S(15) TH(2) A(24) T(16). (9 runes).
# Target: S A M E A S TH A T.

target_indices = [15, 24, 19, 18, 24, 15, 2, 24, 16]

# Calculate REQUIRED Key
print("\n--- Key Repair ---")
for i in range(9):
    stream_idx = 7 + i
    c = segment_indices[i]
    t = target_indices[i]
    
    # P = (C - K) % 29  => K = (C - P) % 29
    req_k = (c - t) % 29
    curr_k = KEY[stream_idx % key_len]
    
    print(f"Pos {stream_idx}: Cipher={LETTERS[c]}, Target={LETTERS[t]}. Req K={req_k} (Curr={curr_k}) {'Mismatch!' if req_k != curr_k else 'Match'}")
    
    # Update Key
    KEY[stream_idx % key_len] = req_k

print("\n--- Updated Key ---")
print(KEY)

# Re-decrypt whole text roughly
full_dec = ""
keys_used = 0
for char in text:
    if char in RUNE_MAP:
        c = RUNE_MAP[char]
        k = KEY[keys_used % key_len]
        p = (c - k) % 29
        full_dec += LETTERS[p]
        keys_used += 1
    else:
        full_dec += char
    
print("\n--- Full Decryption with Repaired Key ---")
print(full_dec)

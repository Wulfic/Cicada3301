import os

LETTERS = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 
           'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D',
           'A', 'AE', 'Y', 'IO', 'EA']

ENG_TO_IDX = {L: i for i, L in enumerate(LETTERS)}

def get_idx(char):
    return ENG_TO_IDX.get(char, None)

# Title ciphertext indices (from analyze_p18_title.py)
# ᛠᚪᛄᛇᛠᛚ-ᚱᚷᛋ-ᚹᚩᛒᛁ-ᛠᚳ-ᛁᛞᛄ-ᛖᛗᚱ-ᚷ
# 28, 24, 11, 12, 28, 20
# 4, 6, 15
# 7, 3, 17, 10
# 28, 5
# 10, 23, 11
# 18, 19, 4
# 6

full_cipher = [
    28, 24, 11, 12, 28, 20, 
    4, 6, 15,
    7, 3, 17, 10,
    28, 5,
    10, 23, 11,
    18, 19, 4,
    6
]

# Structure:
# 6 chars
# 3 chars (BOY)
# 4 chars
# 2 chars (THE)
# 3 chars
# 3 chars (POET?)
# 1 char (N?)

# Current Key (C+K, Shift 7 -> Starts at J)
# Key: Y A H EO O P Y J (26, 24, 8, 12, 3, 13, 26, 11)
# Rotation 7: [11, 26, 24, 8, 12, 3, 13, 26] repeated

# Let's find Key K such that C+K = P
# K = (P - C) % 29

def solve_key_at(index, plaintext_letter):
    c = full_cipher[index]
    p = ENG_TO_IDX[plaintext_letter]
    k = (p - c) % 29
    return k

# KNOWN Constraints
# Word 2 (indices 6,7,8) -> BOY
k6 = solve_key_at(6, 'B')
k7 = solve_key_at(7, 'O')
k8 = solve_key_at(8, 'Y')
print(f"Key at 6,7,8 (BOY): {LETTERS[k6]}, {LETTERS[k7]}, {LETTERS[k8]} ({k6}, {k7}, {k8})")

# Word 4 (indices 13,14) -> THE
k13 = solve_key_at(13, 'TH')
k14 = solve_key_at(14, 'E')
print(f"Key at 13,14 (THE): {LETTERS[k13]}, {LETTERS[k14]} ({k13}, {k14})")

# Assume Key Length 8.
# Indicies mod 8:
# 6%8=6. 7%8=7. 8%8=0.
# 13%8=5. 14%8=6.

# K[6] = 13 (P)
# K[7] = 26 (Y)
# K[0] = 11 (J)
# K[5] = 3 (O)
# K[6] = 13 (P) (Consistent!)

# So we have confirmed Key indices 0, 5, 6, 7.
# K = [11, ?, ?, ?, ?, 3, 13, 26]
# Wait, this is the "Shifted Key". 
# 11=J, 26=Y. 
# Shift 7 of P17 Key was `J, Y, A, H, EO, O, P, Y` ??
# P17 Key: Y A H EO O P Y J.
# Rot 7: J, Y, A, H, EO, O, P, Y.
# My derived: J(11), ?, ?, ?, ?, O(3), P(13), Y(26).
# Matches perfectly!
# So the key is DEFINITELY `J Y A H EO O P Y`.
# Which is `YAHEOOPYJ` rotated.

# So the original decryption was CORRECT.
# `INGGLJD-BOY-RIOAEOE-THE-WCH-PIOT-N`.
# This MUST be the plaintext.
# But it looks weird.
# `INGGLJD`.
# `RIOAEOE`.
# `PIOT`.

# Maybe "PIOT" -> "PILOT"?
# P I L O T.
# `P`(13). `I`(10). `L`(20). `O`(3). `T`(16).
# Cipher: `E M R` (18, 19, 4).
# Key: `A H EO` (24, 8, 12). (Indices 1,2,3 of shifted key).
# Note: Word 6 indices: 18,19,20.
# 18%8=2. 19%8=3. 20%8=4.
# Use Key[2], Key[3], Key[4].
# P17 Rotated: J, Y, A(Key2=24), H(Key3=8), EO(Key4=12).
# `C+K`.
# `18+24 = 42->13 (P)`. Correct.
# `19+8 = 27 (IO)`. Need `I` (10) or `L` (20)?
# `4+12 = 16 (T)`. Correct.
# So we have `P IO T`.
# If we want `P I L O T`, we need more letters or diff key.
# But `P` and `T` are solid. `IO` matches Key.
# Is `PIOT` a word?
# Maybe `RIOT`? No `R`=4. `P`=13.

# What about `INGGLJD`?
# K: `J Y A H EO O`.
# C: `EA A J EO EA L`
# `28+11=10(I)`.
# `24+26=21(NG)`.
# `11+24=6(G)`.
# `12+8=20(L)`.
# `28+12=11(J)`.
# `20+3=23(D)`.
# `INGGLJD`.

# THIS IS THE PLAINTEXT.
# `INGGLJD` `BOY` `RIOAEOE` `THE` `WCH` `PIOT` `N`.
# Is it an anagram?
# "THE BOY INGGLJD ..."

# Maybe "INGGLJD" is "ENGLAND"?
# I N G L A N D.
# I(10) NG(21) G(6) L(20) A(24) N(9) D(23).
# We have `I NG G L J D`.
# `J` (11) vs `A` (24) vs `N` (9).
# `J` is derived from `EA`(28) + `EO`(12) = `J`(11).
# We want `A`(24) or `N`(9).
# If `A`: `28+K=24`. `K=25`(AE).
# If `N`: `28+K=9`. `K=10`(I).

# Is `PIOT` actually `PIOT`?
# Definition? "Piotr"? Peter?
# "THE BOY PIOTR"?
# `N` at end.

# Maybe `WCH` is `WATCH`.
# `W`(7) `C`(5) `H`(8).
# Plaintext `W A T C H`.
# We got `W C H`.
# `C` vs `A T C`? No.
# `C`=5. `A`=24 `T`=16.
# Maybe abbreviations?

# What if it's NOT English?
# "INGGLJD BOY RIOAEOE..."
# "ING GLJD" -> "IN GOLD"?
# "IN GOLD BOY..."

# Let's consider the Title is an Anagram or specific code?
# Or maybe I should try to solve the BODY using this Key.
# If the Title is gibberish-but-structure, maybe the Body clearly decrypts?

print("Done.")

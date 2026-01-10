# GP Runic Table with Sounds
# Based on Cicada / standard Anglo-Saxon futhorc mappings used in LP

GP_DATA = {
    0:  ('F',  'Feoh',   'f'),
    1:  ('U',  'Ur',     'u/v'),
    2:  ('TH', 'Thorn',  'th'),
    3:  ('O',  'Os',     'o'),
    4:  ('R',  'Rad',    'r'),
    5:  ('C',  'Cen',    'c/k'),
    6:  ('G',  'Gyfu',   'g'),
    7:  ('W',  'Wynn',   'w'),
    8:  ('H',  'Haegl',  'h'),
    9:  ('N',  'Nyd',    'n'),
    10: ('I',  'Is',     'i'),
    11: ('J',  'Ger',    'j/y'),
    12: ('EO', 'Eoh',    'eo/ee'), # yew tree
    13: ('P',  'Peorth', 'p'),
    14: ('X',  'Eolhx',  'x/z'),   # elk/sedge
    15: ('S',  'Sigel',  's'),
    16: ('T',  'Tir',    't'),
    17: ('B',  'Beorc',  'b'),
    18: ('E',  'Eh',     'e'),     # horse
    19: ('M',  'Man',    'm'),
    20: ('L',  'Lagu',   'l'),
    21: ('NG', 'Ing',    'ng'),
    22: ('OE', 'Ethel',  'oe'),
    23: ('D',  'Daeg',   'd'),
    24: ('A',  'Ac',     'a'),     # oak
    25: ('AE', 'Aesc',   'ae'),    # ash
    26: ('Y',  'Yr',     'y'),     # bow
    27: ('IA', 'Ior',    'ia/io'), # eel/beaver
    28: ('EA', 'Ear',    'ea')     # grave/soil
}

# Values from the candidate solution
# Extracted from previous runs (Pair Sum - Key)
# We can re-calculate them to be safe, or just hardcode the logic since it's confirmed.

stream_runes = "HOEEDOEBDMEATHLNTHRAIATOEYMYFYTXECCLTPSYTOGNIAOCDWYGDHCFPSMXMOXEOOEAEITYHYOTHTHYWSMFFEOEMTIASFLTEOENEAUOEIAAOECGWEJJDBOETAFHFBGGDTHHWGLARLEEPCMESYEOOENEOCTWFMTHTGEHGW"
key_p24 = [17, 8, 11, 25, 28, 8, 23, 6, 25, 5, 14, 6, 6, 12, 5, 19, 19, 26, 16, 23, 15, 17, 14, 23, 24, 2, 3, 3, 0, 21, 1, 24, 28, 17, 18, 17, 12, 6, 22, 6, 11, 28, 22, 11, 2, 19, 5, 4, 1, 28, 12, 23, 27, 24, 13, 19, 26, 1, 0, 20, 22, 22, 17, 15, 18, 26, 14, 6, 4, 24, 12, 14, 14, 15, 18, 20, 1, 11, 9, 6, 15, 13, 15]

# GP Mapping (for input parsing)
GP_LIST = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
val_map = {r: i for i, r in enumerate(GP_LIST)}

def to_ints_force_single(text):
    single_gp = {k: v for k, v in val_map.items() if len(k) == 1}
    res = []
    for char in text:
        if char in single_gp:
            res.append(single_gp[char])
    return res

stream_ints = to_ints_force_single(stream_runes)

# Calc Result
result_ints = []
for k in range(len(key_p24)):
    idx = k * 2
    if idx+1 >= len(stream_ints): break
    val_pair = (stream_ints[idx] + stream_ints[idx+1]) % 29
    plain = (val_pair - key_p24[k]) % 29
    result_ints.append(plain)

print(f"{'Idx':<4} | {'Val':<3} | {'Rune':<4} | {'Name':<8} | {'Sound':<6} | {'Context'}")
print("-" * 50)

context_buf = ""
for i, val in enumerate(result_ints):
    rune, name, sound = GP_DATA[val]
    # Build a small sliding window context
    ctx = "".join([GP_DATA[x][0] for x in result_ints[max(0, i-2):min(len(result_ints), i+3)]])
    print(f"{i:<4} | {val:<3} | {rune:<4} | {name:<8} | {sound:<6} | {ctx}")

print("\nFull Plaintext Runes:")
print("".join([GP_DATA[x][0] for x in result_ints]))

print("\nFull Plaintext Sounds:")
print("".join([GP_DATA[x][2] for x in result_ints]))

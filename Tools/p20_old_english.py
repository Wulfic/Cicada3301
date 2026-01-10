"""
Page 20 - Old English Interpretation
=====================================
The decoded text contains Old English words like EODE, SEFA
Let's interpret this as potential Anglo-Saxon text
"""

# The 2x83 reading
TEXT = "HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW"

print("Old English Interpretation Analysis")
print("=" * 50)

# Old English dictionary (common words from Deor and other poems)
OLD_ENGLISH = {
    'EODE': 'went, departed',
    'SEFA': 'heart, mind, spirit',
    'MOD': 'mind, courage, spirit',
    'MEOD': 'mead (drink)',
    'DREAG': 'suffered, endured',
    'OFEREODE': 'passed over, ended',
    'WRAECE': 'exile, misery',
    'LONGATH': 'longing',
    'SORGE': 'sorrow, grief',
    'WYRD': 'fate, destiny',
    'SAWOL': 'soul',
    'WITA': 'wise one',
    'EORL': 'nobleman, warrior',
    'THANE': 'servant, warrior',
    'CYNING': 'king',
    'HLAFORD': 'lord',
    'FREOND': 'friend',
    'FEOND': 'enemy, fiend',
    'GAST': 'spirit, ghost',
    'HEOFON': 'heaven',
    'FOLC': 'people, folk',
    'LICHAMA': 'body',
    'SAWLE': 'soul',
    'HEORTE': 'heart',
    'EAGE': 'eye',
    'EARE': 'ear',
    'MUTHA': 'mouth',
    'TUNGE': 'tongue',
    'HAND': 'hand',
    'FOT': 'foot',
    'HEAFOD': 'head',
    'BREOST': 'breast',
    # Common Old English words
    'IC': 'I',
    'HE': 'he',
    'HIM': 'him',
    'HIS': 'his',
    'SE': 'the (masc.)',
    'SEO': 'the (fem.)',
    'THAET': 'that, the (neut.)',
    'ON': 'in, on',
    'IN': 'in',
    'MID': 'with',
    'FOR': 'for, before',
    'OFT': 'often',
    'NE': 'not',
    'AC': 'but',
    'OND': 'and',
    'SWATHE': 'such',
    'HU': 'how',
    'THAS': 'this',
    'WEARD': 'guardian, became',
    'WAES': 'was',
    'WEARTH': 'became',
    'MOSTE': 'must',
    'SCEOLDE': 'should',
    'WOLDE': 'would',
    # From Deor specifically
    'THISSES': 'this (gen.)',
    'SWA': 'so, thus',
    'MAEG': 'may, can',
    'THAES': 'of that',
}

print("\n=== IDENTIFIED OLD ENGLISH WORDS ===")

for oe_word, meaning in OLD_ENGLISH.items():
    if oe_word in TEXT:
        idx = TEXT.find(oe_word)
        context = TEXT[max(0, idx-5):min(len(TEXT), idx+len(oe_word)+5)]
        print(f"  {oe_word} = '{meaning}' at position {idx}")
        print(f"    Context: ...{context}...")

# Now let's try a parse with Old English in mind
print("\n=== OLD ENGLISH PARSE ATTEMPT ===")

# Replace runeglish digraphs with single characters for easier processing
digraph_map = {'TH': 'þ', 'EO': 'ę', 'NG': 'ŋ', 'OE': 'œ', 'AE': 'æ', 'EA': 'ą', 'IA': 'ɨ'}

def to_digraph_text(text):
    """Convert text showing digraphs"""
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in ['TH', 'EO', 'NG', 'OE', 'AE', 'EA', 'IA']:
            result.append('[' + text[i:i+2] + ']')
            i += 2
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

print(f"With digraphs marked: {to_digraph_text(TEXT[:80])}")

# Manual parse with Old English words
print("\n=== POTENTIAL READING ===")

# Key phrase found: "EODE" (went) + "SEFA" (heart/mind)
# "MET" "BID" "AM" are modern English too
# "THE LONE" is clear
# "HER" could be OE "here" or modern "her"

potential_parse = """
Potential Old English reading:

H FO FEE EODE O MET BID AM SEFA LT THE LONE TN HER ...

Interpreted:
- FEE: possibly "fea" = few, or payment
- EODE: went, departed (OE)
- MET: met, encountered
- BID: asked, commanded  
- AM: I am
- SEFA: heart, mind, spirit (OE)
- THE LONE: the lone one, the solitary
- HER: her/here

Possible meaning: "Few departed, I met [and] commanded [my] heart/mind, the lone one here..."

This could be a poetic statement about a spiritual journey or meditation.
"""
print(potential_parse)

# Check if this matches Cicada's thematic style
print("\n=== THEMATIC ANALYSIS ===")

cicada_themes = [
    "THE LONE" - "solitary seeker of truth",
    "SEFA" - "mind/heart - self-knowledge", 
    "EODE" - "journey, departure",
    "HER" - "the feminine, wisdom personified",
]

print("Matches Cicada 3301 themes:")
print("- 'THE LONE' = the solitary seeker motif")
print("- 'SEFA' (heart/mind) = self-knowledge, consciousness")
print("- 'EODE' (went/departed) = journey, initiation")
print("- Mixed Old/Modern English = Cicada's Anglo-Saxon style")

# Check the Deor poem's refrain for comparison
print("\n=== DEOR POEM REFRAIN ===")
print("Þæs ofereode, þisses swa mæg")
print("(That passed over, so may this)")
print("\nThis refrain about overcoming hardship matches the 'LONE' seeker theme")

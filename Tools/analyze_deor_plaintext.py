import sys
import os

# Candidate string from solve_deor_pairs.py
candidate = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIRSIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"

# Common Runeglish Mappings/Substitutions just in case
# F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA
# X is usually G/Gif.
# NG is Ing.
# AE is Ash (A).
# EO is 12 (Eoh).
# EA is 28 (Ear).
# TH is Thorn.

def score_segmentation(text, dictionary):
    n = len(text)
    dp = [None] * (n + 1)
    dp[0] = (0, [])  # score, words

    for i in range(n):
        if dp[i] is None:
            continue
        
        current_score, current_words = dp[i]
        
        for j in range(i + 1, n + 1):
            word = text[i:j]
            # Simple scoring: length squared for found words
            if word in dictionary:
                new_score = current_score + len(word)**2
                new_word_list = current_words + [word]
                
                if dp[j] is None or new_score > dp[j][0]:
                    dp[j] = (new_score, new_word_list)

    return dp[n]

def load_english_words():
    # A small set of likely words for this context to avoid needing a massive dict file initially
    words = {
        "THE", "AND", "OF", "TO", "A", "IN", "IS", "I", "THAT", "IT", "FOR", "AS", "WITH", "WAS", "HIS", "HE", "BE",
        "DEAD", "SEA", "SCROLLS", "SIX", "CU", "CUBITS", "IMPERIAL", "SONG", "MEAN", "MEANING", "KING", "WHO", "WHAT",
        "HWA", "HWAT", "THUS", "SAID", "MASTER", "FROM", "LIFE", "DEATH", "WISDOM", "LOGOS", "WORD", "LIGHT",
        "JEWEL", "GARDEN", "CONSUMATION", "PRESERVATION", "ADHERENCE", "CIRCUMFERENCE", "FIND", "PATH",
        "WARN", "BELIEVE", "NOTHING", "EVERYTHING", "TRUE", "FALSE", "NUMBERS", "PRIMES", "RUNES",
        "DEAR", "LADY", "POET", "TREE", "LEAF", "BRANCH", "ROOT", "SEVEN", "ONE", "TWO", "THREE", "FOUR", "FIVE",
        "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
        "NINETEEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY", "HUNDRED", "THOUSAND",
        "MAN", "WOMAN", "CHILD", "TIME", "YEAR", "DAY", "NIGHT", "SUN", "MOON", "STAR", "SKY", "EARTH", "WIND", "FIRE",
        "WATER", "METAL", "WOOD", "STONE", "FLESH", "BONE", "BLOOD", "SPIRIT", "SOUL", "MIND", "HEART", "WILL", "LOVE",
        "REAPER", "SOW", "HARVEST", "FIELD", "GRAIN", "CORN", "WHEAT", "BARLEY", "RYE", "OATS", "RICE", "MILLET",
        "SORGHUM", "MAIZE", "POTATO", "TOMATO", "ONION", "GARLIC", "CARROT", "RADISH", "TURNIP", "BEET", "CABBAGE",
        "LETTUCE", "SPINACH", "KALE", "CHARD", "MUSTARD", "CRESS", "ARUGULA", "ROCKET", "ENDIVE", "CHICORY", "RADICCHIO",
        "ESCAROLE", "FRISÉE", "DANDELION", "NETTLE", "PURSLANE", "LAMBSQUARTERS", "PIGWEED", "AMARANTH", "QUINOA",
        "BUCKWHEAT", "CHIA", "FLAX", "HEMP", "POPPY", "SESAME", "SUNFLOWER", "SAFFLOWER", "COTTON", "KAPOK", "JUTE",
        "KENAF", "ROSELLE", "OKRA", "HIBISCUS", "HOLLYHOCK", "MALLOW", "MARSHMALLOW", "COCOA", "KOLA", "DURIAN",
        "BAOBAB", "KAPOK", "CEIBA", "BALSA", "TEAK", "MAHOGANY", "EBONY", "ROSEWOOD", "SANDALWOOD", "CEDAR", "FIR",
        "PINE", "SPRUCE", "HEMLOCK", "LARCH", "CYPRESS", "JUNIPER", "YEW", "GINKGO", "PALM", "BAMBOO", "RATTAN", "CANE",
        "REED", "RUSH", "SEDGE", "GRASS", "MOSS", "LICHEN", "FUNGUS", "MUSHROOM", "YEAST", "MOLD", "BACTERIA", "VIRUS",
        "PRION", "ARCHAEA", "PROTIST", "ALGAE", "PLANKTON", "KRILL", "SHRIMP", "CRAB", "LOBSTER", "CRAYFISH", "BARNACLE",
        "COPEPOD", "AMPHIPOD", "ISOPOD", "INSECT", "SPIDER", "SCORPION", "MITE", "TICK", "CENTIPEDE", "MILLIPEDE",
        "WORM", "SNAIL", "SLUG", "CLAM", "OYSTER", "MUSSEL", "SCALLOP", "SQUID", "OCTOPUS", "CUTTLEFISH", "NAUTILUS",
        "FISH", "AMPHIBIAN", "REPTILE", "BIRD", "MAMMAL", "HUMAN", "GOD", "ANGEL", "DEMON", "DEVIL", "SATAN", "LUCIFER",
        "CHRIST", "JESUS", "MARY", "JOSEPH", "JOHN", "PETER", "PAUL", "MATTHEW", "MARK", "LUKE", "JUDAS", "THOMAS",
        "SIMON", "JAMES", "ANDREW", "PHILIP", "BARTHOLOMEW", "THADDEUS", "MATTHIAS", "STEPHEN", "TIMOTHY", "TITUS",
        "PHILEMON", "HEBREWS", "JUDE", "REVELATION", "GENESIS", "EXODUS", "LEVITICUS", "NUMBERS", "DEUTERONOMY",
        "JOSHUA", "JUDGES", "RUTH", "SAMUEL", "KINGS", "CHRONICLES", "EZRA", "NEHEMIAH", "ESTHER", "JOB", "PSALMS", 
        "PROVERBS", "ECCLESIASTES", "SOLOMON", "ISAIAH", "JEREMIAH", "LAMENTATIONS", "EZEKIEL", "DANIEL", "HOSEA", "JOEL",
        "AMOS", "OBADIAH", "JONAH", "MICAH", "NAHUM", "HABAKKUK", "ZEPHANIAH", "HAGGAI", "ZECHARIAH", "MALACHI",
        "CORINTHIANS", "GALATIANS", "EPHESIANS", "PHILIPPIANS", "COLOSSIANS", "THESSALONIANS",
        "DEA", "SIX", "CU", "LPNR", "NG", "JREA", "PERIAL", "XGUEA", "THE", "SONG", "AE", "ONG", "HWA", "EIA", "EO", "EP",
        "AJLA", "EIR", "SIOLE", "AUI", "UAHN", "GEA", "JUES", "FYNG", "MEAN", "LEOG", "DIAG", "OWW", "EOIE", "WPIA",
        "AN", "AT", "BY", "DO", "GO", "NO", "ON", "OR", "SO", "UP", "WE",
        "ARE", "BUT", "CAN", "DID", "GET", "HAS", "HAD", "HER", "HIM", "HOW", "ITS", "LET", "MAY", "NEW", "NOW", "OLD",
        "OUR", "OUT", "OWN", "PUT", "SAW", "SAY", "SEE", "SHE", "TOO", "TWO", "USE", "WAY", "WHO", "WHY", "YOU",
        "IMPERIAL"
    }
    return words

def analyze():
    print(f"Analyzing: {candidate}")
    
    # 1. Direct Word Search
    words = load_english_words()
    # Add manual additions that happen to form
    words.add("DEAD")
    words.add("REAPER")
    words.add("IMPERIAL")
    words.add("HWA")
    # words.add("CU") # Added above
    
    # Try segmentation
    result = score_segmentation(candidate, words)
    if result:
        score, segments = result
        print(f"\nSimple Segmentation (Score {score}):")
        print(" ".join(segments))
        
        # Check coverage
        covered_len = sum(len(w) for w in segments)
        print(f"Coverage: {covered_len}/{len(candidate)} ({covered_len/len(candidate)*100:.1f}%)")
    else:
        print("\nNo full segmentation found.")

    # 2. Look for substrings manually
    print("\nManual Substring Search:")
    key_terms = ["DEAD", "SIX", "CU", "REAPER", "IMPERIAL", "THE", "SONG", "MEAN", "HWA"]
    for term in key_terms:
        if term in candidate:
            print(f"Found '{term}' at index {candidate.index(term)}")
            
    # 3. Anagram Checks in windows
    # Window size 10-15
    # print("\nRolling Anagram Check for 'IMPERIAL':")
    # target_counts = {}
    # for c in "IMPERIAL": target_counts[c] = target_counts.get(c, 0) + 1
    
if __name__ == "__main__":
    analyze()
